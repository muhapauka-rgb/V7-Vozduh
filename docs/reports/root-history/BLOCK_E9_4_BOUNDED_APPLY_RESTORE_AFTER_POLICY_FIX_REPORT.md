# BLOCK E9.4 — Bounded Apply Restore After Policy Fix Report

## Summary

E9.4 did not restore `v7-users-autoswitch.timer`.

The final planner-only gate immediately before restore showed non-zero selected moves:

```text
final_planner_selected_moves=3
selected_move=10.7.0.5:1->vless reason=current_egress_not_eligible
selected_move=10.0.0.2:1->vless reason=current_egress_not_eligible
selected_move=10.0.0.3:1->vless reason=current_egress_not_eligible
```

Because E9.4 allowed restore only when `selected_moves=0`, the block was correctly aborted before starting the apply timer.

## Pre-Restore State

```text
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-users-autoswitch.timer=inactive/held
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Apply Restore Decision

```text
apply_restore_executed=false
apply_restore_aborted=true
abort_stage=final_planner_only_gate
abort_reason=selected_moves_nonzero
final_planner_selected_moves=3
actual_movements_count=0
actual_moved_users=[]
broad_failover_observed=true
emergency_containment_performed=false
```

No emergency containment was required because apply restore was never executed.

## Post-Abort Safety

```text
v7-users-autoswitch.timer=inactive/held
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
```

Runtime checks after abort:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Verdict

```text
apply_restore_clean=false
autoswitch_recovery_bounded=false
current_canary_status=NO-GO_APPLY_RESTORE_ABORTED_AFTER_POLICY_FIX
execution_allowed_now=false
```

The policy fix reduced the prior service-signal broad failover class during E9.3.9, but a fresh E9.4 planner sample still selected three failover moves. Apply restore remains blocked until the selected movement reason is understood under the new policy or the operator explicitly approves that exact movement set.

## Exact Next Step

Run a read-only root-cause block for the post-policy selected moves:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
```

The analysis must determine why egress `1` is still `current_egress_not_eligible` under the deployed policy and whether the trigger is Telegram hard-block, route-class hard failure, persistent service failure, stale state, or another hard eligibility rule.

## Verification

Passed:

```text
tools/v7-run-tests
targeted autoswitch policy tests
tools/v7-control-plane-governance-check --pretty
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
py_compile admin/tools/governance/autoswitch
git diff --check
```

Known read-only governance warnings:

```text
runtime_manifest_not_supplied
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known production-only lineage gaps remain
```

## Final Mutation Statement

```text
Runtime mutation performed: NO — apply timer restore was aborted before execution
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
