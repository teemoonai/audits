# tools

Three stdlib-only scripts. None of them writes a page: they detect, resolve and
gate; the claims are written by review and checked by a person. The procedure
that ties them together is [`RUNBOOK.md`](RUNBOOK.md) (driven by the
`/audit-drift` skill in `.claude/skills/audit-drift/`).

| script | question it answers | run |
|---|---|---|
| [`fleet_drift.py`](fleet_drift.py) | Is what near.ai is running still what this repo has reviewed? Fetches every host's live attestation, hash-checks the measured compose and the log-pinned recipe, diffs the in-scope identities against `index.json`. Exit 0 = nothing unaudited. | `python3 tools/fleet_drift.py [--json out.json]` — daily via `.github/workflows/fleet-drift.yml`, which files an issue on drift |
| [`resolve_identity.py`](resolve_identity.py) | What source tree is this image digest built from, and how strong is the binding? Walks signed attestation → OCI label → release tag → ARG fingerprint → UNRESOLVED and prints a reviewer-ready block. | `python3 tools/resolve_identity.py --brief <image>@sha256:<digest>` |
| [`index_page.py`](index_page.py) | Publish a finished page: infer its gate from the frozen path, refresh every page's verdict and finding headings into `index.json`, validate the whole index. Refuses to gate INCONCLUSIVE pages; `--commit` adds a `sources` pin only for a real digest→commit binding. | `python3 tools/index_page.py <page> [--commit repo@sha] [--no-gate]`, `--validate` |

Two cautions learned the hard way: run `index_page.py` only when no half-written
page is on disk (it reads every page's verdict line verbatim), and treat the
digests in a drift issue as a snapshot — the fleet redeploys mid-session.
