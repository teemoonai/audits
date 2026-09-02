# prod/dsv4-qwen38-glm51.yaml

Inner (model-layer) compose for DeepSeek-V4-Flash + Qwen3.8-27B (+ Qwen3.6 / GLM-5.1 in some revisions) — the gpu02 capacity pack. **Log-pinned**: keyed by
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
| [`46edfb72e0d1…`](sha256-46edfb72e0d15618429cedde9fb527bc4d4c4c4073eac08099e854b43c44bc96.md) | QUALIFIED PASS on logging config | 2026-08-17 |
| [`c27ed3b357f4…`](sha256-c27ed3b357f44673e4a84ef89f4625e1009de619d83ffdaae27c1265f676f4bb.md) | QUALIFIED PASS on logging config | 2026-08-21 |
| [`0c1c6841eeaa…`](sha256-0c1c6841eeaa837f2083660327b34c70df8c69501189f14508aa4fe052692e40.md) | QUALIFIED PASS on logging config | 2026-09-02 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
