# Do two independent reviews converge? A controlled comparison

> Editorial note, outside the path contract. 2026-08-03.

[`method.md`](/notes/method.md) rests on a claim it has never tested: that the audit is
portable, and *"the point of the portable prompt is that independent runs converge."*
On 2026-08-03 two different models reviewed the same two images, from the same deployed
configuration, under the same method. This note reports what actually happened, because
the claim is load-bearing and an untested load-bearing claim is a liability.

## The setup

Two vLLM builds on near.ai's `small-models` node were each reviewed twice:

- `vllm-openai@sha256:6766ce0c…` — the gpt-oss-120b engine, vLLM `v0.12.0`
- `vllm-openai@sha256:ccd6a6db…` — the Qwen3-VL-30B engine, the `v0.17.0` line

**Reviewer A** was Claude Opus 5, the orchestrating model. **Reviewer B** was Fable,
which produces the reviews published in this repo. Both got: the same question, the same
deployed launch command and env from the attested compose, the same instruction set, and
the same already-resolved image identity. Neither saw the other's output. A's drafts were
written first and set aside before B ran; they are preserved outside this repo and were
never published, because a page attributed to "independent AI source review, Fable" must
actually be Fable's work.

One deliberate asymmetry: **image identification** — the registry forensics that resolves
a digest to a source commit — was done once, by A, and handed to both. The comparison is
therefore of *source review*, not of identification.

## What happened

**They converged on the headline, and diverged sharply on completeness.**

### gpt-oss (`6766ce0c`)

Both reached the same broad verdict: no plaintext reaches a log, disk, or non-model
destination at the deployed flags. Both correctly established that request logging is
opt-in and absent, that prompt text additionally needs DEBUG, that no runtime endpoint can
enable logging without a restart, that disk holds only weights and compile artifacts, and
that the usage-stats phone-home is on and content-free.

Then B found something A did not, at all:

> **the crash-path token-ID leak.** `CachedRequestData` carries `all_token_ids` — full
> prompt *plus* generated tokens — and has no `anon_repr`, so an engine-crash dump falls
> through to the `__dict__` serializer and writes it to stdout at ERROR, which this fleet
> ships off-box. `NewRequestData` *is* redacted; the cached path is not.

A had listed the crash-dump path under "not traced" and moved on. Every link in B's chain
was independently re-verified before publication and held.

B also corrected A's reasoning on a point A had gotten *nearly* right. A argued that the
deprecated `--disable-log-requests` alias resolves to a safe default. B ran a whole-tree
grep and established the flag's dest **is never read anywhere** — a pure no-op alias, so
there is no polarity question to reason about. Same conclusion; strictly stronger evidence.

### Qwen3-VL (`ccd6a6db`)

**The independence check passed.** Both reviewers independently found the load-bearing
finding — that `--allowed-media-domains` is absent, that the guard is a truthiness test on
a list which defaults to empty so no check runs, and that redirect-following is left at its
permissive default. Both also independently noticed the thing that makes it a *finding*
rather than an upstream default: the Gemma-4 service in the same attested compose file sets
both controls. Two reviewers, no contact, same conclusion from the same evidence. That is
the convergence `method.md` predicts, and it is the strongest single data point here.

They diverged on severity — A rated it HIGH, B rated it MEDIUM — and B's calibration was
better: no chat plaintext reaches a third party, the URL schemes are constrained, and
`file:` reads are hard-blocked because `--allowed-local-media-path` is unset. A's HIGH
over-weighted the SSRF surface relative to the question this repo actually asks.

B additionally found four things A missed: a prompt-text `logger.debug` at
`chat_utils.py:1175` that sits *outside* the `--enable-log-requests` gate (so one env var
suffices, not a flag plus a level); that `--enable-log-outputs` emits responses at **INFO**
with no level guard, contradicting its own docstring; that the whisper service `pip
install`s `vllm[audio]` from PyPI at build time and can therefore replace the audited engine
inside the enclave; and the shared prefix-cache timing side channel.

B also closed the identity bracket far more rigorously. Both were told the build was
bracketed to a ~3-day window. A wrote "reviewed at `v0.17.0`, drift possible" and left it.
B checked all 18 cited files against the commit API for changes *within that exact window*,
found 16 had zero commits, and named the two that changed with their precise impact — one
shifts a cited line by exactly one. That converts a hand-wave into a bounded claim.

## Scorecard

| | Reviewer A (Opus) | Reviewer B (Fable) |
|---|---|---|
| Verdict, both images | substantively same | substantively same, more precisely worded |
| Findings unique to it | none of substance | 5+ across the two pages |
| Missed a live defect | yes (crash-path leak) | not detected |
| Citation accuracy | 3 wrong line numbers, self-caught pre-filing | spot-checks all held |
| Severity calibration | over-rated one finding | better |
| Overclaim discipline | refused a `sources` pin on bracketed identity | same |

## What this says about the method

**The good news is real.** On the finding that mattered most, two independent reviewers
converged — including on the cross-service comparison that turned a default into a defect.
That is evidence the method is portable rather than a single model's idiosyncrasy.

**The bad news is more useful.** Convergence on the headline did *not* imply convergence on
coverage. One reviewer missed a live defect the other traced end-to-end, and the miss was in
an area it had explicitly marked "not traced" — which is to say the honest-gaps discipline
worked exactly as designed, and the gap was still a gap. "Re-run and compare" surfaces
disagreements; it does not surface *shared* blind spots, and nothing here tests for those.

Two consequences worth acting on:

1. **A finding-derived audit-surface checklist** would have closed this specific gap. Both
   reviewers had to rediscover which files constitute the audit surface. A checklist —
   crash/dump paths, watchdog and hang handlers, `__repr__`/serialization fallbacks,
   runtime-reconfiguration endpoints, log sinks, media ingestion — turns "did the reviewer
   think to look" into "did the reviewer complete the list."
2. **Mechanical checks beat prose for negative claims.** The crash-path leak is detectable
   without any dataflow analysis: *enumerate dataclasses reachable from `SchedulerOutput`;
   flag those lacking `anon_repr` that carry a `*token_ids*` field.* That is a short AST
   check. It would have found the bug in seconds and, run against each new digest, would
   keep finding it — and it would have flagged the upstream fix at `v0.17.0` automatically.

The corollary for readers of this repo: a page's verdict is evidence, not proof, and the
"not traced" section is the most important part of any review here. In this comparison it
was exactly where the missed defect lived.

## Reproducing this

The inputs were identical and are all public: the image digests, the attested compose, and
the pinned source commits are on each page. Anyone can run a third review and compare
against both. If a third reviewer finds something both of these missed, that is the
method working — and it should be written up here the same way.
