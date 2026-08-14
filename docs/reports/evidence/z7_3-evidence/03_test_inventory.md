# Z7.3 Evidence 03 - Test Inventory

## Existing Relevant Tests

| Test File | Coverage Today | Reuse / Extension |
|---|---|---|
| `tests/unit/test_v7_users_autoswitch_policy.py` | Loads `tools/v7-users-autoswitch` as module, creates temp state fixtures, calls `AutoswitchPlanner.plan()`, asserts selected moves, restore barrier behavior, policy behavior | Primary extension target |
| `tests/unit/test_v7_autoswitch_policy_design.py` | Pure design fixture for autoswitch eligibility semantics | No change |
| `tests/unit/test_operator_execution_packet.py` | Packet validation, selected move hash mismatch, runtime snapshot hash, replay denial, governance audit `operation_id` | Reuse; optional extension only if packet interop changes |
| `tests/unit/test_operator_observability.py` | Operator view model, historical operation ids, audit export preview, governance/rehearsal preview, redaction | Optional extension after observability consumes runtime operation audit |
| `tests/contracts/test_endpoint_inventory.py` | Endpoint inventory contracts | No change unless endpoints change |
| `tests/contracts/endpoint_inventory_test.py` | Endpoint inventory helper | No change |

## Test Gaps

| Gap | Required Test Type |
|---|---|
| Autoswitch plan emits operation envelope | Extend `test_v7_users_autoswitch_policy.py` |
| Autoswitch no-op/dry-run still has `operation_id` | Extend `test_v7_users_autoswitch_policy.py` |
| Autoswitch selected move rows reference operation id | Extend `test_v7_users_autoswitch_policy.py` |
| Autoswitch restore-barrier denied operation has terminal state/reason | Extend existing restore-barrier tests |
| Autoswitch apply result rows reference operation id | Add mocked apply test, avoid real `v7-user-switch` |
| Autoswitch terminal audit call uses existing metadata | Add mocked subprocess test or helper-level test |
| `v7-audit-log` preserves operation metadata | Optional shell/CLI-style unit test if test harness supports it |
| Admin closure can close `runtime` object id | Optional Admin helper test if closure helpers are importable in stable way |

## Minimum Test Set

Absolute minimum:

1. `test_plan_contains_operation_envelope_for_noop`
2. `test_selected_moves_include_operation_lineage`
3. `test_restore_barrier_denial_has_operation_terminal_state`
4. `test_apply_result_includes_operation_lineage_with_mocked_switch`
5. `test_audit_metadata_call_is_built_without_changing_audit_schema`

Recommended:

6. `test_admin_autoswitch_apply_returns_operation_id_from_plan`
7. `test_runtime_closure_target_uses_existing_runtime_object_type`

Deferred:

- full operator observability rendering of runtime operations,
- closure workflow UI tests,
- endpoint contract changes.

