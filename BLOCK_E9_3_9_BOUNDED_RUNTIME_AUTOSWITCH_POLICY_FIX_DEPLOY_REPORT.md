# BLOCK E9.3.9 — Bounded Runtime Autoswitch Policy Fix Deploy Report

## Summary

E9.3.9 deployed the E9.3.8 autoswitch transient service signal policy fix to runtime as a single approved file update:

```text
runtime_path=/usr/local/bin/v7-users-autoswitch
repo_source=tools/v7-users-autoswitch
deployed_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
backup_path=/usr/local/bin/v7-users-autoswitch.backup.e9_3_9.20260525T213519Z
backup_hash=e2ebfa53fbbff09d3325f617ecffcf48003c0e710b949a4fd6c983a4bedf3590
```

No autoswitch apply authority was restored. `v7-users-autoswitch.timer` remained held/inactive.

## Deployment Scope

Changed runtime file:

```text
/usr/local/bin/v7-users-autoswitch
```

Unchanged runtime authorities:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
```

No systemd unit files were changed. No routes, ip rules, nftables, registry files, kill switch state, Direct/RU state, Trusted RU state, proxy runtime, or canary state were changed.

## Planner-Only Proof

A manual `v7-users-autoswitch` dry-run was not executed. The escalation reviewer blocked that as out of scope because planner execution may write advisory state. Instead, proof was taken from the already active non-apply planner timer/journal while apply authority remained held.

Observed post-deploy planner behavior:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=no_selected_moves
single_transient_service_signal_broad_failover_observed=false
```

This proves the deployed runtime planner did not reproduce the E9.3.5 broad failover class during the observed post-deploy planner-only window.

## Safety Results

```text
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
autoswitch_apply_manual=false
autoswitch_apply_timer_restored=false
canary_performed=false
```

Runtime checks after deploy:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Status

```text
runtime_policy_deployed=true
runtime_policy_deploy_success=true
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
apply_timer_remained_held=true
planner_only_behavior_changed_without_apply_authority=true
apply_restore_safe_after_runtime_deploy=false_until_separate_apply_restore_approval
current_canary_status=NO-GO_RUNTIME_POLICY_DEPLOYED_APPLY_RESTORE_PROOF_REQUIRED
execution_allowed_now=false
```

## Next Step

The next safe step is a separate approval packet for apply restore after a fresh planner-only sample under the deployed policy. Apply restore is still not authorized by this block.

## Verification

Passed:

```text
tools/v7-run-tests
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_autoswitch_policy_design
tools/v7-control-plane-governance-check --pretty
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff tools/v7-control-plane-governance-check tools/v7-route-movement-preview tools/v7-second-canary-target-readiness tools/v7-users-autoswitch
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
Runtime mutation performed: YES — limited to /usr/local/bin/v7-users-autoswitch policy file only
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
