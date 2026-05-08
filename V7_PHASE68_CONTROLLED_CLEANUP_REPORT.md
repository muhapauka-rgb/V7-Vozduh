# V7 Phase 68: Controlled Cleanup

Date: 2026-05-08

## Goal

Make log/backup cleanup controlled, bounded, visible in admin, and impossible to
trigger accidentally.

## Implemented

Added:

- `hardening/v7-maintenance-cleanup-preview`
- `hardening/v7-maintenance-cleanup-apply`

Updated:

- `hardening/v7-safe-run`
- `admin/v7-admin-api`

## Cleanup Policy

Defaults:

```text
V7_BACKUP_KEEP=10
V7_BACKUP_KEEP_DAYS=14
V7_JOURNAL_VACUUM_SIZE=200M
V7_JOURNAL_VACUUM_TIME=14d
```

Backup pruning only deletes archives that are both:

```text
rank > V7_BACKUP_KEEP
age_days >= V7_BACKUP_KEEP_DAYS
```

This keeps recent backups even if there are many, and keeps enough history even
if older archives exist.

## Admin UI

`Backup Manager -> Log / Disk Limits` now has:

- `Cleanup Preview`
- `Apply Cleanup`

The preview shows:

- disk usage;
- journal current usage;
- planned journal vacuum command;
- logrotate availability;
- every backup with `KEEP` or `DELETE`;
- planned delete count and bytes.

The apply button requires typing:

```text
CLEANUP
```

The backend also requires the same confirmation before running the apply script.

## Safety

Cleanup does not delete:

- configs;
- secrets;
- state files;
- WireGuard client files;
- policy files.

It can only prune old `v7-backup-*.tar.gz` archives under `/root/v7-backups`,
plus matching `.sha256` files, then run bounded journal vacuum and V7 logrotate.

Apply is:

- admin-only;
- blocked by Admin Safe Mode;
- audited.

Preview is:

- viewer-safe;
- allowed through `v7-safe-run`;
- read-only.

## Validation

Local syntax:

```text
admin_syntax_ok
bash -n hardening/v7-maintenance-cleanup-preview OK
bash -n hardening/v7-maintenance-cleanup-apply OK
bash -n hardening/v7-safe-run OK
```

## VPS Deployment

Previous admin binary was backed up on the VPS as:

```text
/usr/local/bin/v7-admin-api.bak.20260508-140521
```

Installed:

```text
/usr/local/bin/v7-maintenance-cleanup-preview
/usr/local/bin/v7-maintenance-cleanup-apply
/usr/local/bin/v7-safe-run
/usr/local/bin/v7-admin-api
```

Validation:

```text
syntax_ok
v7-admin-api active
127.0.0.1:7080 listening
cleanup preview OK
planned_delete_count=0
planned_delete_bytes=0
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
```

Current retention kept all existing backups because they are only about one day
old even though there are more than ten archives. This is intentional: pruning
requires both rank and age conditions.
