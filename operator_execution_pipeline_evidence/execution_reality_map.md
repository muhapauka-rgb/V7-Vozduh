# Operator Execution Pipeline Reality Map

Program: `PROGRAM_OPERATOR_APPROVED_EXECUTION_PIPELINE_AND_GOVERNED_MOVEMENT_CERTIFICATION`

## Existing ownership

| Area | Existing owner | Verdict |
| --- | --- | --- |
| Planner | `tools/v7-users-autoswitch` | REUSE |
| Approval packet validation | `admin_core/operator_execution.py` / `tools/v7-operator-execution-packet` | EXTEND |
| Restore barrier clearance | `admin_core/operator_execution.py` | REUSE |
| Runtime apply | `tools/v7-users-autoswitch --apply --verify` | REUSE |
| Rollback packet | `admin_core/operator_execution.py` + `tools/v7-users-autoswitch --rollback-packet --apply --verify` | REUSE |
| Operator recommendation surface | `admin_core/operator_decision_surface.py` | EXTEND |
| Audit/closure | existing admin audit and operator lifecycle records | EXTEND |

## Bypass closure

Before this program, `POST /api/actions/user-switch` executed `v7-user-switch` directly from the admin API. Egress delete/pause migration helpers also contained direct `v7-user-switch` loops.

After this program:

- `POST /api/actions/user-switch` returns `409 governed_execution_pipeline_required`.
- Admin UI manual switch paths open a governed workflow drawer instead of posting direct movement.
- Egress delete/pause migration with assigned users returns `governed_execution_pipeline_required`.
- `admin/v7-admin-api` no longer contains direct `run_action(["v7-user-switch", ...])`.
- The remaining direct `v7-user-switch` invocation is inside `tools/v7-users-autoswitch`, which is the canonical runtime executor.

