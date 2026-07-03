# Controlled Certification Runtime Eligibility Fix

Timestamp: 2026-07-03 11:54:00

## Summary

Phase 4 MEDIUM_BATCH certification resumed after the Restore Barrier source bundle lease fix and reached a new breakpoint:

- payload: `/tmp/v7_phase4_medium_batch_after_lease_fix_20260703T074801.json`
- final verdict: `STOP_SAFE`
- terminal reason: `l3_production_validation_downstream_proof_failed`
- Runtime Apply: not performed
- Runtime eligibility blocker: `source_recovered_before_apply`
- wake blocker: `l3_wake_not_accepted`
- selected moves: 10 users from `wireguard-1779454504-c43409`

The previous blocker was resolved. `atomic_validation.ok=true`, `source_bundle_stability_lease_used=true`, and `prevalidated_restore_barrier_lease_used=true`.

## Root Cause

`tools/v7-users-autoswitch::_current_channel_failure_evidence()` only evaluated controlled certification current-channel failure when the current candidate had no hard block, no `FAIL` severity, and no diagnose reason.

In production controlled certification, the canonical source of degradation is `egress.registry`:

- `controlled_certification_source=1`
- controlled source unavailable through maintenance/disabled state
- certification users still assigned to the source

However, Runtime Apply live evidence could still receive a neutral `v7-state.json` row such as `diagnose_severity=OK` and `diagnose_reason=OK`. Because a diagnose reason was present, `_current_channel_failure_evidence()` skipped the controlled-certification evidence path and returned an unconfirmed channel failure. `_emergency_failover_move_evidence()` then inserted `required_service_failure_required`, which `_l3_execution_eligibility()` converted to `source_recovered_before_apply`.

## Exact Owner And Function Changed

Owner:

- `tools/v7-users-autoswitch`

Function:

- `_current_channel_failure_evidence()`

Change:

- Controlled certification current-channel failure evidence is now checked first.
- If `_controlled_certification_failure_context()` confirms the same source/user, that production object becomes the channel failure evidence before ordinary `v7-state.json` severity interpretation.

This does not create a new wake source, Runtime, Planner, Authority, Restore Barrier, or execution path.

## Why This Preserves Contracts

- Plain maintenance without `controlled_certification_source=1` remains rejected.
- Real `interface_down_or_missing` evidence remains supported.
- Runtime Apply still performs live evidence validation.
- The accepted object is an existing production object: `egress.registry:controlled_certification_source + users.registry:certification_user + egress.registry enabled/state`.
- Authority, Restore Barrier, selected move identity, packet identity, and max-users budget are unchanged.

## Tests

Added regression:

- `test_controlled_certification_failure_overrides_ok_state_reason_before_apply`

The test proves:

- controlled source unavailable + certification user + neutral `v7-state.json` with `diagnose_reason=OK` still produces `confirmed_current_channel_failure`;
- wake is accepted;
- Runtime eligibility returns `EXECUTE`;
- `source_recovered_before_apply` is not inserted;
- no live evidence blocker remains.

Executed:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_controlled_certification_failure_overrides_ok_state_reason_before_apply
.
Ran 1 test in 0.092s
OK
```

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
Ran 151 tests in 12.079s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
OK
```

## Production Impact

Production impact before deploy: none.

Deploy status at report creation: pending safe deploy.

## Interrupted Certification Mission

Interrupted phase:

- Phase 4 MEDIUM_BATCH certification

Resume point:

- safe deploy this fix;
- convergence check;
- re-run bounded Phase 4 controlled certification against `wireguard-1779454504-c43409`;
- continue the certification ladder only after Phase 4 reaches a terminal engineering outcome.

