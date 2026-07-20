# nearaidev/vllm-proxy-rs

The E2EE terminator: decrypts client requests inside the model enclave and forwards plaintext to the engine over the enclave-internal network. Highest-exposure image in the stack. Source: github.com/nearai/inference-proxy.

## audited builds

| digest | verdict | review |
|---|---|---|
| [`sha256:b183677a5d32...`](sha256-b183677a5d32267539b9b21ec45327a4f3be0a013afeb608c68c4d76e9472e36.md) | PRIVATE (2 opt-in egress caveats) | 2026-07-15 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
