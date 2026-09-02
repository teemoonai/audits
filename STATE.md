# Where things stand — 2026-08-04 (upstream-ask table extended 2026-09-02)

Working notes, not part of the published artifact. Delete when the open items close.
Written so the work does not depend on a chat session surviving.

## Repo state

| where | at | contains |
|---|---|---|
| `teemoonai/audits` **origin/main** | `b3c67e8` | **everything pushed 2026-08-04**: audit content, the `tools/` layer, the link repairs, and the machine-readable index (`verdictClass` + `findings`) |
| local `main` = `tooling-wip` | `b3c67e8` | in sync with origin/main |
| `teemoonai/teemoon-ios` **PR #1** | OPEN | the app change that surfaces verdicts |
| teemoon-ios local `main` | `59855c2` | 45 ahead / 34 behind origin — **unresolved divergence, not mine** |
| teemoon-ios `feat/audit-findings-surfacing` | `51ffb7a` (local, unpushed) | the full audit-surfacing UI: classes, findings rollup, everyday node, hero demotion — 36/36 tests |

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
4. ~~**The tier model contradicts itself.**~~ **Closed 2026-08-04**: README tier
   section rewritten to the transitive rule (*anything reachable from a published
   page moves with tier-1 care*), lineage READMEs classified tier 2, and tier 1 now
   states precisely what is frozen (paths, required keys, normalization) vs what
   evolves additively (page content, optional index keys).

Explicitly judged cargo cult for this repo, do not add: `CONTRIBUTING`, `CODEOWNERS`,
issue templates, `CHANGELOG`, a `docs/` split.

Judged correct, leave alone: `tools/` as a name, `acknowledged.json` at the root, the
identity-named page filenames, the frozen path spec.

## Generated-output shape review — 2026-08-04 (restriction lifted, decisions made)

The earlier organization review excluded the generated miniaudit files; that
exclusion is lifted. Outcomes:

- **Paths stay.** `images/ manifests/ os/` at root re-examined and kept: the repo
  name is the grouping level, the three dirs enumerate the attested coordinate
  spaces, and a container dir (`reviews/`) would add a permanent redundant URL
  segment. A move remains possible only until the app ships.
- **The "verbatim, never a client summary" rule is relaxed** (owner decision).
  Verdict prose still travels; clients may truncate/restyle but not soften.
- **Machine-readable layer added** (additive, `"schema": 1` unchanged):
  `verdictClass` (page path → private/leaks/compromisable/qualified-pass/
  inconclusive) and `findings` (page path → parsed `### SEVERITY (deployed: …) —
  title` headings with GitHub anchors). Extracted mechanically by
  `index_page.py` from each page's own wording — never authored in tooling;
  unreadable pages are omitted + warned (fail-soft to neutral in the app).
  Currently 133 findings across 19 pages; manifest pages use `### Check N`
  structure and contribute class+prose only, until future pages adopt the
  finding-heading house format (now required by the SKILL.md brief).
- **iOS scope EXECUTED** (teemoon-ios, local branch
  `feat/audit-findings-surfacing` @ `51ffb7a`, on top of the PR #1 change;
  unpushed): decode new keys + `updated` + validate `schema` (≠1 fails closed);
  dead `manifestAuditURL` wired (7 recipe reviews now render on the recipe
  card); `FableAuditBlock` badged by class + markdown + 3-line clip; per-node
  "plaintext egress" rollup (live vs latent vs collapsed info, anchor
  deep-links); staleness stamp; everyday-rung audit node (3 states, worst
  class wins) with "see the proof" rung-flip; hero demoted to advisory orange
  on `leaks` (never red, never send-gated; `incomplete` leaves hero alone).
  36/36 tests pass (AuditIndex, EgressRollup, AuditLinkScoping). Note:
  `modelNodeAuditState` recomputes `enclaveGroups` in the hero — acceptable at
  sheet-render frequency, a caching candidate if the sheet ever feels slow.
- **Everyday-rung decision (2026-08-04)**: one plain-language chain node, three
  states derived from `verdictClass` alone (worst class among the node's
  in-scope reviews): any `leaks` → alert ("this setup copies your prompts into
  its operator's logs" — what small-models shows today); all touchers gated
  private/qualified-pass → ok ("none of it is *set to* copy your words" — never
  "can't"); any ungated/inconclusive → neutral gray ("a gap in the checking,
  not an all-clear"). Placed after the identity node so a failed build check
  dims it; tap flips to expert's egress section; no external links at this rung.

## Live findings that need an upstream ask to near.ai

None of these can be fixed in this repo.

| fix | effect |
|---|---|
| `--admin-api-key` on sglang | closes the unauthenticated `/configure_logging` CRITICAL and ~30 other open admin routes. Re-confirmed 2026-08-17 at `fdebc938` (v0.5.16) and `c4271c3f` (nightly): route still `ADMIN_OPTIONAL`, no route anywhere is `ADMIN_FORCE`, and upstream's own FIXME in `http_server.py` says why. HiCache endpoints *are* hard-gated in the same file, which is what makes this an omission rather than a design position |
| `--allowed-media-domains` + `VLLM_MEDIA_URL_ALLOW_REDIRECTS=0` — **no longer just Qwen3-VL** | **widened 2026-08-17.** The v0.5.16 upgrade turned Qwen3.6-27B and Qwen3.6-35B-A3B multimodal (`Qwen3_5(Moe)ForConditionalGeneration`, both carry `vision_config`), and the nightly serves Qwen3.8-27B, also multimodal. All fetch request-supplied URLs with no allowlist and redirects on. Gemma-4 sets both controls in the same file, so the fix is two YAML lines already written next door |
| `--revision` on Qwen3.6 27B/35B and FLUX | stops unpinned model code executing in-enclave. Still open at `795aab85` (2026-08-17): both Qwen3.6 services run `--trust-remote-code` with no `--revision` while DeepSeek and Gemma pin. Now compounded — those models are read from `main`, so the multimodal config above can also change under them |
| ~~publish a build attestation for `compose-manager-launcher@d652f92b`~~ | **CLOSED 2026-08-17** by replacement, not by attestation. That digest is gone from the fleet; `91fdff3c` (4 nodes) and `78afb823` (2 nodes) both carry signed attestations and are audited and gated. `acknowledged.json` is now empty |
| move `FUSION_ENABLED` / `WEB_CONTEXT_SEARCH_*` into the attested compose | turns a vendor assertion into a verifiable fact |
| FLUX engine: prompt logging at INFO + generated images never deleted | the one *actual* leak found, not a latent one. Escalated to **CRITICAL** 2026-08-17 on `small-models.yaml@2443fde4`: the recipe's own otelcol-contrib ships that prompt log off-box to `telemetry.infra.near.ai`, so it is egress, not just a local log |
| pass `--watchdog-timeout` explicitly on every sglang service | **new 2026-08-17.** Upstream dropped the `watchdog_timeout` default from 1800 s to **300 s** (`server_args.py:1226` at `c4271c3f`). The hang-time prompt dump is undisableable, so any service not setting the flag is now armed at a 6x shorter trigger. DeepSeek sets it; the Qwen engines do not |
| set `ulimits: core: 0` (or a `core_pattern` sink) on every engine service | **new 2026-09-02** (drift #7). The upstream `dstack-nvidia-0.5.11` guest that `glm-5-3-flash` now boots has `CONFIG_COREDUMP=y`, no core-dump handler, and `LimitCORE=infinity` on both `docker.service` and `containerd.service`; no recipe sets a core ulimit, so a crashing engine writes its full memory image into its container layer on the data disk. Rated MEDIUM (ARMED) on the OS page; the fix is one compose line per engine |
| fix the glm47 tool-call parser's WARNING log (`glm47_moe_detector.py`, upstream and Phala fork) | **new 2026-09-02.** `Failed to parse '{value}' as number` prints a model-emitted argument value verbatim whenever it is not numeric; the recipe's otelcol ships it to `telemetry.infra.near.ai`. The only live content path on the GLM-5.3 engine page and the reason it is LEAKS rather than PRIVATE. Ask upstream sglang, not just Phala |
| pass `--allowed-media-domains` on GLM-5.3 (sglang now HAS the flag) and on Qwen3.6/3.8 once their builds carry it | **widened 2026-09-02.** The Phala fork at `26f67bd9` ships `download_remote_media` with an exact-hostname allowlist, manual redirects and a 64 MiB cap — but the flag defaults to empty and the recipe does not set it. On the v0.5.16 / nightly Qwen engines the mechanism does not exist yet |
| stop replaying the compose-manager image override at boot without a signature check (`pre_launch_script` on the 0.5.11 harnesses) | **new 2026-09-02.** `341313ae` / `c82b1a2e` read `/var/lib/docker/volumes/dstack_work/_data/.env.launcher` before compose and export `COMPOSE_MANAGER_IMAGE` unvalidated, so the measured digest is the first-boot value only. HIGH on both measured pages |
| vLLM: the shared parser engine logs tool-call argument prefixes at DEBUG with no flag (`vllm/parser/engine/parser_engine.py:948,984,1036` at `ffd46bfa`) | **new 2026-09-02.** OFF at `VLLM_LOGGING_LEVEL=INFO`; a single env change arms it. LOW on the `770fe65b` page |

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
