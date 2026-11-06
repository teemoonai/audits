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
| [`533e43fd215d…`](sha256-533e43fd215d56ec6cd719adb5defe6615f7ba6ae0b018e832f7c8dadf2e25d4.md) | gpu02 | glm-5-3-flash (second CVM, replaced gpu30) | no-Datadog, dstack 0.5.11, gateway off | QUALIFIED PASS at the manifest layer | 2026-09-10 |
| [`55db164f4f8c…`](sha256-55db164f4f8c6a837c2217c601c21bba4758f908536a6cd5b2978550205a9179.md) | gpu03 | glm-5-3-flash (one of two CVMs, beside gpu04) | no-Datadog, dstack 0.5.11, gateway off | QUALIFIED PASS at the manifest layer | 2026-10-02 |
| [`945bcfade2ae…`](sha256-945bcfade2aec53a19da7638774a99caea11395ec03e572a13357a0c63b152b4.md) | gpu23 | glm-5-3-flash-long (one of two CVMs, beside gpu02) | no-Datadog, dstack 0.5.11, gateway off; exporter points at the **staging** telemetry host | QUALIFIED PASS at the manifest layer | 2026-10-02 |
| [`5e513dbd72e1…`](sha256-5e513dbd72e1c0f291f748ad06d4dbc1df55659869e649376213ac7b3c9d2e29.md) | gpu13 | small-models cluster (nine model names, new CVM 2026-10-21) | no-Datadog, dstack 0.5.12 (upstream), gateway off; launcher pinned by child digest `079a14b4` (same bytes as `91fdff3c`) | QUALIFIED PASS at the manifest layer — new HIGH: the proxy's web-search / fusion / Redis / usage-token env arrives only through compose-manager's unattested `/compose/up` env map | 2026-10-22 |
| [`a0e3c6f4f21a…`](sha256-a0e3c6f4f21a60ea3f5c96bc7ef319b03a184ca2049605399275fbcea74e8c5f.md) | gpu03 | glm-5-3-flash (one of two CVMs, beside gpu04 `5f7ebd85`) | no-Datadog, dstack 0.5.12 (upstream; `name` label still says 0.5.11), gateway off; = `55db164f` with the launcher re-pinned by child digest | QUALIFIED PASS at the manifest layer — env-overlay HIGH; **HIGH, exercised 2026-10-29 (addendum 2026-10-30):** the signed log's last entry starts compose-manager `a320bb48` while the measured default stays `6e035c8f`; MEDIUM: the deploy bearer token was rotated 2026-09-29 through that overlay into the launcher's replay file | 2026-10-30 |
| [`ae66f844658a…`](sha256-ae66f844658a7aee331dcb9fb59bd40323d71d192d37719e022cc4af8389265b.md) | gpu02 | glm-5-3-flash-long (one of two CVMs, beside gpu23 `945bcfade2ae`) | no-Datadog, dstack 0.5.12 (upstream; `name` label still says 0.5.11), gateway off; = `533e43fd` with the launcher re-pinned by child digest; exporter on the production telemetry host | QUALIFIED PASS at the manifest layer — env-overlay HIGH; token-rotation MEDIUM | 2026-10-22 |
| [`5f7ebd85cf1f…`](sha256-5f7ebd85cf1f480a118f75dd10fd0cb277e4ddbb23845f1c20d8ea0f1e87efa6.md) | gpu04 | glm-5-3-flash (one of two CVMs, beside gpu03 `a0e3c6f4`) | = the audited gpu04 `c82b1a2e` with the launcher re-pinned to the index's amd64 child `079a14b4` (one line); no-Datadog, dstack 0.5.12, gateway off | QUALIFIED PASS at the manifest layer — env-overlay HIGH carried; **new HIGH, exercised:** the signed log's last entry is a `compose_manager_started` on `a320bb48` (2026-10-29T06:04Z) while the measured default at line 95 is `6e035c8f` — the manager running is not the one measured; token-rotation MEDIUM | 2026-10-30 |
| [`ae0c5a6586c8…`](sha256-ae0c5a6586c82aa891f3a487c932a440f09758dca530cff5009d8e48e7089784.md) | gpu23 | glm-5-3-flash-long (now the only CVM; gpu02 `ae66f844` moved to DeepSeek-V4.1-Flash on 2026-10-27/28) | = the audited gpu23 `945bcfade2ae` with the launcher re-pinned to `079a14b4`; exporter on the **staging** telemetry host (carried MEDIUM); no-Datadog, dstack 0.5.12 | QUALIFIED PASS at the manifest layer — env-overlay HIGH carried; **new HIGH, exercised:** manager swapped to `a320bb48` at 2026-10-29T06:05Z against a measured default of `6e035c8f`; staging-endpoint MEDIUM; token-rotation MEDIUM | 2026-10-30 |
| [`cc846c45cbdd…`](sha256-cc846c45cbdd7a5ba126ae2b362f359307a1dea05468c8f1a3f064f0bb3173d6.md) | cm-gpu32-g7 | qwen3-8-27b + qwen3-8-27b-abliterated (single-GPU CC CVM, fresh 2026-10-29; the same names also served from gpu13) | = `5f7ebd85` with the compose-manager default moved to `a320bb48` and the host label changed; boots guest OS **0.5.11** `a6eafc5f` (not the fleet's 0.5.12); 3-entry log | QUALIFIED PASS at the manifest layer — env-overlay HIGH carried (the abliterated proxy's token arrives only through it); the manager-swap HIGH carries as a mechanism with the default and the occupant the same today; tag-age MEDIUM exercised (1 h 40 min); LOW older guest | 2026-10-30 |
| [`31d3b2389e06…`](sha256-31d3b2389e06a4450e342f3a45fdbb5d7ce4c607c359f5b291635548b0b80007.md) | cm-gpu32-g7 | qwen3-8-27b + qwen3-8-27b-abliterated (single-GPU CC CVM re-created 2026-11-02; both names also served from gpu13) | = `cc846c45` with the outer `name` moved to dstack-nvidia-0.5.12 (one field; compose byte-identical); boots guest 0.5.12 `91fd5d69` | QUALIFIED PASS at the manifest layer — this document is, by one byte substitution and re-hashing, the audited cm-gpu32-g7 harness cc846c45 with its outer name string advanced from dstack-nvidia-0.5.11 to 0.5.12; the 374-line compose, the 34-line pre_launch_scr… | 2026-11-06 |

A hash not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
