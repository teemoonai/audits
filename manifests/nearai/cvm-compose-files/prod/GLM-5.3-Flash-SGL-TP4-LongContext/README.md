# prod/GLM-5.3-Flash-SGL-TP4-LongContext.yaml

The FP8 long-context predecessor of [`GLM-5.3-Flash-SGL-TP4-W4AFP8-LongContext`](../GLM-5.3-Flash-SGL-TP4-W4AFP8-LongContext/)
on the glm-5-3-flash-long CVM (gpu23): two TP4/EP4 replicas of `z-ai/glm-5.3-flash` at a 1M-token context on
near.ai's signed admission-reserve builds of [`nearaidev/sglang`](../../../../../images/docker.io/nearaidev/sglang/)
(r1 on the plain build, r2 on the HiCache build), behind one E2EE proxy and nginx. Upped whole once, on
2026-09-29T15:56:49Z; 58 minutes later the W4AFP8 file's up claimed the same eight GPUs, so what this file
declares has not been the serving stack since — under either compose-project reading. A sibling of
[`GLM-5.3-Flash-SGL-TP4`](../GLM-5.3-Flash-SGL-TP4/), which the page cites for byte-identical blocks.

Identity is **log-pinned**: the file's `file_sha256` against the signed compose-manager action log
(commit + path + file hash), not hardware-measured; the measured layer is the gpu23 node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred to the image pages the
revision links.

The verdict column is the page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`8ab2a4520716…`](sha256-8ab2a4520716cb06b6c3f6764ddbeeaeebdef0ebb89a82c235a598ee68a7a8de.md) | QUALIFIED PASS — at the deployed flags no path this file configures writes message plaintext to any sink in normal operation (both engine images are PRIVATE at these flags on their own pages; the recipe passes … | 2026-11-06 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
