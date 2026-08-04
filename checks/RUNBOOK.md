# Runbook: a fleet-drift issue just opened

The daily check found something in scope running with no page. This is how to
close it. Steps 1 and 4 are scripted; steps 2 and 3 are where the judgement is.

> **The short version: open Claude Code in this repo and run `/audit-drift`.**
> The skill at `.claude/skills/audit-drift/` drives everything below — it reads
> the issue, runs the identity resolver, spawns the Fable reviewers, verifies
> their load-bearing claims and gates the pages. You are not spawning reviewers
> by hand: a Claude session does that with the Agent tool, `model: "fable"`.
> The rest of this file is what that skill is doing, and why, so you can drive it
> manually or check its work.

The shape to keep in mind: **detection is cheap and automated, review is expensive
and deliberate.** Producing one page costs roughly 80–240k tokens and 10–20
minutes of a reviewing model's time. Never put that on a timer, and never publish
what it returns without checking the load-bearing claims yourself.

---

## 0. Read the issue

It lists what is unaudited, and on which hosts. Sort by blast radius: an engine
that sees plaintext on nine hosts outranks a telemetry sidecar on one.

Check the **KNOWN OPEN** section too. Those are recorded in
[`acknowledged.json`](acknowledged.json) and are not new — they are a backlog,
not an alarm.

## 1. Resolve identity — before anything else

```
python3 checks/resolve_identity.py --brief <image>@sha256:<digest>
```

A review keyed to the wrong tree is worse than no review, and this repo has been
wrong twice for exactly that reason: a compose comment was trusted and the
image's own registry metadata was never read. The script walks the evidence
ladder and tells you **which rung answered**, because the strength of the binding
decides what may be claimed later.

- Resolved → `--brief` prints a target block to paste into step 2.
- **UNRESOLVED** → skip to step 5. An INCONCLUSIVE page is a correct outcome, not
  a failure. Do not guess a commit.

If the image is untagged and unlabelled, the script dumps its Dockerfile ARG
defaults so you can bracket a commit range against upstream tags. One more trick
worth trying by hand: an unpinned `git clone` in a build leaves `.git/` in a
layer, and `.git/shallow` has recovered a commit that was otherwise unrecoverable
— confirm with a full tree diff against the upstream tarball.

## 2. Commission the review

One agent per target. **Max 3 concurrent** — a wider fan-out has hit the session
limit twice, and the second time cost seven agents' work.

The brief must contain:

- the resolved target from step 1, **including its identity class and caveat**
- the deployed launch command and env, quoted from the attested compose
- "walk [`notes/audit-surface.md`](/notes/audit-surface.md); report anything you
  could not reach under *Not traced*"
- **write the page to disk as soon as findings exist, refine in place** — this is
  what saved three pages when an agent died mid-run
- return a short summary, not the page text
- `grep -n` with targeted patterns; never `cat` a file over ~300 lines. The most
  expensive review in the corpus read large files whole; the cheapest grepped for
  symbols it already knew to want, at a third of the cost per call
- house rules: cite `file:line` and verify each one; distinguish "OFF at deployed
  flags" from "cannot happen"; a control outside the image is a **residual, not a
  mitigation**; never assert safety you did not verify

Point it at a recent page for format. Ask it to flag anything it wants
independently re-verified — reviewers have done this well, and it is where the
best catches come from.

## 3. Verify before publishing

**Do not skip this.** On the run that produced these pages it caught: an
attestation lookup that read only the first of four results, a severity rated a
level too high, a claim about a Datadog agent that was wrong on first inspection,
and one finding that had to be refuted outright.

You are **not re-doing the review**. A citation either resolves to the claimed
content or it does not, and that is a cheap question — two to four commands per
page. What you are testing is whether the evidence exists and says what the page
says it says.

### What to verify, in priority order

1. **The finding the verdict rests on.** If the page says CRITICAL, verify the
   CRITICAL. Everything else can be sampled.
2. **Anything the reviewer flagged for you.** Good reviewers do this explicitly,
   and it is where the sharpest catches have come from — one wrote *"`6e035c8f`
   has 4 attestations, not 1"*, correcting the identity handed to it; another
   refused to guess whether an S3 path was operator-reachable and said which
   answer would change the severity.
3. **Anything that contradicts a published page.** Settle it at the source, then
   correct the older page with a dated addendum rather than a rewrite.
4. **Novel findings** — anything the brief did not prime the reviewer to look
   for. No prior means no cross-check.
5. **Anything that changes what a user sees**: severity, whether the page gets
   gated, whether a `sources` pin is earned.

Skip: routine INFO items, and ground already verified on a sibling page.

### How to verify a multi-hop finding

Most real findings are chains, and a chain is only as good as its weakest link.
Verify each hop separately rather than the conclusion. For the crash-path leak
that was the run's best catch, that meant five checks:

```
core.py:316          dump_engine_exception(...) is called unconditionally
dump_input.py:79     ... and logs at ERROR
dump_input.py:40-47  anon_repr is preferred, __dict__ is the fallback
output.py:112-123    CachedRequestData has all_token_ids and NO anon_repr
scheduler.py:842     ... populated from req.all_token_ids.copy()
request.py:91        ... which is prompt tokens plus generated tokens
```

Each one held, so the finding held. Had the fourth failed, the whole thing
collapses — and that is exactly the hop a summary would have glossed.

### Verifying a negative claim

"No path allowlist exists", "no route is `ADMIN_FORCE`", "this dest is never
read" — these need a **whole-tree** search, not a spot check, and they need it at
the right commit. Prefer fetching the tree and grepping it over trusting a
reported grep. When a negative claim contradicts a published page, check it at
**both** commits before concluding it is a regression rather than a long-standing
error.

### When a check gives a surprising answer, check what actually matched

A grep for Datadog reported it present on every node, contradicting the page.
The pattern had matched `datadoghq.ad` — an autodiscovery *label* — not the SaaS
endpoint. Re-running against actual service definitions showed two nodes with 11
services and no agent, five with 13 and an agent shipping to `us3.datadoghq.com`.
The page was right and the first check was wrong.

The general form: a surprising result is more often a bad query than a bad page.
Look at the match before you act on the count.

### Do not infer what you can read

An attempt to derive severity levels from verdict prose labelled the genuinely
clean page "qualified" and the page with a live token-ID leak "clean". Severity
is stated by the reviewer or it is not stated. The same applies to anything else
that looks summarisable: read the page.

## 4. Publish

```
python3 checks/index_page.py <page> --commit <repo>@<full-40-hex-sha>
```

Infers the gate from the page path, refreshes every page's verdict verbatim from
its own `## verdict:` heading, and validates the whole index.

- **`--commit` only when identity is a real binding** (signed attestation, OCI
  label, or release tag). A bracket is not a pin — the app renders `sources` as a
  *verified* digest→commit binding.
- It **refuses** to gate an INCONCLUSIVE page. That refusal is deliberate.

Then commit and push. The next scheduled run closes the issue by itself.

## 5. When identity cannot be established

1. Publish an INCONCLUSIVE page that makes **no privacy claim**, and record how
   absence was established — a positive control in the same run is what
   distinguishes "genuinely absent" from "we looked in the wrong place".
2. `python3 checks/index_page.py <page> --no-gate` — verdict recorded, no link.
3. Add it to [`acknowledged.json`](acknowledged.json) with a reason and a
   `closes_when`, so it stops counting as drift.

Without step 3 one permanent gap keeps the check red forever and everyone learns
to ignore it. A new identity is the alarm; a known one is a backlog entry.

## 6. When drift is a *change*, not an addition

If an identity that already has a page reappears with different deployed flags,
the page's verdict may no longer hold — every verdict here is stated relative to
a configuration. Re-read that page's *Controls that would change the verdict*
table against the new config before assuming it still stands.

For a new build of an already-audited image, prefer an explicitly-scoped **delta
review** — diff `old..new` restricted to the audit surface, and re-review in full
only if the diff touches it. That is the only approach that keeps up with an
upstream that moves weekly.

---

### Things that are not this loop

- **Verdicts reach users only through the app.** The repo publishes them; the
  client renders them. A page with a CRITICAL and an app that hasn't shipped the
  `verdicts` support are not the same as a user being informed.
- **Some findings can only be fixed upstream** — an unauthenticated admin
  endpoint, a missing `--revision` pin, an unpublished build attestation. Those
  are asks to near.ai, not work items here. Record them on the page and raise
  them separately.
