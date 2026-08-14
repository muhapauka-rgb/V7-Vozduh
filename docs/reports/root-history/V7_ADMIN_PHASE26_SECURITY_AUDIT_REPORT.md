# V7 Admin Phase 26: Security Audit

Date: 2026-05-07 00:51 MSK

## Goal

Add a dedicated Security Audit screen for V7 Admin.

This screen focuses on administrator/security events:

- admin login
- admin account changes
- RBAC denials
- Safe Mode blocks
- backup/rollback actions
- policy changes
- user and egress admin actions
- export for later review

No VPN routing, users, egresses, or kill switch rules were changed.

## Installed On VPS

VPS: `195.2.79.116`

Updated file:

- `/usr/local/bin/v7-admin-api`

Backup before install:

- `/root/v7-phase26-security-audit-backup-20260507-004942`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-005058.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-005058.tar.gz.sha256`

Backup files count:

- `340`

## Backend Changes

### New Security Audit API

Added owner-only endpoint:

```http
GET /api/security-audit
```

Supported filters:

- `actor`
- `action`
- `result`
- `severity`
- `object_type`
- `limit`

### New Export API

Added owner-only endpoint:

```http
GET /api/security-audit-export
```

Supported formats:

- `json`
- `csv`

Exports are returned as attachments.

### RBAC

New protected GET routes:

- `/api/security-audit`: `owner`
- `/api/security-audit-export`: `owner`

Reason: audit logs may contain sensitive operational details.

## UI Changes

Added `Security Audit` section to Admin UI.

It includes:

- filters by actor/action/result/severity/object type
- summary counters
- blocked/denied count
- actor list
- event table
- details button
- export JSON
- export CSV

## Smoke Test

Security audit endpoint:

```json
{
  "total": 20,
  "blocked": 0,
  "actors": [
    "admin",
    "root"
  ],
  "first": {
    "actor": "root",
    "action": "backup_create",
    "result": "OK",
    "severity": "info"
  }
}
```

JSON export:

```text
HTTP/1.0 200 OK
Content-Type: application/json; charset=utf-8
Content-Disposition: attachment; filename="v7-security-audit-YYYYMMDD-HHMMSS.json"
events=5
```

CSV export:

```text
HTTP/1.0 200 OK
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename="v7-security-audit-YYYYMMDD-HHMMSS.csv"
```

CSV header:

```csv
ts,severity,actor,action,object_type,object_id,result,request_id,message
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
  ],
  "security_total": 10
}
```

No admin accounts were changed.

### Current VPN Users

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

Phase 26 is complete.

V7 Admin now has a dedicated owner-only security audit screen with filtering, detailed event inspection, and JSON/CSV export. This is a necessary building block for safer delegated operations as the system grows.

