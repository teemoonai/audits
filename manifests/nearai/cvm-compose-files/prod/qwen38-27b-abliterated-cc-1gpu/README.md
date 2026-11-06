# prod/qwen38-27b-abliterated-cc-1gpu.yaml

Inner (model-layer) compose for **Qwen3.8-27B** and its **abliterated** LoRA twin on a
single-GPU confidential-computing CVM (`cm-gpu32-g7`, a fresh host whose action log
starts with this file): one `lmsysorg/sglang` engine with LoRA enabled, two E2EE
proxies (the abliterated one gated by organisation id and selecting the adapter by
model name), nginx, registrars, the model and adapter downloaders, dcgm and the
collector. The same two model names are also served from the small-models CVM
(gpu13) by [`small-models`](../small-models/) — a request for `qwen3-8-27b` may be
answered by either host. Sibling of
[`GLM-5.2-W4AFP8-SGL-2xTP4`](../GLM-5.2-W4AFP8-SGL-2xTP4/) (the same sglang engine
build).

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
| [`91214155335a…`](sha256-91214155335ad44fcc4f0cd091dd5bb85c5e10172a1c74bc006ff2e55ed6fddd.md) | QUALIFIED PASS — `256e915c` (v0.0.529), a new file for a new single-GPU CC CVM class: one `lmsysorg/sglang` `febfb971` engine with LoRA serving two names behind two `4937ad68` proxies and one nginx; at the deployed flags no plaintext copy is configured (engine log-requests level 0, json metadata on proxies and nginx, revisions pinned, the abliterated adapter content-pinned by SHA-256 inside the attested file); the sibling's and image pages' qualifications carry — `/configure_logging` reachable without an admin key, web search and fusion ARMED through the unattested env overlay, watchdog token-id dump at the 300 s default (no `--watchdog-timeout`, unlike the sibling's 1800), unscrubbed stdout export, multimodal media fetch on, OTLP receivers open, persistent HF/sglang caches; new LOW for the unpinned `huggingface_hub` downloader; the abliterated proxy's org gate and token arrive only through the overlay; the same two names are also served from gpu13 by `small-models` | 2026-10-30 |
| [`81d8c1265b51…`](sha256-81d8c1265b5132c716a8a78c47fa78ce5f1a2a6fcd0170079c85fcba9c80b832.md) | QUALIFIED PASS — the whole-file revision of a three-revision patchwork on one CVM: the only project-wide up in the CVM's log (2026-11-02T22:42:09Z) created every container from this file, and today three survive from it — the dcgm… | 2026-11-06 |
| [`815dd63f872e…`](sha256-815dd63f872e42066ba4f7ff0e5dacb0947d6d8de09c5821675e11c8b54d6102.md) | QUALIFIED PASS — the engine revision of a three-revision patchwork on one CVM: this file created the running sglang engine, both registrars and the recipe's own collector on 2026-11-03 (five service-scoped ups), and its delta from… | 2026-11-06 |
| [`cd58c977f2fb…`](sha256-cd58c977f2fbb98e4a242fe83a5d2911355b78247c3dac875012534adc1e49d4.md) | QUALIFIED PASS — the proxy revision of a three-revision patchwork on one CVM and the hash the CVM has attested since 2026-11-04T02:58:34Z: this file re-created the two E2EE terminators and nginx, and its only change from the engin… | 2026-11-06 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
