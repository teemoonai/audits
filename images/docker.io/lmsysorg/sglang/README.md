# lmsysorg/sglang

The inference engine - runs the model on decrypted text; sees plaintext by role. Upstream third-party (github.com/sgl-project/sglang).

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:aac6b242680d...`](sha256-aac6b242680daeb74d2ab1d85f70575357552d7d165d2e5d30eb362797db54a1.md) | `dev-cu12` base — GLM-5.1 (`:local` patched) | PRIVATE at deployed flags | 2026-07-15 |
| [`sha256:9e02c8e1fe27...`](sha256-9e02c8e1fe2790a1c445bd5f6814305fe43639a4adb01c8ad1e8e21e750bf581.md) | `v0.5.12-cu129` (`127b9e32`) — Qwen3.6-27B & -35B | PRIVATE at deployed flags | 2026-07-22 |
| [`sha256:6bb5fee34b6c...`](sha256-6bb5fee34b6c4537c09a4775e2292ac40350d5ad1218fcc835b2692142f443b1.md) | cu13 nightly (`7de33ce8`) — DeepSeek-V4-Flash | PRIVATE at deployed flags | 2026-07-22 |
| [`sha256:5027e95bf6ec...`](sha256-5027e95bf6ec536856b1b52a91d1f35ff5c564ab83e8a94758a169ff09bb8df3.md) | **`v0.5.14`** (`49e384ce`) — `z-ai/glm-5.2` (2 × TP4) | private at deployed flags; **CRITICAL + HIGH residuals live** | 2026-08-03 |

All four carry the same CRITICAL residual — the unauthenticated `/configure_logging` runtime switch — which is OFF at deployed flags.

> **Correction (2026-08-03): there is no proxy path-allowlist.** Earlier revisions of this README and of the three 2026-07 pages described that CRITICAL as "guarded only by the (external, unattested) proxy path-allowlist", and recommended "attest the proxy path allowlist" as a fix. **No such allowlist exists.** The [`vllm-proxy-rs@b0c5cd07` review](/images/docker.io/nearaidev/vllm-proxy-rs/sha256-b0c5cd0786b19dfa46144107be15e340b7a338b1c341d02ffa994c9f1ea77dfd.md) establishes from source that the proxy's router ends in `.fallback(catch_all::catch_all)`, which forwards **any** path surviving traversal validation — there is no path list anywhere in that tree, at either attested proxy commit. The only guard is authentication: the deployment `TOKEN` **or any valid `sk-` cloud API key**. So `/configure_logging` is reachable by any paying API-key holder, not just operators, and by any container on the shared `dstack_default` network directly. That is materially worse than what those pages implied. The correct fix is `--admin-api-key` **inside** the engine, not a control in an unattested proxy. The individual 2026-07 pages retain their original wording and are annotated by this note rather than rewritten.

**Version spread:** `aac6b242` (dev-cu12), `9e02c8e1` (v0.5.12-cu129), `6bb5fee3` (cu13 nightly `7de33ce8`), `5027e95b` (v0.5.14). Each page is verified against its own tree.

**Also runs, not yet audited:** `sha256:1c64fde976bd...` (`v0.5.13.post1`, commit `85fd9007` — glm-5.2-long) and `sha256:8ece90ad52fa...` (the `sglang-diffusion` FROM-base on the small-models node). A page previously written for `1c64fde9` was reverted as "source commit unresolved"; that premise was wrong — the image self-declares `ai.sglang.build.commit`.

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
