# prod/small-models.yaml

Inner (model-layer) compose for the small-models cluster — a dozen model containers (gpt-oss, Qwen3-VL, Qwen3.6, embeddings, reranker, Whisper, FLUX, privacy filter) behind one proxy each; the fleet's widest recipe. **Log-pinned**: keyed by
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
| [`a385f19a5105…`](sha256-a385f19a51054767b8be49a64ebc3111e0e62f721a861e54c78984b186904599.md) | qualified PASS on logging config | 2026-08-03 |
| [`2443fde49e26…`](sha256-2443fde49e26f83d931c443501544fa0c510c658360c45324190c3d243dfefa3.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-08-17 |
| [`ce39ea4cfe0d…`](sha256-ce39ea4cfe0ddf4dc2e4fbb96b6c66ab9f72954444d5419b196d06940db5e297.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-08-21 |
| [`cb9040a3e32a…`](sha256-cb9040a3e32a0e9157baf26b804d95a3ec55b91d9ae87383e0acd4300490078e.md) | LEAKS — the FLUX diffusion service this file launches logs every user prompt at INFO and writes every… | 2026-09-01 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
