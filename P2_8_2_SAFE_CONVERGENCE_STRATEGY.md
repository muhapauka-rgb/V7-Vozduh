# P2.8.2 Safe Convergence Strategy

Project: V7 Vozduh
Block: P2.8.2

## Do Not Perform In This Block

No sync, push, merge, rebase, deploy, runtime mutation, systemd change, or service restart.

## Preserve

- Runtime Admin API read-only execution API patch.
- Runtime hash/metadata evidence.
- Local P2.1-P2.7 candidate implementation.
- Existing `origin/Updatesystem` branch history.

## Archive Or Quarantine

- Remote-only branch `codex/dynamic-load-autoswitch-pr` after branch owner/review decision.
- Stale Admin API branch snapshots that are not runtime nor development baseline.
- Any production-only copy that lacks source lineage until mapped.

## Migrate

- Runtime-only execution read APIs into Git through a reviewed patch or explicit replacement by local candidate implementation.
- Local P2.2-P2.7 preview/candidate workflow code into a reviewed commit series.
- Branch policy docs: `main` vs `Updatesystem` release/development roles.

## Review

- Whether local dirty execution/candidate APIs supersede runtime execution read-only APIs.
- All route additions under `/api/execution/*`.
- All UI additions for execution drafts, gates, candidates, approval, governance, rehearsal, and workflow.
- Retention behavior for any added read stores.

## Never Copy Automatically

- Runtime secrets or auth material.
- `/etc/v7` config content without secret-safe classification.
- `/opt/v7` live user/channel/state files.
- Runtime-only Admin API into Git without diff review.
- Local dirty Admin API into runtime without an explicit deploy block.

safe_convergence_strategy_defined=true
