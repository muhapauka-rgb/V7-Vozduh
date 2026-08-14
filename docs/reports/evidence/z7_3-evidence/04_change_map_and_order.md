# Z7.3 Evidence 04 - Change Map and Implementation Order

## Change Map

| File | Function / Area | Reason | Change Class | Risk |
|---|---|---|---|---|
| `tools/v7-users-autoswitch` | new operation context helper | Create one operation id per runtime cycle using existing facts | LINEAGE EXTENSION | LOW/MEDIUM |
| `tools/v7-users-autoswitch` | `AutoswitchPlanner.__init__` | Initialize operation context after generation is available | LINEAGE EXTENSION | MEDIUM |
| `tools/v7-users-autoswitch` | `plan()` | Emit operation envelope, selected move hash, runtime snapshot hash, closure target | METADATA EXTENSION | MEDIUM |
| `tools/v7-users-autoswitch` | selected move rows in `plan()` | Add `operation_id`, selected move hash/index references | LINEAGE EXTENSION | LOW/MEDIUM |
| `tools/v7-users-autoswitch` | `apply(plan)` | Add operation refs and terminal state/reason to `apply_result` | LINEAGE EXTENSION | MEDIUM |
| `tools/v7-users-autoswitch` | audit helper | Emit terminal operation audit through existing `v7-audit-log` in apply/runtime mode | METADATA EXTENSION / BEHAVIOR CHANGE | MEDIUM |
| `tools/v7-users-autoswitch` | `main()` | Ensure printed JSON includes final terminal/audit refs | METADATA EXTENSION | LOW/MEDIUM |
| `tests/unit/test_v7_users_autoswitch_policy.py` | fixture tests | Assert operation envelope and lineage fields | TEST EXTENSION | LOW |
| `tools/runtime-support/v7-audit-log` | no function | Existing metadata is enough | NO CHANGE | LOW |
| `admin/v7-admin-api` | `autoswitch_apply_guarded` | Optional: include plan operation id in Admin wrapper audit/result | OPTIONAL METADATA EXTENSION | MEDIUM |
| `admin/v7-admin-api` | closure functions | Existing `runtime` closure object type is enough | NO CHANGE | LOW |
| `admin_core/operator_observability.py` | operator read model | Optional later: read runtime operation audit records | OPTIONAL FUTURE | LOW/MEDIUM |
| `admin_core/operator_execution.py` | no function | Existing governance operation id remains separate | NO CHANGE | LOW |

## Absolute Minimum Change Set

1. `tools/v7-users-autoswitch`
   - add operation context helper,
   - add operation envelope to plan JSON,
   - add selected move hash and runtime snapshot hash,
   - propagate operation id into selected moves and apply results,
   - derive terminal state/reason,
   - emit terminal audit metadata through existing `v7-audit-log` when in mutating runtime mode.

2. `tests/unit/test_v7_users_autoswitch_policy.py`
   - extend existing fixture tests to assert operation envelope and lineage.

No change required in:

- `v7-audit-log`,
- Admin closure model,
- systemd,
- operator execution governance.

## Recommended Change Set

Absolute minimum plus:

1. `admin/v7-admin-api`
   - `autoswitch_apply_guarded` returns and audits `operation_id` from plan if present.
   - `autoswitch_dry_run_state` returns `operation_id` from plan if present.

2. `tests/unit/test_operator_observability.py`
   - add a read-only test for runtime operation closure target if observability is extended.

## Future Optional Change Set

- Operator observability indexes runtime operation audit events from `v7-audit-log`.
- Admin UI exposes closure action prefilled with runtime operation id.
- Break-glass rollback wrapper requires operation id.
- Direct manual switch wrapper requires operation id.

## Must Be Deferred

- new operation store,
- new API namespace,
- new scheduler,
- new orchestrator,
- new audit sink,
- new closure store,
- generic rollback redesign,
- operator execution packet changes unless needed by later governance stage.

## Implementation Order

1. Add autoswitch operation context and id creation.
2. Add operation envelope to plan output.
3. Add selected move hash/runtime snapshot hash/restore barrier lineage fields.
4. Propagate operation id into selected move rows.
5. Add terminal state/reason mapping in `apply(plan)`.
6. Propagate operation id into apply, verification, and rollback result rows.
7. Add terminal audit call through existing `v7-audit-log`, constrained to mutating/runtime mode.
8. Add closure target metadata to operation output using existing `object_type=runtime`, `object_id=<operation_id>`.
9. Extend autoswitch unit tests.
10. Optional: pass operation id through Admin autoswitch wrapper audit/result.
11. Optional: extend operator observability for runtime audit event indexing.

