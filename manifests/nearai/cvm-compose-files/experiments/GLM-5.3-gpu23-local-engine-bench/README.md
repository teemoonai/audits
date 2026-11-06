# experiments/GLM-5.3-gpu23-local-engine-bench.yaml

A benchmarking file, not a serving recipe: sixteen revisions were upped on the glm-5-3-flash-long CVM
(gpu23) between 2026-09-11T20:47Z and 2026-09-12T05:10Z to compare GLM-5.3 engine arms (a plain
`lmsysorg/sglang` control, a near.ai HiCache build, a vLLM arm) with a host-memory probe, a HiCache
verifier, a host-metrics exporter, a dcgm exporter and its own collector. Every engine arm was downed by
name before the bench ended; what the signed log still attributes to the file is an exited probe, the
exporter and the dcgm exporter, whose liveness the log cannot decide (the next up of another file either
removed them as orphans or left them — the per-deploy compose project is unrecorded).

Identity for every revision below is **log-pinned**: the file's `file_sha256` against the signed
compose-manager action log (commit + path + file hash), not hardware-measured; the measured layer is the
gpu23 node harness under [`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links; the three engine images this file names have no page and are
named as such.

Revisions are listed oldest first. The verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`dab6a4a4bd92…`](sha256-dab6a4a4bd927136b20851908dce43ea2f5e245906beb850324200c621219b42.md) | QUALIFIED PASS — the a509edf7 page's class for the a509edf7 page's reasons, re-read at this revision's lines: at the state the signed gpu23 log attributes to this file, no container that can see message plainte… | 2026-11-06 |
| [`a509edf733e5…`](sha256-a509edf733e54a3cb433c0b5d910d2df8fddd0dcbda0dc87424b7ae4257eefe4.md) | QUALIFIED PASS — at the state the signed gpu23 log attributes to this file, no container that can see message plaintext runs from it: every engine arm (the only services that would handle requests) was downed b… | 2026-11-06 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
