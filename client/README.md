# client — the teemoon app on your device

> **teemoonai/audits** — the client side of the one question. Method:
> [`method.md`](method.md) · Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md) ·
> Surface: [`audit-surface.md`](audit-surface.md) · Server side: [`/README.md`](/README.md).

The other end of the end-to-end encryption. The app composes every prompt and
decrypts every reply, so it holds your plaintext unconditionally — that is
structural, not a finding. This tree answers two questions, keys first
because in a bring-your-own-key app the key is the asset the app alone
custodies and the one most easily leaked: **can your provider API key reach
anywhere but the Keychain and the provider it belongs to?** And the same
question the server-side pages answer for each attested image: **can anything
on the device copy your plaintext to a place you did not intend** — a log, an
unprotected or backed-up file, the system pasteboard, or a network destination
other than the sealed send path you chose?

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
with its own lineage below.

### audited releases

| App Store release | tag → commit | verdict | review |
|---|---|---|---|
| 1.0 (25) | [`v1.0.0` → `2d9e206`](teemoon-ios/v1.0.0-2d9e206.md) | QUALIFIED-PASS — messages private; one HIGH (no-tap markdown-image auto-fetch) fixed before publish; MEDIUM key-in-URL-cache (fixed in 1.0.3) and LOW system-prompt-in-UserDefaults found later by running 1.0.2, present here | full review 2026-08-31; findings back-applied 2026-09-10 |
| 1.0.1 (26) | [`v1.0.1` → `0dfad8b`](teemoon-ios/v1.0.1-0dfad8b.md) | QUALIFIED-PASS (carried) — zero app-code change from 1.0; the 1.0 findings carry | tree comparison 2026-09-10 |
| 1.0.2 (33) | [`v1.0.2` → `21d534e`](teemoon-ios/v1.0.2-21d534e.md) | QUALIFIED-PASS — no new sink in the delta and a live session opened no endpoint the map does not name; **runtime pass found the near.ai key at rest in the URL cache (MEDIUM, since 1.0, fixed in 1.0.3)** and the system prompt in UserDefaults (LOW) | delta 2026-09-10, two blinded reviewers + runtime pass |
| 1.0.3 (35) | [`v1.0.3` → `7edcb55`](teemoon-ios/v1.0.3-7edcb55.md) | QUALIFIED-PASS — **the MEDIUM is closed**: the shared URL cache is emptied and made zero-capacity before any session exists, and running the build found zero archived requests and the key in no file, including on a container brought from 1.0.2; nothing on the plaintext path changed; the LOW system-prompt-in-UserDefaults carries | delta 2026-09-11, two blinded reviewers + runtime pass over a 1.0.2 container |
| 1.0.4 (38) | [`v1.0.4` → `3abe3e2`](teemoon-ios/v1.0.4-3abe3e2.md) | QUALIFIED-PASS — seventeen key-bearing request sites (five new: OpenRouter, NVIDIA), each to its own provider, each run live; the URL-cache fix was rewritten and measured again over a 1.0.2 container — no cache file survives a launch, the key in no file or log line; INFO: a truncated hash of a keyed provider's key outlives the key in a catalogue file; **LOW found by raising the log level: since 1.0 three unfenced log statements carry reply text and tool arguments** (platform-redacted on a phone); the system-prompt LOW carries; new on-device runtime binary re-checked, no path to the network | delta 2026-09-19 (97 files), two blinded reviewers + runtime pass over a 1.0.2 container and five live providers + binary capability check |
| 1.0.5 (43) — App Store 2026-10-16; public tag `v1.0.5` → `304d6bd`, code-identical | [`tf/1.0.5-43` → `705764b`](teemoon-ios/tf-1.0.5-43-705764b.md) | QUALIFIED-PASS — no finding new at this release: the on-device developer card (numbers and a backend word), the Fireworks refresh, the backgrounded-turn re-ask, the host-classification fix and a launch migration of saved Fireworks places (model id and equipped list only, no network, keys untouched; its one-time notice kept in a small text file of names and prices until dismissed) read clean; the test-only seeding surface is compiled out of Release; the 1.0.4 log LOW is CLOSED at build 43 (counts and lengths, no text at any level, pinned and measured), the system-prompt LOW waived by the user (confirmed directly), the INFO carries; runtime passes on builds 39, 42 and 43: offline and live suites green, every endpoint attributed, no key in any file or log line, no URL cache file | the 1.0.4 chain plus two blinded reviewers on the 38→39 delta and one on 39→42, Claude Fable 5.1; runtime passes 2026-10-15 |

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

## teemoon-android (Android)

Source: github.com/teemoonai/teemoon-android, AGPL-3.0 (private at the time of
the first review). Release tags are `vX.Y.Z[-build]`, one per store release.
A GitHub release whose notes record a **verified** reproducible build binds that
APK to its tag — stronger than the iOS binding, and only for that APK: the Play
build can come from a different commit (1.0.4 (3908) did).

| release | tag → commit | verdict | review |
|---|---|---|---|
| Google Play 1.0.4 (3912) | [`v1.0.4-3912` → `7f504ca`](teemoon-android/v1.0.4-3912-7f504ca.md) | QUALIFIED-PASS — the public tree's code is the audited dev tree ab31bff (file by file, non-comment lines identical; 0 NEW sweep rows, native bytes the audited ones); keys only to their own provider, messages only on the chosen send path, measured live with seven keys and at idle launch; the 3910 MEDIUM, both LOWs and three INFOs closed and measured closed; nothing open; the GitHub release APK (`8411f0e4…ed04`) bound to the tag by the repository's release-verify rebuild and checked against the measured APK on the page; the Play bundle not bound | a chain of ten working reviews (the 3910 full review and nine candidate deltas, not published), two blinded reviewers each (Claude Fable 5.1), runtime pass per candidate 2026-10-13/14 |
| Google Play 1.0.4 (3913) | [`v1.0.4-3913` → `317b040`](teemoon-android/v1.0.4-3913-317b040.md) | QUALIFIED-PASS — the public tree's code is the audited dev tree 1ccca1c (file by file, non-comment lines identical, line numbers unchanged; 0 NEW sweep rows, native bytes the audited ones), which is 3912's code plus LiteRT-LM 0.18.0 / LiteRT 2.3.0 (four new-bytes libraries, each byte-identical to its Google Maven artifact, no network import) and the drafter probe through `ModelInfo.from`; nothing open at any severity; keys only to their own provider, messages only on the chosen send path, measured live with seven keys and at idle launch; the GitHub release APK (`850fc987…3198`) bound to the tag by the repository's release-verify rebuild and checked against the measured APK on the page (libraries and three of four dex byte-identical); the Play bundle not bound | the 3912 chain plus one working review of the dev tree (two blinded reviewers, Claude Fable 5.1, not published), runtime pass 2026-10-15 |
| Google Play 1.0.5 (3915) | [`v1.0.5-3915` → `d8e6854`](teemoon-android/v1.0.5-3915-d8e6854.md) | QUALIFIED-PASS — the public tree's code is the audited dev tree 5c8cfa6 (file by file, non-comment lines identical, line numbers unchanged; 0 NEW sweep rows, native bytes the 3913 release's), which is 3913's code plus the developer card's on-device speed line (one in-memory value read only by the developer-mode card and its copy text; the drafter rule false for every NPU) and 1.0.5's Fireworks preset default and OpenRouter price table (data; no host, header or key change); nothing open at any severity; keys only to their own provider, messages only on the chosen send path, measured live with seven keys and at idle launch on both working builds; the GitHub release APK (`61117a45…c9ae`) bound to the tag by the repository's release-verify rebuild and checked against the measured APK on the page (libraries and three of four dex byte-identical); the Play bundle not bound | the 3913 chain plus two working reviews of the dev trees (two blinded reviewers each, Claude Fable 5.1), runtime passes 2026-10-15 |
| Google Play 1.0.5 (3916) | [`v1.0.5-3916` → `34e5566`](teemoon-android/v1.0.5-3916-34e5566.md) | QUALIFIED-PASS — the public tree's code is the audited dev tree 328d0d4 (file by file, non-comment lines identical, line numbers unchanged; 0 NEW sweep rows, native bytes the 3913 release's), which is 3915's code plus the launch-time migration of saved Fireworks places from the retired `kimi-k2p6` to `kimi-k3` (model id and equipped list only, through the existing config writer; no request of its own; the key endpoint-addressed and untouched; one in-memory notice; three mutations red) and the versionCode; nothing open at any severity; keys only to their own provider, messages only on the chosen send path, measured live with seven keys and at idle launch; the GitHub release APK (`fca19ca0…374e`) bound to the tag by the repository's release-verify rebuild and checked against the measured APK on the page (libraries and three of four dex byte-identical); the Play bundle not bound | the 3915 chain plus one working review of the dev tree (two blinded reviewers, Claude Fable 5.1), runtime pass 2026-10-15 |
| Google Play 1.0.6 (3917) | [`v1.0.6-3917` → `63cef55`](teemoon-android/v1.0.6-3917-63cef55.md) | QUALIFIED-PASS — the public tree's code is the audited dev tree 2630d44 (3917.9; file by file, 0 non-comment lines differ, line numbers unchanged; 1 re-fingerprinted sweep row, native bytes the 3913 release's), the 1.0.6 near.ai SDK alignment and send-path rework reviewed as a whole-tree delta from 3916 plus a full read of `confidential/`: the signature verifier fixed per the SDK, the NVIDIA token verified, the TCB allow-list, the TLS probe's quote DCAP-verified, in-flight verdicts settled before the gate; keys only to their own provider (two keyless NVIDIA calls, a keyless first-send probe to the user's own server, a per-chat routing id under a Keystore key to Fireworks/xAI/OpenRouter only); messages only on the chosen send path (`reasoning_effort`/`max_tokens` plaintext beside the sealed fields on near.ai, disclosed); deleted text scrubbed, the kept on-device conversation memory-only, the on-device thought never shown, saved or logged; one INFO (a reply signature labelled verified without the GPU quote's own verified flag; the send gate compensates); 21 of 24 mutations red where predicted, two test gaps; idle launch zero egress; live suite green except two live causes outside the client (the near.ai launcher's unpublished attestation; xAI's camel-case refusal text, fixed at 3917.9); Pixel 10 Pro, Pixel 8a and CPU disk gates clean; the GitHub release APK (`286105ee…488f`) bound to the tag by the repository's release-verify rebuild (MATCH 194) and checked against the CI artifact and the measured APK on the page; the Play bundle not bound | the 3916 chain plus two blinded working reviews of the dev tree at add2a08 (Claude Fable 5.1), the 3917.9 delta read by the orchestrator, runtime pass and mutation checks 2026-10-22/23 |

The GitHub APK 1.0.4 (3910), Play production 1.0.4 (3908) and the tag `v1.0.4`
have no public page: the 3910 review and the candidate reviews that led to 3912
are the auditor's working pages, summarised in the 3912 page's lineage.
