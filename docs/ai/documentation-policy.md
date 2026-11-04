# Technical Documentation Policy

This policy governs public-facing product, architecture, setup, usage, and reference documentation in this repository and its pilot runtime repository. It does not redefine execution permissions; follow [`policies.md`](policies.md). For publication prose such as engineering articles and tutorials, follow [`editorial-policy.md`](editorial-policy.md) as well.

## Language and filenames

- English is the canonical language for public-facing primary documentation.
- The canonical filename has no language suffix: `README.md`, `installation.md`, or `architecture.md`.
- A Japanese translation uses `_jp` immediately before the extension: `README_jp.md`, `installation_jp.md`, or `architecture_jp.md`.
- Preserve code, commands, identifiers, configuration keys, paths, and technical terms accurately. Translate surrounding prose naturally, not word-for-word.
- Keep each translation semantically aligned with its English source. If the translation is incomplete or behind, label that status and link to the English source.
- Internal development notes, experimental records, and historical evidence are not automatically subject to translation.

## Feature status and evidence

Distinguish these states in both language versions:

- **Verified:** observed in the stated repository, environment, or test, with evidence readers can inspect.
- **Experimental:** implemented or evaluated only in a prototype, limited environment, or partial workflow. State the boundary and unresolved checks.
- **Planned:** proposed or intended, with no claim that it is implemented.

Do not turn a passing unit test, a design document, or an agent's report into a broader production claim. Keep environment, version, and test scope attached to the evidence when they affect the result.

## Information architecture

Plan documents by audience and purpose before drafting. Use Diátaxis categories to choose the shape:

- **Tutorials** teach a first successful outcome through a guided lesson.
- **How-to guides** help a reader complete a defined task.
- **Reference** records exact behavior, options, formats, and constraints.
- **Explanation** gives context, rationale, architecture, and trade-offs.

Choose one canonical location for each topic. Keep runtime implementation in `agent-orchestrator`; keep shared orchestration policies here. Link across repositories instead of maintaining duplicate policy text.

## README structure

Use this default outline:

1. Overview
2. Installation
3. Usage
4. Advanced Usage
5. Documentation

For policy-only repositories, use **Adoption** or **Integration** in place of Installation. Keep the README concise and task-oriented. Move detailed procedures, implementation history, experiment records, recovery steps, and internal specifications to dedicated documentation, preserving links and evidence.

## Accuracy and maintenance

- Check claims against the current implementation, tests, configuration, and primary evidence before editing.
- Verify commands, paths, supported features, limitations, and links against the target revision. Mark what could not be run or verified.
- Maintain an inventory and destination map before removing or relocating substantial README content. Do not silently discard historical evidence or present experimental behavior as generally available.
- Review English and Japanese versions for meaning, status labels, commands, and navigation.
- Use Markdown linting, link checking, and Vale when they are available and useful. Report skipped checks; passing lint is not proof of correctness or readability.

## Product website preparation

Markdown in `docs/` is the canonical source for the VitePress prototype. Keep site configuration and navigation separate from copied documentation. This phase does not publish or deploy a site; any later public deployment needs separate authorization.

## Reusable workflow

Use the [`technical-documentation` agent](../../.codex/agents/technical-documentation.toml) and the repository skills under [`.agents/skills/`](../../.agents/skills/). They follow this policy and do not expand the permissions of the parent task.
