# V7 Admin Phase 5 Auth Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase added authentication/session foundation to the local-only V7 Admin wrapper.

The admin service still binds only to:

```text
127.0.0.1:7080
```

No external admin exposure was enabled.

## Installed / Updated Files

```text
/usr/local/bin/v7-admin-api
/usr/local/bin/v7-admin-auth-init
/usr/local/bin/v7-admin-auth-status
```

Auth config:

```text
/etc/v7/admin/auth.json
```

Initial password file:

```text
/root/v7-admin-initial-password.txt
```

Permissions:

```text
/etc/v7/admin => 0700 root:root
/etc/v7/admin/auth.json => 0600 root:root
/root/v7-admin-initial-password.txt => 0600 root:root
```

The initial password was not printed to chat.

## Auth Model

Current model:

- username: `admin`
- password stored as PBKDF2-SHA256 hash
- session cookie: `v7_session`
- cookie flags: `HttpOnly`, `SameSite=Strict`, `Path=/`
- session TTL: 12 hours
- `/api/session` returns a CSRF token for future mutating POST actions

Open endpoint:

```text
GET /health
```

Protected endpoints:

```text
GET /
GET /api/overview
GET /api/state
GET /api/users
GET /api/egress
GET /api/diagnostics
GET /api/events
GET /api/backups
GET /api/session
```

Login/logout:

```text
GET /login
POST /login
POST /logout
```

## Validation

```text
systemctl is-active v7-admin-api => active
GET /health => OK, auth_configured=true
GET /api/overview without cookie => 401 unauthorized
POST /login with generated password => 303 session created
GET /api/session with cookie => user=admin and csrf token returned
GET /api/overview with cookie => valid JSON
ss -lntp => 127.0.0.1:7080 only
curl http://195.2.79.116:7080/health => connection refused
v7-system-check => V7_RESULT=OK
```

## How To Access From Mac

Create SSH tunnel:

```bash
ssh -L 7080:127.0.0.1:7080 root@195.2.79.116
```

Open:

```text
http://127.0.0.1:7080/
```

Initial password is stored on the VPS:

```text
/root/v7-admin-initial-password.txt
```

Do not paste this password into chats. Rotate it later from the admin/security workflow.

## Backup

Backup after Phase 5:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-191724.tar.gz
```

Verification:

```text
sha256=ok
files_count=288
```

## Next Recommended Phase

Phase 6:

- read-only UI polish
- add admin identity into audit events
- add password rotation command
- add safe POST action framework with CSRF verification
- then expose controlled actions:
  - create user
  - show/download config and QR
  - switch one user
  - run rebalance one move
  - set egress maintenance
  - create/verify backup
