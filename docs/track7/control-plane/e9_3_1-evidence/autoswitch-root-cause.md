# E9.3.1 Autoswitch Root Cause

Mode: read-only source and evidence analysis.

## Observed Movement

```text
10.7.0.5: 1 -> vless
table 1003: v7e356a192b79 -> tun0
move_type=failover
manual_autoswitch_apply=false
manual_user_switch_for_10.7.0.5=false
```

## Direct Runtime Cause

The direct runtime cause was timer-driven autoswitch apply after authority restore:

```text
v7-users-autoswitch.timer
  -> v7-users-autoswitch.service
  -> /usr/local/bin/v7-users-autoswitch --apply
  -> v7-user-switch 10.7.0.5 vless
```

The timer/service unit model confirms this:

```text
v7-users-autoswitch.timer:
  OnUnitActiveSec=20s
  Unit=v7-users-autoswitch.service

v7-users-autoswitch.service:
  ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

## Decision Logic Cause

`tools/v7-users-autoswitch` classifies a user movement as `failover` when the current egress is missing or not eligible:

```text
if not current or not current.eligible:
    best_failover = next(eligible failover candidate)
    action = switch
    move_type = failover
    reason += current_egress_not_eligible
```

The same tool prioritizes failovers before reconnect, rebalance, and planned moves:

```text
selected.extend(failovers, autoswitch_max_failover_per_run)
selected.extend(reconnect, autoswitch_max_reconnect_per_run)
selected.extend(rebalance, rebalance_max_moves_per_run)
selected.extend(planned, autoswitch_max_planned_per_run)
```

Runtime policy allowed failovers:

```text
autoswitch_enabled=true
autoswitch_mode=guarded
autoswitch_max_failover_per_run=3
```

## Evidence for Failover Class

`autoswitch-safety.json` was updated at the restore time:

```text
updated=2026-05-25T18:28:50.345236+00:00
user_ip=10.7.0.5
move_type=failover
```

`client-reconnect-state.json` was updated at nearly the same time:

```text
updated=2026-05-25T18:28:50.346439+00:00
10.7.0.5 current_egress=vless
```

## Most Likely Root Cause

The best supported root cause is:

```text
restored apply timer fired immediately;
autoswitch observed 10.7.0.5 on current egress 1;
egress 1 was considered not eligible for that user at that moment;
guarded failover policy allowed a failover;
autoswitch selected vless and invoked v7-user-switch.
```

The exact low-level eligibility reason for egress `1` is not fully reconstructable from the saved grep-limited evidence, but the movement class and policy path are clear: it was an autoswitch failover, not a planned canary, not manual apply, and not routing-sync.

## Not Root Causes

- Not `v7-routing-sync`: no manual routing-sync was executed in E9.3.
- Not manual `v7-user-switch`: the only manual switch commands were for `10.7.0.14`.
- Not OpenVPN canary failure: E9.3 forward/rollback checks remained OK before restore.
- Not kill switch repair: kill switch remained OK and was not mutated.

## Root Cause Verdict

```text
autoswitch_root_cause=timer_restore_immediate_apply_failover
movement_reason_class=current_egress_not_eligible_failover
manual_apply=false
manual_switch_for_10.7.0.5=false
```

