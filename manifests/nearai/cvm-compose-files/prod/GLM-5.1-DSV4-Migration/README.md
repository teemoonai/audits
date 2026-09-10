# prod/GLM-5.1-DSV4-Migration.yaml

Inner (model-layer) compose for the 2026-09-08 bridge that relocated DeepSeek-V4-Flash (two SGLang TP2 replicas) onto the GLM-5.1 AWQ TP4 CVM (hosts dsv4-flash, glm-5, glm-5-1); successor to [`dsv4-flash-glm51.yaml`](../dsv4-flash-glm51/) on those hosts. **Log-pinned**: keyed by
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
| [`2db74d72aea6…`](sha256-2db74d72aea666868a778a4e5c3635ac8940cf0d53095c42d3282f60b115b8d7.md) | QUALIFIED PASS — every service block byte-equivalent to an already-audited GLM-5.1-AWQ-TP4 or DSV4-Flash block; residuals are the fleet's, doubled across two arms | 2026-09-10 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
