# A real brief, exactly as sent

This is the prompt that produced
[`images/docker.io/lmsysorg/sglang/sha256-5027e95b…`](/images/docker.io/lmsysorg/sglang/sha256-5027e95bf6ec536856b1b52a91d1f35ff5c564ab83e8a94758a169ff09bb8df3.md)
— the page carrying the CRITICAL `/configure_logging` finding and the HIGH
watchdog prompt dump. Reproduced verbatim so the template in `SKILL.md` has a
worked example beside it; only the scratchpad paths are shortened.

Two things about it are worth copying, and neither is obvious from the template:

**It names the priority items and demands they be re-derived.** The brief tells
the reviewer that other pages in this repo found an unauthenticated
`/configure_logging`, and then explicitly says *do not assume the earlier finding
still holds — confirm or refute it at this commit*. That is the difference between
priming and prejudging. The reviewer came back having confirmed it **and** having
found the mechanism nobody had documented: `ADMIN_OPTIONAL` permits when no key is
set, and the auth middleware is never installed at all because no route is marked
`ADMIN_FORCE`.

**It says what would make the finding worse, not just what to find.** "If a control
lives OUTSIDE this image, say so explicitly — that is a residual, not a mitigation."
That single rule is why the page correctly refused to treat the proxy as a guard,
which is what surfaced the phantom-allowlist error in three older pages.

---

```
INDEPENDENT privacy source audit for the public repo `teemoonai/audits`. Your review
will be published verbatim as "independent AI source review, Fable". Do your own
reading — do not assume any prior conclusion.

## The one question this repo answers
Can anything exfiltrate the user's plaintext chat messages? "Private" = message
plaintext is visible ONLY to (a) the user and (b) the inference engine process. Any
copy reaching a log, file, DB, cache, crash dump, telemetry exporter, or non-model
network destination is a FINDING.

## Target (identity GIVEN — established from the image's own OCI labels)
- Image: `docker.io/lmsysorg/sglang@sha256:5027e95bf6ec536856b1b52a91d1f35ff5c564ab83e8a94758a169ff09bb8df3`
- Labels: `ai.sglang.build.commit` = `49e384ce9d304648e9959666ecb8ce8cd98d0deb`,
  `ai.sglang.image.tag` = `lmsysorg/sglang:v0.5.14`,
  `org.opencontainers.image.source` = `https://github.com/sgl-project/sglang`.
  Built 2026-06-26.
- Read source at
  `https://raw.githubusercontent.com/sgl-project/sglang/49e384ce9d304648e9959666ecb8ce8cd98d0deb/<path>`

## Why this one matters
This engine serves **`z-ai/glm-5.2`** — currently near.ai's flagship model — and has
never been audited. Other sglang builds in this repo were found to carry a
**CRITICAL residual: an unauthenticated `/configure_logging` runtime endpoint** that
can turn on request/response logging WITHOUT a process restart. Verify from source
whether that endpoint still exists at THIS commit, what exactly it can switch on, and
whether anything authenticates it. Do not assume the earlier finding still holds —
confirm or refute it at `49e384ce`.

## Where it runs (hardware-attested compose)
File on disk: <scratchpad>/yamls/prod_GLM-5.2-W4AFP8-SGL-2xTP4.yaml
Services: `model-sg-glm52-w4a-tp4-r1` and `-r2` (two replicas). READ THE FILE for the
exact `command:`/`environment:` (follow the YAML anchors — `<<: *name` merges and
`command: *name` aliases; the launch flags often live in an `x-*: &name` block). Also
read the sibling services (the `vllm-proxy-rs` E2EE terminator, telemetry sidecars)
for context on where this container's stdout goes — check for `com.datadoghq.ad.logs`
labels.

## What to look for (cite file:line + a short quote for EVERY claim)
1. Request/response logging: the launch flags that enable it, their defaults, and what
   level emits prompt vs. output text. Which of them appear in the DEPLOYED command?
2. **Runtime switches** — the priority item: any HTTP endpoint that can enable
   logging/dumping/tracing without a restart. Enumerate the server's full route list at
   this commit. For any such endpoint, determine whether it requires authentication and
   what it can turn on.
3. Disk persistence: prompt/response caches, tokenizer caches, torch.compile artifacts,
   crash dumps, any request-derived data written to a mounted volume.
4. Network egress from the engine process: telemetry, tracing, phone-home, weight
   download, anything request-driven.
5. Crash/exception handlers that embed request state.
6. Multimodal/media fetch paths, if any are reachable for this model.

## Rules (these are the point)
- EVERY `file:line` you cite MUST be verified by actually fetching that file and
  confirming the line number and content. Do not guess line numbers.
- Distinguish "OFF at deployed flags" from "cannot happen". Severity reflects the
  DEPLOYED state, plus what would activate it.
- If a control is only guarded by something OUTSIDE this image (e.g. a proxy
  path-allowlist that is not itself attested), say so explicitly — that is a residual,
  not a mitigation.
- Never assert safety you did not verify. State untraced areas explicitly.

## Output
Return the COMPLETE markdown body of the audit page, ready to publish, in the house
style:
1. `# docker.io/lmsysorg/sglang @ sha256:5027e95bf6ec...`
2. `## verdict: <short verdict>` + metadata table (image / digest / seen in / source /
   build attestation / review). **review** = `reviewed 2026-08-03 (independent AI
   source review, Fable — method: [/notes/method.md](/notes/method.md))`. For **build
   attestation**: public Docker Hub image, no near.ai attestation; identity from the
   image's own OCI labels (registry-verifiable, but self-asserted by the builder, not a
   signed provenance attestation).
3. A short **coverage:** paragraph on identity strength.
4. `# SGLang inference engine (GLM-5.2) — Privacy Audit` with
   Image/Source/Location/Role/Verdict lines.
5. `## Audit prompt` — fenced text block reproducing YOUR review elsewhere.
6. `## Results` — deployed launch command; **Traced:** vs **Not traced (explicit):**;
   findings as `### SEVERITY (deployed: ON/OFF) — headline`.
7. `### Controls that would change the verdict` — markdown table.
8. `### Verdict: …` + **Residuals**.

Citations as full GitHub blob URLs with `#L<n>`.

Output ONLY the markdown page. No preamble.
```

---

## What changed after this brief

Two instructions were added to the template on the strength of later runs, and the
example above predates both:

- **"Write the page yourself with the Write tool, as soon as findings exist."** This
  brief asked for the page as a return value. When a later agent hit the session
  limit mid-run, everything it had done was lost. The next wave wrote to disk first,
  and an agent that died in exactly the same way still left all three of its pages
  intact.
- **"Never `cat` a file larger than ~300 lines."** Cost per tool call varied threefold
  across reviewers purely by read strategy — the expensive ones read whole files, the
  cheap ones grepped for symbols they already knew to want.

Also worth noting: this brief did not point at
[`notes/audit-surface.md`](/notes/audit-surface.md), which did not exist yet. It
should now.
