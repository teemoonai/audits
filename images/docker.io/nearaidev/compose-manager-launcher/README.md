# nearaidev/compose-manager-launcher

Watchdog that swaps/rolls back compose-manager itself (cosign-gated to nearai/compose-manager workflows). High privilege, no data-plane role. Source: github.com/nearai/compose-manager.

## audited builds

| digest | verdict | review |
|---|---|---|
| [`sha256:78afb8233013...`](sha256-78afb82330137c2fd90a9c8c6e452f8f178c15d863f87c079a11c13e92216e00.md) | COMPROMISABLE by credentialed operator (shared verdict) | 2026-07-15 |
| [`sha256:91fdff3cfa35...`](sha256-91fdff3cfa3543d72656b2368c7d8a0a83d95a0f1087378c897aa1537acdba56.md) | COMPROMISABLE by credentialed operator — the post-attestation mutation engine; no plaintext reach — `8e07c358` | 2026-08-03 |
| [`sha256:d652f92b64f5...`](sha256-d652f92b64f57ef8aa086bd77a4cf932c1976965b3cea2814a7ee82fe73aa993.md) | **INCONCLUSIVE** — no build attestation, source unresolvable; makes no privacy claim and is **not gated**. Gone from the fleet since 2026-08-17 | 2026-08-03 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
