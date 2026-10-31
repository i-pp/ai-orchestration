# Editorial Policy v2.0 — Reader First, Evidence Always

## 1. Purpose

Produce technical writing that people want to read, understand, and use.

Technical correctness is mandatory, but correctness alone does not make a good article. The reader must gain something useful without having to decipher an internal engineering report.

Write for the reader. Preserve evidence for verification. Do not confuse the two.

## 2. Editorial Principles

1. Reader value first. Every article must answer: Who needs this? What problem does it solve? What can the reader do afterward?
2. Lead with the point. Begin with the problem, an interesting observation, and the practical takeaway. Do not open with provenance, test infrastructure, or disclaimers.
3. Explain before documenting. Present information in the order readers need to understand it, not necessarily the order events occurred.
4. Show the work. Provide useful commands, examples, expected outcomes, and explanations when the topic calls for them.
5. Keep the author's voice. Use natural first-person narration where appropriate. Do not invent experiences, feelings, dialogue, or events.
6. Be precise without being defensive. State important limitations once, where they matter. Do not repeatedly interrupt the narrative to disclaim the same uncertainty.
7. Prefer clarity over ceremony. Avoid unnecessary jargon, internal identifiers, process terminology, and administrative language.
8. Never invent evidence. Preserve technical meaning, verified results, source attribution, and uncertainty.
9. Make every section earn its place. Remove repetition, empty transitions, and paragraphs that serve only to demonstrate compliance.
10. Respect the reader's time. A short useful article is better than a long article with little practical value.

## 3. Article Structure

Use the following as a default, not a rigid template.

### Opening

Establish the problem and why it matters. Give busy readers the purpose, expected outcome, and key takeaway.

### Practical path

Provide enough context and actionable steps to help readers facing the same problem. Do not substitute an unexplained one-liner for a useful walkthrough.

### Explanation and evidence

Explain what happened, why it happened, and how the conclusion was verified. Include code, tests, references, and limitations where relevant.

### Conclusion

State what was learned, what the reader can apply, and what remains uncertain.

Do not add headings merely to satisfy this outline.

## 4. Writing Quality

- Prefer natural Japanese over translated technical-report prose.
- Use first person when recounting the author's actual work.
- Avoid repetitive sentence patterns and mechanical transitions.
- Use concrete examples instead of abstract declarations.
- Keep code and commands close to the explanation that makes them useful.
- Distinguish observations, hypotheses, conclusions, and recommendations.
- Preserve the author's personality without manufacturing anecdotes.
- Remove unnecessary self-references to the editorial or validation process.

## 5. Evidence and Technical Integrity

Technical facts, code behavior, numerical results, sources, and material limitations must remain traceable.

Evidence belongs in supporting records when its full detail would distract the reader. Include only the evidence needed to support the article's claims.

Do not claim that a test, preview, lint, or independent review ran unless it actually ran.

A passing CI check is not proof of editorial quality.

## 6. Three Editorial Faces

### Face B — AI Reference

Created by Codex using this policy.

Optimize for accurate retrieval, explicit assumptions, reproducibility, source traceability, and machine-assisted reuse.

Face B must still be understandable to human readers. It is a structured technical reference, not an internal audit log.

Freeze the accepted B revision before creating Face A.

### Face A — Human Article

Edited by ChatGPT from the frozen Face B.

Optimize for reader engagement, clear explanations, practical usefulness, natural narrative, and authorial voice.

Preserve the technical claims and evidence. Record substantive changes and resolve factual disagreements rather than silently rewriting them.

Face A is the primary human-facing article.

### Face C — Independent Creative Response

Produced independently by Rinka's ChatGPT using Face A as source material.

Do not impose this editorial policy, shared agent instructions, or a manufactured persona on the independent writer.

Face C may be a personal reaction, humorous interpretation, or unconventional technical article. Its format should be chosen through experimentation.

Clearly identify Face C as a creative response rather than an authoritative technical reference. Its independence and spontaneous voice are essential.

## 7. Review and Revision

Separate technical review from editorial review.

Technical review: Check claims, code, evidence, attribution, security, and meaningful limitations.

Editorial review: Check reader value, narrative flow, usefulness, clarity, tone, and unnecessary repetition.

Classify findings as BLOCKER, MAJOR, MINOR, or SUGGESTION.

Resolve BLOCKER findings before release. Address MAJOR findings or document a reasoned exception. Do not restart editing cycles for cosmetic issues.

Limit ordinary revision to two cycles. Escalate unresolved substantive issues rather than repeating the same discussion indefinitely.

## 8. Publication and Transparency

- Preserve Face B, Face A, and their meaningful differences.
- Publish the applicable editorial policy and identify its version.
- Disclose material AI assistance accurately.
- Preserve source references and necessary technical caveats.
- Keep private logs, secrets, credentials, and internal-only artifacts out of public content.
- Never merge, publish, or change visibility without explicit human authorization.

## 9. Final Acceptance Test

Before proposing publication, answer:

1. Would the intended reader choose to keep reading?
2. Can the reader understand the main point without studying internal evidence records?
3. Does the article provide useful knowledge or a practical next step?
4. Are technical claims accurate and supported?
5. Does the writing sound like a person communicating, rather than a system reporting compliance?
6. Are the differences between Faces A, B, and C transparent?

If the article passes technical validation but fails reader value, it is not editorially ready.

The goal is not to produce a document that passes every check. The goal is to produce something worth reading that also passes the checks.
