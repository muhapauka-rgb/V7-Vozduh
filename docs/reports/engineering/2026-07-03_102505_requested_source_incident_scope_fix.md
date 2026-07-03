# Requested Source Incident Scope Fix

Timestamp: 2026-07-03 10:25:05 +07

## Summary

After deploying controlled certification wake evidence, Phase 4 MEDIUM_BATCH still stopped before Restore Barrier and Runtime Apply.

Payload:

- `/tmp/v7_phase4_medium_batch_after_wake_fix_20260703T061544.json`
- `final_verdict = GOVERNED_TRANSACTION_STOPPED`
- `transaction_status = STOP_SAFE`
- `stop_reason = l3_production_validation_transition_blocked`
- nested planner summary:
  - `candidate_moves_total = 11`
  - `selected_moves = 0`
  - `l3_wake_decision = REJECT_WAKE`
  - `l3_incident_state = NO_INCIDENT_NO_EVIDENCE`

Further inspection showed `selected_moves_diagnostics.incident_source_continuity_active = true` with `incident_source = awg3`. That unrelated active incident scope filtered the controlled certification candidate pool before emergency evidence could be evaluated.

## Root Cause

The governed L3 production validation owner accepted `--approved-source`, and the autoswitch owner already had `--source-egress`, but the L3 validation preview did not pass the approved source into the Planner preview.

Even when source-scoped selection was requested, `tools/v7-users-autoswitch.plan()` and `_emergency_failover_authority_gate()` allowed an unrelated active incident source to override the requested failed source.

Classification:

- Owner: `tools/v7-governed-canary-dry-run-cycle` and `tools/v7-users-autoswitch`
- Resolution state: `OWNER_INVOCATION_MISSING` plus `IMPLEMENTATION_DEFECT`
- Exact gap: requested source identity was not preserved from governed owner into Planner preview and emergency gate incident-source continuity.

## Changed Files

- `tools/v7-governed-canary-dry-run-cycle`
- `tools/v7-users-autoswitch`
- `tests/unit/test_governed_canary_cli.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`

## Exact Owner / Function Patched

Owner: `tools/v7-governed-canary-dry-run-cycle`

- `run_l3_production_validation_plan`
- `execute_l3_production_validation`

Owner: `tools/v7-users-autoswitch`

- `plan`
- `_emergency_failover_authority_gate`

## Contract Preservation

The patch does not create a new execution path.

Existing source-scoping contracts are reused:

- governed owner: `--approved-source`
- autoswitch owner: `--source-egress`

Requested source override is allowed only when the requested source itself has failed-source scope. If the requested source is not failed, unrelated active incident behavior is not bypassed.

Authority, Restore Barrier, Runtime, Verification, Rollback, and max-users limits remain unchanged.

## Tests

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-governed-canary-dry-run-cycle tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_governed_canary_cli.py
```

Results:

- `148` unit tests passed.
- `py_compile` passed.

## Production Impact

Production was restored to safe baseline before patching:

- `v7-egress-set-state wireguard-1779454504-c43409 enabled --apply`
- certification user routes repaired through `v7-user-reconcile-apply --repair routing --apply --confirm REPAIR_USER`
- `v7-user-route-check = OK`

Deploy not yet performed in this report.

## Next Step

Commit, push, safe deploy, verify convergence, then resume Phase 4 MEDIUM_BATCH with:

```text
v7-governed-canary-dry-run-cycle --max-users 10 --approved-source wireguard-1779454504-c43409 --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED
```
