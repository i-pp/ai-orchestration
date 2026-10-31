---
name: technical-writing
description: Create an evidence-based Face B reference and prepare its frozen handoff for ChatGPT Face A editing; preserve reader value, author voice and independent technical/editorial review.
---

# Technical writing

Read the authoritative [Editorial Policy v2.0](../../docs/ai/editorial-policy.md), [workflow supplement](../../policies/editorial.md), [execution policies](../../docs/ai/policies.md) and [roles](../../agents/README.md). Run `python3 scripts/load_policy.py --show` from this Skill directory and read the returned context. Record hashes and actual version, not a claimed latest policy.

1. Identify the reader's problem, practical payoff and authorized evidence. Separate observed/reported facts, hypotheses and recommendations. Preserve topic IDs and source hashes privately; do not lead the article with them.
2. Codex creates Face B: a readable technical reference with explicit assumptions, useful commands, expected results, source traceability and realistic prerequisites. A launcher alone is not a complete Quick Start. Avoid audit-log narration and repeated caveats.
3. Use [article-editor](../article-editor/SKILL.md) for separate technical and editorial review. Passing lint/CI is not editorial acceptance. Ordinary revision ends within two cycles; escalate substantive disagreements.
4. Freeze the accepted B file hash, policy hash/version, evidence references and acceptance record before A is created. Use [face transitions](../article-editor/references/faces.md). A changed B invalidates the handoff; retain the accepted original rather than overwriting it.
5. ChatGPT edits Face A from that frozen B for natural human reading. Preserve technical meaning, compare B/A and record substantive changes and factual disagreements. Never impersonate a ChatGPT run or fabricate the author's memories, feelings or work. Face A is the human-facing article; its structure is not a fixed template.
6. Check the six acceptance questions in v2 independently of technical accuracy. Keep exact reviews and diff in supporting records. Place accurate AI disclosure after a reader-first opening or in a visible endnote; retain the actual platform topic/tag where applicable. Use the medium Skill for frontmatter, preview and Git conventions. Merge/publication/visibility each need explicit authorization; do not post automatically.

Face C is outside this Skill's authoring/review pipeline. Do not contact Rinka's ChatGPT, inject these instructions or manufacture its persona. Only a separately authorized handoff of Face A is in scope; clearly distinguish any returned creative response from technical reference.

For Japanese use pinned local textlint; English uses Vale. Optional local LanguageTool/noslop keep their existing authorized scope: no external draft API, silent fix, additional dictionary or global hook. Reuse existing roles; when independent review is unavailable, label self-review honestly and leave acceptance pending. The [before/after calibration](../article-editor/references/engineering-example.md) illustrates style, not verified facts or a publication-approved template.
