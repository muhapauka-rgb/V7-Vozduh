# P2.8 Convergence Plan

This is a plan only. No fix, sync, deploy, push, merge, or rebase was performed.

## What Must Be Synchronized

- Local dirty P2.1-P2.7 code and reports need an intentional Git decision.
- Endpoint inventory docs need regeneration or explicit stale marking.
- Runtime source hashes need collection from production.
- GitHub default branch strategy must be clarified: `main` vs `Updatesystem`.
- GitHub-only branch `codex/dynamic-load-autoswitch-pr` needs triage.

## Canonical

- Production runtime is canonical for live user/channel/routing state.
- Local repo is canonical for uncommitted implementation intent only.
- GitHub is canonical for shared committed source, but not for current dirty local work.

## Stale

- `docs/track5/endpoint-inventory.json`
- truth-snapshot endpoint counts
- any report that implies current runtime source equivalence without fresh hash evidence

## Dangerous

- Treating local dirty admin as deployed runtime
- Treating historical truth snapshots as current runtime
- Treating GitHub `main` as equivalent to `Updatesystem`
- Creating fixes before resolving source-of-truth drift

## Can Be Archived Later

- stale generated reports after they are superseded and linked
- historical endpoint inventory snapshots after current inventory is committed
- production-only stale executables only after a fresh runtime manifest

## Requires Migration

- production-only tools without repository lineage
- endpoint inventory contract counts
- default branch or release branch policy

## Recommendation

Do not start P2.9 until runtime source hashes and local/GitHub strategy are resolved.
