# prod/GLM-5.3-Flash-SGL-TP4.yaml

Inner (model-layer) compose for z-ai/glm-5.3-flash — two sglang TP4/EP4 replicas; from 2026-09-09 on near.ai's own signed `nearaidev/sglang` build (earlier revisions: an in-enclave build on a Phala sglang base). **Log-pinned**: keyed by
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
| [`2878b9c4c6db…`](sha256-2878b9c4c6db512a7538dc4e8981fd5acae72cdaace7794509f48161bcce08e3.md) | QUALIFIED PASS — **corrected 2026-10-12**: the glm47 engine finding this class rested on is withdrawn as unreachable (its except clause cannot run); was LEAKS — narrowly, same class and reason as d76413cd; engine now the signed a7b7136a build; new patchwork finding (service-scoped deploys) | 2026-09-10 |
| [`e5d80ab6e1a1…`](sha256-e5d80ab6e1a1188fdf8cd3e7bc2f74da5d4767da15b0644acf07dad08a3b461b.md) | QUALIFIED PASS — **corrected 2026-10-12**: the glm47 engine finding this class rested on is withdrawn as unreachable (its except clause cannot run); was LEAKS — narrowly, identical in class and in every finding to the 2878b9c4 sibling page (one-line proxy-digest delta) | 2026-09-10 |
| [`0844864e1ba1…`](sha256-0844864e1ba1b477cd0e57a1f98e01bbfef9f3dd535e3b8bbbacf2cac97a570f.md) | QUALIFIED PASS — a residual revision with nothing left running by construction. By the signed log of the gpu04 CVM (now serving DeepSeek) this hash created three containers on 2026-09-17: both engine replicas, downed 2026-09-23, and glm53-perception-check, never named in a compose down. | 2026-11-20 |
| [`a2d3f073aa2f…`](sha256-a2d3f073aa2f01864bb8eac72ba1f4292ad8391aebdc28e29b84fe8cde48afab.md) | QUALIFIED PASS — a residual revision. By the signed log of the gpu04 CVM (now serving DeepSeek) this hash created two containers on 2026-09-09, model-proxy-registrar and dcgm-glm53. The registrar was replaced on 2026-09-18 and downed on 2026-11-13. | 2026-11-20 |
| [`b2d8b87cf185…`](sha256-b2d8b87cf185ff809f662ce276c2487da852e9903fe5fe0f0dbc3980af49f4ba.md) | QUALIFIED PASS — a residual revision with nothing left running by construction. By the signed logs of two CVMs (the gpu04 CVM now serving DeepSeek, and gpu03) this hash created two one-shot containers on each on 2026-09-23 … | 2026-11-20 |
| [`dac8e7bd277b…`](sha256-dac8e7bd277ba8f6dbf51201a859374f956e92d2546637e17c73608911e65bf4.md) | QUALIFIED PASS — a residual revision. By the signed log of the gpu04 CVM (now serving DeepSeek) this hash created two containers on 2026-09-15, nginx and proxy-glm53. nginx was replaced on 2026-11-17. proxy-glm53, an E2EE-terminating proxy run privileged with the dstack socket from image b3a8c626 (audited, QUALIFIED PASS … | 2026-11-20 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
