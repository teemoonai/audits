# prod/GLM-5.2-W4AFP8-SGL-TP8.yaml

Inner (model-layer) compose for z-ai/glm-5.2 — the flagship pair, one sglang TP8 engine per node. **Log-pinned**: keyed by
`file_sha256` against the signed compose-manager action log (commit + path +
file hash), not hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; later ones are usually **delta reviews**
against the previous audited revision and say so in their coverage note. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`db6f4e8ffd03…`](sha256-db6f4e8ffd0324fcc3b2c3ef51ec2a4735b888bd9293057295d9161c9585bf38.md) | qualified PASS on what it configures | 2026-08-03 |
| [`ff35ebb9cbf8…`](sha256-ff35ebb9cbf87c28145635ab348155274adb2d4be584da9dcde7be58a0493a70.md) | QUALIFIED PASS — delta review against the audited base… | 2026-08-17 |
| [`d11837e86909…`](sha256-d11837e869090731b1420553bb321ac596b47e92c498bf36890d2963b4be85b1.md) | QUALIFIED PASS — delta review against the audited base… | 2026-08-21 |
| [`09791d872e3f…`](sha256-09791d872e3f59f0aa341c45a0e5fb33cbfe2c0d8197ce32b6768cfb487a50c9.md) | QUALIFIED PASS — delta over d11837e8: proxy bump to 98b57ad7 and Datadog OpenMetrics labels removed; every load-bearing finding carries | 2026-09-10 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
