# prod/dsv4-qwen36-gemma4.yaml

Inner (model-layer) compose for DeepSeek-V4-Flash + Qwen3.6-27B + Qwen3.6-35B-A3B + Gemma-4-31B — the four-model combined node. **Log-pinned**: keyed by
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
| [`cf11b98ccd81…`](sha256-cf11b98ccd81a738e051e8c743a67ded88af181648ab05d44d647409c5127d5e.md) | qualified PASS on logging config | 2026-08-03 |
| [`795aab859865…`](sha256-795aab8598653d4f74e3826d662d35d0040a71bca6e6256e5e3646bd5738d5c8.md) | QUALIFIED PASS on logging config | 2026-08-17 |
| [`52ef39d9746c…`](sha256-52ef39d9746c0c4ac961c881c75efa2893257d2a10cb247f9af364302299a658.md) | QUALIFIED PASS on logging config | 2026-08-21 |
| [`99892545ebf1…`](sha256-99892545ebf1f31c53b3239dc24e3ecf6a2add3366e70b3792496485c9b5e7b3.md) | QUALIFIED PASS on logging config | 2026-08-21 |
| [`c6ef1271ffda…`](sha256-c6ef1271ffdaed7e936b271d371da944644d63f0c277fe84e29582f334119fec.md) | QUALIFIED PASS on logging config | 2026-09-01 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
