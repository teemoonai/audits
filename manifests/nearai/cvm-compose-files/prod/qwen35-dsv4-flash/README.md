# prod/qwen35-dsv4-flash.yaml

Inner (model-layer) compose for Qwen3.5-122B-A10B + DeepSeek-V4-Flash — two-model combined node. **Log-pinned**: keyed by
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
| [`5be223d33093…`](sha256-5be223d330932d118eb8ceee6414304af43c98d9a0f43b8195c8d86dfb77d000.md) | qualified PASS on logging config | 2026-08-03 |
| [`11da948ba44f…`](sha256-11da948ba44faae3f0fd7419197495fe82cbeb221bec5f5f03ea6caf580e9964.md) | QUALIFIED PASS — delta review against the audited A/B revision 5be223d3 | 2026-08-10 |
| [`d1cdff7016b9…`](sha256-d1cdff7016b9b1fef4ad1662678404eca67c07c4e2ca8993795a0f8dbe15af1c.md) | QUALIFIED PASS at the manifest layer, with one qualification that outranks the rest | 2026-08-10 |
| [`14ae94e403ce…`](sha256-14ae94e403ce6de638054b6421f105ab01563521aa150e605440b92e71bfea0f.md) | QUALIFIED PASS at the manifest layer | 2026-08-17 |
| [`cb190fcba6b4…`](sha256-cb190fcba6b49ca2dd5092ed59e61cf1c26370aac50dc78416f8b50492858695.md) | QUALIFIED PASS at the manifest layer | 2026-08-21 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
