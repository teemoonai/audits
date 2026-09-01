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

## The two sides of the question

Your plaintext exists in two places — near.ai's sealed enclave, and your own
device. This repo reviews both.

- **Server side — near.ai's confidential-inference stack.** Per attested
  identity: [`images/`](images/) (each plaintext-handling image),
  [`manifests/`](manifests/) (the configs that define them), and
  [`os/`](os/) (the guest OS underneath). Mapped end to end by
  [`notes/ARCHITECTURE.md`](notes/ARCHITECTURE.md).
- **Client side — the teemoon app on your device.** The
  [teemoon iPhone client review](notes/teemoon-ios-plaintext-audit.md) — the
  other end of the E2EE, which composes every prompt and decrypts every reply. A
  Tier-2 note, not a gated identity page: a client build carries no attested
  digest for a link to key on. The client source is public:
  [teemoonai/teemoon-ios](https://github.com/teemoonai/teemoon-ios), AGPL-3.0.

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

**`verdicts` (additive, optional): page path → that page's own verdict line.**
A link alone cannot say what a review *found* — "a page exists" and "the
review found nothing" are different facts, and an audit link with no verdict
beside it reads as reassurance. This repo publishes verdicts ranging from
"PRIVATE at deployed flags" to "COMPROMISABLE by credentialed operator" to
"INCONCLUSIVE — no build attestation exists", and a client that renders all of
them identically is overclaiming on behalf of the ones that found something.
So the verdict travels with the link. The value is copied from the page's
`## verdict:` heading — the reviewer's wording, which clients may truncate or
restyle for display but must not soften: a rendering that drops the class or
the caveats is overclaiming. A page missing from `verdicts` means the client
must fall back to neutral copy, **never** to reassuring copy.

**`verdictClass` and `findings` (additive, optional): the machine-readable
layer.** Both are derived mechanically from each page's own text by the
indexer — never authored there. `verdictClass` maps page path → the class the
verdict line opens with (`private` / `leaks` / `compromisable` /
`qualified-pass` / `inconclusive`), so a client can badge and color-code
without parsing prose. `findings` maps page path → the page's
`### SEVERITY (deployed: …) — title` finding headings as
`{severity, deployed, qualifier, title, anchor}`, so a client can list a
node's plaintext-egress findings — deployed-ON separated from latent — across
every page its attestation keys into, each linking to its evidence via the
anchor. Both fail soft: a page the extraction rules cannot read is omitted,
and the client falls back to the neutral treatment above.

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
   paths are never renamed or moved. `index.json` carries `"schema": 1` and
   evolves by **additive optional keys** within it; only a change that breaks
   an existing reader — removing/retyping a required key, changing a path
   rule — adds a new tree/schema beside this one.

## What is API here, and what is not

This repo is two things in one tree — **the artifact the app reads**, and **the
machinery that maintains it**. They have different guarantees, and confusing them
matters: a reader checking a claim needs to know which files are claims.

**Tier 1 — the endpoint. Frozen; this is API.**
`index.json`, `images/`, `manifests/`, `os/`. What is frozen, precisely: the
**paths** (clients construct them from attested fields — a rename breaks
released software), the **required index keys** (`schema`, `images`,
`manifests`, `measured`) and the **normalization rules** above. What is not:
page *content* evolves (corrections in place, append-only), and `index.json`
grows by **additive optional keys** — a client that ignores them keeps
working, which is why `verdicts`, `verdictClass` and `findings` could land
without a schema bump. The lineage `README.md` files inside these directories
are tier 2, not tier 1: linkable, but no client constructs their paths.

**Tier 2 — reachable from a published page. Frozen in practice.**
The honest rule is transitive: **anything a published page links to, directly
or through another note, moves only with tier-1 care**, because renaming it
breaks live links in published reviews. Today that closure is
`notes/method.md` (linked from every page), `notes/ARCHITECTURE.md`,
`notes/audit-surface.md` (reached via `method.md`),
`notes/reviewer-comparison-2026-08-03.md` (reached via `audit-surface.md`), and
`notes/teemoon-ios-plaintext-audit.md` (reached via `ARCHITECTURE.md`) — plus the
in-tree lineage READMEs. Notes outside that closure are editorial
and may be reorganised freely.

**Tier 3 — machinery. Free to change.**
`tools/`, `.github/`, `.claude/`. The drift detector, the identity resolver, the
indexer, and the orchestration skill. No client reads any of it.

`acknowledged.json` sits at the root beside `index.json` rather than under
`tools/`, because it is not tooling config: one file says what *is* audited, the
other says what is knowingly running **un**audited. Burying the second inside a
scripts directory would hide exactly the fact a sceptical reader most wants.

**The rule that matters:** *nothing in `tools/` may write a page.* The tooling
reports, validates and gates; the claims are written by review and verified by a
human before publication. `index_page.py` gates a link only after a page exists
and states its own verdict, and refuses outright to gate a page whose verdict is
INCONCLUSIVE — a gated link renders in-app as "source reviewed", which is a claim
such a page does not make.

Why one repo rather than two: a page, its `index.json` gate and its verdict have
to land in a single commit, or there is a window where the index gates a page
that does not exist. And keeping the tooling beside the claims is the point — you
can read exactly what produced them and re-run it, which is what
"[don't trust any one tool](/notes/method.md)" requires.

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
