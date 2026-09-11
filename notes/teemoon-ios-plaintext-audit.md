> **teemoonai/audits** — the teemoon iPhone client, key and plaintext exfiltration review.
> (The filename predates the key axis and is frozen because published pages link it.)
> This path is the stable entry point linked from published pages; the client
> side now has the same shape as the server side and lives under
> [`/client/`](/client/README.md). Method: [`/client/method.md`](/client/method.md)
> · Map: [`/client/ARCHITECTURE.md`](/client/ARCHITECTURE.md) · Surface:
> [`/client/audit-surface.md`](/client/audit-surface.md).

# teemoon iPhone client — can anything exfiltrate your keys or your plaintext?

## verdict: QUALIFIED-PASS — keys: they leave the device only to their own provider, but running the app found the near.ai key at rest in cleartext in the shared URL cache on disk (MEDIUM, since 1.0, fixed in 1.0.3); messages: they reach only the send path you chose and the protected store, at App Store 1.0.2 (`21d534e`) and every release since 1.0, with the user-edited system prompt in UserDefaults inside backups (LOW); one HIGH fixed before the 1.0 publish; the on-device runtime is shown unable to reach the network, its file writes are not traced

The rest of this repo audits near.ai's side of end-to-end encryption: given
that plaintext exists in the model CVM, can any attested server component copy
it somewhere the operator or a third party can read? The client tree asks the
same single question of the **other** end — the device. The app composes every
prompt and decrypts every reply, so it holds plaintext unconditionally (the
yellow `APP` box in the [server-side map](ARCHITECTURE.md)) — and it holds
your provider keys, which no server-side component does. Keys first: can your
provider API key reach anywhere but the Keychain and the provider it belongs
to? Then plaintext: does anything on the device copy it to a log, an
unprotected file, the pasteboard, or a network destination other than the
send path you chose — with no user action, or driven by content a hostile
model controls?

A client build carries no attested identity, so this is not a gated
`index.json` page and the app shows no audit link for it. The identity a page
can claim is the commit its release tag points at, and each page pins it.

## Release coverage

| App Store release | tag → commit | verdict | page |
|---|---|---|---|
| 1.0 (25) | `v1.0.0` → `2d9e206` | QUALIFIED-PASS — one HIGH fixed pre-publish; MEDIUM key-in-URL-cache (fixed in 1.0.3) and LOW system prompt found later, present here | [`v1.0.0-2d9e206.md`](/client/teemoon-ios/v1.0.0-2d9e206.md) |
| 1.0.1 (26) | `v1.0.1` → `0dfad8b` | QUALIFIED-PASS (carried) — zero app-code change from 1.0 | [`v1.0.1-0dfad8b.md`](/client/teemoon-ios/v1.0.1-0dfad8b.md) |
| 1.0.2 (33) | `v1.0.2` → `21d534e` | QUALIFIED-PASS — no new sink in the delta; runtime pass: no unlisted endpoint, but the near.ai key sits in the URL cache on disk (MEDIUM, fixed in 1.0.3) | [`v1.0.2-21d534e.md`](/client/teemoon-ios/v1.0.2-21d534e.md) |

A release with no row has not been reviewed; the same fail-closed rule this
repo applies to server images applies here. The lineage, with what each page
covers, is [`/client/README.md`](/client/README.md).

## What a reader should take away

- **Where plaintext is on the device, and where it may go:**
  [`/client/ARCHITECTURE.md`](/client/ARCHITECTURE.md) — the map, the hot path,
  and the per-hop answer table.
- **How to re-run the review yourself, and what the tag cannot prove:**
  [`/client/method.md`](/client/method.md) — threat model, pinned scope, the
  portable prompt, build-configuration checks, and the honest statement that
  nothing binds the App Store binary to the commit except the developer's word
  and your own build.
- **Where client findings have actually come from:**
  [`/client/audit-surface.md`](/client/audit-surface.md).
