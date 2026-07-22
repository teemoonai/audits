# vllm/vllm-openai

The inference engine — runs the model on decrypted text; sees plaintext by role. Upstream third-party ([github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)). Used for the Gemma-4 engine on near.ai; the sibling engine `lmsysorg/sglang` serves the DeepSeek/Qwen/GLM models.

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:960ac5b3fda0...`](sha256-960ac5b3fda0547c3ce64d8f69bae9fa242d5ae5382fc74a98cd8ef13950e403.md) | v0.23.1rc1 (compose) — Gemma-4-31B | PRIVATE at deployed flags | 2026-07-22 |

**Contrast with sglang:** vLLM's request logging is *opt-in and off by default* at this version, and — unlike sglang — there is **no runtime `/configure_logging` analog**, so the engine cannot be flipped to log content without a restart. The two standing notes are a content-free usage-stats phone-home to `stats.vllm.ai` (on by default) and version drift (the compose names `v0.23.1rc1`, which is not a public tag; audited at the nearest `v0.23.1rc0`).

A build not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
