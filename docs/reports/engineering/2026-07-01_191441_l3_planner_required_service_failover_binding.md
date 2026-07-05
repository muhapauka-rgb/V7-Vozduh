# L3 Planner Required-Service Failover Binding

Timestamp: 2026-07-01 19:14:41 Asia/Bangkok
Status: IMPLEMENTED_LOCALLY_NOT_DEPLOYED

## Summary

Patched the existing Planner/Autoswitch owner so broad current-channel ineligibility no longer becomes an L3-executable `failover` unless the selected current source has same-subject required-service failure evidence.

The Runtime L3 gate remains unchanged and still fails closed when `current_failures` is empty.

## Inputs Read

- `docs/reference/V7_GPT_HANDOFF_2026-07-01.md`
- `docs/reports/engineering/2026-07-01_190048_codex_transition_instructions.md`
- `docs/reports/engineering/2026-07-01_172201_gpt_handoff_package.md`
- `docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md`
- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Owner

Existing owner only:

- `tools/v7-users-autoswitch`

No new Runtime, Planner, Authority, OMP, event bus, wake source, truth source, or owner was created.

## Files Changed

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Implementation

Added `AutoswitchPlanner._current_required_service_failures()` using the same selected-current required-service failure semantics consumed by Runtime L3 evidence extraction:

- `available is False`
- `truth_class == PERSISTENT_FAIL`
- service status in `DOWN`, `FAIL`, `ERROR`, `NOT_STARTED`

Changed `_decision_for_user()` so the `not current or not current.eligible` branch:

- still records `current_egress_not_eligible`;
- emits `move_type=failover` only when `_current_required_service_failures(current, important)` is non-empty;
- otherwise keeps `action=keep`, `move_type=none`, and records:
  - `l3_required_service_failure_absent`
  - `probe_only_required_before_l3_failover`

## Tests Run

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
Ran 108 tests in 8.770s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
OK
```

## Truth Result

Good L3 service-failure paths remain legal failover candidates.

Non-service current ineligibility, such as a disabled current egress without required-service failure evidence, no longer produces an L3-executable failover proposal or selected move.

## Production Impact

None yet. The patch was implemented and verified locally only.

No production deploy was performed.
No production apply endpoint was called.
No users were moved.

## Rollback Plan

Revert the local changes in:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Need New Owner?

FALSE

## Need New Backlog?

FALSE

## Need New Architecture?

FALSE

## Canonical Updates

NONE. This implements already-established L3 semantics.

## Next OMP Step

Deploy the narrow Planner/Autoswitch correction through the existing production deployment path, then rerun the bounded one-user L3 Production Validation. Runtime should now either:

- find a legal candidate with same-subject required-service failure evidence and proceed through the existing L3 gates; or
- produce a clean non-L3/no-action outcome instead of a false L3 failover candidate.

## Final Verdict

LOCAL_FIX_READY_FOR_DEPLOYMENT_VALIDATION
