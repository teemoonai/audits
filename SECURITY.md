# Security and disclosure

This repository publishes exfiltration verdicts about two things: **the teemoon
app on your device** (can it leak your provider keys, or your plaintext?) and
**near.ai's confidential inference stack** (can it leak your plaintext?). We
operate the app but none of the near.ai systems. Three different things can be
wrong, and they go to different places.

## An error in a published verdict

If a page here claims something the source does not support — a wrong line
number, a missed sink, an over- or under-rated severity, a stale "not seen live"
identity — **open a public issue** in this repository with the page path and the
evidence. Pages are corrected with a dated addendum, never silently rewritten,
and the correction is credited unless you ask otherwise. Every claim a page makes
is meant to be checkable by anyone from the cited sources; a report that it is
not checkable is itself a finding.

## A vulnerability in the teemoon app

A defect in the client — a provider key reaching a log, a file outside the
Keychain, the pasteboard, or any host but its own provider; plaintext reaching
anywhere but the send path you chose — is ours to fix, and the client repository
has its own private channel:
[teemoonai/teemoon-ios security advisories](https://github.com/teemoonai/teemoon-ios/security/advisories/new).
Report it there, not here, so the fix and the disclosure stay together. If a
page in this repository asserts the absence of exactly that path, say so in the
report and we will correct the page with a dated addendum once the fix ships —
the way the 1.0.2 URL-cache finding was handled.

## A vulnerability in the audited stack

A defect in near.ai's software (sglang, vLLM, inference-proxy, compose-manager,
dstack, the guest OS) is near.ai's to fix, and disclosing it here first would
publish it before they see it. **Report it to near.ai** through their own
security contact. If you want us to know as well — for example because a
published page asserts the absence of exactly that path — use the private
channel below and say whether near.ai has been notified.

## Private channel

Use GitHub's **private vulnerability reporting** on this repository
(*Security → Report a vulnerability*). It reaches the maintainers only. Use it
for anything that should not be public yet: a live exploitation path in a
deployed configuration a page rates as safe, credentials or private material you
found quoted in a page, or a report you are coordinating with near.ai.

We aim to acknowledge private reports within seven days and to publish a dated
correction or an INCONCLUSIVE fallback within thirty. There is no bounty.

## What this repository is not

It is not a monitoring service and makes no availability promise. Verdicts are
point-in-time claims about an exact identity (digest, file hash, or measurement);
the fleet redeploys freely and a page can describe history within a day. The
daily drift check (`tools/fleet_drift.py`) files an issue when something in
scope runs unaudited; the absence of such an issue is not a guarantee.
