# prod/glm-5.3-flash-vllm-pd2x2.yaml

Inner (model-layer) compose for **z-ai/glm-5.3-flash on vLLM with prefill/decode
disaggregation**: two pairs per host, each pair a two-rank prefill group and a two-rank
decode group on four GPUs, one PD router per pair, behind the E2EE proxy, nginx, the
registrar and the recipe's collector, with a dcgm exporter, two network-namespace
sidecars, a one-shot downloader and a one-shot egress probe. The engines and routers
sit on two internal Docker networks with no route out; the probe asserts that before
the proxy may start. KV state moves prefill to decode over NIXL/UCX `cuda_ipc` inside
each pair's private IPC and network namespace.

It replaced the sglang recipe [`GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8/)
on the `glm-5-3-flash` gpu03 CVM (measured harness
[`d7871cce`](../../../../measured/sha256-d7871cce53c04f1ceae14ec277e2c33b83d275ce0ee8158bac3362113d67f19b.md))
from 2026-11-22T02:28:41Z. On that CVM the proxy, both routers, nginx and the collector
were created from `b293e27a`, and all eight engines and the registrar from `6bcb69e3`,
the last file touched; every non-engine block is byte-identical in the two texts.

Identity for every revision below is **log-pinned**: the file's `file_sha256` against
the signed compose-manager action log (commit + path + file hash), not
hardware-measured. Per-image behaviour is deferred to the image pages each revision
links. The verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`b293e27a1100…`](sha256-b293e27a110083d437934040a46913f59269ed9ea822583691a4614acfc31317.md) | QUALIFIED PASS at the manifest layer — as a document, the decrypted request never leaves the CVM: nginx (TLS) hands it to the E2EE proxy vllm-proxy-rs e3a4fbca … | 2026-11-24 |
| [`6bcb69e3c65a…`](sha256-6bcb69e3c65a4bdd4741c8d1ad6c3e45d3cf5b7295226c527c334626ebd64634.md) | QUALIFIED PASS at the manifest layer — by the signed action log this revision created the eight engines (entries 114 and 116, 2026-11-23) and the registrar … | 2026-11-24 |

## revisions in the log with no page

Action-log entries in this table are numbered from 1 in the 117-entry gpu03 list of 2026-11-24.

| file_sha256 | commit | log entries (gpu03) | state |
|---|---|---|---|
| `2dec2ce133eb…` | `52d7910a` | 108, 109 (2026-11-22T22:58:39Z, 23:04:11Z) | pair A engines on `nearaidev/vllm@80176ef5` (no page) until entry 112; superseded by name |
| `9474d5cdb690…` | `ebd4081b` | 110, 112 (2026-11-23T05:34:27Z, 06:03:51Z) | pair A engines and registrar; differs from `6bcb69e3` in one admission limit; superseded by name at entry 114 |

A revision not listed under "audited revisions" has not been audited — the teemoon app
shows no audit link for it (fail-closed by design). `python3 tools/fleet_drift.py`
reports which revision each host is running now.
