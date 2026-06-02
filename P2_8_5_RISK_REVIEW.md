# P2.8.5 Risk Review

Project: V7 Vozduh
Block: P2.8.5

| Risk | Severity | Evidence | Readiness impact |
| --- | --- | --- | --- |
| Convergence Risk | HIGH | runtime/local/GitHub Admin API files diverge | branch work allowed with waves; deploy blocked |
| Runtime Risk | HIGH | runtime source lineage UNKNOWN | preserve first; no overwrite |
| GitHub Risk | MEDIUM/HIGH | `main` behind; `Updatesystem` not runtime | use `Updatesystem` only as base, not deploy truth |
| Branch Risk | MEDIUM | dirty local worktree and many untracked reports | future branch block must handle worktree explicitly |
| Admin Risk | HIGH | Admin API controls operator surface | require route/API/UI verification |
| Truth Source Risk | HIGH | runtime state and source truth split | branch work allowed; runtime mutation blocked |

## Overall

Overall readiness risk: HIGH but bounded.

Risk status supports `READY_WITH_BLOCKERS`, not `READY`.
