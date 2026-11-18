# client page template

Every release page under `client/teemoon-ios/` and `client/teemoon-android/` follows this order. The top of the page is for someone who uses the app. The bottom is for someone who wants to check the work. Nothing is removed from the evidence to make the top shorter.

## Order

```
# <repo> @ <tag> (<full 40-character commit>) — <version> (<build>)

## verdict: <CLASS> — <one plain sentence>

## Summary
**What was checked.**   one short paragraph
**What was found.**     one short paragraph
**What was not checked.** one short paragraph
### Is my data safe?    two sentences

## What was found, in plain terms
### <the finding users should know about, first>
- What can happen / When / Does it affect you? / Planned fix
### <other findings>     the same four points each; a table when there are many minor ones

## How to check this yourself
the git ls-remote command for the tag, and the commit it should print

## Technical evidence
**Verdict as recorded.** the full verdict sentence
identity table · withdrawn-candidate history · what changed · traces ·
build configuration · sweep · prior claims · findings · residuals ·
not traced · controls · verdict · mutation checks · runtime
```

## Rules for the part above "Technical evidence"

1. **No commit ids and no internal terms** in the Summary or the plain-terms findings. Not "orchestrator", "sink sweep", "carried", "mutants", "H1–H5", "deployed: ON", or a severity code alone. Say "low severity" and "minor note". The commit appears in the title and in "How to check this yourself", where it is the point.
2. **Claim no more than the evidence shows.** "No way was found" is the claim, never "there is no way". Say that this is teemoon's own AI-assisted review. Say what was not checked in the third paragraph, in words a user understands (no physical phone, a test build, a library not read).
3. **End-to-end encryption means near.ai's attested secure enclaves only.** Do not let the phrase cover other providers, your own computer or the phone.
4. **Words come from the lexicon.** Check against `marketing/LEXICON.md` in teemoon-web (read it from `origin/main`): provider, model, the operator, attested, secure enclave, "sealed so only the model can read it", near.ai in lowercase. Never "impossible", "zero-trust", "the only provider", or a blanket "nothing leaves your device".
5. **Each finding answers four questions:** what can happen, when, does it affect you, and the planned fix. If no fix is scheduled, say "None scheduled". Do not write a fix as planned unless the maintainer has said so; a reviewer's suggestion is "proposed".
6. **Lead with the finding a user should act on or know about**, usually an accepted open one. Fixed findings from the previous release are one sentence in "What was found".
7. **People are not named.** Write "the maintainer", as the app repositories do.
8. **The plain-terms findings keep the order of the technical findings**, so a reader can match them.

## Rules that keep the tools working

- The `## verdict: ` line stays directly under the title. `tools/client_drift.py` reads it.
- The identity table writes the pinned commit as: commit, a space, then the 40 characters in backticks, with no bold. `tools/client_drift.py` reads the first such match on the page, so nothing above the identity table may use that form for another commit.
- The file name is `<tag>-<first 7 of the commit>.md`.

## Before publishing

- `git ls-remote` the public repository and require the tag to peel to the audited commit. Record the check in the identity row.
- Check line counts after any scripted edit.
- Publish only on the maintainer's own word.
