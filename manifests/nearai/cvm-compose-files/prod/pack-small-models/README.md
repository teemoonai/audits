# prod/pack-small-models.yaml

Inner (model-layer) compose for the small-model hosts: Qwen3.6, Qwen3.8 and its abliterated adapter, Qwen3-VL, embedding, reranker, privacy-filter, Whisper, FLUX.2-klein and a GLM-5.3 pair. Eight engines sit each on its own internal network behind its own E2EE proxy; the GLM-5.3 pair and its proxy sit on the shared external bridge, the engines in the host IPC namespace.

By the signed action logs it runs on the CVM with measured harness `e3902667`, which served DeepSeek until 2026-11-19: a whole-file `compose_up` at 2026-11-19T23:15Z and a 42-service one at 23:42Z created its containers from `b6eeef75`, and `f4916294` re-created the privacy filter at 2026-11-20T00:30Z. That CVM serves ten hosts (the nine above by name plus glm-5-3-flash).

This file is one of the places the shared glm-5.3-flash model key is opened: the gateway capture of 2026-11-20 lists `e3902667` with `c900dc73` and `fb81c6f2` under one signing key. It was first deployed 2026-11-13/14 on the CVM with measured harness `e8416a02` (gpu13), beside revisions of [`small-models`](../small-models/) that still owned containers there (each page's running table says which revision created which container). The gateway capture of 2026-11-20 no longer lists `e8416a02` for glm-5.3-flash (a capture earlier the same day did), so whether that CVM still runs this file is not established here.

| file_sha256 | verdict | review |
|---|---|---|
| [`bbc809427267…`](sha256-bbc809427267b2efa784a2e51c65ac8f4f3d1efdd6ff28ca2a43c15dcff91118.md) | LEAKS — conditionally, and for this revision in the running state: the Qwen3.6 engine, the FLUX engine and the collector on the small-models CVM were created from this exact revision on 2026-11-14T01:48:40Z; both Qwen services it decla… | 2026-11-19 |
| [`4f4c6c18ad2b…`](sha256-4f4c6c18ad2b9f877dc5144c67a61a403314a219b10b357db81fb7688cd61140.md) | LEAKS — conditionally, through the two Qwen chat engines and the FLUX engine this file declares on the signed sglang build 6de632a5: both Qwen services select the qwen3_coder tool-call parser, which prints a model-written tool argument… | 2026-11-19 |
| [`b6eeef756905…`](sha256-b6eeef7569051d07578968f852d57edeec4ddecbb72e1930e03def3add6dec5e.md) | LEAKS — conditionally, and now for one reason where the base revision had three: the FLUX service is still started without an output path or an input path, so by the image page for sglang 2321e3c2 every generated image, and every image sent in for editing, is written to the container's disk and kept … | 2026-11-20 |
| [`f4916294365d…`](sha256-f4916294365d6ee89143de1a4838625b96ccc1b682812a19a8642ff857058cf4.md) | LEAKS — conditionally, as a document and for the hosts that present it, through one service this revision declares and did not itself create: the FLUX block is byte-identical to b6eeef75's and still passes no output path and no input path, so by the image page for sglang 2321e3c2 every generated image, and every image sent in … | 2026-11-20 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
