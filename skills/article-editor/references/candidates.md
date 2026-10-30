# Candidate review (2026-10-30)

Prefer the smallest source-verified local stack; do not install every candidate. Writing checks support the author's voice, not AI-author detection or removal of the required disclosure.

| Candidate | Verified identity / license | Decision |
| --- | --- | --- |
| textlint-rule-preset-japanese | 10.0.4, MIT, official npm and textlint-ja source | Adopt a small warning-level subset. |
| textlint-rule-preset-ja-technical-writing | 12.0.2, MIT, official npm; overlaps general Japanese rules | Not installed; avoid duplicate grammar/style presets and forced polite voice. Reconsider on a demonstrated missing check. |
| @textlint-ja/textlint-rule-preset-ai-writing | 1.7.0, MIT; requires textlint >=15.1.0 | Adopt list-format/hype candidates at warning severity; other rules off initially. Observe false positives; never edit blindly. |
| noslop | owayo/noslop release v26.10.114, commit b2ef7a4eb7ad03391f9b06e1e5f274313d1c2864; core MIT, bundled notices include NAIST-2003 / Apache-2.0 / BSD-3-Clause | Optional trial, NOT_RUN. No global Skill/hook installation. Its revision comparison may complement fact preservation; it cannot establish correct attribution. Live comparison with textlint is not measured. |
| no-ai-slop | petergyang/no-ai-slop main 000650b156983f5159695b441477f4e63b25dc85, MIT; release v1.0.6 is a different revision | No independent Skill. Keep minimum edits, author vocabulary/uncertainty and reader purpose in existing voice review. Exclude blanket word/contrast bans and indefinite polish loops. |
| slop-shield | cmedfisch/slop-shield 2405d23c545092650ec49f5dc5b4571f3e9bbbae, manifest 0.1.0, MIT | Communication guidance only; long articles/runbooks excluded. Preserve source/hash/limits/FAIL/UNKNOWN/approval information. |
| LanguageTool | official fixed 6.6 ZIP, local optional CLI; Java 25.0.4.1 confirmed | Download returned HTTP 403; not installed or run. Java25 compatibility remains UNVERIFIED. Do not expose a server or use cloud API. |

## Sources and boundaries

- Official npm metadata and lock entries identify all textlint packages above. [Japanese preset](https://github.com/textlint-ja/textlint-rule-preset-japanese), [technical preset](https://github.com/textlint-ja/textlint-rule-preset-ja-technical-writing/releases/tag/v12.0.2), [AI-writing fixed source](https://github.com/textlint-ja/textlint-rule-preset-ai-writing/blob/45bb6485062b96a8578c5fa6ae37a41de01d9b80/README.md).
- [noslop installation](https://github.com/owayo/noslop/blob/b2ef7a4eb7ad03391f9b06e1e5f274313d1c2864/docs/installation.md), [third-party notices](https://github.com/owayo/noslop/blob/b2ef7a4eb7ad03391f9b06e1e5f274313d1c2864/THIRD_PARTY_NOTICES.md), [review data flow](https://github.com/owayo/noslop/blob/b2ef7a4eb7ad03391f9b06e1e5f274313d1c2864/docs/review.md). Source build requires Rust >=1.98. Default make-install also installs user Skills: do not use it for a CLI trial. Any future unknown release executable trial needs the exact asset/hash/command/scope reviewed first; no external reviewer option or draft API.
- [no-ai-slop source](https://github.com/petergyang/no-ai-slop/blob/000650b156983f5159695b441477f4e63b25dc85/skills/no-ai-slop/SKILL.md), [MIT](https://github.com/petergyang/no-ai-slop/blob/000650b156983f5159695b441477f4e63b25dc85/LICENSE).
- [slop-shield scope](https://github.com/cmedfisch/slop-shield/blob/2405d23c545092650ec49f5dc5b4571f3e9bbbae/skills/slop-shield/SKILL.md), [MIT](https://github.com/cmedfisch/slop-shield/blob/2405d23c545092650ec49f5dc5b4571f3e9bbbae/LICENSE).
- [LanguageTool directory](https://languagetool.org/download/) lists LanguageTool-6.6.zip, 251998221 bytes. [Language table](https://dev.languagetool.org/languages) includes Japanese but no Japanese spellcheck. Neither that table nor Java's version output demonstrates a successful local LanguageTool run.

Do not turn documentation-only overlap analysis into a measured output comparison. The aggregator retains provenance for exact duplicates; a future noslop adapter needs actual records before its overlap can be assessed.
