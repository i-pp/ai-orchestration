# Editorial workflow supplement

The sole authoritative editorial standard is [Editorial Policy v2.0 — Reader First, Evidence Always](../docs/ai/editorial-policy.md). It supersedes v1 editorial instructions. [v1.0](../docs/ai/history/editorial-policy-v1.0.md) is an inactive historical snapshot. Apply execution policies and explicit authorization boundaries independently.

Read the standard using `python3 skills/technical-writing/scripts/load_policy.py --show`; record exact hashes/version. An immutable media pin to an older commit is not v2. Do not silently replace Git objects with working files.

Use [technical-writing](../skills/technical-writing/SKILL.md) for Face B and the B→A handoff; [article-editor](../skills/article-editor/SKILL.md) for independent technical/editorial judgments. Keep evidence, policy identity and substantive A/B differences in supporting records rather than administrative prose in the article. A partial launcher is Working Configuration or Troubleshooting, not a complete Quick Start. Facts, source attribution and necessary limitations remain intact.

## Draft lineage and policy selection

Initial is the first completed, delivered Codex manuscript directed by Dot: a non-release historical source, not an internal pre-edit scratch draft and not a later ChatGPT rewrite. Codex rewrites that verified source under the selected policy to create B, an intended publication target. ChatGPT rewrites frozen accepted B into A, also an intended publication target. Rinka's independent ChatGPT may rewrite A into C, an independently authored intended publication target. Intended publication is a purpose, never permission: keep drafts unpublished until the applicable explicit release authorization. C remains outside this shared workflow and must not be contacted or given these instructions.

For each new draft/revision, choose the latest explicitly accepted policy revision available through an authorized source; a newer branch head alone does not establish acceptance. Freeze its exact commit, canonical document version/hash, source manuscript identity and acceptance evidence with that draft. Feedback may revise the policy in a separate reviewed change; it never rebinds an old manuscript to a future latest policy. No automatic newest lookup, unreviewed fetch or second policy registry is introduced. The current loader validates the accepted v2.0 manifest; a future incompatible version requires a reviewed loader update rather than a fallback.

## Branch discipline

Follow [editorial branches and revision history](../docs/ai/editorial-branching.md): one active topic branch/folder, one substantive revision per commit and an explicit PR/base. Rebase work in progress onto the latest accepted media integration base after verified policy-pin updates; preserve frozen applied-policy bindings. Consolidation must preserve actual source lineage, not manufacture a Chat-on-B revision. Remote rewrites require an exact preservation/lease plan and authorization.

## Disclosure placement

Lead with the reader's problem, observation and practical takeaway. Put a concise, visible and accurate AI-assistance notice after that opening (or in a visible endnote), with the medium's valid ChatGPT topic/tag when applicable. This supersedes the former requirement to start the article with provenance or place disclosure before the first heading. Do not hide disclosure in HTML, comments or code blocks. Disclosure is transparency, not an editorial-quality test. Do not automatically rewrite existing article bodies.

## Independence and release boundary

Freeze accepted B bytes and policy/evidence identity before ChatGPT edits Face A. Preserve both and record substantive differences; unresolved factual disagreements remain findings. Face C belongs entirely to Rinka's independent ChatGPT: provide only the authorized Face A source if separately asked, never shared Skills, policy, review rubrics or a fabricated persona. Do not contact that writer as part of this workflow. Label a received C as creative response, not technical authority.

Reuse Writer, Editor and Technical Reviewer assignments for B/A only. Keep their reviews separate. Resolve BLOCKER findings; address MAJOR or record reason/impact/reconsideration; MINOR/SUGGESTION do not restart work. Limit ordinary revision to two cycles and escalate substantive unresolved issues. Tool success and handoff validation never establish reader value or publication readiness. Preserve explicit human merge/publication/visibility authorization; automatic posting remains suspended.
