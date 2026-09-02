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

**Identity.** These images carry no signed build attestation; each page states
how the upstream commit and the patch were recovered from the image itself
(`.git/shallow`, `_version.py`, layer diffs) and how strong that binding is.

A build not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
