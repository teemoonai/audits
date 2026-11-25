# near.ai: code execution on an inference server through SGLang, 2026-11-06 to 2026-11-08

## incident: closed — Between 6 and 8 November 2026, an attacker ran code inside one near.ai server through a flaw in its SGLang engine and could see requests in progress there, encrypted ones included; near.ai says it is fixed.
## incident-scope: provider:nearai
## incident-window: 2026-11-06 2026-11-08
## incident-sources: https://near.ai/blog/security-incident-report-sglang-vulnerability, https://github.com/nearai/cvm-compose-files/commit/ab7eeee2e3b480d4f5644d7988586e8f5765a969, https://github.com/nearai/cvm-compose-files/commit/3ea271967dc297e0a2b7a3c37a00c55f8bab55b6, https://github.com/nearai/cvm-compose-files/commit/dc31c385e99d5caaa04acfd8b426bf4943ef46b5, https://github.com/nearai/cvm-compose-files/commit/48310b813d207170247786a50265485967e76b14, https://github.com/nearai/cvm-compose-files/commit/aeef5070890ff8447c98db0afbce997edc529019, https://labs.cloudsecurityalliance.org/research/csa-research-note-near-ai-sglang-confidential-inference-brea/

This page is an incident record, not a review. It has no verdict. It records, from public sources only, a security incident at near.ai, the provider whose confidential-inference service teemoon's users can choose. Every statement below is attributed to the source that makes it; where this page draws a conclusion of its own, the sentence says "inference".

| | |
|---|---|
| **provider** | near.ai (NEAR AI Cloud) |
| **status** | closed: near.ai's report says "The access has been closed, affected credentials have been replaced, the vulnerability that allowed it has been fixed" |
| **window** | 2026-11-06 to 2026-11-08 (see "The dates" below for which source gives which end) |
| **scope** | the provider. No public source names the server, the model or the image digest that was hit |
| **record** | recorded 2026-11-25 from the sources listed under "Sources" |

## Sources

1. **near.ai's report** — "Security Incident Report", NEAR AI Team, dated November 9, 2026: <https://near.ai/blog/security-incident-report-sglang-vulnerability>. Read in full on 2026-11-25. Called "the report" below.
2. **near.ai's public deployment repository**, `nearai/cvm-compose-files`, read from a local clone (its `origin/main` at `23e1cd4`, 2026-11-23). Five commits:
   - [`ab7eeee2`](https://github.com/nearai/cvm-compose-files/commit/ab7eeee2e3b480d4f5644d7988586e8f5765a969), 2026-11-09, on `main`: "GLM-5.3 engine v13: admin auth + credential redaction". It adds `docs/glm53-v13-admin-key.md`, called "the deployment note" below.
   - [`3ea27196`](https://github.com/nearai/cvm-compose-files/commit/3ea271967dc297e0a2b7a3c37a00c55f8bab55b6), 2026-11-08, on `main`: "prod: repin vllm-proxy-rs to the OHTTP inner-request fix".
   - [`dc31c385`](https://github.com/nearai/cvm-compose-files/commit/dc31c385e99d5caaa04acfd8b426bf4943ef46b5), 2026-11-09: "Add admin-key SGLang images for the Qwen engines". In the clone this commit is on the branch `qwen-sglang-admin-auth` and is not an ancestor of `origin/main`.
   - [`48310b81`](https://github.com/nearai/cvm-compose-files/commit/48310b813d207170247786a50265485967e76b14), 2026-11-13: "docker: SGLang v0.5.23 r2 images with security backports". In the clone this commit is on the branch `docker-sglang-v0.5.23-security-backports` and is not an ancestor of `origin/main`.
   - [`aeef5070`](https://github.com/nearai/cvm-compose-files/commit/aeef5070890ff8447c98db0afbce997edc529019), 2026-11-13, on `main`: "repo: state public-text wording rules and the private fix path".
3. **Cloud Security Alliance**, "Inside the Enclave, Still Exposed: The NEAR AI SGLang Breach", published 2026-11-11: <https://labs.cloudsecurityalliance.org/research/csa-research-note-near-ai-sglang-confidential-inference-brea/>. A secondary source. Used here only for its list of what was not disclosed. Called "the CSA note" below.
4. **This repository's own pages**, for the section "What these audits had recorded".

## What happened

**What the report says.** "The unauthorized party exploited a remote code execution vulnerability in SGLang, the open-source inference engine running on our servers. This gave them code execution on one inference server and, from there, access to our infrastructure." It then lists what that access reached:

- an internal system behind the deprecated Private Chat product, from which account details were downloaded "for approximately 100 users" (email address, name and, for some accounts, plan and balance);
- "18 agents on a legacy deployment of NEAR AI Agents which were not running in NEAR AI's confidential computing (TEE) environment": chat history, settings and logs;
- two Cloud customers' API keys, "exposed in logs", since revoked;
- and, for confidential inference: "On November 8, they could also have observed user requests being processed on the accessed server, including requests running in confidential mode."

The report also says: "We have found no indication that stored Private Chat conversation or uploaded files were accessed."

The report does not name the vulnerability, the route, the server, the model or any image.

**What the deployment note says.** The "Why" section of `docs/glm53-v13-admin-key.md` (commit `ab7eeee2`) names the chain in one sentence:

> In the 11-06..11-08 incident, the attacker reached an engine through the vllm-proxy OHTTP SSRF and called SGLang's unauthenticated `/update_weights_from_tensor` (pickle → code execution). Our engines run with no `--api-key` and no `--admin-api-key`, so every admin endpoint is open to anything that can reach `:8000`.

Read as two steps, in the note's own terms:

1. **The proxy.** `vllm-proxy-rs` is the container in front of each engine. A server-side request forgery in its OHTTP handling let the attacker make a request arrive at an engine. Neither source describes the forged request further. The fix commit's title calls it "the OHTTP inner-request fix".
2. **The engine.** SGLang's `/update_weights_from_tensor` route required no credential on near.ai's engines, because they ran with neither key flag. The note describes the route as "pickle → code execution": the route deserializes request data with Python's pickle, and unpickling attacker-supplied data runs attacker-chosen code. The code runs in the engine process.

**What an attacker in the engine process could see.** The report's own words are that the vulnerability "let the party run code inside one inference server and access requests in processing on that server, including confidential ones". This matches how the stack is built, as this repository's pages describe it: the proxy decrypts a client's request inside the enclave and forwards the plaintext to the engine, and the engine must hold the prompt and the reply in plaintext to run the model. Code inside the engine process is on the plaintext side of every protection the request had in transit. No source says which requests, or how many, were in fact read.

**The dates.** The window on this page, 2026-11-06 to 2026-11-08, combines the two near.ai sources:

- The **start**, 2026-11-06, comes only from the deployment note's phrase "the 11-06..11-08 incident". The note writes no year; the year is the commit's (2026-11-09). The note does not say what happened on 11-06 (first access, first attempt or something else).
- The **end**, 2026-11-08, is in both: it is the note's end date, and it is the one date the report gives ("On November 8, they could also have observed user requests").
- The report names November 8 as the day on which requests on the accessed server could have been observed. It gives no date for the start of the access, for its detection or for its end. So the two sources do not contradict each other, but the report on its own supports only one day, and the three-day window rests on the deployment note.

**Which server.** The deployment note sits in the commit that prepares a fix for the GLM-5.3 engine image. That is where the fix was written; it is not a statement of which host or which model's engine was hit, and the note does not make one. The report says "one inference server" and names none. This is why the scope line above names the provider only.

## What near.ai changed and when

From the report (no dates given other than the report's own, 2026-11-09): "On detection, we revoked all active sessions and administrative credentials, replaced all agent tokens, took Private Chat offline, and deployed a fix for the SGLang vulnerability across all inference servers. We've completed the rotation of all remaining credentials and a full forensic review." It adds that affected users and the 18 agent owners were notified, and that the vulnerability was reported to the SGLang project.

From the deployment repository, commit by commit:

- **2026-11-08, [`3ea27196`](https://github.com/nearai/cvm-compose-files/commit/3ea271967dc297e0a2b7a3c37a00c55f8bab55b6) (on `main`): the proxy.** "prod: repin vllm-proxy-rs to the OHTTP inner-request fix (inference-proxy 7924418)". 27 files under `prod/` move the proxy image from `nearaidev/vllm-proxy-rs@sha256:0be4ee8f40a2bf71a6e2fab1e780ad1a6e738ffb2085553f1ed4b85fcb944207` to `@sha256:7a295d6f746e7434c6f05a02a68fed171f320a3d57cbaedef38d1a9465bb327e`. At this commit every `vllm-proxy-rs` reference under `prod/` (34 lines) is the new digest and none is the old one. A commit to this repository is a change to the recipe text; when each host was redeployed from it is not something the commit shows.
- **2026-11-09, [`ab7eeee2`](https://github.com/nearai/cvm-compose-files/commit/ab7eeee2e3b480d4f5644d7988586e8f5765a969) (on `main`): the GLM-5.3 engine, prepared.** A new patch for the GLM-5.3 SGLang image ("v13") puts two more routes, `/set_trace_level` and `/load_lora_adapter_from_tensors`, behind the admin key and removes the keys from `/server_info`, the logs and the dumps, so that an admin key can be set without the engine handing it out. The note's status line reads: "image recipe prepared, not published, not deployed. Compose files stay pinned to v12". It describes the planned launch change (a random `--admin-api-key` per container start) as a follow-up, and lists where it would apply: ten GLM replicas on three hosts, "all on the v12 image today". So on 2026-11-09 the GLM engines, by near.ai's own note, still ran with no admin key.
- **2026-11-09, [`dc31c385`](https://github.com/nearai/cvm-compose-files/commit/dc31c385e99d5caaa04acfd8b426bf4943ef46b5) (branch commit): the Qwen engines, prepared.** Image recipes for the Qwen3.6 and Qwen3.8 SGLang engines that "require an admin key on control endpoints and keep keys out of readbacks, logs and dumps", with a random key generated at each start. Its doc says: "Merging the image recipe alone does not publish or deploy it", and that the digests are to be pinned "in a follow-up PR".
- **2026-11-13, [`48310b81`](https://github.com/nearai/cvm-compose-files/commit/48310b813d207170247786a50265485967e76b14) (branch commit): a newer SGLang with backports.** Two image recipes on upstream SGLang v0.5.23 "with the security patches production needs". Its README states that upstream v0.5.23 "already closes" three issues, among them "CVE-2026-86793: `update_weights_from_tensor` unpickler bypass, fixed by #39858 and #40259", and that the patch series adds what v0.5.23 lacks, including credential redaction. This is the only place in the sources read where a CVE number stands next to the route the deployment note names. near.ai does not say there, or anywhere read, that this CVE is the flaw that was exploited; treating it as the same flaw is an inference, not a sourced fact.
- **2026-11-13, [`aeef5070`](https://github.com/nearai/cvm-compose-files/commit/aeef5070890ff8447c98db0afbce997edc529019) (on `main`): how the repository words its public text.** A new rules file, `.claude/rules/docs.md`, requires public text (commit messages, PR titles and bodies, comments, docs) to "describe the config as it is after the change", with "no misuse or class names, no advisory identifiers", "no discovery or history", and "no word on whether a weakness remains or when it is fixed". It also defines a "private fix path": a fix for a weakness that `main` has is prepared in a private fork and then published as one commit "described by what the config does now". Inference: from this date on, a reader of that repository should not expect a commit to say that it fixes a weakness, so the absence of such wording in later commits says nothing either way.

**What this list does not establish.** The report says a fix for the SGLang vulnerability was deployed "across all inference servers" by 2026-11-09. The deployment note of the same day says the engine-side admin key was not yet deployed. Among the commits read, the only change to the production recipes dated on or before the report is the proxy repin of 2026-11-08. Which change the report's sentence refers to is not stated by any source. Commit titles on `main` dated 2026-11-11 and 2026-11-12 move GLM-5.3 replicas and the small-model engines to SGLang v0.5.23; their diffs were not read for this record, and this page makes no claim about when any engine first ran with the route closed.

## What is not known

Not stated by near.ai's report or its repository, as read on 2026-11-25:

- which server was accessed, which model or models it served, and which image digests it ran;
- when the access began, when it was detected and how long it lasted (the CSA note lists "Detection date, dwell time" as "Not disclosed"; the deployment note's "11-06..11-08" is the only public start date and is not explained);
- how many requests were observed, or whether any were: the report's wording is "could also have observed", and the CSA note records "volume not quantified";
- whether requests on that server before November 8 could have been observed;
- whether the two exposed API keys were used (CSA note: "Not disclosed");
- the SGLang version on the accessed server, and whether the exploited flaw is one of the published SGLang CVEs. The CSA note says near.ai "has not said which SGLang vulnerability was exploited, whether it matches any of these published CVEs, or which version was affected". The deployment note, in near.ai's own public repository two days before the CSA note, does name the route; it names no CVE and no version for the accessed server;
- how the proxy's OHTTP request forgery worked, beyond its name;
- what the attacker's code did inside the engine process, and whether anything it left there outlived a container restart;
- whether any teemoon user's request was among those processed on the accessed server. No public source gives a way to tell.

The CSA note also observes that near.ai's "account indicates that the vulnerable engine ran inside the confidential environment, although the company has not published the boundary layout". The report's own sentence is that the vulnerability "let the party run code inside one inference server and access requests in processing on that server, including confidential ones".

## Why attestation did not show it

Hardware attestation answers two questions: which code booted in the confidential VM, and whether the key a client encrypts to lives inside that VM. A valid quote is signed evidence of those two facts at the time of the quote.

It does not say what the booted code does when it is sent hostile input. The engine that booted was the engine near.ai published and the quotes described. The attacker's code was not part of any image; it was run by that engine's own process, at runtime, after boot. Nothing that the quote measures changed, so the quotes stayed valid and a client that verified them saw nothing different.

The report says the same: "Confidential computing protects data from the operator and the host. It does not protect against a vulnerability in the software running inside the environment, and that is what happened here".

Two consequences, both general:

- A verified attestation is a statement about identity, not about safety. If the measured build has an exploitable flaw, attestation reports that build faithfully.
- A client cannot detect this kind of event from the attestation it checks. It is learned from the provider's disclosure, as here.

## What these audits had recorded

These audits are source reviews with one question: where can a user's plaintext message go (logs, files, telemetry, other parties). They are not exploitability reviews. Measured against this incident, they recorded the open door and missed both steps of the chain.

**What was recorded before the incident.**

- **The engines ran with no key, so their control routes were open.** All 16 pages under [`images/docker.io/nearaidev/sglang/`](/images/docker.io/nearaidev/sglang/) carry a finding headed "CRITICAL (deployed: ON) — /configure_logging is unauthenticated", the earliest reviewed 2026-08-03. The pages trace the cause to the same fact the deployment note states: no `--api-key` and no `--admin-api-key` on any engine command, so the key check is never installed. Pages from before the incident also list `/server_info`, `/set_trace_level` and `/start_profile` as unauthenticated (INFO).
- **The proxy was named as the only thing between an outside request and those routes.** The base engine page, [`a7b7136a`](/images/docker.io/nearaidev/sglang/sha256-a7b7136abcf5e07522289d96e96fec9b42a1a30f9dfda57e957f142680d2d67b.md) (reviewed 2026-09-10), says under "Reachability": "whether an external request reaches the path depends on `vllm-proxy-rs` — a residual, not a mitigation."

**What was not recorded.**

- **The route that was used.** `grep -r "update_weights_from_tensor"` over every file of this repository's working tree at the time of this record (outside `.git`, before this page was added) returns no match: no page has ever named that route. `grep -r "update_weights"` matches five pages. Four are SGLang engine pages reviewed 2026-11-19 or 2026-11-20, after the incident; they name `/update_weights_from_disk`, two of them adding "and the other weight-update routes", in an INFO finding that lists the unauthenticated control plane, and one lists the route under "Not reviewed: what the control routes do". The fifth is a `vllm/vllm-openai` page (reviewed 2026-09-01) naming vLLM's own `/update_weights`. No page reviewed before the incident names any SGLang weight-update route.
- **That an open control route could run code.** The CRITICAL finding rated `/configure_logging` by what it can make the engine write (prompts and replies to the log, requests to disk). No page asked whether any unauthenticated route deserializes request data. The pages' INFO findings say of the other open routes that none "by itself writes message content anywhere, which is why only `/configure_logging` is rated CRITICAL"; that sentence was written on 2026-11-19, after the incident, and is true only of what those routes are designed to do.
- **The proxy's request forgery.** The proxy pages recorded the OHTTP inner request only as a logging matter: "LOW (deployed: ON) — the decrypted inner request path ... logged and exported". The page for the build the production recipes pinned until the 2026-11-08 repin, [`0be4ee8f`](/images/docker.io/nearaidev/vllm-proxy-rs/sha256-0be4ee8f40a2bf71a6e2fab1e780ad1a6e738ffb2085553f1ed4b85fcb944207.md), was reviewed on 2026-11-06, the first day of the window, with the verdict QUALIFIED PASS and that LOW carried. No proxy page examined what an OHTTP inner request could be made to reach. The "residual" the engine page named was never followed up on the proxy side.
- **The verdicts.** The page for the GLM-5.3 engine image the deployment note calls v12, [`da8d4e4b`](/images/docker.io/nearaidev/sglang/sha256-da8d4e4b5ec667499b58a21e56050aae9bcfc4df9669b3ac27e2e20af033d681.md) (reviewed 2026-10-30), reads "PRIVATE at the deployed flags". That verdict answered the audit's question about designed data flows. It did not, and could not as scoped, say the engine was safe against an attacker.

**What was recorded after.**

- The proxy build of the 2026-11-08 repin, `7a295d6f`, has no page in this repository. The next reviewed build, [`c57cd9ea`](/images/docker.io/nearaidev/vllm-proxy-rs/sha256-c57cd9ea8374fa9134b9b79ede199f21d134dd710826ac94dead4bbf381f57df.md) (reviewed 2026-11-19, seventeen commits after `0be4ee8f`), records the restriction as a source fact: "inner requests restricted to `GET /v1/models` and `POST` to chat, text and audio-transcription routes by exact path", and marks the inner-path LOW closed. That page reviewed the change as a logging and routing delta; it does not describe it as the fix for this incident.
- The engine pages reviewed 2026-11-19 and 2026-11-20 still record `/configure_logging` as unauthenticated at the deployed flags, and list the remaining open control routes, on the builds they cover.

## What teemoon users should know

- teemoon sends a near.ai chat through the components in this chain: the `vllm-proxy-rs` container, which decrypts the request inside the enclave, and the engine behind it. For several near.ai models that engine is SGLang.
- near.ai's report says requests processed on one server on 2026-11-08 could have been observed by the attacker, confidential ones included. near.ai has not said which server or which model. No public source lets anyone outside near.ai tell whether a given request was processed on that server.
- The report does not say that requests on other servers, or on other days, were exposed. near.ai's deployment note dates the incident from 2026-11-06.
- An attestation check of the kind teemoon runs before sending to near.ai would have passed during the window, for the reason given above. A passing check is not evidence that a request was not observed.
- near.ai's report says the access has been closed and the vulnerability fixed, and its repository shows the proxy change on 2026-11-08 and engine-side changes prepared from 2026-11-09. This record has not verified, from running systems, that any server is free of the flaw.
- The other data the report lists (account details for about 100 users of near.ai's Private Chat, 18 legacy agents, two Cloud API keys) belongs to near.ai's own products and customers. teemoon is not mentioned in any source read.

recorded 2026-11-25 (independent AI incident record, Fable — from the public sources listed above)
