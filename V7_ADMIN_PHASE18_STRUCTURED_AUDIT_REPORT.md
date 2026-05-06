# V7 Admin Phase 18 - Structured Audit Log

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Upgrade V7 audit logging from message-only JSONL to structured audit events while keeping compatibility with existing shell-core calls.

## Files Updated Locally

- `hardening/v7-audit-log`
- `admin/v7-admin-api`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-audit-log`
- `/usr/local/bin/v7-admin-api`

Restarted:

- `v7-admin-api`

No VPN, routing, health, benchmark, kill switch, WireGuard, sing-box, or AmneziaWG services were restarted.

## Structured Audit Fields

`v7-audit-log` now writes:

- `schema_version`
- `ts`
- `host`
- `actor`
- `severity`
- `action`
- `component`
- `message`
- `object_type`
- `object_id`
- `user_ip`
- `result`
- `request_id`
- `before_hash`
- `after_hash`
- `metadata`
- `pid`

Legacy calls still work:

```bash
v7-audit-log "user_disable" "users" "ip=10.0.0.2 table=100"
```

Structured calls are also supported:

```bash
v7-audit-log "user_switch" "users" "ip=10.0.0.3 from=awg2 to=vless" \
  severity=warning object_type=user object_id=10.0.0.3 result=OK request_id=req123
```

Environment overrides are supported:

- `V7_AUDIT_SEVERITY`
- `V7_AUDIT_OBJECT_TYPE`
- `V7_AUDIT_OBJECT_ID`
- `V7_AUDIT_RESULT`
- `V7_AUDIT_REQUEST_ID`
- `V7_AUDIT_BEFORE_HASH`
- `V7_AUDIT_AFTER_HASH`
- `V7_AUDIT_USER_IP`

## Admin API Changes

Admin-side audit events now pass structured fields through `audit_admin()`:

- `severity`
- `object_type`
- `object_id`
- `result`
- `request_id`

The `/api/events` timeline now exposes:

- `object_type`
- `object_id`
- `result`
- `request_id`

The Events table now includes `object` and `result` columns.

## Security

Redaction remains active for:

- private keys;
- preshared keys;
- passwords;
- tokens;
- secrets;
- access keys;
- sensitive metadata keys.

## Validation

Local validation:

- `bash -n hardening/v7-audit-log` - OK
- `python3 -m py_compile admin/v7-admin-api` - OK
- structured temp audit write - OK
- legacy temp audit write - OK

VPS validation:

- `v7-admin-api` active - OK
- legacy audit event gained structured fields - OK
- structured audit event preserved explicit fields - OK
- admin backup verify audit event recorded `object_type=backup` - OK
- `/api/events` exposes structured fields - OK
- HTML contains Events object/result markers - OK
- `v7-system-check` - OK
- `v7-killswitch-check` - OK

## Backups

Pre-install backup:

- `/root/v7-phase18-structured-audit-backup-20260506-234018`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-234106.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-234106.tar.gz.sha256`

## Notes

Existing old audit lines remain readable. New lines are schema-versioned so later controller/backend code can migrate them into SQLite/Postgres without guessing object identity from free-form messages.

