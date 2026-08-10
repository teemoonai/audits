#!/usr/bin/env python3
"""index_page.py — gate a published page, and keep index.json honest.

Step 4 of responding to a fleet-drift issue. Adding a page is not publishing it:
the app shows a link only when index.json gates the exact running identity, and
shows the review's conclusion only when `verdicts` carries it. Doing that by hand
means editing five parallel structures consistently, every time, which is exactly
the kind of bookkeeping that has already produced one wrong claim in this repo.

What it does:
  - infers the gate from the page's own path (the frozen path spec is a pure
    function, so the path IS the identity)
  - refreshes `verdicts` for EVERY page on disk, reading each page's own
    `## verdict:` heading verbatim — never a summary written here
  - refreshes the machine-readable layer beside it, also read from the page's
    own text: `verdictClass` (the class token the verdict line opens with) and
    `findings` (the page's `### SEVERITY (deployed: …) — title` headings, with
    GitHub anchors). Pages the rules can't read are omitted and warned — the
    fix is conforming the page's wording, never overriding it here
  - validates the whole index: every gated link has a page, every page has a
    verdict, nothing on disk is silently ungated

Two guards worth knowing about, both learned from real mistakes:

  --no-gate is REQUIRED for a page whose verdict is INCONCLUSIVE. A page that
  makes no privacy claim must not produce an audit link — the app renders links
  as "source reviewed", which would be a claim. The script refuses to gate one.

  A `sources` pin is only accepted with --commit, and the caller is expected to
  have established it with resolve_identity.py. A bracketed identity is not a
  binding; the app renders `sources` as a VERIFIED digest->commit pin.

Usage:
  python3 tools/index_page.py images/docker.io/lmsysorg/sglang/sha256-<64hex>.md \\
      --commit sgl-project/sglang@49e384ce9d304648e9959666ecb8ce8cd98d0deb
  python3 tools/index_page.py manifests/measured/sha256-<64hex>.md
  python3 tools/index_page.py <page> --no-gate       # INCONCLUSIVE: verdict only
  python3 tools/index_page.py --validate             # refresh verdicts + check
"""

import argparse
import collections
import glob
import datetime
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(REPO_ROOT, "index.json")


def load():
    with open(INDEX) as f:
        return json.load(f, object_pairs_hook=collections.OrderedDict)


def save(idx):
    # Stamp `updated` — but only when something else actually moved.
    #
    # This was hand-maintained and drifted: it sat at 2026-07-27 through a
    # publish of 16 new reviews, and a revert walked it BACKWARDS. A field
    # named `updated` that reports a date older than the change shipping with
    # it is the kind of small overclaim the rest of this repo refuses to make.
    #
    # The condition matters as much as the stamp. --validate routes through
    # here to refresh verdicts, so an unconditional bump would make a
    # read-only check produce a diff — a date that moves without an update is
    # the same lie in the other direction.
    try:
        with open(INDEX) as f:
            old = json.load(f, object_pairs_hook=collections.OrderedDict)
    except (OSError, ValueError):
        old = None

    def body(d):
        return json.dumps({k: v for k, v in d.items() if k != "updated"}, sort_keys=True)

    if old is None or body(old) != body(idx):
        # UTC, not local: the scheduled runs that touch this are UTC-clocked.
        idx["updated"] = datetime.datetime.now(datetime.timezone.utc).date().isoformat()

    with open(INDEX, "w") as f:
        json.dump(idx, f, indent=2)
        f.write("\n")


def verdict_of(path):
    with open(os.path.join(REPO_ROOT, path)) as f:
        m = re.search(r"^## verdict:\s*(.+)$", f.read(), re.M)
    return " ".join(m.group(1).split()) if m else None


# ---------------------------------------------------------------------------
# Machine-readable layer, derived from each page's own text — never authored
# here. The verdict prose stays verbatim in `verdicts`; `verdictClass` and
# `findings` are mechanical reads of it so a client can badge/filter without
# parsing prose. A page these rules cannot read is omitted (fail-soft: the
# app falls back to neutral copy) and warned about, so the fix is always
# "make the page's own wording conform", not "override it here".

CLASS_RULES = [
    (r"^leaks\b", "leaks"),
    (r"^compromisable\b", "compromisable"),
    (r"^inconclusive\b", "inconclusive"),
    (r"^qualified pass\b", "qualified-pass"),
    (r"^private\b", "private"),
    # older pages whose verdict lines open with scope wording instead of a
    # class token; all state "no content exposure at the audited config"
    (r"^(clean|core request path clean)\b", "private"),
    (r"^(metadata-only|telemetry-not-content|management-logs only)\b", "private"),
    (r"^management-only\b", "qualified-pass"),
]


def classify(verdict):
    v = verdict.strip().lower()
    for pat, cls in CLASS_RULES:
        if re.match(pat, v):
            return cls
    return None


SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO")
FINDING_RE = re.compile(
    r"^###\s+(CRITICAL|HIGH|MEDIUM|LOW|INFO)(?:-\d+)?\b(.*?)\s+—\s+(.+?)\s*$", re.M)
DEPLOYED_MAP = {"on": "on", "active": "on", "off": "off", "armed": "armed"}


def plain(s):
    """Markdown emphasis/backticks stripped for display fields."""
    return re.sub(r"[`*]", "", s).strip()


def slug(heading, seen):
    """GitHub's anchor for a rendered heading, with duplicate suffixing."""
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    t = re.sub(r"[`*_]", "", t).lower()
    t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
    n = seen.get(t, 0)
    seen[t] = n + 1
    return t if n == 0 else f"{t}-{n}"


def findings_of(path):
    with open(os.path.join(REPO_ROOT, path)) as f:
        text = f.read()
    text = re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)  # no headings in code fences
    seen, out = {}, []
    for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M):
        anchor = slug(m.group(2), seen)  # GitHub's duplicate counter spans ALL heading levels
        if m.group(1) != "###":
            continue
        fm = FINDING_RE.match(m.group(0))
        if not fm:
            continue
        sev, mid, title = fm.group(1), plain(fm.group(2)).strip(), plain(fm.group(3))
        qualifier = mid[1:-1].strip() if mid.startswith("(") and mid.endswith(")") else mid
        dm = re.search(r"deployed:\s*([A-Za-z]+)", qualifier)
        entry = collections.OrderedDict()
        entry["severity"] = sev.lower()
        entry["deployed"] = DEPLOYED_MAP.get(dm.group(1).lower()) if dm else None
        if qualifier:
            entry["qualifier"] = qualifier
        entry["title"] = title
        entry["anchor"] = anchor
        out.append(entry)
    return out


def refresh_verdicts(idx):
    """Every page's own verdict line, verbatim — plus the machine-readable
    layer (`verdictClass`, `findings`) mechanically derived from the page's
    own wording. Nothing synthesized here."""
    v = collections.OrderedDict()
    classes = collections.OrderedDict()
    findings = collections.OrderedDict()
    missing, unclassified = [], []
    for pat in ["images/**/sha256-*.md", "images/**/tag-*.md",
                "manifests/**/sha256-*.md", "os/sha256-*.md"]:
        for f in sorted(glob.glob(os.path.join(REPO_ROOT, pat), recursive=True)):
            rel = os.path.relpath(f, REPO_ROOT)
            got = verdict_of(rel)
            if got:
                v[rel] = got
                cls = classify(got)
                if cls:
                    classes[rel] = cls
                else:
                    unclassified.append(rel)
            else:
                missing.append(rel)
            page_findings = findings_of(rel)
            if page_findings:
                findings[rel] = page_findings
    idx["verdicts"] = v
    idx["verdictClass"] = classes
    idx["findings"] = findings
    for rel in unclassified:
        print(f"  WARN verdict line has no readable class (page omitted from "
              f"verdictClass; open the verdict with PRIVATE / LEAKS / COMPROMISABLE / "
              f"QUALIFIED PASS / INCONCLUSIVE): {rel}")
    return missing


def gate_for(page):
    """Infer the index entry from the page path — the path spec is a pure
    function of attested fields, so this direction works too."""
    p = page.rstrip("/")
    m = re.match(r"^images/(.+)/sha256-([0-9a-f]{64})\.md$", p)
    if m:
        return ("images", m.group(1), m.group(2))
    m = re.match(r"^images/(.+)/tag-(.+)\.md$", p)
    if m:
        return ("tagAudits", m.group(1), m.group(2))
    m = re.match(r"^manifests/measured/sha256-([0-9a-f]{64})\.md$", p)
    if m:
        return ("measured", None, m.group(1))
    m = re.match(r"^os/sha256-([0-9a-f]{64})\.md$", p)
    if m:
        return ("os", None, m.group(1))
    m = re.match(r"^manifests/(.+)/sha256-([0-9a-f]{64})\.md$", p)
    if m:
        return ("manifests", m.group(1) + ".yaml", m.group(2))
    return None


def validate(idx):
    problems = []
    built = [f"images/{r}/sha256-{d}.md" for r, ds in (idx.get("images") or {}).items() for d in ds]
    built += [f"images/{r}/tag-{t}.md" for r, ts in (idx.get("tagAudits") or {}).items() for t in ts]
    built += [f"manifests/{(k[:-5] if k.endswith('.yaml') else k)}/sha256-{s}.md"
              for k, ss in (idx.get("manifests") or {}).items() for s in ss]
    built += [f"manifests/measured/sha256-{m}.md" for m in (idx.get("measured") or [])]
    built += [f"os/sha256-{o}.md" for o in (idx.get("os") or [])]
    verdicts = idx.get("verdicts") or {}
    for b in built:
        if not os.path.exists(os.path.join(REPO_ROOT, b)):
            problems.append(f"gated link has no page on disk: {b}")
        elif b not in verdicts:
            problems.append(f"gated page has no verdict: {b}")
    on_disk = {os.path.relpath(f, REPO_ROOT)
               for pat in ["images/**/sha256-*.md", "images/**/tag-*.md",
                           "manifests/**/sha256-*.md", "os/sha256-*.md"]
               for f in glob.glob(os.path.join(REPO_ROOT, pat), recursive=True)}
    for extra in sorted(on_disk - set(built)):
        note = verdicts.get(extra, "")
        why = " (INCONCLUSIVE — correctly ungated)" if "INCONCLUSIVE" in note.upper() else \
              "  <-- ungated: intentional? if not, gate it"
        problems.append(f"page on disk, not gated: {extra}{why}") if "INCONCLUSIVE" not in note.upper() \
            else print(f"  note: {extra}{why}")
    return problems, len(built)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?", help="repo-relative path to the published page")
    ap.add_argument("--commit", metavar="REPO@SHA",
                    help="record a sources pin, e.g. sgl-project/sglang@49e384ce… "
                         "(only when identity is a real binding — see resolve_identity.py)")
    ap.add_argument("--no-gate", action="store_true",
                    help="record the verdict but do NOT gate a link (INCONCLUSIVE pages)")
    ap.add_argument("--validate", action="store_true", help="refresh verdicts and validate only")
    a = ap.parse_args()

    idx = load()

    if a.page:
        page = os.path.relpath(os.path.abspath(a.page), REPO_ROOT)
        if not os.path.exists(os.path.join(REPO_ROOT, page)):
            sys.exit(f"no such page: {page}")
        v = verdict_of(page)
        if not v:
            sys.exit(f"page has no '## verdict:' heading — every page must state one: {page}")
        print(f"page    : {page}")
        print(f"verdict : {v[:88]}")

        inconclusive = "INCONCLUSIVE" in v.upper()
        if inconclusive and not a.no_gate:
            sys.exit("\nREFUSING to gate an INCONCLUSIVE page.\n"
                     "  The app renders a gated link as 'source reviewed', which is a claim this\n"
                     "  page does not make. Re-run with --no-gate, and record the identity in\n"
                     "  acknowledged.json so the drift check stops counting it.")

        if a.no_gate:
            print("gate    : SKIPPED (verdict recorded only)")
        else:
            g = gate_for(page)
            if not g:
                sys.exit(f"cannot infer an index gate from this path: {page}")
            kind, key, val = g
            if kind in ("measured", "os"):
                idx.setdefault(kind, [])
                if val not in idx[kind]:
                    idx[kind].append(val)
            else:
                idx.setdefault(kind, collections.OrderedDict()).setdefault(key, [])
                if val not in idx[kind][key]:
                    idx[kind][key].append(val)
            print(f"gate    : {kind}" + (f"[{key}]" if key else "") + f" += {val[:16]}")

            if a.commit:
                if "@" not in a.commit:
                    sys.exit("--commit expects REPO@SHA")
                repo, sha = a.commit.rsplit("@", 1)
                if not re.fullmatch(r"[0-9a-f]{40}", sha):
                    sys.exit("--commit SHA must be a full 40-hex commit")
                if kind != "images":
                    sys.exit("--commit only applies to image pages")
                idx.setdefault("sources", collections.OrderedDict()).setdefault(key, collections.OrderedDict())
                idx["sources"][key][val] = {"repo": repo, "commit": sha}
                print(f"sources : {key} {val[:12]} -> {repo}@{sha[:12]}")

    missing = refresh_verdicts(idx)
    for m in missing:
        print(f"  WARN page has no '## verdict:' heading: {m}")
    problems, n = validate(idx)
    save(idx)

    print(f"\nindex.json: {n} gated link(s), {len(idx.get('verdicts') or {})} verdict(s)")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("validation: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
