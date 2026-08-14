# Heartbeat Runtime Summary

Program: PROGRAM_HEARTBEAT_PRODUCTION_MATERIALIZATION_AND_OPERATOR_VISIBLE_CERTIFICATION
Date: 2026-06-04

## Planner Timer

Read-only production systemd inspection:

```text
v7-autoswitch-planner.timer
LoadState=loaded
ActiveState=active
SubState=waiting
UnitFileState=enabled
```

The timer was observed firing every ~30 seconds:

```text
Thu 2026-06-04 18:08:31 MSK ... v7-autoswitch-planner.timer -> v7-autoswitch-planner.service
```

## Planner Service

Read-only production systemd inspection:

```text
v7-autoswitch-planner.service
LoadState=loaded
ActiveState=inactive
SubState=dead
ExecMainStartTimestamp=Thu 2026-06-04 18:06:24 MSK
ExecMainExitTimestamp=Thu 2026-06-04 18:06:27 MSK
ExecMainStatus=0
ExecStart=/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
```

## Apply Service Safety

Read-only production systemd inspection:

```text
v7-users-autoswitch.service
ActiveState=inactive
SubState=dead
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

The movement-capable apply service was not executed during this program.

## Runtime Dry-Run Evidence

Safe production dry-run:

```text
/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=dry-run --pretty
```

Result:

```json
{
  "returncode": 0,
  "terminal_state": "DRY_RUN",
  "terminal_reason": "dry_run_intelligence_snapshot_stop_required",
  "selected_move_count": 0,
  "apply_result": {"applied": false, "reason": "dry_run"},
  "users_moved": false,
  "autoswitch_apply_run": false,
  "elapsed_sec": 2.778
}
```

## Verdict

runtime_heartbeat_active=true
snapshot_refresh_cadence_active=true
autoswitch_apply_run=false
users_moved=false

