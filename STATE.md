# Where things stand — 2026-08-04

Working notes, not part of the published artifact. Delete when the open items close.
Written so the work does not depend on a chat session surviving.

## Repo state

| where | at | contains |
|---|---|---|
| `teemoonai/audits` **origin/main** | `a659360` | the audit content only — 26 pages, `index.json`, corrections |
| **`tooling-wip`** (local, unpushed) | `49e3c4f` | everything below plus the `tools/` restructure |
| `teemoonai/teemoon-ios` **PR #1** | OPEN | the app change that surfaces verdicts |
| teemoon-ios local `main` | `59855c2` | 45 ahead / 34 behind origin — **unresolved divergence, not mine** |

`tooling-wip` holds, and public main does not:

```
tools/fleet_drift.py        daily drift detector
tools/resolve_identity.py   evidence-ladder identity resolution
tools/index_page.py         gate a page + refresh verdicts + validate
tools/README.md             the runbook (misnamed — see open items)
acknowledged.json           knowingly-unaudited identities (root, deliberately)
.github/workflows/fleet-drift.yml
.claude/skills/audit-drift/ SKILL.md + example-brief.md
notes/audit-surface.md      the reviewer's checklist
```

Plus **fixes to live public content that are still unpushed**: `notes/method.md`
pointed at `PRIVACY_AUDIT_RESULTS.md`, which does not exist, and it is linked from
all 38 pages; 7 pages had link text naming a renamed file; `notes/ARCHITECTURE.md`
linked two pages that were never published. Those are repairs to broken links in the
published artifact and are independent of the tooling question.

## Open items, ranked (from the 2026-08-04 organization review)

1. **`manifests/measured/` has no README** — eight opaque hashes, no map from hash to
   node. Called the worst orientation spot in the tree. Also `images/docker.io/nearaidev/sglang/`
   has no lineage README while every sibling ref does, and sits beside
   `images/docker.io/lmsysorg/sglang/` with nothing explaining the relationship.
   Only **1 of 7** `manifests/nearai/cvm-compose-files/prod/*/` dirs has one — a
   half-applied pattern reads as an oversight.
2. **`tools/README.md` is a runbook.** Renaming `RUNBOOK.md` was a mistake: GitHub
   renders it as the directory's face and it opens `# Runbook: a fleet-drift issue
   just opened`, so a browsing reader thinks something is on fire. Restore
   `tools/RUNBOOK.md`; make `README.md` a short index of the three scripts.
3. **`SECURITY.md`** — genuinely earns its place: this repo publishes security
   verdicts about someone else's stack and states no disclosure channel. **Code
   license gap:** `LICENSE.md` is CC BY 4.0 "for documentation"; `tools/*.py` is now
   unlicensed.
4. **The tier model contradicts itself.** README says notes beyond method/ARCHITECTURE/
   audit-surface are "editorial and may be reorganised freely", but the chain
   38 pages → `method.md` → `audit-surface.md` → `reviewer-comparison-2026-08-03.md`
   makes the last frozen in practice. Honest rule: *anything transitively reachable
   from a published page*. Also: lineage `README.md` files inside tier-1 directories
   are unclassified — they are linkable but not code-addressed.

Explicitly judged cargo cult for this repo, do not add: `CONTRIBUTING`, `CODEOWNERS`,
issue templates, `CHANGELOG`, a `docs/` split.

Judged correct, leave alone: `tools/` as a name, `acknowledged.json` at the root, the
identity-named page filenames, the frozen path spec.

## Live findings that need an upstream ask to near.ai

None of these can be fixed in this repo.

| fix | effect |
|---|---|
| `--admin-api-key` on sglang | closes the unauthenticated `/configure_logging` CRITICAL and ~30 other open admin routes |
| `--allowed-media-domains` + `VLLM_MEDIA_URL_ALLOW_REDIRECTS=0` on Qwen3-VL | two YAML lines already written for Gemma-4 in the same file |
| `--revision` on Qwen3.6 27B/35B and FLUX | stops unpinned model code executing in-enclave |
| publish a build attestation for `compose-manager-launcher@d652f92b` | the only unauditable component, on 10 of 17 hosts |
| move `FUSION_ENABLED` / `WEB_CONTEXT_SEARCH_*` into the attested compose | turns a vendor assertion into a verifiable fact |
| FLUX engine: prompt logging at INFO + generated images never deleted | the one *actual* leak found, not a latent one |

## Known residue

`teemoonai/audits` PR #1 permanently reads "Merged" though its commits are not on
`main`; GitHub cannot delete a PR. Caused by force-pushing past a merge. One
explanatory comment is on the PR. Three tooling files stay publicly readable at
`refs/pull/1/head` regardless of `main`.

## How the loop is meant to run

`tools/RUNBOOK.md` and `.claude/skills/audit-drift/` are the real documentation.
In short: the daily workflow files an issue → `resolve_identity.py --brief` on each
target → commission Fable reviews (max 3 concurrent, they write pages to disk
themselves) → **verify the load-bearing claims yourself** → `index_page.py` → push.

The verification step is not optional. On the run that produced these pages it caught
a truncated attestation lookup, an over-rated severity, a wrong conclusion about a
telemetry sidecar, and a finding that had to be refuted outright.
