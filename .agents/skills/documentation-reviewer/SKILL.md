---
name: documentation-reviewer
description: Review technical documentation before delivery. Use to check accuracy, comprehension, structure, links, commands, migration completeness, or English/Japanese consistency.
---

# Documentation Reviewer

Read the [technical documentation policy](../../../docs/ai/documentation-policy.md) and repository-specific instructions. Review the source against the target implementation and evidence.

## Review checklist

- Technical statements match source code, tests, configuration, and the stated environment.
- Intended audience and purpose are clear; the information is in a suitable Diátaxis category and canonical location.
- Commands and paths exist; examples are safe and complete for their stated context.
- Internal and external links resolve, point to the intended detail, and do not expose draft or private material unexpectedly.
- Verified, experimental, and planned behavior are clearly distinguished.
- English and Japanese versions preserve the same meaning, limitations, commands, and status labels.
- README changes preserve access to important technical information and historical evidence; migration destinations are explicit.
- Prose is readable, concise, and free of unexplained jargon or repetition.

Run Markdown linting, link checking, and Vale when available and useful for the target repository. Record tools that are unavailable or checks that were not run. A passing linter is not proof of technical accuracy or reader comprehension.

## Report

Lead with concrete findings, each tied to a file and section. Then list checks run, checks skipped with reasons, unresolved evidence gaps, and any limits on the review. Do not report a path or command as verified unless you checked it.
