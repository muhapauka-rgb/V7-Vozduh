# BLOCK E9.1 - Post-Canary Monitoring And Stability Review

Mode: read-only / post-canary observation.

Live mutation: forbidden.

Canary: forbidden.

## Executive Verdict

```text
post_canary_monitoring_executed=true
delayed_side_effects_observed=false
unexpected_user_movement=false
candidate_10.7.0.15_still_vless=true
table_1013_back_to_tun0=true
users.registry_stable=true
egress.registry_stable=true
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_post_restore_behavior=normal
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
current_canary_status=SUCCESS_ROLLED_BACK_MONITORED_STABLE
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

## What Was Observed

E9.1 observed the runtime after the first one-user canary and rollback:

```text
E9 forward:  10.7.0.15 vless -> 1
E9 rollback: 10.7.0.15 1 -> vless
```

No mutation was executed in E9.1.

Evidence folder:

```text
docs/track7/control-plane/e9_1-evidence/
```

## Baseline Snapshot

Evidence:

```text
docs/track7/control-plane/e9_1-evidence/post-e9-baseline.txt
```

Baseline facts at `2026-05-25T14:57:32Z`:

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
10.7.0.15 current=vless table=1013 enabled=1
table_1013=default dev tun0 scope link
route_get=8.8.8.8 from 10.7.0.15 dev tun0 table 1013
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Switch-history tail still ended with the E9 manual forward and rollback entries. No later movement was visible.

## Monitoring Samples

Evidence:

```text
docs/track7/control-plane/e9_1-evidence/monitor-sample-A.txt
docs/track7/control-plane/e9_1-evidence/monitor-sample-B.txt
docs/track7/control-plane/e9_1-evidence/monitor-sample-C.txt
```

| Sample | Time UTC | Candidate | Table 1013 | Registry Hash | Checks | New Movement |
|---|---:|---|---|---|---|---|
| A | 14:58:10 | `vless` | `tun0` | stable | OK | no |
| B | 14:59:16 | `vless` | `tun0` | stable | OK | no |
| C | 15:00:20 | `vless` | `tun0` | stable | OK | no |

Stable hashes across all samples:

```text
users.registry=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

## Autoswitch Post-Restore Behavior

Evidence:

```text
docs/track7/control-plane/e9_1-evidence/autoswitch-post-restore-behavior.md
```

Verdict:

```text
autoswitch_post_restore_behavior=normal
did_planner_timer_fire_after_restore=true
did_apply_timer_fire_after_restore=true
new_autoswitch_failover_after_E9_rollback=false
unexpected_user_movement=false
10.7.0.15_remained_vless=true
target_1_received_users=false
autoswitch_history_explainable=true
```

The timers are active and firing normally after restore. They did not produce delayed user movement during the E9.1 observation window.

## Drift Analysis

Evidence:

```text
docs/track7/control-plane/e9_1-evidence/drift-analysis.md
```

Verdict:

```text
users.registry_stable=true
egress.registry_stable=true
candidate_assignment_stable=true
table_1013_stable=true
route_get_stable=true
switch_history_no_unexpected_movement=true
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
routing_drift_observed=false
kill_switch_still_OK=true
reconcile_still_OK=true
provisioning_still_OK=true
```

## Second Canary Readiness Opinion

This is not an approval packet. It is only an opinion.

```text
second_canary_readiness=CONDITIONAL
```

Why not `GO`:

- E9.1 did not hold autoswitch authority;
- no second candidate/target packet has been prepared;
- target health and candidate anti-flap state must be checked fresh immediately before any second canary;
- execution remains forbidden without a separate approval.

Recommended second-canary direction:

```text
A) another user on the same target 1
```

Reason:

- target `1` was live-proven for `10.7.0.15` mechanics;
- a second user on the same target isolates whether behavior generalizes across tables/users while keeping target variable stable;
- use rollback again after mechanics proof unless the next approval explicitly requires longer hold.

Avoid for the next target:

```text
awg0
awg3
Direct/RU/Trusted-RU-sensitive paths
any target below current quality floor
```

Recommended second-canary shape:

- choose a fresh enabled user currently on `vless`;
- avoid users with recent anti-flap penalty or noisy switch history;
- target `1` only if it remains healthy and not overloaded;
- repeat quiet hold;
- execute one user-switch only;
- observe 2-5 minutes;
- rollback after mechanics proof unless a separate longer-hold approval is given.

## Required Answers

```text
post_canary_monitoring_executed=true
delayed_side_effects_observed=false
unexpected_user_movement=false
candidate_10.7.0.15_still_vless=true
table_1013_back_to_tun0=true
users.registry_stable=true
egress.registry_stable=true
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_post_restore_behavior=normal
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
current_canary_status=SUCCESS_ROLLED_BACK_MONITORED_STABLE
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

## Exact Next Recommended Step

Prepare E9.2 as a separate second one-user canary approval packet.

It should not execute the canary. It should:

- select a fresh candidate from current runtime evidence;
- prefer another `vless -> 1` mechanics canary if target `1` remains healthy;
- prepare rollback;
- require the same planner/apply hold;
- keep `routing-sync` forbidden.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
