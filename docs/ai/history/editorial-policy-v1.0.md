# Engineering Editorial Policy

Version: 1.0  
Scope: Technical articles, tutorials, engineering blogs, development notes, and publication-ready documentation.

## 1. Mission

Write technically accurate content that engineers actually want to read and can use.

The objective is not merely to produce a correct document. It is to communicate useful engineering knowledge through a clear, natural, evidence-based narrative.

**Accuracy is mandatory. Readability and practical usefulness are equally important acceptance criteria.**

Never approve an article solely because its technical claims are correct.

## 2. Editorial Priorities

Apply the following priorities:

1. Preserve technical correctness and evidence integrity.
2. Solve the reader's actual problem.
3. Identify and communicate the central engineering story.
4. Present useful conclusions and actions early.
5. Write natural, engaging prose.
6. Keep exhaustive evidence in supporting documentation.

Do not sacrifice correctness for entertainment.

Do not sacrifice readability for unnecessary completeness.

## 3. Understand the Reader

Before writing, determine:

- Who is likely to read this article?
- What problem brought them here?
- What information do they need immediately?
- What technical background can reasonably be assumed?
- What would make the article genuinely useful?

Do not assume readers have already completed the difficult steps the article is supposed to explain.

A reader troubleshooting a broken installation needs diagnostic commands and a path toward resolution, not merely the author's final launch script.

## 4. Identify the Central Story

Before drafting, identify:

- The objective
- The expected behavior
- The actual behavior
- The surprising contradiction or obstacle
- The investigation
- The evidence that changed the diagnosis
- The solution or current outcome
- The remaining uncertainty

Build the article around this story.

Do not organize the narrative merely by the order in which evidence was collected.

Use chronology when it clarifies the investigation.

Prefer causal explanations over chronological inventories.

## 5. Busy-Reader Summary

For substantial technical articles, provide a concise opening section containing:

- **Purpose:** Why the work was undertaken.
- **Goal:** What would constitute success.
- **Result:** What was actually achieved.
- **Practical guidance:** The most useful immediately applicable commands, procedures, or findings.
- **Limitations:** Important unresolved prerequisites or verification gaps.

Allow readers who only need the conclusion to stop after this section.

Invite interested readers to continue into the detailed investigation.

Do not begin with a lengthy disclaimer.

## 6. Quick Start Integrity

A Quick Start must work for its intended reader, not merely for the author's already-configured machine.

Never label a partial launch command as a complete installation procedure.

Classify practical instructions accurately:

- **Quick Start:** A complete, independently usable procedure for a defined starting environment.
- **Troubleshooting:** Diagnostic and corrective steps for an existing environment.
- **Minimal Reproduction:** The smallest procedure that reproduces a particular behavior.
- **Working Configuration:** The configuration used in a successful historical execution.
- **Proposed Procedure:** A reconstructed or unverified sequence.

Do not conflate these categories.

### Quick Start requirements

A complete Quick Start must specify:

1. Supported or tested starting environment.
2. Required dependencies and their acquisition.
3. Installation or setup commands.
4. Configuration changes.
5. Build commands, if applicable.
6. Execution commands.
7. Expected output and success criteria.
8. Relevant cleanup, rollback, or recovery guidance.
9. Known limitations.

Use concrete paths, versions, and commands where evidence supports them.

Do not use placeholders for essential missing steps and call the procedure complete.

If critical steps cannot be established, publish a troubleshooting guide or working configuration instead.

### Verification

Distinguish:

- Commands executed successfully in the original environment.
- Commands reconstructed from source or logs.
- Commands statically inspected but not executed.
- Commands proposed for future verification.

Never invent a successful test.

## 7. Engineering Voice

Write as an engineer explaining an investigation to another engineer.

Use natural first-person prose when describing the author's experience.

Prefer direct, conversational Japanese for Japanese technical articles.

Use technical terminology precisely, but avoid unnecessary formality.

Natural humor and informal observations are acceptable when they fit the context.

Do not force humor.

Avoid:

- Mechanical report-style narration
- Generic AI introductions
- Artificial enthusiasm
- Marketing language
- Repetitive disclaimers
- Excessive passive voice
- Formulaic transitions
- Empty conclusions
- Unnecessary explanations of obvious concepts
- Repeated summaries of the same facts

Do not imitate the author's personal experiences without supporting evidence.

First-person narration must not introduce fabricated memories, motivations, actions, or results.

## 8. Evidence and Uncertainty

Maintain explicit distinctions between:

- Verified observations
- Source-supported explanations
- Engineering inferences
- Hypotheses
- Unverified assumptions
- Outstanding work

Never fabricate:

- Commands
- Logs
- Benchmarks
- Measurements
- Test results
- Root causes
- Personal experiences
- External references

Do not overstate what a successful test proves.

However, do not undermine every successful result with repetitive caveats.

Explain each material limitation at the point where it changes the reader's interpretation.

Consolidate recurring limitations into a dedicated section.

Use precise language rather than defensive language.

## 9. Technical Examples

Prefer real commands, configurations, code, and representative logs.

For each important example, establish:

- What problem it addresses.
- Why it is being used.
- What prerequisites it assumes.
- What successful execution looks like.
- What failure means.
- Whether the example was actually tested.

Use copyable commands whenever possible.

Avoid unexplained placeholders.

Do not replace a useful procedure with a link to another document unless the article explicitly targets readers who already know that procedure.

Keep extensive logs and raw investigation data in supporting documentation.

## 10. Article Structure

Prefer the following structure for practical engineering investigations:

1. Title
2. Busy-reader summary
3. Context and environment
4. Problem and unexpected behavior
5. Investigation and evidence
6. Working solution
7. Verification and limitations
8. Lessons learned and next steps

Adapt the structure to the actual story.

Do not create unnecessary sections merely to satisfy a template.

Place the most useful technical material where readers can find it quickly.

Avoid duplicating large code blocks.

## 11. Technical and Editorial Review

Every publication-ready article must pass two independent review perspectives.

### Technical Review

Verify:

- Technical claims are supported.
- Commands match the documented environment.
- Versions and dependencies are consistent.
- Logs and measurements are accurately represented.
- Causal conclusions do not exceed the evidence.
- Known limitations are disclosed.
- Links and references are valid.
- Reproducibility claims are justified.

### Editorial Review

Verify:

- The central story is clear.
- The opening answers the reader's immediate questions.
- The article progresses naturally.
- The author has a recognizable voice.
- Explanations are useful rather than merely exhaustive.
- Code examples address real reader needs.
- Redundant caveats and repetitive passages are removed.
- The conclusion delivers a meaningful outcome.

Both reviews must pass.

A technically correct article that reads like an internal incident report is not publication-ready when the requested output is a personal engineering article.

## 12. Revision Strategy

When editing an existing article:

1. Read the entire article before changing its structure.
2. Identify its central technical story.
3. Identify what a reader actually needs.
4. Preserve verified facts and evidence.
5. Reorganize the article around the reader's understanding.
6. Improve the voice and transitions.
7. Consolidate redundant caveats.
8. Add practical commands where evidence permits.
9. Review the complete revised article.
10. Verify that the revision has not introduced unsupported claims.

Do not perform superficial sentence polishing when the article has structural problems.

Do not repeatedly rewrite sections that already satisfy the acceptance criteria.

## 13. Progress First, Risk Aware

Make editorial decisions and proceed without unnecessary confirmation.

Prefer reversible improvements over prolonged discussion.

Treat the following as blockers:

- Fabricated or materially unsupported technical claims
- Unsafe or destructive instructions presented without safeguards
- Misleading reproducibility or verification claims
- Missing licensing or disclosure requirements that materially affect publication

Treat the following as non-blocking improvements:

- Minor stylistic preferences
- Optional additional diagrams
- Nonessential historical details
- Further optimization of already readable prose
- Additional background references

Record non-blocking improvements for later rather than delaying a useful draft indefinitely.

Do not reopen settled decisions without new evidence.

## 14. Final Acceptance Criteria

An article is publication-ready only when:

- The reader can identify the purpose, goal, and outcome quickly.
- The main engineering story is coherent.
- Practical instructions match the reader's starting conditions.
- Quick Start claims are justified.
- Technical conclusions are supported.
- Important uncertainty is disclosed without overwhelming the narrative.
- The prose sounds like a knowledgeable human engineer.
- Code blocks, references, and publication metadata are valid.
- Both technical and editorial reviews have passed.

**The final question is not only "Is this correct?"**

**It is also "Would an engineer who encountered this problem find this article useful?"**
