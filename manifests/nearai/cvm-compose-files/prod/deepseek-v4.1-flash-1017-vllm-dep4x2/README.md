# prod/deepseek-v4.1-flash-1017-vllm-dep4x2.yaml

Inner (model-layer) compose for **DeepSeek-V4.1-Flash-1017** as two groups of four vLLM ranks, deployed on both DeepSeek CVMs (gpu04, measured `e3902667` since 2026-11-19, earlier `bd0a5446`; gpu02 `08f91377`) from 2026-11-17. Sibling of [`DeepSeek-V4.1-Flash-1017-vLLM-DEP8-Abliterated`](../DeepSeek-V4.1-Flash-1017-vLLM-DEP8-Abliterated/); since 2026-11-19 every model container on both CVMs, the recipe's collector on gpu04 included, was last created from this path at `f392013b` (on gpu02 no retained log entry names a recipe collector).

| file_sha256 | verdict | review |
|---|---|---|
| [`11928bb62184…`](sha256-11928bb62184067aaec222cce18dae034696e29d285d66882258f2efd876e8aa.md) | QUALIFIED PASS at the manifest layer — a full document review of a new file path, sibling of the audited DEP8 file: this revision created the eight engine containers that run on each of the two DeepSeek CVMs (image 2fe23851, reviewed,… | 2026-11-19 |
| [`d4cbe817f102…`](sha256-d4cbe817f102d7c06eb81da306030197a6ac731b7a05e0e952bc0f8725d121f9.md) | QUALIFIED PASS at the manifest layer, for what this revision actually created — the two E2EE proxies on each DeepSeek CVM (image e3a4fbca, reviewed, QUALIFIED PASS) and nginx on one of them; the diff from the reviewed 11928bb6 revision… | 2026-11-19 |
| [`f392013b5e0b…`](sha256-f392013b5e0bf8a2574875df042e6745fe40cbd874793925772a687e61bf72a9.md) | QUALIFIED PASS at the manifest layer — by both signed action logs this revision created every model container that serves the two DeepSeek names: all eight engines, both E2EE proxies, nginx, the registrar, the downloader and dcgm on each CVM, and the recipe's collector on gpu04 … | 2026-11-20 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
