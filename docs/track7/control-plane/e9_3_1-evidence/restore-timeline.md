# E9.3.1 Restore Event Timeline

Mode: read-only reconstruction from E9.3 evidence and E9.3.1 read-only snapshot.

## Timeline

| Time UTC | Time MSK | Event | Evidence |
|---|---:|---|---|
| 2026-05-25 18:26-18:27 | 21:26-21:27 | E9.3 quiet-window canary completed forward and rollback for `10.7.0.14` | `post-switch.txt`, `rollback.txt` |
| 2026-05-25 18:28:28 | 21:28:28 | Restore sequence started planner/apply timers | `post-restore.txt` |
| 2026-05-25 18:28:28 | 21:28:28 | `v7-autoswitch-planner.timer` became active and immediately triggered `v7-autoswitch-planner.service` | `post-restore.txt` |
| 2026-05-25 18:28:28 | 21:28:28 | `v7-users-autoswitch.timer` became active and immediately triggered `v7-users-autoswitch.service` | `post-restore.txt` |
| 2026-05-25 18:28:28 | 21:28:28 | Running processes appeared: `python3 /usr/local/bin/v7-users-autoswitch` and `python3 /usr/local/bin/v7-users-autoswitch --apply` | `post-restore.txt` |
| 2026-05-25 18:28:28 | 21:28:28 | Immediate post-restore registry still showed `10.7.0.5 current=1 table=1003` | `post-restore.txt` |
| 2026-05-25 18:28:50 | 21:28:50 | Autoswitch safety state recorded `10.7.0.5` move with `move_type=failover` | `post-restore-drift-analysis.txt`, `read-only-runtime-snapshot.txt` |
| 2026-05-25 18:29:40 | 21:29:40 | Settle sample showed `10.7.0.5 current=vless table=1003` | `post-restore-settle.txt` |
| 2026-05-25 18:29:40 | 21:29:40 | Table `1003` default route was back to `tun0`; route_get used `tun0` | `post-restore-settle.txt` |
| 2026-05-25 18:30:42 | 21:30:42 | Drift analysis confirmed registry hash changed because `10.7.0.5` moved to `vless`; `10.7.0.14` remained rolled back on `vless` | `post-restore-drift-analysis.txt` |

## Causal Chain

1. E9.3 held both planner and apply authorities during the canary window.
2. E9.3 restored both timers together.
3. `v7-users-autoswitch.timer` uses `OnUnitActiveSec=20s` and `Unit=v7-users-autoswitch.service`.
4. `v7-users-autoswitch.service` executes `/usr/local/bin/v7-users-autoswitch --apply`.
5. The apply service ran immediately after timer restore.
6. The apply service selected a failover movement for `10.7.0.5`.
7. `v7-user-switch` was invoked by autoswitch apply, not manually.
8. Table `1003` and `users.registry` changed for `10.7.0.5` after the canary rollback was already complete.

## Timeline Verdict

The side effect occurred after the held canary window and during the restore phase. The restore phase therefore had independent mutation authority and must be governed as a separate operational stage.

