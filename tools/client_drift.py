#!/usr/bin/env python3
"""Client drift check: does every App Store tag of teemoonai/teemoon-ios have a
page under client/teemoon-ios/?  The server side has fleet_drift.py for attested
identities; this is its counterpart for the one component that has no
attestation, keyed by the release tag and the commit it points at.

Usage:  tools/client_drift.py            # exit 1 and list what is unaudited
        tools/client_drift.py --json     # machine-readable

Reads the tag list from the GitHub API (no token needed for a public repo) and
the page list from the working tree.  A page counts for a tag only if its
filename carries the tag AND its pinned full sha still matches what the tag
points at — a moved tag is drift too.  Never writes a page (see README: nothing
in tools/ may write a page).
"""
import json, os, re, sys, urllib.request

REPO = "teemoonai/teemoon-ios"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(ROOT, "client", "teemoon-ios")
RELEASE_TAG = re.compile(r"^v\d+\.\d+\.\d+$")   # App Store tags; tf/* are TestFlight

def tags():
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/tags?per_page=100",
                                 headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return {t["name"]: t["commit"]["sha"] for t in json.load(r) if RELEASE_TAG.match(t["name"])}

def pages():
    out = {}
    if not os.path.isdir(PAGES):
        return out
    for f in os.listdir(PAGES):
        m = re.match(r"^(v\d+\.\d+\.\d+)-([0-9a-f]{7,})\.md$", f)
        if not m:
            continue
        text = open(os.path.join(PAGES, f), encoding="utf-8").read()
        sha = re.search(r"commit `([0-9a-f]{40})`", text)
        verdict = re.search(r"^## verdict: (.*)$", text, re.M)
        out[m.group(1)] = {"file": f, "sha": sha.group(1) if sha else None,
                           "verdict": verdict.group(1)[:80] if verdict else None}
    return out

def main():
    want_json = "--json" in sys.argv
    live, have = tags(), pages()
    drift = []
    for tag, sha in sorted(live.items()):
        page = have.get(tag)
        if page is None:
            drift.append({"tag": tag, "sha": sha, "problem": "no page"})
        elif page["sha"] != sha:
            drift.append({"tag": tag, "sha": sha, "problem": f"tag moved: page pins {page['sha']}", "page": page["file"]})
        elif not page["verdict"]:
            drift.append({"tag": tag, "sha": sha, "problem": "page has no verdict line", "page": page["file"]})
    if want_json:
        print(json.dumps({"tags": live, "pages": have, "drift": drift}, indent=2))
    else:
        for tag, sha in sorted(live.items()):
            p = have.get(tag)
            print(f"{tag:10s} {sha[:7]}  {'page ' + p['file'] if p else 'NO PAGE'}")
        if drift:
            print("\nunaudited / drifted:")
            for d in drift:
                print(f"  {d['tag']} @ {d['sha'][:7]}: {d['problem']}")
    sys.exit(1 if drift else 0)

if __name__ == "__main__":
    main()
