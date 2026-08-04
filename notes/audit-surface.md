# The audit surface — what to open, and what to ask of it

> Companion to [`method.md`](/notes/method.md). Editorial, outside the path contract.

`method.md` says *what* to look for. It does not say *where*, and every review so
far has had to rediscover that on its own. That cost is measurable: the most
expensive review in the corpus (220k tokens) read large files whole because it
had no map; the cheapest (83k) grepped for symbols it already knew to want.

It also cost a defect. The [reviewer comparison](/notes/reviewer-comparison-2026-08-03.md)
found one reviewer missing a live token-ID leak that the other traced end to end
— and the miss sat in an area the first reviewer had explicitly marked
*"not traced"*. The honest-gaps discipline worked; the gap was still a gap.

So this list is not a summary of findings. It is **the set of places findings
have actually come from**, so the question stops being "did the reviewer think to
look here" and becomes "did the reviewer finish the list." Every item cites the
page it came from. An item you check and clear is worth writing down as cleared.

**Using it.** Walk it per review. Anything you cannot reach, put in *Not traced*
by name — that section is load-bearing, and readers of this repo should treat it
as the most important part of any page.

---

## 1. Logging switches: flags, defaults, and the level that actually emits

The question is never "can it log" — it always can. It is: at the deployed
command, is the switch on, and what would flipping it emit?

- [ ] Every request/response logging flag, its **default**, and whether the
      deployed command passes it.
- [ ] **Which log level emits content**, separately for input and output. These
      differ and the difference matters: vLLM gates prompts behind DEBUG but
      emits generations at **INFO with no level guard**, contradicting its own
      flag docstring — so responses need only the flag, not a level change.
      ([`ccd6a6db`](/images/docker.io/vllm/vllm-openai/sha256-ccd6a6dbf4aba4e94c6f7052d1835d6e742082b6a5095276552e9b7a5a47c2e5.md))
- [ ] **Truncation when unset.** `--max-log-len` defaults to unlimited, so a
      counterfactual "if this were on" is *untruncated*, not sampled.
- [ ] **Deprecated aliases** — read them properly. vLLM still registers
      `--disable-log-requests`; its dest is never read anywhere in the tree, so
      it is a no-op rather than a polarity trap. A whole-tree grep settles it;
      reasoning about the default does not.
      ([`6766ce0c`](/images/docker.io/vllm/vllm-openai/sha256-6766ce0c459e24b76f3e9ba14ffc0442131ef4248c904efdcbf0d89e38be01fe.md))
- [ ] **Switches with no CLI flag at all.** sglang's `dump_requests_folder` can
      only be set at runtime — the absence of a flag is not the absence of the
      feature. ([`5027e95b`](/images/docker.io/lmsysorg/sglang/sha256-5027e95bf6ec536856b1b52a91d1f35ff5c564ab83e8a94758a169ff09bb8df3.md))
- [ ] Any content-logging call site **outside** the main gate. vLLM has a
      `logger.debug("Input prompt: %s", …)` in a multimodal error branch that
      never consults `request_logger`: one env var reaches it, no flag needed.

*Typical files:* `arg_utils.py`, `cli_args.py`, `server_args.py`,
`entrypoints/logger.py`, `utils/request_logger.py`, the serving base's
`_log_inputs`.

## 2. Runtime reconfiguration — the highest-severity class found so far

Anything that changes behaviour **without a restart** is invisible to the
hardware measurement. That is the whole reason it outranks everything else here.

- [ ] Enumerate the **complete route table**, with the auth level attached to each.
- [ ] For any route that can enable logging/dumping/tracing: what exactly can it
      set, and what authenticates it?
- [ ] **Whether the auth middleware is installed at all.** sglang's
      `/configure_logging` carries `ADMIN_OPTIONAL`, which *permits* when no key
      is configured — and the middleware is never even added, because its install
      condition requires some route to be `ADMIN_FORCE` and none is. Reading the
      decorator alone would have called this protected.
- [ ] Whether the project gates a *comparable* endpoint properly elsewhere. sglang
      does exactly this for HiCache storage, which is what makes the logging
      omission an omission rather than a design position.
- [ ] Confirm the negative explicitly when it holds — vLLM has no
      `/configure_logging` analog, and saying so is a finding.

## 3. Crash, hang, and watchdog paths — where both misses happened

Unconditional, undisableable, and reached only under failure, so they survive
review by not being on the happy path. **Both defects the comparison surfaced
lived here.**

- [ ] The crash dump's **serializer dispatch**. vLLM prefers `anon_repr` when a
      class has one and falls through to a `__dict__` walk when it does not —
      `NewRequestData` is redacted, `CachedRequestData` is not, and the latter
      carries `all_token_ids` (prompt **plus** output). Enumerate every class
      reachable from the dumped object and check which have the redacting method.
- [ ] **`__repr__` / `anon_repr` bodies** that interpolate content. sglang's
      `Req.__repr__` prints `origin_input_ids` and `output_ids`, and the watchdog
      dumps `cur_batch.reqs` at ERROR with no flag to disable it.
- [ ] **Watchdog and hang handlers**, not just exception handlers. Ask what the
      trigger costs in practice — the deployment file's own header may document
      the hardware hanging routinely.
- [ ] Crash-dump-to-disk flags, py-spy invocation (**does it pass `--locals`?**),
      and GPU core dumps — the last would contain KV cache and activations.
      Check the env gates *and* their defaults; sglang's are `True` in code and
      blocked only by an absent variable.
- [ ] Sampling params in dumps: `stop`, `bad_words`, guided-decoding schemas are
      client-supplied and content-adjacent even when prompts are redacted.

## 4. Disk

- [ ] Every mounted volume, and which persist across container recreation.
- [ ] Cache roots: what actually lands there — config-hash-keyed compile
      artifacts are fine, request-derived data is not.
- [ ] Prefix/KV cache **location** (GPU vs a disk tier) and whether an offload
      flag is set.
- [ ] Responses store, media cache, profiler output directories.
- [ ] **Coupling bugs between features.** sglang's `--export-metrics-to-file`
      derives its field skip-list from the request logger's metadata, which is
      only computed when `log_requests` is true — so metrics-on/logging-off, the
      natural combination, skips nothing and writes `text` to disk.

## 5. Network egress from the plaintext-handling process

- [ ] Enumerate **every** outbound destination, then classify each by what it carries.
- [ ] Phone-home telemetry and its opt-out (vLLM's `stats.vllm.ai` is on by default).
- [ ] Tracing: whether it is configured, **and** whether any span attribute could
      carry content even if it were.
- [ ] Metrics label cardinality — can a caller inject a label value?
- [ ] **Request-driven fetch.** For any model that ingests media: read the
      *actual guard*, not the docstring. vLLM's domain allowlist is a truthiness
      test on a list that defaults to empty, so an unset flag means no check runs
      at all; redirect-following defaults to on.
- [ ] Where the process's **stdout** goes. A logging finding is a local-file
      finding or an egress finding depending entirely on this, and on this fleet
      there is no redaction stage anywhere in the pipeline.

## 6. Auth posture

- [ ] The flag **and** its env fallback — "no `--api-key`" is not sufficient if
      `VLLM_API_KEY` would also mount the middleware.
- [ ] Which paths are exempt by design (`/metrics`, `/health`) even when auth is on.
- [ ] Who can reach the port: check the network declaration, not just published
      ports. `external: true` is a *shared host* network.

## 7. Config reachability — the reasoning that carries most verdicts

Not a place to look; a habit. Most verdicts here turn on it rather than on dataflow.

- [ ] Trace flag-absent → object never constructed → call sites no-op, and cite
      each hop.
- [ ] **Does the program actually consume the flag?** sglang routes diffusion
      models through `multimodal_gen` rather than `srt`, where `parse_known_args`
      **silently discards** the operator's `--log-requests-level 0`. The safe flag
      was set and ignored. ([`8ece90ad`](/images/docker.io/lmsysorg/sglang/sha256-8ece90ad52faa8b56149f0117227d9009db34513213e35990da468aeb6fe0b75.md))
- [ ] `${VAR:-default}` is a **default, not a pin**.
- [ ] Always distinguish "OFF at deployed flags" from "cannot happen", and say
      what would activate it.

## 8. Manifest pages

- [ ] **`allowed_envs`, verbatim** — what an operator can set without changing the
      measurement. The single highest-value item on a measured page.
- [ ] Privileges and mounts: `pid: host`, `SYS_PTRACE`, `SYS_ADMIN`,
      `privileged: true`, docker socket, container-log mounts.
- [ ] Telemetry pipeline end to end, and whether **any** redaction stage exists.
- [ ] Network topology, published ports, nginx routing (a bare `location /` or an
      allowlist).
- [ ] **Sibling comparison — the highest-yield technique in this repo.** Compare
      services against each other in the same file, and the same service across
      nodes. It produced: the Qwen3-VL media gap (Gemma-4 sets both controls in
      the same file), the unpinned `--trust-remote-code` on Qwen3.6 and FLUX
      (pinned elsewhere), and the node lottery where one node ships engine stdout
      to a third-party SaaS and another does not.
- [ ] `--revision` pins, and whether `--trust-remote-code` is on without one.
- [ ] In-enclave `build:` services: the `FROM` base, and anything resolved from a
      mutable source at build time (`pip install vllm[audio]` can replace a pinned
      engine inside the enclave).

## 9. Identity, before any of the above

A review keyed to the wrong tree is worse than no review. Techniques that have
worked, strongest first:

- [ ] **Signed build attestation** — `GET /repos/<org>/<repo>/attestations/sha256:<digest>`.
      Read **every** attestation returned, not `[0]`: one image here has four.
- [ ] **OCI labels** — `ai.*.build.commit`, `org.opencontainers.image.revision`.
      Two pages were wrong because a compose comment was trusted and the labels
      were never read.
- [ ] **Tag reverse-lookup** — enumerate every tag and match the digest.
- [ ] **Dockerfile-ARG fingerprint** from the image config `history`, diffed
      against upstream tags, to bracket a commit *range*.
- [ ] **Artifacts left in the layers** — an unpinned `git clone` leaves `.git/`;
      `.git/shallow` recovered a commit that was otherwise unrecoverable, and a
      full tree diff confirmed it.
- [ ] A bracket is **not** a pin: it does not earn a `sources` entry, which the
      app renders as a verified binding.
- [ ] If identity cannot be established, publish INCONCLUSIVE and make no privacy
      claim. That is a correct outcome, not a failure.

---

## What this list cannot do

It closes the gap where a reviewer did not think to look. It does nothing about a
**shared** blind spot — somewhere neither reviewer looks because the list does not
mention it. Every item here exists because a finding came from it, which means the
list is shaped by what has already been found.

The mitigation is mechanical checks, not a longer list. Several items above are
short, deterministic queries — *enumerate dataclasses reachable from the dumped
object; flag any lacking `anon_repr` that carry a `*token_ids*` field* is an AST
walk, no dataflow analysis required, and it would have caught the missed leak in
seconds and flagged its upstream fix automatically. Items 1, 2, 3 and 6 are the
best candidates. See §3 of the [reviewer comparison](/notes/reviewer-comparison-2026-08-03.md).
