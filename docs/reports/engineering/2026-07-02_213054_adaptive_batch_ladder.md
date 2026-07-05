# Adaptive Governed Batch Ladder

Timestamp: 2026-07-02 21:30:54 Asia/Bangkok

Mode: Discover -> Reuse -> Extend -> Implement

Result: REMAINING_BATCH_BLOCKER

## Summary

The adaptive governed batch ladder was not implemented in this run.

The strengthened precondition required proving that existing downstream owners are batch-compatible before implementation. That precondition failed at the governed L3 production validation executor.

The system already contains several batch-aware contracts:

- Authority budget classes and evidence-based promotion exist.
- Planner can select more than one move when authority budget permits.
- Packet and Approved Plan Lock can carry multiple selected moves.
- Restore Barrier can serialize selected move count/hash for multiple moves.
- Runtime Apply loops over `plan["selected_moves"]`.
- Runtime Apply records partial success.
- Operation-scoped rollback packet can include and execute multiple users.

However, the existing governed L3 production validation path is explicitly single-user-only. Because this owner is the standard certification and execution path for governed L3 production validation, Stage 1+ cannot be safely implemented or certified without first changing that contract.

## Strengthened Precondition

Before implementation, prove whether existing Runtime Apply, Verification, Rollback, Approved Plan Lock, Restore Barrier, Learning, and OMP already support multi-selected-move execution.

If any owner is not batch-safe, stop with `REMAINING_BATCH_BLOCKER` and identify the first incompatible owner/function/field.

Do not patch around it.

## Contract Reuse Findings

| Owner | Batch Status | Evidence |
|---|---:|---|
| Authority budget | COMPATIBLE | `AUTHORITY_CLASS_BUDGETS` defines `CANARY=1`, `SMALL_BATCH=2`, `MEDIUM_BATCH=5`, `LARGE_BATCH=10`, `POOL=25`; authority promotion rules are evidence-based. |
| Planner selection | COMPATIBLE | Existing tests prove selected moves can be capped by authority budget and more than one move can be selected. |
| Packet | COMPATIBLE | `packet_from_plan()` preserves multiple selected moves and rollback manifest items. |
| Approved Plan Lock | COMPATIBLE | Approved plan lock stores `selected_moves` list and selected move hash/count. |
| Restore Barrier | COMPATIBLE | Restore barrier records `clearance_selected_moves_before_guard`, `clearance_max_selected_moves`, and selected move hash for multi-move plans. |
| Runtime Apply | PARTIALLY_COMPATIBLE | `AutoswitchPlanner.apply()` iterates over every selected move and records per-user result. |
| Verification | PARTIALLY_COMPATIBLE | Route verification runs after each successful switch; service verification runs per emergency move. |
| Rollback | COMPATIBLE | Operation-scoped rollback packet supports multiple users with a budget. |
| Learning / feedback | PARTIALLY_INCOMPATIBLE | Governed transaction feedback materialization is single-user-shaped. |
| Governed L3 production validation executor | INCOMPATIBLE | Explicitly rejects `max_users != 1` and requires exactly one selected move/user/target. |

## First Incompatible Contract

First incompatible owner:

- `tools/v7-governed-canary-dry-run-cycle`

First incompatible function:

- `execute_l3_production_validation()`

Exact field / condition:

- `args.max_users`
- hard condition: `if int(args.max_users) != 1`
- stop reason: `l3_production_validation_max_users_must_be_one`

Related incompatible functions:

- `l3_packet_constraints_ok()`
- `run_autoswitch_apply()`
- `materialize_governed_transaction_feedback()`

## Exact Incompatibilities

### `execute_l3_production_validation()`

The function rejects any production validation request where `max_users != 1`.

This blocks:

- Stage 1 small batch;
- Stage 2 medium batch;
- Stage 3 large batch;
- Stage 4 remaining users.

### `l3_packet_constraints_ok()`

The function rejects:

- `max_users != 1`;
- `selected_move_count != 1`;
- `len(users) != 1`;
- `len(targets) != 1`;
- `len(moves) != 1`.

This means that even if Planner and Packet produce a valid multi-selected-move contract, the governed L3 production validation transition stops before Runtime Apply.

### `run_autoswitch_apply()`

The wrapper invokes `v7-users-autoswitch` with:

- `--max-selected-moves 1`;
- `--user <single-user>`;
- `--source-egress <single-source>`;
- `--target-egress <single-target>`.

This constrains the Runtime consumer to one committed selected move even though the underlying Runtime Apply loop can process a selected move list.

### `materialize_governed_transaction_feedback()`

Feedback materialization is single-user-shaped:

- one `user`;
- one `source`;
- one `target`;
- one `user_outcome`;
- one `service_outcome`.

This is not sufficient for certified batch learning/OMP consumption without a batch-safe feedback shape or per-user materialization through the existing feedback owner.

## Existing Batch-Aware Evidence

Targeted tests run:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest \
  tests.unit.test_operator_execution_packet.OperatorExecutionPacketTest.test_packet_from_plan_prefers_final_selected_moves_over_decisions \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_apply_partial_success_is_classified_without_new_execution_path \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_operation_scoped_rollback_packet_executes_multiple_users_with_budget \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_l3_production_validation_blocks_two_users_and_source_recovered \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_authority_promotion_to_small_batch_uses_same_owner \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_authority_promotion_to_medium_batch_updates_only_authority_budget \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_authority_promotion_to_large_batch_requires_two_medium_runs_and_window \
  tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_routes_through_pipeline_before_apply
```

Result:

- `Ran 8 tests`
- `OK`

The tests prove:

- packet multi-selected-move support exists;
- Runtime Apply can classify partial success from multiple selected moves;
- rollback packet can execute multiple rollback users;
- Authority promotion exists and is evidence-based;
- L3 production validation still blocks two users through the current one-user envelope.

## Batch Object Model Status

Existing object model that can be reused:

- `selected_moves: list[dict]`
- `approved_plan_lock.selected_moves`
- `expected.selected_move_count`
- `expected.selected_move_hash`
- `constraints.allowed_users`
- `constraints.allowed_targets`
- `rollback_manifest.items`
- `apply_result.results`

No duplicate packet format is needed.

No duplicate restore barrier format is needed.

No duplicate Runtime API is needed for the underlying `v7-users-autoswitch` loop.

The missing piece is the governed L3 production validation executor contract, not the object schema itself.

## Promotion Rules Status

Existing Authority promotion model already implements evidence-based promotion:

- `CANARY -> SMALL_BATCH`
- `SMALL_BATCH -> MEDIUM_BATCH`
- `MEDIUM_BATCH -> LARGE_BATCH`
- `LARGE_BATCH -> POOL`

Promotion is based on successful operation ids, feedback closure, and stability windows for larger classes.

This should be reused rather than replaced.

## Demotion / Stop Status

Existing Runtime and Authority controls already stop or classify:

- verification failure;
- rollback success/failure;
- partial success;
- authority budget cap;
- restore barrier block;
- l3 retry budget exhaustion;
- incident/source mismatch.

No new safety rule should be invented.

## Production Impact

Production impact: NONE.

No code patch was applied.

No deployment was performed.

No production users were moved.

Production remains at the already certified governed one-user path.

## Required Future Correction Direction

Minimal future correction must target the existing governed L3 production validation owner:

- `tools/v7-governed-canary-dry-run-cycle`

The correction must make the owner batch-safe without creating a new execution path:

1. Replace hard one-user checks with stage-aware governed limits sourced from existing authority/capability/governance state.
2. Preserve the same `packet_from_plan()` / Approved Plan Lock / Restore Barrier path.
3. Invoke Runtime Apply with the committed approved selected move list rather than forcing a single `--user`.
4. Materialize feedback per moved user or as an existing-owner batch closure consumable by Learning/OMP.
5. Keep production default `max_users=1`.
6. Do not enable Stage 1+ until a separate certification explicitly proves the new batch-safe governed owner path.

## Future Certification Plan

Do not enable larger production batches automatically.

Future work should proceed in this order:

1. Patch only the governed L3 production validation owner to accept a configured stage budget.
2. Add tests proving `1 -> 5 -> 10` promotion gates without production enablement.
3. Add tests proving no promotion after verification failure / rollback / restore barrier block / authority block.
4. Add tests proving per-user feedback/learning/OMP closure for batch results.
5. Safe deploy.
6. Keep production at `max_users=1`.
7. Run a separate Stage 1 certification with explicit approval.

## Final Verdict

REMAINING_BATCH_BLOCKER

Exact owner:

- `tools/v7-governed-canary-dry-run-cycle`

Exact function:

- `execute_l3_production_validation()`

Exact field:

- `args.max_users`

Exact evidence:

- function returns `l3_production_validation_max_users_must_be_one` when `int(args.max_users) != 1`;
- `l3_packet_constraints_ok()` returns `l3_validation_max_users_not_one` and selected/user/target count errors for non-one-user scope;
- `run_autoswitch_apply()` forces `--max-selected-moves 1` and single `--user`;
- existing test `test_l3_production_validation_blocks_two_users_and_source_recovered` proves the current L3 validation envelope blocks two users.
