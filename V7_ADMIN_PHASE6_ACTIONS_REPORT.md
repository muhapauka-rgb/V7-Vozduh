# V7 Admin Phase 6 Actions Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase added:

- password rotation command
- CSRF-protected admin POST action framework
- admin identity propagation into audit events
- first safe admin action: backup create
- autoswitch safety patch discovered during validation

The admin service still binds only to:

```text
127.0.0.1:7080
```

External admin access remains closed.

## Installed / Updated Files

```text
/usr/local/bin/v7-admin-api
/usr/local/bin/v7-admin-password-rotate
/etc/systemd/system/v7-admin-api.service
/usr/local/bin/v7-users-autoswitch
/usr/local/bin/v7-user-history
```

## Password Rotation

Command:

```bash
v7-admin-password-rotate
```

Current rotated password file:

```text
/etc/v7/admin/rotated-password.txt
```

Permissions:

```text
/etc/v7/admin/auth.json => 0600 root:root
/etc/v7/admin/rotated-password.txt => 0600 root:root
```

The old initial password file was removed to avoid confusion:

```text
/root/v7-admin-initial-password.txt => removed
```

Password rotation through admin API:

```text
POST /api/actions/password-rotate
```

Behavior:

- requires valid session
- requires CSRF token
- rotates password hash
- rotates session secret
- invalidates existing sessions
- writes new password to root-only file
- does not print the password in the API response

Validation:

```text
password rotate action => HTTP 200
old session after rotation => 401
login with new password from /etc/v7/admin/rotated-password.txt => 303
authenticated /api/overview => valid JSON
```

## CSRF Framework

`/api/session` returns:

```text
user
csrf
expires_at
```

Admin POST actions require:

```text
X-CSRF-Token: <csrf>
```

Validation:

```text
POST /api/actions/backup-create without CSRF => 403 csrf_failed
POST /api/actions/backup-create with CSRF => 200
```

## Backup Action

Endpoint:

```text
POST /api/actions/backup-create
```

This calls:

```bash
v7-backup-create
```

Audit actor is now propagated:

```text
actor=admin
action=admin_action_backup_create
action=backup_create
```

Validation backup created through admin API:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-193139.tar.gz
```

## Systemd Hardening Update

`v7-admin-api.service` keeps:

```text
ProtectHome=read-only
```

and allows only the minimal write paths needed for controlled admin actions:

```text
ReadWritePaths=/root/v7-backups /etc/v7/admin /opt/v7/audit
```

## Autoswitch Safety Patch

During Phase 6 validation, the health loop moved users from `awg2` to `vless` due autoswitch behavior. This was corrected immediately:

- users restored to `awg2`
- `v7-users-autoswitch` patched to be failover-only
- healthy current egress is never switched by autoswitch
- rebalance remains manual-only
- transient/missing current status is skipped
- failover now requires confirmed failure count
- switch history reason is now explicit

Current users:

```text
10.0.0.2 current=awg2 table=100
10.0.0.3 current=awg2 table=101
```

Validation:

```text
v7-users-autoswitch => ACTION=no_switch
v7-user-route-check => V7_USER_ROUTE_CHECK=OK
v7-system-check => V7_RESULT=OK
v7-killswitch-check => V7_KILLSWITCH_CHECK=OK
```

## Final Admin Overview

```text
users_total=2
egress_healthy=2
route_ok=2
route_leak_risk=false
killswitch_ok=true
stale_ok=true
```

## Final Backup

Backup after Phase 6:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-194123.tar.gz
```

Verification:

```text
sha256=ok
files_count=302
```

## Next Recommended Phase

Phase 7:

- UI polish for authenticated dashboard
- add user creation workflow behind CSRF:
  - create WireGuard user
  - show/download config
  - show QR
  - never expose private keys in logs/audit
- add controlled one-user switch action
- add manual rebalance one move action
- add egress maintenance action with guard
