# HASH_MISMATCH_ROOT_CAUSE_REPORT

Program: PROGRAM_SOURCE1_SNAPSHOT_SOURCE_CONSISTENCY_CLOSURE_AND_OPERATOR_VISIBLE_UNLOCK
Date: 2026-06-05

## Root Cause

Root cause: STALE_SOURCE_REFERENCE.

The planner loaded service_matrix and quality_summary before pre-planner refresh. The refresh command could then build fresh snapshots from newer source files. The planner gate compared the refreshed snapshot source_hashes against the older in-memory objects.

This created false source_hash_mismatch for:

- service-scores:service_matrix
- service-scores:quality_summary
- channel-service-scores:service_matrix
- channel-service-scores:quality_summary

## Not Root Cause

- Not a duplicate truth source.
- Not a duplicate snapshot root.
- Not a broken hash algorithm.
- Not a reason to weaken fail-closed behavior.

## Fix

After REFRESH_SUCCESS in write mode, planner reloads source inputs before snapshot gate.

## Decision -> Action

Condition: snapshot source_hashes do not match planner source inputs.
Decision: fail closed unless planner can prove it validated the same post-refresh source truth.
Action: reload post-refresh source inputs; if mismatch remains, stop planner influence.
Executor: tools/v7-users-autoswitch.
Trigger: source_hash comparison.
Written Evidence: source_reload evidence and snapshot gate validation errors.
Blocked Actions: selected_moves, apply, operator_visible_promotion when mismatch remains.
Next State: fail_closed_snapshot_gate or planner_advisory_context_available.

