# nearaidev/compose-manager

Model-node deployer: pulls stack YAMLs from nearai/cvm-compose-files, runs compose up/down, maintains the signed action log the client verifies. Control-plane; no data-plane role. Source: github.com/nearai/compose-manager.

## audited builds

| digest | verdict | review |
|---|---|---|
| [`sha256:b487f39160e9...`](sha256-b487f39160e9a53c3d98943a9c709d28e12babef75e0bb5a6cd5692abc8b2db6.md) | COMPROMISABLE by credentialed operator | 2026-07-15 |
| [`sha256:5165400d9eb4...`](sha256-5165400d9eb43ab5da36986a85de0ba55f3fb4d05211c4397ecc4bde3ef0113b.md) | COMPROMISABLE by credentialed operator (control-plane; no data-plane role) — `69c363ea` | 2026-08-03 |

**Observed, not audited:** a launcher-swapped build (`sha256:6e035c8fb99c...`) has been running on at least one node since 2026-07-02.

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
