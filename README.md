# teemoon audits

Source-level reviews answering exactly one question about near.ai's
confidential inference stack: **can anything exfiltrate your plaintext?**
Keyed to exact attested identities, so a review only ever claims to cover the
bytes it covered.

**The model: one page per audited build, named by its attested identity.**
`sha256-<digest>.md` *is* the review — verdict first, full analysis beneath —
for the digest-pinned images that are the norm; a tag-pinned image (which the
attestation pins by tag, not bytes) gets a `tag-<tag>.md` page instead (see the
path spec below). A build with no page has not been audited, and the
[teemoon](https://teemoon.ai) app shows no audit link for it. Fail-closed,
never overclaim.

## Scope rule

Under end-to-end encryption, plaintext exists in exactly three places on
near.ai's side: the E2EE terminator's memory, the inference engine's memory,
and GPU memory — all inside the model CVM. An artifact is in scope **iff, per
the attested manifests, it can access that plaintext**:

- **directly** — it decrypts or computes on messages
  (`vllm-proxy-rs`, `sglang`), or
- **by capability** — privileged mounts give it process-memory or log-stream
  access (`pid: host` + `SYS_PTRACE`, `docker.sock`, container-log mounts):
  `compose-manager`, `compose-manager-launcher`, `datadog/agent`,
  `otel/opentelemetry-collector-contrib` — or GPU privilege (`SYS_ADMIN` +
  nvidia runtime over all GPUs): `nvidia/k8s/dcgm-exporter`. At the audited
  config dcgm exports telemetry counters, not content — but it is privileged
  *and* pinned only by tag (its bytes can drift under the attestation), so it
  is kept in scope for its privilege, not assumed benign for its function.
- **as the substrate** — the confidential-VM **guest OS** (kernel + rootfs) all
  of the above run on. The kernel manages every container's memory, so plaintext
  is unavoidably visible to it — the most complete view of anything in the
  enclave. Keyed by its measured `os_image_hash` ([`os/`](os/)).

The **manifests** are in scope because they *define* all of it: which images
run, their invocation flags (logging), their privileges and mounts, network
topology, and egress. Everything else — the gateway/ciphertext side, in-enclave
plumbing that only ever sees OHTTP-sealed bytes, cert/weights/registrar
sidecars — is deliberately out of scope here. (Reviews of those components
exist in the teemoon project; this repo stays scoped to the plaintext
question.)

**What this is not:** a formal third-party audit or a guarantee. Reviews are
point-in-time AI-assisted reads of published source and attested configuration
([method](/notes/method.md) — repeatable; verify everything yourself).

## How the app uses this repo

teemoon fetches [`index.json`](index.json) and shows an "audit" link on an
attestation surface **only when the exact running identity is listed** — the
link lands directly on that identity's review page. Shipped builds construct
these URLs from attested fields, which makes the layout a compatibility
contract:

## Path spec (frozen — this is API)

```
images/<registry>/<namespace>/<name>/sha256-<64 hex>.md      ← the review of that build
images/<registry>/<namespace>/<name>/tag-<tag>.md            ← tag-addressed review (tag-pinned images only)
manifests/<owner>/<repo>/<path minus .yaml>/sha256-<file_sha256>.md
manifests/measured/sha256-<compose_hash>.md
os/sha256-<os_image_hash>.md                                 ← the guest-OS review
index.json
```

`index.json` gates every link: `images` (ref → digests), `tagAudits` (ref →
tags), `manifests` (path → `file_sha256`), `measured` (`compose_hash`), and
`os` (`os_image_hash`). A missing/empty key means nothing published in that
layer → no link.

**Tag-addressed pages (additive):** some attested manifests pin an image only
by tag — no digest exists anywhere in the attestation chain, so a
`sha256-*.md` page would claim a byte-identity the attestation doesn't
provide. Those images get `tag-<tag>.md` pages instead, gated by the
`tagAudits` index key. A tag-addressed page covers the tag string and its
deployed configuration, **never bytes** — the registry can serve different
bytes under the same tag with no attestation-visible trace, and each page
says so. This is an additive sibling to the digest pattern, not a
replacement; digest-pinned images keep digest pages.

Normalization rules (implemented identically in the app; never changed):

1. Bare Docker Hub refs gain `docker.io/`; official single-name images gain
   `library/`.
2. Tags are stripped; the digest is the identity. Exception: tag-addressed
   pages, where the attestation provides no digest — there the verbatim tag
   is the (weaker) identity.
3. Digest filenames are `sha256-` + 64 lowercase hex + `.md`; tag filenames
   are `tag-` + verbatim tag + `.md`.
4. Manifest paths come verbatim from the signed action log, minus `.yaml`.
5. Coordinates — org `teemoonai`, repo `audits`, branch `main` — are
   permanent. Content is append-only: pages are added or corrected in place;
   paths are never renamed or moved. `index.json` carries `"schema": 1`; any
   structural evolution adds a new tree/schema beside this one.

`notes/` is editorial and outside the contract.

## Layout

- [`images/`](images/) — per plaintext-accessing image ref: `sha256-*.md`
  review pages plus a thin `README.md` lineage index (role, audited builds and
  verdicts, observed-but-unaudited builds).
- [`manifests/`](manifests/) — the documents that define the plaintext
  environment: the log-pinned inner stack (by `file_sha256`) and the
  hardware-measured node harness (by `compose_hash`).
- [`os/`](os/) — the confidential-VM guest OS (kernel + rootfs) measured into
  the boot, keyed by `os_image_hash`: the substrate that sees all plaintext.
- [`notes/`](notes/) — the review method and the deployment architecture
  (which derives the scope rule above).

## Audit policy

A new build (new digest / new file_sha256 / new compose_hash) gets a link only
after a review of that build — full or an explicitly-scoped delta review —
publishes its page. Until then the lineage README may note it as *observed,
not audited*. Corrections are made in place, never by moving pages.

## License

Documentation is licensed [CC BY 4.0](LICENSE.md). Quoted source excerpts
remain under their projects' licenses.
