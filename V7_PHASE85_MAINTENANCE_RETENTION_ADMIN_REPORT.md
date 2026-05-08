# V7 Phase85 Maintenance Retention Admin Report

Date: 2026-05-08

## Goal

Make logs, journal usage, and backups a controlled process with visible limits in Admin.

## Changes

- Added admin-managed retention config:
  - `/etc/v7/maintenance.conf`
- Added retention settings to `Log / Disk Limits` modal:
  - backups to keep
  - minimum backup age in days
  - journal vacuum size
  - journal vacuum time
- Cleanup scripts now load the retention config before preview/apply.
- Admin API validates and writes retention settings atomically.
- Settings updates are audited and blocked by Safe Mode.

## Cleanup Logic

Backup deletion is intentionally conservative:

- archive rank must be greater than `V7_BACKUP_KEEP`
- and archive age must be at least `V7_BACKUP_KEEP_DAYS`

This means a large number of fresh backups will not be deleted just because the count is high.

## Live VPS Validation

Admin health:

```text
status=OK
local_only=true
auth_configured=true
```

Retention settings saved through authenticated Admin API with CSRF:

```text
V7_BACKUP_KEEP=10
V7_BACKUP_KEEP_DAYS=14
V7_JOURNAL_VACUUM_SIZE=200M
V7_JOURNAL_VACUUM_TIME=14d
```

Cleanup preview:

```text
backup_count=33
planned_delete_count=0
planned_delete_bytes=0
```

Reason: all current backup archives are newer than the configured age limit.

## Safety Notes

- No cleanup apply was run during this phase.
- Settings file is included in V7 backups because `/etc/v7` is archived.
- Cleanup apply still requires explicit `CLEANUP` confirmation.

