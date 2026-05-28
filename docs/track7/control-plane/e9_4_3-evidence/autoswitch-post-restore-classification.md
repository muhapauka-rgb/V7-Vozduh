# E9.4.3 Autoswitch Post-Restore Classification

Mode: read-only post-restore observation.

## Evidence Files

- `post-restore-baseline.txt`
- `monitor-A.txt`
- `monitor-B.txt`
- `monitor-C.txt`

## Classification

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

## Observed Delayed Autoswitch Movement

E9.4.2 completed with `actual_movements_count=0`, but the E9.4.3 baseline and all three monitoring samples show the runtime state had changed after restore:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
```

The safety state records the movement at:

```text
2026-05-26T07:29:08.088818+00:00 user_ip=10.7.0.5
2026-05-26T07:29:08.088941+00:00 user_ip=10.0.0.2
2026-05-26T07:29:08.088994+00:00 user_ip=10.0.0.3
```

The `users.registry` hash changed from the E9.4.2 clean observation baseline:

```text
E9.4.2 observation-C users.registry=045ff68dcd22267b19c839531307a433776b71886ff4c8018a50783452b81222
E9.4.3 baseline/users.registry=03560a92e27aaa54e1237fce545c5d1d1296976f2615f654a19d7cf3f2c5b7e0
```

## Stability After Movement

Across E9.4.3 monitor samples A/B/C:

```text
users.registry_hash=03560a92e27aaa54e1237fce545c5d1d1296976f2615f654a19d7cf3f2c5b7e0
egress.registry_hash=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
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

Route tables match the post-movement registry state. No route drift was observed relative to the changed registry:

```text
table 100  -> tun0 for 10.0.0.2
table 101  -> tun0 for 10.0.0.3
table 1003 -> tun0 for 10.7.0.5
```

## Interpretation

The restore did not cause immediate movement in E9.4.2, but it did allow a later normal timer-driven autoswitch apply run to move three users. This is a post-restore side effect, not a manual mutation in E9.4.3.

The current timer behavior appears operationally normal after the delayed movement:

- `v7-health.service` remains active;
- `v7-autoswitch-planner.timer` remains active;
- `v7-users-autoswitch.timer` remains active;
- later planner/apply output shows `selected_moves=[]`;
- no hidden `v7-routing-sync` was observed;
- no manual `v7-user-switch` was observed.

Governance impact:

```text
restore_governance_live_proven=false
reason=delayed_autoswitch_movement_after_clean_restore
next_canary_readiness=NO-GO
```

Future canary planning must not rely on immediate post-restore samples alone. It needs a longer post-restore settle gate or a separate root-cause/guard model for delayed timer-driven autoswitch movement.
