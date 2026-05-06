# V7 Admin Phase 4 Report

Date: 2026-05-06
Target: `195.2.79.116`
Status: completed

## Scope

This phase added the first read-only admin/backend wrapper over the existing shell-core.

No mutating admin actions were exposed.

The admin service binds only to localhost:

```text
127.0.0.1:7080
```

External access to `195.2.79.116:7080` is not open.

## Installed Files

```text
/usr/local/bin/v7-admin-api
/etc/systemd/system/v7-admin-api.service
```

Systemd service:

```text
v7-admin-api.service
```

## UI

Local UI:

```text
http://127.0.0.1:7080/
```

The first UI is intentionally read-only. It shows:

- system summary
- users
- egress pool
- route reality
- backups
- diagnostics
- audit/events tail

## API Endpoints

```text
GET /health
GET /api/overview
GET /api/state
GET /api/users
GET /api/egress
GET /api/diagnostics
GET /api/events
GET /api/backups
```

## Safety Model

The wrapper:

- uses Python stdlib only
- does not require extra packages
- calls only read-only/safe commands
- redacts common secret patterns
- does not expose private keys
- does not bind to public interface
- does not provide buttons for switching users, disabling egress, backup restore, or kill switch changes

Dangerous controls remain CLI-only until auth/session/CSRF/audit foundations are implemented.

## Validation

```text
systemctl is-active v7-admin-api => active
ss -lntp => 127.0.0.1:7080 only
curl http://127.0.0.1:7080/health => status OK
curl http://127.0.0.1:7080/api/overview => valid JSON
curl http://127.0.0.1:7080/api/diagnostics => diagnostics OK
curl http://127.0.0.1:7080/api/backups => latest backup verified
curl http://195.2.79.116:7080/health => connection refused
v7-system-check => V7_RESULT=OK
```

Overview summary at validation time:

```text
users_total=2
egress_total=2
egress_healthy=2
route_ok=2
route_leak_risk=false
killswitch_ok=true
stale_ok=true
```

## Backup

Backup after Phase 4:

```text
/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-190943.tar.gz
```

Verification:

```text
sha256=ok
files_count=284
```

## How To View Locally

Because the service is local-only, use an SSH tunnel from your Mac:

```bash
ssh -L 7080:127.0.0.1:7080 root@195.2.79.116
```

Then open:

```text
http://127.0.0.1:7080/
```

## Next Recommended Phase

Phase 5:

- add auth/session layer
- password setup
- CSRF protection before forms
- admin audit identity
- read-only UI polish
- then controlled actions behind auth:
  - add user
  - show QR
  - switch one user
  - run rebalance one move
  - set egress maintenance
  - create/verify backup
