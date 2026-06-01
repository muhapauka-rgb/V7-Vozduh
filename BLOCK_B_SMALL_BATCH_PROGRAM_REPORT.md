# Block B Small Batch Program Report

Project: V7 Vozduh

Block: B

Title: Small Batch Program

Date: 2026-06-01

## Summary

Block B completed a bounded two-user batch movement:

```text
10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14
10.7.0.12: 1 -> amneziawg-exec-20260528-10-8-1-14
```

No third user was moved. No autoswitch apply, rebalance, policy apply, deploy, systemd change, runtime hook, or scope expansion was performed.

## 1. Reality Audit

Reality audit source:

- `/tmp/block-b-small-batch-20260601T105928Z/reality_audit.env`

Before execution:

- Target count: `0`
- Source `1` count: `10`
- Selected moves: `0`
- Autoswitch timer: `inactive`
- Runtime checkers: OK
- Admin API health: unavailable, curl rc `7`

## 2. Conflict Audit

Existing runtime tools were reused:

- `v7-route-movement-preview`
- `v7-user-switch`
- `v7-user-route-check`
- `v7-killswitch-check`
- `v7-provisioning-reconcile-check`

No parallel batch execution system was created.

## 3. Truth Source Audit

Canonical movement truth source:

- `/opt/v7/egress/state/users.registry`

Canonical egress truth source:

- `/opt/v7/egress/state/egress.registry`

No truth source conflict was found.

## 4. Runtime Audit

Stable hashes:

- Outside users: `6234ab46ee2198db3b3319651942fef1f8838146f239d17535214c59a9373cf8`
- Egress registry: `09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- Selected moves: `7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- IP rules: `200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## 5. User Selection

Selected:

- `10.7.0.11`
- `10.7.0.12`

Both were enabled, observable, on rollback egress `1`, and had route tables with working defaults before execution.

## 6. Target Certification

Target:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Hard limit: `10`
- Count before: `0`
- Count after: `2`

Target was certified for the bounded two-user operator batch.

## 7. Packet

Packet:

- `packet_id=block-b-batch-20260601T105928Z`
- `movement_budget=2`
- Allowed users: `10.7.0.11`, `10.7.0.12`
- Allowed target: `amneziawg-exec-20260528-10-8-1-14`
- Rollback target: `1`

## 8. Approval

Approval:

- `approval_id=block-b-approval-20260601T105928Z`
- Dual approvals present
- TTL valid
- Scope valid

## 9. Runtime Recheck

Runtime recheck matched pre-execution hashes and state:

- Target count: `0`
- Source `1` count: `10`
- Selected moves: `0`
- Autoswitch timer: `inactive`
- Both selected users still on `1`

## 10. Execution

Executed:

```text
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.12 amneziawg-exec-20260528-10-8-1-14
```

Audit record:

- `event=block_b_small_batch_movement`
- `movement_count=2`
- `record_hash=bde80c46bb116076050cd28cb2aeba7e90da107037a5a045f9d7fe04299cb10c`

## 11. Observation

Final observation:

- Target count: `2`
- Source `1` count: `8`
- `10.7.0.11` route table `1009`: `default dev v7execwg0 scope link`
- `10.7.0.12` route table `1010`: `default dev v7execwg0 scope link`
- Switch history count: `2742`
- Operator audit count: `14`
- Autoswitch timer: `inactive`

Checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## 12. Rollback Readiness

Rollback was verified but not executed.

Rollback targets:

- `10.7.0.11 -> 1`
- `10.7.0.12 -> 1`

## 13. Replay Test

Replay test results:

- Valid packet: `ok`
- Duplicate packet: denied
- Expired packet: denied
- Invalid scope: denied

## 14. Fail Closed Review

Fail-closed states verified for unknown, missing, stale, expired, invalid, mismatched, and blocked packet conditions.

## 15. Certification

Certification result:

- `READY_WITH_BLOCKERS`

The two-user movement itself is certified. The remaining blocker is unavailable admin API health during the window.

## 16. Remaining Risks

- Admin API health was unavailable on `127.0.0.1:8017`.
- Block B left two users on the execution target by design; rollback is ready but was not executed.
- The batch layer is packet-governed over existing per-user commands, not a standalone durable batch executor.

## 17. Recommendation For BLOCK C

Proceed to Block C only with a fresh packet and no scope reuse from Block B. Before expanding beyond two users, explicitly remediate or accept the admin API health risk.

## Required Verdicts

- `users_selected=true`
- `target_certified=true`
- `packet_created=true`
- `approval_valid=true`
- `runtime_recheck_passed=true`
- `batch_executed=true`
- `observation_completed=true`
- `rollback_ready=true`
- `replay_protection_verified=true`
- `fail_closed_verified=true`
- `small_batch_certified=true`
- `safe_to_continue_to_block_c=true`

## Safety Verdict

- `users_moved_count=2`
- `users_moved_count<=2=true`
- `scope_expanded=false`
- `autoswitch_apply_run=false`
- `routing_changed_outside_scope=false`
- `deploy_performed=false`
- `systemd_changed=false`

