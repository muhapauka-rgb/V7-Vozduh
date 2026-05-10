# V7 Admin Phase 22: Egress Details

Date: 2026-05-07 00:13 MSK

## Goal

Improve the Admin egress table so each tunnel row can be expanded into a useful operational detail view:

- redacted config
- pool state
- assigned users
- server-side speed
- phone through V7 speed
- phone direct speed
- degradation percentage
- recent speed samples
- service matrix
- recent related events

This phase does not change routing, users, egresses, health logic, or kill switch rules.

## Installed On VPS

VPS: `195.2.79.116`

Updated file:

- `/usr/local/bin/v7-admin-api`

Backup before install:

- `/root/v7-phase22-egress-detail-backup-20260507-001033`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-001315.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-001315.tar.gz.sha256`

Backup files count:

- `338`

## Backend Changes

### New Detail Builder

Added `egress_detail(egress_id)` inside `v7-admin-api`.

It returns:

- `registry`
- `state`
- `pool_state`
- `assigned_users`
- `config`
- `server_speed`
- `client_speed`
- `service_matrix`
- `events`

### New API Endpoint

Added:

```http
GET /api/egress-detail?id=<egress_id>
```

The endpoint requires the existing Admin authentication.

### Secret Protection

Config output remains redacted.

Protected values include keys such as:

- `PrivateKey`
- `PresharedKey`
- `password`
- `token`
- `secret`
- `short_id`

Smoke-test confirmed redaction is active for `awg2`.

## UI Changes

The Egress table still shows one compact row per tunnel, but the `Details` button now expands into structured panels:

- `Pool`
- `Speed`
- `Health`
- `Assigned Users`
- `Client Speed Samples`
- `Recent Speed History`
- `Service Matrix`
- `Redacted Config`
- `Recent Egress Events`

The speed panel shows:

- server V7 speed
- phone through V7 speed
- phone direct speed
- degradation %
- freshness window

Current freshness window:

- `86400` seconds
- about 24 hours

That means manual phone/client speed samples remain visible in the admin for roughly the rest of the day.

## Validation

### Backend Smoke-Test

`awg2` detail:

- pool: `enabled`
- assigned users: `2`
- client-speed users: `1`
- service matrix total: `6`
- config redaction: `true`

`vless` detail:

- pool: `enabled`
- assigned users: `0`
- service matrix total: `6`

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

Phase 22 is complete.

The Admin egress rows now expand into a practical tunnel detail view. The view is useful for day-to-day operations and is safer for a larger system because secrets stay masked, speed samples are separated by source, and degradation is visible without constantly loading the VPN/server.

