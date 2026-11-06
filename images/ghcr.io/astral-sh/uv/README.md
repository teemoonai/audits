# ghcr.io/astral-sh/uv

Astral's `uv` on a Debian python image — a script runtime. Out of scope as the fleet's model
downloaders (one-shots that fetch weights and exit, touching no request); in scope where a recipe gives
it the host PID namespace, the guest root or the docker socket — the host-metrics exporter of the gpu23
bench file
([`manifests/nearai/cvm-compose-files/experiments/GLM-5.3-gpu23-local-engine-bench/`](../../../../manifests/nearai/cvm-compose-files/experiments/GLM-5.3-gpu23-local-engine-bench/)).
Upstream third-party (github.com/astral-sh/uv); identity from the image's own OCI labels, self-asserted.

## audited builds

| digest | build | verdict | review |
|---|---|---|---|
| [`sha256:4f5d923c9dce...`](sha256-4f5d923c9dcea037f57bda425dd209f3ec643da2f0b74227f68d09dab0b3bb36.md) | `0.9.30-python3.11-bookworm-slim`, revision `ea456083`, built 2026-02-04 | QUALIFIED PASS — at the deployed script the exporter reads /proc memory counters and two container inspects and serves them as Prometheus gauges on port 9101 to the compose bridge: no message content, no engine… | 2026-11-06 |

A build not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
