# docker.io/levantolabs/sage2-hopper-pod

"Sage 2" by Levanto Labs: a third-party model pod that near.ai hosts inside the small-models confidential VM (cm-gpu13). It is not on the path of the near.ai models teemoon talks to; it runs beside them. The image is private, so its contents cannot be reviewed: the page below is INCONCLUSIVE on the image, makes no privacy claim about it, and records the configuration it runs under. It is not gated in `index.json`, so the teemoon app shows no audit link for it, and it is listed in [`acknowledged.json`](/acknowledged.json) as a known open item.

| digest | verdict | review |
|---|---|---|
| [`sha256:b5268f0a1bdd...`](sha256-b5268f0a1bddf96895baf7b38f28cf814eaecc79d832d5660f4155584506009e.md) | INCONCLUSIVE — the image could not be obtained and was not read; configuration-level record only (own network, no Docker socket, socket filter allowing only Info and GetQuote; it can obtain hardware quotes for the CVM with report data of its own choosing) | 2026-11-19 |
