# AI Orchestration

## Overview

The canonical source for AI development orchestration policies, architecture, agent roles, delegation, escalation, and governance. It defines how work is coordinated; it does not implement task execution.

| Repository | Owns |
| --- | --- |
| `ai-orchestration` | Policies, architecture, roles, delegation, escalation, and governance |
| `agent-orchestrator` | Runtime implementation, scheduling, execution, monitoring, and task lifecycle |

## Adoption

There is no package installation step. Runtime projects should reference the canonical policy source instead of copying policy text. They must document and verify how a runtime loads or enforces a policy; a link alone does not establish enforcement.

## Usage

Use the role boundaries and execution policies when assigning, delegating, reviewing, and escalating work. Runtime-specific commands and behavior belong in `agent-orchestrator`.

## Advanced Usage

- [Technical documentation policy](docs/ai/documentation-policy.md) and [Japanese translation](docs/ai/documentation-policy_jp.md)
- [Technical documentation agent](.codex/agents/technical-documentation.toml)
- Reusable [documentation skills](.agents/skills/documentation-architect/SKILL.md), [writer](.agents/skills/technical-writer/SKILL.md), [README maintainer](.agents/skills/readme-maintainer/SKILL.md), and [reviewer](.agents/skills/documentation-reviewer/SKILL.md)
- [Documentation inventory and README migration map](docs/ai/documentation-inventory.md)

## Documentation

- [Orchestration architecture](docs/ai/orchestration.md)
- [Execution policies](docs/ai/policies.md)
- [Agent roles](agents/README.md) and [skill conventions](skills/README.md)
- [Documentation site prototype](docs/index.md)
- [Japanese README](README_jp.md)
