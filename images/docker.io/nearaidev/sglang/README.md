# nearaidev/sglang

near.ai's **own builds of sglang** — from-source builds of an upstream
`sgl-project/sglang` commit plus one or two local patches, published under
near.ai's Docker Hub namespace. The inference engine for DeepSeek-V4-Flash on the
combined nodes; sees plaintext by role. Sibling of
[`lmsysorg/sglang`](../../lmsysorg/sglang/) (upstream's official images): same
codebase, different builder. Each page here recovers the patch from the image
layers and reviews upstream-at-commit **plus** the patch; upstream findings
(unauthenticated `/configure_logging`, watchdog prompt dump) are re-derived, not
inherited.

## audited builds

| digest | build / model | verdict | review |
|---|---|---|---|
| [`sha256:1e335c485bfe...`](sha256-1e335c485bfe064e1b9cdfdcb2765e327235a59fbb65df91be9b429d23e1db08.md) | upstream `7de33ce8` + one scheduler patch — DeepSeek-V4-Flash | private at deployed flags (patch is a one-file scheduler change) | 2026-08-03 |
| [`sha256:ec518148762e...`](sha256-ec518148762ea02c23aa8615f69ca79b0c18bcd59b3c21c10229db3df323c615.md) | upstream **`v0.5.16`** (`fdebc938`) + two patches — DeepSeek-V4-Flash-0731 | PRIVATE at deployed flags | 2026-08-10 |
| [`sha256:5bc4bc0dfd36...`](sha256-5bc4bc0dfd3629af7e57168098b5e76b4206dcb02b8ed8a872aebfd153ff240b.md) | upstream nightly `c0b6474b` + two patches — DeepSeek-V4-Flash (DS4F nightly) | PRIVATE at deployed flags | 2026-08-21 |
| [`sha256:a7b7136abcf5...`](sha256-a7b7136abcf5e07522289d96e96fec9b42a1a30f9dfda57e957f142680d2d67b.md) | **signed** near.ai build (cvm-compose-files `publish-glm53-fc91d24` workflow) of `PierreLeGuen/sglang-upstream` @ `fc91d24` on upstream nightly `07c8f729` — GLM-5.3-Flash | LEAKS — narrowly: glm47 parser logs a model-emitted tool-argument value at WARNING and stdout ships unredacted; otherwise private at deployed flags, /configure_logging CRITICAL and watchdog dump HIGH live | 2026-09-10 |

**Identity.** The three 2026-08 builds carry no signed build attestation; each of those pages states
how the upstream commit and the patch were recovered from the image itself
(`.git/shallow`, `_version.py`, layer diffs) and how strong that binding is. The `a7b7136a` build is the first with a **signed GitHub build attestation** (from near.ai's compose repo, binding the image to its Dockerfile, which pins the source tarball by checksum).

A build not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
