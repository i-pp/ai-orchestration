# Documentation Inventory and README Migration

This inventory records the two-repository pilot before editing the READMEs. It is a migration record, not a replacement for the linked design and operational documents.

## Repository state inspected

| Repository | `main` revision inspected | README before edit | Existing Japanese README | Open PRs at inspection |
| --- | --- | --- | --- | --- |
| [`ai-orchestration`](https://github.com/i-pp/ai-orchestration) | `81ccf9a35f942ad329742a0182090ab151a6a2c5` | 25 lines, 1,530 characters; concise English overview, ownership table, structure and integration caveat | None | Draft PR [#1](https://github.com/i-pp/ai-orchestration/pull/1), an editorial workflow change |
| [`agent-orchestrator`](https://github.com/i-pp/agent-orchestrator) | `1468c0abb06e0b36ad92a7f041d5305aab688947` | 459 lines, 34,389 UTF-8 bytes; Japanese, combining quick-start, design, operations, experiments, test history and status | None | None |

The revised AI orchestration README is 33 lines / 1,787 UTF-8 bytes, with a 33-line / 2,116-byte Japanese translation. Because the original was already concise, this change improves structure and navigation rather than shortening it: it adopts the requested five-part outline (using Adoption instead of Installation), keeps repository ownership and the no-automatic-enforcement caveat, and adds direct links to the documentation workflow, policy, and site prototype.

No local checkout of either repository was attached to this task workspace. The inspection used the connected GitHub API. The existing `ai-orchestration` draft PR remains untouched; it overlaps with future instruction-file work and should be integrated separately.

## `ai-orchestration`

The original README was already concise and its repository ownership and integration caveat remain in the revised README. No detailed technical content needed to move. The new README adds the documentation policy, workflow entry points, a Japanese pair, and the VitePress source index.

The existing `agents/README.md`, `skills/README.md`, `AGENTS.md`, and `docs/ai/editorial-policy.md` were inventoried. The documentation agent and four skills are additive; publication prose remains governed by the existing editorial policy. Historical Japanese examples under `docs/ai/example/` remain untranslated.

## `agent-orchestrator`

The original README mixes introductory material with detailed usage and operational procedures. The revised README keeps the product scope, material host limits, safe starting commands, and navigation. Detailed material maps as follows:

| Original README content | Canonical destination or disposition |
| --- | --- |
| Product overview, runtime ownership, host and CLI versions, App Server maturity | Concise English/Japanese README; [`docs/systemd-deployment.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/systemd-deployment.md) and [`docs/poc-services.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/poc-services.md) for environment and setup boundaries |
| Runner commands, acceptance fixture, and task lifecycle | Existing [`docs/architecture.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/architecture.md), new [`docs/how-to/run-task.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/how-to/run-task.md), and examples; live/offline test commands move to [`docs/testing.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/testing.md) |
| Workspace isolation and two-session concurrency | [`docs/workspace-isolation.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/workspace-isolation.md) and [`docs/concurrency-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/concurrency-design.md) |
| Implementer, reviewer, acceptance and verification | [`docs/native-agent-team.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/native-agent-team.md) and [`docs/verification-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/verification-design.md) |
| Interrupt, restart, recovery, status, identifiers, saved data and migration | [`docs/recovery-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/recovery-design.md), [`docs/verification-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/verification-design.md), and [`docs/retention-policy.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/retention-policy.md) |
| Daemon, persistent FIFO, scheduler and resource controls | [`docs/daemon-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/daemon-design.md), [`docs/scheduler-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/scheduler-design.md), and [`docs/resource-limits.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/resource-limits.md) |
| Local Git audit and protected files | [`docs/git-tracking.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/git-tracking.md) and `scripts/git_audit.py` |
| Unit, simulated integration, and subscription-consuming live checks | New [`docs/testing.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/testing.md) and [`docs/phase-reports.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/phase-reports.md) index |
| MCP adapter, connection scope, Tunnel, mailbox and grant workflow | [`docs/chatgpt-connection-design.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/chatgpt-connection-design.md), [`docs/mailbox-operations.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/mailbox-operations.md), [`docs/mailbox-grants.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/mailbox-grants.md), and [`docs/poc-services.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/poc-services.md) |
| Blocked standard systemd deployment and separate development PoC | [`docs/systemd-deployment.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/systemd-deployment.md), [`docs/phase2-e3-report.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/phase2-e3-report.md), and [`docs/phase2-e3-2-report.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/phase2-e3-2-report.md) |
| Common policy pinning and local loading behavior | [`docs/common-policy.md`](https://github.com/i-pp/agent-orchestrator/blob/main/docs/common-policy.md) and the canonical [`ai-orchestration` repository](https://github.com/i-pp/ai-orchestration) |

The README's old links to `systemd/aceis-mcp-tunnel.service` and `systemd/aceis-mcp-tunnel.yaml`, and its `systemd-analyze` command using the non-example unit path, did not match the tracked example files. The new navigation points to the deployment and PoC documents, which distinguish templates from installed services.

The old overview described mailbox request/answer and retrieval as confirmed, while a later section marked ChatGPT access, write approval and parent-dot retrieval unverified. The revised README uses the narrower status documented in the unresolved-work section. It also keeps the AppArmor-blocked standard deployment distinct from the development PoC reported separately.

Detailed records and historical test evidence remain in their dedicated documents and phase reports. The old README text remains available through Git history; no runtime code, operational configuration, or historical phase report is removed by this documentation change.

## Remaining follow-up

- Resolve the unrelated editorial PR before integrating overlapping policy or instruction changes; this pilot does not modify its branch.
- Re-run VitePress install/build and Markdown lint after future documentation changes.
- Reconfirm test commands, links, and status claims from a local checkout at the PR head before approval.
- No CI workflow or PR status check was present at review time. No follow-up issue was created; adding non-deploying documentation checks and revisiting the alpha toolchain remain untracked follow-up work.
