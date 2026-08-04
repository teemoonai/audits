> **teemoonai/audits** - the tool-independent audit method.
> From the teemoon privacy-audit run of 2026-07-15. Method: [/notes/method.md](/notes/method.md).

# Plaintext-Privacy Source Audit — near.ai Inference Path

A **tool-independent** procedure for auditing whether your plaintext chat
messages are logged, persisted, or exposed to any actor besides the model
and you. The audit is deliberately portable: it pins the exact source
commits deployed in production, so anyone — a different LLM/agent, an
independent security reviewer, or you — can run the identical review and
compare results. The audit's credibility must not depend on trusting any
one tool (including Claude Code / Fable).

> Scope is the **inference path** only: the code that can observe a message
> in transit or at rest between your device and the model. It complements
> `TEE_STACK_EXPLAINED.md` §7 (audit playbook) with concrete, versioned
> targets.

> **Findings from running this procedure:**
> [`PRIVACY_AUDIT_RESULTS.md`](PRIVACY_AUDIT_RESULTS.md) — the completed report
> (gateway + model node + SGLang engine source + teemoon client), generated
> 2026-07-13 – 2026-07-15 with Claude Code (Claude Opus 4.8 / Claude Fable 5).
> This document is the *method*; that one is the *result* — re-run this procedure
> yourself and compare, rather than taking the result on trust.

---

## 1. Threat model the audit must answer

**"Private"** here means: message plaintext is visible only to (a) you and
(b) the model process performing inference — and to no other actor, where
"other actor" includes near.ai operators, cloud staff, telemetry/observability
backends (Datadog, OpenTelemetry sinks), logs, on-disk caches, crash dumps,
or any network egress other than the legitimate model round-trip.

The TEE hardware already guarantees the *box* is sealed against the host
operator (see `TEE_STACK_EXPLAINED.md`). This audit addresses the
**orthogonal** question the hardware cannot: does the code *inside* the box
handle plaintext safely, or does it copy it somewhere observable?

Where plaintext legitimately exists:
- the **inference engine** (must — it reads your prompt);
- **cloud-api / cvm-ingress** on the **degraded (non-E2EE) path** only —
  with E2EE, these see ciphertext encrypted to the model's key.

Everywhere else, plaintext is a finding.

---

## 2. Exact audit scope (pinned production commits)

Captured from live attestation on 2026-07-13. **Re-derive these yourself**
before trusting the table (§5) — do not take this file's word for it.

| Image | Host / role | Source to audit | Plaintext exposure |
|---|---|---|---|
| `nearaidev/cloud-api` | gateway — API router | `github.com/nearai/cloud-api` @ `dac10078da8d` | plaintext on degraded path; else ciphertext + metadata |
| `nearaidev/cvm-ingress` | gateway — TLS ingress | `github.com/nearai/cvm-ingress` @ `6b1b58c9cf63` | terminates TLS; sees the raw HTTP stream |
| `nearaidev/dstack-vpc` | both — CVM↔CVM mesh | `github.com/nearai/dstack-vpc` @ `931ea22ff1cb` | ciphertext in transit (verify it's actually encrypted) |
| `nearaidev/dstack-vpc-client` | gateway — mesh client | `github.com/nearai/dstack-vpc-client` @ `eafa4b675d52` | ciphertext in transit |
| `nearaidev/compose-manager` | model node — deployer | `github.com/nearai/compose-manager` @ `3d64349a6c71` | no messages; controls what runs (supply chain) |
| `nearaidev/compose-manager-launcher` | model node — launcher | `github.com/nearai/compose-manager` @ `9a035b2fadff` | no messages; supply chain |
| `nearaidev/vllm-proxy-rs` | inference layer — engine proxy | `github.com/nearai/inference-proxy` @ `372824b455f0` | **plaintext** — proxies requests to the engine |
| inference engine (`*-patched:local`) | inference layer — the model | config: `github.com/nearai/cvm-compose-files` @ `c545c95545db`, `prod/GLM-5.1-SGL-AWQ-TP4.yaml`; engine is SGLang built in-enclave | **plaintext** (legitimate) — audit launch flags + engine version |

Third-party sidecars in the manifests (`datadog/agent`,
`otel/opentelemetry-collector-contrib`, `certbot/dns-cloudflare`, `alpine`,
`nginx`, `curlimages/curl`) are **not** source-audited — audit their
*configuration* in the attested compose files instead (§4, telemetry).

Highest priority, in order: **inference engine config → vllm-proxy-rs →
cloud-api → cvm-ingress**, then the mesh, then compose-manager (supply chain).

> **Before reviewing anything, walk [`/notes/audit-surface.md`](/notes/audit-surface.md).**
> This document says *what* to look for; that one says *where*, and every item on
> it exists because a finding actually came from it. It was written after a
> controlled comparison ([`/notes/reviewer-comparison-2026-08-03.md`](/notes/reviewer-comparison-2026-08-03.md))
> showed two independent reviewers converging on a headline finding while
> diverging on coverage — one missed a live token-ID leak in an area it had
> marked "not traced". The checklist turns "did the reviewer think to look" into
> "did the reviewer finish the list", and it starts with **establishing image
> identity**, because a review keyed to the wrong tree is worse than no review.

---

## 3. The portable audit prompt

Paste the block below into any capable coding agent or LLM with code-reading
tools, hand it to a human reviewer, or adapt it for static-analysis tooling.
It is self-contained and names no specific tool.

```text
You are performing a defensive privacy audit of open-source code. Goal: determine
whether a user's plaintext chat messages could be logged, persisted to disk,
transmitted to any telemetry/observability backend, or otherwise made visible to
any actor other than (a) the end user and (b) the model process doing inference.
This is authorized review of public source code to verify a vendor's privacy claim.

SYSTEM CONTEXT
- A confidential-computing LLM inference service. Requests may be end-to-end
  encrypted (E2EE) to the model's key; when E2EE is unavailable the request
  transits the gateway in plaintext ("degraded path").
- Two machines, each a sealed VM: a GATEWAY (API router, TLS ingress, mesh) and
  a MODEL NODE (deployer + inference engine + engine proxy). An encrypted mesh
  links them.
- "Private" = message plaintext is visible ONLY to the user and the inference
  engine process. Any copy of plaintext reaching a log, file, database, cache,
  crash dump, telemetry exporter, or non-model network destination is a FINDING.
- Plaintext legitimately exists in: the inference engine (required); the gateway
  API + ingress ONLY on the degraded (non-E2EE) path. Anywhere else is a finding.

TARGETS (audit each at the EXACT commit given)
  cloud-api            github.com/nearai/cloud-api            @ dac10078da8d
  cvm-ingress          github.com/nearai/cvm-ingress          @ 6b1b58c9cf63
  dstack-vpc           github.com/nearai/dstack-vpc           @ 931ea22ff1cb
  dstack-vpc-client    github.com/nearai/dstack-vpc-client    @ eafa4b675d52
  compose-manager      github.com/nearai/compose-manager      @ 3d64349a6c71 and @ 9a035b2fadff
  inference-proxy      github.com/nearai/inference-proxy      @ 372824b455f0   (image "vllm-proxy-rs")
  cvm-compose-files    github.com/nearai/cvm-compose-files    @ c545c95545db   (file prod/GLM-5.1-SGL-AWQ-TP4.yaml)
Obtain each with:  git clone <url> && cd <repo> && git checkout <commit>
For cvm-compose-files, read the named YAML: it defines the inference engine's
image build and launch arguments.

WHAT TO LOOK FOR (trace the message; for each hit cite file:line)
1. Logging of content: any log/trace/print statement whose arguments include a
   request body, response body, message, prompt, completion, or decrypted
   buffer. Note the log level and whether an env var / config flag can raise
   verbosity to include bodies.
2. Persistence: writes of message content to files, databases, key-value stores,
   disk caches, prompt caches, or temp files. Include crash/panic handlers that
   might dump buffers containing plaintext.
3. Telemetry content: what is handed to metrics/tracing/observability SDKs
   (OpenTelemetry, Datadog, spans, attributes, events). Metrics/counters are
   fine; message content in span attributes or log exports is a finding.
4. Network egress: enumerate every outbound destination each process that can
   see plaintext may connect to. The only legitimate destinations are the model
   round-trip and the encrypted mesh. Anything else (analytics, error reporting
   like Sentry, webhooks) that could carry content is a finding.
5. Degraded-path handling (cloud-api, cvm-ingress): when E2EE is off, are request
   bodies treated as opaque byte streams passed straight through, or are they
   parsed, buffered to disk, or retained?
6. Env-injectable debug: any environment variable or runtime config that switches
   on body/prompt logging or a debug dump. Cross-reference the attested compose
   files' `allowed_envs` — an operator can set only those without changing the
   hardware measurement; flag any that flips a content-logging switch.
7. Mesh confidentiality (dstack-vpc / -client): confirm inter-node traffic is
   actually encrypted (which cipher/handshake), and that there is no
   packet-capture, mirror, or debug-dump path.
8. Supply chain (compose-manager): what compose files it will launch and from
   where; whether it validates/attests them before launch; whether an operator
   can inject arbitrary images or env post-attestation.
9. Inference engine config (cvm-compose-files YAML): the engine's launch flags —
   specifically any request-logging / prompt-logging / debug flag (e.g. vLLM or
   SGLang flags that echo prompts), disk cache locations, and whether telemetry
   sidecars in that compose receive request content.

RULES
- Cite concrete evidence (file:line + a one-line quote) for every finding.
- Distinguish clearly between "code CAN see plaintext" (structural) and "code
  LOGS / PERSISTS / EXFILTRATES plaintext" (the actual privacy risk). Only the
  latter is a finding; the former is context.
- Report uncertainty explicitly; do not assert safety you did not verify.
- Absence of evidence is not proof — if a path is too large to fully trace, say so.

OUTPUT
- Per repo: files reviewed, and a list of findings each tagged
  CRITICAL (plaintext leaves the trust boundary) / HIGH (plaintext logged or
  persisted inside the enclave) / MEDIUM (content in telemetry) /
  INFO (structural exposure, no leak) with file:line evidence.
- A final verdict per repo: PRIVATE / LEAKS (with what, where) / INCONCLUSIVE.
- An overall verdict for the inference path, and a list of anything you could
  not conclusively verify.
```

---

## 4. Manifest-only checks (no source needed)

Some assurance comes straight from the attested compose files — verify these
directly, they need no code reading and are hard evidence:

- **`allowed_envs`** in each dstack wrapper: the complete list of env vars an
  operator can set without changing the hardware measurement. Confirm none
  names a debug/log-level/log-bodies switch.
- **volumes / mounts**: every durable writable path a plaintext-handling
  service touches needs justification.
- **telemetry pipelines**: the Datadog/OTel service configs in the compose —
  confirm they scrape metrics only, and that no receiver ingests request
  content.
- **egress**: ports and destinations declared per service.

---

## 5. Reproducing the scope (don't trust §2's table)

The pinned commits above must be independently re-derivable, or the audit
rests on trusting this document. To regenerate them from live attestation:

1. Fetch both reports with a fresh nonce:
   - `GET https://cloud-api.near.ai/v1/attestation/report?model=<model>&signing_algo=ecdsa&nonce=<hex>`
   - `GET https://<slug>.completions.near.ai/v1/attestation/report?signing_algo=ecdsa&nonce=<hex>`
2. Extract the compose manifests
   (`gateway_attestation.info.tcb_info.app_compose` and the model node's
   `info.tcb_info.app_compose`), and the inner compose via the
   `compose_manager_attestation` action log (`file` + `commit`, fetched from
   `nearai/cvm-compose-files` and hash-checked against `file_sha256`).
3. For each `nearaidev/*@sha256:<digest>`, query
   `GET https://api.github.com/repos/nearai/<repo>/attestations/sha256:<digest>`
   and read `predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit`
   from the (base64) DSSE payload — that is the commit to audit.
   (Repo name = image basename, with aliases `compose-manager-launcher →
   compose-manager`, `vllm-proxy-rs → inference-proxy`.)

teemoon's `teemoon_verify.py` (the self-verify script) performs steps 1–3 for
verification; the same values feed this audit. If your regenerated commits
differ from §2, near.ai has redeployed — audit *your* commits, and note the
drift.

---

## 6. Interpreting results

- **PRIVATE across the path** → plaintext is confined to the inference engine
  (and the degraded gateway path, as opaque bytes), with no logging /
  persistence / telemetry-content / rogue egress. Combined with the hardware
  seal, this is the strong result: private from everyone outside the box, and
  the code inside the box provably doesn't copy plaintext out.
- **LEAKS** → name the exact sink (log line, file, telemetry attribute, egress
  destination) with file:line. A leak inside the enclave still exposes
  plaintext to whoever can read that sink (e.g. a telemetry backend), which is
  precisely an "other actor."
- **INCONCLUSIVE** → list what could not be traced. Honest gaps are part of the
  result; the point of the portable prompt is that independent runs converge.

Residual trust the audit cannot remove (see `TEE_STACK_EXPLAINED.md`):
third-party sidecar *source*, GitHub Actions as trusted builder (no
reproducible builds), and metadata (timing, sizes, API-key identity) which is
outside message-content privacy entirely.
