# Phase 5 Downstream Proof Guard Fix

## Summary

Controlled Production Certification Program execution was in Phase 5: `LARGE_BATCH`.

The latest Phase 5 attempt stopped before apply:

- Payload: `/tmp/v7_phase5_large_batch_after_registry_only_fix_20260703T072130.json`
- `final_verdict`: `GOVERNED_TRANSACTION_STOPPED`
- `transaction_status`: `STOP_SAFE`
- `stop_reason`: `l3_production_validation_transition_blocked`
- `selected_move_count`: `0`
- `apply_executed`: `false`

The stop was not caused by Authority, Approved Plan Lock, Restore Barrier, or Runtime Apply.

The first proven blocker was Planner candidate eligibility:

- controlled incident source: `wireguard-1779454504-c43409`
- affected certification users: `25`
- selected moves: `0`
- controlled users remained on source: `25`
- all alternative targets were rejected by safety:
  - `egress_safety_quarantine`
  - `egress_failed_verifications_limit`

The safety quarantine was traced to the previous Phase 4 `MEDIUM_BATCH` execution.

## Root Cause

The previous Phase 4 production payload was incorrectly classified as PASS.

Payload:

`/tmp/v7_phase4_medium_batch_after_metadata_fix_20260703T063801.json`

Top-level result claimed:

- `final_verdict`: `L3_PRODUCTION_PROVEN`
- `transaction_status`: `COMPLETED`
- `apply_executed`: `true`
- `users_moved`: `10`

However, the actual downstream apply result contained verification and rollback failures:

- users `10.7.0.16` through `10.7.0.25`
- every `apply_result.results[*].verify_rc = 1`
- every `apply_result.results[*].rollback_rc = 1`

This means Phase 4 did not satisfy the Controlled Production Certification Program PASS criteria.

## Owner Resolution

Blocking owner:

`tools/v7-governed-canary-dry-run-cycle`

Exact function:

`execute_l3_production_validation()`

Terminal classification:

`IMPLEMENTATION_DEFECT`

Reason:

The owner trusted `l3_learning_closure.capability_state.production_proven` without independently validating the downstream proof returned by the existing Runtime Apply owner:

- `apply_result.applied`
- `apply_result.results[*].verify_rc`
- `apply_result.results[*].rollback_rc`
- apply command status

This allowed a failed verification/failed rollback batch to be reported as `L3_PRODUCTION_PROVEN`.

## Fix

Patched existing owner only:

- `tools/v7-governed-canary-dry-run-cycle`

Added:

- `l3_production_validation_proof_quality()`

The production validation verdict now requires both:

1. existing learning/capability state claims production was proven;
2. downstream proof quality is clean:
   - autoswitch apply command succeeded;
   - Runtime Apply was performed;
   - verification results exist;
   - every selected move has `verify_rc == 0`;
   - no rollback failure is present.

If downstream proof contradicts the learning claim, the result becomes:

- `final_verdict`: `STOP_SAFE`
- `transaction_status`: `STOP_SAFE`
- `stop_reason`: `l3_production_validation_downstream_proof_failed`

`users_moved` now counts verified successful users for certification evidence.

## Tests

Added regression test:

- `test_l3_production_validation_rejects_learning_proven_when_verification_failed`

Test proves:

- learning may claim `production_proven=true`;
- if `verify_rc=1` and `rollback_rc=1`, governed validation returns `STOP_SAFE`;
- `production_proven=false`;
- `users_moved=0`;
- blockers include:
  - `verification_failed`
  - `rollback_failed`

Commands:

`python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_v7_users_autoswitch_policy`

Result:

- `Ran 149 tests`
- `OK`

Compile:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-governed-canary-dry-run-cycle tests/unit/test_governed_canary_cli.py`

Result:

- `PASS`

## Production State Before Deploy

Controlled source restoration verified:

- interface: `v7e06a394c478`
- `interface_rc = 0`
- certification users on source: `25`
- `V7_USER_ROUTE_CHECK=OK`

## Certification Program Impact

Phase 4 `MEDIUM_BATCH` must be reclassified from PASS to interrupted/invalid evidence because the persisted payload proves downstream verification and rollback failures.

Phase 5 `LARGE_BATCH` is not eligible to continue until Phase 4 is rerun and reaches a real terminal engineering outcome under the corrected proof guard.

This is not a new architecture.

This is a correction to the existing governed production validation owner.

## Next Step

Safe deploy the fix.

Then resume the interrupted certification program by rerunning Phase 4 `MEDIUM_BATCH` through controlled production after restoring the controlled source and ensuring target quarantine is either expired or resolved by existing safety policy.

