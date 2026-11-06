# docker (Docker Inc. official CLI image)

The `docker` binary and a busybox shell — a conduit, no behaviour of its own. In scope only where a recipe
gives it the docker socket: the compose-manager token-rotation runbook
([`manifests/nearai/cvm-compose-files/prod/rotate-compose-manager-token/`](../../../../manifests/nearai/cvm-compose-files/prod/rotate-compose-manager-token/)).
Upstream third-party (github.com/docker-library/docker); no near.ai provenance attestation — identity is
the digest pin plus the builder-declared provenance and the Docker Hub tags that carry the digest.

## audited builds

| digest | build | verdict | review |
|---|---|---|---|
| [`sha256:851f91d24121...`](sha256-851f91d241214e7c6db86513b270d58776379aacc5eb9c4a87e5b47115e3065c.md) | `27.5.1-cli` (alpine 3.21), tags `27-cli` / `27.5-cli` / `27.5.1-cli` / `27.5.1-cli-alpine3.21`, built 2025-02-12 | QUALIFIED PASS — at its one deployed invocation this image contributes no behaviour of its own: the recipe replaces its entrypoint with sh -c and runs a script this run read in full, whose only use of the image… | 2026-11-06 |

A build not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
