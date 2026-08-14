# V7 Admin Phase 23: Admin Safe Mode

Date: 2026-05-07 00:18 MSK

## Goal

Add a switchable Admin Safe Mode.

Safe Mode is a backend-enforced read-only protection mode for the V7 Admin panel. When enabled, diagnostics and previews remain available, but dangerous mutation actions are blocked by the API.

## Installed On VPS

VPS: `195.2.79.116`

Updated file:

- `/usr/local/bin/v7-admin-api`

New state file:

- `/etc/v7/admin/safe-mode.json`

Backup before install:

- `/root/v7-phase23-admin-safe-mode-backup-20260507-001616`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-001745.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-001745.tar.gz.sha256`

Backup files count:

- `340`

## Backend Changes

### Safe Mode State

Safe Mode state is stored in:

```text
/etc/v7/admin/safe-mode.json
```

Current final state:

```json
{
  "schema_version": 1,
  "enabled": false,
  "updated_by": "codex-phase23-smoke",
  "reason": "smoke test complete"
}
```

The file is root-only:

```text
-rw------- root root /etc/v7/admin/safe-mode.json
```

### New API Action

Added:

```http
POST /api/actions/safe-mode-set
```

Confirmations:

- enable requires `SAFE_MODE`
- disable requires `DISABLE_SAFE_MODE`

### Overview

`/api/overview` now includes:

```json
admin_safe_mode
```

It contains:

- `enabled`
- `updated`
- `updated_by`
- `reason`
- `blocked_actions`

### Backend Enforcement

When Safe Mode is enabled, the API blocks mutation endpoints with HTTP `423`.

Blocked actions:

- `/api/actions/backup-create`
- `/api/actions/client-speed-request`
- `/api/actions/egress-set-state-apply`
- `/api/actions/egress-speedtest`
- `/api/actions/password-rotate`
- `/api/actions/policy-systemd-apply`
- `/api/actions/policy-update`
- `/api/actions/rollback-apply`
- `/api/actions/service-matrix-test`
- `/api/actions/service-preferences-update`
- `/api/actions/user-create`
- `/api/actions/user-disable`
- `/api/actions/user-enable`
- `/api/actions/user-reissue-config`
- `/api/actions/user-rotate-key`
- `/api/actions/user-switch`

Still allowed:

- read-only pages and API reads
- diagnostics
- backup verify
- restore preview
- rollback preview
- egress lifecycle preview
- policy systemd preview
- Safe Mode enable/disable

## UI Changes

The Admin header now shows:

- `Live Mode`
- or `Safe Mode ON`

There is a button to toggle the mode.

The toggle is protected by typed confirmation:

- `SAFE_MODE`
- `DISABLE_SAFE_MODE`

## Smoke Test

Safe Mode was enabled and then disabled.

Result:

```json
{
  "enabled_after_on": true,
  "blocked_count": 16,
  "user_switch_blocked": true,
  "egress_apply_blocked": true,
  "enabled_final": false
}
```

Safe Mode was intentionally left disabled after the test so normal admin operations continue to work.

## Validation

### Current Users

```text
ip=10.0.0.2 current=awg2 table=100 enabled=1
ip=10.0.0.3 current=awg2 table=101 enabled=1
```

No users were moved.

### Services

All checked services are active:

- `v7-api`
- `v7-health`
- `v7-benchmark`
- `v7-killswitch`
- `dnsmasq`
- `v7-admin-api`
- `v7-client-speed-api`

### Route Check

```text
V7_USER_ROUTE_CHECK=OK
```

### System Check

```text
V7_RESULT=OK
```

Direct egress checks:

- `vless_ip=77.110.103.131`
- `awg2_ip=94.241.139.241`

### Kill Switch

```text
V7_KILLSWITCH_CHECK=OK
```

## Result

Phase 23 is complete.

The admin panel now has a real Safe Mode. It is enforced on the server side, visible in the UI, protected by typed confirmation, and suitable for safer operator/assistant access workflows later.
