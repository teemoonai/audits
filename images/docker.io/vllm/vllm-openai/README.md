# vllm/vllm-openai

The inference engine — runs the model on decrypted text; sees plaintext by role. Upstream third-party ([github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)). Serves the Gemma-4, gpt-oss and Qwen3-VL models on near.ai, and since 2026-08-25 DeepSeek-V4-Flash (moved off sglang); the sibling engine `lmsysorg/sglang` serves the DeepSeek/Qwen/GLM models.

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:960ac5b3fda0...`](sha256-960ac5b3fda0547c3ce64d8f69bae9fa242d5ae5382fc74a98cd8ef13950e403.md) | nightly `b4c80ec0` (2026-06-18) — Gemma-4-31B | PRIVATE at deployed flags | 2026-07-22 (pin corrected 2026-08-03) |
| [`sha256:6766ce0c459e...`](sha256-6766ce0c459e24b76f3e9ba14ffc0442131ef4248c904efdcbf0d89e38be01fe.md) | release **`v0.12.0`** — gpt-oss-120b (3 × TP1) | clean in steady state; **1 crash-path token-ID leak** | 2026-08-03 |
| [`sha256:ccd6a6dbf4ab...`](sha256-ccd6a6dbf4aba4e94c6f7052d1835d6e742082b6a5095276552e9b7a5a47c2e5.md) | untagged, `v0.17.0` line (bracketed) — Qwen3-VL-30B | PRIVATE for content; **media fetch unrestricted** | 2026-08-03 |
| [`sha256:770fe65b2c73...`](sha256-770fe65b2c73ee74a5c42165cf3433de4048cc2cd9c57a937ca4e35aba5aa87b.md) | **`v0.26.0` line** (`ffd46bfa`, 2 commits before the tag) — DeepSeek-V4-Flash-0731 (DP4 × TP1 + EP, 1M context) | PRIVATE at deployed flags; crash-path token-ID leak fixed; new latent DEBUG parser log | 2026-09-01 |

**Contrast with sglang:** vLLM's request logging is *opt-in and off by default* at all three audited versions, and — unlike sglang — there is **no runtime `/configure_logging` analog**, so the engine cannot be flipped to log content without a restart. The standing note common to all three is a content-free usage-stats phone-home to `stats.vllm.ai`, on by default.

**A defect fixed between two of these builds.** The gpt-oss page's crash-path finding — `CachedRequestData` lacking an `anon_repr`, so an engine-crash dump serialises its `all_token_ids` (full prompt **and** output token ids) through the `__dict__` fallback to stdout — is present at `v0.12.0` and **absent at `v0.17.0`** and at the `v0.26.0` line, where `CachedRequestData.anon_repr` redacts to `all_token_ids_lens`. Same file, same class, upstream fix in between. The two reviews were conducted independently and each verified its own tree; the divergence is real, not a disagreement.

**Version spread is wide.** These builds span ~14 minor releases: gpt-oss runs the **v0.12.0** release (2025-12), Qwen3-VL an untagged **v0.17.0-line** build (2026-03), Gemma-4 a **2026-06 nightly**. Each page is verified against its own tree — no finding is carried across.

**Identity strength differs, and the pages say so.** Gemma-4's digest is tied to a commit by the image's own OCI label; gpt-oss's is tied to a published release tag; Qwen3-VL's is **bracketed to a ~3-day window** by Dockerfile-ARG fingerprinting, because it is untagged and unlabelled. Only the first two carry a source pin in `index.json`.

**Standing deployment gap:** the Qwen3-VL service omits `--allowed-media-domains` and `VLLM_MEDIA_URL_ALLOW_REDIRECTS=0`, both of which the Gemma-4 service applies in the same compose file — see that page's HIGH finding.

A build not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
