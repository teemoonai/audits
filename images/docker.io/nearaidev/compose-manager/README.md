# nearaidev/compose-manager

Model-node deployer: pulls stack YAMLs from nearai/cvm-compose-files, runs compose up/down, maintains the signed action log the client verifies. Control-plane; no data-plane role. Source: github.com/nearai/compose-manager.

## audited builds

| digest | verdict | review |
|---|---|---|
| [`sha256:b487f39160e9...`](sha256-b487f39160e9a53c3d98943a9c709d28e12babef75e0bb5a6cd5692abc8b2db6.md) | COMPROMISABLE by credentialed operator | 2026-07-15 |
| [`sha256:5165400d9eb4...`](sha256-5165400d9eb43ab5da36986a85de0ba55f3fb4d05211c4397ecc4bde3ef0113b.md) | COMPROMISABLE by credentialed operator (control-plane; no data-plane role) — `69c363ea` | 2026-08-03 |
| [`sha256:6e035c8fb99c...`](sha256-6e035c8fb99c1d31f41760d25af178683a658cca4afd73cd0d366fbb5bf884be.md) | COMPROMISABLE by credentialed operator (control-plane; no data-plane role) — wider blast radius than the earlier builds; **signed** build attestation, `f91a2045` (the measured harnesses' pinned `COMPOSE_MANAGER_IMAGE` default) | 2026-08-03 |
| [`sha256:a320bb488234...`](sha256-a320bb4882341c8e19ef1944436f6591ed73303732009ed5db9f6db6c9da756a.md) | COMPROMISABLE by credentialed operator (control-plane; no data-plane role) — the 6e035c8f findings carry; new: the first implemented cross-container file read (`docker cp -L` of the CVM's `completions.near.ai` TLS key out of certbot, fixed target at the deployed env) and `/compose/logs` reaching any non-reserved compose project; TLS on the API port, constant-time multi-token auth, the compose project pinned on every call — but the attested action log still records neither the project nor the env overlay; **signed**, `be649f88` (= `754d65c3` + one CI workflow file); the default manager on the cm-gpu32-g7 harness and the boot-time override on the two glm-5-3-flash harnesses | 2026-10-30 |
| [`sha256:a0c073085684...`](sha256-a0c073085684e12e19f31bb279fc8da663a374199bfecc47b04167ae79eaa766.md) | COMPROMISABLE by credentialed operator (control-plane; no data-plane role) — every a320bb48 finding carries unchanged at new lines; the delta is a hardening pass (request-path, tag and service-name validation, the raw fetch pinned… | 2026-11-06 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
