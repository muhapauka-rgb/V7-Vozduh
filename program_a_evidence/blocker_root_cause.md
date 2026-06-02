# Program A Blocker Root Cause

## Blocker

Program A cannot proceed to live execution because the mandatory pre-execution candidate gate produced no selected move and the restore-barrier clearance no longer matches the fresh planner generation.

## Evidence

- `phase1_fresh_runtime_reality.txt`: runtime branch/commit/deploy are known and aligned, but restore barrier still references an older Z3.2 clearance.
- `phase2_local_fresh_planner_plan.json`: selected move count is `0`; terminal reason is `dry_run_restore_barrier_clearance_generation_expired`.
- `phase3_restore_settle_local.txt`: restore-settle gate is `CONDITIONAL`; execution is not allowed now.

## Immediate causes

1. Restore-barrier generation clearance expired at `2026-06-01T18:02:59.305408+00:00`.
2. Approved generation id is `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`.
3. Fresh planner generation id is `6b1bf2bd3db4835bfc3c4e8d99ea2fe4506f96a7d6c4bfeb3667015cf7223d52`.
4. Approved selected move hash expects one move, but the fresh planner selected hash is the empty-move hash.
5. Current runtime health/capacity/service evidence yields no eligible target.

## Why this was not fixed in Program A

Program A explicitly forbids restore-barrier modification, scheduler modification, service matrix modification, policy modification, user movement, runtime mutation, and bypass execution. The only fixes that could make execution possible would require one or more forbidden actions:

- refresh or regenerate restore-barrier clearance;
- refresh health/service/runtime state through mutating runtime tools;
- change canary/manual/reserve policy status;
- execute movement through direct `v7-user-switch` or admin endpoints.

Those actions would violate Program A. Therefore the correct outcome is NO-GO with evidence, not a bypass or partial lifecycle claim.

## Root cause verdict

root_cause=stale_expired_restore_clearance_plus_no_fresh_eligible_selected_move
external_blocker=true
safe_in_scope_fix_available=false
live_execution_performed=false
