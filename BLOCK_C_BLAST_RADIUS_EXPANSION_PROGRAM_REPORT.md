# Block C Blast Radius Expansion Program Report

Project: V7 Vozduh

Block: C

Title: Blast Radius Expansion Program

Date: 2026-06-01

## Summary

Block C expanded the governed movement blast radius through the required ladder:

```text
2 -> 5 -> 10
```

The program started with two users already on the execution target from Block B, moved three additional users to certify the five-user stage, then moved five additional users to certify the ten-user stage.

Final target:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Final target count: `10`

## 1. Reality Audit

Initial state:

- `initial_target_count=2`
- `initial_rollback_count=8`
- `initial_selected_count=0`
- `initial_autoswitch_timer=inactive`
- `initial_audit_count=14`
- `initial_switch_history_count=2742`

Runtime checkers were OK. Admin API health at `127.0.0.1:8017` was unavailable with curl rc `7`.

## 2. Conflict Audit

Existing runtime movement implementation was reused:

- `v7-route-movement-preview`
- `v7-user-switch`
- `v7-user-route-check`
- `v7-killswitch-check`
- `v7-provisioning-reconcile-check`

No parallel batch system, runtime hook, autoswitch authority, rebalance, policy apply, deploy, or systemd change was introduced.

## 3. Truth Source Audit

Canonical movement truth source:

- `/opt/v7/egress/state/users.registry`

Canonical egress truth source:

- `/opt/v7/egress/state/egress.registry`

No conflict was found between packet scope, registry state, route tables, and checker outputs.

## 4. Runtime Audit

Initial hashes:

- `initial_users_hash=0c8a625da1e572f49247b87c95d1188a98f02fb079be01f0a7ef6ad599ed3d4d`
- `initial_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `initial_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `initial_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

Final hashes:

- `final_ten_users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `final_ten_outside_scope_hash=f06aedcc6e8459553f14c2e110409e36cb4bc50c60979968de9649b78c0647cb`
- `final_ten_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `final_ten_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `final_ten_routes_outside_scope_hash=0c7a2021bf63faff31ff6970fa72c2ad2ef776ca6a4c7f9510df81e01417b12a`
- `final_ten_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## 5. Five User Certification

Five-user stage scope:

- Existing target users: `10.7.0.11`, `10.7.0.12`
- New movement users: `10.7.0.3`, `10.7.0.4`, `10.7.0.5`

Packet:

- `packet_id=block-c-five-20260601T143754Z`
- `movement_budget=3`
- Stage total scope: `5`

## 6. Five User Execution

Executed:

```text
v7-user-switch 10.7.0.3 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.4 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.5 amneziawg-exec-20260528-10-8-1-14
```

Final Stage 5:

- `final_five_target_count=5`
- `final_five_rollback_count=5`
- `final_five_selected_count=0`
- `final_five_autoswitch_timer=inactive`

## 7. Five User Verification

Stage 5 passed:

- Scope respected
- Rollback ready
- Outside users unchanged
- Routing outside scope unchanged
- Runtime checkers OK

## 8. Ten User Certification

Ten-user stage scope:

- Stage 5 users
- New movement users: `10.7.0.2`, `10.7.0.6`, `10.7.0.8`, `10.7.0.14`, `10.7.0.15`

Packet:

- `packet_id=block-c-ten-20260601T144027Z`
- `movement_budget=5`
- Stage total scope: `10`

## 9. Ten User Execution

Executed:

```text
v7-user-switch 10.7.0.2 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.6 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.8 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.14 amneziawg-exec-20260528-10-8-1-14
v7-user-switch 10.7.0.15 amneziawg-exec-20260528-10-8-1-14
```

Final Stage 10:

- `final_ten_target_count=10`
- `final_ten_rollback_count=0`
- `final_ten_selected_count=0`
- `final_ten_autoswitch_timer=inactive`
- `final_ten_audit_count=16`
- `final_ten_switch_history_count=2750`

## 10. Ten User Verification

Stage 10 passed:

- Scope respected
- Rollback ready
- Outside users unchanged
- Routing outside scope unchanged
- Runtime checkers OK

## 11. Rollback Readiness

Rollback previews exist for all ten users. Rollback was not executed.

Rollback target:

- `1`

Rollback interface:

- `v7e356a192b79`

## 12. Replay Test

Stage 5:

- Valid packet: `ok`
- Duplicate packet: denied
- Expired packet: denied
- Invalid scope: denied

Stage 10:

- Valid packet: `ok`
- Duplicate packet: denied
- Expired packet: denied
- Invalid scope: denied

## 13. Fail Closed Review

Fail-closed conditions verified:

- Unknown
- Missing
- Stale
- Expired
- Invalid
- Mismatched
- Blocked

The first wrapper stopped after Stage 5 on a local verification key mismatch. Stage 10 only continued after a fresh readback confirmed Stage 5 was clean.

## 14. Certification

Certification result:

- `READY_WITH_BLOCKERS`

The blast-radius expansion itself is certified through the `2 -> 5 -> 10` ladder.

## 15. Remaining Risks

- Admin API health remained unavailable at `127.0.0.1:8017`.
- The execution target is at hard limit `10`, leaving no headroom.
- Ten users remain on execution target by design; rollback readiness exists but rollback was not executed.

## 16. Recommendation For BLOCK D

Before Block D expands beyond ten users, explicitly resolve or accept:

- Admin API health unavailability
- Capacity policy for execution target at hard limit
- Whether the ten-user execution cohort should remain on target or be rolled back before further expansion

## Required Verdicts

- `five_user_certified=true`
- `five_user_execution_successful=true`
- `ten_user_certified=true`
- `ten_user_execution_successful=true`
- `rollback_ready=true`
- `replay_protection_verified=true`
- `fail_closed_verified=true`
- `blast_radius_expansion_certified=true`
- `safe_to_continue_to_block_d=true`

## Safety Verdict

- `users_moved_count=8`
- `final_approved_scope_count=10`
- `users_moved_count<=10=true`
- `scope_expanded_only_as_authorized=true`
- `autoswitch_apply_run=false`
- `routing_changed_outside_scope=false`
- `deploy_performed=false`
- `systemd_changed=false`

