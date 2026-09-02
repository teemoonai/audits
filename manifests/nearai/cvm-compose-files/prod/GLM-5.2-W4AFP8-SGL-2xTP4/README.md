# prod/GLM-5.2-W4AFP8-SGL-2xTP4.yaml

Inner (model-layer) compose for z-ai/glm-5.2 — two sglang TP4 replicas (the earlier flagship layout). **Log-pinned**: keyed by
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
| [`f408de5c89d7…`](sha256-f408de5c89d7e7f8b4715b1f62409f67cadf52e232cfdce663f94482a134bba2.md) | qualified PASS on what it configures | 2026-08-03 |
| [`5b8fd687ad6f…`](sha256-5b8fd687ad6fa58747fcb5731fc28b2d1e91dac121c7843df525f6a93252fa34.md) | QUALIFIED PASS — carried unchanged from f408de5c | 2026-08-21 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
