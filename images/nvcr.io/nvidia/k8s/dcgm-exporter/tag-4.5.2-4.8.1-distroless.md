# nvcr.io/nvidia/k8s/dcgm-exporter : 4.5.2-4.8.1-distroless

## verdict: telemetry-not-content at audited config — but GPU-privileged, and the tag can drift

| | |
|---|---|
| **image** | `nvcr.io/nvidia/k8s/dcgm-exporter` |
| **tag** | `4.5.2-4.8.1-distroless` — **no digest**; the attested manifest pins the tag string only |
| **seen in** | node inner compose (GLM-5.1 node; also present in the dsv4 multi-model node's inner compose) |
| **source** | NVIDIA — open-source exporter ([NVIDIA/dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter)) wrapping proprietary DCGM/NVML libraries |
| **build attestation** | public image (third-party); **tag-pinned by the attested manifest, not digest-pinned** — the registry can serve different bytes under this tag with no trace in the attestation chain |
| **review** | reviewed 2026-07-23 (independent AI source review — method: [/notes/method.md](/notes/method.md)); build identity captured from live attestation |

**coverage:** configuration-level only — the deployed service configuration was reviewed; the upstream source was not. and because the identity is a mutable tag, this page covers the *configuration around the tag*, never the bytes behind it.

---

## role

GPU-telemetry exporter. Reads aggregate GPU counters via DCGM/NVML — utilization, temperature, power, ECC errors, total/used memory **bytes** — and serves them as openmetrics on `:9400`, where the otel and datadog sidecars scrape them (metrics only; its compose labels carry autodiscovery/scrape annotations, no content routing).

## review (configuration-level)

The audited service block ([inner compose @ `c545c955`, line 365](https://github.com/nearai/cvm-compose-files/blob/c545c95545dba47d8bea293aaae317089ea52f4d/prod/GLM-5.1-SGL-AWQ-TP4.yaml#L365)):

```yaml
dcgm-glm51:
  image: nvcr.io/nvidia/k8s/dcgm-exporter:4.5.2-4.8.1-distroless   # tag only, no digest
  runtime: nvidia
  cap_add: [SYS_ADMIN]
  environment: [NVIDIA_VISIBLE_DEVICES=all]
  ports: ["9400:9400"]
  # full GPU device reservation; no volumes block at all
```

What it does **not** have: no `volumes:` of any kind — no `docker.sock`, no `/var/lib/docker/containers` log mount, no `pid: host`, no `SYS_PTRACE`. (The container-log mount in this compose belongs to the otel/datadog log shippers, not dcgm.) Its only declared surface is the `:9400` metrics endpoint, and what crosses it is aggregate counters — how *much* GPU memory is used, never what it *contains*. At the audited configuration this container observes telemetry, not message content.

Now the honest tension. This is the most privileged sidecar in the compose: `SYS_ADMIN` (a broad capability, not a narrow one), the nvidia runtime, and every GPU (`NVIDIA_VISIBLE_DEVICES=all` + full device reservation) — the GPUs on which plaintext is computed. And unlike every digest-pinned peer in the recipe, its bytes are not fixed: the manifest's `file_sha256` pins the *tag string*, so what actually runs can drift with a registry-side re-push, invisibly to the attestation chain. The control that keeps this container benign is its function — an exporter that reads counters, not GPU memory contents — and that control is **not cryptographically pinned**. A different image published under the same tag would inherit these privileges. Both manifest reviews carry this as a MEDIUM finding; this page exists to make it a first-class identity.

## why this is tag-addressed, not digest-addressed

Every other in-scope image is digest-pinned, so its page is named by the digest of the reviewed bytes — the page and the bytes are the same identity. The attested manifest pins dcgm-exporter **by tag only**; no digest exists anywhere in the attestation chain. Naming this page `sha256-*.md` would claim a byte-identity the attestation doesn't provide. `tag-<tag>.md` is the honest key: it covers exactly what the attestation pins (the tag string and the configuration around it) and nothing more.

Deployment analysis: [the audited manifest version](/manifests/nearai/cvm-compose-files/prod/GLM-5.1-SGL-AWQ-TP4/sha256-eb00b404e3218e2e8c8ab8da5845af10ce79929fd232fe8ac3d2f688582817be.md) and [/notes/ARCHITECTURE.md](/notes/ARCHITECTURE.md).

## source / upstream

upstream: [NVIDIA/dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter) — the exporter itself is open source, but it wraps NVIDIA's proprietary DCGM/NVML libraries, so the running container is not fully open source. The shipped build was **not** source-audited (this page is configuration-level only), and with no digest there is no way to bind the running bytes to any source at all — the link is a project pointer, not a verified-source proof.
