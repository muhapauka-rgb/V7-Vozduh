# V7 Phase84 Backup Identity Restore Preview Report

Date: 2026-05-08

## Goal

Make backup/restore preview safer for the current V7 admin and Identity onboarding model.

The backup archive must explicitly show whether it contains:

- Identity database: `/opt/v7/admin/v7-identity.db`
- Admin auth config: `/etc/v7/admin/auth.json`
- Admin API executable: `/usr/local/bin/v7-admin-api`
- Profile delivery state: `/opt/v7/egress/state/profile-delivery-tokens.json`

## Changes

- `v7-backup-restore-preview` now prints explicit yes/no checks for core Identity/Admin files.
- Admin API now returns a structured `preview` object for backup restore preview actions.
- Restore preview remains read-only. It does not extract files and does not change the system.

## Live VPS Validation

Fresh backup created:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260508-173835.tar.gz
```

Restore preview result:

```text
OK: tar_readable=true
files_count=481
identity_db_included=yes
admin_auth_included=yes
admin_api_included=yes
profile_delivery_state_included=yes
SECRET_RISK=contains_vpn_configs_and_keys
MODE=preview_only
ACTION=none
NEXT_STEP=manual_restore_plan_required
```

Direct tar listing confirmed:

```text
/etc/v7/admin/auth.json
/opt/v7/admin/v7-identity.db
/usr/local/bin/v7-admin-api
```

## Safety Notes

- Archive contains VPN configs and keys. It must be treated as a secret.
- Restore remains a manual, preview-first operation.
- Old VPS files were backed up before deployment with `.bak.phase84.<timestamp>` suffixes.

