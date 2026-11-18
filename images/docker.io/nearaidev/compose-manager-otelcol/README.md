# docker.io/nearaidev/compose-manager-otelcol

The management telemetry collector that the compose-manager launcher runs beside the manager on the newer harness template (first seen 2026-11 on the two DeepSeek CVMs). Upstream `otel/opentelemetry-collector-contrib` plus one near.ai layer, a baked-in config. Built by `nearai/compose-manager`'s `build.yml`: its signed build attestation is published under **that** repository, not under one named after the image.

| digest | verdict | review |
|---|---|---|
| [`sha256:3a9ac823d90e...`](sha256-3a9ac823d90e24e0f4b6aad8fd4af6a7b914411b8592e4451daa0d17d6271ce3.md) | QUALIFIED PASS — at the measured configuration this collector exports only the stdout of compose-manager, the launcher and certbot, plus host and container metrics, to telemetry.infra.near.ai; every other container's log lines, the eng… | 2026-11-19 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
