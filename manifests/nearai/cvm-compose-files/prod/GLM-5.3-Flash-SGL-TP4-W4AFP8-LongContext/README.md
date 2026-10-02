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
| [`09cbbffd508d…`](sha256-09cbbffd508d7f0037f34fde22cbda57a45c950c1f91ac86ccff4e57cf7055fe.md) | LEAKS — narrowly: the glm47 parser warning on both replicas, shipped unscrubbed to telemetry.infra.near.ai; heavy patchwork — this hash created only nginx and the proxy on one CVM; first audited revision, reviewed whole | 2026-10-02 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
