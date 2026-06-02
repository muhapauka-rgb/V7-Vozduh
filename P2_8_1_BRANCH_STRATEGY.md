# P2.8.1 Branch Strategy

Project: V7 Vozduh
Block: P2.8.1

## Current Branch Reality

| Branch/ref | Role today | SHA |
| --- | --- | --- |
| `main` | GitHub default branch | `593619d494e215d11fd826086593527a4a555690` |
| `Updatesystem` | active local branch and upstream | `b848fbf82f76f916b2fc6e5d04b24a1068e6048f` |
| `codex/dynamic-load-autoswitch` | remote branch | `0ea6d4ef82abaad26b0609d254bb6cf297db6432` |
| `codex/dynamic-load-autoswitch-pr` | remote-only branch observed by `ls-remote` | `3b0fab9b639a10d55e232a8d6320a12d97f0c34e` |
| `codex/integratsiya-tunelya` | remote branch | `a0e689c67ef7d47e7f04e5c30e5430acd05752cb` |

## Strategy

1. Freeze runtime mutation until source certification is complete.
2. Keep `main` as protected production/default history until explicitly changed by repository governance.
3. Treat `Updatesystem` as the candidate convergence branch because it contains most runtime tool paths and matches several runtime hashes.
4. Do not merge or rebase during P2.8.1.
5. Triage local dirty `admin/v7-admin-api` before any branch action.
6. Triage remote-only `codex/dynamic-load-autoswitch-pr` before closing or merging related work.
7. Create a future release/convergence branch only after runtime deploy manifest fields are known.

branch_strategy_defined=true
