# prod/pack-small-models.yaml

Inner (model-layer) compose for the nine small-model hosts on one CVM (gpu13; measured harness `e8416a02`): Qwen3.6, Qwen3.8, Qwen3-VL, embedding, reranker, privacy-filter, Whisper, FLUX.2-klein and a GLM-5.3 pair, each engine on its own internal network behind its own E2EE proxy. First deployed 2026-11-14; successor of [`small-models`](../small-models/), several of whose revisions still own running containers on the same CVM (each page's running table says which).

| file_sha256 | verdict | review |
|---|---|---|
| [`bbc809427267…`](sha256-bbc809427267b2efa784a2e51c65ac8f4f3d1efdd6ff28ca2a43c15dcff91118.md) | LEAKS — conditionally, and for this revision in the running state: the Qwen3.6 engine, the FLUX engine and the collector on the small-models CVM were created from this exact revision on 2026-11-14T01:48:40Z; both Qwen services it decla… | 2026-11-19 |
| [`4f4c6c18ad2b…`](sha256-4f4c6c18ad2b9f877dc5144c67a61a403314a219b10b357db81fb7688cd61140.md) | LEAKS — conditionally, through the two Qwen chat engines and the FLUX engine this file declares on the signed sglang build 6de632a5: both Qwen services select the qwen3_coder tool-call parser, which prints a model-written tool argument… | 2026-11-19 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
