# measured composes

The **hardware-measured** layer of every GPU node: the dstack `app_compose`
document whose SHA-256 is sealed into the TDX quote as `compose_hash`. It is the
management harness only — otel collector, certbot, compose-manager and its
launcher — not the model stack. The model stack is the runtime-fetched inner
recipe pinned by the signed compose-manager action log; those live under
[`../nearai/cvm-compose-files/prod/`](../nearai/cvm-compose-files/prod/). A
page here answers what the harness itself can read, log or ship, and what it
lets the recipe do.

One hash per harness *template × host label*: the same template on two hosts
gives two hashes (only `INSTANCE_LABEL` differs), so several rows below are
near-identical documents. The "template" column is the axis that decides who
reads engine stdout: on the **Datadog side** of the node lottery a measured agent
ships every container's stdout to `us3.datadoghq.com`; on the **no-Datadog**
side the only off-box log path is near.ai's own gateway at
`telemetry.infra.near.ai`. Node placement is from the fleet capture at review
time; `python3 tools/fleet_drift.py` says which hashes are live today.

## reviewed documents

| compose_hash | host label | serving at review time | template | verdict | review |
|---|---|---|---|---|---|
| [`2c650eae8160…`](sha256-2c650eae81601afade86d1aa5ad898473b992081998026bb42ee1524ce99ee38.md) | — | GPU-node management harness (first review run) | — | management-only; zero plaintext-toucher signals | 2026-07-15 |
| [`db6943f37a4f…`](sha256-db6943f37a4f54bd12144ecbf9f8c780ca14c0c44600a5a9ca09a041d92ba5ca.md) | — | dsv4-qwen36-gemma4 combined node | first review run | qualified PASS at the manifest layer | 2026-07-22 |
| [`002b406e4770…`](sha256-002b406e4770df733eba8f7dfce066f1c8e8d041d972cc02da8b9e3756ebca9a.md) | gpu23 | glm-5-2 + glm-5-2-long | Datadog side | qualified PASS at the manifest layer | 2026-08-03 |
| [`0fccab4eb7ff…`](sha256-0fccab4eb7ffc4c9ec1be8e2851e7b820efef0485cfd21ac027bf1408dc836b0.md) | gpu11 | dsv4-flash / glm-5-1 host set | Datadog side | qualified PASS at the manifest layer, weaker than its sibling on the one axis that… | 2026-08-03 |
| [`66007399f064…`](sha256-66007399f064f058af68771c552bcae150c9f88622305631b5141da1aa2f7b7e.md) | gpu30 | qwen35-122b + dsv4-flash | Datadog side | qualified PASS at the manifest layer | 2026-08-03 |
| [`9385918de0a7…`](sha256-9385918de0a73b861ae833d99fb5be6f7e1c8a50487a835df4f277497c206825.md) | gpu04 | glm-5-2, later gemma-4-31b / Qwen3.6 | no-Datadog | qualified PASS at the manifest layer | 2026-08-03 |
| [`d98a2568546a…`](sha256-d98a2568546afce9ab53f7eb4d4b2058e5497e1efd05a8ad0934793043240ed7.md) | gpu02 | dsv4-flash + glm-5-1, later Qwen3.6/3.8 + dsv4 | no-Datadog | qualified PASS at the manifest layer | 2026-08-03 |
| [`fb3d47e5ae94…`](sha256-fb3d47e5ae94ddfd43721002b127ce07d3828b05687e4e5a394a7a827d0ec55c.md) | gpu13 | small-models node | Datadog side | qualified PASS at the manifest layer | 2026-08-03 |
| [`546161bcde5e…`](sha256-546161bcde5ef901652e7b5b774322e790748e725fbfb158d0f394153271bc86.md) | gpu23 | glm-5-2 + glm-5-2-long | no-Datadog (regenerated) | QUALIFIED PASS at the manifest layer | 2026-08-17 |
| [`d4c89033fb55…`](sha256-d4c89033fb55cdac9db00c775fbbbeff6319fba7249344b2dca99b23ff048479.md) | gpu13 | small-models cluster | no-Datadog (regenerated) | QUALIFIED PASS at the manifest layer | 2026-08-17 |
| [`5c027cc86ab4…`](sha256-5c027cc86ab48fa98550f5be9be0621adff811fa231d955653396f6e13f85bd2.md) | gpu26 | glm-5-2 (third flagship node) | no-Datadog (regenerated) | QUALIFIED PASS at the manifest layer | 2026-08-21 |
| [`341313aed433…`](sha256-341313aed4336a5fb592cef58004b3abc82f2ba751df32be69f3169eeba40c14.md) | gpu30 | glm-5-3-flash | no-Datadog, dstack 0.5.11, gateway off | QUALIFIED PASS at the manifest layer | 2026-09-01 |
| [`c82b1a2eaf69…`](sha256-c82b1a2eaf6996154a5f39ae621643f034b082d5e51edd3d2ba6009273881d86.md) | gpu04 | glm-5-3-flash (second CVM) | no-Datadog, dstack 0.5.11, gateway off | QUALIFIED PASS at the manifest layer | 2026-09-02 |

A hash not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
