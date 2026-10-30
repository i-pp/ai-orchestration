# Orchestration Architecture

## Scope

AI orchestration defines how work is assigned, coordinated, reviewed, and governed. It is separate from runtime implementation: scheduling, process execution, monitoring, and task lifecycle belong in `agent-orchestrator`.

The agent roles and delegation boundaries are defined in [`../../agents/README.md`](../../agents/README.md). Execution permissions and escalation are defined in [`policies.md`](policies.md).

## Operating principles

### Progress First, Risk Aware

1. Prioritize implementation progress while maintaining correctness.
2. Make explicit decisions instead of repeatedly comparing alternatives.
3. Implement and verify reversible, low-risk changes without unnecessary approval.
4. Distinguish blockers from non-blocking improvements.
5. Track non-blocking issues without interrupting execution.
6. Reopen decisions only when new evidence justifies reconsideration.
7. Escalate security, privacy, destructive operations, and irreversible decisions.
8. Report decisions, actions, verification results, residual risks, and follow-up tasks.

## Work flow

Set the outcome and scope, assign a responsible role, and delegate bounded work where useful. Treat generated output as unverified until it has been checked against task requirements; integrate it only after that validation. Record unresolved issues with their impact and the condition for reconsideration; stop only when a blocker or policy requires it.
