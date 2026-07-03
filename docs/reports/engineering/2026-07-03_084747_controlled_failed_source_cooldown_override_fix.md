# Controlled Failed Source Cooldown Override Fix

timestamp: 2026-07-03_084747

## Summary

Phase 4 MEDIUM_BATCH certification resumed after service verification wrapper deployment.
The run did not reach Runtime Apply because Planner produced zero selected moves.

Production artifact:

- `/tmp/v7_phase4_medium_batch_after_service_timeout_fix_20260703T083414.json`

Observed terminal state:

- `final_verdict=GOVERNED_TRANSACTION_STOPPED`
- `stop_reason=l3_production_validation_transition_blocked`
- `transition.errors=["l3_validation_selected_move_count_missing"]`
- `transition.selected_move_count=0`

Direct Planner probe confirmed:

- users `10.7.0.16` through `10.7.0.40` were assigned to `wireguard-1779454504-c43409`;
- `wireguard-1779454504-c43409` was a controlled certification source and unavailable;
- healthy targets existed;
- Planner still selected no moves because recent pool restore created `cooldown_active_*` for certification users.

## Root Cause

Owner:

- `tools/v7-users-autoswitch`

Function:

- `_l3_failed_source_cooldown_override_context()`

Defect:

- Existing cooldown override allowed persisted failed-source incident evacuation.
- It also built requested-source context for `--source-egress`, but the final allow condition only accepted `continuity_source == persisted_incident`.
- Controlled certification failed-source observations with `continuity_source == confirmed_observation` therefore remained trapped by normal recent-switch cooldown.

This blocked certification users immediately after controlled pool restore even though:

- source was a controlled failed source;
- users were certification users on that source;
- targets were eligible;
- the mission explicitly requested that source.

## Implementation

Changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Correction:

- Cooldown override remains allowed for:
  - persisted incident continuation;
  - requested failed source scope;
  - confirmed observation only when the scope proves `controlled_certification_failure.confirmed`.

Normal production observation cooldown remains enforced.

No broad automation was enabled.
No max-users increase was introduced.
No Runtime/Planner/Authority/Restore Barrier bypass was introduced.

## Tests

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-governed-canary-dry-run-cycle tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_governed_canary_cli.py
```

Results:

- `tests.unit.test_v7_users_autoswitch_policy`: 138 tests OK
- affected combined suites: 167 tests OK
- `py_compile`: OK

Regression added:

- `test_requested_controlled_failed_source_cooldown_does_not_trap_certification_user`

Regression preserved:

- `test_emergency_failover_autonomy_blocks_recent_cooldown`

## Production Impact

Local patch only until deployment.

Expected production behavior after deployment:

- Controlled certification pool restore cooldown no longer prevents evacuation from the controlled failed source.
- Ordinary emergency failover cooldown still blocks non-controlled observations.

## Current Certification State

Current phase:

- Phase 4 MEDIUM_BATCH certification

Current status:

- Not certified yet.

Next step:

- Safe deploy.
- Resume Phase 4 on `wireguard-1779454504-c43409` with `--max-users 10`.
