# prod/small-models.yaml

Inner (model-layer) compose for the small-models cluster — a dozen model containers (gpt-oss, Qwen3-VL, Qwen3.6, embeddings, reranker, Whisper, FLUX, privacy filter) behind one proxy each; the fleet's widest recipe. **Log-pinned**: keyed by
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
| [`a385f19a5105…`](sha256-a385f19a51054767b8be49a64ebc3111e0e62f721a861e54c78984b186904599.md) | qualified PASS on logging config | 2026-08-03 |
| [`2443fde49e26…`](sha256-2443fde49e26f83d931c443501544fa0c510c658360c45324190c3d243dfefa3.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-08-17 |
| [`ce39ea4cfe0d…`](sha256-ce39ea4cfe0ddf4dc2e4fbb96b6c66ab9f72954444d5419b196d06940db5e297.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-08-21 |
| [`cb9040a3e32a…`](sha256-cb9040a3e32a0e9157baf26b804d95a3ec55b91d9ae87383e0acd4300490078e.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-09-01 |
| [`a03816ba0c73…`](sha256-a03816ba0c737f1ed438bd595bbd6fba6ed1657bff4283c02655e06f1729df60.md) | LEAKS — the FLUX diffusion service this file launches still logs every user prompt at INFO and writes every… | 2026-09-10 |
| [`65724b385465…`](sha256-65724b385465af96a1062c2524cf78d791ebd54051d61e63008353a8f5416284.md) | LEAKS — the FLUX prompt log and image-to-disk carry; GLM-5.1 replaced by a GLM-5.3 Flash engine on the signed 47aff791 build, whose glm47 parser warning joins the unredacted export; every proxy on d61357da…; glm47 finding withdrawn 2026-10-12, class unchanged (FLUX) | 2026-10-02 |
| [`9ee0d8a6353f…`](sha256-9ee0d8a6353fb8200e5f43cc3b3b1de30d7aa07b08c7a5d93154be3d1641f379.md) | LEAKS — the FLUX prompt log and image-to-disk carry (the running FLUX container is from an older unaudited revision, identical for that service); GLM-5.3 becomes two TP2 replicas on the signed v7 build fa730e6e (FP8 KV, ghost prefix cache to a key-holding sidecar — LOW, preprocess pool, tool-schema caps) whose glm47 parser warning rides the unredacted export; a dedicated Qwen3.8-27B replica on the audited lmsysorg febfb971 build joins; only r1a, r1b and otelcol run from this hash; glm47 finding withdrawn 2026-10-12, class unchanged (FLUX) | 2026-10-12 |
| [`addbc5fc3d3c…`](sha256-addbc5fc3d3c43a455f44178c1525dd21f6c84dedf26ed9b4c725ac384ee980d.md) | LEAKS — the FLUX prompt log at INFO and image-to-disk carry, exported by this file's otelcol unredacted (wholesale, FLUX users only); `6000fd05` (v0.0.496), live 2026-10-21 on a NEW CVM (harness `5e513dbd72e1`, gpu13): the GLM-5.3 replicas and ghost aggregator re-pinned to the v10 engine `c15a3367` with the Q8 DSA prefill selected and 16K chunks, transformers pinned by version, otherwise the 9ee0d8a6 document; the re-pin adds no sink | 2026-10-22 |
| [`254ac8b3c655…`](sha256-254ac8b3c655126390b6038d96e9c9e378f8e2421585a5fd0f46f211d6822cd4.md) | LEAKS — `cd1a323d` (v0.0.530), delta from `addbc5fc` in 16 commits: the FLUX prompt log and image-to-disk CRITICAL/HIGH and the unredacted stdout export carry; the two GLM TP2 replicas and the aggregator move to the signed v12 engine `da8d4e4b` (PRIVATE at the deployed flags), the qwen38 proxies to `4937ad68`, the other eight stay on `e4a42b32` (both QUALIFIED PASS); new: the qwen3-8-27b abliterated LoRA stack (hash-pinned adapter, org-gated proxy, the same names also served from the cm-gpu32-g7 CVM), `sage`/`sage-dstack` now declared here — a third-party `levantolabs/sage2-hopper-pod` inference container with no page, its own CloudWatch log credential, own bridge, filtered dstack socket (HIGH, unaudited image); the running table is seven revisions deep (most model servers from the unaudited `dfac2898`, the qwen38 engine and proxies from `88e83711`, the GLM pair from `c2c83d9c`), and the log ends with a project-wide `sage-pull.yaml` up at 13:22Z — the attestation documents the proxies served afterwards show the small-models containers survived it (per-model compose projects) | 2026-10-30 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
