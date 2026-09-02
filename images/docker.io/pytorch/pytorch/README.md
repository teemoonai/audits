# pytorch/pytorch

The official PyTorch runtime image, used on near.ai only as the **`FROM` of an
in-enclave build**: the `privacy-filter` service in `prod/small-models.yaml`
builds `privacy-filter-hf` from this tag with its application source inlined in
the recipe. The filter reads request text by role, so the page reviews the
inlined application source and the base's configuration rather than PyTorch
itself. **Tag-pinned, not digest-pinned** — the attestation binds the tag, and
the registry can serve different bytes under it tomorrow (the page says so).

## audited builds

| tag | verdict | review |
|---|---|---|
| [`2.5.1-cuda12.4-cudnn9-runtime`](tag-2.5.1-cuda12.4-cudnn9-runtime.md) | QUALIFIED PASS at configuration and inline-source level; base bytes can drift under the tag | 2026-08-07 |

A build not listed here has not been audited — the teemoon app shows no audit
link for it (fail-closed by design).
