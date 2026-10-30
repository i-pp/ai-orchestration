# AI Orchestration

This repository is the canonical source for AI development orchestration policies, architecture, agent roles, delegation, escalation, and governance. It defines how work is coordinated; it does not implement task execution.

## Responsibilities

| Repository | Owns |
| --- | --- |
| `ai-orchestration` | Policies, architecture, roles, delegation, escalation, and governance |
| `agent-orchestrator` | Runtime implementation, scheduling, execution, monitoring, and task lifecycle |

Runtime behavior and its technical configuration belong in `agent-orchestrator`. Any mechanism that loads or enforces these policies must be documented and verified there; this repository does not imply automatic synchronization.

## Structure

- [`AGENTS.md`](AGENTS.md) — Minimal entry point for coding agents.
- [`docs/ai/orchestration.md`](docs/ai/orchestration.md) — Core architecture and operating principles.
- [`docs/ai/policies.md`](docs/ai/policies.md) — Execution permissions, risk classes, and escalation.
- [`agents/README.md`](agents/README.md) — Agent responsibilities and delegation boundaries.
- [`skills/README.md`](skills/README.md) — Skill organization and reuse conventions.

## Integration

Agents and runtime projects should reference these documents instead of copying policy text. Keep runtime-specific instructions and implementation details in their owning repository. A reference alone does not prove that a runtime has loaded or enforces a policy; report that only after verifying the integration.
