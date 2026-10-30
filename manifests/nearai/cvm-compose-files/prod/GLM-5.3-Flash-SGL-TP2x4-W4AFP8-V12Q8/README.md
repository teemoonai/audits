# prod/GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8.yaml

The **v12 / Q8-DSA** successor of
[`GLM-5.3-Flash-SGL-TP2x4-W4AFP8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8/) for the two
`glm-5-3-flash` CVMs (gpu03, gpu04): four TP2/EP2 replicas on near.ai's signed
[`nearaidev/sglang`](../../../../../images/docker.io/nearaidev/sglang/) v12 build with
`--dsa-prefill-backend flashmla_sparse_q8` on every replica and the HiCache-off
"candidate" argv, the E2EE proxy, nginx, the registrar, the ghost-cache sidecar,
dcgm and the collector. On gpu04 the `sage` project that had held GPU 6 (see
[`…-gpu04`](../GLM-5.3-Flash-SGL-TP2x3-W4AFP8-gpu04/)) was taken down on 2026-10-24
and the four-replica lineage redeployed; this file then replaced replicas r1-r3 there,
while r4 was last created by a pageless canary file (`Q8Canary.yaml`) with the same
engine image and command.

Identity for every revision below is **log-pinned**: the file's `file_sha256`
against the signed compose-manager action log (commit + path + file hash), not
hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; a sibling review cites the sibling's page for
every block it proves byte-identical and still sweeps the whole file. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`904054f502cc…`](sha256-904054f502ccdb2f913d6b80f156ea658b8bc5cb6f8af06082723581d62a45c0.md) | QUALIFIED PASS — sibling review of `a49d9c15` (`7ee4a4c7`, v0.0.521): the four replicas and the sidecar move to the signed v12 engine `da8d4e4b`, `--dsa-prefill-backend flashmla_sparse_q8` on the HiCache-off candidate argv, the proxy to `e4a42b32`; nothing else in 1861 lines differs; the sibling's CRITICAL (`/configure_logging` on the shared bridge; web search ARMED), HIGHs (fusion ARMED, 1800 s watchdog dump, unscrubbed export) and MEDIUMs carry; gpu04 runs r1-r3 from this file and r4 from a pageless canary with the same resolved block, gpu03 runs r1-r4 from this file under a proxy from an unaudited canary revision with an identical block; both aggregators are v7 leftovers; two readings stated for every beside-recipe container | 2026-10-30 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
