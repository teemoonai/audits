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
| [`sha256:d61357da3991...`](sha256-d61357da39918a57126864a451eaf054f06a6989c03fe9a1666f7e6374ba6907.md) | QUALIFIED PASS — 77-commit delta adds gateway-mode machinery (admission, context tiers, replica-state publishing) with no content sink at the deployed env; the catch-all route is deleted, unknown routes fail closed; opt-in caveats carry; fleet-wide on 11 hosts — signed attestation → `0f37728a` | 2026-10-02 |
| [`sha256:295f16f892d7...`](sha256-295f16f892d7e2f7c59e54354007762b5f0054d00467d42183f95d1596d8c916.md) | QUALIFIED PASS — 45-file delta adds a multi-model gateway list mode (refused at startup under OHTTP), per-model metric labels, usage-report retry delivery and a first-token deadline, with no content sink at the deployed env; web search (CRITICAL, armed) and fusion (HIGH, armed) remain client-opt-in plaintext egress gated by unattested host env; glm-5-3-flash — signed attestation → `1f0cfb71` | 2026-10-22 |
| [`sha256:e4a42b327523...`](sha256-e4a42b327523e304c0fc389f656ba7a02fd7b3d4a38cdc822f9288fd193a525a.md) | QUALIFIED PASS — the 295f16f8 build plus one commit (PR 311: optional per-request result count, 0–20, on web_context_search); only new sink is a debug line with a tool name and id; glm-5-3-flash-long — signed attestation → `f18298f4` | 2026-10-22 |

A build not listed here has not been audited - the teemoon app shows no audit link for it (fail-closed by design).
