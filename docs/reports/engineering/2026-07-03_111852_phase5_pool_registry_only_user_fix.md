# Phase 5 Pool Expansion And Registry-Only User Fix

Timestamp: 2026-07-03 11:18:52 Asia/Bangkok

## Certification Phase

Current Program Phase: Phase 5 LARGE_BATCH Certification

Current Task: Certification Pool Sufficiency and first LARGE_BATCH execution attempt.

Terminal State for pool decision: `POOL_EXPANDED`

Terminal State for phase execution: not yet terminal; breakpoint resolved locally, deploy pending.

## Pool Sufficiency Decision

Required pool for LARGE_BATCH:

25 enabled Certification Users on the same controlled incident source.

Initial pool after MEDIUM_BATCH:

1 enabled Certification User remained on `wireguard-1779454504-c43409`.

Decision:

Pool insufficient, expansion allowed through existing owners.

Existing owners reused:

- `v7-user-switch`
- `v7-user-create-from-ipam`
- `v7-egress-set-state certification-scope`
- `v7-user-reconcile-apply`

No new owner, Runtime, Planner, Authority, Restore Barrier, Wake owner, packet owner, or execution path was created.

## Pool Expansion Performed

Returned existing Certification Users to controlled source:

- `10.7.0.16` through `10.7.0.25`

Created new real production IPAM users:

- `10.7.0.27` through `10.7.0.40`

Creation owner:

`v7-user-create-from-ipam --apply --confirm CREATE_IPAM_USER`

Certification scope owner:

`v7-egress-set-state wireguard-1779454504-c43409 certification-scope --certification-users ... --certification-group large-batch --apply`

Post-expansion pool:

25 enabled users assigned to `wireguard-1779454504-c43409`.

Route verification after restoration and repair:

`V7_USER_ROUTE_CHECK=OK`

## First LARGE_BATCH Attempt

Command:

`/usr/local/bin/v7-governed-canary-dry-run-cycle --max-users 25 --approved-source wireguard-1779454504-c43409 --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --pretty`

Payload:

`/tmp/v7_phase5_large_batch_20260703T071613.json`

Result:

- final_verdict = `GOVERNED_TRANSACTION_STOPPED`
- transaction_status = `STOP_SAFE`
- stop_reason = `l3_production_validation_transition_blocked`
- apply_executed = false
- users_moved = 0
- transition error = `l3_validation_selected_move_count_missing`

## Root Cause

The controlled source scope saw 23 affected Certification Users instead of the 25 users present in `users.registry`.

The missing users were newly provisioned registry-only users:

- `10.7.0.39`
- `10.7.0.40`

`AutoswitchPlanner._load_users()` still preferred `v7-state.json:users` as the complete user list when present. The previous metadata fix merged `users.registry` fields into live users, but it did not append registry users absent from the live snapshot.

This caused freshly provisioned Certification Users to exist in production registry and routing, but remain invisible to Planner until a later state snapshot caught up.

## Owner And Function Changed

Owner:

`tools/v7-users-autoswitch`

Function:

`AutoswitchPlanner._load_users()`

Change:

- If `v7-state.json:users` exists, keep it as the live-precedence source.
- Append `users.registry` rows whose IPs are absent from `v7-state.json:users`.
- Preserve registry metadata merge for rows present in both objects.

## Why This Is Minimal

The patch only corrects the existing user loader's object continuity.

Unchanged:

- Runtime Apply
- Authority
- Approved Plan Lock
- Restore Barrier
- Verification
- Rollback
- Wake policy
- max-users budget
- batch ladder contract

## Tests

Command:

`python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli`

Result:

`Ran 148 tests in 10.518s - OK`

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py`

Result:

PASS

## Regression Added

The controlled certification wake test now reproduces a live snapshot missing one registry Certification User.

Expected result:

- The incident source continuity affected-user count includes the registry-only user.
- The selected move cap still limits execution to the requested budget.

## Production Impact

Users moved during failed LARGE_BATCH attempt:

0

Controlled source was restored after STOP_SAFE.

Route repair was applied through `v7-user-reconcile-apply`.

Final safety check:

`V7_USER_ROUTE_CHECK=OK`

## Current Execution Position

Phase 5 LARGE_BATCH remains active.

Next required step:

1. Commit and deploy the registry-only user visibility fix.
2. Recreate controlled degradation.
3. Resume the same Phase 5 LARGE_BATCH execution with `--max-users 25`.

## Automation Debt Delta

Created:

- Manual pool expansion required several owner commands.
- Manual route repair was needed after source restoration for newly created users.

Classification:

`PIPELINE_CANDIDATE`

Required future pipeline:

Certification Pool Expansion owner command that creates, assigns, marks, repairs routing, and emits a pool decision record in one governed workflow.

## Workflow Debt Delta

Created:

- Manual Phase 5 preparation workflow.

Closed:

- Owner Resolution proved existing owners can expand the pool; no new architecture is required.
