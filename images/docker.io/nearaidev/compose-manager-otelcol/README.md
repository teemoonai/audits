# docker.io/nearaidev/compose-manager-otelcol

The management telemetry collector that the compose-manager launcher runs beside the manager on the newer harness template (first seen 2026-11 on the two DeepSeek CVMs). Upstream `otel/opentelemetry-collector-contrib` plus one near.ai layer, a baked-in config. Built by `nearai/compose-manager`'s `build.yml`: its signed build attestation is published under **that** repository, not under one named after the image.

| digest | verdict | review |
|---|---|---|
| [`sha256:3a9ac823d90e...`](sha256-3a9ac823d90e24e0f4b6aad8fd4af6a7b914411b8592e4451daa0d17d6271ce3.md) | QUALIFIED PASS — at the measured configuration this collector exports only the stdout of compose-manager, the launcher and certbot, plus host and container metrics, to telemetry.infra.near.ai; every other container's log lines, the eng… | 2026-11-19 |
| [`sha256:ac9b349081fc...`](sha256-ac9b349081fc86413c2e25b44558daa14e8b33669f9e50fc0fec92dc77ce768a.md) | QUALIFIED PASS — a rebuild of the 3a9ac823 collector at a later commit with the same collector config byte for byte and the same upstream base digest; none of the 62 hunks between the two commits reaches this image … | 2026-11-20 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
