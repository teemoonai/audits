# prod/GLM-5.3-Flash-SGL-TP4-W4AFP8-LongContext.yaml

Inner (model-layer) compose for z-ai/glm-5.3-flash, long-context tier, on the W4AFP8 weights — two sglang TP4 replicas with a host-RAM HiCache tier, on near.ai's signed `nearaidev/sglang` HiCache build. Serves `glm-5-3-flash-long` from two CVMs (gpu02, gpu23). A new file path in 2026-09; its nearest audited relative is [`GLM-5.3-Flash-SGL-TP4`](../GLM-5.3-Flash-SGL-TP4/). **Log-pinned**: keyed by
`file_sha256` against the signed compose-manager action log (commit + path +
file hash), not hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; later ones are usually **delta reviews**
against the previous audited revision and say so in their coverage note. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`09cbbffd508d…`](sha256-09cbbffd508d7f0037f34fde22cbda57a45c950c1f91ac86ccff4e57cf7055fe.md) | QUALIFIED PASS — **corrected 2026-10-12**: the glm47 engine finding this class rested on is withdrawn as unreachable (its except clause cannot run); was LEAKS — narrowly: the glm47 parser warning on both replicas, shipped unscrubbed to telemetry.infra.near.ai; heavy patchwork — this hash created only nginx and the proxy on one CVM; first audited revision, reviewed whole | 2026-10-02 |
| [`b4006c232e5d…`](sha256-b4006c232e5d5820ebcd73789f2a2afd684071c11e43cc92512182b618e0045d.md) | QUALIFIED PASS — **corrected 2026-10-12**: the glm47 engine finding this class rested on is withdrawn as unreachable (its except clause cannot run); was LEAKS — narrowly, unchanged in kind: delta against `09cbbffd`; four new TP2 replicas on the signed v7 build fa730e6e (FP8 KV, HiCache on at 325 GiB each, ghost prefix cache — LOW, preprocess pool, tool-schema caps) serve the tier, the TP4 pair is re-declared on the v6 build 9c6ddd43 but has been down since 2026-10-06; the running proxy is from an unaudited revision whose default backend pool names those two down engines and whose real pool is an unlogged env (MEDIUM) | 2026-10-12 |
| [`f77f4b5dd41f…`](sha256-f77f4b5dd41f4e322d2194a3d0774235a2686c5d7105e24bc1b800b4a4842196.md) | QUALIFIED PASS — `4addbf4e` (v0.0.492): the b4006c23 document with the engine moved to v10 `c15a3367` and two scheduling flags per TP2 replica (16K chunks, `flashmla_sparse_q8` prefill — the Q8 patch is live here); no new sink; today the gpu23 CVM serves it (engines from this hash, proxy `d61357da` from an older revision, a five-revision patchwork), the gpu02 CVM took it down whole on 2026-10-21 | 2026-10-22 |
| [`94580ae74c8a…`](sha256-94580ae74c8a903cf3ca7c039d8e2465c05692bc7e283de6459eb9061ddb10a7.md) | QUALIFIED PASS — `8977a0e8` (v0.0.502): f77f4b5d plus the proxy anchor moved to `e4a42b32` (one commit: a bounded client result count on web search); brought up project-wide on the gpu02 CVM 2026-10-22T01:10Z, every container from this hash; the declared v6 TP4 pair ran for 112 s and was downed | 2026-10-22 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
