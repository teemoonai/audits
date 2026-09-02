#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""resolve_identity.py — what source tree is this digest actually built from?

Step 1 of responding to a fleet-drift issue. A review keyed to the wrong tree is
worse than no review, and this repo has been wrong twice for the same reason: a
compose comment was trusted and the image's own registry metadata was never read.
So identity gets established mechanically, before any reviewing starts, and the
result is handed to the reviewer as a given.

It walks the evidence ladder strongest-first and stops at the first rung that
answers, reporting WHICH rung answered — because the strength of the binding is
itself part of the finding, and it decides whether the digest may carry a
`sources` pin in index.json:

  1. SIGNED ATTESTATION   a GitHub build attestation binds digest -> commit.
                          Strongest available. Reads EVERY attestation, not the
                          first: one image on this fleet has four.
  2. OCI BUILD LABEL      the image declares its own commit. Registry-verifiable
                          but self-asserted by whoever ran the build.
  3. RELEASE TAG          exactly one published tag resolves to this digest, and
                          that tag is a real git tag.
  4. ARG FINGERPRINT      untagged and unlabelled: dump the Dockerfile ARG
                          defaults from the image's config history so a human can
                          bracket a commit RANGE against upstream tags. A bracket
                          is NOT a pin and earns no `sources` entry.
  5. UNRESOLVED           publish an INCONCLUSIVE page making no privacy claim,
                          leave it out of index.json, and record it in
                          acknowledged.json. That is a correct outcome.

One technique is deliberately not automated: when a build `git clone`s an
unpinned ref it leaves `.git/` in a layer, and `.git/shallow` recovers the commit.
That worked once here and is worth trying by hand at rung 4 -- it needs a layer
download and a full-tree diff to confirm, which is too heavy to run speculatively.

Usage:
  python3 tools/resolve_identity.py lmsysorg/sglang@sha256:5027e95b...
  python3 tools/resolve_identity.py nvcr.io/nvidia/k8s/dcgm-exporter@sha256:ed59...
  python3 tools/resolve_identity.py --brief lmsysorg/sglang@sha256:...  # agent-ready block

Stdlib only. GITHUB_TOKEN is optional and only raises the rate limit.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# Images whose attestations are published by a repo the image name does not name.
REPO_ALIASES = {"compose-manager-launcher": "compose-manager",
                "vllm-proxy-rs": "inference-proxy"}

ACCEPT = ",".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])


class _StripAuthOnCrossHostRedirect(urllib.request.HTTPRedirectHandler):
    """Registries hand blob reads off to a CDN with a pre-signed URL. urllib
    replays the bearer token to that new host; the CDN sees two credentials and
    answers 400, which reads exactly like "this image has no labels". curl drops
    the header on a cross-host hop -- so did every by-hand check that contradicted
    this script. Drop it here too, or rung 2 silently misses and a live image gets
    published INCONCLUSIVE on the strength of a transport bug."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlsplit(newurl).netloc != \
                urllib.parse.urlsplit(req.full_url).netloc:
            for h in list(new.headers):
                if h.lower() == "authorization":
                    del new.headers[h]
            new.unredirected_hdrs.pop("Authorization", None)
        return new


_OPENER = urllib.request.build_opener(_StripAuthOnCrossHostRedirect)


def get(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 0, str(e).encode()


def gh_headers():
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
         "User-Agent": "teemoonai-audits-resolve-identity"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def split_ref(ref):
    m = re.match(r"^(.*?)@sha256:([0-9a-f]{64})$", ref)
    if not m:
        sys.exit(f"expected <image>@sha256:<64 hex>, got: {ref}")
    image = m.group(1)
    if ":" in image.split("/")[-1]:
        image = image.rsplit(":", 1)[0]          # drop a tag; the digest is the identity
    return image, m.group(2)


# ---- rung 1: signed build attestation -------------------------------------

def rung_signed(image, digest):
    name = image.split("/")[-1]
    repo = f"nearai/{REPO_ALIASES.get(name, name)}"
    st, body = get(f"https://api.github.com/repos/{repo}/attestations/sha256:{digest}", gh_headers())
    if st != 200:
        return None, f"repo-level {repo}: HTTP {st}"
    try:
        atts = json.loads(body).get("attestations") or []
    except Exception:
        return None, "undecodable attestation response"
    if not atts:
        return None, f"{repo}: 200 but zero attestations"
    import base64
    seen = []
    for a in atts:
        try:
            p = json.loads(base64.b64decode(a["bundle"]["dsseEnvelope"]["payload"]))["predicate"]["buildDefinition"]
            seen.append((p["resolvedDependencies"][0]["digest"].get("gitCommit"),
                         p["externalParameters"]["workflow"].get("ref", "?")))
        except Exception:
            continue
    if not seen:
        return None, "attestations present but no gitCommit could be read"
    commits = {c for c, _ in seen}
    note = f"{len(seen)} attestation(s)"
    if len(commits) > 1:
        note += f" naming {len(commits)} DIFFERENT commits — verify the trees match before pinning"
    return {"repo": repo, "commit": seen[0][0], "all": seen}, note


# ---- registry access -------------------------------------------------------

def registry_for(image):
    """-> (registry_host, repo_path, token_url). nvcr.io uses a different token
    endpoint than Docker Hub; discovered the hard way."""
    parts = image.split("/")
    if parts[0].count(".") or ":" in parts[0]:
        host, repo = parts[0], "/".join(parts[1:])
        if host == "nvcr.io":
            return host, repo, f"https://nvcr.io/proxy_auth?scope=repository:{repo}:pull"
        return host, repo, None
    repo = image if "/" in image else f"library/{image}"
    return "registry-1.docker.io", repo, \
        f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repo}:pull"


def image_config(image, digest):
    host, repo, token_url = registry_for(image)
    headers = {"Accept": ACCEPT}
    if token_url:
        st, b = get(token_url)
        if st == 200:
            try:
                headers["Authorization"] = "Bearer " + json.loads(b)["token"]
            except Exception:
                pass
    base = f"https://{host}/v2/{repo}/manifests"
    st, b = get(f"{base}/sha256:{digest}", headers)
    if st != 200:
        return None, f"manifest HTTP {st}"
    m = json.loads(b)
    child = next((x["digest"] for x in m.get("manifests", [])
                  if (x.get("platform") or {}).get("architecture") == "amd64"), None) \
        or f"sha256:{digest}"
    st, b = get(f"{base}/{child}", headers)
    if st != 200:
        return None, f"child manifest HTTP {st}"
    cfg_digest = json.loads(b)["config"]["digest"]
    auth = {k: v for k, v in headers.items() if k == "Authorization"}
    st, b = get(f"https://{host}/v2/{repo}/blobs/{cfg_digest}", auth)
    if st != 200:
        return None, f"config blob HTTP {st}"
    return json.loads(b), None


# ---- rung 2: OCI build labels ---------------------------------------------

COMMIT_LABELS = ["ai.sglang.build.commit", "ai.vllm.build.commit",
                 "org.opencontainers.image.revision"]


def rung_labels(cfg):
    labels = (cfg.get("config") or {}).get("Labels") or {}
    commit = next((labels[k] for k in COMMIT_LABELS if labels.get(k)), None)
    if not commit or not re.fullmatch(r"[0-9a-f]{40}", commit):
        return None, "no build-commit label"
    src = labels.get("org.opencontainers.image.source") or ""
    repo = src.replace("https://github.com/", "").strip("/") or "?"
    tag = labels.get("ai.sglang.image.tag") or labels.get("ai.vllm.image.tag") \
        or labels.get("org.opencontainers.image.version") or ""
    return {"repo": repo, "commit": commit, "tag": tag}, "self-asserted by the builder"


# ---- rung 3: tag reverse-lookup -------------------------------------------

def rung_tags(image, digest):
    _, repo, token_url = registry_for(image)
    if not token_url or "auth.docker.io" not in token_url:
        return None, "tag reverse-lookup only implemented for Docker Hub"
    url = f"https://hub.docker.com/v2/repositories/{repo}/tags?page_size=100"
    hits, scanned = [], 0
    while url and scanned < 3000:
        st, b = get(url)
        if st != 200:
            break
        d = json.loads(b)
        for t in d.get("results", []):
            scanned += 1
            if (t.get("digest") or "").endswith(digest):
                hits.append(t["name"])
        url = d.get("next")
    if not hits:
        return None, f"no tag among {scanned} resolves to this digest"
    release = [h for h in hits if re.fullmatch(r"v?\d+\.\d+(\.\d+)?", h)]
    return {"tags": hits, "release": release[0] if release else None}, f"{scanned} tags scanned"


# ---- rung 4: ARG fingerprint ----------------------------------------------

def rung_fingerprint(cfg):
    args = []
    for h in cfg.get("history", []):
        c = (h.get("created_by") or "").replace("\n", " ")
        m = re.match(r"\s*(?:/bin/sh -c #\(nop\)\s*)?ARG\s+([A-Z0-9_]+=\S.*)$", c.strip())
        if m:
            args.append(m.group(1).strip())
    return {"created": cfg.get("created"), "args": sorted(set(args))}, \
        "bracket manually against docker/Dockerfile at candidate upstream tags"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", help="<image>@sha256:<64 hex>")
    ap.add_argument("--brief", action="store_true", help="emit a target block ready to paste into a reviewer brief")
    a = ap.parse_args()
    image, digest = split_ref(a.ref)

    print(f"resolving {image}@sha256:{digest[:12]}…\n")
    resolved, cls = None, None

    r, note = rung_signed(image, digest)
    print(f"  [1] signed attestation  {'HIT' if r else 'miss'}  — {note}")
    if r:
        resolved, cls = r, "signed attestation"
        for c, ref in r["all"]:
            print(f"        {c[:12]}  {ref}")

    cfg, err = image_config(image, digest)
    if err:
        print(f"  [!] registry: {err}")
    else:
        if not resolved:
            r, note = rung_labels(cfg)
            print(f"  [2] OCI build label     {'HIT' if r else 'miss'}  — {note}")
            if r:
                resolved, cls = r, "OCI build label"
        if not resolved:
            r, note = rung_tags(image, digest)
            print(f"  [3] release tag         {'HIT' if r else 'miss'}  — {note}")
            if r:
                resolved, cls = {"repo": "?", "commit": None, "tags": r["tags"],
                                 "release": r["release"]}, "release tag"
        if not resolved:
            r, note = rung_fingerprint(cfg)
            print(f"  [4] ARG fingerprint     — {note}")
            print(f"        image created: {r['created']}")
            for x in r["args"]:
                print(f"        {x}")
            print("        also try: pull a layer and look for .git/shallow (see the docstring)")

    print()
    if not resolved:
        print("VERDICT: UNRESOLVED.")
        print("  Publish an INCONCLUSIVE page that makes NO privacy claim, leave the digest")
        print("  out of index.json, and add it to acknowledged.json.")
        return 2

    print(f"VERDICT: resolved by {cls.upper()}")
    print(f"  repo   : {resolved.get('repo')}")
    print(f"  commit : {resolved.get('commit') or '(tag only — ' + str(resolved.get('release')) + ')'}")
    pinnable = cls in ("signed attestation", "OCI build label", "release tag")
    print(f"  sources pin in index.json: {'YES' if pinnable else 'NO — a bracket is not a binding'}")

    if a.brief:
        print("\n--- paste into the reviewer brief ---")
        print(f"- Image: `{image}@sha256:{digest}`")
        print(f"- Identity GIVEN, established by **{cls}**: "
              f"`{resolved.get('repo')}` @ `{resolved.get('commit')}`")
        if cls == "OCI build label":
            print("- Class caveat: registry-verifiable but **self-asserted by the builder** — "
                  "not a signed provenance attestation. Say so on the page.")
        if cls == "signed attestation":
            print("- Class note: this is the STRONGEST binding in the repo — a signed provenance "
                  "attestation, not a self-asserted label. Say so on the page.")
        print(f"- Read source at `https://raw.githubusercontent.com/{resolved.get('repo')}/"
              f"{resolved.get('commit')}/<path>`")
        print("- Walk `notes/audit-surface.md` and report anything you could not reach under "
              "*Not traced*.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
