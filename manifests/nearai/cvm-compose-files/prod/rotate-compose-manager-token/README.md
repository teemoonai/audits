# prod/rotate-compose-manager-token.yaml

A control-plane runbook, not a serving recipe: one `docker:27-cli` one-shot (`profiles:
[cm-token-rotate]`, `restart: "no"`, no network) that rotates the compose-manager's `BEARER_TOKEN` by
`docker exec` into the launcher, rewriting the launcher's env file and re-creating compose-manager under
the `dstack` project, with a health check and a rollback. It was upped once on each of four CVMs on
2026-09-29 (gpu03, the DeepSeek CVM, gpu04, gpu23), each followed within a minute by a
`compose_manager_started` entry — the attested trace of a rotation. The exited container persists or was
removed as an orphan by the next up of another file; the log records no compose project, so it cannot say
which, and under neither reading is a process running.

Identity is **log-pinned**: the file's `file_sha256` against the signed compose-manager action log
(commit + path + file hash), not hardware-measured; the measured layer is each node's harness under
[`../../../../measured/`](../../../../measured/). The image is reviewed at
[`images/docker.io/library/docker/`](../../../../../images/docker.io/library/docker/).

The verdict column is the page's own `## verdict:` line, truncated.

## audited revisions

| file_sha256 | verdict | review |
|---|---|---|
| [`0d1263e5169e…`](sha256-0d1263e5169ebacdb1da157857aafff9a5bb5645aabbd921b3bd7e18d60a8ee2.md) | QUALIFIED PASS — nothing this file runs can see message plaintext: one container, no network, no model volume, no engine, no proxy, and its only reach — a read-write docker socket, which is root-equivalent on t… | 2026-11-06 |

A revision not listed here has not been audited — the teemoon app shows no audit link for it (fail-closed by design).
