# V7 Hardening Phase 2 Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase added operational safety tools and production cooldown behavior.

It did not change current user assignments:

```text
10.0.0.2 -> awg2
10.0.0.3 -> awg2
```

## Installed Scripts

```text
/usr/local/bin/v7-backup-list
/usr/local/bin/v7-backup-verify
/usr/local/bin/v7-rollback-last-change
/usr/local/bin/v7-safe-run
```

## Updated Scripts

```text
/usr/local/bin/v7-users-autoswitch
```

The previous version was backed up before replacement:

```text
/usr/local/bin/v7-users-autoswitch.bak.phase2.20260506-185007
```

## Backup List / Verify

Commands:

```bash
v7-backup-list
v7-backup-verify
```

Validation result:

```text
backup=v7-backup-v3119922.hosted-by-vdsina.ru-20260506-183730.tar.gz sha256=ok
tar_readable=true
files_count=258
```

## Rollback

Command:

```bash
v7-rollback-last-change
```

Default mode is dry-run only.

To apply a rollback:

```bash
v7-rollback-last-change --apply
```

This command restores the newest timestamped `*.bak.*` or `*.backup.*` file found in known V7 paths. Before applying, it creates a `*.pre-rollback.*` copy of the current target.

## Safe Mode

Command:

```bash
v7-safe-run <diagnostic-command>
```

Allowed commands are read-only diagnostics:

```text
v7-system-check
v7-state-stale-check
v7-killswitch-check
v7-killswitch-status
v7-direct-status
v7-direct-list
v7-direct-test-domain
v7-users-rebalance-dry-run
v7-log-maintenance-status
v7-backup-list
v7-backup-verify
v7-recent-performance
```

Validation:

```text
v7-safe-run v7-state-stale-check 180 => OK
v7-safe-run v7-user-switch 10.0.0.3 vless => BLOCKED
```

## Autoswitch Cooldown

`v7-users-autoswitch` now has production cooldown and batch controls:

```text
V7_SWITCH_COOLDOWN_SECONDS=180
V7_AUTOSWITCH_MAX_PLANNED_PER_RUN=1
V7_AUTOSWITCH_MAX_FAILOVER_PER_RUN=25
```

Behavior:

- if the user's current egress is healthy (`code=200`), planned switches respect the 180-second cooldown and only one planned switch per run
- if the current egress is down, failover can bypass cooldown but is still batched
- every actual autoswitch is written to audit log

Current validation:

```text
GLOBAL_DECISION=awg2
10.0.0.2 ACTION=no_switch
10.0.0.3 ACTION=no_switch
```

## Final Validation

```text
v7-backup-list => rc=0
v7-backup-verify => rc=0
v7-rollback-last-change => dry-run rc=0
v7-safe-run allowed diagnostic => rc=0
v7-safe-run blocked mutating command => rc=2
v7-users-autoswitch => rc=0, no_switch
v7-system-check => V7_RESULT=OK
v7-killswitch-check => V7_KILLSWITCH_CHECK=OK
```

## Next Recommended Phase

Hardening Phase 3:

- structured switch history per user
- egress maintenance/disabled state
- prevent egress removal while users are assigned
- route reality check per user
- admin MVP backend wrapper over current shell-core
