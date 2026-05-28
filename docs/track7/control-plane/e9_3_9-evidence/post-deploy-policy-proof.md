# E9.3.9 Post-Deploy Policy Proof

Timestamp basis:

```text
deploy_file_verification=2026-05-25T21:37:20Z
planner_timer_observation=2026-05-25T21:38:54Z
post_deploy_safety=2026-05-25T21:39:41Z
```

Runtime file:

```text
path=/usr/local/bin/v7-users-autoswitch
deployed_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
mode_owner=755 root root
size=83266
backup_path=/usr/local/bin/v7-users-autoswitch.backup.e9_3_9.20260525T213519Z
backup_hash=e2ebfa53fbbff09d3325f617ecffcf48003c0e710b949a4fd6c983a4bedf3590
```

Authority state after deploy:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
apply_timer_remained_held=true
```

Manual planner dry-run:

```text
manual_v7_users_autoswitch_run=false
reason=blocked_as_out_of_scope_by_escalation_reviewer_because_planner_may_write_advisory_state
```

Planner-only proof source:

```text
source=systemd planner timer/journal observation
apply_authority_enabled=false
autoswitch_apply_manual=false
latest_observed_selected_moves=[]
latest_observed_apply_result.applied=false
latest_observed_apply_result.reason=no_selected_moves
single_service_transient_broad_failover_observed=false
```

Safety proof:

```text
users.registry_hash_pre=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
users.registry_hash_post=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
egress.registry_hash_pre=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
egress.registry_hash_post=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
strict_process_guard_empty=true
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Verdict:

```text
runtime_policy_deployed=true
planner_only_behavior_changed_without_apply_authority=true
apply_restore_safe_now=false
apply_timer_should_remain_held=true
execution_allowed_now=false
```

Reasoning:

- The runtime policy file now matches the E9.3.8 repo-fixed hash.
- The apply timer stayed inactive for the whole post-deploy evidence window.
- The active planner timer produced `selected_moves=[]` and did not apply movement.
- Registry hashes remained unchanged.
- No manual autoswitch apply, user-switch, routing-sync, canary, route mutation, or kill switch mutation was performed.
