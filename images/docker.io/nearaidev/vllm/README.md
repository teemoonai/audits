# nearaidev/vllm

near.ai's **own builds of vLLM** — the upstream [`vllm/vllm-openai`](../../vllm/vllm-openai/) release image
plus a handful of local patches, rebuilt by a signed GitHub workflow in `nearai/cvm-compose-files` and published
under near.ai's Docker Hub namespace. The inference engine for DeepSeek-V4.1-Flash on gpu02 (eight data-parallel
ranks serving both the plain and the LoRA-"abliterated" model names); sees plaintext by role. Sibling of
[`nearaidev/sglang`](../sglang/) (near.ai's own sglang builds): same filing — each page recovers the recipe from
the signed attestation, reviews upstream-at-release **plus** the patches, and re-derives upstream findings rather
than inheriting them.

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:5eaa0d463708...`](sha256-5eaa0d4637080c10958b6cd8a371ae2ebb749b7a1e19c85bcb1abb89ee2540e4.md) | **signed** near.ai build (cvm-compose-files `publish-vllm-dsv41-lora` workflow @ `c8771522`, recipe `docker/vllm-dsv41-lora` by the attested workflow's `BUILD_CONTEXT`) of upstream `vllm/vllm-openai:v0.32.0` plus five patches (three LoRA-on-`wo_b` enablers, UVA disable for confidential computing, Engram tables gathered on the CPU from `/dev/shm`) and pinned pip/certifi/uv upgrades — DeepSeek-V4.1-Flash-1017 (DP8, 1M context, heretic LoRA) | QUALIFIED PASS at the deployed flags — no content path to log, disk or telemetry in steady state, the five patches add no sink; two qualifications: MEDIUM ARMED crash dump prints every in-flight request's speculative draft token ids (speculative decoding is deployed; `SchedulerOutput` has no redacting repr), MEDIUM ON the deployed model class is multimodal so chat `image_url` parts are fetched with no allow-list and redirects on from the host network namespace; request logging OFF by default, no `/configure_logging` analogue, `stats.vllm.ai` phone-home LOW ON, torch 2.13 NCCL flight recorder default-on INFO; identity verified (Hub tag → `befccf0e`, tag `v0.32.0` = `5df63a72`, pre-patch file hashes 5/5, wheel hashes on PyPI) | 2026-10-30 |

**Identity.** The image carries no recipe label; the recipe is established by the **signed build attestation**
(Sigstore, GitHub OIDC) whose workflow sets `BUILD_CONTEXT: docker/vllm-dsv41-lora` and whose buildkit metadata
asserts the same local context — not inferred from the workflow's name. The upstream base digest it builds on
(`vllm/vllm-openai@sha256:befccf0e…`, the `v0.32.0` release) has no page of its own in this repo; the page here
covers the upstream engine at that release in full, carrying the `v0.26.0`-line page's findings forward only
where it locates them in the `v0.32.0` tree.

A build not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
