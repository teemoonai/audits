---
name: audit-drift
description: Close a fleet-drift issue in teemoonai/audits — resolve image identity, commission Fable source reviews, verify their load-bearing claims, and gate the pages in index.json. Use when the daily drift check has filed an issue, when something in-scope is running with no audit page, or when asked to audit a new near.ai image, deployment config, or model-layer recipe.
---

# Closing a fleet-drift issue

You are the orchestrator. You do **not** write the reviews — the pages in this
repo are published as "independent AI source review, Fable", so a page you wrote
yourself would make that attribution false. Your job is the four steps around the
review: establish identity, commission it, verify it, publish it.

Read [`tools/README.md`](../../../tools/README.md) before starting. It has the
reasoning; this file has the mechanics.

## 1. Read the issue and triage

`gh issue list --label fleet-drift` then read it. Sort targets by blast radius —
an engine that sees plaintext on nine hosts outranks a telemetry sidecar on one.
Ignore the **KNOWN OPEN** section; those are recorded in
`acknowledged.json` and are backlog, not alarm.

## 2. Resolve identity — before commissioning anything

```bash
python3 tools/resolve_identity.py --brief <image>@sha256:<digest>
```

A review keyed to the wrong tree is worse than no review. Never let an agent go
hunting for its own target — that is how budget evaporates with nothing to show.

If it reports **UNRESOLVED**, skip to step 6.

## 3. Commission the review

Spawn one agent per target with the **Agent tool**, `subagent_type:
"general-purpose"`, **`model: "fable"`**. Never more than **3 concurrent** — a
wider fan-out has hit the session limit twice, the second time losing seven
agents' work.

For a deployment config or recipe manifest, the target is a document rather than
an image: skip step 2 and say so in the brief (`method.md` §4 is the method —
no upstream source reading).

### Brief template

Fill every placeholder. Do not shorten the Rules section.

A real brief, exactly as sent — the one that produced the CRITICAL
`/configure_logging` finding — is in [`example-brief.md`](example-brief.md),
with notes on the two things about it worth copying and the two instructions
added to the template after it.

```
INDEPENDENT privacy source audit for the public repo `teemoonai/audits`,
published verbatim as "independent AI source review, Fable".

REPO ROOT: <absolute path to this repo>
Read first: `notes/method.md`, `notes/audit-surface.md` (the checklist — walk
it), `README.md` (scope rule + frozen path spec), and <a recent page of the
same kind> for house format. Match that format exactly.

## The question
Can anything exfiltrate the user's plaintext chat messages? Plaintext is
visible ONLY to (a) the user and (b) the inference engine process. Any copy
reaching a log, file, DB, cache, crash dump, telemetry exporter, or non-model
network destination is a FINDING.

## Target — identity is GIVEN, do not re-derive
<paste the block resolve_identity.py --brief printed, including the identity
class and its caveat>

## Where it runs
<service name(s)> in <compose file>, on disk at <path>. READ IT and follow the
YAML anchors for the real command and env. Note where this container's stdout
goes (`com.datadoghq.ad.logs` labels, the otel sidecar config).
<For an already-audited image at a new digest: this is a DELTA. Name the base
page, enumerate the diff, and say which findings carry over and which are new.>

## Priority items
<the 2-4 things that matter most for this target — e.g. for sglang: the
unauthenticated /configure_logging endpoint and the watchdog dump_info prompt
dump; confirm or refute at YOUR commit, do not assume they transfer>

## Rules
- EVERY file:line MUST be verified by fetching the file and confirming the line
  number and content. Never guess a line number.
- Distinguish "OFF at deployed flags" from "cannot happen". Severity reflects
  the DEPLOYED state, plus what would activate it.
- A control outside this image is a RESIDUAL, not a mitigation.
- Never assert safety you did not verify. State untraced areas explicitly under
  "Not traced" — that section is load-bearing.
- If identity or source is unavailable, write an INCONCLUSIVE page that makes NO
  privacy claim. Failing closed is a correct outcome, not a failure.
- review line: `reviewed <YYYY-MM-DD> (independent AI source review, Fable —
  method: [/notes/method.md](/notes/method.md))`
- The `## verdict:` line must OPEN with its class token — PRIVATE / LEAKS /
  COMPROMISABLE / QUALIFIED PASS / INCONCLUSIVE — and contain no markdown.
  The indexer machine-reads it into `verdictClass`; a line it cannot read
  ships to the app as an unbadged neutral verdict.
- Each finding is a heading of the exact shape
  `### <CRITICAL|HIGH|MEDIUM|LOW|INFO> (deployed: <ON|OFF|ARMED>[, qualifier]) — <title>`
  with the title in plain text and naming the sink (log / disk / telemetry /
  egress). The indexer machine-reads these into `findings`, which the app
  renders as the node's plaintext-egress list — a finding in prose under a
  differently-shaped heading is invisible to the app.
- Plain ASCII in fenced code blocks; no HTML entities.

## Efficiency
`grep -n` with targeted patterns. NEVER `cat` a file larger than ~300 lines —
that is the dominant token cost. One Write per page.

## Output
Write the page yourself with the Write tool to:
  <exact repo-relative path, from the frozen path spec>
Write it AS SOON AS the findings exist and refine in place — an interrupted run
loses only unwritten pages. Do NOT edit index.json; the orchestrator gates links
after verifying.

Then return ONLY a compact summary (max 20 lines): the one-line verdict, finding
headlines with severity and deployed state, and any claim you want the
orchestrator to re-verify independently. Do NOT paste the page contents back.
```

## 4. Verify before publishing — do not skip

The agent's summary is a claim, not evidence. Check, in priority order:

1. the finding the verdict rests on
2. anything the agent asked you to re-verify
3. anything contradicting a published page — settle it at the source, then
   correct the older page with a **dated addendum**, not a rewrite
4. novel findings the brief did not prime it for
5. anything changing severity, gating, or whether a `sources` pin is earned

Verify **chains hop by hop**, not at the conclusion. Verify **negative claims**
against a whole tree at the right commit. When a check surprises you, look at
what actually matched before acting on it. See the runbook for worked examples.

## 5. Publish

```bash
python3 tools/index_page.py <page> --commit <repo>@<full-40-hex-sha>
```

`--commit` only when identity is a real binding (signed attestation, OCI label,
release tag). A bracketed range is not a pin.

Then commit and push. The next scheduled run closes the issue.

## 6. When identity cannot be established

1. Commission an INCONCLUSIVE page that makes no privacy claim, recording how
   absence was established — a **positive control in the same run** is what
   separates "genuinely absent" from "we looked in the wrong place".
2. `python3 tools/index_page.py <page> --no-gate`
3. Add it to `acknowledged.json` with a reason and `closes_when`, so it
   stops counting as drift.

## What you must not do

- **Do not write a review yourself.** The attribution on every page says Fable.
- **Do not gate an INCONCLUSIVE page.** A gated link renders as "source
  reviewed", which is a claim such a page does not make. `index_page.py` refuses.
- **Do not add a `sources` pin for a bracketed identity.** The app renders
  `sources` as a verified digest→commit binding.
- **Do not publish an agent's claim you have not checked**, however confident the
  summary sounds.
