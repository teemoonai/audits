#!/usr/bin/env python3
"""Public-tag check: is the commit a release tag points at the audited build's code?

Until 1.1.0 the iOS audit ran on the TestFlight build commit (tf/<ver>-<n>) and the
public tag was cut afterwards as a scrub of that tree: development-only folders
removed, comments reworded. A page for the public tag then needs one fact: that no
non-comment line differs. This tool emits that fact; it never writes a page
(README: nothing in tools/ may write a page). From 1.1.0 the audited commit is the
tagged commit and this check is a no-op.

Usage:  tools/public_tag_check.py <git-dir> <audited-ref> <public-ref> [--diff]

Prints a JSON summary: deleted/added/modified files, deleted top-level entries,
per-file numstat, and `modified_with_non_comment_change` — the modified files that
still differ after `/* */` blocks and `//` comments (outside string literals and
URLs, approximately) and blank lines are removed. `--diff` appends `git diff -U0`
of the modified files. Binary blobs are compared as bytes decoded with replacement.
"""
import collections, json, re, subprocess, sys

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    repo, a, b = args
    def git(*x):
        return subprocess.run(["git", "-C", repo, *x], capture_output=True, check=True).stdout.decode("utf-8", "replace")
    status = [l.split("\t") for l in git("diff", "--name-status", a, b).splitlines() if l]
    deleted = [p for s, *r in status for p in r if s.startswith("D")]
    added = [p for s, *r in status for p in r if s.startswith("A")]
    modified = [r[-1] for s, *r in status if not s.startswith(("A", "D"))]
    def strip(src):
        src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
        out = []
        for line in src.splitlines():
            line = re.sub(r"(?<![:\"'])//.*$", "", line).strip()
            if line:
                out.append(line)
        return out
    code = [f for f in modified if strip(git("show", f"{a}:{f}")) != strip(git("show", f"{b}:{f}"))]
    numstat = git("diff", "--numstat", a, b, "--", *modified).strip().splitlines() if modified else []
    print(json.dumps({
        "audited": git("rev-parse", a + "^{commit}").strip(), "public": git("rev-parse", b + "^{commit}").strip(),
        "audited_tree": git("rev-parse", a + "^{tree}").strip(), "public_tree": git("rev-parse", b + "^{tree}").strip(),
        "deleted": len(deleted), "deleted_top_level": dict(collections.Counter(p.split("/")[0] for p in deleted)),
        "added": added, "modified": modified, "modified_numstat": numstat,
        "modified_with_non_comment_change": code,
        "code_identical": not added and not code}, indent=1))
    if "--diff" in sys.argv and modified:
        print(git("diff", "-U0", a, b, "--", *modified))

if __name__ == "__main__":
    main()
