# prod/GLM-5.3-Flash-SGL-TP2x4-W4AFP8.yaml

Inner (model-layer) compose for z-ai/glm-5.3-flash on the W4AFP8 weights — four sglang TP2 replicas behind one proxy, on near.ai's signed `nearaidev/sglang` HiCache build; the only recipe that turns the admission reserve on. Serves `glm-5-3-flash` from two CVMs (gpu04, gpu03). A new file path on 2026-10-01; its nearest audited relative is [`GLM-5.3-Flash-SGL-TP4`](../GLM-5.3-Flash-SGL-TP4/). **Log-pinned**: keyed by
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
| [`5745db6b0d3e…`](sha256-5745db6b0d3e4a4f1ff6872acbf90da254ef83ca834c0bfd4cffb86f540ff781.md) | LEAKS — narrowly: the glm47 parser warning on four replicas, shipped unscrubbed to telemetry.infra.near.ai; first audited revision, reviewed whole | 2026-10-02 |
| [`e3c487c72189…`](sha256-e3c487c72189010f5afadc486c8c04ffb3a49a4d485827844e7c8fd105729359.md) | LEAKS — narrowly, unchanged in kind: delta against `5745db6b`; two mamba-state flags raise the running cap from 15 to 32 per replica (engine side not traced), so the armed watchdog dump can carry more; engines run this hash, sidecars the base | 2026-10-04 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
