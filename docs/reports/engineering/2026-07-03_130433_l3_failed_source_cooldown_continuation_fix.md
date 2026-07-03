# L3 Failed Source Cooldown Continuation Fix

## Summary

Phase 4 MEDIUM_BATCH certification resumed after the stale Restore Barrier preflight reset fix. The next production run stopped before Runtime Apply:

- final_verdict: `GOVERNED_TRANSACTION_STOPPED`
- transaction_status: `STOP_SAFE`
- stop_reason: `l3_production_validation_transition_blocked`
- transition error: `l3_validation_selected_move_count_missing`
- selected_move_count: `0`

The production artifact showed an active persisted incident-source continuity object for `wireguard-1779454504-c43409` with 20 affected users, but every affected user decision stayed `keep` with `cooldown_active_*` even though healthy failover candidates were eligible.

## Root Cause

Owner: `tools/v7-users-autoswitch`

Function: `_decision_for_user`

Field: `cooldown_ok`

The normal switch cooldown was applied before active failed-source incident continuation could select the next affected user. This trapped remaining users on an already persisted failed-source L3 incident and prevented the existing downstream contracts from running.

A second matching gate existed in `_emergency_failover_move_evidence`, which would have added `emergency_failover_cooldown_active` even if `_decision_for_user` selected the move.

## Correction

Added a narrow helper:

- `_l3_failed_source_cooldown_override_context`

The override is allowed only when all conditions are true:

- emergency incident source continuity is active;
- continuity source is `persisted_incident`;
- the source is still failed;
- the user is currently on the incident source;
- the user is in the affected-user scope when that scope is present.

The fix does not:

- reset retry budget;
- ignore duplicate semantic attempts;
- bypass Authority;
- bypass Restore Barrier;
- bypass Runtime;
- bypass Verification;
- create a new owner;
- create a new execution path;
- enable broad automation.

## Changed Files

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Tests

Targeted regression:

```text
python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_emergency_failover_autonomy_blocks_recent_cooldown \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_active_l3_failed_source_incident_cooldown_does_not_trap_affected_user

OK
```

Full affected unit suite:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy

Ran 136 tests in 10.324s
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile \
  tools/v7-users-autoswitch \
  tests/unit/test_v7_users_autoswitch_policy.py

OK
```

## Current Phase Position

Current Phase: Phase 4 MEDIUM_BATCH certification

Interrupted breakpoint: selected move count was zero because active failed-source incident continuation was blocked by cooldown.

Next step: deploy the scoped owner fix through the standard safe deployment path and resume the same Phase 4 certification run with `--max-users 10`.

## Automation Debt

No new automation debt created. The manual breakpoint investigation remains part of the Controlled Production Certification Program execution loop.

## Workflow Debt

The repeated patch -> test -> deploy -> production validation workflow remains an existing certification execution workflow. It should be considered for future governed pipeline consolidation, but this fix does not create a new workflow dependency.
