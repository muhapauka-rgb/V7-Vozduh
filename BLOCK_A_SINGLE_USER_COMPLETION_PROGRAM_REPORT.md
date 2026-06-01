# Block A Single User Completion Program Report

Project: V7 Vozduh

Block: A

Title: Single User Completion Program

Date: 2026-06-01

## Summary

Block A completed the lifecycle for exactly one approved user:

```text
10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14 -> 1
```

The rollback was executed with the existing runtime command:

```text
v7-user-switch 10.7.0.11 1
```

No second user, batch, autoswitch apply, rebalance, deploy, systemd change, runtime hook, or scope expansion was performed.

## Reports Created

- `BLOCK_A_REALITY_AUDIT.md`
- `BLOCK_A_IMPLEMENTATION_CONFLICT_AUDIT.md`
- `BLOCK_A_TRUTH_SOURCE_AUDIT.md`
- `BLOCK_A_RUNTIME_AUDIT.md`
- `BLOCK_A_POST_MOVE_OBSERVATION.md`
- `BLOCK_A_MOVE_CERTIFICATION.md`
- `BLOCK_A_ROLLBACK_PACKET.md`
- `BLOCK_A_ROLLBACK_APPROVAL.md`
- `BLOCK_A_ROLLBACK_RECHECK.md`
- `BLOCK_A_ROLLBACK_EXECUTION.md`
- `BLOCK_A_ROLLBACK_OBSERVATION.md`
- `BLOCK_A_ROLLBACK_CERTIFICATION.md`
- `BLOCK_A_SINGLE_USER_CERTIFICATION.md`

## Reality Audit

The runtime truth source is registry based:

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`

Pre-rollback state:

- `10.7.0.11` current egress: `amneziawg-exec-20260528-10-8-1-14`
- Execution egress user count: `1`
- Egress `1` user count: `9`
- Table `1009`: `default dev v7execwg0 scope link`
- Autoswitch timer: `inactive`

## Existing Implementation

Existing implementation was reused:

- Preview: `v7-route-movement-preview`
- Execution: `v7-user-switch`
- Verification: `v7-user-route-check`, `v7-killswitch-check`, `v7-provisioning-reconcile-check`

No parallel execution system was created.

## Rollback Packet

Packet:

- `packet_id=block-a-rollback-20260601T104148Z`
- `approval_id=block-a-approval-20260601T104148Z`
- `operation_id=BLOCK_A_SINGLE_USER_COMPLETION`
- Movement budget: `1`
- Allowed user: `10.7.0.11`
- Allowed target: `1`

## Execution

Execution output confirmed:

```text
[V7] user 10.7.0.11 -> 1 / table 1009 / dev v7e356a192b79
```

Post-rollback state:

- `10.7.0.11` current egress: `1`
- Execution egress user count: `0`
- Egress `1` user count: `10`
- Table `1009`: `default dev v7e356a192b79 scope link`

## Verification

Checker results:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Final delayed observation:

- Outside users unchanged: true
- Egress registry unchanged: true
- IP rules unchanged: true
- Routes outside table `1009` unchanged: true
- Selected move queue unchanged: true
- Autoswitch timer inactive: true

## Required Verdicts

- `move_certified=true`
- `rollback_packet_created=true`
- `rollback_approved=true`
- `rollback_recheck_passed=true`
- `rollback_executed=true`
- `rollback_observed=true`
- `rollback_certified=true`
- `single_user_movement_certified=true`
- `safe_to_continue_to_block_b=true`

## Safety

- `users_moved_count=1`
- `users_moved_count<=1=true`
- `scope_expanded=false`
- `autoswitch_apply_run=false`
- `routing_changed_outside_scope=false`
- `deploy_performed=false`
- `systemd_changed=false`
- `runtime_hooks_implemented=false`

## Recommendation For Block B

Block B is safe to start only as another explicit, bounded packet with a fresh reality audit and a newly approved scope. Do not reuse Block A approval for any additional user movement.

