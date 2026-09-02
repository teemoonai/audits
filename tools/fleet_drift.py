#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""fleet_drift.py — is what near.ai is running still what this repo has reviewed?

Every page in this repo is a point-in-time claim about a configuration nobody is
watching. A verdict reads "PRIVATE at deployed flags"; the flags are in a compose
file that can be redeployed any day. This script closes that gap: it fetches the
live attestation from every host in near.ai's public directory, extracts the
identities the teemoon app would build audit links from, and diffs them against
index.json.

It answers three questions:

  1. UNAUDITED  — something in-scope is running that has no page. New links are
                  missing; users on that host see no audit where they should.
  2. UNOBSERVED — a page exists for an identity no longer seen live. Not an
                  error (node lotteries mean identities come and go), but if it
                  stays unobserved for a long time the page is describing
                  history rather than production.
  3. BROKEN     — the index gates a link whose page is absent, or a page that
                  carries no verdict. Both are contract violations.

Deterministic, stdlib only, no API keys, no LLM. Seconds to run. It never writes
to the repo and never publishes anything — it reports, and a human decides.

SCOPE. It mirrors the repo's scope rule (README) and the app's own classifier
(`PlaintextExposure.swift`): an artifact is in scope iff, per the attested
manifests, it can reach plaintext — directly (it decrypts or computes on
messages), by capability (docker socket / host pid / SYS_PTRACE / SYS_ADMIN /
container-log mounts), or as the substrate (the guest OS). Ciphertext-side
plumbing (nginx, certbot, curl, uv) is deliberately not reported, so a drift
alert always means something that matters.

INTEGRITY. Every measured compose is checked with sha256(app_compose) ==
info.compose_hash — the value sealed into the TDX quote — before anything is
extracted from it. Every model-layer recipe is fetched at the commit the signed
action log pins and hash-checked against that log's file_sha256. A mismatch is
reported as an integrity break, never silently skipped.

EXIT CODES
  0  no drift: everything in-scope and live has a page, and the index is intact
  1  drift: at least one in-scope identity is running unaudited
  2  inconclusive: hosts unreachable, an integrity check failed, or the index is
     internally broken — nothing may be concluded about coverage

Usage:
  python3 tools/fleet_drift.py                 # human-readable report
  python3 tools/fleet_drift.py --json out.json # machine-readable, for CI
  python3 tools/fleet_drift.py --samples 5     # LB'd hosts serve different CVMs
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

ENDPOINTS = "https://completions.near.ai/endpoints"
COMPOSE_REPO = "nearai/cvm-compose-files"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, timeout=60):
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 0, str(e).encode()


# ---------------------------------------------------------------- path spec

def normalized_ref(image):
    """docker-ref normalization — mirrors AuditIndex.normalizedRef exactly."""
    ref = image
    colon = ref.rfind(":")
    if colon > 0 and "/" not in ref[colon:]:
        ref = ref[:colon]
    first = ref.split("/")[0]
    if not ("." in first or ":" in first):
        ref = ("docker.io/" + ref) if "/" in ref else ("docker.io/library/" + ref)
    return ref


# ------------------------------------------------------------ compose parse

def compose_yaml(text):
    """Unwrap the dstack manifest JSON when that is what we were handed."""
    t = text.strip()
    if t.startswith("{") and '"docker_compose_file"' in t:
        try:
            return json.loads(text)["docker_compose_file"]
        except Exception:
            return text
    return text


def anchor_blocks(yaml):
    out, lines = {}, yaml.split("\n")
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#"):
            continue
        m = re.search(r"&([A-Za-z0-9_\-]+)", line)
        if not m:
            continue
        indent = len(line) - len(line.lstrip(" "))
        block, j = [line], i + 1
        while j < len(lines):
            nxt = lines[j]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip(" "))) <= indent:
                break
            block.append(nxt)
            j += 1
        out[m.group(1)] = "\n".join(block)
    return out


def service_blocks(yaml):
    lines = [l for l in yaml.split("\n") if not l.lstrip().startswith("#")]
    blocks, i = [], 0
    while i < len(lines):
        if re.match(r"^\s*services:\s*$", lines[i]):
            base = len(lines[i]) - len(lines[i].lstrip(" "))
            j, child_indent, cur = i + 1, None, None
            while j < len(lines):
                l = lines[j]
                if l.strip():
                    ind = len(l) - len(l.lstrip(" "))
                    if ind <= base:
                        break
                    if child_indent is None:
                        child_indent = ind
                    if ind == child_indent and l.rstrip().endswith(":"):
                        if cur:
                            blocks.append("\n".join(cur))
                        cur = [l]
                    elif cur is not None:
                        cur.append(l)
                elif cur is not None:
                    cur.append(l)
                j += 1
            if cur:
                blocks.append("\n".join(cur))
            i = j
        else:
            i += 1
    return blocks


def expand(block, anchors):
    # Transitive: a service may alias an `x-*` anchor whose body aliases
    # another (`<<: *engine-common` -> `build: *engine-build`). One level
    # missed the `FROM` of every in-enclave build on the GLM-5.3 node.
    text, seen, todo = block, set(), re.findall(r"\*([A-Za-z0-9_\-]+)", block)
    while todo:
        name = todo.pop()
        if name in seen or name not in anchors:
            continue
        seen.add(name)
        text += "\n" + anchors[name]
        todo += re.findall(r"\*([A-Za-z0-9_\-]+)", anchors[name])
    return text


def block_image(block):
    m = re.search(r"^\s*image:\s*[\"']?([^\s\"'#]+)", block, re.M)
    if not m:
        return None
    img = m.group(1)
    d = re.search(r"\$\{[A-Za-z0-9_]+:-([^}]+)\}", img)   # ${VAR:-default}
    return d.group(1) if d else img


# ------------------------------------------------- in-scope classification
# Mirrors PlaintextExposure.swift. Kept deliberately close to the Swift so the
# two can be compared line by line when either changes.

def sig_terminator(b):
    u = b.upper()
    return "OHTTP_ENABLED" in u or "TLS_CERT" in u


def sig_model_server(b):
    l = b.lower()
    return ("launch_server" in l or "--model-path" in l or "vllm serve" in l
            or "vllm/vllm-openai" in l or "lmsysorg/sglang" in l)


def sig_process(b):
    l = b.lower()
    return "docker.sock" in l or "pid: host" in l


def sig_log(b):
    l = b.lower()
    return "/var/lib/docker/containers" in l or "/run/log/journal" in l


def sig_device(b):
    l = b.lower()
    if "privileged: true" in l or "sys_admin" in l:
        return True
    return "runtime: nvidia" in l and ("driver: nvidia" in l or "capabilities: [gpu]" in l or "devices:" in l)


def backend_service_names(yaml, anchors):
    """Containers a terminator forwards decrypted requests to — the data path
    stated by the component holding the plaintext. Catches engines whose image
    name says nothing (the `model-privacy-filter` case)."""
    names = set()
    for raw in service_blocks(yaml):
        b = expand(raw, anchors)
        if not sig_terminator(b):
            continue
        for line in b.split("\n"):
            s = line.strip(" -\"'")
            if not (s.startswith("VLLM_BASE_URL=") or s.startswith("VLLM_BACKEND_URLS=")):
                continue
            for url in s.split("=", 1)[1].split(","):
                h = url.strip(" \"'")
                if "://" in h:
                    h = h.split("://", 1)[1]
                h = h.split(":")[0].split("/")[0]
                if h:
                    names.add(h)
    return names


def parse_looks_degenerate(yaml, blocks):
    """Guard against the dangerous failure direction.

    This file parses compose YAML with an indent-and-regex approximation rather
    than a real YAML library. That is deliberate (see the note at the bottom of
    this file), but it means a compose using YAML this parser mishandles would
    yield too FEW service blocks -- and an in-scope image would be silently
    missed. A false positive is noise; a false negative is an audit tool quietly
    under-reporting, which is worse than no tool.

    So cross-check the structural parse against a dumb independent count of
    `image:` keys. If the block parser found materially fewer services than there
    are images, the parse is not trustworthy and the caller must say so out loud
    rather than return a short list that looks like an answer.
    """
    images = len(re.findall(r"^\s*image:\s*\S", yaml, re.M))
    return images > 0 and len(blocks) < images / 2


def in_scope_images(doc):
    """-> ({verbatim image ref: role}, [parse warnings])"""
    yaml = compose_yaml(doc)
    anchors = anchor_blocks(yaml)
    backends = backend_service_names(yaml, anchors)
    blocks = service_blocks(yaml)
    warnings = []
    if parse_looks_degenerate(yaml, blocks):
        warnings.append(
            f"compose parse looks degenerate: {len(blocks)} service block(s) for "
            f"{len(re.findall(r'^\s*image:\s*\S', yaml, re.M))} image key(s) — "
            f"in-scope images may be MISSING from this run")
    out = {}
    for raw in blocks:
        b = expand(raw, anchors)
        img = block_image(b)
        if not img:
            continue
        name = raw.split("\n")[0].strip().rstrip(":")
        cname = re.search(r"^\s*container_name:\s*[\"']?([^\s\"']+)", b, re.M)
        is_backend = name in backends or (cname and cname.group(1) in backends)
        if sig_terminator(b):
            role = "e2ee-terminator"
        elif sig_model_server(b) or is_backend:
            role = "model-server"
        elif sig_process(b):
            role = "process-access"
        elif sig_device(b):
            role = "device-privilege"
        elif sig_log(b):
            role = "log-access"
        else:
            continue                      # ciphertext-side: deliberately silent
        # An in-enclave build has no registry identity of its own: the running
        # bytes are `<name>:local`, and its provenance and audit live on the
        # base it builds FROM. Reporting the local name would be permanent
        # noise -- there can never be a page for `sglang-diffusion`. So resolve
        # to the base; if the FROM cannot be parsed, say exactly that rather
        # than inventing an identity.
        if re.search(r"^\s*build:", b, re.M):
            m = re.search(r"FROM\s+(\S+)", b)
            if m:
                out.setdefault(m.group(1), role + " (in-enclave build base)")
            else:
                out.setdefault(f"{name} (in-enclave build, FROM unresolved)", role)
            continue
        out.setdefault(img, role)
    return out, warnings


# --------------------------------------------------------------- the sweep

def sample_host(domain):
    nonce = hashlib.sha256(os.urandom(32)).hexdigest()
    st, body = get(f"https://{domain}/v1/attestation/report?nonce={nonce}&signing_algo=ecdsa")
    if st != 200:
        return {"host": domain, "error": f"attestation HTTP {st}"}
    try:
        rep = json.loads(body)
    except Exception as e:
        return {"host": domain, "error": f"undecodable report: {e}"}

    info = rep.get("info") or {}
    tcb = info.get("tcb_info") or {}
    out = {"host": domain, "model": rep.get("model_name"), "images": {},
           "compose_hash": info.get("compose_hash"), "os": info.get("os_image_hash"),
           "recipe": None, "integrity": []}

    outer = tcb.get("app_compose") or ""
    if not outer:
        out["integrity"].append("report carries no info.tcb_info.app_compose")
    elif hashlib.sha256(outer.encode()).hexdigest() != (info.get("compose_hash") or ""):
        out["integrity"].append("sha256(app_compose) != info.compose_hash — the manifest is not the measured one")
    else:
        imgs, warns = in_scope_images(outer)
        out["images"].update(imgs)
        out["integrity"] += [f"outer compose: {w}" for w in warns]

    acts = ((rep.get("compose_manager_attestation") or {}).get("actions")) or []
    ups = [a for a in acts if a.get("action") == "compose_up"]
    if not ups:
        out["integrity"].append("no compose_up in the signed action log — model layer UNCHECKED")
        return out
    up = ups[-1]
    path, commit, want = up.get("file"), up.get("commit"), (up.get("file_sha256") or "").lower()
    st, yb = get(f"https://raw.githubusercontent.com/{COMPOSE_REPO}/{commit}/{path}")
    if st != 200:
        out["integrity"].append(f"could not fetch {path}@{commit[:12]} (HTTP {st}) — model layer UNCHECKED")
        return out
    got = hashlib.sha256(yb).hexdigest()
    if got != want:
        out["integrity"].append(
            f"{path}@{commit[:12]} hashes {got[:12]} but the action log pins {want[:12]} — INTEGRITY BREAK")
        return out
    out["recipe"] = (path, want)
    imgs, warns = in_scope_images(yb.decode("utf-8", "replace"))
    out["images"].update(imgs)
    out["integrity"] += [f"recipe {path}: {w}" for w in warns]
    return out


# --------------------------------------------------------------- the diff

def load_acknowledged():
    """Known-open items: reported, but not counted as drift. Without this a
    single permanent gap keeps the check red forever and the signal dies."""
    try:
        with open(os.path.join(REPO_ROOT, "acknowledged.json")) as f:
            return {a["id"]: a for a in json.load(f).get("acknowledged", [])}
    except Exception:
        return {}


def load_index():
    with open(os.path.join(REPO_ROOT, "index.json")) as f:
        return json.load(f)


def audited_image(idx, ref_verbatim):
    m = re.match(r"^([A-Za-z0-9._/\-]+?)(?::[A-Za-z0-9._\-]+)?@sha256:([0-9a-f]{64})$", ref_verbatim)
    if m:
        return m.group(2) in (idx.get("images") or {}).get(normalized_ref(m.group(1)), [])
    nref = normalized_ref(ref_verbatim)
    last = ref_verbatim.split("/")[-1]
    tag = last.split(":")[1] if ":" in last else "latest"
    return tag in (idx.get("tagAudits") or {}).get(nref, [])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--samples", type=int, default=3,
                    help="requests per host; load-balanced hosts serve different CVMs (default 3)")
    ap.add_argument("--json", metavar="PATH", help="also write a machine-readable report")
    args = ap.parse_args()

    idx = load_index()
    st, b = get(ENDPOINTS)
    if st != 200:
        print(f"FATAL: endpoint directory HTTP {st} — cannot enumerate the fleet")
        return 2
    eps = json.loads(b)
    eps = eps["endpoints"] if isinstance(eps, dict) else eps
    domains = [e["domain"] for e in eps]

    jobs = [d for d in domains for _ in range(args.samples)]
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(sample_host, jobs))

    live_images, live_measured, live_os, live_recipes = defaultdict(set), defaultdict(set), defaultdict(set), defaultdict(set)
    unreachable, integrity = defaultdict(set), []
    for r in results:
        host = r["host"].split(".")[0]
        if r.get("error"):
            unreachable[host].add(r["error"])
            continue
        for note in r["integrity"]:
            integrity.append((host, note))
        for img, role in r["images"].items():
            live_images[(img, role)].add(host)
        if r["compose_hash"]:
            live_measured[r["compose_hash"]].add(host)
        if r["os"]:
            live_os[r["os"]].add(host)
        if r["recipe"]:
            live_recipes[r["recipe"]].add(host)

    ack = load_acknowledged()
    unaudited, unobserved, broken, known = [], [], [], []

    for (img, role), hosts in sorted(live_images.items()):
        if not audited_image(idx, img):
            entry = {"kind": "image", "id": img, "role": role, "hosts": sorted(hosts)}
            (known if img in ack else unaudited).append(entry)
    for h, hosts in live_measured.items():
        if h not in (idx.get("measured") or []):
            unaudited.append({"kind": "measured", "id": h, "role": "deployment config", "hosts": sorted(hosts)})
    for h, hosts in live_os.items():
        if h not in (idx.get("os") or []):
            unaudited.append({"kind": "os", "id": h, "role": "guest OS", "hosts": sorted(hosts)})
    for (path, sha), hosts in live_recipes.items():
        key = f"{COMPOSE_REPO}/{path}"
        if sha not in (idx.get("manifests") or {}).get(key, []):
            unaudited.append({"kind": "recipe", "id": f"{path} {sha}", "role": "model-layer recipe", "hosts": sorted(hosts)})

    live_img_ids = {i for i, _ in live_images}
    for ref, digests in (idx.get("images") or {}).items():
        for d in digests:
            if not any(f"@sha256:{d}" in i for i in live_img_ids):
                unobserved.append(f"{ref}@sha256:{d[:12]}")
    for h in (idx.get("measured") or []):
        if h not in live_measured:
            unobserved.append(f"measured {h[:12]}")
    for key, shas in (idx.get("manifests") or {}).items():
        for s in shas:
            if not any(s == sha for _, sha in live_recipes):
                unobserved.append(f"recipe {key.split('/')[-1]} {s[:12]}")

    # index self-consistency: every gated link must have a page, and a verdict
    verdicts = idx.get("verdicts") or {}
    built = [f"images/{r}/sha256-{d}.md" for r, ds in (idx.get("images") or {}).items() for d in ds]
    built += [f"images/{r}/tag-{t}.md" for r, ts in (idx.get("tagAudits") or {}).items() for t in ts]
    built += [f"manifests/{(k[:-5] if k.endswith('.yaml') else k)}/sha256-{s}.md"
              for k, ss in (idx.get("manifests") or {}).items() for s in ss]
    built += [f"manifests/measured/sha256-{m}.md" for m in (idx.get("measured") or [])]
    built += [f"os/sha256-{o}.md" for o in (idx.get("os") or [])]
    for p in built:
        if not os.path.exists(os.path.join(REPO_ROOT, p)):
            broken.append(f"index gates a link with no page on disk: {p}")
        elif p not in verdicts:
            broken.append(f"page has no verdict recorded (client must fall back to neutral copy): {p}")

    # ---- report
    W = 78
    print("=" * W)
    print(f"fleet drift — {len(domains)} hosts advertised, {args.samples} sample(s) each")
    print("=" * W)
    if unreachable:
        print("\nADVERTISED BUT NOT SERVING (not a coverage gap):")
        for h, errs in sorted(unreachable.items()):
            print(f"  {h}: {sorted(errs)[0]}")
    if integrity:
        print("\n!! INTEGRITY — nothing may be concluded about these hosts:")
        for h, note in integrity:
            print(f"  {h}: {note}")
    print(f"\nUNAUDITED — in scope, running, no page  ({len(unaudited)})")
    for u in unaudited or [None]:
        if u is None:
            print("  none")
            continue
        hosts = sorted(u["hosts"])
        # Cap the line, but say so — a bare [:6] under a count of 7 reads as a
        # bug in the counter. The full list is always in --json.
        more = f" (+{len(hosts) - 6} more)" if len(hosts) > 6 else ""
        print(f"  [{u['kind']:<8}] {u['role']:<26} {u['id'][:64]}")
        print(f"{'':14}on {len(hosts)} host(s): {', '.join(hosts[:6])}{more}")
    if known:
        print(f"\nKNOWN OPEN — acknowledged, not counted as drift  ({len(known)})")
        for k in known:
            print(f"  [{k['kind']:<8}] {k['role']:<26} {k['id'][:64]}")
            print(f"{'':14}since {ack[k['id']].get('since','?')} — {ack[k['id']].get('reason','')[:96]}")
    print(f"\nUNOBSERVED — page exists, not seen live  ({len(unobserved)})")
    print("  none" if not unobserved else "  " + "\n  ".join(sorted(unobserved)))
    print(f"\nINDEX INTEGRITY  ({len(broken)})")
    print("  ok" if not broken else "  " + "\n  ".join(broken))

    if args.json:
        with open(args.json, "w") as f:
            json.dump({"hosts": len(domains), "samples": args.samples,
                       "unreachable": {k: sorted(v) for k, v in unreachable.items()},
                       "integrity": [{"host": h, "note": n} for h, n in integrity],
                       "unaudited": unaudited, "known_open": known,
                       "unobserved": sorted(unobserved),
                       "broken": broken}, f, indent=2)

    if integrity or broken or len(unreachable) == len(domains):
        return 2
    return 1 if unaudited else 0


if __name__ == "__main__":
    sys.exit(main())


# ---------------------------------------------------------------------------
# WHY THIS IS PYTHON, AND WHY IT DOES NOT USE A REAL YAML PARSER
#
# The obvious objection: a proper YAML library (or Go with gopkg.in/yaml.v3)
# would parse these composes correctly, and this file approximates YAML with
# indentation rules and regexes. That objection is right about YAML and wrong
# about the job.
#
# What this check must answer is not "what does this compose mean" but "what
# would the teemoon app conclude from this compose". The app classifies scope in
# PlaintextExposure.swift using exactly this approximation: textual anchor
# expansion, indent-delimited service blocks, regex signals. If this checker used
# a real YAML parser it would be MORE correct and LESS useful -- it would diverge
# from the client whose behaviour it exists to verify, and report in-scope images
# the app renders untagged, or miss ones it tags. Fidelity to the app is the
# requirement; YAML correctness is not.
#
# Two secondary reasons to stay on stdlib Python:
#   - Zero dependencies. This is an audit repo; its own tooling having a supply
#     chain would be a poor look, and a CI job that installs nothing cannot be
#     compromised through what it installs. Neither PyYAML nor a Go module tree
#     is free here.
#   - The likely growth direction is the checks Fable proposed in the 2026-08-03
#     method review: route/auth conformance, redaction conformance, repr
#     conformance. Those parse Python ASTs, which is native here and awkward in
#     Go.
#
# The real risk of the approximation is silent under-reporting, and that is what
# `parse_looks_degenerate` is for: it fails loud rather than returning a short
# list that looks like an answer.
#
# If PlaintextExposure.swift is ever rewritten against a real YAML parser, this
# file should follow it -- and at that point Go would be a reasonable choice.
