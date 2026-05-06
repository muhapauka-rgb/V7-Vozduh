# V7 Admin Phase 13: Optional Service Preferences

Date: 2026-05-06

## Goal

Make service-aware recommendations optional and user-scoped.

The admin should be able to:

- enable or disable recommendations globally;
- choose which services matter for each user;
- avoid noisy warnings for users who do not need a specific service.

## Implemented

### State

Added state file:

- `/opt/v7/egress/state/service-preferences.json`

Shape:

- `enabled`: global recommendations toggle;
- `users.<ip>.services`: important services for that user;
- `updated`;
- `updated_by`.

### Admin API

Added:

- `POST /api/actions/service-preferences-update`

It can:

- enable/disable recommendations;
- update important services for one user.

### Admin UI

Recommendations section now has:

- global enable/disable button;
- per-user checkboxes:
  - YouTube
  - Telegram
  - WhatsApp
  - Google
  - Apple
  - Cloudflare
- save button per user;
- warnings only when:
  - recommendations are enabled;
  - the service is selected for that user;
  - the current egress fails that service;
  - another tested egress works better.

## Validation

Initial behavior:

- recommendations disabled;
- warnings empty.

Then enabled recommendations and set:

- `10.0.0.2`: important service `telegram`

Result:

- warning appears only for `10.0.0.2`;
- no warning for `10.0.0.3`, because it has no selected service preferences.

Current warning:

- `10.0.0.2`
- service: Telegram
- current egress: `awg2`
- status: FAIL
- recommended egress: `vless`

No automatic switching was performed.

Current users remained unchanged:

- `10.0.0.2 current=awg2 table=100 enabled=1`
- `10.0.0.3 current=awg2 table=101 enabled=1`

## Safety

- This is advisory only.
- Autoswitch remains failover-only.
- Manual rebalance remains manual.
- Admin must explicitly press switch to move a user.

## Final Checks

- All V7 services active.
- `v7-system-check` result:
  - `V7_RESULT=OK`
- `v7-killswitch-check` result:
  - `V7_KILLSWITCH_CHECK=OK`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-225542.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-225542.tar.gz.sha256`

## Next Logical Step

Add a clearer user details view:

- preferences;
- speed freshness;
- service warnings;
- route reality;
- switch history;
- QR/config actions.

This will make the admin panel more useful as user count grows.
