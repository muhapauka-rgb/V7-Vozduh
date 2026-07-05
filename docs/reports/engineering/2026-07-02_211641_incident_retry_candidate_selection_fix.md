# Incident Retry Candidate Selection Fix

Timestamp: 2026-07-02 21:16:41 Asia/Bangkok

Mode: Discover -> Reuse -> Extend -> Implement

## Summary

Implemented the minimal candidate-selection fix for active failed-source L3 incident continuation after retry budget consumption.

The defect was that an active incident could repeatedly select the same semantic attempt:

- user: `10.7.0.2`
- source: `openvpn-1779388847-d2ad7c`
- target: `vless`

even after that same semantic attempt had already reached terminal rollback:

- `ROLLED_BACK`
- `verification_failed_rollback_completed`

This consumed `retry_budget_per_incident` and then blocked the incident with:

- `duplicate_apply_attempt`
- `l3_retry_budget_exhausted`

The fix excludes exhausted semantic attempts during active failed-source incident continuation, then continues normal ranking among remaining eligible affected users on the same `incident_source`.

## Root Cause

Candidate selection did not filter already-exhausted semantic attempts before picking the bounded `max-users=1` move for the next incident continuation cycle.

Because `10.7.0.2` kept ranking first, the Planner repeatedly selected the already-consumed semantic attempt and the governed execution chain correctly stopped on retry-budget enforcement.

The retry-budget gate was correct. The selection input to that gate was wrong for continuation.

## Changed Files

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Commit:

- `6f8775f94044b9dae5953971d424525dab72d3cb`
- `Fix L3 incident retry candidate selection`

Pushed branch:

- `origin/Updatesystem`

## Exact Owner And Functions Patched

Owner:

- `tools/v7-users-autoswitch`

Functions:

- `AutoswitchPlanner._l3_semantic_attempt_signature`
- `AutoswitchPlanner._l3_consumed_retry_attempts`
- `AutoswitchPlanner._l3_retry_budget_exhausted_for_move`
- `AutoswitchPlanner._select_moves`
- `AutoswitchPlanner._pick_projected_moves`
- `AutoswitchPlanner._emergency_failover_authority_gate`

Selection filter location:

- during `_pick_projected_moves`, after the projected target is known and before the move is accepted into `picked`.

Reason:

- semantic attempt identity requires `user`, `source`, `target`, `move_type`, and `incident_key`;
- target is only final after projected target selection;
- filtering earlier would not know the exact semantic attempt;
- filtering later would allow exhausted attempts to occupy the one-user budget.

## Retry Semantics Preservation

The implementation does not reset retry budget.

The implementation does not ignore retry budget.

The implementation does not retry exhausted semantic attempts.

The implementation does not create a new incident.

The implementation does not change Authority, Restore Barrier, Runtime, Verification, or Rollback.

The implementation only excludes a candidate when all are true:

- incident continuation is active;
- candidate `current_egress == incident_source`;
- candidate belongs to the same `incident_key`;
- candidate semantic attempt signature already has consumed retry-budget history;
- consumed attempts count is greater than or equal to `retry_budget_per_incident`.

## Unit Tests

Added regression:

- `test_active_incident_skips_exhausted_semantic_attempt_and_selects_next_user`

The test proves:

- exhausted semantic attempt is excluded;
- next remaining user is selected;
- `incident_source` remains unchanged;
- retry budget remains enforced;
- `max-users` remains `1`;
- unrelated source is not selected;
- no new incident is created.

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_active_incident_skips_exhausted_semantic_attempt_and_selects_next_user tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_persistent_retry_budget_blocks_second_attempt tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_retry_budget_ignores_denied_no_execution_attempts
```

Result:

- `Ran 3 tests`
- `OK`

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result:

- `Ran 120 tests`
- `OK`

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli
```

Result:

- `Ran 17 tests`
- `OK`

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

- PASS

## Safe Deploy

Safe deploy path:

```text
tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json
```

Deploy result:

- PASS
- blockers: `[]`
- deployment delta after deploy: `[]`
- production deploy id: `deploy-z8-14-Updatesystem-6f8775f-20260702T211435`

Production fingerprint after deploy:

```json
{
  "fingerprint_branch": "Updatesystem",
  "fingerprint_commit": "6f8775f94044b9dae5953971d424525dab72d3cb",
  "fingerprint_deploy_id": "deploy-z8-14-Updatesystem-6f8775f-20260702T211435",
  "autoswitch_sha256": "442258b99180749ef547bc1b3e767938d3600b465d934df112e409f09b921927"
}
```

## Production Validation

Command:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

Before validation:

```json
{
  "source": "openvpn-1779388847-d2ad7c",
  "remaining_enabled_users": [
    "10.7.0.2",
    "10.7.0.4",
    "10.7.0.6",
    "10.7.0.8",
    "10.7.0.9",
    "10.7.0.10",
    "10.7.0.11",
    "10.7.0.12",
    "10.7.0.13",
    "10.7.0.15"
  ],
  "count": 10
}
```

Production validation result:

```json
{
  "final_verdict": "L3_PRODUCTION_PROVEN",
  "operation_id": "govexec_7ba62cef716cc537aed3a6f0",
  "runtime_operation_id": "runtime_autoswitch_0645b377bcd6f9c8f8be6f1c",
  "incident_key": "dd5b6289529f22197e6694a7",
  "incident_source": "openvpn-1779388847-d2ad7c",
  "selected_user": "10.7.0.4",
  "selected_source": "openvpn-1779388847-d2ad7c",
  "selected_target": "vless",
  "selected_move_hash": "ff76a4b023c3b9d3ed321164676291d824f18a6d5dc554c16a7a3069abec0a98",
  "selected_moves_before_restore_barrier": 1,
  "selected_moves_after_gate": 1,
  "l3_wake_decision": "ACCEPT_WAKE",
  "approved_plan_lock_ok": true,
  "approved_plan_lock_consumed": true,
  "restore_barrier_execution_blocked": false,
  "runtime_apply_rc": 0,
  "verify_rc": 0,
  "service_verify_rc": 0,
  "verification_result": "PASS",
  "rollback_result": "NOT_REQUIRED",
  "transaction_status": "COMPLETED",
  "users_moved": 1,
  "max_users": 1
}
```

Important production proof:

- the previously exhausted user `10.7.0.2` was not selected again;
- next eligible remaining user `10.7.0.4` was selected;
- the same failed source was preserved;
- no unrelated source was selected;
- Authority, Approved Plan Lock, Restore Barrier, Runtime Apply, Verification, Rollback all remained on the existing governed path;
- Runtime mutation occurred for exactly one user;
- verification passed;
- rollback was not required.

After validation:

```json
{
  "source": "openvpn-1779388847-d2ad7c",
  "remaining_enabled_users": [
    "10.7.0.2",
    "10.7.0.6",
    "10.7.0.8",
    "10.7.0.9",
    "10.7.0.10",
    "10.7.0.11",
    "10.7.0.12",
    "10.7.0.13",
    "10.7.0.15"
  ],
  "count": 9,
  "moved_user_current": "vless",
  "exhausted_user_current": "openvpn-1779388847-d2ad7c"
}
```

Incident state after validation:

```json
{
  "incident_key": "dd5b6289529f22197e6694a7",
  "incident_source": "openvpn-1779388847-d2ad7c",
  "failed_sources": ["openvpn-1779388847-d2ad7c"],
  "selected_users": ["10.7.0.4"],
  "status": "OPEN",
  "terminal_state": "APPLIED",
  "terminal_reason": "selected_moves_applied",
  "operation_id": "runtime_autoswitch_0645b377bcd6f9c8f8be6f1c",
  "closed_at": ""
}
```

## Remaining Users

Remaining enabled users on failed source after validation:

- `10.7.0.2`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.9`
- `10.7.0.10`
- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.13`
- `10.7.0.15`

## Next Blocker

No blocker was observed for the incident retry candidate selection defect.

The bounded validation completed successfully with one real production user moved from the failed source to a healthy production target.

Further evacuation of the remaining users requires subsequent governed cycles and remains bounded by the existing max-users and validation ladder.

## Final Verdict

INCIDENT_CONTINUATION_FIXED
