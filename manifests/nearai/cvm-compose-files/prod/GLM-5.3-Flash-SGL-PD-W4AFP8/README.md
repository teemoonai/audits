# prod/GLM-5.3-Flash-SGL-PD-W4AFP8.yaml

A **prefill/decode (P/D) qualification file**, not a serving config: generated from
[`GLM-5.3-Flash-SGL-TP2x4-W4AFP8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8/) for one drained
`glm-5-3-flash` host (gpu03). Eight sglang engines in prefill or decode mode on a stock
upstream `lmsysorg/sglang` image with no page, three PD routers, a TLS relay on host
ports 8008-8011 behind the proxy bearer token, dcgm and the collector. It has **no E2EE
proxy, no registrar and no production nginx**. Five revisions of it were brought up on
gpu03 on 2026-10-06 between 07:37Z and 14:37Z, by branch name from a development branch
(the path does not exist on `main`), while production on that CVM was down; the stack
was taken down by name at 15:32Z and the production file restored a minute later.

It has a page because one container name of one revision, `pd-router-3p1d`, has no
later logged up or down, and the client app counts every revision that may still run on
a host holding the `z-ai/glm-5.3-flash` key.

Identity for every revision below is **log-pinned**: the file's `file_sha256`
against the signed compose-manager action log (commit + path + file hash), not
hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

The verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`1229cea05316…`](sha256-1229cea053163a5e524690135232765de384ba00076b7675044a3f5470937569.md) | QUALIFIED PASS — for the one container this revision may still account for on the glm-5-3-flash gpu03 CVM, and by reachability, not by its image: pd-router-3p1d is an sglang prefill/decode router on lmsysorg/sglang b1259f3e, which has no page… | 2026-11-20 |

## revisions in the log with no page

Action-log entries in this table are numbered from 0 (the first entry is entry 0).

| file_sha256 | commit | log entries (gpu03) | state |
|---|---|---|---|
| `41bf814e0933…` | `bf4bc29a` | 149 | superseded by name |
| `5d0c19d9f2ac…` | `e3219fb0` | 150 | superseded by name |
| `c28905d4fd9c…` | `ec6b2a68` | 152, 153 | every container it named has a later by-name `compose_down` (154, 159) or, for the collector and dcgm, a later up from another file (160) |
| `7da6fb45825e…` | `0aac6906` | 155, 157, 158 | every container it created has a by-name `compose_down` (156, 159) |

A revision not listed under "audited revisions" has not been audited — the teemoon app
shows no audit link for it (fail-closed by design). `python3 tools/fleet_drift.py`
reports which revision each host is running now.
