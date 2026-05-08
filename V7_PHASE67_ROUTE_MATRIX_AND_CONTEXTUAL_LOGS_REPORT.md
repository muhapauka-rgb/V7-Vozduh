# V7 Phase 67: Route Matrix And Contextual Logs

Date: 2026-05-08

## Goal

Make route capability and logs easier for an operator to understand:

- traffic types across the top;
- channels/routes down the side;
- each cell shows state and existing measured detail;
- logs are opened from the object they belong to.

## Implemented

Updated:

- `admin/v7-admin-api`

## Route Capability Matrix

The Service-aware Policy section now includes a route capability matrix.

Columns:

- Ordinary RU
- Gos/ESIA/FNS
- Banks
- VK/OK/social
- Marketplaces
- Video/YouTube
- Telegram/Stable
- Global Fast

Rows:

- active egresses from `egress.registry`
- `V7 direct RU`
- `Client direct`

Cells show:

- status: `OK`, `FAIL`, `RISK`, `DEPENDS`, `PARTIAL`, `UNKNOWN`,
  `NOT_TESTED`, etc.;
- measured speed when already available;
- service matrix first-byte/http details when already available;
- no automatic tests are launched just by opening the page.

## Contextual Logs

Added object-local log entry points:

- egress row: `Logs`
- route matrix row: `Logs`
- user row: `Logs`
- backup card: `Backup Manager`
- backup card: `Log / Disk Limits`

Logs and backup details open in a modal instead of being dumped into the main
page. This keeps operational information near the object it belongs to.

## Backup / Log Visibility

The backup card now shows:

- backup directory;
- backup count;
- total backup size;
- disk used percent;
- recent backups with size and SHA status.

`Log / Disk Limits` opens the current `v7-log-maintenance-status` output:

- journal disk usage;
- largest V7 log files;
- logrotate config presence;
- journald limit config presence.

## Safety

This phase is UI/read-only except existing buttons that already required
confirmation and RBAC. No cleanup/prune action was added yet.

## Next Step

Add controlled cleanup:

- cleanup preview first;
- prune old backups by retention policy;
- journal vacuum bounded by configured limit;
- logrotate dry-run/apply;
- audit each cleanup action.

## VPS Deployment

Previous admin binary was backed up on the VPS as:

```text
/usr/local/bin/v7-admin-api.bak.20260508-135327
```

Validation:

```text
syntax_ok
v7-admin-api active
127.0.0.1:7080 listening
admin login page responds
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
```

Current user route observed during validation:

```text
10.0.0.3 route_get uses tun0
```

Log maintenance status is bounded:

```text
journal usage: 204.4M
/etc/logrotate.d/v7 exists
SystemMaxUse=200M
RuntimeMaxUse=100M
MaxRetentionSec=14day
```
