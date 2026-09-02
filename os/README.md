# guest OS

The confidential-VM **guest image** (kernel + initrd + rootfs) every near.ai
enclave boots on — measured by the CPU into RTMR0–2 and surfaced in the
attestation as **`os_image_hash`**. It is near.ai's
[`nearai/private-ml-sdk`](https://github.com/nearai/private-ml-sdk) build (a
GPU-TEE derivation of dstack), not upstream dstack.

**Why it's in scope.** As the kernel it manages every container's memory, so it
has the most complete view of your plaintext of anything in the enclave —
strictly above the `docker.sock` / log-mount capability tiers. Its integrity is
load-bearing for the plaintext question, which is why it is measured into the
quote and surfaced in the [teemoon](https://teemoon.ai) app as a tier-1
("sees your message") row.

## Builds

| `os_image_hash` | node | verdict | review |
|---|---|---|---|
| [`9b69bb1698ba...`](sha256-9b69bb1698bacbb6985409a2c272bcb892e09cdcea63d5399c6768b67d3ff677.md) | model (GLM-5.1 + shared fleet, live 2026-07-22) | PRIVATE at measured configuration | 2026-07-22 |
| [`a6eafc5f007f...`](sha256-a6eafc5f007f642d8ea90c7fa8881f1e6715720ccb531941a28218f4f26d7b02.md) | `glm-5-3-flash` (gpu30) only, live 2026-09-01 — **upstream** `Dstack-TEE/meta-dstack` release `dstack-nvidia-0.5.11`, not near.ai's fork | QUALIFIED PASS at measured configuration (armed core-dump path, kernel without an LSM) | 2026-09-02 |

**Two builds, two repos (2026-09-02).** Every node but one boots near.ai's own
`private-ml-sdk` v0.5.5 build below. The `glm-5-3-flash` node boots the
*upstream* Dstack-TEE `dstack-nvidia-0.5.11` release: its `os_image_hash` is,
byte for byte, the `digest.txt` of `meta-dstack` release v0.5.11 (commit
`ce04e924`, `is_dev: false`), recomputed from the published asset the same way.
near.ai did not build that image; see its page for what the repo switch means.

**Identity verified (reproduce-and-match).** This hash is, byte for byte, the
`digest.txt` published in private-ml-sdk **v0.5.5** (commit
`25c25025c556ab2f797eeda3bab433f38a8ffb7a`) — so the deployed guest OS is
near.ai's own published release, not an unrecognized build. The measurement rule
(`os_image_hash = sha256(sha256sum.txt)` over `ovmf.fd bzImage
initramfs.cpio.gz metadata.json`) was re-derived from the shipped bytes and
matches live attestation. The gateway node runs a *different* image, off the
plaintext path.

**Source-audited (2026-07-22).** The review page confirms the production image
ships **no plaintext sink**: no login/serial-shell/ssh/capture tooling (dev-only,
different hash), no telemetry or log-shipping agent, journald RAM-capped and
local, container stdout confined to a KMS-keyed LUKS2 disk, dm-verity read-only
rootfs with panic-on-failure. The one content-capable route (guest-agent
`/logs`) is compiled in but **disabled by the measured manifest** (`public_logs:
false`), and every operator-flippable switch found lands inside the measurement.
Verdict **PRIVATE at measured configuration**.

**Residuals (see the page):** reproducibility is verified-by-design but the
multi-hour Yocto rebuild was not exercised here; the Linux kernel + upstream
Yocto layer *source* were not line-audited (config fragments + recipes only); the
**NVIDIA CC driver** is a proprietary, sha256-pinned but unauditable blob; and
the host serial console is a standing (content-free today) host-readable channel.
