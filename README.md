# AI Orchestration

## Overview

AI Orchestration helps teams coordinate work across repositories with shared rules for agent roles, delegation, escalation, and governance. Start with the [agent role guide](agents/README.md) and [execution policies](docs/ai/policies.md), then verify how your runtime loads or enforces them. This repository defines coordination policy, not task execution.

| Repository | Owns |
| --- | --- |
| `ai-orchestration` | Policies, architecture, roles, delegation, escalation, and governance |
| `agent-orchestrator` | Runtime implementation, scheduling, execution, monitoring, and task lifecycle |

## Adoption

There is no package installation step. Runtime projects should reference the canonical policy source instead of copying policy text. They must document and verify how a runtime loads or enforces a policy; a link alone does not establish enforcement.

## Usage

Start with the [agent role guide](agents/README.md) when assigning work, and the [execution policies](docs/ai/policies.md) before delegating or escalating. Runtime-specific commands and behavior belong in `agent-orchestrator`. For multi-part engineering work, use the [parallel development plan](docs/ai/orchestration.md#parallel-development-plan) and [selectable development assignments](agents/README.md#development-assignments). Every new assignment records its model and reasoning effort; the default development profile is GPT-6.1 Sol MAX.

## Advanced Usage

- [Technical documentation policy](docs/ai/documentation-policy.md) and [Japanese translation](docs/ai/documentation-policy_jp.md)
- [Technical documentation agent](.codex/agents/technical-documentation.toml)
- Reusable [documentation skills](.agents/skills/documentation-architect/SKILL.md), [writer](.agents/skills/technical-writer/SKILL.md), [README maintainer](.agents/skills/readme-maintainer/SKILL.md), and [reviewer](.agents/skills/documentation-reviewer/SKILL.md)
- [Documentation inventory and README migration map](docs/ai/documentation-inventory.md)

## Documentation

- [Orchestration architecture](docs/ai/orchestration.md)
- [Execution policies](docs/ai/policies.md)
- [Agent roles](agents/README.md) and [skill conventions](skills/README.md)
- [Branch reconciliation and recovery references](docs/ai/branch-reconciliation.md)
- [Documentation site prototype](docs/index.md)
- [Japanese README](README_jp.md)
