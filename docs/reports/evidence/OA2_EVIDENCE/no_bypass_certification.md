# OA.2 No-Bypass Certification

## Controller Scope

The controller is preview-only.

It models one operator decision:

- `APPROVE`
- `REJECT`

It does not execute either path.

## APPROVE Preview Chain

1. `fresh_planner` -> `tools/v7-users-autoswitch`
2. `packet` -> `tools/v7-operator-execution-packet`
3. `runtime_recheck` -> `admin_core/operator_execution.py`
4. `restore_barrier` -> `admin_core/operator_execution.py`
5. `apply` -> `tools/v7-users-autoswitch --apply --verify`
6. `verify` -> `tools/v7-users-autoswitch --apply --verify`
7. `rollback_readiness` -> `admin_core/operator_execution.py`
8. `feedback` -> `admin_core/operator_execution_feedback.py`
9. `closure` -> `admin_core/operator_execution_feedback.py`
10. `trust_refresh` -> `tools/v7-intelligence-snapshot-refresh`

## REJECT Preview Chain

1. `reject_closure` -> `admin_core/operator_execution_feedback.py`

## Forbidden Bypasses

| Bypass | Possible |
|---|---|
| planner bypass | false |
| governance bypass | false |
| packet bypass | false |
| restore barrier bypass | false |
| apply verification bypass | false |
| rollback bypass | false |
| feedback bypass | false |

## Runtime Safety

`APPROVE` and `REJECT` previews both return:

- `preview_only=true`
- `execution_allowed_now=false`
- `apply_executed=false`
- `users_moved=0`
- `autonomy_enabled=false`

