# teemoonai/teemoon-ios @ tf/1.0.5-43 (705764b) — TestFlight candidate 1.0.5 (43), not yet submitted

## verdict: QUALIFIED-PASS — keys: no new request site, no new host, no new file; the one new key-touching surface is a UI-test seeder that reads provider keys from files on the developer's Mac and is compiled out of the Release configuration (DEBUG is set only for Debug, the file's body is wholly inside #if DEBUG, every door also needs the --uitesting launch argument); the host-classification bug that let a public hostname wearing a private IPv4 prefix read as the user's own machine is fixed and pinned, and it never moved a key off its own endpoint; messages: the backgrounded on-device turn is re-asked through the same send gate to the same provider; the developer card's new on-device speed row is two numbers, a backend word and a boolean; a finished E2EE turn's card now carries the sealed body it had been dropping; the Brave search context gains a fixed citation sentence; the three findings of the v1.0.4 page — two LOWs and one INFO — are all still open at 8ab468a; at the page's commit 705764b (build 43, second addendum) the log LOW is CLOSED (counts and lengths replace the text in all three statements, pinned and measured), the system-prompt LOW stays open under the user's waiver as relayed, and the INFO carries: the commit titled "the 1.0.4 audit's three cheap findings" closes a product review's items, not this audit's; the on-device runtime binary is the same pin, not re-checked

| | |
|---|---|
| **client** | teemoon iPhone app — TestFlight candidate **1.0.5 (43)**, uploaded to App Store Connect 2026-10-15 16:12 EDT (VALID), not submitted to the App Store. Builds 39, 40, 41 and 42 (`8ab468a`, `45b3bb3`, `8622780`, `719ea1c`) were uploaded and withdrawn in turn as the scope widened; the review body below was written against build 39, and the `8ab468a` → `719ea1c` → `705764b` deltas (six shipped commits) are the two addenda before Findings |
| **identity** | tag `tf/1.0.5-43` → commit `705764b71ec5…` (`705764b`, tree `c1199303…`), worktree checked out detached and `git rev-parse HEAD` compared; the body of this page reads `tf/1.0.5-39` → `8ab468ab9fdfd2b83ce851d6452b7cb4ac8acc07` (tree `faf352dc…`), of which `705764b` is a descendant by six shipped commits (`719ea1c` = build 42 after four, then `f742cc7` and the version bump) |
| **seen in** | not yet seen on any store; TestFlight build 43 |
| **source** | [github.com/teemoonai/teemoon-ios](https://github.com/teemoonai/teemoon-ios) — dev tree; the public tag follows the App Store release |
| **binary binding** | the developer's figures, orchestrator verification pending: `.xcarchive` built from a clean worktree of `tf/1.0.5-39`, copy at `~/teemoon-backups/release-1.0.5-39/teemoon-b39.xcarchive`; archive zip sha256 `44a5eac849ed26da4552131f543fdee39b2bc986df379266e73ee49839e2fc47`; `teemoon.app/teemoon` sha256 `92b1620e2751b336b6fa9214dd6d98e63f064509504c5579b65bbec3b9896df6`, arm64 UUID `DA109A19-7AAA-3D78-9FFD-292079527711`; `CFBundleVersion` 39, `CFBundleShortVersionString` 1.0.5, `ai.teemoon.app`, team `4786V39YGH`; Release configuration, development-signed on disk, App Store signing at upload, no IPA kept. None of this was reproduced by this review. |
| **review** | independent AI source review, Claude Fable 5.1 (reviewer A), 2026-10-15 — delta from [`v1.0.4-3abe3e2.md`](v1.0.4-3abe3e2.md) (diff base `tf/1.0.4-38` → `e4df0e2`, code-identical to the page's tree under `teemoon/`); static source read of every hunk of the shipping diff and of every load-bearing line of the base page at its new number; blinded from the second reviewer; skeleton page written before the first source read. Runtime pass and binary check are the orchestrator's. Method: [`/client/method.md`](/client/method.md) |

**coverage:** every hunk of the shipping-code diff `e4df0e2 → 8ab468a` under
`teemoon/`, `Packages/` and `teemoon.xcodeproj` (35 files, +589/−222; tests,
docs and tooling excluded) read in full and traced from where a key or
plaintext exists to any sink it touches; the project file read for the
compilation conditions of both configurations and for the new source file's
target membership; every claim of the v1.0.4 page re-read at 8ab468a; the
orchestrator's 832-row fingerprint sweep of the whole tree skimmed in
context, its 24 NEW rows adjudicated one by one. The ten points of the
reviewer brief are each answered below. Not read: the on-device runtime
binary (same pin as at 1.0.4), upstream LiteRT-LM source, the vendored
renderer beyond its loader, and large view files outside the diff.

---

# teemoon iPhone client (1.0.5 candidate) — Key and Plaintext Exfiltration Audit (delta from `e4df0e2`)

> Client side of the teemoon plaintext question. Lineage: [`../README.md`](../README.md)
> · Map: [`../ARCHITECTURE.md`](../ARCHITECTURE.md) · Surface: [`../audit-surface.md`](../audit-surface.md)

Build 39 is a maintenance release built mostly for its UI-test harness:
sixty-six commits, twenty-four touching shipping code, and of those the
substantive ones are a one-launch setup seeder for capture rigs, an on-device
speed row on the developer card, a fix that re-asks an on-device turn cut
off by backgrounding, a host-classification fix, a developer-card fix for
finished E2EE turns, a Fireworks preset refresh, and a regenerated price
table. For keys that means one new reader of key files on a developer's
host and one new override of the Brave endpoint — both of which have to be
shown dead in the App Store build. For plaintext it means a re-ask path, a
new row of figures on the one card that prints request bodies, and a fixed
sentence appended to what the search tool feeds the model. Each is traced
below.

## Audit prompt

The portable prompt in [`method.md` §3](../method.md#3-the-portable-audit-prompt),
in its delta form, with:

```text
TARGET   teemoon-ios  tag tf/1.0.5-39  @ 8ab468ab9fdfd2b83ce851d6452b7cb4ac8acc07
PREVIOUS teemoon-ios  tag tf/1.0.4-38  @ e4df0e2  (== v1.0.4 @ 3abe3e2 under teemoon/)
DIFF     git diff e4df0e2 8ab468a -- teemoon/ Packages/ teemoon.xcodeproj
           (1,631 lines, 35 files)
```

plus the ten questions of the reviewer brief: the seeder and its fences; the
Brave endpoint override and the citation suffix; the developer card's new
figures, its copy path, and the E2EE-card fix; the LiteRT backgrounded-turn
re-ask, drain log and cache directory; the host-classification fix; the
commit named for "the 1.0.4 audit's three cheap findings"; the Fireworks
preset and price data; the 24 NEW sweep rows; the turn-off-and-retry and
glide changes; the LiteRT-LM package pin.

---

## Results

### Delta map: `e4df0e2` → `8ab468a`

| Area | Change | Reaches keys? | Reaches plaintext? |
|---|---|---|---|
| `App/UITestSetupSeed.swift` (new, +124), `App/ContentView.swift` (+40/−2), `App/teemoonApp.swift` (+53), `App/NetworkPathObserver.swift` (+6/−1) | a one-launch multi-provider seeder reading keys from host files; a placeholder Brave key; every unseeded preset's key slot cleared and the Brave slot deleted on a keyless test launch; a stand-in weights file; a planted config under `temporaryDirectory`; a simulated-offline path | **yes — reads key files and writes the Keychain; wholly `#if DEBUG` + `--uitesting`** | no |
| `Inference/BraveWebSearchTool.swift` (+20/−2) | a `--uitesting` loopback override of the Brave endpoint inside `#if DEBUG`; a fixed citation sentence appended after the `<source>` XML | the override is dead in Release | the suffix is a constant, not content |
| `Inference/LastRequestDebugInfo.swift` (+87/−2), `Views/Chat/RequestDebugView.swift` (+28/−83), `Inference/ChatGeneration+Stream.swift`, `GenerationEngine.swift`, `GenerationEvents.swift`, `GenerationTransport.swift`, `HTTPTransport.swift`, `SSEParser.swift` (+6) | on-device speed row (decode rate, prefill rate, backend word, speculative flag); llama.cpp `timings` parsed from the stream; the sealed body carried through `finishGeneration` | no | the card still prints the request body and reply it always printed; the new fields are numbers and a word |
| `Inference/LiteRTTransport.swift` (+46/−27), `Chat/ChatViewModel.swift` (+9/−2) | a backgrounded on-device turn throws `CancellationError` after the drain so the view re-asks it; the engine records its backend; `LocalEngineResidency.lastLoad` removed | no | **the re-ask goes through the send gate to the same provider** |
| `Providers/Provider.swift` (+7/−2) | `isPrivateHost` requires every dotted label to be an octet | **strengthened** — the key field could be hidden and the cleartext warning skipped for an attacker-registered host; no key ever left its own endpoint | **strengthened** — the trust sheet no longer says "on your own machine" for a public host wearing a private prefix |
| `Providers/Provider+Presets.swift` (+5/−9), `ListPriceSnapshot.swift`, `NearAIModelCatalog.swift` (1/1) | Fireworks default model `kimi-k2p6` → `kimi-k3`; seven Fireworks price rows dropped, one added; OpenRouter price snapshot regenerated 2026-10-15; `typesafe/` classified as proxied | no — the Fireworks endpoint line is unchanged | no — data read by the catalogue and the browser's price column |
| `Views/Chat/ConversationView.swift` (+16/−8), `TranscriptCollectionView.swift` (+21/−4), `FollowGlide.swift` (+9), `ChatView.swift` (+3), `WhereChip.swift` (+7/−1), `TrustLadderView*.swift`, `ModelDetailView.swift` (+6) | "turn off & retry" declines the thread's search offer before retrying; one eased glide at turn start; accessibility labels; the not-encrypted sheet re-reads whether a near.ai key exists when its key form closes; one fetch per push | the key re-read is a Keychain boolean | UI state only |
| `Inference/LocalRuntime.swift` (+1/−24), `LocalLanguageModel.swift`, `LiteRTSpeculativeDecoding.swift`, `XAIAdapter.swift`, `OpenRouterAdapter.swift` | comments and a removed property | no | no |
| `Packages/LiteRTLM/` | `Package.swift` comments, `.gitignore`, `VENDORING.md` — the binary target pin unchanged | no | same binary as 1.0.4 |
| `project.pbxproj` | `MARKETING_VERSION` 1.0.4 → 1.0.5, `CURRENT_PROJECT_VERSION` 38 → 39; nothing else | no | no |
| `Package.resolved`, `Info.plist`, `teemoon.entitlements`, `PrivacyInfo.xcprivacy`, `Vendor/`, `Packages/ModelBackend`, `Packages/TDXQuoteVerifier`, `Packages/LiteRTLM/artifacts` | byte-identical (same git blob or tree ids: `f9bff56`, `0ffa0bd`, `80486f2`, `cc092a8`, `0fa3ad7`, `8135f4d`, `d351d91`, `e162e66`) | — | — |

### Traced — keys

**No new authenticated request site.** The seventeen sites of the v1.0.4
page were re-read at 8ab468a; every one is at its old line or within a few
lines of it, and no new `Authorization`, `X-Subscription-Token` or
`authHeaderName` set exists anywhere in `teemoon/` (whole-tree grep, then
each hit read): `Inference/HTTPTransport.swift:77-81`;
`Providers/NearAIModelCatalog.swift:280-282`;
`Confidential/AttestationService.swift:59-62`;
`Confidential/AttestationService+Model.swift:107-110`;
`Confidential/TEESignatureVerifier.swift:161-164`;
`Providers/ProviderKeyValidator.swift:56-58`, `:59-61`, `:62-66`;
`Inference/BraveWebSearchTool.swift:459` and `:582` (the search call moved
from `:568` by the fourteen lines of the endpoint override);
`Providers/Adapters/FireworksAdapter.swift:217-220`;
`Providers/EndpointModelCatalog.swift:209-215` via `XAIAdapter.swift:51-56`,
`OpenRouterAdapter.swift:48-49`, `:331-334`, `:387-390` and
`NVIDIAAdapter.swift:52-53`; plus the two generic probes
(`EndpointModelCatalog.swift:169-170`, `Views/Where/HomeServerProbe.swift:149-151`).
The structural guarantee is unchanged: an adapter is chosen from the host of
the provider's own base URL (`EndpointModelCatalog.swift:147-155`) and the
request is built from that same base; the background catalogue refresh
still passes an empty key to every public list
(`Providers/LiveCatalogStore.swift:127`, `:200-205`). No `URLQueryItem`
carries a key (grep: the only query items are Brave's `q`, counts and
budgets, and Fireworks' `pageToken`). **Unchanged.**

**The host-classification fix (`e1f8636`) — what was wrong, and whether a
key could travel.** At e4df0e2 `Provider.isPrivateHost` parsed the host's
dotted labels with `compactMap { UInt8($0) }` and required four results.
`compactMap` drops what it cannot parse, so `10.0.0.1.attacker.com` kept
four octets and classified as 10.0.0.0/8. At 8ab468a
`Providers/Provider.swift:121-123` splits the labels, parses them, and
requires both counts to be four. `isSelfHosted` (`:80-83`) is the only
caller, and what hangs off it is: `requiresAPIKey` and the key field
(`Views/Settings/AddEditProviderView.swift`, `ProviderStore+Healing.swift:162`),
the cleartext-http warning, the Where sheet's `home` filing
(`Providers/WhereLocality.swift:62`), the Ollama warm-up gate
(`Providers/Adapters/OllamaAdapter.swift:283`), and — the one the commit
names as the product's central claim — `TrustVerdict.chipMode` returning
`.selfHosted` (`Confidential/TrustVerdict.swift:104`), which makes the trust
sheet say "on your own machine". None of these changes where a key is
sent: a key is stored under the endpoint it was entered for and attached
only to requests built from that endpoint, and the misclassification's
effect on keys was to *hide* the key field (`requiresAPIKey` false), not to
route a stored key elsewhere. The exposure was a user who added an
endpoint under an attacker's hostname being told their plaintext stayed
home while it went to a public server — a user-chosen send path with a
false label on it, which is the UI-claim class [`method.md` §7](../method.md#7-what-this-audit-does-not-cover-on-purpose)
leaves to the attestation-surface review, not an exfiltration sink. The
fix is pinned by `teemoonTests/PrivateHostTests.swift`: eight public hosts
wearing private prefixes (including an out-of-range label and a trailing
root dot), both ends of every private range, the presets that must stay
public, and the `isSelfHosted → chipMode` chain. `NetworkPathObserver` is
not involved; its change (`App/NetworkPathObserver.swift:53-64`) is a
`-simulateOfflinePath` launch argument inside `#if DEBUG`, `false` in the
`#else` branch. The `typesafe/` line in `a064c91`
(`Providers/NearAIModelCatalog.swift:140`) adds a vendor namespace to the
proxied tier, so a `typesafe/…` model on near.ai is never presented as
attested; it does not touch a request. **Strengthened; not a base-page
item.**

**The seeder: what it reads, what it writes, and why the App Store build
cannot run it.** `App/UITestSetupSeed.swift` is a new file under
`teemoon/App/`, so it is compiled into the `teemoon` target by the
synchronized folder (`project.pbxproj:64-70`; the folder's only membership
exceptions are the two Info plists, `:42-49`; the file is not named
anywhere in the project). Its entire body is inside `#if DEBUG`
(`UITestSetupSeed.swift:41` … `:124`); outside that fence the file is two
imports. `DEBUG` is defined once, in the project-level Debug
configuration — `SWIFT_ACTIVE_COMPILATION_CONDITIONS = "DEBUG $(inherited)"`
at `project.pbxproj:479` and `GCC_PREPROCESSOR_DEFINITIONS = DEBUG=1` at
`:465-468` — and nowhere in the Release configuration (`:485-536`) or in
either target-level configuration (`:539-586`, `:589-636`), which set no
compilation condition at all. So in a Release build the type does not
exist. In a Debug build it is reached from one place,
`App/ContentView.swift:130-136`, inside the `#if DEBUG` block `:125-299`,
and only when `--uitesting` is among the launch arguments (`:105`), the
process environment carries `UITEST_SEED_SETUP`, and the JSON parses.
What it then does: replaces the provider list — which under `--uitesting`
is in memory (`App/teemoonApp.swift:292-300`, the `#else` branch returns
`false`) — with the named presets, local servers and on-device models
(`UITestSetupSeed.swift:97-98`); for each cloud preset reads a key from a
file on the host and writes it to the Keychain under the preset's endpoint
(`:100-108`, via `UITestHostSecrets.keyFromHostFile`); optionally marks
on-device models resident (`:110-114`); picks the active one (`:116-118`).
The key files are `UITestHostSecrets.swift:20-27` (`.NEAR_AI_API_KEY`,
`.XAI_API_KEY`, `.FIREWORKS_API_KEY`, `.OPENROUTER_API_KEY`,
`.NVIDIA_API_KEY`, `.BRAVE_ANSWERS_API_KEY`, `.BRAVE_API_KEY` and their
lower-case twins), looked for in three directories (`:49-61`): the path in
`TEEMOON_STAGED_KEYS` or `Application Support/uitest-host-keys` (`:79-87`),
the path in `TEEMOON_HOST_HOME` (`:90-93`), and `SIMULATOR_HOST_HOME`,
which is `nil` off the simulator (`:98-105`). The keys never come from the
environment — the file's own header says why (`:5-8`) — and the whole enum
is `#if DEBUG` (`:16`, `:115`). Its six `os_log` lines (`:77`, `:90`,
`:104`, `:106`, `:113`, `:119`) carry preset names, repo ids and counts,
never a key. **Dead code in the App Store build; in a Debug build it
touches only an in-memory store and the Keychain slots the test owns.**

Two more DEBUG-only doors in the same block, each read: the placeholder
Brave key `uitest-brave-key` written when `UITEST_SEED_GROUNDING ==
"placeholder"` (`ContentView.swift:276-278`), and the keyless-launch
clearing — every preset endpoint this launch did not seed gets an empty
credential (`:279-288`, which `setCredential("")` turns into a Keychain
delete, `Providers/ProviderStore+Credentials.swift:146-147`), and the Brave
grounding slot is deleted outright (`Keychain.delete(for:
BraveWebSearchTool.keychainKey)` at `:295`, under the condition at `:289`:
`--uitesting` and `UITEST_SEED_GROUNDING` neither `"1"` nor
`"placeholder"`). On a signed simulator the Keychain outlives a run, which
is the reason given (`:280-283`, `:290-294`). The commit `d9febed` says the
on-device journeys were run on a phone under a separate bundle id so that
this clearing could not touch the owner's keys — a developer-process
observation, not a code property; the code property is that `:295` is
inside `#if DEBUG` and behind `--uitesting`. **Dead in Release.**

**The planted config and the stand-in weights.** `App/teemoonApp.swift:257-290`
(`#if DEBUG`) builds a `ConfigStore` in a fresh
`temporaryDirectory/uitest-config-<UUID>/` (`:269-272`) when `--uitesting`
and `UITEST_SEED_CONFIG` are set (`:268`), and writes either a deliberately
unparseable file (`:275-276`) or two copies of the Fireworks preset
(`:280-283`). The config projection carries no credential — the key lives in
the Keychain under the server id (`Providers/ConfigStore.swift:12-14`, `:49`;
`ProviderConfigProjection.swift:62`) — and the preset written has none. The
stand-in weights (`:128-137`) are the eight bytes `stand-in` written to a
catalogue model's path, inside both `#if DEBUG` (`:117`) and
`#if targetEnvironment(simulator)` (`:128`), and never over a file that
exists (`:132`). The store selection at `:73-78` is the only place either
reaches the app: the `#else` branch is the 1.0.4 line. **Dead in Release.**

**The Brave endpoint override.** `Inference/BraveWebSearchTool.swift:521-531`:
inside `#if DEBUG` (`:522-529`), with `--uitesting` present and
`UITEST_BRAVE_ENDPOINT` set, the endpoint is the override if it
`hasPrefix("http://127.0.0.1:")` (`:526`); otherwise, and always in Release,
it is `https://api.search.brave.com/res/v1/llm/context` (`:530`). The brief
asked whether the prefix check can be made to name another host. It can:
Foundation's `URLComponents(string:)` reads
`http://127.0.0.1:1@evil/` as user `127.0.0.1`, password `1`, host `evil`,
and appending the query items at `:556` yields
`http://127.0.0.1:1@evil/?q=…` with host `evil` (checked by running the
parse, not inferred). The key would then ride `X-Subscription-Token`
(`:582`) to `evil`. What stops that: the branch does not exist in the
Release binary, and in a Debug build it needs both the launch argument and
the environment variable, which only the test runner sets — no URL scheme,
intent or other app can add a launch argument to a running or launched
teemoon process. A tighter check (parse, then require host `127.0.0.1`) is
a developer note, not a finding. The sweep's two NEW rows here (`:526`,
`:530`) are this override and the real endpoint. **Dead in Release.**

**`Keychain.deleteAll()`** (`Providers/Keychain.swift:105-114`) is still
called from one place, `App/teemoonApp.swift:65`, inside `#if DEBUG`
(`:42-67`) behind `--fresh-install`. Storage class and sync flag unchanged
(`Keychain.swift:49`, `:61`). **Unchanged.**

**The not-encrypted sheet's key re-read** (`8618ac2`):
`Views/Chat/TrustLadderView+None.swift:273-275` re-snapshots
`providerStore.hasCredential(for:)` — a boolean from a Keychain round trip —
when the key form closes (`:258`), replacing the once-per-appearance read
(`TrustLadderView.swift:218`). No key value leaves the store. **Clean.**

**Everything else on the key path** — entry field, the local expiring
pasteboard for key copy (`Views/PlatformChrome.swift:139-147`), copy-path
redaction on every debug card (`Views/Chat/DebugHeaderRedaction.swift:69-72`,
unconditional), the self-verify script reading the key from the environment
(`Confidential/SelfVerifyScript.swift:155`) — re-read at the same lines.
**Unchanged.**

### Traced — prompt and reply text

**The send gate and the new re-ask path.** `d9febed` makes an on-device turn
that was stopped because the app went to the background reach
`ChatGeneration` as a `CancellationError` instead of as a partial answer:
`Inference/LiteRTTransport.swift:714-717` throws after the drain when
`backgrounded` is set. `ChatGeneration.swift:321-329` catches it and, since
the user did not tap stop, records `interruptedThreadID`. On return to the
foreground `Views/Chat/ChatView.swift:694-699` asks
`ChatViewModel.interruptedUserMessage` (`Chat/ChatViewModel.swift:180-192`,
now tolerant of a saved partial reply after the question) and calls
`retry(from:)` — `ChatView.swift:870-878`, which runs `prepareSend` with
`trust: confidentialSession.sendPolicy` (`:875`), the one definition
(`Confidential/ConfidentialSession+Verdict.swift:252`), and then
`ChatViewModel.retry` (`:194-240`) → `generateResponse` (`:242`), which
refuses a keyed provider with no key (`:258-267`) and re-reads the policy
after `prepareTurn` (`:269-280`). The re-asked prompt is the thread's own
last user message, sent to the active provider through the same transport
it would have used on a tap. It goes nowhere new. The Siri intent still
refuses on a pending verdict (`App/RequestLLMIntent.swift:87-90`).
**Strengthened in reach, unchanged in gate.**

One thing the developer flagged and this read confirms, as behaviour rather
than as privacy: the wait loop at `LiteRTTransport.swift:656-683` tests
`backgrounded || dead` (`:659`) before `finished` (`:670`), so an answer that
completed inside the 100 ms sleep (`:679`) just as the app backgrounded is
returned as the drained partial and then thrown at `:716` — a finished
answer re-asked. Same provider, same gate; a double answer, not a leak.

**The developer card.** The new on-device row is built from
`OnDeviceRun` — a `backend` string that is one of two literals, `"gpu"` or
`"cpu"` (`LiteRTTransport.swift:230-232`, from an enum switch), and a
`speculative` boolean (`Inference/LastRequestDebugInfo.swift:155-162`) — and
`EngineTimings` — three numbers and a count (`:165-172`), filled on-device
from LiteRT's benchmark info (`LiteRTTransport.swift:722-727`) and over
HTTP from a llama.cpp `timings` object read as `NSNumber`s only
(`Inference/SSEParser.swift:250-252`; `LastRequestDebugInfo.swift:176-184`).
`speedLine` (`:142-149`), `timingLine` (`:124-134`) and `prefillSummary`
(`:112-117`) format nothing but those. No model name, path or text enters
through the new fields; the model file's name was already in the on-device
card's `requestHeaders` (`LiteRTTransport.swift:769-775`) and the messages
in its `requestBodyJSON` (`:776`), unchanged. The card is shown only with
developer mode on, the per-thread toggle on, and no error
(`Views/Chat/ConversationView.swift:319-322`), hosted as the tail card
(`:973-981`, `:983-988`).

Where the card's text goes: the context-menu copy is
`UIPasteboard.general.string = debugText` (`Views/Chat/RequestDebugView.swift:226`)
— the plain general pasteboard, not the expiring concealed one the key
copy uses. `debugText` (`:37-66`) redacts header credentials on the copy
path unconditionally (`:50`, `DebugHeaderRedaction.swift:69-72`) and includes
the request body (`:52-53`), tool results and the reply — the user's own
conversation, on a user tap, which the base page carries as a residual.
Unchanged by this release.

**`7ca0b46` — the E2EE card fix, and which item it closes.** Before it,
`finishGeneration` rebuilt `LastRequestDebugInfo` without `sealedBodyJSON`
(a field that defaults to `nil`, `LastRequestDebugInfo.swift:56`), so for
every *finished* E2EE turn the on-screen row — which shows the sealed bytes
when it has them and the pre-seal plaintext otherwise
(`Views/Chat/DebugComponents.swift:19-23`, mounted at
`RequestDebugView.swift:187-193`) — printed the plaintext under the green
"encrypted" label. At 8ab468a the field is carried: set from the transport
at `Inference/ChatGeneration+Stream.swift:69` and preserved at `:184`;
`HTTPTransport.swift:298` is where the sealed body originates; `dd2d893`
pins it. What this was: the developer's own prompt, on the developer's own
screen, in developer mode, under the wrong caption — a claim-correctness
bug on the one surface whose job is to show what the wire saw, not a sink
(the wire was sealed: `HTTPTransport.swift:425-437` still fails closed). It
is **not** an item on the v1.0.4 page, which did not read this path; it is
a new fix, closed. The copy path (`RequestDebugView.swift:52-53`) still
copies the plaintext body (compacted for E2EE by `compactRequestBody`,
`:312-318`, which only shortens long hex), as it did before — carried.

**The search tool's citation ask.** `BraveWebSearchTool.swift:630` returns
the `<source>` XML plus `citationAsk` (`:633`), a fixed sentence asking the
model to cite with markdown links. It is appended to the tool *result*
that goes back to the model in the same turn, after the XML so
`parseSources` (`:486-497`) is unaffected. No new sink: the text already
flowed to the model; what is added is a constant. **Confirmed, no sink.**
The tools are otherwise unchanged: one fixed host, opt-in, no model-chosen
URL, no cross-thread read.

**"Turn off & retry" (`0a4df3c`).** Both handlers now call
`llm.declineOffer(inThread:messageIDs:)` before retrying
(`ConversationView.swift:542`, `:1077`); the method
(`Inference/ChatGeneration+SearchOffer.swift:27-32`) inserts the thread id
into a set and clears the pending offer so the keyless `web_search` schema
is not attached to the retry. State in memory; the retry goes through
`onRetry`, the same path as above. **UI, no sink.** The one-glide changes
(`FollowGlide.swift:43-50`, `TranscriptCollectionView.swift:345-352`,
`:382-388`) are scroll geometry; the `StreamTrace.event` added at
`TranscriptCollectionView.swift:447-451` is inside `#if DEBUG` and carries
offsets. **No sink.**

**The LiteRT turn lifecycle — the four lines the brief named.**
`LiteRTTransport.swift:228` logs `took.description` — a `Duration` — with
`privacy: .public`; `:706` logs a boolean with `.public`; `:728-734` logs
five numbers with `.public`; all three are unchanged lines that the sweep
re-fingerprinted because their neighbours changed. The new `DiagLog.note`
at `:707` adds `chars=\(answer.count)` — a count; `:715` is a fixed string.
`DiagLog` (`Inference/LocalRuntime.swift:220-227`) writes to stderr only
when `TEEMOON_NATIVE_LOG=1`, the same environment gate as the stderr
redirect to `Documents/native.log` (`App/teemoonApp.swift:30-36`) that the
base page carries as a residual; every `DiagLog.note` in the tree was
listed and read — reasons, counts, flags, model ids, file names, never a
body. `cacheDir: FileManager.default.temporaryDirectory.path` (`:212`) is
also an unchanged line; the wrapper documents it as "the directory for
placing cache files", defaulting to the model's own directory
(`Packages/LiteRTLM/Sources/LiteRTLM/Config.swift:57-59`, `:75-76`), and
the C header says no more (`engine.h`, `litert_lm_engine_settings_set_cache_dir`).
What the native engine writes there is a property of the binary and is
recorded under *not traced*; `tmp` is outside backups and inside the
container. **No new sink.**

**The renderer.** `blockingRemoteTranscriptAttachments()` is still
installed at the two SwiftUI roots, `ConversationView.swift:141` and `:812`
(moved from `:805` by the item-policy change), and the parse-level image
strip is still unconditional (`Views/Chat/MarkdownParseCache.swift:52`,
`:68`). The tail-card host is now `TranscriptCollectionView.swift:1257`
(moved from `:1240`), mounted by `setTailCard` (`:1242`), and what it hosts
is still fixed at `ConversationView.swift:973-981`: the debug card or the
error card, neither of which renders markdown. **Unchanged.**

**Logs on the reply path.** The three unfenced statements of the base
page's LOW are still there, unfenced and without a privacy level:
`Inference/ChatGeneration.swift:358`, `Inference/GenerationEngine.swift:394`
(moved from `:392` by two added lines) and `:307`. No new statement
interpolates a body, prompt or key: every `logger.*` line in the diff was
read (listed above), and the sweep's 301 CARRIED log rows were skimmed
against that question. **Unchanged — the LOW carries.**

**Data changes.** The Fireworks preset's default model string
(`Providers/Provider+Presets.swift:71`) is sent as the `model` field of a
request to the same endpoint (`:68`, unchanged — the sweep's NEW row there
is a re-fingerprint of an unchanged line). `KnownModel.fireworksPrices`
(`:343`) is read only by `FireworksAdapter.swift:148`, `:150`, `:160` to
fill the browser's price column; `ListPriceSnapshot.prices` only by
`EndpointModelCatalog.swift:193`. Both tables are string-to-string literals;
the regenerated snapshot's diff is price strings and model ids and was read
whole. **Data; no sink.**

### Build configuration

`Package.resolved` (`f9bff56`), `teemoon/Info.plist` (`0ffa0bd`),
`teemoon/teemoon.entitlements` (`80486f2`) and `PrivacyInfo.xcprivacy`
(`cc092a8`) are the same blobs as at e4df0e2 (and as at 3abe3e2 per the
base page). `project.pbxproj` changes are the version and build number at
`:546`, `:569`, `:594`, `:617` and the test bundles' version lines. Still
one application target (`:182-207`) plus two test bundles;
`TARGETED_DEVICE_FAMILY = 1` (`:583`, `:633`). `DEBUG` is set only for
Debug (`:465-468`, `:479`); the Release configuration (`:485-536`) sets no
compilation condition. `Packages/LiteRTLM/Package.swift:50-54` names the
same remote binary target — LiteRT-LM v0.17.1, SwiftPM checksum
`c94fc12aa0403cb47208e419cc3bfe258214ea17035f7a63c16de536869f2186` — as at
1.0.4; the file's diff is comments. The macOS slice at `:103-106` is a local
artifact whose tree id is unchanged (`e162e66`). **Clean; no new binary.**

### Sweep adjudication — the 24 NEW rows

| Rows | What they are | Reachable in Release? |
|---|---|---|
| `ContentView.swift:218`, `:272`, `:297` | `[uitest]` `os_log` lines: endpoint and model name, fixed strings | no — `#if DEBUG` (`:125-299`) and `--uitesting` |
| `ContentView.swift:295` | `Keychain.delete(for: "brave-grounding")` on a keyless test launch | no — same fence, condition at `:289` |
| `UITestSetupSeed.swift:77`, `:90`, `:104`, `:106`, `:113`, `:119` | `[uitest]` `os_log` lines: preset names, repo ids, counts | no — whole file `#if DEBUG` (`:41-124`) |
| `teemoonApp.swift:134-135` | stand-in weights file, eight bytes | no — `#if DEBUG` (`:117`) and `#if targetEnvironment(simulator)` (`:128`) |
| `teemoonApp.swift:269`, `:271`, `:276`, `:287` | planted config under `temporaryDirectory`, its `os_log` of kind and path | no — `#if DEBUG` (`:257-290`), `--uitesting` + `UITEST_SEED_CONFIG` (`:268`) |
| `BraveWebSearchTool.swift:526` | the loopback-prefix override | no — `#if DEBUG` (`:522-529`) and `--uitesting` |
| `BraveWebSearchTool.swift:530` | the real Brave endpoint, unchanged text | yes — the 1.0.4 host |
| `LiteRTTransport.swift:185`, `:212`, `:228`, `:706`, `:728` | unchanged lines re-fingerprinted by changed neighbours: a file-exists check, the cache directory, three numeric/boolean log lines with `privacy: .public` | yes — as at 1.0.4, no body |
| `Provider+Presets.swift:68` | the Fireworks endpoint, unchanged text, re-fingerprinted by the model line | yes — as at 1.0.4 |

Nothing in the 24 is a sink the App Store build can execute that it could
not at 1.0.4. The 808 CARRIED rows were skimmed in full — net, log, store,
pasteboard, render and entry kinds — for a line that interpolates a body or
a key; the hits are the three statements of the carried LOW and the
previews, demo and vendor-example lines the base page already excludes.

### Prior claims re-verified (line numbers at `8ab468a`)

| Claim on the 1.0.4 page | Now at | Status |
|---|---|---|
| `disable()` deletes the four default-store files, then swaps the zero cache; first statement of `init` | `Support/SharedURLCache.swift:20-23`, `:34-38`; `App/teemoonApp.swift:40` | unchanged |
| First `URLSession.shared` access is `ConfidentialSession(providers:)`; nothing new runs ahead of the init | `teemoonApp.swift:79`; the new `#if DEBUG` store selection at `:73-78` runs after the swap | unchanged |
| Seventeen authenticated sites, each to its own provider | table above | **seventeen**, unchanged; Brave search call at `:582` |
| Catalogue scope hash; `forget(endpoint:)` has no caller | `Providers/LiveCatalogStore.swift:208-212`; `:171-178`, no caller (grep) | unchanged — **INFO carries** |
| `Keychain.deleteAll()` only from `#if DEBUG` | `Providers/Keychain.swift:105-114`; `teemoonApp.swift:65` in `:42-67` | unchanged |
| UI-test seeding `#if DEBUG` | `ContentView.swift:125-299`; `UITestSetupSeed.swift:41-124`; `UITestHostSecrets.swift:16-115` | unchanged — **more of it**, same fence |
| Three unfenced log statements carry reply text / tool arguments | `Inference/ChatGeneration.swift:358`; `GenerationEngine.swift:394`, `:307` | unchanged — **LOW carries** |
| LOW: system prompt in UserDefaults | `Settings/AppSettings.swift:28`, `:32` | unchanged — **LOW carries** |
| Chat request on an ephemeral session; TLS probe carries no credential | `Inference/ConfidentialLanguageModel.swift:111-113`; `Confidential/TLSAttestationVerifier.swift:85` | unchanged |
| Single send-authorization definition, re-read after prepare | `Confidential/ConfidentialSession+Verdict.swift:252`; `Chat/ChatViewModel.swift:269-280` (moved from `:263`) | unchanged; **one more caller**, the background re-ask, goes through it |
| Siri refuses on a pending verdict | `App/RequestLLMIntent.swift:87-90` | unchanged |
| Loader at both SwiftUI roots; tail card without it hosts no markdown | `ConversationView.swift:141`, `:812`; `TranscriptCollectionView.swift:1257`; `ConversationView.swift:973-981` | unchanged (lines moved) |
| Image strip unconditional | `Views/Chat/MarkdownParseCache.swift:52`, `:68` | unchanged |
| Keychain class, not synchronizable | `Keychain.swift:49`, `:61` | unchanged |
| Self-verify script reads the key from the environment | `Confidential/SelfVerifyScript.swift:155` | unchanged |
| `captureNativeLogIfAsked` env-gated, not DEBUG-fenced | `teemoonApp.swift:30-36`, called `:41`; `DiagLog` at `Inference/LocalRuntime.swift:220-227` on the same variable | unchanged residual |
| OpenRouter and NVIDIA never presented as attested | `Providers/Provider.swift:290-292` (moved from `:285-287`) | unchanged |
| near.ai directory host must be `https` and `*.near.ai` | `Providers/EndpointDirectory.swift:112-130` | unchanged |
| Web search: one fixed host, opt-in | `BraveWebSearchTool.swift:530` | unchanged in Release; DEBUG override above |
| Runtime binary: same pin, capability check stands | `Packages/LiteRTLM/Package.swift:50-54` | unchanged — same checksum, not redone |
| No analytics / crash SDK; config files unchanged | same blobs | unchanged |

**Hand-off items of the v1.0.4 page, at 8ab468a.** The base page's three
findings each carry a remediation; none is done:

1. *Log counts and lengths, not content* (LOW) — **open**:
   `ChatGeneration.swift:358`, `GenerationEngine.swift:394`, `:307`
   unchanged.
2. *System prompt out of UserDefaults* (LOW) — **open**:
   `AppSettings.swift:28`, `:32` unchanged.
3. *Call `forget(endpoint:)` on key removal; salt the scope* (INFO) —
   **open**: `LiveCatalogStore.swift:171` still uncalled, `:208-212`
   unsalted.

`8618ac2`, titled "fix: the 1.0.4 audit's three cheap findings", is not
about this page: its message and diff are a product review's three items —
the not-encrypted sheet's CTA re-reading the key state when its form
closes (`TrustLadderView+None.swift:258`, `:273-275`), the transcript item
policy computed once per body pass (`ConversationView.swift:826-831`), and
`ModelDetailView`'s one-fetch guard (`ModelDetailView.swift:52-55`,
`:214-215`). The name collision is worth a line in the developer notes so
nobody reads it as closing the exfiltration findings. Two fixes in this
build close things no page had raised: the E2EE card (`7ca0b46`) and the
host classification (`e1f8636`).

### Not traced (explicit)

- The on-device runtime binary: the same bytes as at 1.0.4 by package pin
  and checksum; the capability check was not redone and what the engine
  writes under `cacheDir` (`LiteRTTransport.swift:212`) is not known from
  the wrapper's documentation.
- Upstream LiteRT-LM source at v0.17.1.
- Large view files in the diff (`TranscriptCollectionView`, `ConversationView`,
  `TrustLadderView*`, `ModelDetailView`, `WhereChip`) were read at their
  hunks and at the lines the base page cites, not line by line; the
  streaming host at `TranscriptCollectionView.swift:1193` was not re-read
  for the loader question (unchanged since 1.0.4).
- `Vendor/textual` internals beyond the loader and parser entry points.
- Whether `URLSession` forwards `Authorization` across a cross-host
  redirect; not new, no page has traced it.
- The developer's archive figures in the binding row; the orchestrator's
  binary check.
- Anything at run time: this is a static read. No runtime measurement is
  claimed here.
- A phone.

## Runtime

### The archive, checked (orchestrator, 2026-10-15)

`~/teemoon-backups/release-1.0.5-39/teemoon-b39.xcarchive.zip` hashes to
`44a5eac849ed26da4552131f543fdee39b2bc986df379266e73ee49839e2fc47` (the
developer's figure); inside the archive `Products/Applications/teemoon.app/teemoon`
hashes to `92b1620e2751b336b6fa9214dd6d98e63f064509504c5579b65bbec3b9896df6`
with arm64 UUID `DA109A19-7AAA-3D78-9FFD-292079527711` (both the developer's
figures); `Info.plist` reads `CFBundleVersion 39`, `CFBundleShortVersionString
1.0.5`, `ai.teemoon.app`; `codesign -dv` names team `4786V39YGH`; the
archive's own `Info.plist` records scheme `teemoon`, created 2026-10-15
14:09:30. What this binds: the bytes on disk are the bytes the developer
uploaded (their copy, their hash, recomputed here). What it does not: no
rebuild was attempted (code signatures and timestamps make a byte-identical
rebuild impossible by the developer's own account), so the archive's
provenance from `8ab468a` rests on the developer's statement of a clean
worktree — as on every iOS page.

### Runtime pass (method §4b) — 2026-10-15, build 39

Built from source at `8ab468a` (`xcodebuild build-for-testing`, Xcode 26.6,
iOS 26.5 simulator `audit-1.0.5` created for this pass, Debug configuration
— so the `#if DEBUG` test surfaces above ARE compiled in this binary; the
shipped Release binary lacks them). Sockets polled once a second (`lsof`),
the unified log streamed **at debug level** throughout, the Keychain
attributes and the container read afterwards; the seven host key files'
bytes searched for (UTF-8 and UTF-16, never printed).

**Sessions.** The offline product suite `ProductE2ETests` (23 tests, all
passed, 503 s) and the live near.ai suite `ProductLiveE2ETests` (5 tests,
all passed, 301 s — the first fully green live run on this lineage; the
pinned model `z-ai/glm-5.3-flash` is served).

| Measurement | Result |
|---|---|
| **Egress** — every remote endpoint the process opened | 20 addresses, every one attributed to a host the exits table names: `cloud-api.near.ai` / `completions.near.ai` / the model host (`40.160.1.150`, `160.72.54.150`, forward-resolved), `raw.githubusercontent.com` (`185.199.108.133`), `api.github.com` (three GitHub load balancers `140.82.112-114.6`), `nras.attestation.nvidia.com` (`34.120.45.54`), `api.trustedservices.intel.com` (`4.255.75.174`), `certificates.trustedservices.intel.com` (five CloudFront edges `3.167.69.8/69/118/119`, `3.167.112.45` — each answers `curl --resolve` as that host under its certificate), `openrouter.ai` (`104.18.3.115`), `api.x.ai` (`104.18.19.80`), `api.fireworks.ai` (`13.57.174.69`), `integrate.api.nvidia.com` (`75.2.113.119`), `api.search.brave.com` (`3.33.153.106`). Two Ollama endpoints are the harness's own: `127.0.0.1:11434` (the UI tests' embedded fake server, with five more loopback ports for its other fakes) and `100.96.112.39:11434`, the developer's home server over Tailscale, which `ProductE2ESupport.swift:149` names as the default `TEEMOON_OLLAMA_ENDPOINT` — a user-chosen send path, keyless. No other address. |
| **Logs** — a credential in any line | 5.31 million lines (790 MB); **0** contain any of the seven key values; three lines contain the word `Bearer`, all three the self-verify script's template text (`headers["authorization"] = f"Bearer {api_key}"`) in the generated script and its accessibility value — no token. |
| **Logs** — message text in an app-originated line | **21 lines** in `ai.teemoon` categories: 17 `output='<first 120 characters of the reply>'` (`ChatGeneration.swift:358`) and 4 `[ToolCall] … args=` (`GenerationEngine.swift:394`) — the carried LOW, observed again in clear; 0 `<private>` markers (the simulator renders private interpolations). |
| **Keychain** | 1 item in access group `4786V39YGH.ai.teemoon.app`, `pdmn = ck` (AfterFirstUnlock), `sync = 0` — the near.ai key the live suite seeded; the other rows are the system's. |
| **Container** | 18 files. **No URL cache file**: `Library/Caches/ai.teemoon.app/` holds only Metal's four shader-cache files (the 1.0.3 fix holds). The key values: in no file. `Application Support/ModelLists/<64-hex>.json` present — the carried INFO (its name a truncated key hash, its content the catalogue). `Documents/scrolltrace.log` — the one-glide work's scroll trace, written by `ScrollTrace.swift` inside `#if DEBUG` (`TranscriptCollectionView.swift:447-451`): numbers and view names, absent from a Release build. The rest is the system's (preferences plist, saved state, snapshots, HTTP storages with no key bytes, binary cookies, a pasteboard temp file). |

Not measured: a phone; the Release binary's behaviour (the `#if DEBUG`
surfaces are a source claim fenced by the project's configuration, read on
this page; the archive above is the Release binary and was not run); the
store at rest (the harness runs an in-memory store); an on-device-model
session (no bundle on the simulator), so the LiteRT changes — the
backgrounded re-ask, the engine's `cacheDir` under `tmp/` — are static
results only; a keyed send through Fireworks on `kimi-k3`.

**Second-reviewer agreement.** The other reviewer, blinded to this page,
reached QUALIFIED-PASS with no finding in the delta, the same fence reading
(DEBUG only in the project's Debug configuration, every seeding and override
path behind it and a launch argument), the same card and copy reading, the
same account of `e1f8636` (a trust-label correction, no key-destination
change) and `7ca0b46` (a new fix for a display no page had raised), the same
carried LOWs and INFO open, and the same developer notes; it adds that the
Brave override's `hasPrefix` also admits `http://127.0.0.1:8080@evil.example/v1`
(host `evil.example`), that the E2EE copy path still pastes the pre-seal body,
and that `UITestSetupSeed`'s comment "cannot replace anyone's real
configuration" is true of the store but not of the Keychain it writes under
the preset's endpoint — all DEBUG-only.


### Addendum — build 42: `8ab468a` → `719ea1c` (2026-10-15, one blinded reviewer plus the orchestrator)

Four shipped commits and three test files; `project.pbxproj` differs by
`CURRENT_PROJECT_VERSION` 39 → 42 only; `Package.resolved`, `Info.plist`,
the entitlements, `PrivacyInfo`, the vendored `ModelBackend`,
`TDXQuoteVerifier` and `LiteRTLM` artifacts are the same blobs as at
`8ab468a`; the LiteRT-LM checksum (`Packages/LiteRTLM/Package.swift:53`)
unchanged; `DEBUG` still defined only in the project's Debug configuration.
The sweep at `719ea1c`: 26 NEW rows against 24 — the Brave `hasPrefix`
literal gone, the three re-marked log lines and the unchanged Brave constant
re-fingerprinted; the five LiteRT rows at shifted lines.

- **`e1a6d74` — the wait loop** (`LiteRTTransport.swift:94-103` adds
  `WaitStep`/`waitStep`; loop `:666-699`; post-loop throw `:730-733` now
  requires `abandoned && backgrounded`). A finished answer is collected
  before background-or-dead abandons; the two exits existed before and lead
  where the 39 body traced them (`.collect` → the normal reply outcome;
  `.abandon` → the shown partial and `CancellationError` → the re-ask path
  through the send gate). One fewer send for an answer that finished as the
  app left the foreground; text moves nowhere new. Closes developer note 2.
  Pinned by `LiteRTTurnWaitTests` (the pure truth table, four cases; the
  loop's wiring is covered by the device test only).
- **`e5adc2e` — the three log statements** (`ChatGeneration.swift:358`,
  `GenerationEngine.swift:307`, `:394`, same line numbers) now interpolate
  the reply, the stripped fragments and the tool arguments with
  `privacy: .private` (`.public` on the count and the tool name). **The
  carried LOW stays OPEN, narrowed:** the method counts a log line that can
  carry a body as a finding at any privacy level (the 1.0.4 finding's own
  words), the text is still interpolated into the same three unfenced
  statements at the same levels, and a `Logger` interpolation of a dynamic
  string was already private by default — a phone's observable behaviour is
  identical to 39. What changed: the redaction is now the app's explicit
  decision, pinned by `LogPrivacyTests` (which reads every single-line
  `logger.*` call for eight content-bearing names without the mark). The
  reviewer's own grep over every logger interpolation in `teemoon/` and the
  two vendored packages found no other line carrying user or model text,
  and nothing content-bearing marked `.public`. The base remediation
  (counts or lengths instead of the text; or `#if DEBUG` and drop the
  fragment) still closes it.
- **`e5adc2e` — the Brave test override** now goes through
  `BraveWebSearchTool.isLoopbackOverride` (`:535-539`: `URLComponents`,
  scheme `http`, host `127.0.0.1`, a port, no user, no password); the call
  at `:526` stays inside `#if DEBUG` behind `--uitesting`, so Release returns
  the constant at `:530` and the function ships uncalled. Closes developer
  note 1. Pinned by `LogPrivacyTests` on the function (six cases, the
  `http://127.0.0.1:1@evil/` shape among them); the call site is not.
- **`5d2fb66` — the Fireworks migration**
  (`ProviderStore+Healing.swift:342-366`, called from `ProviderStore.init`'s
  load at `ProviderStore.swift:337` when the load succeeded): for every
  saved place whose `openAIBaseURL` host resolves to Fireworks
  (`fireworks.ai` or `*.fireworks.ai`, `FireworksAdapter.swift:40-43`), the
  retired `accounts/fireworks/models/kimi-k2p6` becomes `…/kimi-k3` in
  `model` (`:349`) and in `equippedModels` (`:350-354`, de-duplicated) — and
  nothing else: the record is updated only when the copy differs (`:355`),
  through `updateProvider` → `providers.didSet` → `save()` → the
  credential-free config JSON. No network call of its own; the next
  Fireworks request is the user's next send to the unchanged endpoint with
  the new id in the body. No Keychain call; keys are addressed by endpoint
  (`ProviderStore+Credentials.swift:34-41`), which does not change. Runs on
  the main actor, synchronously, once per load, and is idempotent (after
  the move nothing matches the retired id). The notice (`:325-328`: display
  names plus two price strings) is appended to `mergeNotice`
  (`ProviderStore.swift:80`), in memory only, shown by the Where sheet
  until dismissed, never persisted or logged — one-time because the moved
  record is. Pinned by `RetiredFireworksModelHealingTests`
  (`ProviderTests.swift:499-554`: the move, the equipped-only move, the
  de-dup, the exact notice, other-model and other-provider no-ops, every
  successor priced and every retired id gone from the price table);
  unpinned: the call site and its `loadFailure` guard. Two product notes:
  the de-dup also collapses unrelated duplicates in a Fireworks equipped
  list, silently; and `RequestLLMIntent` (Siri) builds its own persisting
  store, so a user whose first post-update turn is through Siri is migrated
  without ever seeing the price notice.

**Archive, checked (orchestrator).** `~/teemoon-backups/release-1.0.5-42/teemoon-b42.xcarchive.zip`
hashes to `c5f0ed452d19349ab68387f0ee085b12b8f02b394007c34412001fec580bde94`;
`Products/Applications/teemoon.app/teemoon` to
`90ea48b359e8810cc3e83b072a75bdb5de25d818144d42961151caea5bb8ce48`, arm64
UUID `F2780D6B-9A0B-361C-9E8C-AC09B073C190`; `CFBundleVersion 42`,
`1.0.5`, `ai.teemoon.app`, team `4786V39YGH`, created 2026-10-15 15:40:18 —
all the developer's figures, recomputed here. Same binding and the same
limits as the build-39 archive above.

**Measurements at `719ea1c` (orchestrator).** Built for testing on the audit
simulator; the unit target 1,730 tests in 258 suites green (the three new
suites 11/11 among them). Mutation checks, each restored to green: the
background check put back above the finished check in `waitStep` →
`LiteRTTurnWaitTests` 2 issues; the `.private` mark dropped at
`GenerationEngine.swift:394` → `LogPrivacyTests` red naming that line;
`isLoopbackOverride` reverted to the prefix check → the
`http://127.0.0.1:1@evil/` expectation red; the migration's successor
swapped for the retired id → `RetiredFireworksModelHealingTests` red at the
moved model. Runtime pass (same method as build 39's above):
`ProductE2ETests` 23/23, `ProductLiveE2ETests` 5/5; every remote address
attributed — the build-39 set plus one more Fireworks edge (`35.207.52.96`,
which answers `curl --resolve` as `api.fireworks.ai` under its certificate)
and GitHub's third load balancer; the log stream (5.32 M lines) held no key
byte and three `Bearer` template lines as before; **17 `output='` lines and
4 `[ToolCall] args=` lines still carried the text in clear** — the
simulator renders private interpolations, which is the measurement behind
"narrowed, not closed" above; the container (71 files, because the unit
target had run in the same container) held no key byte.

### Addendum — build 43: `719ea1c` → `705764b` (2026-10-15, orchestrator)

Two commits: `f742cc7` and the version bump (`CURRENT_PROJECT_VERSION` 43,
the pbxproj's only change). Seven files; under `teemoon/` four.

- **The three log statements, closed.** `ChatGeneration.swift:358` now
  logs `output \(self.output.count, privacy: .public) chars`;
  `GenerationEngine.swift:307` the fragment count and the summed fragment
  length (`removedMarkup.reduce(0) { $0 + $1.count }`), the joined
  fragments gone; `:394` `args \(tc.arguments.count, privacy: .public)
  chars`. Counts and lengths, no body text at any level — the base
  remediation. `LogPrivacyTests` no longer exempts `.private`: any
  interpolation naming a content-bearing variable fails it. **The carried
  LOW "reply text and model-written tool arguments are interpolated into
  unfenced log statements" is CLOSED at `705764b`** — see Findings.
- **The Fireworks notice survives a Siri-first launch.**
  `healRetiredFireworksModels` also writes the joined notice to
  `teemoon-pending-notice.txt` beside `teemoon-config.json` in the app's
  Application Support directory (`ProviderStore+Healing.swift`:
  `pendingNoticeURL`, `readPendingNotice`, `writePendingNotice`,
  `joinNotices`; nothing on disk for an in-memory config); `ProviderStore`'s
  load joins the file's text into `mergeNotice` after the heals, never
  repeating text already there; `dismissMergeNotice()` now also removes the
  file. The file holds the notice text only — two display names and two
  price strings — no key, no message, no path. Its write is
  `Data.write(to:options: .atomic)` without the explicit
  `.completeFileProtectionUntilFirstUserAuthentication` the config write
  carries (`ConfigStore.swift:457`): it takes the container's default
  class, and like the config beside it carries no backup exclusion
  (developer note; the content makes it no finding). Pinned by
  `PendingHealNoticeTests` on a temp-directory config: a setup store, a
  "Siri" store that heals and persists, an "app" store that says the
  notice once and once again on reopen, nil after dismiss. Stated limit:
  an app process already running when the Siri intent heals shows the
  banner at its next launch, not on return to the foreground.
  The sweep at `705764b`: 28 NEW rows against 42's 26 — the two added are
  this file's read and write (`ProviderStore+Healing.swift:385`, `:387`,
  `store` kind), adjudicated above; nothing else moved.

**Archive, checked (orchestrator).** `~/teemoon-backups/release-1.0.5-43/teemoon-b43.xcarchive.zip`
hashes to `ca2f88acab864c9164f02c46dc7bd11222512681ebe76167bb5567dd9d0acf5e`;
`Products/Applications/teemoon.app/teemoon` to
`0668a91fd0c5795c2a920c143a4f3942a22ee68545cff4707c661a8578416447`, arm64
UUID `8562F860-CCFC-3C73-A846-431F4D3990F7`; `CFBundleVersion 43`,
`1.0.5`, `ai.teemoon.app`, team `4786V39YGH`, created 2026-10-15 16:12:04
— the developer's figures, recomputed here; same binding and the same
limits as the build-39 archive above.

**Measurements at `705764b` (orchestrator).** Built for testing on the
audit simulator (incrementally on the build-42 derived data, the worktree
moved to `705764b`, clean); the unit target 1,731 tests in 259 suites
green (the four new suites 12/12). Mutation checks, each restored to green:
the tool arguments put back into the `:394` statement with
`privacy: .private` → `LogPrivacyTests` red naming the line (the test now
rejects the mark); the load-time read of the pending notice dropped →
`PendingHealNoticeTests` red (the "app" store says nothing). Runtime pass
on an **erased** simulator (so the container below is this pass's alone):
`ProductE2ETests` 22/23 on the first run — the one red,
`testAddingAKeyFlipsTheEncryptedModelCTAWithoutReopeningTheSheet`, is a
5 s wait for the "who can read this?" sheet after a tap on the title block
(a case green on the 39 and 42 runs; the 42 → 43 delta touches no view) —
rerun alone on the same build it passed in 17.6 s (1/1), so 23 of 23 across the two runs; `ProductLiveE2ETests` 5/5. Every remote address attributed
(the near.ai hosts, `raw.githubusercontent.com`, `api.github.com`,
`nras.attestation.nvidia.com`, `api.trustedservices.intel.com`, the
certificate host's CloudFront edges now also at `18.161.34.25/.53`, which
the host resolves to, `openrouter.ai`; the embedded fakes on loopback). The
log stream (5.20 M lines): **0 `output='` lines**; the six `[ToolCall]`
lines read `'web_search' args 28 chars` / `62 chars` and `executing 1 tool
call(s)` — counts only; 0 `[containment]` lines fired; no key byte; the
three `Bearer` template lines as before. Keychain: the one app item,
`pdmn = ck`, `sync = 0`. Container: 18 files, the same set as build 39's —
no URL cache file, no key byte, no `teemoon-pending-notice.txt` (nothing
to heal on a fresh container; the file's lifecycle is the unit test's
measurement).

### Findings

No finding new at this release at any severity. The three findings of the
v1.0.4 page carry, re-read at their 8ab468a lines:

### LOW (deployed: yes — since 1.0; carried at builds 39–42; **CLOSED at build 43**, `f742cc7`) — reply text and model-written tool arguments were interpolated into unfenced log statements

Unchanged. `Inference/ChatGeneration.swift:358` (debug level, the first 120
characters of every finished reply); `Inference/GenerationEngine.swift:394`
(debug level, the JSON arguments of every tool call — for web search a
query the model wrote from the user's prompt); `GenerationEngine.swift:307`
(warning level, up to four fragments of reply text stripped as residual
tool markup). None inside `#if DEBUG`, none with an explicit privacy level.
The platform's defaults — private interpolation rendered `<private>`
without a profile, debug level unpersisted — stand between these lines and
a reader, not the app's code. **Remediation** as on the base page: log
counts and lengths, or fence the two debug lines and drop the fragment
from the warning. Not addressed at builds 39–42 (build 41 added
`privacy: .private` marks, which narrowed the rationale without closing the
finding). **Closed at build 43** (`f742cc7`): all three statements log
counts and lengths only — `output N chars`, the fragment count and summed
length, `args N chars` — with no body text at any level; `LogPrivacyTests`
rejects any interpolation of a content-bearing name regardless of privacy
mark, and reverting `:394` to the marked text turns it red; the build-43
runtime log stream carried 0 `output='` lines and `[ToolCall]` lines of the
form `'web_search' args 28 chars` (second addendum).

### LOW (deployed: yes — since 1.0, carried) — the user-edited system prompt is stored in UserDefaults, outside the protected store and inside backups

Unchanged. `Settings/AppSettings.swift:28`, `:32`. **Remediation** as on the
base page. Not addressed by this build. **Waiver, relayed:** on 2026-10-15 the
release coordinator session relayed the user's decision not to fix this item
("That's not user plain text"). The finding keeps its class on this page — the
method counts the prompt the user edits as their text, and the storage is
unchanged — and the waiver is recorded as a product decision taken outside
this audit session, to be confirmed by the user to the auditor directly.

### INFO (deployed: yes — since 1.0.4, carried) — a truncated hash of a keyed provider's API key is written to a catalogue file and is never removed

Unchanged. `Providers/LiveCatalogStore.swift:208-212` derives `key-` plus
sixteen hex digits of an unsalted SHA-256 of the key as the list's scope;
`forget(endpoint:)` (`:171-178`) still has no caller; provider deletion
(`Providers/ProviderStore.swift:188-189`) still deletes the Keychain items
and not the list. **Remediation** as on the base page. Not addressed by
this build.

### Residuals — by design, stated not hidden

Carried from the base page: opt-in web search is content-driven egress to
one fixed host; provider keys restore via encrypted backup; an unattested
provider reads plaintext by definition; user-initiated copies — including
the developer card's "Copy Debug Info", which carries the request body and
reply to the general pasteboard on a tap — go to the general pasteboard;
E2EE metadata is plaintext by protocol; a no-tap re-send after
backgrounding goes through the gate; a developer-only stderr capture ships
env-gated in the release binary (`TEEMOON_NATIVE_LOG`, now also the gate
for `DiagLog`, whose lines are counts and flags); the cache fix is one
silent mechanism; `Keychain.deleteAll()` ships compiled. New or changed at
this release:

- **The background re-ask now reaches on-device turns.** An on-device turn
  cut off by backgrounding is asked again on return without a tap
  (`ChatView.swift:694-699`), through the gate, to the same provider; a
  turn that finished inside the 100 ms window is asked twice.
- **More `--uitesting` doors in the Debug build.** The seeder reads
  provider keys from files on the developer's host and writes the
  Keychain; a keyless test launch deletes the Brave slot and empties every
  unseeded preset slot; the Brave endpoint accepts a loopback-prefixed
  override whose prefix check a credential-shaped URL can defeat. Every
  one is `#if DEBUG` and argument-gated; none exists in the App Store
  binary. Running a Debug `--uitesting` build against a real Keychain is a
  developer-process risk, not a user's.
- **The developer card's E2EE row** now shows both bodies for a finished
  turn (`DebugComponents.swift:19-23`); its copy still carries the
  pre-seal plaintext (`RequestDebugView.swift:52-53`), under the
  developer's own tap.

### Controls that would change the verdict

- `DEBUG` added to the Release configuration's compilation conditions, or
  any of the `--uitesting` doors (`ContentView.swift:125-299`,
  `teemoonApp.swift:42-67`, `:117-138`, `:257-290`,
  `BraveWebSearchTool.swift:522-529`, `UITestSetupSeed.swift`,
  `UITestHostSecrets.swift`) moved outside `#if DEBUG` or off the launch
  argument.
- `UITestHostSecrets` reading a key from the process environment, or a
  seeder writing a key anywhere but the Keychain.
- The Brave endpoint override accepting anything but a parsed host of
  `127.0.0.1`, if it ever leaves `#if DEBUG`.
- A re-ask path that does not go through `retry(from:)` and the gate, or
  that sends to a provider other than the thread's active one.
- `OnDeviceRun` or `EngineTimings` gaining a text field, or the speed row
  reading anything but numbers and a backend word.
- Any `DiagLog.note` or `logger.*` line interpolating a body, prompt or
  key; any of the three carried log statements gaining `privacy: .public`
  or a persisted level.
- `isPrivateHost` losing the label-count guard (`Provider.swift:123`); the
  pinned test suite removed.
- Any session created before `TeemoonApp.init`, any configuration setting
  its own `urlCache`, any later assignment of `URLCache.shared`.
- A markdown or image view placed in the tail-card root
  (`TranscriptCollectionView.swift:1257`) without the non-fetching loader.
- An adapter that builds a request from anything but the provider's own
  base URL, or a background catalogue refresh that starts passing a key.
- A caller for `Keychain.deleteAll()` outside `#if DEBUG`.
- A model-callable tool that fetches a model-chosen URL or reads other
  threads.
- A changed `Packages/LiteRTLM/Package.swift` checksum, or a dependency
  added to `Package.resolved` with its own network client.

### Verdict: QUALIFIED-PASS

Keys: at `8ab468a` a provider key lives in the Keychain and nowhere else
on disk, and leaves only in a request to the endpoint it was saved with —
the same seventeen sites as at 1.0.4, each re-read; the one new surface
that reads keys, the UI-test setup seeder, reads them from files on a
developer's Mac into an in-memory test configuration and is compiled out
of the Release configuration together with every other `--uitesting` door,
including a Brave endpoint override whose prefix check would otherwise be
weak. The host-classification fix removes a false "on your own machine"
claim for attacker-registered hostnames without ever having moved a key
off its endpoint. Messages: the send gate is still one definition and now
also governs the on-device background re-ask; the renderer fetches
nothing; the developer card's new figures are numbers and a word, and a
finished E2EE turn's card now shows the sealed body it had been dropping;
the search tool's new suffix is a constant. Of the v1.0.4 page's two LOWs and INFO, at `8ab468a` all three were still
open — the commit named for "the 1.0.4 audit's three cheap findings" closes
a product review's items; at `705764b` (build 43) the log LOW is closed by
counts-and-lengths logging, the system-prompt LOW stays open under the
user's waiver as relayed, the INFO carries — and no new finding at any
severity was found in any of the six commits since. The on-device runtime binary is the
same pin as at 1.0.4 and was not re-checked; what it writes under its
cache directory, and the app on a phone, remain unobserved. The runtime
pass and binary binding are the orchestrator's.

**Developer notes (not findings):**

1. `Inference/BraveWebSearchTool.swift:526` — `hasPrefix("http://127.0.0.1:")`
   accepts `http://127.0.0.1:1@evil/`, which Foundation parses as host
   `evil`. Parse the override and require `host == "127.0.0.1"` before
   trusting it; DEBUG-only today, so a hygiene note.
2. `Inference/LiteRTTransport.swift:659` vs `:670` — the wait loop tests
   `backgrounded || dead` before `finished`, so an answer that completed
   during the 100 ms sleep at the moment of backgrounding is thrown at
   `:716` and re-asked. Check `finished` first, or skip the throw when the
   consumer completed.
3. `8618ac2`'s title says "the 1.0.4 audit's three cheap findings"; those
   are the product review's. This audit's three remain open:
   `ChatGeneration.swift:358`, `GenerationEngine.swift:394`, `:307`;
   `AppSettings.swift:28`, `:32`; `LiveCatalogStore.swift:171` uncalled.
4. `Views/Chat/RequestDebugView.swift:52-53` — the copy of an E2EE turn's
   card carries the pre-seal plaintext body while the screen now shows
   both; consider copying the sealed body alongside it, or captioning the
   copied block as plaintext.
