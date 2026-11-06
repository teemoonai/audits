# prod/GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8-gpu04-3B1L.yaml

The gpu04 variant of [`GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8`](../GLM-5.3-Flash-SGL-TP2x4-W4AFP8-V12Q8/):
"3 base + 1 long" — the three base-tier TP2/EP2 replicas r1-r3 of the V12Q8 lineage on near.ai's
signed [`nearaidev/sglang`](../../../../../images/docker.io/nearaidev/sglang/) v12 build, plus a fourth
engine `l4` running gpu23's long-context argv (1M-token context, HiCache in host RAM) and a second E2EE
proxy `proxy-glm53-long` that fronts it alone, so that `glm-5-3-flash-long` is served from gpu04 as well
as from gpu23. The file replaced the Q8Canary replica r4 on 2026-11-04 (downed at 22:28Z, l4 up at
22:30Z) and re-created the proxy, nginx, registrar and collector on 2026-11-05.

Identity for every revision below is **log-pinned**: the file's `file_sha256` against the signed
compose-manager action log (commit + path + file hash), not hardware-measured; the measured layer is the
gpu04 node harness under [`../../../../measured/`](../../../../measured/). Per-image behavior is
deferred to the image pages each revision links.

Revisions are listed oldest first; a sibling review cites the sibling's page for every block it proves
byte-identical and still sweeps the whole file. The verdict column is each page's own `## verdict:`
line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`6ce091c9c12d…`](sha256-6ce091c9c12d2024263fa54d3ccc2a9a54ecf04d13de203989ed0b1fe344ff1a.md) | QUALIFIED PASS — against the audited sibling 904054f5 this file adds one engine and one E2EE terminator to gpu04 and changes nothing that writes message plaintext to a sink: l4 is gpu23's audited long replica argv on the same PRIV… | 2026-11-06 |
