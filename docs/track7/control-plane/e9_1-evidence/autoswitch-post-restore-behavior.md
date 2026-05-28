# Autoswitch Post-Restore Behavior

Observed after E9 rollback and timer restore.

## Timer Behavior

At baseline capture, both autoswitch authorities were active again:

```text
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
```

`systemctl list-timers` showed both timers with recent and next trigger times, so the timers did fire after restore.

## Process Behavior

The baseline snapshot caught `v7-users-autoswitch.service` transiently `activating`, which is expected after restoring the timer authority. Monitoring samples A/B/C did not catch persistent `v7-users-autoswitch`, `v7-user-switch`, or `v7-routing-sync` processes.

## Movement Behavior

Switch-history tail remained stable across baseline and samples A/B/C. The latest entries remained:

```text
2026-05-25T14:28:16Z 10.7.0.15 vless -> 1 reason=manual
2026-05-25T14:30:34Z 10.7.0.15 1 -> vless reason=manual
```

No later `autoswitch_failover` or manual movement appeared during the E9.1 observation window.

## Candidate Behavior

```text
10.7.0.15 remained current=vless
table 1013 remained default dev tun0
route_get remained dev tun0 table 1013
```

## Target `1` Behavior

The users registry hash stayed unchanged from the E9 rollback baseline across all samples. Since all enabled users were already on `vless` at baseline, target `1` did not receive users during the E9.1 observation window.

## Verdict

```text
autoswitch_post_restore_behavior=normal
delayed_autoswitch_movement_observed=false
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
```
