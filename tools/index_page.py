#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
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
import subprocess
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


def strip_fences(text):
    return re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)


def verdict_of(path):
    with open(os.path.join(REPO_ROOT, path)) as f:
        m = re.search(r"^## verdict:\s*(.+)$", strip_fences(f.read()), re.M)
    return " ".join(m.group(1).split()) if m else None


# A reviewer's skeleton page carries a verdict line that is a promise, not a
# claim. The indexer once shipped one of those as a verdict (2026-10, see the
# RUNBOOK). A line that reads like a placeholder is refused outright.
PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|placeholder|skeleton|pending review|in progress|to be written)\b", re.I)


def body_verdict_of(path):
    """The first bold token of the page's `## Verdict` section, or None when the
    page has no such section or it does not open with one. The heading line is
    what the app reads; the body is what a reader sees first. They must agree."""
    with open(os.path.join(REPO_ROOT, path)) as f:
        text = strip_fences(f.read())
    m = re.search(r"^## Verdict\s*$", text, re.M)
    if not m:
        return None
    for line in text[m.end():].split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            return None
        b = re.search(r"\*\*(.+?)\*\*", line)
        return b.group(1) if b else None
    return None


def checked_of(path):
    """Date the page's text last changed, from git — the evidence date a client
    can show beside `updated` (which is only the index body's change date).
    None when git cannot answer (no repo, or a shallow CI clone whose history
    would attribute every page to HEAD's date)."""
    try:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=REPO_ROOT,
                                 capture_output=True, text=True).stdout.strip()
        if shallow != "false":
            return None
        dirty = subprocess.run(["git", "status", "--porcelain", "--", path], cwd=REPO_ROOT,
                               capture_output=True, text=True).stdout.strip()
        if dirty:
            return datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=REPO_ROOT,
                             capture_output=True, text=True).stdout.strip()
        return out or None
    except OSError:
        return None


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
    # No prose fallbacks. Until 2026-11-06 "clean", "metadata-only",
    # "telemetry-not-content" and "management-logs only" mapped to `private`,
    # which badged a page with an ARMED token-ID leak and a page with a
    # CRITICAL/HIGH pair as PRIVATE in the app. A verdict line that does not
    # open with its class token is now a validation failure, not a guess.
]


def classify(verdict):
    v = verdict.strip().lower()
    for pat, cls in CLASS_RULES:
        if re.match(pat, v):
            return cls
    return None


# A LEAKS verdict says that plaintext reaches a sink; it does not say how much
# or how often. The app used to render every LEAKS as "copies what you type",
# which overstated a one-value-per-rare-trigger finding as wholesale logging.
# A LEAKS page therefore carries one more machine-read line, directly under
# the verdict:
#
#     ## exposure: <scope> — <one plain-text sentence: what leaks, and when>
#
# with <scope> one of:
#   wholesale    every request's content (or every reply) reaches the sink
#   conditional  content reaches the sink only on a stated trigger, and then
#                one bounded piece of it (a value, a field, a truncated reply)
#   metadata     no message content; identifiers, sizes, timings, labels
#
# The sentence after the dash is the page's own wording and is shipped
# verbatim; nothing is synthesized here. A LEAKS page without the line is
# warned about and omitted — the app falls back to neutral copy.
#
# A recipe page also names the compose services that carry the leak, on the
# line directly under it, so a client can tell a leak on the chat's own path
# from a sibling service in the same file (the FLUX engine beside the Qwen
# and GLM replicas in small-models, 2026-11-06):
#
#     ## exposure-services: <service>[, <service>...]
#
# copied to `exposure[page].services`, with `scope_kind: "recipe"`. An image
# page's scope is the image itself (`scope_kind: "image"`, no services): its
# leak is on the path when a path service runs that image. The client computes
# the path from the ingress config, the proxy's backend list and the running
# table (README, "exposure"); a gated LEAKS recipe page without a readable
# services line fails --validate.
EXPOSURE_SCOPES = ("wholesale", "conditional", "metadata")
SERVICE_NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*")


def exposure_of(path):
    with open(os.path.join(REPO_ROOT, path)) as f:
        text = f.read()
    m = re.search(r"^## exposure:\s*(.+)$", text, re.M)
    if not m:
        return None, "no '## exposure:' line"
    line = " ".join(m.group(1).split())
    sm = re.match(r"(\w+)\s*[—-]\s*(.+)$", line)
    if not sm or sm.group(1).lower() not in EXPOSURE_SCOPES:
        return None, f"exposure line does not open with one of {EXPOSURE_SCOPES}: {line[:60]}"
    entry = collections.OrderedDict()
    entry["scope"] = sm.group(1).lower()
    entry["summary"] = plain(sm.group(2))
    entry["scope_kind"] = "recipe" if path.startswith("manifests/") else "image"
    if entry["scope_kind"] == "recipe":
        sv = re.search(r"^## exposure-services:\s*(.+)$", text, re.M)
        if sv:
            names = [n.strip() for n in sv.group(1).split(",") if n.strip()]
            if not names or any(not SERVICE_NAME_RE.fullmatch(n) for n in names):
                return None, ("exposure-services line is not a comma-separated list of compose "
                              f"service names: {sv.group(1)[:60]}")
            entry["services"] = names
    return entry, None


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
    exposure = collections.OrderedDict()
    findings = collections.OrderedDict()
    missing, unclassified, unscoped = [], [], []
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
                exp, why = exposure_of(rel)
                if exp:
                    exposure[rel] = exp
                elif cls == "leaks":
                    unscoped.append((rel, why))
            else:
                missing.append(rel)
            page_findings = findings_of(rel)
            if page_findings:
                findings[rel] = page_findings
    idx["verdicts"] = v
    idx["verdictClass"] = classes
    idx["exposure"] = exposure
    idx["findings"] = findings
    checked = collections.OrderedDict()
    for rel in v:
        d = checked_of(rel)
        if d:
            checked[rel] = d
    if checked:
        idx["checked"] = checked          # page path -> YYYY-MM-DD, same keys as `verdicts`
    elif v:
        print("  WARN git history unavailable (shallow clone?) — `checked` left as loaded")
    derive_projects(idx)
    for rel in unclassified:
        print(f"  WARN verdict line has no readable class (page omitted from "
              f"verdictClass; open the verdict with PRIVATE / LEAKS / COMPROMISABLE / "
              f"QUALIFIED PASS / INCONCLUSIVE): {rel}")
    for rel, why in unscoped:
        print(f"  WARN LEAKS page has no readable exposure scope (page omitted from "
              f"exposure; the app falls back to neutral copy) — {why}: {rel}")
    return missing


def derive_projects(idx):
    """`projects.status` used to be hand-written and said "pinned by tag · can
    drift" about a project with two digest-gated pages. The pinning facts are
    in the gates; derive them, and keep the hand-written sentence under `note`
    so it is visibly a human claim, not a mechanical one."""
    for ref, proj in (idx.get("projects") or {}).items():
        digests = (idx.get("images") or {}).get(ref, [])
        tags = (idx.get("tagAudits") or {}).get(ref, [])
        parts = []
        if digests:
            parts.append(f"{len(digests)} build(s) reviewed by digest")
        if tags:
            parts.append(f"tag page(s) {', '.join(tags)} — a tag can drift")
        if not parts:
            parts.append("no gated page")
        old = proj.get("status")
        if old and "note" not in proj and old != "; ".join(parts):
            proj["note"] = old
        proj["status"] = "; ".join(parts)


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
    classes = idx.get("verdictClass") or {}
    findings = idx.get("findings") or {}
    for b in built:
        if not os.path.exists(os.path.join(REPO_ROOT, b)):
            problems.append(f"gated link has no page on disk: {b}")
            continue
        if b not in verdicts:
            problems.append(f"gated page has no verdict: {b}")
            continue
        note = verdicts[b]
        if b not in classes:
            problems.append(f"gated page's verdict line opens with no class token "
                            f"(PRIVATE / LEAKS / COMPROMISABLE / QUALIFIED PASS): {b}: {note[:60]}")
        elif classes[b] == "inconclusive":
            problems.append(f"gated page is INCONCLUSIVE — revoke the gate (--no-gate): {b}")
        if PLACEHOLDER_RE.search(note):
            problems.append(f"gated page's verdict line reads like a placeholder: {b}: {note[:60]}")
        body = body_verdict_of(b)
        if body is not None:
            bc = classify(body)
            if bc and b in classes and bc != classes[b]:
                problems.append(f"heading class {classes[b]} but the body's ## Verdict opens "
                                f"{bc.upper()}: {b}")
        if classes.get(b) == "leaks" and b not in (idx.get("exposure") or {}):
            problems.append(f"gated LEAKS page has no readable '## exposure:' line — the app would fall back "
                            f"to generic copy that understates a leak: {b}")
        elif classes.get(b) == "leaks" and b.startswith("manifests/") and \
                not (idx.get("exposure") or {}).get(b, {}).get("services"):
            problems.append(f"gated LEAKS recipe page has no readable '## exposure-services:' line — the app "
                            f"cannot tell a leak on the chat's path from a sibling service: {b}")
        for fnd in findings.get(b, []):
            if fnd["severity"] in ("critical", "high", "medium") and fnd["deployed"] is None:
                problems.append(f"{fnd['severity'].upper()} finding without a readable deployed: "
                                f"field (ON/OFF/ARMED): {b} — {fnd['title'][:50]}")
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

    before = json.dumps({k: v for k, v in idx.items() if k != "updated"}, sort_keys=True)
    missing = refresh_verdicts(idx)
    for m in missing:
        print(f"  WARN page has no '## verdict:' heading: {m}")
    problems, n = validate(idx)
    if a.validate:
        # Read-only: report, never write. A page edited without re-running the
        # indexer (an addendum that moved a heading) shows up here as a stale
        # index — the 2026-11-06 case the app would otherwise never see.
        after = json.dumps({k: v for k, v in idx.items() if k != "updated"}, sort_keys=True)
        if before != after:
            problems.append("index.json is stale against the pages on disk — run the indexer and commit")
    else:
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
