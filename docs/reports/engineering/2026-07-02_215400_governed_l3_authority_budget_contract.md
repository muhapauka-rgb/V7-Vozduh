# Governed L3 Authority Budget Contract

Timestamp: 2026-07-02 21:54:00 Asia/Bangkok

Verdict: GOVERNED_L3_BUDGET_CONTRACT_READY

## Summary

The hard single-user constraint in the governed L3 production validation owner has been replaced with the existing authority budget contract.

The production default remains CANARY / max_users=1. Larger batches are now structurally possible only when the existing Planner/Authority budget gate authorizes them. No new Runtime, Planner, Authority, Restore Barrier owner, Wake owner, Packet owner, or execution path was created.

Commit deployed:

- Branch: Updatesystem
- Commit: e390d924987f3283b2424deb133a4bbf963c2b7a
- Message: Use authority budget for governed L3 validation

## Changed Files

- tools/v7-governed-canary-dry-run-cycle
- tools/v7-users-autoswitch
- admin_core/operator_execution_pipeline.py
- tests/unit/test_governed_canary_cli.py
- tests/unit/test_v7_users_autoswitch_policy.py

## Exact Owners And Functions Patched

### tools/v7-governed-canary-dry-run-cycle

Owner: governed L3 production validation owner.

Functions changed:

- `execute_l3_production_validation()`
- `l3_packet_constraints_ok()`
- `run_autoswitch_apply()`
- `materialize_governed_transaction_feedback()`

New helper:

- `authorized_l3_budget_from_plan()`

The former hard stop:

```text
max_users == 1
```

is now:

```text
requested_max_users <= plan.safety.authority_budget_gate.current_allowed_user_budget
```

If the authority budget gate is absent, the owner fails closed to CANARY behavior:

```text
authorized_l3_budget = 1
```

Batch apply no longer forces `--max-selected-moves 1` when the existing authority budget permits more than one selected move. For CANARY, the prior single-user user/source/target apply identity is preserved.

Feedback materialization now writes per-user feedback records through the existing `operator_execution_feedback` owner. No new Learning owner was introduced.

### admin_core/operator_execution_pipeline.py

Owner: operator execution transition owner.

Function changed:

- `l3_production_validation_runtime_action_transition()`

The old transition rejected any `max_users != 1` and any selected move count other than one. It now accepts:

```text
1 <= len(selected_moves) <= max_users
```

All existing failover, user/source/target, and emergency failover requirements remain enforced.

### tools/v7-users-autoswitch

Owner: Planner/autoswitch policy owner.

Function changed:

- `AutoswitchPlanner._approved_l3_production_validation_envelope()`

The approved production validation envelope now validates selected moves against `authority_budget.current_allowed_user_budget` instead of requiring exactly one selected move. CANARY remains one user because the default authority budget remains one.

## Contract Reuse

No new contract was created.

Existing contract reused:

```text
plan.safety.authority_budget_gate.current_allowed_user_budget
```

Existing authority classes are preserved:

```text
CANARY        -> 1
SMALL_BATCH   -> 5
MEDIUM_BATCH  -> 10
LARGE_BATCH   -> 25
XLARGE_BATCH  -> 50
FULL_INCIDENT -> remaining affected users on the same active failed-source incident
```

The implementation consumes the current allowed budget emitted by the existing authority/capability model. It does not promote the class, certify Stage 1, or change production timer scope.

## Safety Invariants Preserved

- Authority is still required.
- Approved Plan Lock is still required.
- Restore Barrier is still required.
- Runtime Apply is still required.
- Verification is still required.
- Rollback/no-rollback closure is still required.
- Retry-exhausted semantic attempts remain governed by the existing selection logic.
- Incident source continuity remains governed by the existing incident continuation logic.
- `max_users` from CLI is not trusted by itself.
- `requested_max_users > authorized_l3_budget` is rejected before apply.
- CANARY default remains max_users=1.

## Tests

Focused regression:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_routes_through_pipeline_before_apply \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_rejects_requested_batch_above_canary_budget \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_accepts_medium_budget_batch_without_single_user_override \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_packet_constraints_reject_selected_count_above_authorized_budget \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_packet_constraints_accept_small_batch_two_users_with_small_budget \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_production_validation_blocks_two_users_and_source_recovered
```

Result:

```text
Ran 6 tests
OK
```

Governed canary CLI:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 21 tests
OK
```

Autoswitch policy:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
```

Result:

```text
Ran 120 tests
OK
```

Operator execution packet and pipeline:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_operator_execution_pipeline
```

Result:

```text
Ran 77 tests
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile \
  tools/v7-governed-canary-dry-run-cycle \
  tools/v7-users-autoswitch \
  admin_core/operator_execution_pipeline.py \
  tests/unit/test_governed_canary_cli.py \
  tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
PASS
```

Diff hygiene:

```text
git diff --check -- tools/v7-governed-canary-dry-run-cycle tools/v7-users-autoswitch admin_core/operator_execution_pipeline.py tests/unit/test_governed_canary_cli.py tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
PASS
```

## Safe Deploy

Safe deploy was run through the existing deployment owner.

Post-deploy dry-run verification after apply:

```json
{
  "final_verdict": "PASS",
  "deployment_required": false,
  "blockers": []
}
```

Actual production fingerprint read over SSH from `/opt/v7/runtime-fingerprint.json`:

```json
{
  "runtime_branch": "Updatesystem",
  "runtime_commit": "e390d924987f3283b2424deb133a4bbf963c2b7a",
  "runtime_created_at": "2026-07-02T14:51:36+00:00"
}
```

Deployed runtime files relevant to this task:

```json
[
  {
    "local_path": "tools/v7-users-autoswitch",
    "remote_path": "/usr/local/bin/v7-users-autoswitch",
    "sha256": "60c229a396a7cba2a3332468f9e3055fcd0fcad3b0f6aaba22a4157b3c2fba67"
  },
  {
    "local_path": "tools/v7-governed-canary-dry-run-cycle",
    "remote_path": "/usr/local/bin/v7-governed-canary-dry-run-cycle",
    "sha256": "2de46317fe7c92fea81a41118249d5db08d0a8f0b1c772ed6c393188eaa5c993"
  },
  {
    "local_path": "admin_core/operator_execution_pipeline.py",
    "remote_path": "/usr/local/bin/admin_core/operator_execution_pipeline.py",
    "sha256": "212cc3e436ba75b3fffa008cc71de14cec7bd433b6fa498be65df0c993431e11"
  }
]
```

## Production Impact

Production remains bounded to one user per governed cycle.

Actual production systemd entrypoint read over SSH:

```text
ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1
```

No Stage 1+ production movement was run.

No `max_users=5` production movement was run.

No broad automation was enabled.

Users moved by this task: 0

## What This Fix Enables

Future certified stages can now consume the existing authority budget instead of hitting a hardcoded one-user wall in the governed owner.

The owner will allow a batch only when both are true:

```text
requested_max_users <= authorized_l3_budget
selected_move_count <= authorized_l3_budget
```

If production remains CANARY, the behavior remains one-user validation.

## What This Does Not Certify

This task does not certify Stage 1.

It does not prove that a two-user or five-user production batch should be executed now.

It only removes the incompatible hardcoded validation limit and proves that the existing authority budget can control the governed owner contract.

## Next Required Action

Run a separate Stage 1 certification task only after explicit authorization.

That task should prove the existing authority budget has promoted beyond CANARY and then run a bounded production validation at the certified budget. Until then, production remains max_users=1.
