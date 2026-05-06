# V7 Admin Phase 25: Admin Accounts

Date: 2026-05-07 00:46 MSK

## Goal

Add admin account management on top of the RBAC foundation from Phase 24.

The current single-admin setup remains compatible:

- existing `admin` still works
- existing `admin` is treated as `owner`
- no forced auth migration
- no real extra account was left on the VPS during testing

## Installed On VPS

VPS: `195.2.79.116`

Updated file:

- `/usr/local/bin/v7-admin-api`

Auth file used:

- `/etc/v7/admin/auth.json`

Backup before install:

- `/root/v7-phase25-admin-accounts-backup-20260507-004218`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-004607.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-004607.tar.gz.sha256`

Backup files count:

- `340`

## Backend Changes

### Multi-Account Auth Support

`v7-admin-api` now supports both:

- legacy single-admin auth format
- new `users` map inside `/etc/v7/admin/auth.json`

Legacy remains the fallback, so current access does not break.

### Account Operations

New owner-only endpoints:

- `GET /api/admin-accounts`
- `POST /api/actions/admin-account-create`
- `POST /api/actions/admin-account-update`
- `POST /api/actions/admin-account-disable`
- `POST /api/actions/admin-account-enable`
- `POST /api/actions/admin-account-reset`

### Confirmations

Typed confirmations:

- create: `CREATE_ADMIN`
- update role: `UPDATE_ADMIN`
- disable: `DISABLE_ADMIN`
- enable: `ENABLE_ADMIN`
- reset credential: `RESET_ADMIN`

### Safety Guard

The backend blocks changes that would leave the system without an enabled `owner`.

This protects against accidental lockout.

### Password Rotate Compatibility

The old `Rotate Password` button was originally written for the single-admin format.

It now remains compatible: after the legacy password rotation runs, the multi-account user record is synchronized with the rotated hash.

## UI Changes

Added Admin Accounts section:

- list accounts
- show role
- show enabled/disabled state
- create account
- change role
- reset credential
- disable account
- enable account

Generated credentials are returned only in the authenticated owner UI response and are not written into audit logs.

## Smoke Test

Smoke test was run against a temporary copy:

```text
/tmp/v7-admin-auth-phase25-smoke.json
```

Real `/etc/v7/admin/auth.json` was not mutated by the smoke test.

Result:

```json
{
  "create_ok": true,
  "created_role": "operator",
  "credential_once_present": true,
  "state_has_operator_test": true,
  "update_role": "viewer",
  "reset_credential_present": true,
  "disable_ok": true,
  "legacy_owner_disable_blocked": true
}
```

Live API check:

```json
{
  "role": "owner",
  "accounts": [
    {
      "username": "admin",
      "role": "owner",
      "enabled": true
    }
  ],
  "roles": [
    "admin",
    "operator",
    "owner",
    "viewer"
  ]
}
```

## Validation

### Current Admin Accounts

```json
{
  "accounts": [
    {
      "username": "admin",
      "role": "owner",
      "enabled": true
    }
  ]
}
```

### Current Users

```text
ip=10.0.0.2 current=awg2 table=100 enabled=1
ip=10.0.0.3 current=awg2 table=101 enabled=1
```

No VPN users were moved.

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

Phase 25 is complete.

V7 Admin now has practical owner-level admin account management. It is ready for creating viewer/operator/admin accounts without exposing infrastructure root access and without weakening the existing owner login.

