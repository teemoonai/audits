# ghcr.io/phala-network/sglang

Third-party sglang builds published by Phala Network — a fork of
`sgl-project/sglang` ([github.com/Phala-Network/sglang](https://github.com/Phala-Network/sglang))
carrying GLM-5.3 multimodal patches ahead of upstream. On near.ai this image is
not run directly: it is the `FROM` of an **in-enclave build**
(`prod/GLM-5.3-Flash-SGL-TP4.yaml`, anchor `x-glm53-build`) that hash-checks and
patches one file (`protocol.py`, a thinking-budget validator) and runs the
result as `nearai/glm53-sglang-r12-budget:local`. The inference engine — sees
plaintext by role. The page covers the base image bytes and the inline patch.

## audited builds

| digest | build | verdict | review |
|---|---|---|---|
| [`sha256:2488ca13aee7...`](sha256-2488ca13aee77ffd24ba2181b1b05dcf5e1c76e6477002c7b2f074b44fa49193.md) | Phala release scope `glm53-mmembed-isolation-r12`, labelled `Phala-Network/sglang@26f67bd9`; image python tree = that commit **except six files** from Phala patch layers, four from non-public commits — GLM-5.3-Flash | LEAKS — narrowly: glm47 tool-call parser logs a model-emitted argument value at WARNING, shipped by the recipe's otelcol; plus the fleet's sglang CRITICAL/HIGH residuals live | 2026-09-02 |

**Identity is the weakest of any engine image here.** No build attestation; the
OCI labels are self-asserted by a third party, and the image bytes were shown to
differ from the labelled commit, so `index.json` carries **no `sources` pin** for
this digest. The page reviewed the reconstructed image tree itself, which is
stronger than a label — but the base build's own provenance
(`ai.sglang.build.commit=unknown`) and a bundled patched `transformers` are not
recoverable.

A build not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
