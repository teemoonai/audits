# prod/GLM-5.3-Flash-SGL-TP2x3-W4AFP8-gpu04.yaml

A three-replica variant of [`GLM-5.3-Flash-SGL-TP2x4-W4AFP8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8/)
for the gpu04 CVM only: the fleet file with the fourth replica (GPUs 6-7) and its
entry in the proxy's backend list removed, so that GPU 6 is free for the separate
`sage` project that near.ai runs beside it on that host (the file's own header says
"never deploy a 4-replica file to gpu04 while the sage project runs"). Everything
else — the three TP2 replicas on near.ai's signed `nearaidev/sglang` HiCache build,
the proxy, nginx, the registrar, the ghost-cache sidecar, dcgm and the collector —
is byte-identical to the sibling at the revision each page names.

Identity for every revision below is **log-pinned**: the file's `file_sha256`
against the signed compose-manager action log (commit + path + file hash), not
hardware-measured; the measured layer is the node harness under
[`../../../../measured/`](../../../../measured/). Per-image behavior is deferred
to the image pages each revision links.

Revisions are listed oldest first; a sibling review cites the plain file's page
for every block it proves byte-identical and still sweeps the whole file. The
verdict column is each page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`6dacc0c5300b…`](sha256-6dacc0c5300babc48ccef99cc86c9cfdea6b8cae1603f21c0c567e684cb0fcb4.md) | QUALIFIED PASS — sibling review against `a49d9c15`: r1-r3, both anchors, sidecar, collector, nginx, registrar and dcgm byte-identical; engine `fa730e6e` (v7), proxy `d61357da`; the sibling's qualifications carry on three engines; two gpu04 facts recorded — the third-party `sage` stack on GPU 6 (own bridge, no docker socket, LOW) and the v10 Q8 canary replica from an earlier file whose fate the attested log cannot settle (compose-manager's `--remove-orphans` under an unrecorded project) | 2026-10-22 |

A revision not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design). `python3 tools/fleet_drift.py` reports which
revision each host is running now.
