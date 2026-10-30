# Skills

Skills are reusable, task-specific procedures. They support policies and agent work; they do not replace or redefine canonical policy.

## Organization and reuse

- Keep each skill narrowly scoped and place it with the tool, domain, or workflow it serves.
- State when to use it, required inputs and permissions, the procedure, validation, and expected report.
- Link to canonical policies in [`../docs/ai/policies.md`](../docs/ai/policies.md) instead of copying their rules.
- Reuse a skill only when its stated scope and prerequisites match the task. Verify references and tool capabilities in the current environment.
- Do not include secrets, credentials, private endpoints, or machine-specific assumptions. Keep runtime implementation instructions in `agent-orchestrator`.

[technical-writing](technical-writing/SKILL.md) owns the shared evidence-to-publication-preparation workflow. Media repositories supply their own publishing skills and verify the pinned shared revision they read.

[article-editor](article-editor/SKILL.md) owns local mechanical lint, editorial/voice references, severity dispositions and bounded independent review within technical-writing.
