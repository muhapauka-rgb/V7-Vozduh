# V7 Hardening Phase 1 Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase did not change user routing, egress assignment, failover logic, or rebalance behavior.

Implemented safe production-hardening foundations:

- audit log foundation
- backup creation command
- stale-state detection
- journal/log size limits
- logrotate config
- `v7-system-check` stale-state integration
- audit hooks for mutating user/direct/killswitch commands

## Installed Scripts

```text
/usr/local/bin/v7-audit-log
/usr/local/bin/v7-backup-create
/usr/local/bin/v7-state-stale-check
/usr/local/bin/v7-log-maintenance-status
```

## Updated Scripts

```text
/usr/local/bin/v7-system-check
/usr/local/bin/v7-user-create
/usr/local/bin/v7-user-disable
/usr/local/bin/v7-user-switch
/usr/local/bin/v7-users-rebalance
/usr/local/bin/v7-direct-add-domain
/usr/local/bin/v7-direct-remove-domain
/usr/local/bin/v7-killswitch-enable
/usr/local/bin/v7-killswitch-disable-temporary
```

Each updated file was backed up on the VPS with a timestamp suffix before replacement.

## Audit Log

Audit events are written to:

```text
/opt/v7/audit/audit.jsonl
```

Permissions:

```text
/opt/v7/audit: 0700
/opt/v7/audit/audit.jsonl: 0600
```

Current audited actions:

- hardening install/fix events
- backup creation
- user create
- user disable
- user switch
- user rebalance
- direct domain add/remove
- kill switch enable
- kill switch temporary disable

Secrets are not printed by the new audit helper, and message fields are defensively redacted for common secret names.

## Backup

Backup command:

```bash
v7-backup-create
```

Created backup:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-183730.tar.gz
```

The backup includes V7 scripts, systemd units, routing/config directories, protocol configs, and `/opt/v7` state/config files. It does not include huge logs by default.

## Stale State

Check command:

```bash
v7-state-stale-check 180
```

Thresholds:

```text
health pipeline files: 180 seconds
benchmark status file: 420 seconds
```

`v7-system-check` now includes this check and reports stale state as WARN/FAIL.

## Log Controls

Installed:

```text
/etc/logrotate.d/v7
/etc/systemd/journald.conf.d/v7-limits.conf
```

Journald limits:

```text
SystemMaxUse=200M
RuntimeMaxUse=100M
MaxRetentionSec=14day
```

Log status command:

```bash
v7-log-maintenance-status
```

## Validation

Latest validation:

```text
v7-state-stale-check 180 => V7_STALE_RESULT=OK
logrotate -d /etc/logrotate.d/v7 => rc=0
v7-killswitch-check => V7_KILLSWITCH_CHECK=OK
v7-system-check => V7_RESULT=OK
systemctl is-active v7-api v7-health v7-benchmark dnsmasq v7-killswitch => all active
```

## Next Recommended Phase

Hardening Phase 2:

- rollback-last-change command
- structured event history for route/user switch actions
- production cooldown audit and bump to 180 seconds where still lower
- safe-mode command wrapper
- stale-state display in admin MVP
- backup list/restore dry-run
