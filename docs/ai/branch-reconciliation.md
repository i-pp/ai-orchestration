# Branch Reconciliation: 2026-11-13

The integration baseline is `211c98e5fcdeaef45da54d5683270f2b488ecdd3`. Divergence counts alone do not identify missing content: earlier work was integrated through squashed pull requests. This inventory compares each old branch's changed paths with the baseline's final Git blobs before considering another merge.

| Source branch and recovery commit | Evidence at the baseline | Resolution |
| --- | --- | --- |
| `ci/nonpublishing-docs-20261104` at `681f759fbc20258d82cdb7c212787b872b0c03e3` | Both changed files are byte-identical to main; its patch is equivalent to an integrated patch. | Already integrated; do not replay the CI change. |
| `docs/technical-documentation-2026-11-04` at `823e64c2f20826715237645e542b22da57dfcee0` | All 18 changed files are byte-identical to main, including skills, docs, lockfile, and VitePress configuration. | Already integrated despite divergent commit history; preserve this recovery reference. |
| `editorial/technical-writing-workflow` at `1b2175498854666218d556e98a916b111a8295bf` | The branch tip is an ancestor of main. | Already integrated; no content merge required. |

The new integration changes the canonical parallel-development plan and selectable development assignments, explicitly records model/effort selection, and keeps runtime implementation in `agent-orchestrator`. It does not overwrite older worktrees, rewrite branch history, publish runtime state, or deploy the prototype site. Historical Japanese translations and editorial examples remain intentionally available; English is the canonical working documentation.

Source reconciliation, remote branch deletion, and deployment are separate actions. These recovery references preserve the original public commits even when an obsolete branch is later removed after verification.
