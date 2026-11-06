# prod/DeepSeek-V4.1-Flash-1017-vLLM-DEP8-Abliterated.yaml

Inner (model-layer) compose for **DeepSeek-V4.1-Flash-1017** on one CVM (gpu02, the
host that served GLM-5.3-Flash long-context until 2026-10-27): eight data-parallel
vLLM ranks on near.ai's signed [`nearaidev/vllm`](../../../../../images/docker.io/nearaidev/vllm/)
build (upstream `v0.32.0` plus LoRA-on-`wo_b`, UVA-disable and Engram patches),
under `ipc: host` and `network_mode: host`, serving two model names from the same
ranks — `deepseek-v4-1-flash` and `deepseek-v4-1-flash-abliterated`, the second
through a LoRA adapter the proxy selects by model name and gates by organisation id.
Two E2EE proxies, one nginx serving the prod and staging zones, a registrar, the
model and adapter downloader, dcgm and the collector. Sibling of
[`qwen35-dsv4-flash`](../qwen35-dsv4-flash/) (the earlier DeepSeek-V4-Flash layout
on vLLM).

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
| [`ce0dbf705aa9…`](sha256-ce0dbf705aa950db96e6c5cb169b13d1feb1716b02968418a3b5b43606e26440.md) | QUALIFIED PASS at the manifest layer — `4f7a11dc` (v0.0.528): no logging, dump, trace or debug switch to any of the eight vLLM ranks or the two proxies, OHTTP literal true, checkpoints revision-pinned and offline, every image paged; MEDIUMs: the engine's crash dump of speculative draft token ids is ARMED by `--speculative-config` on every rank and shipped unredacted, the engine's image fetch is unbounded by this file (no media allow-list, no rejected content-part types) so an `image_url` is fetched twice from the host namespace, eight unauthenticated ranks on `0.0.0.0:9100-9107` bypass the proxies' model and org gates, web search ARMED, unpinned `uvx` downloader with the HF token; the eight running engines (`e5468c4e`) and the downloader/dcgm/collector (`bb8f92c9`) are byte-identical to this file; the abliterated proxy ran seven hours without its org gate; the four LongContext engines and the DEP4x2 engines cannot hold the GPUs beside these eight — two readings for the rest | 2026-10-30 |
| [`594648eec0c1…`](sha256-594648eec0c19759ea2f595a8ac21fa84ef0c98023127ce24db95cf0c3370335.md) | QUALIFIED PASS at the manifest layer — an 11-hunk delta from the audited ce0dbf70 revision, every hunk read and re-derived (git diff: +13/-1): all eight ranks gain --scheduling-policy priority, both proxies gain VLLM_PROXY_PRIORIT… | 2026-11-06 |
| [`048f54e8ed74…`](sha256-048f54e8ed740216bbe6e5ecf0e65b59433c1754da5b26e9e68228cd6c5039ff.md) | QUALIFIED PASS at the manifest layer — this file is the 594648ee revision with exactly one line changed, proven by diff: the proxy anchor's image at line 48 moves from the pageless a99b89aa to 0be4ee8f, the inference-proxy 53d7944… | 2026-11-06 |
| [`80ab61cebfe4…`](sha256-80ab61cebfe424f79c981493176b27e4964a26daeac81b7ef3e4d1017f5819f6.md) | QUALIFIED PASS at the manifest layer — a 48-hunk delta from the audited ce0dbf70 revision, every hunk read and accounted for (git diff re-derived: +82/-46): the proxy image moves to the reviewed 0be4ee8f build, both proxies gain V… | 2026-11-06 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
