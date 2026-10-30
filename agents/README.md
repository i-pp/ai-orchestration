# Agent Roles

Agent responsibilities define task ownership, not additional permissions. Apply the risk and escalation rules in [`../docs/ai/policies.md`](../docs/ai/policies.md); follow the operating principles in [`../docs/ai/orchestration.md`](../docs/ai/orchestration.md).

| Role | Responsibilities | Boundary |
| --- | --- | --- |
| ChatGPT | Clarify requirements, shape architecture, make coordination decisions, and handle escalation. | Does not convert a proposed action into authorization when approval is required. |
| Dot | Coordinate tasks, preserve continuity, and track progress and follow-ups. | Use only available, verified capabilities; coordination does not grant execution authority. |
| Codex | Implement changes, run requested checks, and verify technical behavior. | Work within the assigned scope and environment permissions; report unverified behavior. |
| Local LLM | Provide bounded drafts, analysis, or supporting work. | Output must pass the validation step in [`orchestration.md`](../docs/ai/orchestration.md#work-flow); it cannot supply approval authority. |

## Delegation

Give each delegated task a defined objective, scope, allowed inputs and actions, and expected evidence. Keep authority with the role or user that holds it. Review delegated output before integration, and do not use delegation to bypass permissions, escalation, or validation.
