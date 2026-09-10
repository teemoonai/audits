# client — the teemoon app on your device

> **teemoonai/audits** — the client side of the one question. Method:
> [`method.md`](method.md) · Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md) ·
> Surface: [`audit-surface.md`](audit-surface.md) · Server side: [`/README.md`](/README.md).

The other end of the end-to-end encryption. The app composes every prompt and
decrypts every reply, so it holds your plaintext unconditionally — that is
structural, not a finding. The question this tree answers is the same one the
server-side pages answer for each attested image: **can anything on the device
copy that plaintext to a place you did not intend** — a log, an unprotected or
backed-up file, the system pasteboard, or a network destination other than the
sealed send path you chose? And its device-side twin: **can your provider API
key reach anywhere but the Keychain and the provider it belongs to?**

**One page per audited release, named by tag and commit.** A client build has no
attested digest: nothing measures an App Store binary, and Apple re-signs and
thins what the developer uploads. The identity a page can honestly claim is the
**git commit the release tag points at**, so pages are named
`<tag>-<short sha>.md` and each pins the full sha. What binds the binary on your
phone to that commit is the developer's word — [`method.md` §5](method.md#5-reproducing-the-scope-dont-trust-2s-table)
says what you can do about that (build it yourself), and no page here claims
more.

## teemoon-ios (iPhone)

Source: [github.com/teemoonai/teemoon-ios](https://github.com/teemoonai/teemoon-ios),
AGPL-3.0. iPhone-only (`TARGETED_DEVICE_FAMILY = 1`); the tree's `#if os(macOS)`
branches are not a shipped product. The Android client is a separate codebase
and will get its own lineage when it ships.

### audited releases

| App Store release | tag → commit | verdict | review |
|---|---|---|---|
| 1.0 (25) | [`v1.0.0` → `2d9e206`](teemoon-ios/v1.0.0-2d9e206.md) | QUALIFIED-PASS — private at the reviewed tree; one HIGH (no-tap markdown-image auto-fetch) found and fixed before publish; residuals are by design | full review 2026-08-31, re-pinned to the public root 2026-09-01 |
| 1.0.1 (26) | [`v1.0.1` → `0dfad8b`](teemoon-ios/v1.0.1-0dfad8b.md) | QUALIFIED-PASS (carried) — zero app-code change from 1.0; covered by the 1.0 read | delta 2026-09-10 (tree comparison) |
| 1.0.2 (33) | [`v1.0.2` → `21d534e`](teemoon-ios/v1.0.2-21d534e.md) | QUALIFIED-PASS — no new plaintext or key sink in the 38-file delta; keys leave only to their own provider; two independent reviewers, no finding; two new by-design residuals | delta 2026-09-10 (two blinded reviewers) |

A release not listed here has not been audited. The same fail-closed rule the
server-side pages follow applies: no page, no claim.

### what "the client" contains

At every audited release the shipping tree is the app target `teemoon/`, three
local packages (`Packages/LiteRTLM` — Google's LiteRT-LM on-device runtime,
vendored; `Packages/ModelBackend` — the transport-agnostic generation seam over
Hugging Face's `AnyLanguageModel`; `Packages/TDXQuoteVerifier`), the vendored
markdown renderer `Vendor/textual`, and the SPM dependencies pinned in
`Package.resolved`. Test targets are not shipped and are outside every page's
scope. [`ARCHITECTURE.md`](ARCHITECTURE.md) maps where plaintext lives in that
tree and every sink each page has to clear.
