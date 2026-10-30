# Skills

Skills are reusable, task-specific procedures. They support policies and agent work; they do not replace or redefine canonical policy.

## Organization and reuse

- Keep each skill narrowly scoped and place it with the tool, domain, or workflow it serves.
- State when to use it, required inputs and permissions, the procedure, validation, and expected report.
- Link to canonical policies in [`../docs/ai/policies.md`](../docs/ai/policies.md) instead of copying their rules.
- Reuse a skill only when its stated scope and prerequisites match the task. Verify references and tool capabilities in the current environment.
- Do not include secrets, credentials, private endpoints, or machine-specific assumptions. Keep runtime implementation instructions in `agent-orchestrator`.
