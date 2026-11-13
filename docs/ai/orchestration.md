# Orchestration Architecture

## Scope

AI orchestration defines how work is assigned, coordinated, reviewed, and governed. It is separate from runtime implementation: scheduling, process execution, monitoring, and task lifecycle belong in `agent-orchestrator`.

The agent roles and delegation boundaries are defined in the [agent role guide](https://github.com/i-pp/ai-orchestration/blob/main/agents/README.md). Execution permissions and escalation are defined in [`policies.md`](policies.md).

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

## Parallel development plan

The coordinating parent owns the user's outcome, permissions, scheduling, integration, and final response. Add workers when independently scoped work or review can reduce the critical path, not simply to maximize agent count. Use a small task directly when delegation would cost more than it saves.

1. Inspect the repository instructions, original requirements, current branches, dirty state, and actual execution capabilities. Compare patches or trees before deciding that a divergent branch contains unmerged work.
2. Fix a completion contract: inputs and revisions, allowed paths/actions, acceptance criteria, worktree ownership, dependencies, model and reasoning effort, time and dispatch budgets, and evidence to return.
3. For cross-project, advanced, or multi-part work, optionally select an Orchestrator assignment to propose a dependency graph and role mix. It advises the coordinating parent; it does not create a second unbounded dispatcher.
4. Select the implementation level from the [role guide](https://github.com/i-pp/ai-orchestration/blob/main/agents/README.md). Parallel writers use separate clean worktrees and disjoint ownership. Use research and focused reviews in parallel when their inputs are ready.
5. Review the fixed candidate independently. Correctness and test adequacy are separate perspectives; add security, performance, or documentation review when the change crosses those boundaries. Editorial review remains a separate article workflow.
6. Collect the artifacts, inspect the actual diff and evidence, and integrate in a controlled worktree. Run an independent Verifier against the original requirements and the integrated revision.
7. Before an authorized merge, verify the exact remote head, required CI, and completion of configured asynchronous repository reviews for that same head. An empty review list while a review is pending is not completion. Resolve substantive findings or record an explicit reasoned disposition, then recheck after any head change. Preserve branch recovery references and do not delete dirty, uncertain, or unmerged work as routine cleanup.

A worker is a leaf by default. It returns a result or a proposed subdivision to its parent instead of recursively expanding the team. The parent can then select another role within the same recorded budget. A role or worktree is an operational boundary, not an OS sandbox or new approval authority.

## Explicit model selection

Record both the model identifier and reasoning effort before new model work. For this development profile, prefer `gpt-6.1-sol` with `max` reasoning. Only when that model is unavailable and the user's task permits fallback, select an available `gpt-6-luna` with `max` reasoning before starting the new work. Do not select `gpt-6-astra` or the older `gpt-6-sol` for this profile. A task's stricter explicit model requirement takes precedence.

Check the current executor's actual model/tool support. A configuration, cached model list, or requested setting is not proof of the model that executed. Pass explicit settings through a supported spawn interface or fail closed; do not silently drop them or substitute a model. Record observed model metadata separately when available.

Never retry an uncertain generation, spawn, or other side effect by selecting another model. Reconcile the original action and its artifacts first. A model fallback is a pre-dispatch decision, not an error-retry strategy. Do not weaken a local-only product boundary or enable a cloud provider merely because the development agents use cloud models.

## Bounded concurrency and continuity

Use the minimum of the task budget, executor slots, independent worktrees, and measured resource limits. Treat worker count, total dispatches, retries, deadlines, and resource cost as separate limits. An unknown or timed-out worker keeps its slot until its actual terminal state is confirmed; elapsed time or an accepted interrupt is not a release receipt.

Maintain a concise task inventory with owner, input revision, state, evidence, blocker, and next action. Continue ready independent work while one part waits. Stop or revise assignments when the user's direction changes, and collect partially completed effects before retrying or cleaning up. Runtime enforcement and concrete profiles belong in `agent-orchestrator`, not in this policy repository.
