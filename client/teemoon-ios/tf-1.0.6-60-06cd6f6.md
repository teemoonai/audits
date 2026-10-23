# teemoonai/teemoon-ios @ tf/1.0.6-60 (06cd6f6) — App Store 1.0.6 (60); public tag `v1.0.6` → `ab64f15`, the same code

## verdict: QUALIFIED-PASS — keys: no new host; every provider key still leaves only in a request to the endpoint it was saved with (the 1.0.5 sites re-read at their new lines, none added, none removed; the near.ai signature fetch keeps its gateway host and key; the two new NVIDIA attestation calls and the first-send probe to the user's own self-hosted server carry no key; the attestation, key-check and search requests move off the default session onto an ephemeral session with no cache); one new non-secret header, a per-chat routing id (an HMAC of the thread id under a per-Keychain secret — AfterFirstUnlock, not synchronizable, so it restores with an encrypted backup — that never leaves the Keychain) to Fireworks, xAI and OpenRouter only, never near.ai, NVIDIA or a home server; messages: the send gate is still one definition and also governs Think Harder and the effort-refusal retry, which is rebuilt and re-sealed from plaintext with fresh per-field envelopes under the same session client key and keeps nothing from the 400 body; reasoning_effort and, on Think Harder, max_tokens are plaintext fields beside the sealed messages on near.ai, by protocol and disclosed; the replaced reply never reaches the model; a stop now cancels the request and a late reply is neither drawn nor saved; the request-body sort touches the plaintext nowhere new; on-device thought reaches neither the store, the card nor a log; the kept on-device conversation is memory only, released on background, memory warning, dead engine, chat delete and the next on-device turn, not on a thread or cloud switch; deleted chats are scrubbed from the store at the next launch and from the index at delete time, on the two chat-delete paths only (replaced and retried replies are not, inside the protected files, a note); the Confidential tree's signature verifier is fixed as the SDK comparison asked (kind branch and signing_algo, model prefix, ed25519 against the quote-bound key, rotation path deleted, gateway signer never verified), NRAS tokens are signature-, issuer-, window- and nonce-checked, the TCB allow-list is the SDK's, the TLS probe quote is DCAP-verified, a pending verdict refuses the send; still open there and stated in ATTESTATION.md: the model compose and os_image_hash unbound, only the first model report verified, no OHTTP, no x-no-aliasing, the debug bit resting on a binary; one new INFO, a verification label not a sink (the key-binding properties behind the model-signer verdict never read whether their quote verified; the DCAP gate blocks a send before any reply is labelled; no test covers it), nothing new above INFO; the system-prompt LOW carries under the user's waiver, the catalogue INFO carries, the log LOW stays CLOSED; the on-device runtime binary is the same pin as at 1.0.4, not re-checked; runtime pass and binary binding are the orchestrator's

| | |
|---|---|
| **client** | teemoon iPhone app — **App Store 1.0.6 (60)**, live on the App Store from 2026-10-23 (the release coordinator's figure); submitted to App Review on 2026-10-23 (ASC: VALID, APP_STORE_ELIGIBLE); its code is build 59's (`378f8ba`) to the byte — the unsigned Mach-O hashes the same — plus the build number and the two accepted `ATTESTATION.md` commits (build-60 addendum). Build 59 was uploaded TestFlight-internal-only on 2026-10-22 and could not be attached to the App Store version. The body of this page reads build 58 (`d7ac963`), of which 59 is the descendant by one shipped change (the xAI refusal matcher, `09dcb6e`) and one test-only commit — the build-59 addendum below reads that delta. Builds 50, 51, 54, 56, 57 and 58 preceded it on TestFlight (55 skipped; 52 and 53 were version bumps), per the developer's hand-offs |
| **identity** | tag `tf/1.0.6-60` → commit `06cd6f6ed56f636d9dde4b1bdc1fcf600825f34a` (`06cd6f6`), resolved by the orchestrator in the development clone: its tree equals `9fc55ec` (the accepted documentation commit) in every file but `project.pbxproj` (`CURRENT_PROJECT_VERSION` 59 → 60, twice), and `git diff --stat tf/1.0.6-59 tf/1.0.6-60` is `ATTESTATION.md` (+21/−6) and that bump; build 59 was tag `tf/1.0.6-59` → commit `378f8ba405363fc2d281881639288efe3c593024` (`378f8ba`, tree `69b0e37d354ec7af90bf2b48f1379425eba9529e`), a detached worktree checked out and `git rev-parse HEAD` compared by the orchestrator; the body of this page reads `tf/1.0.6-58` → `d7ac9639fad0c4c36c7dbb9968ea7b35a2c7468d` (`d7ac963`, tree `ea783301652695ae5f8acb5be5d42148f7f91c2a`), confirmed by the reviewer's own `rev-parse`, of which `378f8ba` is the descendant by `09dcb6e` (shipped), `f4ceb4e` (tests only) and the build bump |
| **seen in** | App Store 1.0.6 (60) from 2026-10-23; TestFlight internal builds 58 and 59 before it |
| **source** | [github.com/teemoonai/teemoon-ios](https://github.com/teemoonai/teemoon-ios) at `v1.0.6` → commit `ab64f1515baadab42f85ca2539548557ca233cf6` (tree `2d3caf532001…`, parent `304d6bd`, the 1.0.5 public commit; annotated tag object `530a2742f1ab8093bd00adbef129583e5e9e06a5`, tagger garry, 2026-10-23 19:11 UTC, message "chore(release): 1.0.6 (60)"), the public squash of the audited dev tree `tf/1.0.6-60` → `06cd6f6`, read from a scratch clone after the push with the development tag fetched beside it; the release notes link this page. **Its code is the audited tree:** `git diff 06cd6f6 ab64f15` lists 323 files — the development-only files removed (`docs/`, `tools/`, `scripts/`, `design/`, `conformance/`, `Playgrounds/`, `CLAUDE.md`, `Makefile`; the public top level is `ATTESTATION.md`, `Packages`, `Vendor`, `teemoon`, `teemoon.xcodeproj`, the two test targets, `assets` and the repository files) and, under the shipping tree (`teemoon/`, `Packages/`, `Vendor/`, the project file), **7 files, +8/−8, every changed line a comment** (the developer's name rewritten to "the maintainer" and one "pm's eval" to "an internal eval" in `LastRequestDebugInfo.swift`, `ReasoningEffort.swift`, `TurnPhases.swift`, `ProviderStore+Healing.swift`, `ReplyActionsMenu.swift`, `RequestDebugView.swift`, `StreamingMessageView.swift`), each file's line count unchanged, so every line number on this page holds at `ab64f15`; `Info.plist`, the entitlements, `Package.resolved`, `Vendor/` and `Packages/` byte-identical; `ATTESTATION.md` is the `9fc55ec` text accepted below. The preflight run on the public tree against this page's ledger: shipping diff those 8 comment lines, config diff empty, sweep 835 rows all CARRIED, 0 NEW (`sweep/v1.0.6.tsv`). `conformance/requests.json` is not in the public tree (development-only); its sha256 at the tag was `642d7555…` |
| **binary binding** | build 60, the App Store submission, re-hashed by the orchestrator: the submitted IPA (App Store Connect export, this time the bytes Apple received) `f0b3dc521aa5f0ddf59e83b655ca16b455d7012b77e8971ea5799c55429e396f`; `teemoon-b60.xcarchive.zip` `96cea1bb7cf45b85685a56d2a2d556465a7d1c17376351cb5c5423a93dc75839`; signed Release binary `5bb01e20b8c0523cf0d562f3cd28c6ab442b55b85d86157dd71889cdd5ebef6e`; **both the archive binary and the IPA's Payload binary strip (`codesign --remove-signature`) to `08cb2c1b905a03bae238c1278b4ab5c82e9566c41a034da7b192070200263856`, the same Mach-O as build 59 and as the storage-gate probe build**; `Info.plist` 60 / 1.0.6 / `ai.teemoon.app`; 0 `__llvm_prf` sections; `conformance/requests.json` `642d7555…` unchanged. Build 59, the developer's archive of `378f8ba`, re-hashed by the orchestrator: Release binary `teemoon.app/teemoon` sha256 `ba8b758344761cb26713bf6b5efc793c89b612bfde958b322fe0eca0146532a9` (`08cb2c1b905a03bae238c1278b4ab5c82e9566c41a034da7b192070200263856` after `codesign --remove-signature`); `teemoon-b59.xcarchive.zip` `ca2ca5f324f45b1219ad0d17bcb7759dee7f0aca9c43661cee7b9009c9a055b1`; IPA (export-only re-export) `500692a747efd37188bce401ae99f09f07a50ba80825ca612698aa81a5b3b500`; `Info.plist` 59 / 1.0.6; 0 `__llvm_prf` sections. Build 58 (`d7ac963`), the body's commit: Release binary `40788098ed33de3cb82a20ac19e16b68d8c17e45865b402c8ff5337129adeeb6`; `teemoon-b58.xcarchive.zip` `0d324f414263010aac500778fccc036d1df7abacb96450e1ce6390cee0fa22da`; IPA `25c767ce20e3a35e5597717dd6e61af7a28cfe12d9405d53fabcb66272c7ce24`; `MARKETING_VERSION 1.0.6`, `CURRENT_PROJECT_VERSION 58` at `project.pbxproj:545`, `:569`, `:595`, `:619`. No reproducible build binds an iOS binary to a commit ([`method.md` §5.2](../method.md#5-reproducing-the-scope-dont-trust-2s-table)): the archive's provenance from `d7ac963` is the developer's statement of a clean `git archive` of the tag, as on every iOS page. None of this was reproduced by this review. |
| **review** | independent AI source review, Claude Fable 5.1 (reviewer A), 2026-10-22 — delta from [`tf-1.0.5-43-705764b.md`](tf-1.0.5-43-705764b.md) (`705764b` = App Store 1.0.5 (43), code-identical to public `v1.0.5` → `304d6bd`), plus a full read of `teemoon/Confidential/` (38 files) against the near.ai SDK comparison; static source read; blinded from the second reviewer; skeleton page written before the first source read. Runtime pass and binary check are the orchestrator's. Method: [`/client/method.md`](/client/method.md) |

**coverage:** every hunk of the shipping-code diff `705764b → d7ac963` under
`teemoon/` (57 files, +1938/−349 by `git diff --stat`; the prep tool's 58th
file is `project.pbxproj`, whose only change is the two version lines) read in
full and traced from where a key or plaintext exists to any sink it touches,
with the unchanged neighbours read as needed; **all 38 files of
`teemoon/Confidential/` read whole** (9,666 lines), the ten changed ones line
by line, and each line of the SDK comparison's "weaker" and "bugs" lists
answered with file:line and the test that pins it; the project file read for
the compilation conditions of both configurations; every load-bearing claim of
the 1.0.5 page re-read at its `d7ac963` line; the orchestrator's 835-row
fingerprint sweep of the whole tree skimmed in context and its 56 NEW rows
adjudicated one by one; the whole-tree negative greps (auth headers, URL
sessions, query items, pasteboard, delete paths, logger interpolations,
`DiagLog`, `print`) quoted below with their counts. The nine priority items
of the reviewer brief are each answered. Not read: the on-device runtime
binary (same pin as at 1.0.4), upstream LiteRT-LM source, the dcap-qvl Rust
core (a binary xcframework), the vendored renderer beyond confirming it is
byte-identical, and the large view files outside their hunks. Nothing was
run; no network request was made; the privacy web page was not fetched.

---

# teemoon iPhone client (1.0.6 candidate) — Key and Plaintext Exfiltration Audit (delta from `705764b`)

> Client side of the teemoon plaintext question. Lineage: [`../README.md`](../README.md)
> · Map: [`../ARCHITECTURE.md`](../ARCHITECTURE.md) · Surface: [`../audit-surface.md`](../audit-surface.md)

Build 58 is the "near.ai SDK alignment + performance" release: fifty-odd
merges from `release-1.0.6` over the 1.0.5 store build. For keys it means a
new per-chat routing header to three cloud providers, a new per-Keychain
secret behind it (it restores with an encrypted backup, like the keys), a new egress to the user's own self-hosted server
on a first send, a rewritten signature verifier whose fetch still carries the
near.ai key, two new keyless calls to NVIDIA's attestation service, and a
change of URL session under every authenticated attestation, key-check and
search request. For plaintext it means new fields beside the sealed messages
(`reasoning_effort`, and `max_tokens` on Think Harder), a 400-driven retry
that rebuilds and re-seals the request, a reply-supersession that must keep
the replaced reply out of the next request, a stop that must actually cancel
the request, an on-device conversation kept in memory between turns, Gemma
thinking that must never be shown or saved, a request-body sort that must not
touch the plaintext anywhere else, and the deleted-text residue work in the
store and its search index. Each is traced below; the Confidential tree gets
its own full section because the brief asked for it and because its changes
are where a verifier could have started sending something it did not before.

## Audit prompt

The portable prompt in [`method.md` §3](../method.md#3-the-portable-audit-prompt),
in its delta form, with:

```text
TARGET   teemoon-ios  tag tf/1.0.6-58  @ d7ac9639fad0c4c36c7dbb9968ea7b35a2c7468d
PREVIOUS teemoon-ios  tag tf/1.0.5-43  @ 705764b  (== App Store 1.0.5 (43); public v1.0.5 @ 304d6bd, code-identical)
DIFF     git diff 705764b d7ac963 -- teemoon/ Packages/ teemoon.xcodeproj
           (3,986 lines, 58 files; Packages/ and Vendor/ empty)
PLUS     a full read of teemoon/Confidential/ (38 files) against
         COMPARISON-2026-10-19.md (near.ai inference-sdk @ 4bccfd9)
```

plus the nine items of the reviewer brief: every key-bearing request site and
its host, the new session-affinity header and its secret, the new `URLSession.chat`;
the send path's new branches (effort fields, the refusal retry, the stop fix,
keep-reply, the time note, the stall watchdog, the Siri entry, the first-send
probe); the Confidential tree line by line against the comparison and the
`ATTESTATION.md` sentences it called overstated; the residue work at rest and
the kept on-device conversation; the renderer and the developer card; the 18
NEW log rows; the pasteboard; the carried findings; and the disclosures the
page was asked to carry.

---

## Results

### Delta map: `705764b` → `d7ac963`

| Area | Change | Reaches keys? | Reaches plaintext? |
|---|---|---|---|
| `Inference/SessionAffinity.swift` (new, 57), `HTTPTransport.swift:104-106`, `ChatGeneration+Stream.swift:166` | a per-chat routing id — HMAC-SHA256(per-Keychain secret, thread id), 32 hex chars — sent as `x-session-affinity` (Fireworks), `x-grok-conv-id` (xAI), `x-session-id` (OpenRouter) | **a new Keychain item** (`sessionAffinity.secret`, 32 random bytes) that never leaves the Keychain; the id is not a secret | no |
| `Inference/ConfidentialLanguageModel.swift:78-91`, `:131`; `HTTPClient.swift:19` | one app-lifetime `URLSession.chat`: ephemeral, `urlCache = nil`, `.reloadIgnoringLocalCacheData`, 600 s header wait; `URLSessionHTTP` (attestation, key validation, Brave search) moves from `.shared` onto it | **strengthened** — four key-bearing request families leave the default session; the signature fetch stays on `.shared` (zero-capacity cache) | no |
| `Inference/ReasoningEffort.swift` (new, 165), `HTTPTransport.swift:93`, `:149-154`, `:398-400`, `ChatViewModel.swift:343-344`, `ChatView.swift:874-915` | `reasoning_effort` low/high (near.ai, Fireworks, xAI, Ollama), `reasoning.effort` (OpenRouter with `reasoning`), `chat_template_kwargs.enable_thinking` (NVIDIA), `max_tokens 8192` on near.ai Think Harder; a status-400 body naming one of five tokens (`reasoning_effort`, `reasoning effort`, `reasoning.effort`, `chat_template_kwargs`, `enable_thinking`) → one retry without the field, remembered in process memory | no | **new plaintext fields beside the sealed messages on near.ai** (metadata, by protocol); the retry re-seals from plaintext |
| `Inference/ReasoningEffort.swift:150-157`, `Providers/Adapters/OllamaAdapter.swift:39-49` | first send to an unclassified self-hosted endpoint asks `GET {root}/api/version` once per launch, 2 s | **a new egress, no key**, to the user's own server only | no body |
| `Inference/ChatGeneration.swift:308-314`, `:150-157`, `Chat/ReplySupersession.swift` (new), `ChatViewModel.swift:217-219`, `:277-279`, `:360-376` | the model's own stream is iterated so a stop cancels the request; Think Harder keeps the old reply until the new one is saved and filters it out of the request | no | **the replaced reply never reaches the model; a stopped late reply is neither drawn nor saved** |
| `Inference/ChatGeneration+Transcript.swift:19-46`, `:64-79`, `Settings/AppSettings.swift:20-21`, `:214` | `{{date}}`/`{{datetime}}` resolve to the day; each user turn carries `[Sent at h:mm a]` on the wire, never stored | no | a minute-resolution timestamp per user turn goes to the chosen provider |
| `Inference/HTTPTransport.swift:402` | request bodies serialized with `.sortedKeys` | no | the sort is on the plaintext before sealing; no new copy kept |
| `Inference/StreamStallWatchdog.swift` (new), `ProviderWait.swift` (new), `TurnPhases.swift` (new), `HTTPTransport.swift:174-177`, `:224-237`, `GenerationEngine.swift:211-232`, `:350-368` | 600 s header wait, 240 s stream-idle cancel; "waiting for provider" chip; phase timings and cache % on the card; the reply-signature check runs after the turn closes | no | numbers, a provider name, nothing logged with a body |
| `Chat/StoreCompaction.swift` (new, 96), `ThreadDeletion.swift:31-32`, `:41`, `Search/ChatSearchIndex.swift:283`, `:302`, `:399-401`, `:406-410`, `ChatSearchReconciler.swift:60-64`, `ChatSearchService.swift:138-154`, `App/teemoonApp.swift:205-206`, `ChatsListView.swift:426-428`, `ChatsSettingsView.swift:66-68` | a delete is saved at once; the store is `secure_delete`+`VACUUM`ed at the next launch before SwiftData opens it; the FTS index zeroes freed pages, drops deleted terms at delete time, optimizes and truncates its WAL; the launch reconcile purges dropped rows | no | **deleted chat text leaves the store and the index** (the two chat-delete paths; retry and Think Harder deletions are not covered — note) |
| `Inference/LiteRTTransport.swift:155-194`, `:303-312`, `:538-557`, `:812-819`, `LiteRTConversationReuse.swift` (new), `LocalLanguageModel.swift:76`, `:106`, `LiteRTTransport.swift:373-377`, `:622-634`, `:676-727`, `:854-864`, `:896-940` | an on-device turn keeps last turn's LiteRT conversation in memory and sends only the new message; Gemma thinking off by default, on for Think Harder, the thought never shown or kept; an inline `<\|channel>thought…` is held back and stripped | no | **a plaintext heap copy of the transcript lives between on-device turns**; released on background, memory warning, dead engine, chat delete, the next on-device turn; never written |
| `Inference/HTTPTransport.swift:370-377`, `LiteRTTransport.swift:881`, `LastRequestDebugInfo.swift:80-97`, `:149-154`, `RequestDebugView.swift:46-47`, `:129-144` | the on-device card shows the tools JSON; effort, phases, cache % on the card and in the copied text | no | the card prints what it always printed plus numbers and words; copy still redacts credentials, not the routing id |
| `Confidential/` — `TEESignatureVerifier.swift` (+271/−), `NRASService.swift` (+107), `TLSAttestationVerifier.swift` (+24), `DCAPService.swift`, `DCAPVerifier.swift`, `AttestationService.swift:28-44`, `AttestationService+GPU.swift` (−33), `AttestationRecord.swift:128-135`, `ConfidentialSession.swift:333-339`, `ConfidentialSession+Refresh.swift:130`, `:145-151` | signature kinds, prefixes, ed25519 against the quote-bound key, rotation path deleted, gateway never verified; NRAS JWT ES384/issuer/window/nonce; TCB allow-list; DCAP on the TLS probe quote; bounded waits; atomic adoption of a record with its verifiers | **the signature fetch keeps its Bearer key and its gateway host** (`:171-179`); the JWKS GET and NRAS POST carry no key (`:86-94`, `:60-76`, `:133`) | no |
| `App/RequestLLMIntent.swift:105` | Siri records the late signature verdict | no | no |
| `App/ContentView.swift:238-240` | `UITEST_SEED_LOCAL_KIND=ollama` seeds a server kind | inside `#if DEBUG` (`:125-303`) and `--uitesting` (`:213`) | no |
| `Providers/Provider+Presets.swift:92`, `ProviderStore+Healing.swift:319-366`, `ListPriceSnapshot.swift` | NVIDIA default `nemotron-3.5-lightning-30b-a3b`; saved NVIDIA setups on the retired id migrate with a notice; OpenRouter prices 2026-10-22 | no — config only | no |
| `Settings/Appearance.swift:181-190`, `AppearanceSettingsView.swift:66`, `ContentView.swift:381-383`; `Views/Chat/ReplyActionsMenu.swift` (new), `MessageView.swift:191-211`, `:246-262`, `:312`, `SupersededReplyDimming.swift` (new), `GenerationActivityChipView.swift`, `StreamingMessageView.swift`, `TranscriptCollectionView.swift:939-949`, `ConversationView.swift:231-236`, `:420-427`, `:1067-1076` | window tint; a long-press edit menu (think harder, copy) on replies; dimming; chips; a crossfade | no | the copy item writes the reply to the general pasteboard on a tap, as the 1.0.5 context menu did |
| `project.pbxproj` | `MARKETING_VERSION` 1.0.5 → 1.0.6, `CURRENT_PROJECT_VERSION` 43 → 58; nothing else | no | no |
| `Package.resolved`, `Info.plist`, `teemoon.entitlements`, `PrivacyInfo.xcprivacy`, `Vendor/`, `Vendor/textual`, `Packages/` | byte-identical (blob/tree ids `f9bff56`, `0ffa0bd`, `80486f2`, `cc092a8`, `0fa3ad7`, `a39f89a`, `ab23b2a` at both commits) | — | — |

### Traced — keys

**Every key-bearing request site at `d7ac963`, and its host.** Whole-tree
grep `forHTTPHeaderField` over `teemoon/` (29 hits; 19 after dropping
`Content-Type`/`Accept`), then each hit read. The sites that attach a key, and
where each goes:

| Site | Header | Host it reaches | Session |
|---|---|---|---|
| `Inference/HTTPTransport.swift:99-103` | `authHeaderName` or `Authorization: Bearer` | the provider's own base URL + `chat/completions` (`:88`) | `.chat` (`ConfidentialLanguageModel.swift:131`) |
| `Providers/NearAIModelCatalog.swift:282` | Bearer | the near.ai catalogue on the provider's base | as at 1.0.5 |
| `Confidential/AttestationService.swift:66` (built by `makeAttestationRequest`, used at `:174` for the gateway and `+GPU.swift:28` for the direct node) | Bearer | the provider's base (gateway) and the model's direct host from near.ai's directory (`EndpointDirectory.swift`, unchanged: `https://completions.near.ai/endpoints`, hosts under `near.ai`) | `URLSessionHTTP` → **`.chat`** (`HTTPClient.swift:19`) |
| `Confidential/AttestationService+Model.swift:109` | Bearer | the directory's direct host, or a derived `https://<slug>.completions.near.ai/v1` (`:62-69`), and the gateway (`:49-53`) | `.chat` |
| `Confidential/TEESignatureVerifier.swift:173` | Bearer | `ctx.baseURL` + `signature/<id>?model=&signing_algo=` (`:164-170`) — the gateway the chat went to | **`URLSession.shared`** (`:179`), whose cache is zero-capacity (`Support/SharedURLCache.swift:20-23`, unchanged; `teemoonApp.swift:40`) |
| `Providers/ProviderKeyValidator.swift:58`, `:61`, `:66` | Bearer / `X-Subscription-Token` | the endpoint being validated | `.chat` (`:53`) |
| `Inference/BraveWebSearchTool.swift:459`, `:590` | `X-Subscription-Token` | `api.search.brave.com` (`:530`, file unchanged; the DEBUG override still parses to loopback `:535-539`) | `.chat` (`:265`, `:449`) |
| `Providers/Adapters/FireworksAdapter.swift:220` | Bearer | `api.fireworks.ai` | as at 1.0.5 |
| `Providers/EndpointModelCatalog.swift:213-214`, called from `XAIAdapter.swift:51`, `:54`, `OpenRouterAdapter.swift:48`, `:331`, `:387`, `NVIDIAAdapter.swift:52` | Bearer or `authHeaderName` | the provider's own base URL (the adapter is chosen from that host) | as at 1.0.5 |
| the two generic probes `EndpointModelCatalog.swift:169-170`, `Views/Where/HomeServerProbe.swift:149-151` | as configured | the endpoint the user is adding | as at 1.0.5 |

The set is the 1.0.5 page's set: no site added, none removed; two moved
(`TEESignatureVerifier` `:161-164` → `:173`, Brave `:582` → `:590`). The
structural guarantee is unchanged: a key is stored under the endpoint it was
entered for and attached only to requests built from that endpoint. No
`URLQueryItem` carries a key (grep: 24 query items — nonces, `signing_algo`,
`model`, `include_tls_fingerprint`, Brave `q`/counts/budgets, Fireworks
`pageSize`/`filter`/`pageToken`). The keyless requests, for the exits table:
NVIDIA JWKS `GET https://nras.attestation.nvidia.com/.well-known/jwks.json`
(`NRASService.swift:86`, `:91`, `.shared`, cached an hour `:90`) and the NRAS
`POST …/v3/attest/gpu` (`:103`, `:133`; `URLSessionNRASHTTP:60-76` sets
`Content-Type` only; the body is the `nvidia_payload` string the model
attestation served, `AttestationService.swift:139` — GPU evidence, no key, no
message); Intel PCS (`CollateralService.swift:89`, `:145-157`); GitHub
attestations and the compose repo (`ProvenanceService.swift:388`, `:515`);
the audits index (`AuditIndex.swift:26`); the TLS probe (`TLSAttestationVerifier.swift:139-141`,
no credential, no redirects `:253-257`); the Ollama version probe
(`OllamaAdapter.swift:39-49`); the model-weight download session.

**The new header: a per-chat routing id (`SessionAffinity.swift`).** The
value is `HMAC-SHA256(secret, lowercase thread UUID)` cut to 16 bytes, 32 hex
chars (`:33-37`). The secret is 32 random bytes from `SymmetricKey(size:
.bits256)`, stored base64 in the Keychain under the account
`sessionAffinity.secret` (`:23`, `:39-46`) through the same `Keychain.save`
the provider keys use — `kSecAttrAccessibleAfterFirstUnlock`
(`Providers/Keychain.swift:49`, `:61`), no `kSecAttrSynchronizable` (grep 0 in
`Keychain.swift`). It is read back on first use per launch and derived ids are
memoized per thread in memory (`:22`, `:25-31`); if the Keychain refuses, the
id is a random UUID for the launch (`:28`) and nothing is stored. **Which
hosts get it:** `header(for:)` (`:49-55`) returns a header name for exactly
three hosts — `api.fireworks.ai` → `x-session-affinity`, `api.x.ai` →
`x-grok-conv-id`, `openrouter.ai` → `x-session-id` — and `nil` for every
other host, including near.ai, NVIDIA, Brave and any self-hosted server; the
transport sets it only when both an id and a header name exist
(`HTTPTransport.swift:104-106`). The id is computed for every
`ConfidentialLanguageModel` (`ChatGeneration+Stream.swift:166`), so the HMAC
runs for a near.ai turn too, but no header is set. **Is the secret ever
logged, copied, exported?** Grep for `secretAccount`, `sessionAffinity`,
`SessionAffinity` outside the file: nine hits, all `header(for:)` / `id(for:)`
plumbing (`HTTPTransport.swift:39-40`, `:50`, `:59`, `:104-105`;
`ConfidentialLanguageModel.swift:112`, `:122`, `:125`, `:141`;
`GenerationEngine.swift:118`, `:127`; `ChatGeneration+Stream.swift:166`); no
`logger` line names it; the self-verify script embeds attested values only
(`SelfVerifyScript.swift:97-110`); no file writes it. The **id** (not the
secret) does appear in the developer card's header list and its copied text:
`request.allHTTPHeaderFields` is captured at `HTTPTransport.swift:132` into
`TurnReport.requestHeaders`, and `DebugHeaderRedaction.secretHeaders`
(`Views/Chat/DebugHeaderRedaction.swift:36`) masks only `authorization`,
`x-subscription-token`, `x-api-key`, `api-key` on copy — a pseudonymous
per-chat value on a developer's own tap, recorded under Residuals. Pinned by
`SessionAffinityTests`: stable per thread and distinct across threads, the
thread id never visible (`:17-22`); keyed derivation, a different secret gives
a different id (`:25-33`); the header name per host and `nil` for near.ai,
NVIDIA, a LAN host and an unknown cloud host (`:37-45`); and a header-capturing
`URLProtocol` that sees the documented header and no other on each of the
three, and none on NVIDIA (`:47-65`). **Mutation:** add
`case "cloud-api.near.ai": return "x-session-id"` to `SessionAffinity.swift:50-55`
→ `eachProviderGetsItsOwnDocumentedKey` red at `:41-43`.

**The new session.** `URLSession.chat` (`ConfidentialLanguageModel.swift:83-90`)
is `URLSessionConfiguration.ephemeral` with `timeoutIntervalForRequest = 600`,
`urlCache = nil` and `requestCachePolicy = .reloadIgnoringLocalCacheData`: no
disk cache, no in-memory cache, cookies and credentials in memory for the
process only (the app sets none). It replaces the per-generation ephemeral
session of 1.0.5 (`:131`) and, through `URLSessionHTTP`'s new default
(`HTTPClient.swift:19`), now carries the gateway and direct-host attestation
fetches, the key validator and the Brave search and key check — four
key-bearing families that at 1.0.5 rode `URLSession.shared` behind the
zero-capacity shared cache. What still rides `.shared`: the signature fetch
(`TEESignatureVerifier.swift:179`), the JWKS GET, the collateral, provenance,
audit-index and Ollama-probe requests (grep `URLSession.shared`: 3 call sites
in `teemoon/` plus the `.shared` defaults in `NRASService.swift:63`,
`CollateralService.swift:37`, `ProvenanceService.swift:50`,
`OllamaAdapter.swift:39`). The 1.0.3 fix stands:
`SharedURLCache.disable()` is the first statement of `TeemoonApp.init`
(`App/teemoonApp.swift:38-41`, the file's only diff is `:205-206`), and
`Support/SharedURLCache.swift` is unchanged (`git diff --stat`: 0 lines).
Grep `URLSessionConfiguration.|URLSession(configuration|= URLSession(` over
`teemoon/`, `Packages/`, `Vendor/`: six hits — the background download session
(`LocalModelDownloadSession.swift:41`, `:95`), the TLS probe's delegate session
(`TLSAttestationVerifier.swift:92`), `.chat` (`:84`, `:89`), and the vendored
image loader (`Vendor/textual/Sources/Textual/Internal/Image/ImageLoader.swift:20`),
whose tree is byte-identical (below). **Strengthened.**

**The signature fetch (`TEESignatureVerifier.swift:163-200`).** The key is
the near.ai key (`ctx.apiKey`, `TEEContext` from `ConfidentialSession.currentTEEContext()`
`:195-202`), the host is `ctx.baseURL` — the provider's own base, the gateway
the chat was sent to (`ConfidentialLanguageModel.swift:46-47`) — with
`signature/<chat id>` and the two query items `model`, `signing_algo`
(`:164-170`). The 1.0.5 verifier fetched once; this one fetches
`signing_algo=ed25519` first when the model key is attested and refetches as
`ecdsa` when the answer is a gateway signature (`:150-156`) — same host, same
key, at most two more requests per reply. The removed key-rotation path
(`AttestationService+GPU.swift` no longer defines `fetchSigningAddress`; grep
0) took the key to the direct GPU host and the gateway on a mismatch; that
egress is gone. The old debug line that logged the first 200 characters of the
signature body is gone too (now `:181`: attempt, status, algorithm).

**NVIDIA (`NRASService.swift`).** Two hosts, both `nras.attestation.nvidia.com`,
both keyless: the JWKS GET (`:84-96`) and the attest POST (`:60-76`, `:133`).
What the POST carries is the `nvidia_payload` JSON string from the model
attestation (`AttestationService.swift:139` ← `+Model.swift:168`), the GPU
evidence near.ai served; the nonce inside it is checked against the one
teemoon sent (`:119-129`) before any request. Nothing of the user's enters
either request.

**The first-send probe (`ReasoningEffort.swift:150-157`).** Called from
`ChatViewModel.generateResponse` at `:343`, after the missing-key refusal
(`:287-296`), after `prepareTurn` and the settled-gate refusal (`:298-320`)
and after the unsealed-send refusal (`:321-341`), before `llm.generate`
(`:345`). Its guard: not on-device, `provider.isSelfHosted`, no stored server
kind (`ProviderStore+Recents.swift:114`), not yet asked this launch
(`probed[endpoint] == nil`), a parseable base URL. So a cloud host is never
asked (`isSelfHosted` is the 1.0.5 page's `isPrivateHost` rule,
`Providers/Provider.swift:82`, `:114`, file unchanged), and a server the Where
sheet already classified is never asked. The request is
`OllamaAdapter.isOllama(baseURL:timeout: 2)` (`:39-49`): `GET {root}/api/version`
on `URLSession.shared`, no header but the system defaults, no body, every
error swallowed to `false` (`:42-46`). A `true` is recorded through
`store.recordProbe` (the server kind into the config JSON — no key, no
message); a `false` is remembered for the launch only. The Siri path never
calls it (`RequestLLMIntent.swift:106-114` goes straight to `generate`), so an
unclassified server reached through Siri gets no field and no probe
(`ReasoningControl.current` falls back to `resolve(serverKind: nil)` `:126-128`
→ `.none` `:115-116`). Pinned by `ReasoningEffortTests`
`anUnclassifiedServerIsAskedOnceAndAnOllamaAnswerCounts` (`:104-113`) and
`aNoIsRememberedAndACloudHostIsNeverAsked` (`:115-127`, the Fireworks host is
never asked). **Mutation:** drop `provider.isSelfHosted` from the guard at
`:152` → the Fireworks case at `:124-126` asks → red. The cancellation swallow
the hand-off names is real: a stop during the ≤2 s probe makes `isOllama`'s
`try?` return `false` (`OllamaAdapter.swift:42`), which `:155` records as a
"no" for the launch — it fails nothing and sends nothing; the send proceeds
unchanged (`:343` → `:345`). An egress to the user's own configured server,
keyless and bodiless: a residual, not a finding.

**The seeder fence, re-read at the new lines.** `App/ContentView.swift:125`
`#if DEBUG` … `:303` `#endif` (grep); the local-provider seed at `:213-241`
needs `isUITesting` (`:105`, the `--uitesting` argument) and
`UITEST_SEED_LOCAL_ENDPOINT`; the new `UITEST_SEED_LOCAL_KIND` line
(`:238-240`) is inside both and writes `ReasoningControl.seededKinds`, itself
declared under `#if DEBUG` (`ReasoningEffort.swift:159-164`) so a Release
build would not compile a reference to it. `UITestSetupSeed.swift` and
`UITestHostSecrets.swift` are not in the diff (whole-file fences `:41-124`,
`:16-115` as on the 1.0.5 page). `DEBUG` is still defined only by the
project-level Debug configuration (`project.pbxproj:465-466`, `:479`); the
Release configuration (`:485-536`) and both target configurations set no
condition (grep `SWIFT_ACTIVE_COMPILATION_CONDITIONS|DEBUG=1`: two hits).
**Dead in Release.**

**Everything else on the key path** — entry field, the local expiring
pasteboard for key copy (`Views/PlatformChrome.swift:134-147`;
`AddEditProviderModel.swift:546`, `SearchSettingsView.swift:388`), copy-path
redaction on both cards (`DebugHeaderRedaction.swift:69-72`, unconditional;
`RequestDebugView.swift:49-52`, `ErrorMessageView.swift` header map), the
self-verify script reading the key from the environment
(`Confidential/SelfVerifyScript.swift:155`, `:19-20`), `Keychain.deleteAll()`
called only from `#if DEBUG` (`teemoonApp.swift:42-67`, unchanged) — re-read.
**Unchanged.** The catalogue-scope INFO carries (below).

### Traced — prompt and reply text

**One gate, and the new callers.** `ConfidentialSession.sendPolicy`
(`Confidential/ConfidentialSession+Verdict.swift:252-257`) is still the only
derivation (grep `var sendPolicy`: one in the session, one as a field of
`TrustVerdict`). The composer and every retry go through
`ChatViewModel.prepareSend` and then `generateResponse`
(`Chat/ChatViewModel.swift:267-399`), which refuses a keyed provider with no
key (`:287-296`), runs `prepareTurn` (`:298`), refuses on a `.block`, an
unaccepted `.confirm` or a verdict still pending (`:306-320` via
`postPrepareRefusal` `:100-113`), and refuses an attested provider without a
peer (`:321-341`, `mustRefuseUnsealedSend` `:115-117`). Think Harder is a
retry: `ChatView.thinkHarder` (`:880-884`) finds the question and calls
`retry(from:effort: .thinkHarder)` (`:886-899`), the same `prepareSend` and
`presentSend` as a plain retry, carrying the effort through the degraded-send
alert (`pendingRetryEffort`, `:76`, `:895-896`, `:834`, `:861`;
`performRetry` `:901-915`). The Siri
intent still consults the same gate and refuses on a pending verdict
(`App/RequestLLMIntent.swift:70-90`) and on a missing key (`:93-96`); its one
change is recording the late signature verdict (`:105`). **Sealing still
fails closed:** `HTTPTransport.swift:108-122` throws before the wire when
`codec != nil` and the seal throws or returns an unchanged body
(`e2eeSealedBody` `:490-511`); the plaintext path exists only for `codec ==
nil` (`:116`). `E2EESecurityExploitTests` still hold it
(`runTurn_encryptionFailure_throwsAndNothingTouchesTheWire` `:234`,
`unchangedBody_becomesAHardFailure_notAPlaintextSend` `:275`,
`attestedProvider_nilPeer_isRefused` `:304`, `intent_refusesAttestedUnsealed`
`:450`). **Unchanged in gate; two more callers.**

**(a) Effort fields, and what the gateway reads.** `ReasoningEffort.bodyFields(for:)`
(`Inference/ReasoningEffort.swift:25-37`) adds, by `ReasoningControl`
(`:107-117`): `reasoning_effort: "low"|"high"` for a near.ai host
(`Provider.isNearAIHost`), `api.fireworks.ai`, `api.x.ai` and an Ollama server
(`:111-112`, `:115`); on near.ai Think Harder also `max_tokens: 8192` (`:21`,
`:31`); `reasoning: {effort}` on `openrouter.ai` when the model's catalogue
entry lists `reasoning` (`:113`, `:34`); `chat_template_kwargs: {enable_thinking}`
on `integrate.api.nvidia.com` (`:114`, `:35`); nothing for on-device, LM
Studio, llama.cpp, a custom host or Brave (`:108-110`, `:116`, `:36`). The
fields enter the body in `makeBody` after the provider's own extra parameters,
which win on a clash (`HTTPTransport.swift:398-400`). **On near.ai these are
plaintext top-level fields beside the sealed messages**: `E2EEPeer.encryptRequestBody`
(`Confidential/E2EEPeer.swift:114-192`) seals `messages[].content` when it is
a string (`:121-123`), `name` (`:126-128`), `refusal` (`:129-131`),
`tool_calls[].function.name` and `.arguments` (`:133-147`),
`tools[].function.name`, `.description` and the `parameters` schema serialized
whole (`:153-180`), and `tool_choice.function.name` (`:183-189`); everything
else — `model`, `stream`, `stream_options`, the provider's extras,
`reasoning_effort`, `max_tokens`, `reasoning`, `chat_template_kwargs`, a tool
message's `tool_call_id`, the role sequence, the count and lengths of the
ciphertexts — passes through (`:191`). A non-string `content` (an array) would
pass in the clear, but none is reachable: `WireMessage.content` is a `String`
(`ConfidentialLanguageModel.swift:21-24`) and the tool-round follow-ups are
strings (`GenerationEngine.swift:650-676`); `reasoning_content`, `audio` and
`function_call` are never put in a request by this client. The gateway therefore
reads the model id, the sampling parameters including the new effort level and
cap, and the shape of the conversation — metadata by protocol, which
teemoon.ai/privacy ("Last updated October 19, 2026"; fetched by the
orchestrator 2026-10-22, not by this review) states as "Your message text is
then encrypted to that enclave; the model name and request settings are not,
so near.ai can route the request.", and which `ATTESTATION.md:140-143` states
generically. It
goes in the exits table as a disclosure, not a sink. Pinned by
`ReasoningEffortTests` (`fireworksNearAndXAIUseReasoningEffort` `:29-36`,
`openRouterNestsItWhereTheModelSaysItReasons` `:39-48`,
`unverifiedServersAreLeftAloneAndOfferNoThinkHarder` `:77-88`,
`ollamaGetsEffortWithoutACap` `:91-101`, `nvidiaSwitchesThinkingOffThenOn`
`:130-137`, `onlyNearAICapsThinkHarder` `:140-146`,
`everyRoundOfASearchTurnSendsTheTurnsLevel` `:52-73`). **Mutation:** return
`.effort(cap: nil)` for an unknown host at `ReasoningEffort.swift:116` →
`unverifiedServersAreLeftAloneAndOfferNoThinkHarder` red.

**The refusal retry.** `HTTPTransport.runTurn` remembers whether it sent an
effort field (`:93`); on a status ≥ 400 it drains the error body (`:147-148`)
and, when `ReasoningEffort.isRefusal` (`:77-83`: status 400 **and** the
lowercased body contains `reasoning_effort`, `reasoning effort`,
`reasoning.effort`, `chat_template_kwargs` or `enable_thinking` — two names
more than the brief listed, both NVIDIA's) says yes, records the refusal
(`noteRefused` `:85-87`, a `LockedBox<Set<String>>` in process memory `:70`
keyed `host|model` `:72-74`) and calls `runTurn` again (`:149-154`). The
recursion rebuilds the plaintext body from the same `messages` (`:92` →
`makeBody` `:379-403`, now without the field because `bodyFields` returns
`nil` for a refused key `:26`), creates a new `E2EEStreamCodec` around the
**same** `teeContext.e2eePeer` (`:89`) and seals again (`:117-121`): every
sealed field gets a fresh ephemeral X25519 key (`E2EEEnvelope.seal`
`E2EEPeer.swift:227-237`, `:228`) while the client identity in the headers —
the peer's signing key, created once per `TEEContext` derivation
(`E2EEPeer.swift:44-51`, `:68-77`; `ConfidentialLanguageModel.swift:52-61`)
— is the same. So: **rebuilt and re-sealed from plaintext, fresh per-field
envelopes, the same session client key.** Nothing from the 400 body is kept:
it is matched and dropped (`:149`), reaching the `ErrorDrainer` only on the
non-retry path (`:155`); the only thing remembered is the `host|model` key.
A second refusal cannot loop: `sentEffort` is `false` on the retry. Pinned by
`aModelThatRefusesIsAskedAgainWithoutItAndRemembered` (`:206-222`: two
bodies, the second without the field, the next turn one body, another model
on the host unaffected), `onlyA400NamingTheParameterIsARefusal` (`:197-204`)
and `anE2EERetryIsSealedAfresh` (`:225-253`: two sealed bodies, the two
ciphertexts differ, neither contains the plaintext, the retry has no field).
**Mutations:** replace the recursive `runTurn` at `:152-153` with a resend of
`bodyToSend` → `anE2EERetryIsSealedAfresh` red (`first == retry`); widen
`isRefusal` to any 400 at `:78-82` → `onlyA400NamingTheParameterIsARefusal`
red.

**(b) `.sortedKeys` (`HTTPTransport.swift:402`).** The sort is applied by
`JSONSerialization` to the plaintext dictionary in `makeBody`, before
`e2eeSealedBody` runs on its bytes (`:92` then `:117-121`), and only object
keys sort — arrays (`messages`, `tools`, `tool_calls`, content parts) keep
their order. The E2EE peer re-serializes the sealed dictionary without the
option (`E2EEPeer.swift:191`), so the wire body of a sealed request is not
sorted; the gateway signs the bytes it received and the verifier offers both
the wire bytes and the plaintext as candidates (`TEESignatureVerifier.swift:34-41`).
No new copy of the plaintext exists because of the sort: the card's
`requestBodyJSON` is the pretty-printed plaintext it always was (`:133`, now
in sorted order), no log line carries it (below), and `TurnReport` is in
memory. Pinned by `PromptCachePrefixTests`: three runs serialize to one byte
string that equals its own sorted re-serialization (`:20-41`); a six-message
body with array content, two tool calls and two tool results keeps every
array in order (`:44-77`); sealing the sorted plaintext yields one ciphertext
string per content and a sealed schema string, with no plaintext in the wire
body (`:81-105`). **Mutation:** drop `options: .sortedKeys` at `:402` →
`aRequestBodyIsTheSameBytesEveryTime` red at `:39-40`.

**(c) The stop fix (`cf85750`).** `ChatGeneration.generate` now iterates
`model.streamResponse(within: session, to: Prompt(...), …)` (`:312-314`)
instead of the session's relay, on a consumer task (`:317-345`) that
`stop()` cancels directly (`:150-157`), under `withTaskCancellationHandler`
(`:350-354`); cancelling the consumer tears down the engine's stream and the
transport's `URLSession` task. The E2EE seal and the attestation gate are
unchanged on this path: the prompt reaches `HTTPTransport.runTurn` through
the same `GenerationEngine` (`ConfidentialLanguageModel.swift:136-142`), and
the gate ran before `generate` was called (`ChatViewModel.swift:298-341`). A
late reply after a stop is neither drawn nor saved: the consumer breaks on
`cancelled` (`:320`), the view-model saves only when `lastError == nil` and
the output is non-empty, and a cancelled Think Harder restores (`:360-365`).
Pinned by `ThinkHarderKeepReplyTests.aStoppedThinkHarderCancelsTheRequestAndDrawsNoLateReply`
(`:151-163`: the held transport sees the cancel, writes nothing late, the
output is empty, the old reply stands) and
`aStoppedPlainSendCancelsTheRequestAndSavesNothing` (`:165-180`). The 1.0.5
behaviour — an abandoned cloud request running to completion and billed — is
disclosed below. **Mutation:** revert `:312-314` to
`session.streamResponse(to: lastMessage.content + timeNote)` → both tests red
(`sawCancel` false, `lateWrites == 1`).

**(d) Keep-reply (`ReplySupersession`).** On a Think Harder, `ChatViewModel.retry`
does not delete the old reply; it records the ids after the question in
`llm.superseding` (`:217-219`). `generate` builds its history from
`superseding.history(thread.sortedMessages)` (`ChatGeneration.swift:241`;
`ReplySupersession.swift:29-32` filters the superseded ids whenever a
supersession is active), so **the model never receives the reply it is
replacing**; when no Think Harder is in flight the history is unfiltered
(`:31`). The outcome is decided after `generate` (`ChatViewModel.swift:360-376`):
`.replace` deletes the old reply in the same context that then saves the new
one (`:366-373`, `ChatSearchService.didDelete` first `:368`); `.restore` on a
failure, a stop or an empty output keeps it and clears the interruption so no
re-ask at default effort follows (`:361-365`; `ReplySupersession.outcome`
`:48-54`); the in-memory state is cleared on every exit after the save
(`:277-279`). The transcript hides the old reply only once the new one has
text (`:22-27`, `:35-38`; `ChatView.swift:232`). Pinned by
`ThinkHarderKeepReplyTests.aNewReplyReplacesTheOldOneInOneSave` (`:91-102`,
the wire never contains `OLD ANSWER`), `aFailureKeepsTheOldReply` (`:104-112`),
`aStopKeepsTheOldReply` (`:114-122`), `anInterruptionKeepsTheOldReplyAndIsNotReasked`
(`:125-131`), `theTranscriptDropsTheOldReplyAtTheFirstText` (`:133-147`).
**Mutation:** make `history(_:)` return `messages` unfiltered at
`ReplySupersession.swift:31` → `aNewReplyReplacesTheOldOneInOneSave` red at
`:100-101`.

**(e) The time note.** `resolvePromptTemplates` (`ChatGeneration+Transcript.swift:64-68`)
replaces `{{date}}` and `{{datetime}}` with the day only (`dateFormatter`
`:48-52`, `"EEEE, MMMM d, yyyy"`); the minute goes on each user turn as
`"\n\n[Sent at h:mm a]"` (`timeNote(sentAt:)` `:77-79`), appended on the wire
only when the persona asks for the date (`wantsTimeNotes` `:71-73`,
`ChatGeneration.swift:281-282`) — to prior user turns from their stored
timestamps (`:37-38`) and to the live prompt from the message's timestamp, or
"now" on a Think Harder (`ChatGeneration.swift:308-309`). It is never stored:
`Message.content` is written from the prompt and the reply as before
(`ChatViewModel.swift:166`, `:385-389`); the note is built at send time.
The kept on-device conversation holds it in memory with the rest of the
transcript (below). The default persona now reads `Today's date is {{date}}.`
(`AppSettings.swift:21`) and the migration table knows the old default
(`:214`). What the chosen provider learns: the day in the system prompt and
the minute each message was sent — timestamps the provider already had from
the request itself; a disclosure. Pinned by `PromptPrefixStabilityTests`
(`:28-34`, `:43-49`, `:53-66`).

**(f) The stall watchdog and `ProviderWait`.** `StreamStallWatchdog`
(`:14-54`) holds a `Date` and a flag; on a stall it calls
`dataTask.cancel()` (`HTTPTransport.swift:174-177`) and the loop rethrows
`URLError(.timedOut)` (`:236-237`, `:272-273`). What is logged on a stall:
`ChatGeneration.swift:367` or `:372` logs the `LLMError.userMessage` or the
`URLError` description — fixed sentences and a URL whose host is the
provider's; no body, no key (the key is a header). Nothing is retried on a
stall. `ProviderWait` (`:12-29`) is a turn index, a `Date` and the provider's
display name, rendered as `waiting for <name>... Ns` (`:27-29`) on the chip
(`StreamingMessageView.swift:71-87`); not logged. `TurnPhases` (`:15-141`) is
offsets, token counts and a cache percentage; `LastRequestDebugInfo.phases`
(`:81`) is in memory for the card and its copy (`RequestDebugView.swift:46-47`).
**Numbers and a name; no sink.** Pinned by `StreamStallTests` (`:18-29`,
`:31-38`, `:40-53`) and `ProviderWaitTests`.

**(g) The Siri entry.** `RequestLLMIntent.swift:106-114` calls `llm.generate`
without an `effort`, so the default `.chatDefault` (`ChatGeneration.swift:200-204`)
applies: a Siri turn to near.ai, Fireworks, xAI or Ollama also carries
`reasoning_effort: "low"`, and a Siri turn to the three affinity hosts carries
a routing id for its detached thread (a fresh UUID per intent, so a fresh id
per Siri turn, never linking two). The probe is not reached from Siri
(above). Gate unchanged (`:70-96`).

**(h) The first-send probe** — traced under keys; no body, no key, to the
user's own server, once per launch.

**The kept on-device conversation (`LiteRTTransport.swift`).** After a
completed, tool-free, non-thinking turn, the transport keeps the
`LiteRTLM.Conversation` object and a `KeptConversationState` — the system
message, the tool names and the transcript turn for turn, as plain `String`s
(`LiteRTConversationReuse.swift:25-30`; `afterTurn` `:42-51`) — in
`EngineCache.kept` (`LiteRTTransport.swift:155-163`, `:172`, stored at
`:812-819`). The next on-device turn takes it (`takeKept` `:166-170`, which
forgets it whether or not it is reused) and reuses the native conversation
only on exact equality with what it would seed (`canReuse` `:35-39`;
`:552-555`): same persona, same tools, same history including each turn's time
note. So between two on-device turns a plaintext copy of the transcript lives
in the heap twice — in the kept state and in the native KV cache. **Released**
on background and on a memory warning (`LocalRuntime.swift:244-258` →
`evictEngines` `:303-305` → `evictAll` `:176-182`, `kept.removeAll()` first;
started from `teemoonApp.swift:587`), on a dead engine (`:784` → `discard`
`:190-194`), on a chat delete and on delete-all (`forgetKeptConversations`
`:310-312`, called from `ChatsListView.swift:427` and `ChatsSettingsView.swift:67`
— the only two callers, grep), on the next on-device turn (`:552`), and at
process exit. **Not released** on a thread switch or a switch to a cloud
provider: nothing calls `dropKept` there (grep: three callers, listed), so the
last on-device thread's transcript stays in memory until one of the events
above. Nor on a plain retry (`ChatViewModel.swift:220-232`) or a Think Harder
replace (`:366-373`): neither calls `forgetKeptConversations()`, so the
dropped reply's plaintext stays in `Kept` (heap copy + native KV) until the
next on-device turn takes the entry (`:166-170`, removed regardless; rebuilt,
since the transcript differs — `everyMismatchRebuilds` `:33-41`) or until
background, memory warning, a dead engine or exit — memory only, the same
carve-out as the deletion ruling. **Never written:** `Kept` is a class in an actor's dictionary; the only
path the engine is given is `cacheDir: FileManager.default.temporaryDirectory.path`
(`:254`), for the runtime's own weight and program caches — what the native
engine writes there is a property of the binary (Not traced). A thinking turn
is never kept and never reuses a kept conversation (`:35-39`, `:46-50`;
`aThinkingTurnIsNeverKept` `:58-62`, `aConversationIsNotReusedAcrossThinkingModes`
`:64-69`); a tool turn and an unfinished turn are not kept
(`notKeptAfterAToolOrAnUnfinishedTurn` `:48-55`); a stopped, abandoned or dead
turn is not kept (`:812`). Pinned by `LiteRTConversationReuseTests`
(`:28-31`, `:33-41`, `:43-46`, `:109-112`). **Mutation:** drop `!thinking`
from `afterTurn`'s guard at `LiteRTConversationReuse.swift:46` →
`aThinkingTurnIsNeverKept` red. A residual, stated below.

**Gemma thinking (`a6ce6e8`).** `LocalLanguageModel.defaultEnableThinking` is
`false` (`:76`); Think Harder passes `enableThinking: effort == .thinkHarder`
(`ChatGeneration+Stream.swift:160`) into `LiteRTTransport(thinking:)`
(`LocalLanguageModel.swift:106`; `LiteRTTransport.swift:556`, the
`ThinkingConfig` of a newly created conversation `:588-599`). The consumer
keeps only `.text` contents of each chunk (`:679-682`), so a thought LiteRT
delivers on its own channel never enters `answer`; a thought delivered inline
as `<|channel>thought…<channel|>` is held back while it streams by
`InlineThoughtFilter` (`:896-940`; used at `:676`, `:688`, `:727`) so it never
reaches a partial, and stripped from the final text before parsing
(`strippingInlineThought` `:377`, applied `:854`), so it reaches neither
`Message.content` nor the card's response (`TurnOutput.content` `:856`) nor a
log (no `logger`/`DiagLog` line in the file interpolates `answer` or a piece;
the stopped-turn line logs `answer.count` `:801`). A thought cut off by the
cap leaves no reply and nothing for the reasoning-only fallback to promote
(`:377-379`, test `:79-82`). The cap grows by 2048 tokens for a thinking turn
(`:373`, `:622`); hitting it marks the turn truncated (`:634`, `:693`,
`:864`). The card's headers gain `conversation: reused|rebuilt` and
`thinking: on|off` (`:878-879`) — two words. Pinned by the sentinel tests
`anInlineThoughtIsStrippedFromTheReply` (`:73-83`) and
`anInlineThoughtNeverReachesAPartial` (`:86-107`, every chunk size 1…12).
**Mutation:** make `InlineThoughtFilter.append` (`:901-918`) return `text`
unchanged → `anInlineThoughtNeverReachesAPartial` red at every size. What a
unit test cannot pin: that the runtime really delivers a thought as non-text
content when `ThinkingConfig` is on — a property of the LiteRT binary (Not
traced; the hand-off's device gate is still pending). The **reasoning-only
fallback** of 1.0.5 is unchanged: a complete reply that is only reasoning is
saved as the reply text — existing behaviour, disclosed below.

**The renderer.** `Vendor/textual` is byte-identical: `git rev-parse
705764b:Vendor/textual d7ac963:Vendor/textual` → `a39f89a59558dcfa2d3d5c43453b0122dc17f078`
twice (and `Vendor` → `0fa3ad7…` twice), so the patch-7 selection gate the
hand-offs describe adding at build 56 and removing at 57 leaves no trace at
58. `blockingRemoteTranscriptAttachments()` is still installed at both SwiftUI
roots (`ConversationView.swift:141`, `:826`), the parse-level image strip is
unconditional (`MarkdownParseCache.swift:70-71`, file unchanged), and the
developer card is still hosted as the tail card
(`ConversationView.swift:521-526`, `:987`; `TranscriptCollectionView.swift:1250`),
which renders no markdown. The new reply menu (`ReplyActionsMenu.swift`) is
a `UIEditMenuInteraction` with a long-press recognizer on the cell
(`:48-72`); its two items are Think Harder and copy (`MessageView.swift:246-262`);
no network, no new render surface. The on-device card's new **tools**
display is `HTTPTransport.wireTools` (`:370-377`) pretty-printed into the
card's `requestBodyJSON` (`LiteRTTransport.swift:881`, `prettyRequest`
`:420-427`) — the same JSON the cloud request carries, display only:
`LastRequestDebugInfo` is not persisted (`Message` has `role`, `content`,
`timestamp`, `generatingTime`, `sourcesJSON` — `Chat/ChatModels.swift:20-24`,
no debug field), and the card's copy still redacts credentials
(`RequestDebugView.swift:49-52` → `DebugHeaderRedaction.copyHeaderBlock`).
Pinned by `OnDeviceCardToolsTests` (`:19-45`, `:53-59`). **Unchanged in
reach.**

**Logs on the reply path — the 18 NEW `log` rows, each read.**

| Row | Interpolations | Body text? |
|---|---|---|
| `ChatViewModel.swift:308` | the refusal sentence (`:104-110`, fixed), `.public` | no |
| `StoreCompaction.swift:34-35` | an `Outcome` case name and seconds, `.public` | no |
| `ConfidentialSession+Refresh.swift:129` | model id, 4 hex of the gateway nonce, compose path, `.public` | no |
| `ConfidentialSession+Refresh.swift:132` | `\(error)` — the `NSError` thrown at `AttestationService.swift:116-117` (a fixed sentence), a `URLError`, or a cancellation; the key is a header, never in a URL or an error; default privacy | no |
| `NRASService.swift:186` | fixed string | no |
| `TEESignatureVerifier.swift:181` | attempt, status, algorithm | no (the 1.0.5 line's `body.prefix(200)` is gone) |
| `TEESignatureVerifier.swift:198` | fixed string | no |
| `TEESignatureVerifier.swift:214` | a `SignedText.mismatch` reason (`:288-292`, fixed sentences), `.public` | no |
| `TLSAttestationVerifier.swift:112`, `:115` | a `TLSAttestation.failed` reason (`:165-198`, `:126-127`, fixed sentences), `.public` | no |
| `GenerationEngine.swift:397`, `:399`, `:401`, `:403` | signing addresses, an expected/got pair (addresses or the fixed strings of `:210-258`), `.public` | no |
| `GenerationEngine.swift:409` | `\(err)` — a `URLError`/`DecodingError` from the signature fetch | no |
| `LiteRTTransport.swift:179`, `:851` | counts, `.public` | no |
| `ChatsSettingsView.swift:70` | a SwiftData error from `delete(model:)` | no |

The 1.0.4 LOW stays **CLOSED** at the new lines: `ChatGeneration.swift:392`
logs `snapshotCount` and `self.output.count`; `GenerationEngine.swift:331`
the fragment count and summed length; `:440` `tc.arguments.count`. Whole-tree
grep over the 177 `logger.*` lines in `teemoon/` (and `Packages/`) for an
interpolation naming `output|content|answer|body|prompt|message|reply|args|arguments|text|systemPrompt|apiKey|key|token|secret|affinity|raw|snippet|query`:
five hits, none a body — `LiveCatalogStore.swift:274` (an endpoint string),
`ChatSearchIndex.swift:699` (SQLite's error message, `.public`; its statements
bind values `:690-692`), `Keychain.swift:84` (the account name, `.private`),
`SSEParser.swift:304` (`key` is the JSON field name), `ChatGeneration.swift:392`
(a count). `LogPrivacyTests.noLoggerInterpolatesUserOrModelTextAtAnyPrivacyLevel`
(`:28-51`) still rejects eight content-bearing names at any mark. The 29
`DiagLog.note` lines (`LocalRuntime.swift:220-226`, stderr only under
`TEEMOON_NATIVE_LOG=1`) were listed and read: reasons, counts, model ids,
file names, percentages, a `reused (N turns cached)|seeded` word
(`LiteRTTransport.swift:557`) — no body. No bare `print(` in Swift (the only
hits are inside the generated Python of `SelfVerifyScript.swift`).

**Pasteboard — every write, from a whole-tree grep (`UIPasteboard|NSPasteboard|copySensitive`, 31 hits).**
General-pasteboard writes on iOS: `CodeBlock.swift:81` (a code block, tap),
`ModelDetailView.swift:78` and `ChatView.swift:160` (a model id, tap),
`ErrorMessageView.swift:187` and `RequestDebugView.swift:220` (the debug
dumps, tap, credentials redacted), `MessageView.swift:255` (the reply, from
the new menu's copy item — the same text the 1.0.5 context menu copied, user
tap on visible content) and `:358` (a user message, tap). Secrets go through
`Clipboard.copySensitive` only (`PlatformChrome.swift:134-147`;
`AddEditProviderModel.swift:546`, `SearchSettingsView.swift:388`). One read:
`WebSearchOffer.swift:143` reads the pasteboard when the user taps paste on
the key offer. The `NSPasteboard` lines (`MessageView.swift:257-258`, `:360-361`
and the macOS branches elsewhere) are not a product. **No new write; none on
render, none on error.**

### Traced — `teemoon/Confidential/` in full, against the SDK comparison

All 38 files read (9,666 lines). For the two questions, the tree's network
behaviour is: four key-bearing requests to near.ai hosts (the gateway and the
direct-host attestation reports, the model attestation race, the signature
fetch — all listed under keys), and keyless requests to NVIDIA, Intel PCS,
GitHub and the audits index. No file writes message text; the two files that
persist anything write to `UserDefaults` — the verified-digest cache
(`ProvenanceService.swift:560-587`: repo, identity, ref, commit, a flag per
digest) and the audits index snapshot with its ETag (`AuditIndex.swift:153-155`,
`:230-233`). Every `previewForLog` of a server body is `.private` and bounded
to 2 KB (`Data+LogPreview.swift:18`, `:29-44`). The self-verify script embeds
attested values and reads the key from the environment (`SelfVerifyScript.swift:97-110`,
`:155`; control characters escaped `:48-64`). Nothing here copies plaintext
anywhere. What follows is the brief's line-by-line answer to the comparison —
the attestation surface, which is outside this audit's axis unless the code
sends plaintext where the doc says it does not. It does not.

**Signatures (bugs), at `d7ac963`.**

| Comparison line | Status | Where | Test that pins it | Mutation that makes it red |
|---|---|---|---|---|
| `signature_kind` ignored; no `signing_algo` sent | **FIXED** | `TEESignatureVerifier.swift:81-85` decodes the kind (absent → `provider_tee`, as the SDK); `:168-169` sends `model` and `signing_algo`; `:150-156` asks ed25519 first when the model key is attested and refetches ecdsa for a gateway answer; `evaluate` branches on the kind `:241-261` | `SignatureVerdictTests.gatewayKindOverModelTextIsRejected` (`:147-152`), `unknownSignatureKindIsRejected` (`:173-178`), `gatewaySignatureIsGatewayTrustOnly` (`:182-188`); `ConformanceSignatureTests.vectorsReproduceUnderProduction` (14 cases, exactly 2 verified and 1 gateway-trust, `:149-156`) | make `.gateway` return `.verified` at `:252-258` → `gatewaySignerIsNeverVerifiedEvenAsAModelKey` (`:191-197`) red |
| text accepted with or without the model prefix | **FIXED** | `SignedText.expected` builds the exact text per kind (`:269-282`: `model:req:resp` for `provider_tee`, `req:resp` for `gateway`, matching the SDK's `core/chat.py:53-58`) and `mismatch` compares whole (`:285-293`; a bound text with the wrong prefix is "wrong prefix") | `modelSignatureWithoutPrefixIsRejected` (`:138-145`), `gatewaySignatureWithModelPrefixIsRejected` (`:207-212`) | return `nil` when `binding.isBound` at `:290` → `modelSignatureWithoutPrefixIsRejected` red |
| non-ECDSA: the server-asserted address trusted | **FIXED** | `:225-235`: ed25519 is `.verified` only for `provider_tee`, a 32-byte attested model key bound to the model quote (`e2eeKeyBoundToModelTEE == true` — which, like `gpuSigningKeyBoundToHardware` in the `provider_tee` branch, never reads the quote's own `isVerified`: the new INFO under Findings), an asserted address equal to that key, and a valid `Ed25519Signature` over the text (`:300-307`); any other algorithm is rejected (`:236-239`) | `modelEd25519ByBoundKeyIsVerifiedAndUnboundIsNot` (`:233-252`, incl. a zero signature on the asserted key), `gatewayEd25519IsRejected` (`:224-231`), `realEd25519SignatureChecksAgainstItsKey` (`:216-221`), `unknownAlgorithmOnATrustedAddressIsRejected` (`:164-171`) | drop `Ed25519Signature.isValid(...)` from the guard at `:231` → the forged case at `:247-251` verifies → red |
| `fetchSigningAddress` rotation path returns `.verified` unverified | **REMOVED** | `AttestationService+GPU.swift` now holds only `fetchGPUData` (`:16-105`); grep `fetchSigningAddress` → 0; `evaluate` has no refetch (`:206-262`) | `signerOutsideTheAttestationIsAMismatch` (`:156-162`) | in the `.providerTEE` branch return `.verified` when `att.quoteVerification?.isVerified == true` → red |
| a gateway signer counts as model-verified | **FIXED** | `:252-258` → `.unverified(.gatewayTrustOnly)` at most, and only when the signer is the quote-bound gateway address (`signingKeyBoundToHardware`, `AttestationRecord.swift:118-126`) of a verified gateway quote; counted apart (`ConfidentialSession.swift:308-316`) | `gatewaySignerIsNeverVerifiedEvenAsAModelKey` (`:191-197`), `gatewaySignatureByUnboundKeyIsAMismatch` (`:199-205`) | as row 1 |
| (new) a model signer not bound to its quote | **ADDED** | `.signerUnattested` (`:120`, `:247-249`) when the GPU report's address is not in the GPU quote's `report_data` (`gpuSigningKeyBoundToHardware`, `AttestationRecord.swift:128-135`) | `modelSignatureByUnboundKeyIsNotVerified` (`:121-127`) | delete the `att.gpuSigningKeyBoundToHardware == true` clause at `:244` → red |

**Where teemoon is weaker, at `d7ac963`.**

| Comparison line | Status | Where |
|---|---|---|
| checks in flight (`nil`/`.verifying`) do not block the send | **REFUTED at the gate**, confirmed at the state level | `attestationState` reads a `nil` DCAP/GPU/TLS verdict as neutral (`ConfidentialSession+Verdict.swift:71`, `:79`, `:84`), but `prepareTurn` waits up to 15 s for the key (`ConfidentialSession.swift:210`) and up to 15 s for the verifiers to settle (`:215`, `:224`, `settleVerifiers` `:256-261`), and `postPrepareRefusal` refuses while `verdictsPending` (`ChatViewModel.swift:108-110`; `verdictsPending` `:246-253` is true for any launched hard-block verifier without an answer); Siri refuses the same way (`RequestLLMIntent.swift:87-90`); a record is adopted with its verifiers launched in one synchronous call (`adopt` `ConfidentialSession+Refresh.swift:145-151`), so no window exists between a record and its pending flags; `awaitValue` is bounded by a continuation and a sleep task, never a task group that waits for the slow child (`AttestationService.swift:28-44`); `e2eeKey`/`attestationOutcome` poll instead of awaiting the fetch task (`ConfidentialSession.swift:333-339`, `:344-350`). Pinned by `SendPrepTests.postPrepareRefusalHonoursTheSettledGate` (`:89-96`, pending → refusal at `:94-95`), `E2EESecurityExploitTests.intent_refusesOnBlock_andOnConfirm` (`:443`), `AttestationLegIndependenceTests` (the model leg's bounded wait, `:247-296`). **Mutation:** remove the `if verdictsPending` branch at `ChatViewModel.swift:108-110` → `SendPrepTests` `:94` red. After the 15 s timeout a still-pending verdict is a refusal, not a send. |
| NRAS JWT decoded without verifying its signature | **FIXED** | `NRASService.swift:155-190`: ES384 only (`:164`), `kid` required (`:165`), `iss == https://nras.attestation.nvidia.com` (`:166`, `:104`), `eat_nonce == our nonce` (`:167-169`), `nbf`/`exp`/`iat` with 120 s leeway (`:170-174`, `:106`), the key looked up in the JWKS and refetched once on an unknown `kid` (`:176-182`; `LiveNRASKeys` `:84-96`, cached an hour), unknown key or unreachable keys → `.inconclusive` (soft) (`:179`, `:183`), bad signature → `.failed` (hard) (`:184-188`); the verdict claim is read only after the token checks (`:142-143`). Matches the SDK's `utils/nvidia.py:147-170`. Pinned by `NRASServiceTests`: `mintedToken_verifies` (`:202-206`), `tokenForAnotherNonce_failsHard` (`:208-213`), `tokenFromAnotherIssuer_failsHard` (`:215-220`), `nonES384Token_failsHard` (`:222-227`), `realToken_expiredAnHourLater` (`:229-234`), `realToken_unknownKeyIsInconclusive` (`:236-241`), `realToken_keysUnreachableIsInconclusive` (`:243-249`), `failVerdict_rejected` (now fails on the signature, `:140-166`). **Mutation:** drop the `nonce.lowercased() == nonceHex.lowercased()` clause at `:167` → `tokenForAnotherNonce_failsHard` red. |
| every TCB status but Revoked passes | **FIXED** | `DCAPTcbStatus.isAccepted` = `upToDate || outOfDate` (`DCAPVerifier.swift:44`; the mapping `:46-54` sends `OutOfDateConfigurationNeeded` to `configurationNeeded`); `isHardFailure` = `!tcb.isAccepted` (`DCAPService.swift:75-80`); the reason names the status (`:59-70`). The SDK's default is the same pair (`core/dstack_attestation.py:34`). Pinned by `TcbAllowListTests` (`:22-26` accepted, `:28-35` seven rejected statuses, `:37-41` the live statuses). **Mutation:** `isAccepted` → `self != .revoked` → `rejected("ConfigurationNeeded")` red. |
| no debug-bit check | **UNCONFIRMED** | `DCAPVerifier.verify` calls `DcapQvl.verify(rawQuote:collateralJson:nowSecs:)` with no policy argument (`:87-88`); the Swift package `dcap-qvl-swift` 0.5.2 @ `80a8a56` (`Package.resolved:14-20`) is a UniFFI binding (`Sources/DcapQvl/DcapQvl.swift`, 1,788 lines, read from the SwiftPM repository cache on this Mac) over the prebuilt `DcapQvlFFI.xcframework` binary; the binding exposes no debug or allow option (grep `debug|allow`: 0) and no Swift line in `Confidential/` checks `TD attributes`. The SDK rejects `quote.debug_enabled` itself (`core/dstack_attestation.py:78-79`). Whether the Rust core refuses a debug TD by default is a property of the binary — Not traced. The developer's own table says "likely refuted … not run against a debug quote"; this review cannot improve on that. |
| only `.first` of the model reports verified | **STILL OPEN** | `AttestationService+Reports.swift:225-232` resolve key, quote, payload and OS hash from the top level or `.first` of `all_attestations`/`model_attestations`; `fetchModelAttestation` verifies that one (`+Model.swift:124-170`). |
| model compose / `os_image_hash` from unauthenticated JSON | **STILL OPEN, now disclosed** | `AttestationService+GPU.swift:86-100` reads compose hash, manifest, file hash, path, commit, tag and timestamps from the report JSON; `modelOSImageHash` from the model report (`AttestationService.swift:132` ← `+Reports.swift:232`); the only `mr_config` binding is the gateway's (`AttestationRecord.codeIdentityVerified` `:165-174`); the GPU and model quotes are DCAP- and nonce-checked (`DCAPService.swift:99-104`, `AttestationRecord.swift:183-197`) but their measurements bind nothing. `ATTESTATION.md:67-73` and `:98-103` now say exactly this (below). |
| E2EE: only string content sealed; `reasoning_content`, audio, `function_call` unsealed; no `x-no-aliasing` | **STILL OPEN as a wire-coverage gap; not reachable today** | coverage at `E2EEPeer.swift:114-192` as traced above; the client never sends an array content or those fields; `x-no-aliasing` is nowhere in the app (grep `no-aliasing|ohttp` over `teemoon/`: display strings only), while the SDK sends it (`core/e2ee_request.py:70`). On the response side the stream decrypts `content` and `reasoning_content` (`SSEParser.swift:297-306`); a `reasoning_content` that fails to decrypt is passed through as ciphertext into the reasoning block rather than failing the stream (`:304-305`) — a display/claim note, not a plaintext sink. |
| TLS probe: wrong host, quote only parsed | **HALF FIXED, disclosed** | the probe quote is now DCAP-verified like the record's quotes (`TLSAttestationVerifier.swift:66-71`, `:113-116`, `withQuoteCheck` `:122-129`: a hard DCAP failure or a TCB outside the allow-list fails the check); the host is still the model's direct host from the directory (`ConfidentialSession+Verifiers.swift:180-187`), not the gateway the chat uses; still credential-free (`:139-141`; `probeRequest_carriesNoAuthorizationHeader` `:48-55`) and redirect-free (`:253-257`). Pinned by `dcapFailureFailsAVerifiedBinding` (`:117-124`). **Mutation:** `guard dcap.isHardFailure else { return .verified }` → `return .verified` unconditionally at `:124` → red. `ATTESTATION.md:152-157` now says the host is the direct host and chat is not covered. |
| OHTTP missing | **STILL OPEN** | no OHTTP client in the tree (grep above). Not a sink. |
| endpoints: direct host preferred for model attestation; no `provider=near`, no `include_tls_fingerprint` on the main fetch | **STILL OPEN** | `+Model.swift:40-54` races the direct sources first; `makeAttestationRequest` sends `nonce` and `signing_algo` only (`AttestationService.swift:56-59`). Chat goes to the gateway (`ConfidentialLanguageModel.swift:46-47`). Not a sink. |
| gateway `signing_algo=ecdsa`, model `ed25519` | **unchanged** | `AttestationService.swift:58`, `+Model.swift:92`. |
| `mr_config_id` checked for the gateway only; no RTMR3 replay | **STILL OPEN** | `AttestationRecord.swift:165-174`. |

**`ATTESTATION.md` at `d7ac963` (171 lines), sentence by sentence where the
comparison called it overstated.**

- `:32-34` "a failed check blocks the send": **ACCURATE for every hard check,
  narrowly overstated for a soft one.** A hard failure — code identity,
  recipe hash, DCAP, nonce, a genuine NVIDIA or TLS rejection, an unbound or
  unsealed key — makes `sendPolicy` `.block` (`degradeIsHardFailure`
  `ConfidentialSession+Verdict.swift:217-244`; `TrustVerdict.sendPolicy`
  `:87-90`); an image that fails provenance, an unreachable NRAS or TLS check,
  or a missing key degrades to `.confirm`, which pauses the send until the
  user accepts (`:241-243`, `:261-267`; `ChatViewModel.postPrepareRefusal`
  `:105-106`). "Blocks" is the hard tier; the soft tier asks.
- `:67-73` (was `:71-72`): "MRTD and the RTMRs are not compared against a
  published build, and the model node's quote is DCAP- and nonce-checked but
  its measurements are not yet bound to a config" — **ACCURATE** (the gateway
  `mr_config` check `AttestationRecord.swift:165-174`; nothing else binds).
- `:98-103` (was `:97-100`): "The model node's compose, its hashes and its
  OS image hash come from the node's report as served and are not yet bound
  to its quote" — **ACCURATE** (`+GPU.swift:86-100`, `+Reports.swift:232`).
- `:104-114` (was `:101-107`): the signer is recovered (ecdsa) or checked
  against the attested key (ed25519) and must be a key the model node's quote
  binds; the signed text is compared whole, `<model>:<req>:<resp>` for
  `provider_tee`, no prefix for `gateway`; any other algorithm or kind is
  rejected; a gateway signature is `.unverified(.gatewayTrustOnly)` — **ACCURATE**,
  line for line with `TEESignatureVerifier.swift:206-262`, `:269-293`.
- `:140-143` (was `:133`): "seals message content, `name`, `refusal`,
  `tool_calls`, the tool schemas and `tool_choice`, and passes the rest …
  model id, sampling parameters, the sequence of roles, and the count and
  ciphertext length of your messages stay readable" — **ACCURATE** for what
  the client sends (`E2EEPeer.swift:114-192`; array content is not sent). The
  developer's draft (`attestation-both-platforms.patch`, not applied at
  `d7ac963` — the tree's `:140-143` has no `reasoning_effort`, `max_tokens` or
  routing-id wording) would name the new fields and add the routing-id bullet;
  until it lands the file is **UNDERSTATED** on those two points, in the safe
  direction.
- `:144-151`: an out-of-date TCB is flagged and continues; "Any other TCB
  status … fails the quote, as near.ai's own SDK does" — **ACCURATE**
  (`DCAPVerifier.swift:44`).
- `:152-157` (was `:144-147`): the probe goes to the model's direct host,
  accepts any certificate, compares the SPKI to the attested fingerprint,
  "and that quote is DCAP-verified like the others. Chat itself goes to the
  gateway … which this check does not cover" — **ACCURATE** (`TLSAttestationVerifier.swift:66-71`,
  `:109-116`, `:246-270`; `Verifiers.swift:180-187`). The old "detects
  interception" claim is gone.
- `:161-164`: gateway-trust-only responses counted separately, never shown as
  verified — **ACCURATE** (`ConfidentialSession.swift:308-316`;
  `AttestationSummary.responseSigState` `:344-348`).
- `:165-169` (was `:156-157`): "the NRAS token's own signature is not checked
  against NVIDIA's JWKS (`NRASService.swift:15-17`)" — **NOW UNDERSTATED /
  STALE**: it is checked (`NRASService.swift:155-190`; the file header `:15-17`
  says so). Wrong in the safe direction; the sentence should be rewritten.
- `:170-171` "The shipped binary is not reproducible" — **ACCURATE**.

None of the overstated sentences concerned a place where plaintext goes; the
tree sends plaintext only where the document says it does (the sealed path's
unsealed metadata), so the claim-correctness items above live under
Residuals and the developer notes, not Findings.

### Traced — at rest

**Store compaction (`Chat/StoreCompaction.swift`).** `requestAfterDelete`
(`:23-25`) sets one `UserDefaults` boolean, `storeCompactionPending` (`:16`)
— no text. `runIfPending` (`:28-37`) runs from `TeemoonApp` before the
`ModelContainer` is created (`App/teemoonApp.swift:205-206`), so it is the
file's only connection: `compact` (`:39-71`) opens the store read-write with
SQLite directly, requires `quick_check == ok` (`:60`), sets `temp_store =
MEMORY` so the rewrite's temporary copy of every remaining chat never lands
in `tmp/` as a file (`:61-66`), `secure_delete = ON` (`:64`), checkpoints and
truncates the WAL (`:67`, `:78-87`), `VACUUM`s (`:68`) and checkpoints again
(`:69`). It refuses when the volume lacks room for a second copy (`:47-49`)
and keeps the flag so the next launch tries again (`:33`); any failure
leaves the file untouched (`:52-56`, `:65`, `:68-69`). Pinned by
`StoreResidueTests`: a 300-message deleted chat's marker is on disk before
and gone after, the kept chat intact and reopenable (`:74-92`); too little
space leaves file and flag (`:125-137`); a non-database file is left alone
(`:139-147`); nothing runs without a delete (`:149-153`). **Mutation:** drop
the `VACUUM` at `:68` (keep the checkpoints) →
`theNextLaunchRewritesTheStoreWithoutTheDeletedChat` red at `:85` — the free
pages the test's premise at `:80` shows are rewritten only by the rebuild;
the `secure_delete` pragma (`:64`) is belt-and-braces for the rewrite's own
deletes, not what removes the existing residue.

**Delete is saved at once (`e871b7a`).** `ThreadDeletion.delete` saves after
the cascade (`Chat/ThreadDeletion.swift:31-32`), `deleteAll` after both
`delete(model:)` calls (`:41`). Store 1.0.5 (43) lacks both lines: a kill
right after a delete could bring the chat back at the next launch — disclosed
below for 1.0.5. Pinned by `StoreResidueTests.aDeleteIsOnDiskBeforeAutosave`
(`:98-123`, a fresh container after each delete sees it gone). **Mutation:**
remove `try? context.save()` at `:32` → red at `:116-117`.

**The search index.** `createSchema` sets `secure_delete = ON` on every open
(`Chat/Search/ChatSearchIndex.swift:283`) and asks FTS5 for `secure-delete`
(`:302`, SQLite ≥ 3.42; older ignores it and `optimize` covers);
`removeAll` drops and recreates both tables (`:399-401`); `purgeDeleted`
merges the segments and truncates the WAL (`:406-410`). It runs after a chat
delete and after delete-all (`ChatSearchService.swift:138-154`) and in the
launch reconcile after stale rows are dropped (`ChatSearchReconciler.swift:60-64`,
`c65fd43`) — so a delete whose hook never ran (a kill, an older build) is
scrubbed at the next launch. The sidecar's protection and backup exclusion
are applied where they were (`ChatSearchService.swift:55-65`, `:85-88` →
`TeemoonApp.hardenConversationStore` `teemoonApp.swift:333-346`, unchanged:
`.completeUnlessOpen` and `isExcludedFromBackup` on the file and its `-wal`/
`-shm`, re-applied each launch). Pinned by
`StoreResidueTests.theSearchIndexKeepsNoTextOfADeletedChat` (`:155-183`) and
`ChatSearchReconcilerTests.reconcile_leavesNoTextOfTheDroppedRowsOnDisk`
(`:140-156`). **Mutation:** remove the `purgeDeleted()` call at
`ChatSearchReconciler.swift:63` → the reconciler test red at `:155`.

**Every delete path, from a whole-tree grep** (`ThreadDeletion\.|\.delete(model:|context\.delete(|modelContext\.delete(|didDeleteThread|didDeleteAllChats|forgetKeptConversations|requestAfterDelete|runIfPending`, 20 hits):

| Path | Store | Index | Kept conversation | Compaction |
|---|---|---|---|---|
| chat list swipe — `Views/Chat/ChatsListView.swift:426-435` | `ThreadDeletion.delete` (`:435`, after a 1 s delay on phone) | `didDeleteThread` → `remove` + `purgeDeleted` (`:426`) | `forgetKeptConversations` (`:427`) | `requestAfterDelete` (`:428`) |
| settings delete all — `Views/Settings/ChatsSettingsView.swift:60-72` | `ThreadDeletion.deleteAll` (`:63`) | `didDeleteAllChats` → drop + recreate + purge (`:66`) | (`:67`) | (`:68`) |
| plain retry — `Chat/ChatViewModel.swift:220-232` | `modelContext.delete` of every message after the question (`:226-227`), saved (`:230`) | `didDelete(messageIDs:)` → `remove` only, **no purge** (`ChatSearchService.swift:131-134`) | not forgotten (the equality rule rebuilds on the next turn, `LiteRTConversationReuse.swift:35-39`) | **not requested** |
| Think Harder `.replace` — `:366-373` | `modelContext.delete` of the superseded reply (`:369`), saved with the new one | `didDelete(messageIDs:)` → `remove` only (`:368`) | not forgotten | **not requested** |
| Siri (`RequestLLMIntent`) | a detached thread, never inserted | `didWrite` is a no-op for it (`ChatSearchService.swift:115-121`) | — | — |

So the two chat-delete paths are the only ones that scrub, as the brief
asked to prove — and the two message-delete paths are not: a retried or
replaced reply's text stays in the index WAL (and the store WAL for a plain
retry, SwiftData's SQLite without `secure_delete`) until the next compaction
or checkpoint — the index's FTS5 `secure-delete` applies at delete time only
on SQLite ≥ 3.42, whose availability on the device was not checked, and its
WAL is truncated only by `purgeDeleted`. Both files are in the protected,
backup-excluded class; this is residue inside the intended place, not a sink
outside it — the same class as the 1.0.5 disclosure, narrower, with no test
covering it: a residual and a developer note, not a finding.

**Backup exclusion and protection class, each launch.** `hardenConversationStore`
(`teemoonApp.swift:333-346`) is unchanged and still called for the store at
`:239` and for the index at `ChatSearchService.swift:64` and `:87`; the
compaction opens the same file before it (`:205-206`) and never creates a
new one (`VACUUM` rewrites in place), so the attributes it carries are the
ones the previous launch set and this launch re-sets. `ConfigStore` still
writes the providers JSON with `.completeFileProtectionUntilFirstUserAuthentication`
and no key in it (unchanged file; the 1.0.5 page's `ConfigStore.swift:457`,
`:12-14`); the NVIDIA migration writes only a model id into it and a notice
sentence into `teemoon-pending-notice.txt` (`ProviderStore+Healing.swift:328-330`,
`:342-346`, the 1.0.5 addendum's mechanism). The verified-digest and
audit-index caches in `UserDefaults` hold no text. The system prompt is still
in `UserDefaults` (`Settings/AppSettings.swift:28`, `:32`) — the carried LOW.

### Build configuration

Confirmed with this review's own commands in the source worktree:
`git diff --stat 705764b d7ac963 -- Vendor/ Packages/ teemoon/Info.plist
teemoon/teemoon.entitlements teemoon.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`
prints nothing for each path (0 stat lines, five times); `git rev-parse` gives
the same ids at both commits — `Vendor` `0fa3ad74…`, `Vendor/textual`
`a39f89a5…`, `Packages` `ab23b2a6…`, `teemoon/Info.plist` `0ffa0bd3…`,
`teemoon/teemoon.entitlements` `80486f2d…`, `Package.resolved` `f9bff566…`,
`PrivacyInfo.xcprivacy` `cc092a89…`. So the dependency graph, the background
modes, the entitlements, the vendored renderer and the three local packages
are the 1.0.5 bytes; `Packages/LiteRTLM/Package.swift:50-54` still names
LiteRT-LM v0.17.1 with checksum
`c94fc12aa0403cb47208e419cc3bfe258214ea17035f7a63c16de536869f2186`, so **the
on-device runtime binary is the 1.0.5 (and 1.0.4) pin** and was not
re-checked. `dcap-qvl-swift` is `0.5.2` @ `80a8a566…` (`Package.resolved:14-20`).
`project.pbxproj` differs by `MARKETING_VERSION` (`:332`, `:356`, `:382`,
`:407`, `:569`, `:619` → 1.0.6) and `CURRENT_PROJECT_VERSION` (`:545`, `:595`
→ 58) only (`git diff … | grep '^[-+]'`: four distinct lines). Still one
application target plus two test bundles; `TARGETED_DEVICE_FAMILY = 1`
(`:583`, `:633`); `DEBUG` only in the project's Debug configuration
(`:465-466`, `:479`). **Clean; no new binary, no new dependency, no new
capability.**

### Sweep adjudication — the 56 NEW rows

`dev-d7ac963.sweep.tsv`: 835 rows, 56 NEW (log 18, net 28, pasteboard 4,
store 6), 779 CARRIED from `tf-1.0.5-43`. Every NEW row, read at its line:

| Rows | What they are | Reachable in Release? | Sink? |
|---|---|---|---|
| `Chat/ChatViewModel.swift:308` (log) | the post-prepare refusal sentence, `.public` | yes | no — fixed text |
| `Chat/StoreCompaction.swift:23`, `:28`, `:40` (store), `:34` (log) | the `UserDefaults` boolean, the launch hook, `FileManager` for the size check; a notice with the outcome name and seconds | yes | no — no text in the flag or the line |
| `Confidential/ConfidentialSession+Refresh.swift:129`, `:132` (log) | model id, 4 hex of a nonce, a compose path; the fetch error | yes | no (table above) |
| `Confidential/NRASService.swift:86`, `:91`, `:103`, `:104`, `:108` (net), `:186` (log) | the JWKS URL and GET, the attest endpoint and issuer, the service init; "token signature invalid" | yes | **no key, no message** — the GPU evidence only |
| `Confidential/TEESignatureVerifier.swift:171`, `:173`, `:179` (net), `:181`, `:198`, `:214` (log) | the signature request with the near.ai Bearer key to the gateway on `URLSession.shared`; attempt/status/algo; fixed strings and a binding reason | yes | **the carried key site**, same host, zero-capacity cache; no body logged (the 1.0.5 `body.prefix(200)` line is gone) |
| `Confidential/TLSAttestationVerifier.swift:112`, `:115` (log) | failure reasons, fixed sentences | yes | no |
| `Inference/ConfidentialLanguageModel.swift:78`, `:83`, `:84`, `:89`, `:110`, `:120` (net) | `URLSession.chat`: ephemeral, no cache, 600 s; the model's session field and its default | yes | no — the session every chat request rides; **strengthened** |
| `Inference/GenerationEngine.swift:116` (net), `:397`, `:399`, `:401`, `:403`, `:409` (log) | the session parameter; the `[TEE]` verdict lines: addresses, expected/got, fixed details, a fetch error | yes | no — addresses and fixed strings, `.public`; no body |
| `Inference/HTTPClient.swift:16`, `:17`, `:19`, `:21` (net) | `URLSessionHTTP` on `.chat` | yes | no — moves four key-bearing families off the shared session |
| `Inference/HTTPTransport.swift:36`, `:48`, `:96`, `:98`, `:102`, `:105` (net) | the session field and parameter; the request with the 600 s header wait; `Content-Type`; the Bearer line (unchanged text, re-fingerprinted by the affinity line); **the affinity header** | yes | the Bearer to the provider's own endpoint (carried); the routing id to three hosts (new, disclosed) |
| `Inference/LiteRTTransport.swift:179`, `:851` (log) | engine and tool-call counts, `.public` | yes | no |
| `Inference/SessionAffinity.swift:40`, `:44` (store) | `Keychain.load`/`save` of the 32-byte secret under `sessionAffinity.secret` | yes | **the Keychain**, AfterFirstUnlock, not synchronizable — the intended place; the secret never leaves it |
| `Providers/Adapters/OllamaAdapter.swift:39`, `:40` (net) | the version probe, now with a timeout parameter; `GET {root}/api/version` on `.shared` | yes — on the first send to an unclassified self-hosted endpoint | a keyless, bodiless request to the user's own server (residual) |
| `Providers/Provider+Presets.swift:91` (net) | the NVIDIA endpoint, unchanged text, re-fingerprinted by the model line `:92` | yes | as at 1.0.5 |
| `Settings/AppSettings.swift:23` (store) | `UserDefaults.standard`, unchanged line re-fingerprinted by the prompt-version change `:20-21` | yes | the carried system-prompt LOW's store |
| `Views/Chat/MessageView.swift:255` (pasteboard) | the reply menu's copy → `UIPasteboard.general` on a tap | yes | a user tap on visible content, the 1.0.5 copy moved into the new menu |
| `Views/Chat/MessageView.swift:257`, `:258`, `:361` (pasteboard) | `NSPasteboard` under `#elseif os(macOS)` | no — not a product | — |
| `Views/Settings/ChatsSettingsView.swift:70` (log) | a SwiftData error from `delete(model:)` | yes | no |

Nothing in the 56 is a sink the App Store build can execute that it could not
at 1.0.5, with two honest additions that are disclosures rather than sinks:
the routing header to three third-party hosts and the first-send probe to the
user's own server. The 779 CARRIED rows were skimmed in full — net, log,
store, pasteboard, render and entry kinds — for a line that interpolates a
body or a key; the hits are the previews, demo and vendor-example lines the
earlier pages exclude, the carried key sites listed under keys, and no
content-bearing log line (the whole-tree logger grep above is the check that
a carried neighbour did not make one new).

### Prior claims re-verified (line numbers at `d7ac963`)

| Claim on the 1.0.5 page | Now at | Status |
|---|---|---|
| `disable()` deletes the four default-store files, then swaps the zero cache; first statement of `init` | `Support/SharedURLCache.swift:20-23` (file unchanged); `App/teemoonApp.swift:38-41` | unchanged |
| First `URLSession.shared` access is `ConfidentialSession(providers:)`; nothing new runs ahead of the init | `teemoonApp.swift` differs only at `:205-206` (the compaction hook, inside the container setup after the init); `URLSession.chat` is a lazy static created on first use | unchanged |
| Seventeen authenticated sites, each to its own provider | table under keys | same set; two lines moved (`TEESignatureVerifier.swift:173`, `BraveWebSearchTool.swift:590`); four families now on the ephemeral no-cache session; **one new non-credential header** to three hosts |
| Catalogue scope hash; `forget(endpoint:)` has no caller | `Providers/LiveCatalogStore.swift:208-211`; `:171`, no caller (grep `forget(endpoint`: the definition only) | unchanged — **INFO carries** |
| `Keychain.deleteAll()` only from `#if DEBUG` | `Providers/Keychain.swift:105-114`; `teemoonApp.swift:42-67` (unchanged) | unchanged |
| UI-test seeding `#if DEBUG` | `ContentView.swift:125-303` (one more door at `:238-240`); `UITestSetupSeed.swift:41-124`, `UITestHostSecrets.swift:16-115` (files unchanged) | unchanged — same fence |
| Three log statements log counts and lengths (LOW CLOSED at 43) | `Inference/ChatGeneration.swift:392`; `GenerationEngine.swift:331`, `:440` | unchanged — **CLOSED** |
| LOW: system prompt in UserDefaults | `Settings/AppSettings.swift:28`, `:32` | unchanged — **LOW carries, waived** |
| Chat request on an ephemeral session; TLS probe carries no credential | `Inference/ConfidentialLanguageModel.swift:83-90`, `:131` (one app-lifetime ephemeral session, `urlCache = nil`); `Confidential/TLSAttestationVerifier.swift:139-141`, `Verifiers.swift:184-187` | strengthened (no cache at all); probe unchanged |
| Single send-authorization definition, re-read after prepare | `Confidential/ConfidentialSession+Verdict.swift:252-257`; `Chat/ChatViewModel.swift:306-320` | unchanged; **two more callers** (Think Harder, the effort retry) go through it |
| Siri refuses on a pending verdict | `App/RequestLLMIntent.swift:87-90` | unchanged |
| Loader at both SwiftUI roots; tail card without it hosts no markdown | `Views/Chat/ConversationView.swift:141`, `:826`; the debug card at `:521-526`, `:987`; `TranscriptCollectionView.swift:1250` | unchanged (lines moved) |
| Image strip unconditional | `Views/Chat/MarkdownParseCache.swift:70-71` (file unchanged) | unchanged |
| Keychain class, not synchronizable | `Keychain.swift:49`, `:61`; no `kSecAttrSynchronizable` (grep 0) | unchanged; one more item under the same class |
| Self-verify script reads the key from the environment | `Confidential/SelfVerifyScript.swift:155`, `:19-20` | unchanged |
| `captureNativeLogIfAsked` env-gated, not DEBUG-fenced | `teemoonApp.swift:30-36`, called `:41`; `DiagLog` at `Inference/LocalRuntime.swift:220-226` | unchanged residual |
| OpenRouter and NVIDIA never presented as attested | `Providers/Provider.swift:291` (file unchanged) | unchanged |
| near.ai directory host must be `https` and `*.near.ai` | `Providers/EndpointDirectory.swift` (file unchanged; `:31`, `:35`) | unchanged |
| Web search: one fixed host, opt-in; DEBUG override parses to loopback | `BraveWebSearchTool.swift:530`, `:535-539` (file unchanged) | unchanged |
| `isPrivateHost` requires four dotted octets | `Providers/Provider.swift:114` (file unchanged) | unchanged; now also gates the first-send probe |
| Fireworks retirement migration: model id and equipped list only, no network | `ProviderStore+Healing.swift:319-366` — the table gains a `source`/`place` and an NVIDIA row | unchanged in mechanism; one more retirement |
| Runtime binary: same pin, capability check stands | `Packages/LiteRTLM/Package.swift:50-54` | unchanged — same checksum, not redone |
| No analytics / crash SDK; config files unchanged | same blobs | unchanged |

**Hand-off claims checked against the tree.** Confirmed: the routing id goes
to the three named hosts and nowhere else (`SessionAffinity.swift:49-55`;
test `:37-45`); `ChatGeneration.generate` iterates the model's stream
(`:312-314`); the sort reorders no array and sealing takes the sorted
plaintext (`PromptCachePrefixTests`); the first-send probe cannot fail or
alter a send and its cancellation is swallowed as a "no" (`ReasoningEffort.swift:150-157`,
`OllamaAdapter.swift:42-46`); thought text reaches neither `Message.content`
nor the card nor a log for the inline form (sentinel tests) and for the
channel form by the `.text`-only chunk filter (`LiteRTTransport.swift:679-682`)
— the latter rests on the runtime's behaviour, which no unit test pins; the
Confidential changes all predate build 50, consistent with every hand-off
saying "nothing under `teemoon/Confidential` changed" from 47 on. Not
confirmed: the developer's "debug bit — likely refuted" (a binary; Not
traced). Refuted or corrected: the `ATTESTATION.md` draft patch is **not
applied** at `d7ac963` (the routing-id bullet and the `reasoning_effort`/`max_tokens`
wording are absent from the tree's `:140-143`), and `ATTESTATION.md:165-169`
still says the NRAS token's signature is not checked, which the code no
longer matches. One observation the hand-offs do not make: the store-residue
fix covers the two chat-delete paths and not the retry / Think Harder
message deletions (at rest, above).

### Not traced (explicit)

- The on-device runtime binary (`CLiteRTLM.xcframework`, the same bytes as at
  1.0.4 by package pin and checksum): the capability check was not redone;
  what it writes under `cacheDir` (`LiteRTTransport.swift:254`, `tmp/`) and
  whether a `ThinkingConfig` thought is really delivered as non-text content
  are properties of the binary.
- Upstream LiteRT-LM source at v0.17.1.
- The dcap-qvl Rust core (`DcapQvlFFI.xcframework`, v0.5.2): whether `verify`
  refuses a TD with the DEBUG attribute by default. The Swift binding was read
  from the SwiftPM cache and exposes no option for it.
- `Vendor/textual` internals: byte-identical to `705764b` by tree id, so not
  re-read beyond the loader and parser entry points the earlier pages cite.
- The large view files (`TranscriptCollectionView`, `ConversationView`,
  `TrustLadderView*`, `VerificationRunView`, `MessageView` outside its hunks)
  were read at their hunks and at the lines cited, not line by line.
- `ChatSearchIndex`'s search path (whether every FTS `MATCH` string is bound
  rather than interpolated); its `exec` logs SQLite's message `.public`
  (`:699`), a carried line.
- The SQLite version on the device (FTS5 `secure-delete` needs ≥ 3.42;
  `optimize` covers older).
- Whether `URLSession` forwards `Authorization` across a cross-host redirect;
  not new, no page has traced it.
- `teemoon.ai/privacy`: not fetched by this review (no network); the quotes on
  this page are from the orchestrator's capture of 2026-10-22.
- The developer's archive figures in the binding row; the orchestrator's
  binary check; the runtime pass; a phone. This is a static read; no runtime
  measurement is claimed here.

## Runtime

### The archive, checked (orchestrator, 2026-10-22)

The developer's `teemoon-b58.xcarchive.zip` re-hashed to
`0d324f414263010aac500778fccc036d1df7abacb96450e1ce6390cee0fa22da` and its
`Products/Applications/teemoon.app/teemoon` to
`40788098ed33de3cb82a20ac19e16b68d8c17e45865b402c8ff5337129adeeb6` (both the
hand-off's figures); `Info.plist` reads `CFBundleVersion 58`,
`CFBundleShortVersionString 1.0.6`, `ai.teemoon.app`. The export-only IPA
(`25c767ce…`) is a second export of the same archive and not byte-for-byte
what Apple received (its signature differs); both its Payload binary and the
archive binary hash to the same bytes after `codesign --remove-signature`
(`18fa0970…`), so the page binds to the archive binary. What this binds: the
bytes on disk are the bytes the developer uploaded to TestFlight (internal
only). What it does not: no rebuild was attempted, so the archive's
provenance from `d7ac963` rests on the developer's statement of a clean
`git archive tf/1.0.6-58` build — as on every iOS page.

### Runtime pass (method §4b) — 2026-10-22, build 58

Built from source at `d7ac963` (`xcodebuild build-for-testing`, Xcode 27.0,
iOS 27.0 simulator `audit-106` created for this pass, Debug configuration —
so the `#if DEBUG` test surfaces above ARE compiled into this binary; the
shipped Release binary lacks them: `teemoon` `5c81db57…`,
`teemoon.debug.dylib` `77789409…`). Sockets polled every two seconds
(`lsof`), the unified log streamed **at debug level** throughout, the
Keychain attributes and the container read afterwards; the nine host key
files' bytes searched for (UTF-8, UTF-16LE and UTF-16BE, never printed).

**Sessions.** The offline product suite `ProductE2ETests` (23 tests, all
passed, 647 s) and the live suite `ProductLiveE2ETests` (5 tests, 4 passed,
275 s): `testLiveTwoTurnWithDebugPanelShowsE2EE` (two sealed turns, the
developer card showing the E2EE request), `testLiveAttestationSheetNamesTheModel`,
`testReverifyRefreshesTheStampAndCopyPutsTheScriptOnTheClipboard` and
`testARejectedCloudKeyIsSaidByTheForm` green;
`testLiveTwoTurnReplySignatureChecksOut` red: "session never reached
end-to-end encrypted (title=near.ai · glm-5.3-flash, encrypted — image
unpublished …)". The app's own log for that session:
`[gateway] model attestation: quote verified, key bound: true, gpu: HOPPER`,
`[nras] GPU attestation verified — verdict PASS, nonce matched`,
`[provenance] all 10 near.ai image(s) trace to a pinned workflow (9
third-party sidecar(s) digest-pinned)` and `[provenance] 10 verified, 1
unpublished (GitHub 404) — sealed send still allowed`. The unpublished
image is the CVM harness's `nearaidev/compose-manager-launcher@sha256:079a14b4…`,
the linux/amd64 child-manifest digest the new measured compose names, for
which GitHub's attestations API answers 404 while the provenance is
published on the OCI index digest `91fdff3c…` (200) — both checked by the
orchestrator on the day. A near.ai-side fact since the fleet move (the
server-side pages of 2026-10-22); the session stays sealed, the send still
goes out encrypted, and the test's stricter wait for "verified" is what
fails. The Android live suite shows the same state.

| Measurement | Result |
|---|---|
| **Egress** — every remote endpoint the process opened | 9 remote `:443` peers over the live session, every one attributed by its certificate (`curl --resolve`) or PTR to a host the exits table names: `40.160.1.150` cloud-api / `glm-5-3-flash.completions.near.ai`; `160.72.54.150` the model's direct host; `104.18.2.115` the Cloudflare edge shared by `openrouter.ai`, `api.fireworks.ai`, `api.x.ai` and `cloud-api.near.ai`; `34.120.45.54` `nras.attestation.nvidia.com`; `4.255.75.174` `api.trustedservices.intel.com`; `13.33.153.12` / `.101` CloudFront (`certificates.trustedservices.intel.com`, `integrate.api.nvidia.com`); `20.26.156.210` `api.github.com`; `185.199.110.133` `raw.githubusercontent.com`. No unexpected host; the offline session opened none. |
| **Logs** — a credential in any line | 2.40 million lines (offline) + 2.29 million (live); **0** contain any of the nine key values. |
| **Logs** — message text in an app-originated line | **0.** Every line holding a session prompt (`seal-me-or-refuse`, `chip-and-panel`, `should-not-leave`, `still-open`, `draft-keep-out`, `live-e2e-debug-one`: 580 lines in all) is the test runner's accessibility snapshot or assertion, none in an `ai.teemoon` subsystem line — the 1.0.4 log LOW stays closed at run time. |
| **Keychain** | 2 items in access group `4786V39YGH.ai.teemoon.app`, both `pdmn = ck` (AfterFirstUnlock), `sync = 0`: the near.ai key the live suite seeded and, new at this release, the routing-id secret (`sessionAffinity.secret`, 32 bytes) — the 1.0.5 pass saw one. The other rows are the system's. Attributes only; never the data column. |
| **Container** | 17 files after both suites. **No URL cache file** (`Library/Caches/ai.teemoon.app/` holds only Metal's four shader-cache files; the 1.0.3 fix holds). The key values: in no file; the prompts: in no file. `Application Support/ModelLists/<64-hex>.json` present (the carried INFO's catalogue file). `Library/Preferences/ai.teemoon.app.plist` keys: `ai.teemoon.auditIndex.{etag,fetchedAt,json}` (the audits index, 839 KB), `ai.teemoon.endpointDirectory.json`, `ai.teemoon.provenance.verified`, `appFontSize`, `braveGroundingEnabled`, `developerModeEnabled`, `numberOfVisits`, `numberOfVisitsOfLastRequest`, `storeCompactionPending` (a boolean — the residue flag holds no text), `systemPrompt` and `systemPromptVersion` (the carried LOW). `Library/Cookies/ai.teemoon.app.binarycookies` (462 B): **one cookie**, `openrouter.ai` `__cf_bm` — Cloudflare's bot-management cookie, set by the OpenRouter catalogue fetch on `URLSession.shared`'s persistent cookie storage and sent back only to that host (the chat session is ephemeral and keeps no cookie); metadata to the key's own provider, noted, not a finding. `Library/HTTPStorages/` (HSTS / alt-svc). `Documents/scrolltrace.log` (115 KB, numeric scroll and stream counters) is `ScrollTrace`, whole type `#if DEBUG` and gated on the `-scrollTrace` argument / `TEEMOON_SCROLL_TRACE` (`ScrollTrace.swift:45-237`, `:271-276`) — written by the DEBUG harness, absent from Release; carried since 1.0. Two SplashBoard `.ktx` snapshots and the saved scene state (the residual stated above). The conversation store itself is not in the container: the UI harness runs an in-memory store, so the at-rest claims stay source, unit-test and (for this release) the developer's phone-gate claims. |

### Mutation checks (orchestrator)

At `d7ac963` (`mut58/mutate.py`: one source edit at a time in a second
detached worktree, `xcodebuild test` of the named Swift Testing suite on the
audit simulator, failures read from the result bundle, the file restored
and `git diff` clean each time). Twenty-one ran and **all twenty-one went
red where the reviewers predicted**: the routing header offered to
`cloud-api.near.ai` (`SessionAffinity.swift:53` →
`eachProviderGetsItsOwnDocumentedKey`); the effort-refusal retry disabled
(`HTTPTransport.swift:149` → `aModelThatRefusesIsAskedAgainWithoutItAndRemembered`,
`anE2EERetryIsSealedAfresh`); `.sortedKeys` dropped (`:402` →
`aRequestBodyIsTheSameBytesEveryTime`); the matcher widened to any 4xx
(`ReasoningEffort.swift:78` → `onlyA400NamingTheParameterIsARefusal`) and
the probe's self-hosted guard dropped (`:152` →
`aNoIsRememberedAndACloudHostIsNeverAsked`); the stop fix reverted to the
session relay (`ChatGeneration.swift:312` →
`aStoppedThinkHarderCancelsTheRequestAndDrawsNoLateReply`,
`aStoppedPlainSendCancelsTheRequestAndSavesNothing`); the history filter
returning every message (`ReplySupersession.swift:30` → four
`ThinkHarderKeepReplyTests` cases, `aNewReplyReplacesTheOldOneInOneSave`
among them — the request-side filter is pinned here, unlike on Android);
the thinking-turn keep rule (`LiteRTConversationReuse.swift:46` →
`aThinkingTurnIsNeverKept`) and the inline-thought strip
(`LiteRTTransport.swift:378` → `anInlineThoughtIsStrippedFromTheReply`);
the VACUUM skipped (`StoreCompaction.swift:68` →
`theNextLaunchRewritesTheStoreWithoutTheDeletedChat`), the immediate save
dropped (`ThreadDeletion.swift:32` → `aDeleteIsOnDiskBeforeAutosave`), the
reconcile purge dropped (`ChatSearchReconciler.swift:63` →
`reconcile_leavesNoTextOfTheDroppedRowsOnDisk`); the in-flight refusal
removed (`ChatViewModel.swift:108` →
`MissingKeySendGateTests.postPrepareRefusalHonoursTheSettledGate`; a first
run against the file's other suite was green — the harness's suite name,
not a gap); the ed25519 quote-binding guard and the ECDSA binding clause
(`TEESignatureVerifier.swift:229`, `:244` →
`modelEd25519ByBoundKeyIsVerifiedAndUnboundIsNot`,
`modelSignatureByUnboundKeyIsNotVerified`), a gateway signature promoted
to verified (`:255` → `gatewaySignerIsNeverVerifiedEvenAsAModelKey`,
`gatewaySignatureIsGatewayTrustOnly`), the content binding accepting any
text (`:286` → both prefix tests and `gatewayKindOverModelTextIsRejected`);
the NRAS token check removed (`NRASService.swift:142` → seven of fourteen
red: `failVerdict_rejected`, nonce, issuer, alg, expiry and the two
inconclusive cases) and the nonce equality alone (`:167` →
`tokenForAnotherNonce_failsHard`); the TCB allow-list widened to everything
but Revoked (`DCAPVerifier.swift:44` → `TcbAllowListTests.rejected(_:)`); the
TLS probe's DCAP outcome ignored (`TLSAttestationVerifier.swift:124` →
`dcapFailureFailsAVerifiedBinding` — pinned here, unlike the Android
seam). Not attempted: the log LOW's closed line (a re-introduction, not a
mutation) and anything needing a device.

### Developer notes from the runtime pass (orchestrator)

- **Regression from 1.0.5, product correctness, fails closed:** every plain
  send to an xAI model that refuses `reasoning_effort` ends in an error
  because xAI's refusal text is `does not support parameter
  reasoningEffort` and the matcher (`ReasoningEffort.swift:77-83`) has no
  separator-free spelling; 1.0.5 (43) never sent the field. Confirmed live
  by the developer on 58 (`grok-build-0.1` 400, `grok-4.3` 200) after the
  orchestrator found it on Android. Fix shape: match `reasoningeffort` (and
  `enablethinking`, `chattemplatekwargs`), status 400 only, with a test on
  xAI's exact body. Nothing leaves the device that the user did not send.
- **near.ai, not the client:** the measured harness compose names the
  launcher by its amd64 child digest (`079a14b4…`, attestation 404) while
  the provenance is on the index digest (`91fdff3c…`); until it is pinned
  by the index or attested per child, every near.ai model reads "encrypted
  — image unpublished" and the sheet never reaches verified.
- **The shared cookie storage** keeps OpenRouter's Cloudflare `__cf_bm`
  cookie between launches (set by the catalogue fetch on
  `URLSession.shared`); metadata to the key's own host, but an ephemeral
  configuration for every non-chat request would leave nothing behind.

### Addendum — build 59: `d7ac963` → `378f8ba` (orchestrator, 2026-10-22)

The developer re-cut after the runtime pass above found the xAI refusal
text that the matcher missed. `git diff --stat tf/1.0.6-58 tf/1.0.6-59`:
four files, +201/−5 — `teemoon/Inference/ReasoningEffort.swift` (+5/−3),
`project.pbxproj` (`CURRENT_PROJECT_VERSION` 58 → 59, twice),
`teemoonTests/ReasoningEffortTests.swift` (+3) and
`teemoonTests/PromptCachePrefixTests.swift` (+191, a new suite). Commits:
`09dcb6e` fix(inference): xAI's camel-case refusal of reasoningEffort is a
refusal, so the send retries without it; `f4ceb4e` test(cache): the prefix
across turns; `378f8ba` the release bump. Nothing else moved: the
preflight's whole-tree sweep at `378f8ba` has **0 NEW** rows against the
58 ledger (835 CARRIED), `conformance/requests.json` is the same
`642d7555…` (normal-send bytes unchanged), `Vendor/`, `Packages/`,
`Info.plist`, the entitlements and `Package.resolved` are untouched.

**The one shipped change, read.** `ReasoningEffort.isRefusal` still
requires `status == 400`; the body is lowercased as before and now has
`_`, `.` and spaces removed before the match, and the match is on three
tokens — `reasoningeffort`, `chattemplatekwargs`, `enablethinking` — so
"Invalid reasoning effort.", `reasoning_effort`, `reasoning.effort` and
xAI's "does not support parameter reasoningEffort" all count, and so does
any body in which those letters appear across a separator. What that
changes for the two questions: nothing. The retry path it feeds is the
one traced above (one re-run of the same turn without the field, rebuilt
and re-sealed from plaintext, the refusal remembered in process memory);
a wider matcher can only cost one such re-run and a quality downgrade on
that model for the launch. The new test bodies pin xAI's exact
`grok-build-0.1` reply and a camel-case `enableThinking`. The new
`PromptCachePrefixTests` suite (`"Prompt cache prefix across turns"`,
serialized, a `URLProtocol` stub serving scripted SSE) asserts that the
request bytes of a search turn, a Think Harder re-ask and a cloud reply's
thinking extend the previous send as a prefix — test-only, not shipped,
and the cache question is not a privacy one.

**Mutation checks at `378f8ba`** (the same harness, the mutation
worktree moved to the tag): a clean baseline of `ReasoningEffortTests` and `PromptCachePrefixTests`
at the tag (21 cases, all green), then two edits, each restored to green:
the new token put back to the 58 spelling (`text.contains("reasoningeffort")`
→ `"reasoning_effort"`, which the separator-stripped text can never
contain) → **3 red** — `onlyA400NamingTheParameterIsARefusal`,
`aModelThatRefusesIsAskedAgainWithoutItAndRemembered`,
`anE2EERetryIsSealedAfresh`, so the xAI body now drives the retry tests
too; and the status guard widened to any 4xx (`== 400` → `>= 400`) →
`onlyA400NamingTheParameterIsARefusal` red, as at 58.

**Storage gate on the shipped build, run by the developer on the user's
phone (2026-10-22 21:54–22:11 CEST, on the user's "go gate"), evidence
re-checked by the orchestrator.** Binding: the 59 archive's Release app
with only its bundle id (`ai.teemoon.app.probe`) and display name changed
and re-signed with a development profile — the orchestrator stripped the
probe binary's signature and it hashes to `08cb2c1b…3856`, the same bytes
as the shipped archive's; `Info.plist` 59; 0 `__llvm_prf` sections. No
`--uitesting`, not the dev bundle, so the real on-disk store was used; the
Gemma bundle (2,588,147,712 B, sha256 `18193810…a63c` at staging) copied
into the probe container and excluded from the grep by path and size.
Turns with the marker `VELLIQUOR-59417-MARKER`: a normal on-device turn, a
Think Harder run to the end, a Think Harder stopped about a second in
(the old reply restored, frames captured). The orchestrator re-grepped the
pulled containers: before the delete 27 files, the marker in exactly
`default.store-wal` (×7) and `chat-search-index.sqlite-wal` (×9), UTF-8
only — the grep finds it when it is there; after a real swipe-and-confirm
delete, a relaunch and 30 s, 28 files and **0 hits in UTF-8, UTF-16LE and
UTF-16BE**, the 776 MB `mldrift_weight_cache.bin` in `tmp/` included;
`default.store-wal` 313,152 → 0 B, the index WAL 276,072 → 12,392 B. Only
the throwaway container was read. Two observations, neither the app's: the
`.profraw` files in `tmp/` come from the test harness's `libRPAC`
injection (the app has no coverage sections); the staged model file's
mtime moved during the run with its size unchanged — pulled back
read-only afterwards it hashes to the same `18193810…a63c` (the
orchestrator re-hashed the pulled copy, 2,588,147,712 B), and its one
extended attribute, `com.apple.dataprotection.policy.exception-applied-by
= com.apple.containermanagerd`, names the cause: the system applied a
data-protection policy to the file, a metadata touch with the contents
identical. Model unchanged by hash.

**Build 60 — the App Store submission (orchestrator, 2026-10-23).** Build
59 had been uploaded TestFlight-internal-only and could not be attached to
the App Store version, so the developer cut `tf/1.0.6-60` → `06cd6f6` from
`9fc55ec`: the tree is `378f8ba`'s code plus the two documentation commits
below and the build-number bump — `git diff --stat tf/1.0.6-59
tf/1.0.6-60` is `ATTESTATION.md` (+21/−6, byte-identical to the diff read
below) and `project.pbxproj` (`CURRENT_PROJECT_VERSION` 59 → 60, twice);
`git diff --stat 9fc55ec tf/1.0.6-60` is the pbxproj alone. No Swift
changed, so the sweep ledger, the mutation results and the storage gate
carry: the unsigned Mach-O of the submitted build is `08cb2c1b…3856`, the
same bytes as 59's archive binary and as the storage-gate probe binary —
the orchestrator stripped both the 60 archive's binary and the submitted
IPA's own Payload binary and both hash to it. Export method
`app-store-connect`, not internal-only; App Store Connect reports the build
VALID and APP_STORE_ELIGIBLE (the developer's figure). The identity rows
above name 60; the review body and every measurement are the 58/59 reads.

**On the tag at 60, documentation only (after the 59 tag at the time):** `3be2c91` then `9fc55ec` on
`release-1.0.6` amend `ATTESTATION.md` (+21/−6, the only file): the sealed
set's line reference corrected to `E2EEPeer.swift:114-192`, the metadata
bullet naming `max_tokens` and `reasoning_effort`, a new bullet for the
per-chat routing id (its three hosts and headers, the 32-byte Keychain
secret — AfterFirstUnlock, not synchronizable, "not in iCloud Keychain but
included in encrypted device backups" — never to near.ai, NVIDIA, Brave or
a home server), and the NVIDIA paragraph rewritten to say the token IS
verified (ES384 against the JWKS, issuer, validity window, `eat_nonce`;
inconclusive on an unreachable JWKS or unknown key id). The orchestrator
read the diff against the code claims verified above and accepts it as
the public text; the tag does not carry it, so the public squash may
differ from `378f8ba` by this file — to be stated at re-identification.
Developer note 1 of the runtime pass (the xAI regression) is therefore
**CLOSED at 59**; the near.ai launcher note stands.

### Findings

One finding new at this release, an INFO on a verification label (below the
carried three); nothing new above INFO. The three findings of the 1.0.4 page
carry with their 1.0.5 statuses, re-read at their `d7ac963` lines:

### LOW (deployed: yes — since 1.0; **CLOSED at 1.0.5 build 43**, `f742cc7`; stays closed) — reply text and model-written tool arguments were interpolated into unfenced log statements

Closed, and still closed. `Inference/ChatGeneration.swift:392` logs the
snapshot count and `self.output.count`; `Inference/GenerationEngine.swift:331`
the stripped-fragment count and their summed length; `:440` `tc.arguments.count`
— counts and lengths at `.public`, no body text at any level. The whole-tree
logger grep above (177 lines) found no interpolation naming a body, prompt or
key, and the 18 NEW log rows of this release are addresses, statuses, counts,
reasons and fixed sentences. `LogPrivacyTests` (`:28-51`) still rejects any
interpolation of eight content-bearing names regardless of privacy mark.
**Mutation:** put `self.output` back into `:392` with `privacy: .private` →
`LogPrivacyTests` red naming the line.

### LOW (deployed: yes — since 1.0, carried) — the user-edited system prompt is stored in UserDefaults, outside the protected store and inside backups

Unchanged. `Settings/AppSettings.swift:28`, `:32`. The default persona's text
changed (`:21`, `{{date}}`) and the migration table knows the old default
(`:214`); the storage did not. **Remediation** as on the base page. **Waiver:**
the user's product decision, relayed on 2026-10-15 and confirmed to the
auditor directly the same day, carries; the finding keeps its class and its
remediation stands for whenever they choose to take it.

### INFO (deployed: yes — since 1.0.4, carried) — a truncated hash of a keyed provider's API key is written to a catalogue file and is never removed

Unchanged. `Providers/LiveCatalogStore.swift:208-211` derives `key-` plus
sixteen hex digits of an unsalted SHA-256 of the key as the list's scope;
`forget(endpoint:)` (`:171`) still has no caller (grep); provider deletion
still deletes the Keychain items and not the list. **Remediation** as on the
base page. Not addressed by this build.

### INFO (deployed: yes) — two key-binding checks read a quote's `report_data` without reading whether that quote verified

A verification label, not a sink: no key and no plaintext moves anywhere
because of it. `AttestationRecord.gpuSigningKeyBoundToHardware`
(`Confidential/AttestationRecord.swift:128-135`) requires a
`gpuQuoteVerification` object and the model node's ECDSA address in its
`report_data`, but never reads `qv.isVerified`; `e2eeKeyBoundToModelTEE`
(`:139-146`) has the same shape for the model quote and the Ed25519 key. The
verifier's gateway branch does require a verified quote
(`TEESignatureVerifier.swift:253`: `att.quoteVerification?.isVerified == true`);
the `provider_tee` branch (`:242-244`) and the ed25519 branch (`:228-231`,
through `e2eeKeyBoundToModelTEE == true`) rely on the two properties alone, so
a `.verified` reply verdict can rest on a quote whose own signature or
certificate chain the Swift parser rejected. The Android reviewer found the
same on the Kotlin port; the orchestrator confirmed the Swift. **Compensation,
from this page's own lines:** the send never waits on the reply verdict — the
gate runs before it. `prepareTurn` settles the DCAP, NRAS and TLS verifiers
(`ConfidentialSession.swift:207-220`, `:246-261`) and a DCAP hard failure on
any quote makes `sendPolicy` `.block` before anything is sent
(`ConfidentialSession+Verdict.swift:71`, `:224`, `:252-257`); a model quote
the parser rejects degrades the state (`:98-100`) and is a hard failure
(`:236-238`). What the gap affects is the per-reply "signed by the model"
label and counter after a turn that was already allowed. **Test gap:** no
fixture builds a record with an unverified quote — `SignatureVerdictTests.quote(reportData:)`
(`:69-85`) always sets `signatureValid: true, certChainValid: true`, and
`record()` (`:98-109`) and the conformance vectors (`ConformanceVectorsSignatures.swift:63-68`)
build on it; the only `isVerified` in both files is that constructor's.
**Remediation:** require `qv.isVerified` in both properties (or in the two
verifier branches, as the gateway branch does), and add a case to
`SignatureVerdictTests` with `signatureValid: false`. **Mutation:** require
`qv.isVerified` in `gpuSigningKeyBoundToHardware` at `:129` → no test red
(the gap this finding names).

### Residuals — by design, stated not hidden

Carried from the 1.0.5 page: opt-in web search is content-driven egress to
one fixed host; provider keys restore via encrypted backup (AfterFirstUnlock,
not synchronizable — now one more item, the affinity secret, in the same
class); an unattested provider reads plaintext by definition; user-initiated
copies — including both developer cards' "Copy Debug Info", which carry the
request body and reply to the general pasteboard on a tap with credentials
redacted — go to the general pasteboard; E2EE metadata is plaintext by
protocol; a no-tap re-send after backgrounding goes through the gate; a
developer-only stderr capture ships env-gated in the release binary
(`TEEMOON_NATIVE_LOG`, also the gate for `DiagLog`); the cache fix is one
silent mechanism; `Keychain.deleteAll()` ships compiled; the reasoning-only
fallback saves a complete reasoning-only reply as the reply text; the
`--uitesting` doors exist in a Debug build only. New or changed at this
release:

- **A per-chat routing id to three third-party providers.** Every request to
  Fireworks, xAI or OpenRouter carries a 32-hex HMAC of the thread id under a
  per-Keychain secret (`SessionAffinity.swift`; AfterFirstUnlock, not
  synchronizable, so it restores with an encrypted backup onto a new phone,
  like the provider keys — "per-Keychain", not strictly per-install), stable
  across launches, so that provider can link one chat's turns to each other
  and to a later launch — which is its purpose (prompt caching). It reveals
  neither the thread id nor the device (keyed, truncated), and never goes to
  near.ai, NVIDIA, Brave or a self-hosted server. It is visible in the
  developer card's header list and in the card's copied text (not in the
  redaction list, `DebugHeaderRedaction.swift:36`). The draft `ATTESTATION.md`
  names it; the tree's `ATTESTATION.md` does not, and neither does
  `teemoon.ai/privacy` — fetched by the orchestrator 2026-10-22 ("Last updated
  October 19, 2026"): its near.ai sentence reads "Your message text is then
  encrypted to that enclave; the model name and request settings are not, so
  near.ai can route the request."; it says "What teemoon collects: Nothing."
  and "On-device models never leave the phone."; it has no sentence on a
  routing or session id, on Fireworks, xAI or OpenRouter linking a chat's
  turns, or on the in-memory kept on-device conversation — two disclosures the
  developer owed on 2026-10-22. Re-fetched by the orchestrator 2026-10-23 after the developer's web
  commit `dfcc648` (tag `prod/2026-10-23`): the page now reads "Last updated
  October 23, 2026" and carries the routing id — "With Fireworks, xAI and
  OpenRouter, teemoon also sends a routing id for each chat" so the provider
  can reuse cached work; "The id stays the same for every message in that
  chat, even after you restart the app, and is different for each chat."; "It
  is made on your phone."; "The id itself doesn't link your chats to each
  other or to you, but the provider can still see that they all use your API
  key." — accurate against the code read above. The in-memory kept on-device
  conversation is still unmentioned ("On-device models never leave the
  phone."): one disclosure the developer owes.
- **Plaintext request settings beside the sealed messages on near.ai.**
  `reasoning_effort` ("low" by default, "high" on Think Harder) and, on Think
  Harder, `max_tokens: 8192` are top-level fields the gateway reads, like
  `model` and the provider extras (`E2EEPeer.swift:191`). By protocol;
  `ATTESTATION.md:140-143` covers them generically ("sampling parameters");
  the privacy page's wording (message text sealed, model name and request
  settings not) covers them. The same effort fields go in the clear to
  Fireworks, xAI, OpenRouter, NVIDIA and an Ollama server — unsealed
  providers that read everything anyway.
- **A minute-resolution send time per user turn** (`[Sent at h:mm a]`) goes
  to the chosen provider when the persona asks for the date, in place of the
  minute that used to sit in the system prompt; never stored.
- **A first-send probe to the user's own self-hosted server** —
  `GET {root}/api/version`, 2 s, no key, no body, once per launch, only for an
  endpoint `isPrivateHost` classifies as the user's and that the Where sheet
  has not already classified. A stop during it records "no" for the launch and
  changes nothing else. A cloud host is never asked.
- **The kept on-device conversation.** Between two on-device turns a
  plaintext copy of the persona, the tool names and the transcript (with the
  time notes) stays in the process heap beside the native KV cache. Released
  on background, memory warning, dead engine, chat delete, delete-all, the
  next on-device turn and exit; **not** on a thread switch or a switch to a
  cloud provider. Never written to disk by the app; the engine's own `tmp/`
  caches are the binary's (Not traced).
- **Residue of replaced and retried replies.** The 1.0.6 scrub covers chat
  delete and delete-all. A retried or replaced reply's text stays in the index
  WAL (and the store WAL for a plain retry) until the next compaction or
  checkpoint: the plain retry deletes and saves at `ChatViewModel.swift:226-230`
  and the Think Harder replace at `:366-373`, both through
  `ChatSearchService.didDelete(messageIDs:)` (`:131-134`), which removes rows
  without `purgeDeleted()`, and neither calls `StoreCompaction.requestAfterDelete()`
  (its two callers are the chat-delete paths, `ChatsListView.swift:428`,
  `ChatsSettingsView.swift:68`). Inside the protected, backup-excluded files;
  the same class as disclosure (a) below, narrower; no test covers it. The
  same two paths also do not call `forgetKeptConversations()` (callers:
  `ChatsListView.swift:427`, `ChatsSettingsView.swift:67`), so on an on-device
  chat the dropped reply's plaintext also stays in `EngineCache.Kept` (heap
  copy + native KV) until the next on-device turn takes the entry
  (`LiteRTTransport.swift:166-170`, removed regardless, rebuilt since the
  transcript differs) or until background, memory warning, a dead engine or
  exit — memory only, the same carve-out as the user's deletion ruling. A
  developer note.
- **Store 1.0.5 (43) residue, disclosed for 1.0.5.** Until this release's
  compaction runs on their container, a user's deleted chats are still
  readable in `default.store`'s free pages and WAL (SwiftData's SQLite without
  `secure_delete`) and in the index until FTS merged them; and a kill right
  after a delete could bring the chat back, because 1.0.5's `ThreadDeletion`
  did not save (`:31-32`, `:41` are new). Both files were protected and
  backup-excluded at 1.0.5 too. The first launch of 1.0.6 after any chat delete
  rewrites the store.
- **The 1.0.5 stop bug, disclosed for 1.0.5.** A stopped cloud request at
  1.0.5 ran to completion on the provider (billed), and a tool round could
  continue; the late reply was never drawn or saved. Fixed here (`cf85750`).
- **SplashBoard app-switcher snapshots.** iOS keeps `.ktx` snapshots of the
  app's last screen in the system's own container; they could not be pulled
  or grepped in the developer's storage gate (two pulls failed, hand-off 51)
  and are outside the app's control — a platform residual the method's §6
  already names.
- **The developer card.** Shows, on a developer's own screen, the request
  body (sorted now; the sealed bytes beside it on E2EE turns), the reply, the
  tool results, the tools JSON on on-device turns, the effort word, phase
  times and a cache percentage; its copy carries the plaintext body and reply
  with credentials redacted. Unchanged in kind.
- **`ATTESTATION.md`** at `d7ac963` is accurate or understated on every
  sentence the comparison flagged, and stale in one safe direction (the NRAS
  token is now signature-checked). The attestation-surface gaps that remain —
  the model compose and `os_image_hash` unbound to a quote, only the first
  model report verified, no OHTTP, no `x-no-aliasing`, the TLS probe on the
  direct host — are stated in the document and are not plaintext sinks.
- **Siri turns** carry `reasoning_effort: low` and a fresh routing id per
  intent to the three affinity hosts, through the same gate, without the probe.

### Controls that would change the verdict

- `SessionAffinity.header(for:)` returning a name for a near.ai, NVIDIA,
  Brave or self-hosted host, or the affinity id being derived from anything
  but the thread id, or the secret being read anywhere but `installSecret()`
  (`SessionAffinity.swift:39-46`), logged, or put in a request.
- `URLSession.chat` gaining a `urlCache`, or any session created before
  `TeemoonApp.init`, or a later assignment of `URLCache.shared`;
  `URLSessionHTTP`'s default moving back to `.shared` with a cache.
- `TEESignatureVerifier.fetch` building its URL from anything but
  `ctx.baseURL`, or `fetchSigningAddress` returning with a key to another
  host.
- The NRAS POST or JWKS GET gaining an `Authorization` header or any body
  but the `nvidia_payload`.
- `classifyIfNeeded` losing the `isSelfHosted` or `storedKind == nil` guard
  (`ReasoningEffort.swift:152-153`), or `isOllama` gaining a header or a body.
- The refusal retry resending `bodyToSend` instead of recursing through
  `makeBody` and `e2eeSealedBody` (`HTTPTransport.swift:149-154`), or
  `isRefusal` (`ReasoningEffort.swift:77-83`) matching a status other than 400
  or more than its five tokens (`reasoning_effort`, `reasoning effort`,
  `reasoning.effort`, `chat_template_kwargs`, `enable_thinking`), or the 400
  body being kept, logged or shown.
- `E2EEPeer.encryptRequestBody` gaining a plaintext pass-through for a
  message field it now seals, or the client starting to send array content,
  `reasoning_content`, `audio` or `function_call` without sealing them.
- `ReplySupersession.history` returning the superseded reply, or
  `generate` building its history from `thread.sortedMessages` directly.
- `ChatGeneration.generate` returning to `session.streamResponse(to:)`, or
  `stop()` no longer cancelling `streamConsumer`.
- `.sortedKeys` applied anywhere but `makeBody`, or a sorted copy of the
  plaintext kept, logged or persisted.
- `LiteRTConversationReuse.afterTurn` keeping a thinking, tool or unfinished
  turn; `EngineCache.Kept` or its state written to disk; `evictAll` no longer
  clearing `kept`; the memory-pressure observer unregistered.
- `InlineThoughtFilter` or `strippingInlineThought` bypassed, or a
  `logger`/`DiagLog` line interpolating `answer`, `piece` or `text` in
  `LiteRTTransport`.
- `StoreCompaction.compact` losing `temp_store = MEMORY` (the rewrite's copy
  would land in `tmp/`), the `VACUUM`, or the WAL truncate; the flag
  carrying anything but a boolean; `ThreadDeletion` losing its saves;
  `purgeDeleted` dropped from the delete hooks or the reconcile;
  `hardenConversationStore` no longer called for the store and the index.
- A `requestAfterDelete`/`forgetKeptConversations` caller added to a path
  that is not a user's delete, or — the other way — the two existing callers
  removed.
- `DEBUG` added to the Release configuration's compilation conditions, or
  any `--uitesting` door (`ContentView.swift:125-303`, `teemoonApp.swift:42-67`,
  `BraveWebSearchTool.swift:522-539`, `UITestSetupSeed.swift`,
  `UITestHostSecrets.swift`, `ReasoningEffort.swift:159-164`) moved outside
  `#if DEBUG` or off the launch argument.
- Any `logger.*` or `DiagLog.note` line interpolating a body, prompt, key or
  the affinity secret; `LogPrivacyTests` losing a name.
- A markdown or image view placed in the tail-card root or the reply menu
  without the non-fetching loader; `Vendor/textual`'s tree id changing.
- An adapter that builds a request from anything but the provider's own base
  URL, or a background catalogue refresh that starts passing a key.
- A model-callable tool that fetches a model-chosen URL or reads other
  threads.
- A changed `Packages/LiteRTLM/Package.swift` checksum, a changed
  `dcap-qvl-swift` pin, or a dependency added to `Package.resolved` with its
  own network client.

### Verdict: QUALIFIED-PASS

Keys: at `d7ac963` a provider key lives in the Keychain and nowhere else on
disk, and leaves only in a request to the endpoint it was saved with — the
1.0.5 sites re-read at their new lines, none added, none removed; the
signature fetch keeps its gateway host and its key; the two new NVIDIA calls
and the first-send probe to the user's own server carry no key; four
key-bearing request families move off the default session onto an ephemeral
session with no cache at all. The one new header is a per-chat routing id —
an HMAC of the thread id under a per-Keychain secret (AfterFirstUnlock, not
synchronizable; it restores with an encrypted backup) that never leaves the
Keychain — sent to Fireworks, xAI and OpenRouter only, pinned by a test that
sees it on those three and on no other host. Messages: the send gate is still
one definition and now also governs Think Harder and the effort-refusal retry,
which is rebuilt and re-sealed from plaintext with fresh per-field envelopes
under the same session client key, nothing from the 400 body kept;
`reasoning_effort` and, on Think Harder, `max_tokens` are plaintext fields
beside the sealed messages on near.ai, by protocol and disclosed; the replaced
reply never reaches the model; a stop cancels the request and a late reply is
neither drawn nor saved; the request-body sort touches the plaintext nowhere
new; on-device thought reaches neither the store, the card nor a log; the
kept on-device conversation lives in memory only and is released on the
events listed; deleted chats are scrubbed from the store at the next launch
and from the index at delete time, and the two chat-delete paths are the only
ones that scrub — replaced and retried replies are not, inside the protected
files, a note. The Confidential tree's signature verifier is what the SDK
comparison asked for (kind branch and `signing_algo`, the model prefix,
ed25519 against the quote-bound key, the rotation path deleted, a gateway
signer never verified), NRAS tokens are signature-, issuer-, window- and
nonce-checked, the TCB allow-list is the SDK's, the TLS probe quote is
DCAP-verified, a pending verdict refuses the send; what stays open there —
the model compose and `os_image_hash` unbound, only the first model report,
no OHTTP, no `x-no-aliasing`, the debug bit resting on a binary — is stated
in `ATTESTATION.md` and sends no plaintext anywhere the document does not
say. One new INFO — two key-binding properties and the two model-signer
branches of the verifier never read whether the quote they bind to verified
(a reply label after a send the DCAP gate already allowed, not a sink; no test
covers it); nothing new above INFO; the system-prompt LOW carries under the
user's waiver, the catalogue INFO carries, the log LOW stays closed. The on-device
runtime binary is the same pin as at 1.0.4 and was not re-checked; the
runtime pass and the binary binding are the orchestrator's.

**Developer notes (not findings):**

1. `Chat/ChatViewModel.swift:226-230` and `:366-373` delete messages without
   `StoreCompaction.requestAfterDelete()` and through
   `ChatSearchService.didDelete(messageIDs:)` (`:131-134`), which does not
   `purgeDeleted()`: a retried or replaced reply's text stays in the index
   WAL (and the store WAL for a plain retry) until the next compaction or
   checkpoint; no test covers it. Neither path calls
   `LiteRTTransport.forgetKeptConversations()` either (its callers are
   `ChatsListView.swift:427` and `ChatsSettingsView.swift:67`; `kept` is
   otherwise cleared only by `evictAll` on background/memory warning
   (`LocalRuntime.swift:249-254` → `LiteRTTransport.swift:176-182`), by
   `discard` on a dead engine (`:784` → `:190-194`), by `takeKept` on the next
   on-device turn (`:166-170`, the entry removed regardless and the
   conversation rebuilt because the transcript differs —
   `LiteRTConversationReuseTests.everyMismatchRebuilds` `:33-41`), and by
   exit), so after a retry on an on-device chat the dropped reply's plaintext
   stays in `EngineCache.Kept` (heap copy + native KV) until one of those —
   memory only, the same carve-out as the user's deletion ruling. Request the
   compaction, the purge and the forget on both paths, and add a residue test
   for the retry path.
2. `ATTESTATION.md:165-169` says the NRAS token's signature is not checked
   against NVIDIA's JWKS; `NRASService.swift:155-190` checks it. Apply the
   draft `attestation-both-platforms.patch` (the `reasoning_effort`/`max_tokens`
   wording and the routing-id bullet), and rewrite `:165-169`.
3. `Views/Chat/DebugHeaderRedaction.swift:36` could add `x-session-affinity`,
   `x-grok-conv-id` and `x-session-id` so a pasted card does not carry the
   per-chat routing id. Not a secret; hygiene.
4. `Inference/SSEParser.swift:303-306`: a `reasoning_content` field that
   fails to decrypt is passed through as ciphertext into the reasoning block,
   where a `content` field that fails to decrypt fails the stream. A
   claim-correctness note for the attestation surface, not a privacy sink.
5. `Inference/ReasoningEffort.swift:154-155` with `OllamaAdapter.swift:42`: a
   stop during the first-send probe is recorded as "not Ollama" for the
   launch (the hand-off already lists it for 59). Check cancellation before
   recording.
6. `teemoon.ai/privacy` (the orchestrator's capture of 2026-10-22, "Last
   updated October 19, 2026") omits the routing id to three providers and the
   in-memory kept on-device conversation ("On-device models never leave the
   phone."); both belong in the disclosure.
7. `teemoonTests/SharedURLCacheTests.swift:46`'s comment ("Chat, attestation,
   Brave and key checks run on `.chat` since 1.0.6") overstates: the signature
   fetch (`TEESignatureVerifier.swift:179`), the NRAS POST and JWKS GET
   (`NRASService.swift:63`, `:91`), the collateral, provenance, audit-index
   and Ollama-probe requests still run on `URLSession.shared` — behind the
   zero-capacity cache, so not a sink; the comment should say which.
8. Attestation-surface items outside this audit's axis, for the record:
   only `.first` model report verified (`AttestationService+Reports.swift:225-232`);
   the model/GPU quotes' measurements bind nothing (`AttestationRecord.swift:165-174`
   is gateway-only); no OHTTP; no `x-no-aliasing`; the TLS probe's host is the
   direct host, not the chat gateway.
