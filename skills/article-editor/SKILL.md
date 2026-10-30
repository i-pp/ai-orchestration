---
name: article-editor
description: Review and revise technical article drafts for reader value, coherent reasoning and the author's supported voice; pair mechanical lint with independent editorial and technical judgments before publication preparation.
---

# Article editor

Use within [technical-writing](../technical-writing/SKILL.md), after evidence and topic selection. Read [editorial policy](../../policies/editorial.md). Reuse the existing Editor assignment; do not create an additional agent definition or treat tool output as editorial acceptance.

Load the authoritative [Engineering Editorial Policy](../../docs/ai/editorial-policy.md), roles and sample calibration using `python3 ../technical-writing/scripts/load_policy.py --show` from this Skill directory. Read the [before/after assessment](references/engineering-example.md). Missing context remains a hold on acceptance. Samples guide reader value and voice; their factual claims and missing metadata are not automatically approved. Preserve the supplied originals and report proposed corrections separately.

Read [candidate review](references/candidates.md) before adding an external style tool; unresolved optional candidates do not block the primary workflow. Read [Editorial](references/editorial.md) for argument and reader payoff, [Voice and style](references/voice-style.md) when revising prose, and [Technical review](references/technical-review.md) for source verification and severity. Keep the intended language and the author's intent. First person requires an attributed action or judgment; never manufacture experience, feelings or results. Without representative prose, use supplied preferences and report the style-reference limit.

## Bounded review

Follow Draft → Mechanical Lint → Editorial → Technical → Targeted Revision → Final Verification → Ready. Run `python3 scripts/check.py ARTICLE --lang ja|en --output REPORT`; see [local tools](references/tools.md). For an authorized Japanese sanitized copy, add `--noslop --sanitized-sha256 EXACT_SHA256` when the approved local CLI is available. English records noslop as NOT_APPLICABLE. A matching hash binds the copy; it does not itself authorize data use or prove confidentiality. This command checks prose locally and never sends it to an API. No automatic fix is applied. Optional LanguageTool is a separate on-demand local CLI check, documented in the tools reference; never claim it ran merely because jars are installed. Record findings against the exact article hash.

Assign the existing Editor independently of the Writer, and a separate Technical Reviewer. For each finding record id, severity, source/line, impact, proposed action and disposition. BLOCKER means a substantial technical error, security/privacy issue or clear falsehood and must be fixed. MAJOR normally needs a change; a specific recorded rationale may justify proceeding. MINOR and SUGGESTION do not stop the work. A mechanical warning is a review candidate, not proof of a factual error.

Record an explicit conclusion from both perspectives. The Editor must explain what an unfamiliar reader can now do, why the result matters and whether the prose reads as an engineering article rather than an internal report. The Technical Reviewer checks evidence attribution, instruction prerequisites, actual success scope and later source updates. Technical accuracy, first person, chronological order or lint success cannot compensate for an editorial rejection. `READY_FOR_HUMAN_REVIEW` remains a handoff state, not a declaration of publication readiness.

Use `scripts/review.py` to bind both reviews and final verification to the exact file. At most two revision/review cycles: after cycle 2 return Ready with justified residuals or Blocked with the unresolved blocker; do not restart without new substantial evidence and a recorded decision. A new BLOCKER may reopen a bounded attempt with its evidence recorded; safety and correctness take priority over the old attempt’s cycle count. A changed article invalidates previous final verification.

Preserve raw/edited text and the diff. Compare numbers, code, quotations, links and limitations; require human review for a meaning-changing edit. Ready is editorial preparation only: exact human merge/publication authorization, disclosure and the target repository's confidentiality/delivery checks remain separate.
