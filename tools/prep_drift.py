#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""prep_drift.py — do the deterministic half of a drift response before any model runs.

Step 0 of responding to a fleet-drift issue. Reviewing is expensive (80-240k
tokens a page); everything a reviewer needs handed to it is not. Each of the
things below was at some point rediscovered by hand, or by a reviewer on the
clock, and each has cost a run:

  - the issue body is a snapshot: the fleet has redeployed between the issue
    and the session more than once, and a review of a superseded hash is wasted
  - near.ai deploys with service-scoped `compose up`, so the recipe hash a host
    attests is the LAST file touched, not what every container was created from
  - a new revision of an audited file is a delta, and the diff is one command
  - one hostname can front two CVMs; three samples can miss one

So this script re-runs the sweep, says what moved since the issue, and for every
unaudited target writes the evidence to disk and prints a block to paste into
the reviewer brief:

  recipe    the file at the log-pinned commit (hash-checked), the audited base
            revision and the patch against it, a per-service table of which
            revision last created each container, the patch from each of those
            older revisions, and every in-scope image with its audit status
  image     delta or new, the base page, and resolve_identity.py --brief output
  measured  the measured compose (hash-checked) and its in-scope images
  os        the hash, and the hosts

It writes NOTHING in the repo, publishes nothing and judges nothing. It does not
choose a severity, a verdict or a reviewer. Evidence goes to --out (default: a
directory under the system temp dir), the compose-repo clone to --cache.

EXIT CODES
  0  no drift — nothing to commission
  1  drift — targets printed
  2  inconclusive — the sweep could not run or an integrity check failed; fix
     that first, commission nothing

Usage:
  python3 tools/prep_drift.py                      # sweep + briefs for every target
  python3 tools/prep_drift.py --issue 8            # also diff against that issue's list
  python3 tools/prep_drift.py --out DIR --samples 12

Stdlib only, plus `git` (for the compose-repo clone) and optionally `gh`.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fleet_drift as fd  # noqa: E402  — same scope rule, same parser, on purpose
import resolve_identity as ri  # noqa: E402

REPO_ROOT = fd.REPO_ROOT
TOOLS = os.path.dirname(os.path.abspath(__file__))


def sh(args, cwd=None, timeout=300):
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    except Exception as e:
        return 127, "", str(e)


# ------------------------------------------------------------ compose clone

def ensure_clone(cache):
    """A full clone of the compose repo: `git diff`, `git log` and every
    revision's bytes for the price of one fetch. Returns None if git fails —
    callers fall back to raw.githubusercontent.com."""
    path = os.path.join(cache, "cvm-compose-files")
    if os.path.isdir(os.path.join(path, ".git")):
        sh(["git", "fetch", "--quiet", "--tags", "origin"], cwd=path)
        return path
    os.makedirs(cache, exist_ok=True)
    rc, _, _ = sh(["git", "clone", "--quiet", f"https://github.com/{fd.COMPOSE_REPO}", path])
    return path if rc == 0 else None


def file_at(clone, commit, path):
    """Bytes of `path` at `commit`, or None. A commit on a deleted branch is not
    in a plain clone but can still be fetched by its full sha."""
    if clone:
        rc, _, _ = sh(["git", "cat-file", "-e", f"{commit}:{path}"], cwd=clone)
        if rc != 0:
            sh(["git", "fetch", "--quiet", "origin", commit], cwd=clone)
        p = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=clone, capture_output=True)
        if p.returncode == 0:
            return p.stdout
    st, body = fd.get(f"https://raw.githubusercontent.com/{fd.COMPOSE_REPO}/{commit}/{path}")
    return body if st == 200 else None


def revisions_of(clone, path):
    """[(file_sha256, commit)] newest first, for every commit that touched path."""
    if not clone:
        return []
    rc, out, _ = sh(["git", "log", "--all", "--format=%H", "--", path], cwd=clone)
    revs = []
    for c in out.split():
        p = subprocess.run(["git", "show", f"{c}:{path}"], cwd=clone, capture_output=True)
        if p.returncode == 0:
            revs.append((hashlib.sha256(p.stdout).hexdigest(), c))
    return revs


# ------------------------------------------------------------- live capture

def fetch_report(domain):
    nonce = hashlib.sha256(os.urandom(32)).hexdigest()
    st, body = fd.get(f"https://{domain}/v1/attestation/report?nonce={nonce}&signing_algo=ecdsa")
    if st != 200:
        return None
    try:
        return json.loads(body)
    except Exception:
        return None


def capture_cvms(domains, samples):
    """Sample every affected host `samples` times and collapse to distinct CVMs.
    Identity of a CVM here = (measured compose hash, action-log hash)."""
    jobs = [d for d in domains for _ in range(samples)]
    with ThreadPoolExecutor(max_workers=12) as ex:
        reports = list(ex.map(fetch_report, jobs))
    cvms = {}
    for d, rep in zip(jobs, reports):
        if not rep:
            continue
        info = rep.get("info") or {}
        cm = rep.get("compose_manager_attestation") or {}
        acts = cm.get("actions") or []
        key = (info.get("compose_hash") or "?",
               cm.get("actions_hash") or hashlib.sha256(json.dumps(acts, sort_keys=True).encode()).hexdigest())
        c = cvms.setdefault(key, {"hosts": set(), "actions": acts, "info": info,
                                  "compose_hash": key[0], "os": info.get("os_image_hash")})
        c["hosts"].add(d.split(".")[0])
        if len(acts) > len(c["actions"]):       # same CVM, log grew mid-capture
            c["actions"] = acts
    return list(cvms.values())


def service_names(text, default_only=False):
    """Service names in a compose file. `default_only` drops profile-gated
    services: a project-wide `up` does not start them, and listing them as
    running from that revision was wrong on the first run of this script."""
    yaml = fd.compose_yaml(text)
    anchors = fd.anchor_blocks(yaml)
    out = []
    for b in fd.service_blocks(yaml):
        if default_only and re.search(r"^\s*profiles:", fd.expand(b, anchors), re.M):
            continue
        out.append(b.split("\n")[0].strip().rstrip(":"))
    return out


def service_table(actions, content_of):
    """Which revision last (re)created each service. `services: []` on an entry
    means the whole file. Returns {service: entry}."""
    live = {}
    for a in actions:
        act = a.get("action")
        if act not in ("compose_up", "compose_down"):
            continue
        svcs = a.get("services") or []
        if act == "compose_down":
            for s in (svcs or [k for k, v in live.items() if v.get("file") == a.get("file")]):
                live.pop(s, None)
            continue
        if not svcs:
            body = content_of(a.get("commit"), a.get("file"))
            svcs = service_names(body.decode("utf-8", "replace"), default_only=True) if body else []
            if not svcs:
                svcs = [f"<all services of {a.get('file')} — file unavailable>"]
        for s in svcs:
            live[s] = a
    return live


# ------------------------------------------------------------------ helpers

def page_date(path):
    try:
        with open(os.path.join(REPO_ROOT, path)) as f:
            m = re.search(r"reviewed (\d{4}-\d{2}-\d{2})", f.read())
            return m.group(1) if m else ""
    except Exception:
        return ""


def unified(a, b, la, lb):
    return "".join(difflib.unified_diff(a.decode("utf-8", "replace").splitlines(True),
                                        b.decode("utf-8", "replace").splitlines(True), la, lb))


def patch_stat(patch):
    add = sum(1 for l in patch.split("\n") if l.startswith("+") and not l.startswith("+++"))
    rem = sum(1 for l in patch.split("\n") if l.startswith("-") and not l.startswith("---"))
    return patch.count("\n@@ ") + patch.startswith("@@ "), add, rem


def write(out, name, data):
    p = os.path.join(out, name)
    with open(p, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)
    return p


def image_status(idx, ref, target_ids):
    if fd.audited_image(idx, ref):
        return "audited"
    return "UNAUDITED — a target of this run" if ref in target_ids else "no page (out of scope, or see acknowledged.json)"


def issue_ids(number):
    """12-hex prefixes the issue's UNAUDITED section names. Best effort."""
    args = ["gh", "issue", "view", str(number), "--json", "body,number"] if number else \
           ["gh", "issue", "list", "--label", "fleet-drift", "--state", "open", "--limit", "1", "--json", "body,number"]
    rc, out, _ = sh(args, cwd=REPO_ROOT, timeout=60)
    if rc != 0:
        return None, None
    try:
        j = json.loads(out)
        j = j[0] if isinstance(j, list) else j
    except Exception:
        return None, None
    m = re.search(r"UNAUDITED.*?\n(.*?)\n\s*\n", j["body"], re.S)
    sect = m.group(1) if m else ""
    return j["number"], set(re.findall(r"\b([0-9a-f]{12})[0-9a-f]*\b", sect))


def short_id(t):
    m = re.search(r"([0-9a-f]{64})", t["id"])
    return m.group(1)[:12] if m else t["id"][:12]


# ------------------------------------------------------------ target briefs

def brief_recipe(t, cvms, idx, clone, out, target_ids):
    path, sha = t["id"].split(" ")
    key = f"{fd.COMPOSE_REPO}/{path}"
    stem = os.path.basename(path)[:-5] if path.endswith(".yaml") else os.path.basename(path)
    L = [f"page:     manifests/{key[:-5] if key.endswith('.yaml') else key}/sha256-{sha}.md",
         "method:   notes/method.md §4 — a DOCUMENT review, no upstream source reading"]
    cache = {}

    def content_of(commit, p):
        if (commit, p) not in cache:
            cache[(commit, p)] = file_at(clone, commit, p)
        return cache[(commit, p)]

    mine = [c for c in cvms if any(a.get("action") == "compose_up" and (a.get("file_sha256") or "").lower() == sha
                                   for a in c["actions"][-40:])]
    if not mine:
        L.append("!! no sampled CVM attests this hash any more — the fleet moved during the run; re-run")
        return L
    ups = [a for a in mine[0]["actions"] if a.get("action") == "compose_up" and (a.get("file_sha256") or "").lower() == sha]
    commit, tag = ups[-1].get("commit"), ups[-1].get("tag")
    new = content_of(commit, path)
    if new is None or hashlib.sha256(new).hexdigest() != sha:
        L.append(f"!! could not reproduce {sha[:12]} from {path}@{commit} — INTEGRITY, do not commission")
        return L
    new_file = write(out, f"{stem}@{sha[:12]}.yaml", new)
    declared = set(service_names(new.decode("utf-8", "replace")))
    L.append(f"identity: log-pinned — compose_up of {path} at {fd.COMPOSE_REPO} commit {commit} (tag {tag}),")
    L.append(f"          file_sha256 {sha} — fetched and re-hashed, match")
    L.append(f"file:     {new_file}  ({new.count(b'\n')} lines)")
    if clone:
        L.append(f"clone:    {clone}  (git show/diff/log work here; `git fetch origin <full sha>` for deleted-branch commits)")

    # --- base: the newest audited revision of this path; else the nearest audited sibling
    audited = (idx.get("manifests") or {}).get(key, [])
    revs = revisions_of(clone, path)
    by_sha = dict(reversed(revs))                      # sha -> newest commit carrying it
    for c in mine:
        for a in c["actions"]:
            if a.get("file") == path and a.get("file_sha256"):
                by_sha.setdefault(a["file_sha256"].lower(), a.get("commit"))
    base = None
    order = [s for s, _ in revs if s in audited] + sorted(
        (s for s in audited if s in by_sha), key=lambda s: page_date(f"manifests/{key[:-5]}/sha256-{s}.md"), reverse=True)
    for s in order:
        body = content_of(by_sha[s], path)
        if body is not None and hashlib.sha256(body).hexdigest() == s:
            base = (key, s, by_sha[s], body, "same file")
            break
    if base is None:
        best = None
        for k2, shas in (idx.get("manifests") or {}).items():
            p2 = k2[len(fd.COMPOSE_REPO) + 1:]
            for s2, c2 in revisions_of(clone, p2):
                if s2 in shas:
                    body = content_of(c2, p2)
                    n = sum(patch_stat(unified(body, new, "a", "b"))[1:])
                    if best is None or n < best[0]:
                        best = (n, (k2, s2, c2, body, "SIBLING file — no audited revision of this path exists"))
                    break                               # newest audited revision of each sibling only
        base = best[1] if best else None

    if base is None:
        L.append("base:     none recoverable — FULL review")
    else:
        bkey, bsha, bcommit, bbody, how = base
        bpath = bkey[len(fd.COMPOSE_REPO) + 1:]
        patch = unified(bbody, new, f"a/{bpath}@{bsha[:12]}", f"b/{path}@{sha[:12]}")
        pf = write(out, f"{stem}@{bsha[:12]}..{sha[:12]}.patch", patch)
        h, a, r = patch_stat(patch)
        L.append(f"base:     manifests/{bkey[:-5]}/sha256-{bsha}.md  ({how}; reviewed {page_date(f'manifests/{bkey[:-5]}/sha256-{bsha}.md') or '?'})")
        L.append(f"          base commit {bcommit}")
        L.append(f"patch:    {pf}  ({h} hunks, +{a}/-{r}) — this is a DELTA review against the base page")
        if clone and how == "same file":
            rc, log, _ = sh(["git", "log", "--oneline", f"{bcommit}..{commit}", "--", path], cwd=clone)
            commits = log.strip().split("\n") if log.strip() else []
            L.append(f"commits:  {len(commits)} touch the file between the pins" +
                     (": " + ", ".join(c.split(" ")[0] for c in commits[:20]) if commits else ""))

    # --- what is actually running: per-service revisions, per CVM
    for c in mine:
        table = service_table(c["actions"], content_of)
        groups, firsts, gone, other, same_bytes = {}, {}, [], {}, {}
        for svc, a in table.items():
            if a.get("file") != path:
                if svc not in declared:     # same name = recreated from this file's lineage; else a stranger
                    other.setdefault((a.get("file"), (a.get("file_sha256") or "?").lower()[:12]), []).append(
                        (svc, (a.get("timestamp") or "")[:10]))
                continue
            s = (a.get("file_sha256") or "?").lower()
            firsts.setdefault(s, (s, a.get("commit"), a.get("tag"), (a.get("timestamp") or "")[:16]))
            groups.setdefault(firsts[s], []).append(svc)
            # one hash can be upped from several commits; the label must not pin them all to the first
            cs = same_bytes.setdefault(s, [])
            if a.get("commit") and a["commit"] not in cs:
                cs.append(a["commit"])
        L.append("")
        L.append(f"running on {', '.join(sorted(c['hosts']))} — one CVM, measured harness {c['compose_hash'][:12]}, "
                 f"{len(c['actions'])}-entry action log:")
        L.append("  (which revision last created each container — the attested hash is only the last file touched;")
        L.append("   patches named here are in the evidence directory)")
        for (s, cm, tg, ts), svcs in sorted(groups.items(), key=lambda kv: kv[0][3]):
            mark = "THIS FILE" if s == sha else ("audited" if s in audited else "NOT audited")
            live = sorted(x for x in svcs if x in declared)
            stale = sorted(x for x in svcs if x not in declared)
            also = [x[:8] for x in same_bytes.get(s, []) if x != cm]
            line = (f"  {s[:12]} @ {str(cm)[:8]}{' and ' + ', '.join(also) + ' (same bytes)' if also else ''} "
                    f"({tg}, {ts[:10]}) [{mark}] — {', '.join(live) or '-'}")
            if s != sha and live:
                body = content_of(cm, path)
                if body is not None:
                    p = unified(body, new, f"a/{path}@{s[:12]}", f"b/{path}@{sha[:12]}")
                    h, a_, r_ = patch_stat(p)
                    line += f"  [{h} hunks, +{a_}/-{r_} vs this file: {os.path.basename(write(out, f'{stem}@{s[:12]}..{sha[:12]}.running.patch', p))}]"
            if live:
                L.append(line)
            if stale:
                gone.append(f"{', '.join(stale)} ({s[:12]})")
        for (f, s12), pairs in sorted(other.items(), key=lambda kv: max(t for _, t in kv[1])):
            svcs, ts = [x for x, _ in pairs], max(t for _, t in pairs)
            known = s12 in {x[:12] for x in (idx.get("manifests") or {}).get(f"{fd.COMPOSE_REPO}/{f}", [])}
            L.append(f"  !! from ANOTHER file, last up {ts} with no down logged since — may still be running beside this recipe: "
                     f"{f} {s12} [{'audited' if known else 'NOT audited'}] — {', '.join(sorted(svcs)[:12])}"
                     + (f" (+{len(svcs) - 12} more)" if len(svcs) > 12 else ""))
        if gone:
            L.append(f"  no longer declared by this file, last up never followed by a logged down — confirm gone: {'; '.join(gone)}")
        write(out, f"actions-{c['compose_hash'][:12]}.json", json.dumps(c["actions"], indent=1))

    # --- images this file names, and whether each has a page
    imgs, warns = fd.in_scope_images(new.decode("utf-8", "replace"))
    old = base[3].decode("utf-8", "replace") if base else ""
    L.append("")
    L.append("in-scope images this file names (defer per-image behavior to these pages):")
    for ref, role in sorted(imgs.items()):
        d = re.search(r"sha256:([0-9a-f]{64})", ref)
        fresh = "" if (d.group(1) if d else ref) in old else "  << NEW in this revision"
        L.append(f"  {role:<16} {ref}  [{image_status(idx, ref, target_ids)}]{fresh}")
    for w in warns:
        L.append(f"  !! {w}")
    return L


def brief_image(t, idx, cvms, out, target_ids):
    ref = t["id"]
    m = re.match(r"^(.+?)(?::[A-Za-z0-9._\-]+)?@sha256:([0-9a-f]{64})$", ref)
    L, src = [], None
    if not m:
        nref = fd.normalized_ref(ref)
        L.append(f"page:     images/{nref}/tag-<tag>.md  (tag-only reference: {ref})")
        return L
    nref, digest = fd.normalized_ref(m.group(1)), m.group(2)
    L.append(f"page:     images/{nref}/sha256-{digest}.md")
    prior = (idx.get("images") or {}).get(nref, [])
    if prior:
        pages = sorted(((page_date(f"images/{nref}/sha256-{d}.md"), d) for d in prior), reverse=True)
        src = ((idx.get("sources") or {}).get(nref) or {}).get(pages[0][1])
        L.append(f"kind:     DELTA — {len(prior)} audited digest(s) of this ref; lineage in images/{nref}/README.md")
        L.append(f"base:     images/{nref}/sha256-{pages[0][1]}.md  (most recent review, {pages[0][0] or '?'})")
        if src:
            L.append(f"          base source pin: {src['repo']}@{src['commit']} — diff old..new restricted to the audit surface")
        else:
            L.append("          base has no `sources` pin — read its identity row before diffing")
    else:
        L.append("kind:     NEW — no audited digest of this ref; FULL review")
    L.append(f"role:     {t['role']}")
    rc, o, e = sh([sys.executable, os.path.join(TOOLS, "resolve_identity.py"), "--brief", f"{m.group(1)}@sha256:{digest}"],
                  timeout=180)
    L.append("")
    L.append("resolve_identity.py --brief:")
    L += ["  " + l for l in (o.strip() or f"(no output, rc={rc})").split("\n")]
    if rc not in (0, 2):
        L.append(f"  !! resolver crashed (rc={rc}): {e.strip().splitlines()[-1][:200] if e.strip() else ''}")
    got = re.search(r"repo   : (\S+)\n\s+commit : ([0-9a-f]{40})", o)
    if got and got.group(1) == fd.COMPOSE_REPO:
        # An image built by a compose-repo workflow: the commit pins a build
        # recipe, and a diff of the whole compose repo says nothing about it.
        # What bounds the review is the chain of base images down to one that
        # has a page — every layer in between is unaudited patch stack.
        L.append("")
        L.append("build chain (image labels, self-asserted — each layer's recipe dir at its own commit is in the compose clone):")
        d, hops = digest, 0
        while d and hops < 8:
            cfg, err = ri.image_config(m.group(1), d)
            lab = ri.build_labels(cfg) if not err else {}
            status = "THIS IMAGE" if d == digest else ("audited — stop here" if d in prior else "NO PAGE — its patches are in scope")
            L.append(f"  {d[:12]}  {lab.get('nearai.build.recipe', '(no recipe label: ' + (err or 'unlabelled') + ')')} "
                     f"@ {lab.get('nearai.build.source_revision', '?')[:12]}  [{status}]")
            if d != digest and d in prior:
                break
            nxt = lab.get("org.opencontainers.image.base.digest", "").replace("sha256:", "")
            if not nxt or fd.normalized_ref(lab.get("org.opencontainers.image.base.name", "")) != nref:
                if nxt:
                    L.append(f"  base leaves this ref: {lab.get('org.opencontainers.image.base.name')}@sha256:{nxt[:12]} "
                             f"[{image_status(idx, lab.get('org.opencontainers.image.base.name', '') + '@sha256:' + nxt, target_ids)}]")
                else:
                    L.append("  !! chain ends without reaching an audited digest — scope is NOT bounded; treat as a full review")
                break
            d, hops = nxt, hops + 1
    elif got and prior and src and src["repo"] == got.group(1):
        st, body = fd.get(f"https://github.com/{src['repo']}/compare/{src['commit']}...{got.group(2)}.diff", timeout=120)
        if st == 200 and body.strip():
            patch = body.decode("utf-8", "replace")
            pf = write(out, f"{nref.split('/')[-1]}@{src['commit'][:8]}..{got.group(2)[:8]}.source.patch", patch)
            files = re.findall(r"^diff --git a/(\S+)", patch, re.M)
            h, a, r = patch_stat(patch)
            L.append("")
            L.append(f"source delta {src['commit'][:12]}...{got.group(2)[:12]} in {src['repo']}: {len(files)} files, {h} hunks, +{a}/-{r}")
            L.append(f"  patch: {pf}")
            L.append("  files: " + ", ".join(files[:60]) + (f" (+{len(files) - 60} more)" if len(files) > 60 else ""))
        else:
            L.append(f"\nsource delta: compare {src['commit'][:12]}...{got.group(2)[:12]} could not be fetched (HTTP {st}) — diff by hand")
    if "UNRESOLVED" in o or rc != 0:
        L.append("  !! not resolved mechanically — try the ghcr anonymous-token / upstream-release routes by hand")
        L.append("     before settling for an INCONCLUSIVE page (SKILL.md step 6)")
    return L


def brief_measured(t, cvms, idx, out, target_ids):
    h = t["id"]
    L = [f"page:     manifests/measured/sha256-{h}.md",
         "method:   notes/method.md §4 — a DOCUMENT review; map of hash -> node in manifests/measured/README.md"]
    c = next((c for c in cvms if c["compose_hash"] == h), None)
    if not c:
        L.append("!! no sampled CVM reports this hash any more — the fleet moved during the run; re-run")
        return L
    outer = ((c["info"].get("tcb_info") or {}).get("app_compose")) or ""
    if hashlib.sha256(outer.encode()).hexdigest() != h:
        L.append("!! sha256(app_compose) != compose_hash — INTEGRITY, do not commission")
        return L
    L.append(f"identity: hardware-measured — sha256(app_compose) == info.compose_hash, re-hashed, match; guest OS {str(c['os'])[:12]}")
    L.append(f"file:     {write(out, f'measured@{h[:12]}.json', outer)}  (the dstack manifest, verbatim)")
    L.append(f"          {write(out, f'measured@{h[:12]}.yaml', fd.compose_yaml(outer))}  (its docker_compose_file)")
    L.append(f"hosts:    {', '.join(sorted(c['hosts']))}")
    MEASURED[h] = fd.compose_yaml(outer)
    L.append("base:     the measured compose of an earlier harness is not recoverable from the fleet; use the newest")
    L.append("          page in manifests/measured/ for the same node (README) as the format and carry-over base")
    imgs, warns = fd.in_scope_images(outer)
    L.append("")
    L.append("in-scope images this harness names:")
    for ref, role in sorted(imgs.items()):
        L.append(f"  {role:<16} {ref}  [{image_status(idx, ref, target_ids)}]")
    for w in warns:
        L.append(f"  !! {w}")
    return L


# --------------------------------------------------------------------- main

MEASURED = {}       # hash -> compose yaml, for the near-twin check in main()

ROLE_WEIGHT = {"model-server": 5, "e2ee-terminator": 5, "process-access": 4, "guest OS": 4,
               "deployment config": 3, "model-layer recipe": 3, "device-privilege": 2, "log-access": 2}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--issue", type=int, help="drift issue to compare against (default: the open fleet-drift issue)")
    ap.add_argument("--samples", type=int, default=8,
                    help="attestation samples per affected host, to catch a second CVM behind one name (default 8)")
    ap.add_argument("--full", action="store_true", help="print every target block in full instead of the summary")
    ap.add_argument("--out", help="evidence directory (default: a fresh dir under the system temp dir)")
    ap.add_argument("--cache", default=os.path.expanduser("~/.cache/teemoon-audits"),
                    help="where the compose-repo clone lives (default ~/.cache/teemoon-audits)")
    args = ap.parse_args()
    out = args.out or tempfile.mkdtemp(prefix="prep-drift-")
    os.makedirs(out, exist_ok=True)

    # 1. the sweep, fresh — the issue body is a snapshot
    report = os.path.join(out, "fleet_drift.json")
    for attempt in range(3):
        if os.path.exists(report):
            os.remove(report)
        rc, text, err = sh([sys.executable, os.path.join(TOOLS, "fleet_drift.py"), "--json", report], timeout=600)
        write(out, "fleet_drift.txt", text + err)
        if not os.path.exists(report):
            print("STOP — the sweep could not run (no network, or the endpoint directory is down).")
            print("Commission nothing: a reviewer with no network can only write INCONCLUSIVE.")
            print((text + err).strip()[-600:])
            return 2
        with open(report) as f:
            drift = json.load(f)
        # A timed-out fetch (HTTP 0) is weather, not an integrity break; a hash
        # mismatch is never retried away.
        if not drift["integrity"] or not all("(HTTP 0)" in i["note"] for i in drift["integrity"]):
            break
    targets = drift["unaudited"]
    print(f"# drift prep — {len(targets)} unaudited target(s), {drift['hosts']} hosts advertised, "
          f"{len(drift['unreachable'])} not serving")
    print(f"evidence: {out}")
    if drift["integrity"] or drift["broken"]:
        print("\nSTOP — integrity problems; nothing may be concluded about these hosts until they are explained:")
        for i in drift["integrity"]:
            print(f"  {i['host']}: {i['note']}")
        for b in drift["broken"]:
            print(f"  index: {b}")
        return 2
    if drift["known_open"]:
        print(f"known open (acknowledged.json, backlog not alarm): {len(drift['known_open'])}")

    # 2. what moved since the issue was filed
    num, named = issue_ids(args.issue)
    if named is not None:
        live = {short_id(t) for t in targets}
        gone, new = sorted(named - live), sorted(live - named)
        print(f"\nvs issue #{num}: " + ("identical target list" if not gone and not new else
              f"THE FLEET MOVED — {len(new)} target(s) not in the issue: {', '.join(new) or '-'}; "
              f"{len(gone)} named by the issue and no longer live-and-unaudited: {', '.join(gone) or '-'}"))
    if not targets:
        print("\nNothing to commission.")
        return 0

    # 3. capture every affected CVM once, and the compose repo once
    eps_st, eps_b = fd.get(fd.ENDPOINTS)
    eps = json.loads(eps_b)
    eps = eps["endpoints"] if isinstance(eps, dict) else eps
    dom = {e["domain"].split(".")[0]: e["domain"] for e in eps}
    hosts = sorted({h for t in targets for h in t["hosts"]})
    cvms = capture_cvms([dom[h] for h in hosts if h in dom], args.samples)
    clone = ensure_clone(args.cache)
    idx = fd.load_index()
    # The sweep takes 3 samples a host; this capture takes more. Anything the
    # deeper capture sees that the sweep's lottery missed is a target too.
    have = {t["id"] for t in targets}
    for c in cvms:
        extra = []
        if c["compose_hash"] != "?" and c["compose_hash"] not in (idx.get("measured") or []):
            extra.append({"kind": "measured", "id": c["compose_hash"], "role": "deployment config"})
        ups = [a for a in c["actions"] if a.get("action") == "compose_up" and a.get("file_sha256")]
        if ups:
            f, h = ups[-1]["file"], ups[-1]["file_sha256"].lower()
            if h not in (idx.get("manifests") or {}).get(f"{fd.COMPOSE_REPO}/{f}", []):
                extra.append({"kind": "recipe", "id": f"{f} {h}", "role": "model-layer recipe"})
        for e in extra:
            if e["id"] not in have:
                have.add(e["id"])
                targets.append(dict(e, hosts=sorted(c["hosts"]), missed_by_sweep=True))
    target_ids = {t["id"] for t in targets}

    print(f"\n{len(cvms)} distinct CVM(s) behind {len(hosts)} affected host(s) ({args.samples} samples each):")
    for c in cvms:
        print(f"  harness {c['compose_hash'][:12]} · os {str(c['os'])[:12]} · {len(c['actions'])} log entries · "
              f"{', '.join(sorted(c['hosts']))}")
    split = [h for h in hosts if sum(h in c["hosts"] for c in cvms) > 1]
    if split:
        print(f"  !! {', '.join(split)} answer from more than one CVM"
              + (" — re-run with --samples 24 to be sure none is missed" if args.samples < 24 else ""))
    last = max((a.get("timestamp", "") for c in cvms for a in c["actions"] if a.get("action") == "compose_up"), default="")
    print(f"  newest compose_up anywhere: {last[:19]}Z — several close together means a rollout in progress; expect more")

    # 4. targets, by blast radius
    targets.sort(key=lambda t: (-len(t["hosts"]) * ROLE_WEIGHT.get(t["role"].split(" (")[0], 1), t["kind"], t["id"]))
    for n, t in enumerate(targets, 1):
        hs = sorted(t["hosts"])
        head = [f"TARGET {n}/{len(targets)}  [{t['kind']}] {t['role']} — {t['id']}"
                + ("  (the 3-sample sweep missed this one)" if t.get("missed_by_sweep") else ""),
                f"on {len(hs)} host(s): {', '.join(hs)}"]
        if t["kind"] == "recipe":
            L = brief_recipe(t, cvms, idx, clone, out, target_ids)
        elif t["kind"] == "image":
            L = brief_image(t, idx, cvms, out, target_ids)
        elif t["kind"] == "measured":
            L = brief_measured(t, cvms, idx, out, target_ids)
        else:
            L = [f"page:     os/sha256-{t['id']}.md",
                 "identity: recompute against upstream Dstack-TEE/meta-dstack release digests before calling it UNRESOLVED"]
        bf = write(out, f"brief-{n}-{t['kind']}-{short_id(t)}.txt", "\n".join(head + [""] + L) + "\n")
        print(f"\n{head[0]}\n  {head[1]}")
        for l in L:
            if args.full or l.startswith(("kind:", "base:", "patch:", "identity:", "!!", "  !!", "source delta", "  VERDICT", "build chain")) \
                    or "<< NEW" in l or "NOT audited" in l or "UNAUDITED" in l or "NO PAGE" in l or "THIS IMAGE" in l:
                print("  " + l.strip())
        print(f"  -> {os.path.basename(bf)}  ({len(L)} lines — paste into the brief's Target / Where-it-runs sections, or have the reviewer Read it)")

    # 5. how to spend the reviewers
    print("\n" + "=" * 78)
    print("COMMISSIONING")
    print("  one reviewer per target above, in this order, at most 3 running at once;")
    print("  image targets before the recipes that name them, so a recipe page can cite a page that exists.")
    print("  A target marked DELTA gets the delta brief (base page + patch); the whole-file sink sweep stays mandatory.")
    hs = sorted(MEASURED)
    for i, a in enumerate(hs):
        for b in hs[i + 1:]:
            p = unified(MEASURED[a].encode(), MEASURED[b].encode(), a[:12], b[:12])
            _, add, rem = patch_stat(p)
            if add + rem <= 40:
                pf = write(out, f"measured@{a[:12]}..{b[:12]}.patch", p)
                print(f"  measured {a[:12]} and {b[:12]} are near-twins (+{add}/-{rem}: {os.path.basename(pf)}) —")
                print("  one reviewer writes both pages; the second is the first plus that patch, each line of it reviewed.")
    print("  After each wave: no index_page.py while a skeleton page is on disk; then re-run this script —")
    print("  exit 0 is the only finish line.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
