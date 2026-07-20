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

| `os_image_hash` | node | status |
|---|---|---|
| `9b69bb1698bacbb6985409a2c272bcb892e09cdcea63d5399c6768b67d3ff677` | model (GLM-5.1 fleet, live 2026-07-20) | **observed — identity verified, not yet source-audited** |

**Identity verified (reproduce-and-match, 2026-07-20).** This hash is, byte for
byte, the `digest.txt` published in private-ml-sdk **v0.5.5** (commit
`25c25025c556ab2f797eeda3bab433f38a8ffb7a`) — so the deployed guest OS is
near.ai's own published release, not an unrecognized build. All five public
releases were pulled and compared; only v0.5.5 matches. The gateway node runs a
*different* image (`da9a3d5c…`), off the plaintext path. Method + full walk:
teemoon `docs/privacy-audit/guest-os.md`.

**Not yet done** — which is why there is no `sha256-<hash>.md` review page and no
`index.json` entry, so the app shows **no** guest-OS audit link (fail-closed):

- a **source-level review** of the guest OS's own plaintext handling —
  disk-encryption + KMS key-release posture, kernel/rootfs configuration; and
- the full **source→binary rebuild** (`reproduce.sh` from `25c25025…`) proving
  the published image derives from the pinned source, not merely matches its
  binary.

The **NVIDIA CC driver** is a proprietary blob: it does not block reproducibility
(pinned, publicly downloadable bytes) but it blocks full source review of the
driver itself.

A build gets an indexed `sha256-<os_image_hash>.md` review page — and thus an
in-app audit link — only once that review publishes. Until then this note stands
as *observed, identity-verified, not audited*.
