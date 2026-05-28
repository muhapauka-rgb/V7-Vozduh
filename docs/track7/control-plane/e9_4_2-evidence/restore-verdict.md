# E9.4.2 Restore Verdict

Mode: bounded live apply-restore retry.

## Gate

Fresh final planner-only gate was accepted because the latest planner sample showed:

```text
selected_moves=[]
egress_1_eligible=true
telegram_hard_blocked=false
runtime_checkers=OK
```

Older journal entries in the same evidence file still contain the earlier Telegram hard-block sample. They were not the current gate decision.

## Restore

```text
systemctl start v7-users-autoswitch.timer
start_rc=0
manual_autoswitch_apply=false
manual_user_switch=false
manual_routing_sync=false
```

## Observation

Across immediate post-restore and samples A/B/C:

```text
users.registry_hash=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
egress.registry_hash=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
actual_movements_count=0
actual_moved_users=[]
broad_failover_observed=false
emergency_containment_performed=false
```

Observed timer-driven apply runs produced:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=no_selected_moves
```

Runtime checks remained OK:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Classification

```text
restore_verdict=CLEAN_RESTORE
autoswitch_recovery_bounded=true
apply_restore_clean=true
```

This proves that restoring `v7-users-autoswitch.timer` can be clean when the immediate planner-only gate is clean. It does not authorize canary execution or manual user movement.
