# Execution Summary

## Planner Candidate

- User: `10.0.0.2`
- Source egress: `awg3`
- Target egress: `vless`
- Action: `switch`
- Move type: `failover`
- Reason: `current_egress_not_eligible`
- Selected move hash: `ef70877188c72befad38d84bfdbb334923fa855bc096182c80e48cbc7382a9f8`

## Approval Packet

- Packet path: `/opt/v7/admin/operator-approval-execution-packet-20260605T0923Z.json`
- Approval id: `appr_620119835b058d481fafa37a`
- Allowed users: `10.0.0.2`
- Allowed target: `vless`
- Rollback target: `awg3`
- Selected move budget: `1`

## Runtime Action

Approval packet runtime action result:

- `execution_allowed_now=true`
- `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- `runtime_mutation_scope=restore_barrier_clearance_only`
- `users_moved=0`

## Governed Apply

Command scope:

- guarded mode;
- apply;
- verify;
- one user only;
- target egress pinned;
- selected move budget pinned to `1`;
- bounded pre-planner refresh explicitly allowed.

Result:

- `terminal_state=APPLIED`
- `terminal_reason=selected_moves_applied`
- `selected_move_count=1`
- `apply_result.applied=true`
- `operation_id=runtime_autoswitch_e33f678dabd7ad432b38f2a7`
- moved `10.0.0.2` from `awg3` to `vless`
- `verify_rc=0`

## Production Registry After Execution

`ip=10.0.0.2 current=vless table=100 enabled=1`

