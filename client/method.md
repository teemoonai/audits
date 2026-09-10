> **teemoonai/audits** — the tool-independent audit method, client side.
> Companion to the server-side method in [`/notes/method.md`](/notes/method.md).
> Architecture: [`ARCHITECTURE.md`](ARCHITECTURE.md) · Surface: [`audit-surface.md`](audit-surface.md) · Pages: [`README.md`](README.md).

# Plaintext-Exfiltration Source Audit — teemoon Client

A **tool-independent** procedure for auditing whether the teemoon app on your
phone can move your plaintext — prompt text, model replies, or your provider
API keys — to a place you did not intend. Like the server-side method it pins
exact source commits so that anyone — a different LLM/agent, an independent
reviewer, or you — can run the identical review and compare. Its credibility
must not depend on trusting any one tool, including the ones that produced the
pages here.

> Scope is the **device**: the app process, what it stores, what it copies,
> and every network stack it can reach. It is deliberately orthogonal to the
> server-side method: that one audits near.ai's attested images, manifests and
> guest OS; this one audits the other end of the same encryption. Neither
> depends on the other, and a reader wanting to know "is my plaintext
> exfiltrated?" needs both.

> **Findings from running this procedure:** the per-release pages in
> [`teemoon-ios/`](teemoon-ios/) *are* the result, keyed to the exact tag and
> commit each reviewed. This document is the *method*; those are the *results*.

---

## 1. Threat model the audit must answer

**"Private"** here means: on the device, message plaintext and provider keys
are visible only to (a) you, on screen, and (b) the send path you aimed at —
the sealed near.ai request, the home or cloud endpoint you configured, or the
on-device model. "Other place" means a log, a file that is unprotected or
included in backups, the system pasteboard, a second network destination, or
any third-party SDK.

The device has no enclave. Apple's OS, its sandbox, its data-protection
classes and its Keychain are the substrate, and they are trusted the way the
server-side audit trusts the TDX hardware: this audit asks the orthogonal
question the platform cannot — does the **app's own code** handle plaintext
safely, or does it copy it somewhere observable?

Where plaintext legitimately exists on the device:
- the **app process** — it composes prompts and decrypts replies (must);
- the **conversation store** and its search index, in a protected class,
  excluded from backup;
- the **on-device inference runtime**, in-process, when you run a local model;
- the **plain transport**, when you chose a non-attested endpoint — that
  endpoint reads plaintext by definition, and the audit's job is to confirm
  nothing else does and the UI never calls it sealed.

**Keys are the second axis, and on the device they are as important as the
messages.** A provider API key is what lets anyone bill you and speak as you;
the near.ai key is the identity the whole attested session hangs on. "Private"
for a key means: it exists in the Keychain and in the memory of a request to
**the provider it belongs to**, and nowhere else. A key reaching a log, a file
outside the Keychain, the general pasteboard, a URL query string, an exported
script, a screenshot-able surface the user did not open, or **any host other
than its own provider** — a probe, a catalog fetch, a third-party service — is
a finding. The one pre-publish key finding was exactly that last kind: a
certificate-agnostic TLS probe carrying the Bearer token.

Everywhere else, plaintext is a finding. Two kinds of path count, and the
second is the one that has actually produced findings:
- paths that need **no user action** (a render, a launch, a background event);
- paths driven by **adversary-controlled content** — a hostile or
  prompt-injected model reply, a tool result, a search-grounding snippet, a
  pasted document. **Assume the model and the provider are hostile.** The
  server-side audit protects you from the operator; this one has to protect
  you from the model you are talking to.

---

## 2. Exact audit scope (pinned releases)

A client build carries no attestation. The identity a page can claim is the
**commit the release tag points at**; the binding from the App Store binary to
that commit is the developer's word (§5). Re-derive the table before trusting
it.

| App Store release | tag | commit | reviewed | page |
|---|---|---|---|---|
| 1.0 (25) | `v1.0.0` | `2d9e206c099a6cd85289bd7c5af8a385c441b2bd` | 2026-08-31 / 09-01 | [`v1.0.0-2d9e206.md`](teemoon-ios/v1.0.0-2d9e206.md) |
| 1.0.1 (26) | `v1.0.1` | `0dfad8bb4733ea8ca8140c6b33acc2a67e66fa75` | 2026-09-10 | [`v1.0.1-0dfad8b.md`](teemoon-ios/v1.0.1-0dfad8b.md) |
| 1.0.2 (33) | `v1.0.2` | `21d534e6e6f70e750f5654e4b27ffc41592c4101` | 2026-09-10 | [`v1.0.2-21d534e.md`](teemoon-ios/v1.0.2-21d534e.md) |

What is in scope at every release, and its plaintext exposure:

| Component | Path in the tree | Plaintext exposure |
|---|---|---|
| App target | `teemoon/` | **plaintext** — composer, store, transports, renderer, Siri entry, tools, logs |
| Generation seam | `Packages/ModelBackend` (over `huggingface/AnyLanguageModel`) | plaintext — the tool-round loop shared by every place a model runs |
| On-device runtime wrapper | `Packages/LiteRTLM` (vendored Google LiteRT-LM Swift, patch register in its `VENDORING.md`) | plaintext — feeds the native `CLiteRTLM` xcframework, which is a **binary** (not source-auditable) |
| Quote parser | `Packages/TDXQuoteVerifier` | none — attestation bytes |
| Markdown renderer | `Vendor/textual` (vendored, `VENDORING.md`) | plaintext — renders every reply; owns an image loader with its own `URLSession` |
| SPM dependencies | `teemoon.xcodeproj/.../Package.resolved` | audit for telemetry/analytics/crash SDKs and for anything that makes its own network requests |
| Build configuration | `teemoon/Info.plist`, `teemoon/teemoon.entitlements`, `project.pbxproj` | defines background modes, file sharing, extensions, ATS — §4 |

Test targets (`teemoonTests/`, `teemoonUITests/`) are not shipped and are out
of scope. `#if os(macOS)` branches are not a shipped product. `#if DEBUG`
blocks are compiled out of the App Store binary and are read only to confirm
the fence is real.

Highest priority, in order: **renderer and every other no-tap path →
send-path gate and seal → alternate entry points → model-callable tools →
at-rest store and sidecars → logs and diagnostics → pasteboard → keys →
dependencies and build config**. The [audit surface](audit-surface.md) says
*where* each of these has actually produced a finding.

---

## 3. The portable audit prompt

Paste the block below into any capable coding agent or LLM with code-reading
tools, hand it to a human reviewer, or adapt it for static analysis. It is
self-contained and names no specific tool. Substitute the tag and commit for
the release you are reviewing; for a point release, add the delta form at the
end.

```text
CLIENT PLAINTEXT-EXFILTRATION AUDIT — teemoon iPhone client (teemoon-ios).
Defensive review of public open-source code (AGPL-3.0) to verify a privacy claim.

THE TWO QUESTIONS
(1) PLAINTEXT. On the user's device, can anything move prompt text or model
replies to a place the user did not intend: a log, an unprotected or
un-backup-excluded file, the system pasteboard, or a network destination other
than the send path the user aimed at (the sealed near.ai request, the
home/cloud endpoint they configured, or the on-device model)?
(2) KEYS. Can a provider API key reach anywhere but the Keychain and a request
to the provider it belongs to: a log, a file, a URL query, the general
pasteboard, an exported script or share sheet, an unmasked screen the user did
not open, or ANY host other than its own provider (a probe, a catalog fetch, a
third-party service)?
For both: count paths that need NO user action and paths driven by
ADVERSARY-CONTROLLED content (a hostile or prompt-injected model reply, a tool
result, a search-grounding snippet, a pasted document). Assume the model and
the provider are hostile. This is the device axis; do NOT audit near.ai server
images, manifests, or OS.

TARGET (audit at the EXACT commit)
  teemoon-ios   github.com/teemoonai/teemoon-ios   tag <TAG>  @ <FULL SHA>
Obtain with:  git clone https://github.com/teemoonai/teemoon-ios
              && cd teemoon-ios && git checkout <TAG>
              && git rev-parse HEAD        # must equal <FULL SHA>
Shipping tree: teemoon/ (app), Packages/{LiteRTLM,ModelBackend,TDXQuoteVerifier},
Vendor/textual, and the SPM graph in Package.resolved. Tests are not shipped.
The app is iPhone-only; #if os(macOS) branches are not a product.

METHOD
For each place plaintext exists, trace to every sink it can reach and decide,
with file:line evidence, whether a leak is reachable. Finder→refuter: try to
disprove each suspected leak before reporting it. A finding sensitive before
it is fixed gets file:line pointers, never a working exploit recipe.

SURFACES (each gets an explicit answer, clean or not)
1. SEND PATH & EGRESS — is send-authorization ONE definition that the composer,
   any retry/re-ask path, and every alternate entry consult; does E2EE sealing
   fail CLOSED (throws; a byte-identical body throws; an attested provider with
   no peer is refused); does the request session persist cookies/cache; any
   URLSession anywhere that fetches a content-influenced URL.
2. CONTENT RENDERERS — does any renderer (markdown, HTML, image, link preview,
   favicon, embed, web view) fetch a URL from model or user content ON RENDER,
   no tap. Read the vendored renderer's attachment/image loader and confirm
   the app disables it on every transcript hosting root, streaming included.
3. AT REST — the conversation store and EVERY sidecar holding message text
   (search index, -wal, -shm): data-protection class and backup exclusion,
   applied and RE-APPLIED each launch. The provider config file: no key in it.
4. ALTERNATE ENTRY POINTS — Siri/Shortcuts intents, widgets, share/notification
   extensions, URL schemes, Spotlight, Handoff, a re-send after backgrounding.
   Each must go through the gate in (1).
5. MODEL-CALLABLE TOOLS — enumerate every Tool the engine can offer. For each:
   what content the model can put in its arguments, which host(s) it reaches,
   whether it is opt-in, whether it fetches URLs the model chose, whether it
   reads plaintext beyond the current thread (history search) and what it
   returns to the model.
6. ON-DEVICE INFERENCE — the native runtime the wrapper links: what it can log,
   where stderr goes, any file it writes, any network it has. State plainly
   what is a binary and could not be read.
7. LOGS & DIAGNOSTICS — every Logger/os_log/print: could an argument carry a
   body, a prompt, a key; at what privacy level; any bounded preview helper and
   its bound. Every diagnostic writer (hang reporter, traces, stderr capture):
   is it #if DEBUG, env-gated, or live in Release; where does it write; what
   does it capture. Crash/analytics reporters.
8. PASTEBOARD — are secrets confined to a local/concealed/expiring pasteboard;
   any general-pasteboard or Handoff write that is not a user tap on visible
   content; the debug panel's redaction on COPY (not just on screen).
9. KEYS — trace every key from entry to exit. Entry: the field type
   (SecureField / reveal toggle), autofill classification. Storage: Keychain
   accessibility class, synchronizable flag, backup behaviour; confirm no key
   in the config JSON, UserDefaults, or any file. Exit: ENUMERATE EVERY request
   that attaches a key (every `Authorization` / provider-header set) and name
   the host each reaches; each must be the key's own provider or an endpoint
   the user configured together with that key. Any probe that accepts any
   certificate must carry no key. Any URL query carrying a key. Error and
   debug structs that carry request headers: where they surface (screen,
   copy, persistence) and the redaction on each path. Exported artifacts (a
   self-verify script, a share sheet): confirm the key is read from the
   environment, never embedded. Log lines that interpolate a key at any
   privacy level. UI-test seeding compiled out.
10. DEPENDENCIES & BUILD CONFIG — Package.resolved and Vendor/: any
    telemetry/analytics/crash SDK, any component with its own network client.
    Info.plist and entitlements: background modes, file sharing, ATS
    exceptions, app groups, iCloud, extension targets.

RULES
- Cite file:line at the pinned commit for every claim, clean or not.
- Distinguish "code CAN see plaintext" (structural — the whole app can) from
  "code COPIES plaintext to a sink" (the finding). Only the latter is a finding.
- Report uncertainty explicitly. Absence of evidence is not proof — if a path
  is a binary or too large to trace, say so under NOT TRACED.
- DEBUG-fenced code is compiled out; confirm the fence, then say so.

OUTPUT
- A verdict line opening with a class — private / leaks / compromisable /
  qualified-pass / inconclusive — plus caveats.
- Findings as `### SEVERITY (deployed: yes/no[ — qualifier]) — title`, each
  with file:line evidence and a concrete leak scenario.
- Per surface (1–10): traced, with the evidence; or not traced, by name.
- The runtime pass (method §4b): each of its four measurements, with the
  observed endpoint list, or the step skipped and why.
- Residuals that are by design, stated not hidden.
- What was not covered.

DELTA FORM (point releases). Add:
  Previously reviewed: <TAG_PREV> @ <SHA_PREV> (verdict on file).
  Produce the shipping-code diff (tests, docs, assets excluded):
    git diff <SHA_PREV> <SHA> -- . ':(exclude)*Tests*' ':(exclude)*.md' \
      ':(exclude)*.png' ':(exclude)*.xcassets*'
  Read EVERY hunk; for each, trace from where plaintext exists to any sink it
  touches, reading unchanged surrounding code as needed. Then re-read every
  load-bearing claim of the previous page at its new line numbers and report
  each as unchanged / weakened / strengthened. Confirm Package.resolved,
  entitlements and Info.plist are byte-identical or say what changed.
```

---

## 4. Build-configuration checks (no source needed)

Some assurance comes straight from the build manifests — the client's analog of
the server side's manifest-only checks. Verify these directly:

- **`Info.plist`**: no `UIBackgroundModes` (a background URLSession needs none,
  so its presence would mean a new capability); no `UIFileSharingEnabled` or
  `LSSupportsOpeningDocumentsInPlace` (the `Documents` folder stays private);
  `NSAppTransportSecurity` allows only local networking (home servers), no
  arbitrary-loads exception.
- **Entitlements**: app sandbox, `network.client`, one Keychain access group,
  user-selected read-only files. No app groups, no iCloud containers, no
  push, no extensions sharing the group.
- **`project.pbxproj`**: exactly one application target plus test bundles — no
  extension, widget, or share target; `TARGETED_DEVICE_FAMILY = 1`.
- **`Package.resolved`**: enumerate every dependency; none is a
  telemetry/analytics/crash SDK. At `v1.0.2` the app graph is AnyLanguageModel,
  dcap-qvl-swift, EventSource, JSONSchema, PartialJSONDecoder, swift-atomics,
  swift-collections, swift-concurrency-extras, swift-nio, swift-secp256k1,
  swift-syntax, swift-system, swiftui-math; the vendored renderer adds pointfree
  test/support packages.

---

## 4b. Runtime pass (required per release)

The server side cannot observe its enclave; the client side can be run. A
static read answers "does the code copy plaintext"; this pass answers "does
the running app, including the binaries the source read cannot see, actually
do it." It is mechanical, needs no reading, and every release page records
its result or says which step was skipped and why. Build the tag yourself,
run it on a simulator, and measure four things while a scripted session
sends and receives messages:

1. **Egress.** Record every remote endpoint the app process opens during the
   session and map each to a host the source names. Root-free: poll
   `lsof -a -i -n -P -c teemoon` and reverse-resolve; with packet-capture
   permission, `tshark -i en0 -Y 'tls.handshake.type == 1' -T fields -e
   tls.handshake.extensions_server_name` gives exact hostnames. Any endpoint
   not in the exits table is a finding. This is the one measurement that
   covers the native inference runtime.
2. **Logs.** Stream the unified log for the app process
   (`xcrun simctl spawn <sim> log stream --predicate 'process == "teemoon"'`)
   through the session, then search it for the session's message text and
   for credential patterns. Attribute every hit to its subsystem: the UI-test
   runner logs accessibility snapshots inside the app process, which is a
   harness artifact, not the app; an `ai.teemoon` hit is a finding.
3. **Keychain.** Read the simulator's Keychain database attributes only —
   `sqlite3 <sim>/data/Library/Keychains/keychain-2-debug.db "select agrp,
   pdmn, sync from genp"` — and confirm the app's items carry the protection
   domain the source claims (`ck` = AfterFirstUnlock) and `sync = 0`. Never
   select the `data` column.
4. **Container.** After the session, inventory the app's data container
   (`xcrun simctl get_app_container <sim> ai.teemoon.app data`): list every
   file; search all of them for the session's message text and for the
   provider key's value (compare, never print); read UserDefaults key names
   and cookie-storage tables; and **parse the URL cache's archived requests**
   (`Library/Caches/<bundle>/Cache.db`, table `cfurl_cache_blob_data`, column
   `request_object`, a binary plist — a byte grep misses UTF-16 strings) for
   any `Authorization` or provider-header value. Message text may appear only
   in the store and its search index; a key may appear nowhere; anything else
   that holds prompt text is a finding. The 1.0.2 pass found the near.ai key
   in that cache after neither source read had.

What the simulator cannot measure: iOS data-protection classes are not
enforced there, so the store's `.completeUnlessOpen` claim stays a source and
unit-test claim; and the shipped UI-test harness runs the app on an in-memory
store, so step 4 sees the store only when the session is driven by hand.
Record both as skipped when they are.

---

## 5. Reproducing the scope (don't trust §2's table)

1. **Tag → commit.** `git clone` the repo, `git checkout <tag>`, `git rev-parse
   HEAD`, and compare with the page's full sha. Tags are mutable; the sha is the
   identity, and a page pins the sha.
2. **The one thing the tag cannot give you.** Nothing binds the binary Apple
   delivered to your phone to that commit: there is no build attestation, no
   reproducible build, and the developer builds and uploads from a workstation.
   The App Store listing's version and build number (`1.0.2 (33)`) match the
   tag's `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION` in `project.pbxproj`,
   and that is the developer's claim, not a proof. This is the client-side
   counterpart of "GitHub Actions as trusted builder" on the server side, and
   it is weaker. To remove it: build the tag yourself with Xcode and install
   that on your device — the source is public precisely so that you can.
3. **History can be rewritten.** The public repository was re-rooted once after
   the 1.0 review (the reviewed commit `3521656` became an orphan; the
   replacement root `2d9e206` has an identical tree). A page pins a sha; if the
   sha you check out is not reachable from any branch, compare trees
   (`git rev-parse <sha>^{tree}`) before concluding the page is stale.
4. **TestFlight builds** are tagged `tf/<version>-<build>` and are not App
   Store releases; a page exists only for App Store tags unless it says
   otherwise.

If your checkout differs from what a page pinned, the developer has released
again — audit *your* tag, and note the drift.

---

## 6. Interpreting results

- **PRIVATE / QUALIFIED-PASS** → no path copies plaintext or keys out of the
  process except the send path you chose and the protected store; qualified
  when residuals exist that a reader should weigh (an opt-in content-driven
  egress, a by-design backup behaviour, a diagnostics hook in the release
  binary).
- **LEAKS** → the exact sink with file:line: the log line, the file, the
  pasteboard write, the host.
- **COMPROMISABLE** → a path that is closed at the reviewed configuration but
  that content, a setting, or an entry point could open without a code change.
- **INCONCLUSIVE** → identity could not be established, or a load-bearing path
  could not be traced. Honest gaps are part of the result.

Residual trust the audit cannot remove: Apple's OS, sandbox, data protection
and Keychain; the App Store's signing and thinning of the uploaded binary
(§5.2); the native on-device runtime binary; the vendored renderer beyond its
loader entry points unless re-read; and the endpoint you chose when it is not
near.ai — it reads your plaintext because you sent it there.

## 7. What this audit does not cover, on purpose

A reader should not assume a page checked these. They are adjacent to the
question and answered elsewhere or not at all:

- **Correctness of the E2EE itself.** A wrong seal would expose plaintext in
  transit without touching any sink these pages look at. The client repo's
  `ATTESTATION.md` describes the construction (X25519, HKDF, XChaCha20-Poly1305
  via CryptoKit; the only hand-written primitive is HChaCha20, pinned to the
  IETF draft vectors) and its tests pin it. This repo verifies that sealing
  fails closed and that the key is bound to the attested quote — not that the
  cipher is used correctly.
- **What dependencies do on the network.** The pages check `Package.resolved`
  for telemetry and crash SDKs and read the vendored renderer's loader. They do
  not trace the Hugging Face model layer, the SSE client, the DCAP verifier, or
  the secp256k1 binding for network calls of their own. The runtime pass's
  endpoint list is the only evidence on that, and it covers only the code paths
  a session exercised.
- **Whether the UI's claims match what the code verifies.** The client repo's
  security policy treats an overstating checkmark as a security bug; that is a
  separate review of the attestation surface, not of exfiltration.
- **A jailbroken or otherwise compromised device**, and Apple's platform
  itself.
- **Metadata.** Model id, sampling parameters, message count and ciphertext
  lengths are readable by the gateway by protocol; the server-side pages cover
  that perimeter.
