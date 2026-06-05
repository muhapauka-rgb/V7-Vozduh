# Duplication And Safety Audit

## Movement-capable paths

Canonical movement-capable runtime owner:

- `tools/v7-users-autoswitch`
- governed apply command: `tools/v7-users-autoswitch --apply --verify`
- governed rollback command: `tools/v7-users-autoswitch --rollback-packet --apply --verify`

Admin direct movement path:

- `POST /api/actions/user-switch` is preserved for compatibility but returns `409 governed_execution_pipeline_required`.
- It no longer calls `run_action(["v7-user-switch", ...])`.

Egress migration path:

- Delete/pause migration with assigned users returns `governed_execution_pipeline_required`.
- Empty-channel delete/pause behavior is not classified as user movement.

## Source scan

`rg -n "run_action\\(\\[\\\"v7-user-switch\\\"|\\[\\\"v7-user-switch\\\"" admin/v7-admin-api admin_core tools tests -g '!*.json'`

Remaining findings:

- `tools/v7-users-autoswitch`: canonical executor uses `v7-user-switch` internally.
- `tests/unit/test_v7_users_autoswitch_policy.py`: test stubs for canonical executor.

No admin direct movement invocation remains.

## Runtime safety

This program did not:

- deploy
- move users
- run autoswitch apply
- mutate routes
- mutate runtime
- create a new planner
- create a new rollback owner
- create a new governance owner
- create a new truth source

