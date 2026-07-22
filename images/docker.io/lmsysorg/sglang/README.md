# lmsysorg/sglang

The inference engine - runs the model on decrypted text; sees plaintext by role. Upstream third-party (github.com/sgl-project/sglang).

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:aac6b242680d...`](sha256-aac6b242680daeb74d2ab1d85f70575357552d7d165d2e5d30eb362797db54a1.md) | `dev-cu12` base — GLM-5.1 (`:local` patched) | PRIVATE at deployed flags | 2026-07-15 |
| [`sha256:9e02c8e1fe27...`](sha256-9e02c8e1fe2790a1c445bd5f6814305fe43639a4adb01c8ad1e8e21e750bf581.md) | `v0.5.12-cu129` (`127b9e32`) — Qwen3.6-27B & -35B | PRIVATE at deployed flags | 2026-07-22 |
| [`sha256:6bb5fee34b6c...`](sha256-6bb5fee34b6c4537c09a4775e2292ac40350d5ad1218fcc835b2692142f443b1.md) | cu13 nightly (`7de33ce8`) — DeepSeek-V4-Flash | PRIVATE at deployed flags | 2026-07-22 |

All three carry the same CRITICAL residual — the unauthenticated `/configure_logging` runtime switch — which is OFF at deployed flags and guarded only by the (external, unattested) proxy path-allowlist.

**Observed, not audited:** the GLM-5.2 stack pins a different build (`sha256:5027e95bf6ec...`). It has no page here until its source delta is reviewed.

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
