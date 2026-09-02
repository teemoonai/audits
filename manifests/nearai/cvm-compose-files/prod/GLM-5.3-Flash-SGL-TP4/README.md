# prod/GLM-5.3-Flash-SGL-TP4.yaml

Inner (model-layer) compose for z-ai/glm-5.3-flash — two sglang TP4/EP4 replicas from an in-enclave build on a Phala sglang base. **Log-pinned**: keyed by
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
| [`d1cc22eb8a25…`](sha256-d1cc22eb8a25890e42a090d2c309b5045cdf374e000ed7228d9394f36f7f96d1.md) | LEAKS — narrowly, and the leak is completed by this document | 2026-09-02 |
| [`d76413cd231a…`](sha256-d76413cd231a4e871a515e4fa829c6510a374fe335e77fae3ea5a6dccf783909.md) | LEAKS — narrowly, identical in class and in every finding to the d1cc22eb sibling page | 2026-09-02 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
