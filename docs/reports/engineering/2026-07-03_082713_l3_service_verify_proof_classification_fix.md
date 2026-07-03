# L3 Service Verification Proof Classification Fix

timestamp: 2026-07-03_082713

## Summary

Phase 4 MEDIUM_BATCH certification was resumed after the governed apply timeout fix.
Production reached Runtime Apply with `max-users=10`; the apply command completed with return code `0` and timeout budget `360` seconds.

The run did not certify Phase 4 because the governed owner reported:

- `final_verdict=STOP_SAFE`
- `stop_reason=l3_production_validation_downstream_proof_failed`
- `users_moved=10`
- `verification_result=PASS`
- `rollback_result=ROLLBACK_FAILED`

This was internally contradictory. The production artifact proved that one row had:

- `user_ip=10.7.0.18`
- `verify_rc=0`
- `service_verify_rc=1`
- `verification_failure_reason=required_service_verify_timeout`
- `rollback_attempted=true`
- `rollback_rc=1`
- `rollback_output=egress disabled: wireguard-1779454504-c43409`

The route check passed, but required-service verification failed. The governed proof owner counted route verification only and therefore incorrectly classified the row as a verified success.

## Production Evidence

Artifact:

- `/tmp/v7_phase4_medium_batch_after_timeout_fix_20260703T062509.json`

Evidence:

- `transition.ok=true`
- `transition.status=READY`
- `transition.selected_move_count=10`
- `autoswitch_apply.ok=true`
- `autoswitch_apply.returncode=0`
- `autoswitch_apply.timeout_seconds=360`
- `apply_executed=true`
- `users_moved=10`
- `production_proof_quality.blockers=["rollback_failed"]`
- `production_proof_quality.verified_success_count=10`
- `production_proof_quality.rollback_failures[0].user_ip=10.7.0.18`

Raw failed service probe:

```text
service verify error: Command '['v7-service-matrix-test', 'vless', 'telegram', '--timeout', '5', '--state-dir', '/opt/v7/egress/state']' timed out after 10 seconds
```

## Root Cause

Owner:

- Governed L3 production validation owner

File:

- `tools/v7-governed-canary-dry-run-cycle`

Function:

- `l3_production_validation_proof_quality()`

Defect:

- The proof-quality classifier treated `verify_rc == 0` as complete verification success.
- It did not include `service_verify_rc`.
- Therefore a row with route verification PASS and required-service verification FAIL was counted as `verified_success`.

## Implementation

Changed:

- `tools/v7-governed-canary-dry-run-cycle`
- `tests/unit/test_governed_canary_cli.py`

Correction:

- Added row-level verification semantics:
  - route verification must pass;
  - if required-service verification exists, `service_verify_rc` must also pass.
- `verification_failures` now include rows where `service_verify_rc != 0`.
- `verified_successes` now exclude rows where required-service verification failed.
- top-level `verification_result` now reports FAIL when any required-service verification failed.

## Tests

Commands:

```text
python3 -m unittest tests.unit.test_governed_canary_cli
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-governed-canary-dry-run-cycle tests/unit/test_governed_canary_cli.py
```

Results:

- `tests.unit.test_governed_canary_cli`: 29 tests OK
- `py_compile`: OK

Regression added:

- `test_l3_production_proof_counts_service_verify_failure_as_verification_failure`

## Production Impact

Production movement impact:

- None from this local patch.

Behavioral impact after deployment:

- No Planner change.
- No Runtime change.
- No Authority change.
- No Restore Barrier change.
- No user movement logic change.
- Governed proof classification now reports required-service verification failure correctly.

## Current Certification State

Current phase:

- Phase 4 MEDIUM_BATCH certification

Terminal state:

- Not certified yet.

Current blocker after proof-classification correction:

- Required-service verification timeout for `vless telegram`.
- Rollback then attempted to return `10.7.0.18` to the controlled failed source and failed because `wireguard-1779454504-c43409` was disabled/failed.

## Next Required Engineering Mission

Continue Phase 4 from the same breakpoint.

Owner Resolution:

- Blocking owner: Runtime required-service verification / rollback outcome classification.
- Exact failed command: `v7-service-matrix-test vless telegram --timeout 5 --state-dir /opt/v7/egress/state`.
- Required resolution:
  1. Determine why `v7-service-matrix-test` timed out for `vless telegram` during batch verification.
  2. Determine whether rollback to a controlled failed incident source is canonical or should be classified as containment / no-safe-rollback.
  3. Reuse existing owners only.
  4. Resume Phase 4 MEDIUM_BATCH certification after correction.
