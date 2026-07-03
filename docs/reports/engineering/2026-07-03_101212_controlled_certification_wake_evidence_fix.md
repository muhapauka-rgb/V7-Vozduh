# Controlled Certification Wake Evidence Fix

Timestamp: 2026-07-03 10:12:12 +07

## Summary

Phase 4 MEDIUM_BATCH controlled production certification reached a governed STOP before Restore Barrier and Runtime Apply.

Payload:

- `/tmp/v7_phase4_medium_batch_20260703T060314.json`
- `final_verdict = GOVERNED_TRANSACTION_STOPPED`
- `transaction_status = STOP_SAFE`
- `stop_reason = l3_production_validation_transition_blocked`
- nested planner summary:
  - `candidate_moves_total = 11`
  - `selected_moves = 0`
  - `emergency_failed_sources = []`
  - `emergency_failover_authorized = false`
  - `l3_wake_decision = REJECT_WAKE`
  - `l3_incident_state = NO_INCIDENT_NO_EVIDENCE`

## Root Cause

The controlled certification source `wireguard-1779454504-c43409` was intentionally placed into `maintenance` through the existing egress lifecycle owner, and certification users remained assigned to it.

Planner correctly produced failover candidate decisions for the affected controlled users:

- `current_egress = wireguard-1779454504-c43409`
- `move_type = failover`
- `reason = current_egress_not_eligible`

However, the existing L3 wake bridge only accepted canonical current-channel failure evidence produced from `v7-state.json` severity:

- `diagnose_severity = FAIL`
- `diagnose_reason = interface_down_or_missing`

Controlled certification maintenance made the source unavailable through `egress.registry enabled/state`, not through `v7-state.json` diagnostic severity. Therefore Wake had candidate proposals but no confirmed current-channel-failure evidence.

Classification:

- Owner: `tools/v7-users-autoswitch`
- Resolution state: `IMPLEMENTATION_DEFECT`
- Exact gap: controlled production evidence generation was not consumed by existing L3 Wake/Incident source scope.

## Changed Files

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Exact Owner / Function Patched

Owner: `tools/v7-users-autoswitch`

Functions:

- `_controlled_certification_failure_context`
- `_current_channel_failure_evidence`
- `_l3_failed_source_scope`
- `_candidate_json`

## Contract Preservation

The patch does not make plain maintenance a legal L3 wake source.

Confirmed current-channel failure is produced for controlled certification only when all of the following are true:

- source has `controlled_certification_source=1`;
- source is unavailable by existing registry state (`enabled=0` or `maintenance|disabled|quarantine|down`);
- enabled affected users on that source have `certification_user=1`;
- production registry evidence is fresh;
- the affected user is inside the certification scope.

Plain operator maintenance remains non-executable:

- Wake remains `REJECT_WAKE`;
- selected moves remain empty;
- broad automation remains disabled.

## Tests

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Results:

- `125` unit tests passed.
- `py_compile` passed.

## Production Impact

Production was restored to safe baseline before patching:

- `v7-egress-set-state wireguard-1779454504-c43409 enabled --apply`
- certification user routes repaired via `v7-user-reconcile-apply --repair routing --apply --confirm REPAIR_USER`
- `v7-user-route-check = OK`

Deploy not yet performed in this report.

## Next Step

Commit, push, safe deploy, verify convergence, then resume Phase 4 MEDIUM_BATCH from the interrupted controlled certification mission.
