# L3 Service Verification Wrapper Timeout Fix

timestamp: 2026-07-03_083120

## Summary

Phase 4 MEDIUM_BATCH certification reached Runtime Apply and required-service verification.
One row failed because the parent `v7-users-autoswitch` process killed the existing service verification owner before it could return a structured verdict.

Failed production row:

- user: `10.7.0.18`
- source: `wireguard-1779454504-c43409`
- target: `vless`
- route verification: `verify_rc=0`
- required-service verification: `service_verify_rc=1`
- failed command: `v7-service-matrix-test vless telegram --timeout 5 --state-dir /opt/v7/egress/state`
- error: `timed out after 10 seconds`

## Root Cause

Owner:

- Runtime Apply / required-service verification wrapper

File:

- `tools/v7-users-autoswitch`

Function:

- `_verify_emergency_required_services()`

Defect:

- The parent wrapper used `timeout=timeout_sec + 5`.
- With the default emergency service timeout of `5`, the parent killed `v7-service-matrix-test` after `10` seconds.
- The child owner has an existing canonical writer-lock timeout (`DEFAULT_LOCK_WAIT_SECONDS=90`) and can return structured `LOCK_TIMEOUT` if the lock is unavailable.
- The parent timeout was therefore shorter than the child owner's legal lock/probe budget.

This is an owner invocation defect, not a new architecture issue.

## Implementation

Changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Correction:

- `_verify_emergency_required_services()` now passes the existing `--lock-timeout-sec` argument to `v7-service-matrix-test`.
- Parent subprocess timeout is now:

```text
service_verify_timeout_seconds + service_matrix_lock_timeout_sec + 5
```

The child owner remains responsible for:

- acquiring the service-matrix writer lock;
- returning `LOCK_TIMEOUT` when appropriate;
- running the real required-service probe;
- returning the service verdict.

No lock bypass was introduced.
No verification weakening was introduced.
No Runtime shortcut was introduced.

## Tests

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Results:

- `tests.unit.test_v7_users_autoswitch_policy`: 137 tests OK
- `py_compile`: OK

Regression added:

- `test_emergency_service_verification_parent_timeout_includes_lock_timeout`

## Production Impact

Production movement impact from local patch:

- None.

Expected production behavior after deployment:

- Required-service verification is still mandatory.
- Lock contention still fails safely.
- Parent wrapper no longer kills `v7-service-matrix-test` before the child can return its canonical verdict.

## Current Certification State

Current phase:

- Phase 4 MEDIUM_BATCH certification.

Current terminal state:

- Interrupted at required-service verification / rollback breakpoint.

Next step:

- Deploy through safe path.
- Resume the same Phase 4 MEDIUM_BATCH certification on controlled source `wireguard-1779454504-c43409`.
- If verification still fails, classify the child verdict as real service failure or lock timeout based on structured output.
