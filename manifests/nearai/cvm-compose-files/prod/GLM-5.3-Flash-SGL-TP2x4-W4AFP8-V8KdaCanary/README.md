# prod/GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V8KdaCanary.yaml

A one-service canary copy of [`GLM-5.3-Flash-SGL-TP2x4-W4AFP8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8/), generated from it by near.ai's `scripts/prepare_glm53_v8_kda_canary.py`: the whole fleet file with only `model-sg-glm53-w4afp8-tp2-r4` changed to the signed v8 engine build (`nearaidev/sglang@59700363…`, v7 plus one arithmetic patch) and its label strings. Deployed to gpu03 only, scoped to that one service, so the CVM runs a three-file patchwork: v8 on r4 from this file, v7 on r1-r3 from the plain file, sidecars from an older revision of the plain file. **Log-pinned**: keyed by
`file_sha256` against the signed compose-manager action log (commit + path +
file hash), not hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; a sibling review cites the plain file's page
for every block it proves byte-identical and still sweeps the whole file. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`c7c1bf4d82e1…`](sha256-c7c1bf4d82e137b8d2e0788f41cd6637b38bd08fdc74f38e87b4571ce0c8562e.md) | QUALIFIED PASS — **corrected 2026-10-12**: the glm47 engine finding this class rested on is withdrawn as unreachable (its except clause cannot run); was LEAKS — narrowly, unchanged in kind from the plain file's `a49d9c15` page: gpu03 r4 runs the v8 build on the same candidate argv (glm47 parser, no admin key) and every container's stdout still ships unscrubbed to telemetry.infra.near.ai; the canary adds no finding in kind; the running collector still labels r4's metrics with the v7 image id | 2026-10-12 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
