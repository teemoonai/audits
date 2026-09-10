# The client audit surface — what to open, and what to ask of it

> Companion to [`method.md`](method.md). Editorial, like the server-side
> [`/notes/audit-surface.md`](/notes/audit-surface.md). Every item below is a
> place a client finding has actually come from, or a place the server-side
> comparison showed reviewers skip.

`method.md` says *what* to look for. This list says *where*, so the question
stops being "did the reviewer think to look here" and becomes "did the reviewer
finish the list." Walk it per release. Anything you cannot reach goes under
*Not traced* by name — on a client page that section is as load-bearing as on
a server page, and it currently always contains one item (§6).

---

## 1. Renderers — where the client's one HIGH came from

A renderer is a network client that nobody aimed at the network.

- [ ] The vendored markdown renderer's **attachment / image loader**: what it
      defaults to, which `URLSession` it uses, and whether it runs on render
      with no tap. At 1.0 pre-publish it defaulted to a URL-fetching image
      loader reached by every transcript path — the [HIGH on the 1.0 page](teemoon-ios/v1.0.0-2d9e206.md#the-one-finding).
- [ ] The fix has **two layers** and both must hold on every hosting root,
      streaming included: the `imageURL` strip in the single shared parser, and
      the non-fetching loader installed beside the transcript styling. Confirm
      by reading each root, not by trusting the test name.
- [ ] Any new render surface: link previews, favicons, embeds, `AsyncImage`,
      `WKWebView`, `LPLinkView`, custom emoji. Each is the same question again.
- [ ] `Vendor/textual` is re-read whenever it is bumped — its own examples use
      remote image hosts, which is what its loader is for.

## 2. The send gate and the seal — three pre-1.0 HIGHs

Closed before the public root and regression-pinned; the tests are in the
public tree even though the fixing commits are not.

- [ ] **Fail-open sealing.** The transport once wrapped E2EE sealing in `try?`
      and sent the plaintext body under an E2EE promise on any failure. Confirm
      the seal *throws*, that a byte-identical body throws, and that the
      plaintext path exists only for `codec == nil` (non-attested providers).
      (`teemoonTests/E2EESecurityExploitTests.swift` — the tripwire sees zero
      requests.)
- [ ] **One verdict definition.** `ConfidentialSession.sendPolicy` must be the
      only derivation; a second one is exactly how Siri bypassed the gate.
      (`SendPolicyChokePoint` suite.) A present-but-wrong-length model key must
      degrade, not show green.
- [ ] **A probe that accepts any certificate must carry no credential.** The
      TLS-attestation probe accepts any server cert and checks the fingerprint
      afterwards; it once sent the Bearer token. Confirm the request is
      credential-free and refuses redirects.
      (`probeRequest_carriesNoAuthorizationHeader`.)
- [ ] The request session: ephemeral, no persisted cookies or cache.

## 3. Entry points that are not the composer

- [ ] **Siri / Shortcuts** (`App/RequestLLMIntent.swift`): consults
      `session.sendPolicy` and refuses on anything but `.allow` — a headless
      intent cannot show the confirmation the UI would. Any guard added after
      the gate may only refuse more.
- [ ] **Re-send on return.** Since 1.0.2 an on-device turn cut off by
      backgrounding is re-asked once when the app returns — a no-tap send.
      Confirm it goes through `prepareSend(trust: sendPolicy)` like a tap.
- [ ] Widgets, share extensions, notification extensions, URL schemes,
      Spotlight, Handoff (`NSUserActivity`): confirm the *absence* explicitly
      (`project.pbxproj` targets; grep the frameworks). Saying "none exist" is
      a finding.

## 4. Model-callable tools — content-driven egress

The model writes the arguments. A tool is a way for a hostile model to send
the conversation somewhere.

- [ ] Enumerate every `Tool` conformance the engine can offer, per place a model
      runs (near.ai, home, on-device).
- [ ] For `web_search`: opt-in on a user-supplied key; **one fixed host**;
      result text is extracted and **no result URL is fetched**; keyless it
      only shows an offer card. It remains a by-design residual on every page.
- [ ] **Tools that read beyond the thread.** A model-callable history-search
      tool was excised before 1.0 pending its own review; confirm it is still
      absent, or audit what it returns to the model and to which provider.
- [ ] Any tool that opens or fetches a model-chosen URL changes the verdict.

## 5. At rest — the store and every copy of it

- [ ] The SwiftData store **and** its `-wal` / `-shm` sidecars:
      `.completeUnlessOpen` + `isExcludedFromBackup`, re-applied every launch
      (`App/teemoonApp.swift`, `hardenConversationStore`).
- [ ] **The full-text search index is a second file holding the same text.**
      `ChatSearchService.configure` and `rehardenIfNeeded` must run the
      identical hardening. Adding search would otherwise quietly undo the store's
      protection — the reason this item exists.
- [ ] `ConfigStore`: protection class on the providers JSON, and **no key in
      it** (keys live in the Keychain under the provider id).
- [ ] Model-weight and download bookkeeping files: no message content; the
      failure file is an error string.

## 6. On-device inference — the standing *not traced*

- [ ] `Packages/LiteRTLM` is source; `CLiteRTLM.xcframework` is not. What the
      wrapper passes in, whether verbose logging has a caller, and where the
      process's stderr goes are readable. What the binary prints and writes is
      not. Every page carries this under *Not traced* until someone reads it.
- [ ] `captureNativeLogIfAsked`: env-gated stderr capture to
      `Documents/native.log`, present in the Release binary (not DEBUG-fenced).
      Unreachable without developer tooling and file sharing is off; still,
      record it, and note if it ever becomes a setting.

## 7. Logs and diagnostics

- [ ] Every `Logger(subsystem: "ai.teemoon")` line whose interpolation could be
      a body, a prompt, a key, or a header block: privacy level, and whether a
      bounded preview helper (`previewForLog`, 2048 bytes, `.private`) is the
      only way a body reaches a log.
- [ ] `DiagLog` (env-gated stderr): enumerate every call site; counts and
      literals only.
- [ ] `Support/MainThreadHangReporter.swift` and `Views/Chat/ScrollTrace.swift`
      write to `Documents/`: confirm the whole types are `#if DEBUG` and armed
      only by a launch flag. A backtrace with locals would be a different
      question.
- [ ] No crash or analytics reporter (`Package.resolved`, grep `track(` /
      `logEvent` / the usual SDK names).

## 8. Pasteboard

- [ ] Secrets go through `Clipboard.copySensitive` only: `localOnly`, 120 s
      expiry on iPhone. (`SensitiveClipboardTests`.)
- [ ] General-pasteboard writes: each must be a user tap on visible content
      (message copy, code-block copy, model id). None on render, none on error.
- [ ] The debug panel: credentials redacted on **copy** unconditionally, not
      just on screen. (`DebugCopyRedactionTests`.) The copied dump does
      contain the user's own request and response — a user-initiated copy of
      their own content, stated as such.
- [ ] Handoff / universal clipboard broadcast: absent.

## 9. Keys

- [ ] `kSecAttrAccessibleAfterFirstUnlock`, not `ThisDeviceOnly`, not
      `kSecAttrSynchronizable`: keys restore through an encrypted backup and do
      not sync. A deliberate decision; state it as a residual each time.
- [ ] Any request that sends a key to a host other than its own provider (a
      catalog fetch, a key-check probe, the signature fetch). The near.ai key
      to near.ai is fine; the near.ai key to anything else is a finding.
- [ ] Error text and log lines name the provider, never the key.
- [ ] UI-test key seeding: `#if DEBUG` end to end **and** gated on a launch
      flag; absent from a shipping build.

## 10. Identity, before any of the above

- [ ] `git checkout <tag>; git rev-parse HEAD` equals the page's full sha.
- [ ] If the sha is on no branch, compare **trees** before calling the page
      stale — the public history was re-rooted once with an identical tree.
- [ ] The App Store version/build matches `MARKETING_VERSION` /
      `CURRENT_PROJECT_VERSION` at the tag. That is the developer's claim; the
      page says so, and never claims to have reviewed the binary.

---

## What this list cannot do

Same limit as the server-side list: it closes the gap where a reviewer did not
think to look, and does nothing about a shared blind spot. The client's HIGH
came from a renderer feature that no checklist mentioned. The mitigation is
mechanical: *enumerate every `URLSession` and `URLSessionConfiguration` in the
shipping tree and name the code path that decides each URL* is a grep plus one
read per hit, and it would have surfaced the image loader in seconds. Items 1,
4 and 7 are the best candidates for that treatment.
