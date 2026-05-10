# V7 Admin Phase 24: Role-Based Access Control

Date: 2026-05-07 00:29 MSK

## Goal

Add a role foundation for V7 Admin without breaking the current single-admin setup.

Current `admin` remains fully compatible and is treated as `owner`.

## Installed On VPS

VPS: `195.2.79.116`

Updated file:

- `/usr/local/bin/v7-admin-api`

Backup before install:

- `/root/v7-phase24-admin-roles-backup-20260507-002627`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-002857.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-002857.tar.gz.sha256`

Backup files count:

- `340`

## Roles

Added roles:

- `viewer`
- `operator`
- `admin`
- `owner`

Role intent:

- `viewer`: read-only visibility, diagnostics, previews
- `operator`: operational actions such as tests, user switch, client speed request
- `admin`: user/egress/policy/backup management
- `owner`: credentials and rollback apply

## Backend Changes

### Session Role

Admin sessions now include:

- `user`
- `role`
- `access`

The existing single admin user is automatically assigned:

```text
admin -> owner
```

No auth migration was required.

### Overview

`/api/overview` now includes:

```json
access
```

The UI header shows:

```text
admin:owner
```

### Action Guards

Every mutation action now has a minimum role.

Examples:

- `user-switch`: `operator`
- `user-create`: `admin`
- `egress-set-state-apply`: `admin`
- `policy-update`: `admin`
- `rollback-apply`: `owner`
- `password-rotate`: `owner`

### Sensitive GET Guards

Added GET role guards:

- `/api/backup-download`: `owner`
- `/api/client-artifact`: `admin`

This prevents low-privilege roles from downloading backups or client configs later.

### CSRF/Session Cache

Added per-request session and CSRF caching so the new global role guard does not conflict with the existing endpoint-level CSRF checks.

## Smoke Test

RBAC matrix test:

```json
{
  "auth_user": "admin",
  "role": "owner",
  "owner_can_password_rotate": true,
  "viewer_can_overview": true,
  "viewer_cannot_switch": true,
  "operator_can_switch": true,
  "operator_cannot_user_create": true,
  "admin_can_egress_apply": true,
  "admin_cannot_password_rotate": true,
  "overview_role": "owner",
  "actions": 22
}
```

Live API test:

```json
{
  "role": "owner",
  "user": "admin",
  "safe_mode": false,
  "users": 2
}
```

Note: one JSON key containing `password-rotate` is redacted by the existing secret redaction filter because it contains the word `password`. The permission matrix itself works correctly.

## Validation

### Current Users

```text
ip=10.0.0.2 current=awg2 table=100 enabled=1
ip=10.0.0.3 current=awg2 table=101 enabled=1
```

No users were moved.

### Safe Mode

Safe Mode remains disabled:

```json
{
  "enabled": false
}
```

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

Phase 24 is complete.

V7 Admin now has a real RBAC foundation. The current admin continues to work as `owner`, and the backend is ready for future multi-user admin accounts with operator/viewer access.

