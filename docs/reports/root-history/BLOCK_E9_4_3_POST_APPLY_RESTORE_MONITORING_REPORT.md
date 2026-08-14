# BLOCK E9.4.3 — Post-Apply-Restore Monitoring Report

Mode: read-only post-restore observation.

## Executive Verdict

```text
post_restore_monitoring_executed=true
delayed_side_effects_observed=true
unexpected_user_movement=true
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_timer_behavior=normal
selected_moves_status=delayed_timer_driven_failover_then_selected_moves_empty
restore_governance_live_proven=false
next_canary_readiness=NO-GO
execution_allowed_now=false
```

E9.4.2 proved a clean immediate apply restore, but E9.4.3 found a delayed timer-driven autoswitch side effect after that restore. This reopens restore governance as a blocker for any next canary.

## What Was Observed

E9.4.2 ended with:

```text
actual_movements_count=0
restore_verdict=CLEAN_RESTORE
```

The E9.4.3 baseline showed the runtime had changed after that clean observation:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
```

The autoswitch safety state records the three incoming `vless` moves at `2026-05-26T07:29:08Z`.

## Registry And Routing State

The `users.registry` hash changed from the E9.4.2 clean baseline:

```text
E9.4.2 observation-C: 045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
E9.4.3 baseline/A/B/C: 03560a92e27aaa54e1237fce545c5d1d1296976f2615f654a19d7cf3f2c5b7e0
```

The `egress.registry` hash remained stable:

```text
67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

The affected route tables now match the changed registry:

```text
10.0.0.2 table=100  current=vless default dev tun0
10.0.0.3 table=101  current=vless default dev tun0
10.7.0.5 table=1003 current=vless default dev tun0
```

Therefore this is user movement and route-table mutation by autoswitch authority after restore, not routing drift against the current registry.

## Runtime Checks

Across baseline and monitoring samples, the platform checks remained OK:

```text
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
```

Observed evidence:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Autoswitch Behavior

The apply/planner timers are active and behave like normal systemd authority:

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
```

Later planner/apply output in the E9.4.3 samples shows:

```text
selected_moves=[]
apply_result.applied=false
apply_result.reason=no_selected_moves
```

This means the delayed side effect already happened before E9.4.3 sampling, and the runtime then stabilized with no additional selected moves during A/B/C.

## Required Final Answers

```text
post_restore_monitoring_executed=true
delayed_side_effects_observed=true
unexpected_user_movement=true
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_timer_behavior=normal
selected_moves_status=delayed_timer_driven_failover_then_selected_moves_empty
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
restore_governance_live_proven=false
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## Next Recommendation

Do not return directly to second-canary planning. The safest next step is a read-only root-cause block for the delayed autoswitch movement after E9.4.2:

```text
recommended_next_step=classify_delayed_post_restore_autoswitch_movement_before_new_canary_approval
```

After that, the project can choose whether to:

- add a longer post-restore settle gate;
- require a zero-selected-moves window across multiple apply timer periods;
- add a suppression/approval window after restoring apply authority;
- or accept exact timer-driven movements as a separately bounded autoswitch recovery stage.

## Mutation Statement

```text
Runtime mutation performed by this block: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed by this block: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```

Important distinction: E9.4.3 observed timer-driven runtime movement that occurred after E9.4.2 restore. E9.4.3 itself performed only read-only monitoring.
