# V7 Admin Phase 17 - Events And Audit Log

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Turn raw event JSON into a usable admin event timeline:

- normalized audit events;
- normalized user switch history;
- filters by source, severity, component, action, user IP, and limit;
- details view without exposing secrets;
- cleaner UI table instead of a raw JSON block.

## Files Updated Locally

- `admin/v7-admin-api`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-admin-api`

Restarted:

- `v7-admin-api`

No VPN, routing, health, benchmark, kill switch, WireGuard, sing-box, or AmneziaWG services were restarted.

## Admin API Updated

`GET /api/events` now supports:

- `source=all|audit|switch`
- `severity=error|warning|info`
- `component=<component>`
- `action=<action>`
- `user_ip=10.0.0.x`
- `limit=1..300`

Output is normalized to:

- `source`
- `ts`
- `severity`
- `host`
- `actor`
- `component`
- `action`
- `user_ip`
- `message`
- `details`

Invalid user IP filters are rejected with HTTP 400.

## Admin UI Updated

The `Events` section now has:

- source filter;
- severity filter;
- component filter;
- action filter;
- user IP filter;
- limit selector;
- event summary counters;
- event table;
- `Details` button that sends event details to the Actions panel.

## Validation

Local validation:

- `python3 -m py_compile admin/v7-admin-api` - OK

VPS validation:

- `v7-admin-api` active - OK
- `GET /api/events?limit=5` - OK
- `GET /api/events?source=audit&component=admin&limit=5` - OK
- `GET /api/events?source=switch&limit=5` - OK
- `GET /api/events?user_ip=10.0.0.3&limit=10` - OK
- `GET /api/events?user_ip=1.1.1.1` - HTTP 400
- HTML contains Events UI markers - OK
- `v7-system-check` - OK
- `v7-killswitch-check` - OK

## Backups

Pre-install backup:

- `/root/v7-phase17-events-admin-backup-20260506-233412`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-233500.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-233500.tar.gz.sha256`

## Notes

Severity is inferred for the current shell-core event format because existing audit events do not yet store a dedicated severity field. Later, `v7-audit-log` should accept structured fields such as:

- `severity`
- `request_id`
- `object_type`
- `object_id`
- `result`
- `before_hash`
- `after_hash`

