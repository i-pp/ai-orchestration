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

## Editorial assignments

Reuse Codex or a bounded Local LLM assignment as Writer (draft), Editor (independent editorial review of reader value, purpose, reasoning and supported author voice), or Technical Reviewer (evidence and correctness). These are media-independent responsibilities, not new execution agents or permissions. Assign Editor and Technical Reviewer independently of the Writer and record who checked what. Follow [editorial policy](../policies/editorial.md); keep provider operations in the target repository.

Use the authoritative [Engineering Editorial Policy](../docs/ai/editorial-policy.md) through the technical-writing context loader. The Writer identifies the reader's goal and a practical path; the Editor independently judges that path, narrative and reader payoff; the Technical Reviewer validates claims and the scope of commands/results. Both review perspectives must pass before publication readiness can be proposed. The user's examples calibrate editorial decisions, not technical truth or authority to merge/publish.

The Editor uses [article-editor](../skills/article-editor/SKILL.md) and returns a consolidated severity/location/impact/action list, checks targeted revisions and identifies the final article hash. Hand technical meaning changes to the separate Technical Reviewer. Reuse this assignment; do not add a duplicate Editorial Review execution agent. Ready means preparation for human review, never merge/publication authority.

For handoffs and short progress reports, use [communication quality](../policies/communication-quality.md); preserve audit information and do not apply short-message restrictions to long articles.

## Editorial v2 boundaries

Writer/Codex creates Face B; ChatGPT edits Face A only after B acceptance and freeze. Editor and Technical Reviewer assess different criteria for B/A; technical correctness never substitutes for reader value. Use [v2](../docs/ai/editorial-policy.md) and [face transitions](../skills/article-editor/references/faces.md). Rinka's Face C is independent and outside shared assignments: no contact, policy/Skill injection, manufactured persona or forced review format.
