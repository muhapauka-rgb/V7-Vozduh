# Incident Source Continuity Implemented

Timestamp: 2026-07-02_175926

Mode: Discover -> Reuse -> Extend -> Implement

## Summary

Implemented the minimal `incident_source` continuity contract inside the existing V7 L3 governed execution owner.

The fix preserves the failed production source that opened an L3 emergency failover incident across bounded governed cycles. After one successful user move, the incident remains open if the failed source is still failed and enabled affected users remain assigned to it.

No new Runtime, Planner, Authority, Restore Barrier, Wake owner, truth source, or architecture was created.

## Defect Fixed

Confirmed defect:

`INCIDENT_SOURCE_NOT_PRESERVED`

Previously, after one successful L3 move, the incident could close and the next timer/governed cycle could select an unrelated failover from a different current egress. This allowed the execution chain to evaluate `confirmed_current_channel_failure` against the selected move source instead of the original failed incident source.

## Files Changed

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Contract Implemented

`incident_source` is the failed production source that opened the L3 emergency failover incident.

For an active failed-source incident:

- planner selection is constrained to users whose `current_egress == incident_source`;
- approved plan lock is invalid if locked selected moves use a different source;
- L3 gate reuses the active incident key for continuation;
- retry budget blocks duplicate semantic apply attempts, not different users on the same failed incident source;
- successful terminal closure keeps the incident `OPEN` when remaining enabled users still exist on the failed source;
- closure still proceeds for rollback/failure/STOP containment outcomes.

## Existing Owners Reused

- Observation evidence: `v7-state.json`, `service-matrix.json`, `users.registry`
- Incident state: `l3-runtime-state.json`
- Planner/Runtime owner: `tools/v7-users-autoswitch`
- Approved Plan Lock: existing restore barrier `approved_plan_lock`
- Restore Barrier: existing `autoswitch-restore-barrier.json`

## Acceptance Coverage

Added tests proving:

1. Active failed-source incident constrains the next L3 selected move to `incident_source`.
2. An approved plan lock for a non-incident source is rejected during incident continuation.
3. A successful one-user L3 move keeps the failed-source incident open when users remain.
4. Existing retry protection still blocks repeated duplicate apply attempts.

## Verification

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_active_failed_source_incident_constrains_next_l3_selection tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_approved_plan_lock_rejects_non_incident_source_during_l3_continuation tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_success_keeps_failed_source_incident_open_when_users_remain tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_persistent_retry_budget_blocks_second_attempt
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Results:

```text
Targeted L3 tests: 4 passed
Full policy suite: 116 passed
py_compile: passed
```

## Production Impact

Production deploy performed: NO

Production validation performed: NO

Users moved: 0

## Deployment Recommendation

Deploy through the standard safe deployment path, then run one bounded governed production validation with `max-users=1`.

Expected production behavior after deploy:

- `incident_source` remains the failed source while it is still failed;
- next selected user is one of the remaining enabled users on that source;
- `confirmed_current_channel_failure` is evaluated against the failed incident source;
- `selected_moves_after_gate == 1`;
- unrelated source moves are rejected for this incident.

## Final Verdict

`INCIDENT_SOURCE_CONTINUITY_FIXED`
