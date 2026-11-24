# prod/pack-glm-53-flash-pd2-long.yaml

A **new file path** of 2026-11-20 for z-ai/glm-5.3-flash on the gpu23 CVM
(hosts `glm-5-3-flash` and `glm-5-3-flash-long`, measured harness
[`fb81c6f2`](../../../../measured/sha256-fb81c6f2c1eae762ece8912e1f50e80697964cc93a112da03834369fa1ab5b0b.md)):
one vLLM prefill/decode pair on GPUs 0-3 behind near.ai's
[prefill/decode router](../../../../../images/docker.io/nearaidev/vllm/sha256-cc0066b599ab2d2c75a4b06ed7df4711cb181d110d5448dde894e17661e4c405.md)
for the base tier, and two SGLang TP2 long-context replicas on GPUs 4-7 behind a
second E2EE terminator for the long tier (advertised as `z-ai/glm-5.3-flash-long`);
nginx, two registrars, the collector, dcgm, a downloader and a one-shot egress
probe. Every engine is declared on an `internal: true` network. It replaced the
[`GLM-5.3-Flash-SGL-TP4-W4AFP8-LongContext`](../GLM-5.3-Flash-SGL-TP4-W4AFP8-LongContext/)
stack's front door on that CVM; that file's two long replicas still serve the long
tier there (see the pages).

Identity for every revision below is **log-pinned**: the file's `file_sha256`
against the signed compose-manager action log (commit + path + file hash), not
hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; later ones are usually **delta reviews**
against the previous audited revision and say so in their coverage note. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`c9c477286e51…`](sha256-c9c477286e5132f5ff0ddb2cce5187ce1db6028108ae52a959f68f264faefbac.md) | QUALIFIED PASS — for the ten containers this revision last created on gpu23 (nginx, proxy-glm53, proxy-glm53-long, pd-router-glm53-a, sidecar-glm53-netns-a, model-proxy-registrar-long, otelcol-contrib, dcgm-glm53, and the exited one-shots … | 2026-11-24 |
| [`6a4001e90fd5…`](sha256-6a4001e90fd5fdfea26d999f23e6db2d3ef315b0e6d0d1388e3481c5550d2f18.md) | QUALIFIED PASS — for the five containers this revision last created on gpu23 (model-vllm-glm53-a-prefill0, -prefill1, -decode0, -decode1 and model-proxy-registrar) and scoped to them: a nine-hunk delta from the c9c47728 page … | 2026-11-24 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
