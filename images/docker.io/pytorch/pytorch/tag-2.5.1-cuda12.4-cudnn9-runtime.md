# pytorch/pytorch : 2.5.1-cuda12.4-cudnn9-runtime

## verdict: QUALIFIED PASS at configuration and inline-source level — the measured file embeds the privacy filter's entire application source, and that source logs, stores, and transmits no message content; but the build stands on a mutable base tag plus unpinned pip installs, so nothing binds this review to the bytes actually running

| | |
|---|---|
| **image** | `pytorch/pytorch` (docker.io) — build base for `privacy-filter-hf`, an in-enclave `dockerfile_inline` build with no registry identity of its own |
| **tag** | `2.5.1-cuda12.4-cudnn9-runtime` — **no digest anywhere in the attestation chain**; the measured compose pins the tag string only (identity class UNRESOLVED, rung 5 — `resolve_identity.py` refuses this ref because it requires `<image>@sha256:<64hex>`) |
| **seen in** | [`nearai/cvm-compose-files` @ `6a284da3`, `prod/small-models.yaml` line 247](https://github.com/nearai/cvm-compose-files/blob/6a284da32cbd385192d3d9de96f48af2d5794cbc/prod/small-models.yaml#L247) — the measured inner compose of the small-models nodes, live on 9 hosts (flux2-klein, gemma-4-31b, gpt-oss-120b, privacy-filter, qwen3-6-35b, qwen3-embedding, qwen3-reranker, qwen3-vl-30b, whisper-large-v3 — `<name>.completions.near.ai`) |
| **file identity** | `file_sha256 = a385f19a51054767b8be49a64ebc3111e0e62f721a861e54c78984b186904599` — re-verified locally (`shasum -a 256` of the file fetched at commit `6a284da3` ✓); matches the `file_sha256` in the signed `compose_up` action log per the orchestrator's attestation capture |
| **source** | base: PyTorch official Docker Hub image (closed build pipeline, no attestation). Application: **inline in the measured file** — `server.py`, lines 254-412, pinned by `file_sha256` |
| **build attestation** | none for the base. Docker Hub resolves this tag **today (2026-08-07)** to `sha256:c8268a92a69bd500f8be0e665b2630ee006dadaf7bfbc24249141b15ff622755` (verified against `registry-1.docker.io` during this review) — that is today's answer, **not** the bytes any running enclave built from; the registry can serve different bytes under this tag with no trace in the attestation chain |
| **review** | reviewed 2026-08-07 (independent AI source review, Fable — method: [/notes/method.md](/notes/method.md)) |

**coverage:** configuration-level plus inline-source. The reviewed artifacts are the hash-pinned compose configuration around the tag and the complete embedded application source (`server.py`, 159 lines) — the base image bytes, and the PyPI packages resolved at build time, were **not** and cannot be reviewed, because no digest or lockfile pins them. This page covers the configuration around the tag, never the bytes behind it.

---

## role

Build base for `privacy-filter-hf` — the PII classifier of the small-models fleet. The service (`x-privacy-filter-common`, [lines 239-445](https://github.com/nearai/cvm-compose-files/blob/6a284da32cbd385192d3d9de96f48af2d5794cbc/prod/small-models.yaml#L239); instantiated once, as `model-privacy-filter`, line 1253) runs a HF `token-classification` pipeline over full request text and returns PII spans. It is the **PII-densest plaintext process on the node**: a privacy filter sees user content by definition, so what it does with that content is the entire question this page answers.

Request path: nginx `:8007` (line 2296) → `proxy-privacy-filter` ([`vllm-proxy-rs@b183677a`](/images/docker.io/nearaidev/vllm-proxy-rs/sha256-b183677a5d32267539b9b21ec45327a4f3be0a013afeb608c68c4d76e9472e36.md), `OHTTP_ENABLED=true` line 1227, `VLLM_BASE_URL=http://model-privacy-filter:8000` line 1231) → this container's `uvicorn` on `:8000` (CMD, line 414). Registered as `privacy-filter.completions.near.ai` (line 2219). GPU 7, shared with five other services (device_ids `["7"]`, line 444).

## review — the inline application source (lines 254-412, pinned by the measured hash)

This is the unusual case where the application source is *inside* the hash-verified manifest: `COPY <<'PYEOF' /app/server.py` (line 254). The 159 lines were read in full. Tracing request content end to end:

- **Input:** `POST /v1/privacy/classify` takes `input: str | list[str]` (lines 346-348, 372-376). Text goes into `clf(texts, batch_size=BATCH_SIZE, stride=STRIDE)` (line 380) — the HF pipeline forward, under `torch.no_grad()` — and into one batched tokenizer call for usage counts (line 388). Nowhere else.
- **Logging of content: none.** The source contains no `print`, no `logging` import, no content-bearing write of any kind. The only writes to stderr are the GPU watchdog's numeric VRAM lines (`reserved %.1f GB > %.1f GB limit`, lines 332-336). The other route, `GET /v1/models` (351-353), returns a constant.
- **Verdict logging: none.** The classifier's output — PII spans with `text`, `category`, `score`, offsets (lines 392-409) — exists only in the HTTP response body (line 411), back through the proxy to the caller. Verdicts are not printed, not written to disk, not counted into metrics; `usage.input_tokens` (line 407) travels in-band only.
- **Persistence: none from request handling.** The only volume is `hugginface_cache:/root/.cache/huggingface` (line 416), written by the model download at startup — model artifacts, never request data. No temp files, no request dump feature, no cache keyed on input.
- **Crash paths: no dumps.** CUDA OOM in a request calls `torch.cuda.empty_cache()` then `os._exit(1)` (lines 381-385); the watchdog does the same on a VRAM limit breach (line 337). `os._exit` produces no traceback, no core, no buffer dump — the container just recycles under `restart: unless-stopped` (line 436). An unhandled exception would print a standard traceback (frame lines, not variable values) — no `--locals`-style anything exists here.
- **Outbound network in the handler path: none.** The source makes no network call after startup. Startup fetches are covered below.
- **Runtime knobs** (`PRIVACY_BATCH_SIZE/MAX_LENGTH/STRIDE`, `GPU_MEM_LIMIT_GB`, `WATCHDOG_INTERVAL_S`, lines 301-305, set at 428-435) bound batch size, chunk window, and the watchdog — none enables any logging or dump behavior; there is no debug switch in this program at all.

At the reviewed source, the answer to "what does the filter do with user content" is: classifies it in memory and returns the spans to the caller. Nothing else.

## where its stdout goes

The container logs via `json-file` (`logging: *logging-conf`, line 438 → anchor lines 1-6, which exposes the `com.datadoghq.ad.logs` label to the log pipeline). Its Datadog label (line 1257) tags it `model:openai/privacy-filter, deployment:small-models` — which means it **passes** otelcol's `filter/app_logs` (lines 2021-2030 drop only untagged/management containers) and ships: `otelcol-contrib` (digest-pinned, [audited](/images/docker.io/otel/opentelemetry-collector-contrib/sha256-85ac41c2db88d0df9bd6145e608a3cb023f5d8443868adbfbbf66efb51087917.md)) tails `/var/lib/docker/containers/*/*-json.log` (mount line 1404, receiver line 1464) and exports to the literal `https://telemetry.infra.near.ai` (line 2058, pipeline `logs/app` lines 2073-2076). The measured harness additionally runs a datadog-agent with container-collect-all, shipping the same stream to `us3.datadoghq.com` (that finding lives on the [manifest pages](/manifests/nearai/cvm-compose-files/prod/small-models/sha256-a385f19a51054767b8be49a64ebc3111e0e62f721a861e54c78984b186904599.md)). **No processor in either pipeline redacts content.**

So the guarantee "no content leaves via logs" is exactly equivalent to "this process never prints content". At the reviewed source that holds: stdout carries uvicorn access lines (client address, method, path, status — request bodies are never access-logged; the deployed CMD passes no `--access-log` change and no log-config), the numeric watchdog lines, and framework startup chatter. But the equivalence is only as strong as the *actual* uvicorn/transformers bytes — see the findings.

## startup egress and the model fetch (priority: is the model fetched at runtime?)

Yes. The image bakes no weights; `pipeline(model="openai/privacy-filter", revision="7ffa9a043d54d1be65afb281eddf0ffbe629385b", ...)` (lines 309-317) and the usage tokenizer (line 323) fetch from huggingface.co at container start (cache-miss), authenticated by `HF_TOKEN` (line 418), with `HF_HUB_OFFLINE=${HF_HUB_OFFLINE:-0}` (line 419) — a default, not a pin. Checked during this review: the pinned revision exists publicly and contains **no Python files and no `auto_map`** in `config.json` — only weights, tokenizer, and ONNX exports — so `trust_remote_code=True` (lines 316, 323) loads *no* repo code at this revision; the architecture (`OpenAIPrivacyFilterForTokenClassification`) resolves inside the installed `transformers` library. The revision pin is itself inside the hash-pinned inline source, so it cannot drift without changing `file_sha256`. This fetch happens before any request exists, so it cannot carry user content; what it *can* carry is hub telemetry metadata (`HF_HUB_DISABLE_TELEMETRY` is not set).

## findings

### HIGH (deployed: ARMED) — mutable base tag: a registry re-push silently replaces every layer under the plaintext process, with no attestation trace (egress-capable code)

Line 247: `FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime` — tag only. The attestation chain pins the *recipe* (`file_sha256`), and the recipe pins a *mutable name*. Whoever controls what Docker Hub serves under this tag (Docker Hub itself, the PyTorch org, or a credential thief) chooses the OS, Python, and CUDA userspace beneath the PII classifier at the next build, and neither manifest, measurement, nor action log would change. Today (2026-08-07) the tag resolves to `sha256:c8268a92a69bd500f8be0e665b2630ee006dadaf7bfbc24249141b15ff622755`; nothing establishes that any running node was built from those bytes, and this page deliberately does not audit them. ARMED, not ON: activation requires a registry-side swap (or simply a rebuild after one), and the current inline source on top would still have to be subverted by the swapped layers — which base layers trivially can (they provide `python`, `pip`, and every shared library the process loads).

**Positive control — the absence is a choice, not a parser artifact.** The same file at the same commit pins its other two in-enclave build bases by digest, verified in this run at their exact lines:

```
line 159:  FROM lmsysorg/sglang@sha256:8ece90ad52faa8b56149f0117227d9009db34513213e35990da468aeb6fe0b75
line 1177: FROM vllm/vllm-openai@sha256:ccd6a6dbf4aba4e94c6f7052d1835d6e742082b6a5095276552e9b7a5a47c2e5
line 247:  FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime
```

The file format, the tooling, and the authors demonstrably support digest-pinned `FROM` — this one base was left mutable. The fix is one line.

### HIGH (deployed: ARMED) — unpinned pip install resolves PyPI-latest into the plaintext process at every build (egress-capable code)

Lines 248-252:

```
RUN pip install --no-cache-dir \
    "transformers>=4.46" \
    accelerate \
    fastapi \
    "uvicorn[standard]"
```

An open-ended lower bound and three entirely unpinned packages (plus their full transitive closure), resolved from PyPI at whatever moment the enclave build runs. Consequences: (a) **unreproducible** — two nodes deploying the same measured file on different days run different code, and no record of the resolved versions exists anywhere in the attestation chain; (b) **unbindable** — this review's statements about uvicorn access-log defaults and transformers behavior are statements about those projects generically, not about the deployed bytes; (c) **supply chain** — a malicious release of any of these packages (or a dependency) executes inside the process that reads every user's PII-densest text, tracelessly. `transformers` and `uvicorn` are the packages that actually touch request content here. Same class as the mutable base tag: attacker-chosen code under the plaintext process with no attestation-visible change.

### LOW (deployed: ON, metadata-only at reviewed source) — container stdout/stderr ships unredacted to two off-node telemetry backends (telemetry)

Deployed ON: the pipe itself runs today. `model-privacy-filter`'s stdout is tailed by otelcol-contrib and exported to `https://telemetry.infra.near.ai` (lines 1257, 1464, 2058, 2073-2076), and by the measured harness's datadog-agent to `us3.datadoghq.com`, with no redaction stage anywhere. At the reviewed inline source what ships is metadata: uvicorn access lines, numeric watchdog lines, framework warnings. LOW rather than clear, because the pipe is content-blind — any content-bearing print introduced by a swapped base, a rogue PyPI release, or a future framework version ships to third-party-visible sinks the moment it is emitted. The two ARMED findings above are what could put content into this ON pipe.

### LOW (deployed: ON, inert at pinned revision) — model and tokenizer fetched from huggingface.co at startup with trust_remote_code enabled (egress)

Lines 309-323: runtime network fetch from huggingface.co (`HF_HUB_OFFLINE` defaults to 0, line 419 — a default, not a pin), with `trust_remote_code=True` at both call sites. Inert as deployed: the revision is pinned to commit `7ffa9a04…` inside the hash-pinned source, and that revision was checked during this review to contain no executable code and no `auto_map`, so the flag currently loads nothing. It remains a loaded footgun — pointing the same code at any revision that *does* carry an `auto_map` would execute HF-repo Python in the plaintext process; here that would require changing the measured file (visible) — unlike FLUX in this same file, whose unpinned `--trust-remote-code` is the manifest page's HIGH. Startup egress carries HF hub telemetry metadata (library/version headers; `HF_HUB_DISABLE_TELEMETRY` unset), never user content: the fetch completes before traffic exists.

### INFO (deployed: ON) — unauthenticated classify endpoint and host IPC namespace: lateral plaintext exposure inside the enclave, no external sink

The server binds `0.0.0.0:8000` with no authentication (line 414); the compose network is the shared `dstack_default` (`external: true`, lines 1419-1422), so every container on the node — and anything else attached to that external bridge — can submit text and read PII verdicts, or replay traffic to it. The service also inherits `ipc: host` from the `*nvidia` anchor (line 12 via line 240), joining one shared IPC namespace with all nine model services. Both are structural, in-enclave-only exposures (every peer is inside the same measured CVM); they became relevant only as blast-radius multipliers for the ARMED findings above. The manifest page carries the node-wide `ipc: host` as MEDIUM.

## why this is tag-addressed, not digest-addressed

Every digest-pinned image in this fleet gets a `sha256-*.md` page — the page and the bytes are the same identity. The attested manifest pins this base **by tag only**; no digest exists anywhere in the attestation chain, and `resolve_identity.py` refuses the ref for exactly that reason. Naming this page `sha256-*.md` would claim a byte-identity the attestation doesn't provide — including naming it after today's Docker Hub resolution, which is a lookup result, not an attested fact. `tag-<tag>.md` is the honest key: it covers exactly what the attestation pins (the tag string, and the hash-verified configuration and inline source built on top of it) and nothing more. The running container (`image: privacy-filter-hf`) has no registry identity at all — it is built in-enclave from this recipe — so its provenance lives on this base, and this base's provenance is a mutable name.

## not traced

- **The bytes behind the tag.** The base image's OS layers, Python build, bundled CUDA userspace, and any preinstalled packages were not reviewed and cannot be bound to any running node. Every safety statement on this page is scoped above that line.
- **The resolved PyPI set.** Which `transformers`/`accelerate`/`fastapi`/`uvicorn` (and transitive) versions each node actually built with — unrecorded, unreproducible. Statements about uvicorn access-log content and transformers behavior are generic-upstream, not deployed-bytes.
- **Framework internals at the deployed versions**: transformers' warning/crash paths under malformed input, HF hub telemetry payload details, uvicorn error-path logging. At reviewed defaults none emits request bodies; unverified for the actual installed versions.
- **The model weights' behavior** (what the classifier flags or misses) — quality, not exfiltration; out of scope.
- **`vllm-proxy-rs` in front** (request/usage logging at the proxy hop) — covered by its own [source page](/images/docker.io/nearaidev/vllm-proxy-rs/sha256-b183677a5d32267539b9b21ec45327a4f3be0a013afeb608c68c4d76e9472e36.md), not re-traced here.
- **Whether the built image digest is recorded anywhere post-build** (e.g. by compose-manager) — if it were, it would partially mitigate the reproducibility gap; not found in this file, not traced further.

Deployment analysis: [the audited manifest version](/manifests/nearai/cvm-compose-files/prod/small-models/sha256-a385f19a51054767b8be49a64ebc3111e0e62f721a861e54c78984b186904599.md) and [/notes/ARCHITECTURE.md](/notes/ARCHITECTURE.md).

## source / upstream

upstream base: [pytorch/pytorch on Docker Hub](https://hub.docker.com/r/pytorch/pytorch) — official PyTorch runtime image; no build attestation, no digest in the attestation chain, so there is no way to bind any running node's base layers to any source at all — the link is a project pointer, not a verified-source proof. Application source: none to link — the entirety of `server.py` is embedded in the measured file itself ([lines 254-412](https://github.com/nearai/cvm-compose-files/blob/6a284da32cbd385192d3d9de96f48af2d5794cbc/prod/small-models.yaml#L254)), which is this page's reviewed artifact. Model: [`openai/privacy-filter` @ `7ffa9a04`](https://huggingface.co/openai/privacy-filter/tree/7ffa9a043d54d1be65afb281eddf0ffbe629385b) (public; weights and tokenizer only, no repo code at the pinned revision).
