# nvidia/k8s/dcgm-exporter

GPU-telemetry exporter (node inner compose). Runs `SYS_ADMIN` + nvidia runtime over all GPUs; metrics-only surface at audited config. **Pinned by tag, not digest** — the attested manifest fixes the tag string only, so the registry can serve different bytes under a listed tag. Entries below are therefore *tag* identities: they cover deployed configuration, never bytes.

## audited builds

| tag | verdict | review |
|---|---|---|
| [`4.5.2-4.8.1-distroless`](tag-4.5.2-4.8.1-distroless.md) | telemetry-not-content at audited config; GPU-privileged, tag can drift | 2026-07-23 |
| [`sha256:ed594cf53fe6...`](sha256-ed594cf53fe6942e84b07b0740cdcbb249fa4b39cb21feeebf93881ae51f0b5e.md) (digest-pinned build of the same tag) | telemetry-not-content at deployed config; GPU-privileged; bytes pinned | 2026-08-04 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
