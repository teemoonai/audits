# nearaidev/vllm-proxy-rs

The E2EE terminator: decrypts client requests inside the model enclave and forwards plaintext to the engine over the enclave-internal network. Highest-exposure image in the stack. Source: github.com/nearai/inference-proxy. Every build here carries a **signed GitHub build attestation** — the strongest identity in this repo — and each page's `sources` pin is that attested commit.

## audited builds

| digest | verdict | review |
|---|---|---|
| [`sha256:b183677a5d32...`](sha256-b183677a5d32267539b9b21ec45327a4f3be0a013afeb608c68c4d76e9472e36.md) | PRIVATE (2 opt-in egress caveats) | 2026-07-15 |
| [`sha256:b0c5cd0786b1...`](sha256-b0c5cd0786b19dfa46144107be15e340b7a338b1c341d02ffa994c9f1ea77dfd.md) | core request path clean; two client-opt-in egress caveats (web search, fusion) — signed attestation → `48d7e349` | 2026-08-03 |
| [`sha256:e665ebb9998f...`](sha256-e665ebb9998fcf333a1611ecb4c49bd209b90aa9e09547ed792bd0436b132f30.md) | QUALIFIED PASS — DP-affinity key is a salted digest confined to memory; attribution diagnostics emit bounded labels; opt-in caveats carry — signed attestation → `101aa49f` | 2026-09-01 |
| [`sha256:27265f5a10ab...`](sha256-27265f5a10abcacc3fe80604a00ed2ba32c6e082895115e4b652b40525cb554d.md) | QUALIFIED PASS — backend conversation affinity reuses the salted, memory-only conversation digest; SSE watchdog change content-free; opt-in caveats carry — signed attestation → `c59ea60e`; declared by the GLM-5.3 `e5d80ab6` revision but the proxy container was last recreated from `98b57ad7` | 2026-09-10 |
| [`sha256:98b57ad7aa4f...`](sha256-98b57ad7aa4f9afd8ffff3ac9f4773303997f667e1d221be076c2f064e4a1284.md) | QUALIFIED PASS — refuses /v1/responses in the catch-all before the body is read, no new sink; opt-in caveats carry; fleet-wide on 15 hosts — signed attestation → `ee53bec3` | 2026-09-10 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
