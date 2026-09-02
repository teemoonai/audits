# prod/dsv4-flash-glm51.yaml

Inner (model-layer) compose for DeepSeek-V4-Flash + GLM-5.1 sharing one CVM. **Log-pinned**: keyed by
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
| [`d085dcfc4ee0…`](sha256-d085dcfc4ee0fbb13b183d52cf3a140cbc075e5e3de44fc039df961a4913ca4c.md) | qualified PASS on what it configures | 2026-08-03 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
