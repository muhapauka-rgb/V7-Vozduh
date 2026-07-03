# Controlled L3 Runtime Pre-Apply Evidence Fix

Timestamp: 2026-07-03_155811

## Summary

Phase 4 MEDIUM_BATCH certification reached Planner, Authority, Approved Plan Lock, Restore Barrier, and Runtime apply invocation with 10 committed selected moves for:

- incident_source: `wireguard-1779454504-c43409`
- requested max users: `10`
- selected users: `10.7.0.16` through `10.7.0.25`

Runtime pre-apply then returned `STOP_SAFE` before applying, with:

- `source_failure_evidence_not_fresh_before_apply`
- `source_recovered_before_apply`

The selected move identity, approved plan lock, and restore barrier identity were already preserved. The breakpoint was inside the Runtime pre-apply evidence check.

## Root Cause

`tools/v7-users-autoswitch::_emergency_failover_move_evidence()` recomputed current-source failure from the frozen Planner candidate snapshot in `move["candidates"]`.

For controlled certification failed-source incidents, the canonical failed-source evidence is the live controlled production source scope:

- `egress.registry:controlled_certification_source`
- source enabled/state
- `users.registry:certification_user`
- fresh registry evidence

If the frozen candidate snapshot was missing the current candidate, still marked it eligible, or contained stale per-service rows, Runtime pre-apply could classify the same committed incident-source move as recovered or stale even though the live controlled failed-source evidence remained valid.

## Exact Owner And Function Patched

Owner: `tools/v7-users-autoswitch`

Function: `_emergency_failover_move_evidence()`

Change:

- Resolve controlled certification current-channel failure directly from `current_egress` and `user_ip` when the frozen current candidate does not already prove current-channel failure.
- Treat confirmed current-channel failure as sufficient current-source failure evidence for this L3 path.
- Do not emit `current_candidate_still_eligible` or `fresh_service_failure_evidence_required` from stale frozen service rows when confirmed current-channel failure is the active evidence owner.

## Safety Preservation

Unchanged:

- Planner
- Authority
- Approved Plan Lock
- Restore Barrier
- Runtime API
- Verification
- Rollback
- max-users budget
- target live existence/enabled checks
- ordinary recovered-source STOP_SAFE behavior

No new Runtime, Planner, Authority, Wake, Restore Barrier owner, packet owner, or execution path was created.

## Tests

Added regression tests:

- `test_controlled_certification_failure_survives_missing_current_candidate_before_apply`
- `test_controlled_certification_failure_suppresses_stale_service_failure_before_apply`

Preserved safety regression:

- `test_l3_recovery_before_apply_stops_safe`

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result:

```text
Ran 140 tests in 11.117s
OK
```

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 169 tests in 13.466s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result: PASS

## Production Impact

Production impact before deploy: NONE.

Deploy status at report creation: pending.

## Current Certification Position

Program phase: Phase 4 MEDIUM_BATCH certification.

Interrupted breakpoint: Runtime pre-apply evidence check.

Expected next step:

1. Commit and push the fix.
2. Safe deploy through the standard path.
3. Verify convergence.
4. Refresh controlled failed-source evidence if required.
5. Resume the same Phase 4 execution with `--max-users 10`.

