# V7 Hardening Phase 3 Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase added user switch history, route reality checks, and egress protection commands.

It did not change current assignments:

```text
10.0.0.2 -> awg2
10.0.0.3 -> awg2
```

It did not disable or put any egress into maintenance.

## Installed Scripts

```text
/usr/local/bin/v7-switch-log
/usr/local/bin/v7-user-history
/usr/local/bin/v7-user-route-check
/usr/local/bin/v7-egress-guard
/usr/local/bin/v7-egress-set-state
```

## Updated Scripts

```text
/usr/local/bin/v7-user-switch
/usr/local/bin/v7-safe-run
/usr/local/bin/v7-system-check
```

Backups were created before replacement:

```text
/usr/local/bin/*.bak.phase3.20260506-190007
```

## Switch History

Switch events are now written to:

```text
/opt/v7/events/switch-history.jsonl
```

`v7-user-switch` now writes:

- audit log event
- switch-history event with user IP, previous egress, new egress, table, reason

Read history:

```bash
v7-user-history
v7-user-history 10.0.0.3
```

Current result:

```text
WARN: no switch history found
```

This is expected because no user was switched during Phase 3.

## Route Reality Check

Command:

```bash
v7-user-route-check
```

It checks:

- `users.registry`
- `user-<ip>.assign`
- expected interface from current egress
- routing table default route
- `ip route get 8.8.8.8 from <user_ip> iif wg0`
- direct leak to `ens3`

Validation:

```text
10.0.0.2 table 100 default dev awg2
10.0.0.3 table 101 default dev awg2
V7_USER_ROUTE_CHECK=OK
```

`v7-system-check` now includes this check.

## Egress Guard

Command:

```bash
v7-egress-guard <egress_id>
```

Validation:

```text
v7-egress-guard awg2 => BLOCK, users assigned:
  10.0.0.2 table=100
  10.0.0.3 table=101

v7-egress-guard vless => OK, no users assigned
```

## Egress State

Command:

```bash
v7-egress-set-state <egress_id> <enabled|disabled|maintenance> [--apply]
```

Default mode is dry-run.

Safety rules:

- cannot disable or put an egress into maintenance while active users are assigned
- writes timestamped backups before any `--apply`
- writes state into `/opt/v7/egress/state/egress-flags.state`
- updates `egress.registry enabled=0/1` so existing orchestration loops respect it

Validation:

```text
v7-egress-set-state awg2 maintenance => blocked, users assigned
v7-egress-set-state vless maintenance => dry-run only, no change
```

## Safe Mode

`v7-safe-run` now allows:

```text
v7-user-route-check
v7-user-history
v7-egress-guard
```

It still blocks mutating commands:

```text
v7-safe-run v7-egress-set-state vless maintenance => BLOCKED
```

## Backup

Created after Phase 3:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-190159.tar.gz
```

Verification:

```text
sha256=ok
files_count=281
```

## Final Validation

```text
v7-user-route-check => V7_USER_ROUTE_CHECK=OK
v7-system-check => V7_RESULT=OK
v7-killswitch-check => V7_KILLSWITCH_CHECK=OK
v7-backup-list => latest backup sha256=ok
```

## Next Recommended Phase

Phase 4 should start the admin/backend wrapper:

- read-only local API wrapper around current shell-core
- dashboard JSON endpoint
- users endpoint
- egress endpoint
- diagnostics endpoint
- no external admin exposure until auth exists
- auth/session/audit foundation before dangerous buttons
