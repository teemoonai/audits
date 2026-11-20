# prod/GLM-5.3-Flash-SGL-TP4-W4AFP8.yaml

The first **W4AFP8 base-tier** recipe for `z-ai/glm-5.3-flash`: generated from
[`GLM-5.3-Flash-SGL-TP4`](../GLM-5.3-Flash-SGL-TP4/) for 8x H200 hosts, two sglang
TP4/EP4 engines (GPUs 0-3 and 4-7) behind one E2EE-terminating `vllm-proxy-rs`, with
nginx, the registrar, dcgm and the collector. Its engine image,
`nearaidev/sglang@sha256:8bce6a7c…`, **has no page**. On the `glm-5-3-flash` gpu03 CVM
it was the serving recipe from 2026-09-23 to 2026-10-02, when
[`GLM-5.3-Flash-SGL-TP2x4-W4AFP8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8/) (four TP2
engines on the same GPUs) replaced it.

It has a page because the two engine containers of its first revision,
`model-sg-glm53-w4afp8-tp4-r1` and `-r2`, have no later logged up or down, and the
client app counts every revision that may still run on a host holding the
`z-ai/glm-5.3-flash` key.

Identity for every revision below is **log-pinned**: the file's `file_sha256`
against the signed compose-manager action log (commit + path + file hash), not
hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

The verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`bcd313cf7117…`](sha256-bcd313cf7117b82f0f850f9b93da06a4129a3073ae4a58c017a3723eb30a7255.md) | QUALIFIED PASS — for what this revision can still expose on the glm-5-3-flash gpu03 CVM today, stated as a reachability and resource result and not as a result about its engine image: model-sg-glm53-w4afp8-tp4-r1 and -r2 run nearaidev/sglang 8bce6a7c, which has no page… | 2026-11-20 |

## revisions in the log with no page

Action-log entries in this table are numbered from 1 (the first entry is entry 1).

| file_sha256 | commit | log entries (gpu03) | state |
|---|---|---|---|
| `1528ba57ffed…` | `b996e382` | 130 | scoped to `proxy-glm53`, re-created by name at 134 and from other files since |
| `4247dec8b67e…` | `81ea8f03` | 131 | scoped to `nginx`, re-created by name at 134 and from other files since |
| `dec66aa4f0d7…` | `e7a3faba`, `b177e78b` | 134, 135 | scoped to `nginx`, `proxy-glm53` and `otelcol-contrib`; all three re-created from other files since (136 onward) |

All three declare the two tp4 engines with a definition equal to `bcd313cf`'s and
never named them in an up, so the engine containers are that page's.

A revision not listed under "audited revisions" has not been audited — the teemoon app
shows no audit link for it (fail-closed by design). `python3 tools/fleet_drift.py`
reports which revision each host is running now.
