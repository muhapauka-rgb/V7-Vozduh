# V7 Admin Phase 8: User Lifecycle + Manual Egress Speed Probe

Date: 2026-05-06

## Goal

Continue the admin control plane after user creation:

- add controlled user lifecycle actions;
- make tunnel rows expandable with redacted config details;
- add a manual speedometer-style egress probe without creating continuous load;
- prepare the model for comparing client-direct speed vs V7-routed speed.

## Implemented

### Admin API

- Added `GET /api/egress-config?id=<egress>`.
- Added `GET /api/user-history?ip=<user_ip>`.
- Added `POST /api/actions/user-switch`.
- Added `POST /api/actions/user-disable`.
- Added `POST /api/actions/egress-speedtest`.

### Admin UI

- Egress/tunnel rows now have:
  - details button;
  - redacted config view;
  - manual speed test button;
  - V7 speed column;
  - direct phone speed column;
  - degradation/drop column.
- User rows now have:
  - history action;
  - manual switch action;
  - disable action.

### New CLI

- Added `/usr/local/bin/v7-egress-speedtest`.
- Script writes manual speed results to:
  - `/opt/v7/egress/state/egress-speed.json`
- It currently measures:
  - `server_v7_mbps`: speed from the V7 server through a selected egress.
- It preserves optional:
  - `client_direct_mbps`
  - `degradation_pct`

## Important Measurement Note

The VPS cannot honestly measure "phone connected directly to the external VPN without V7".

That value must come from a client-side measurement:

- iPhone/user page later;
- mobile app later;
- separate benchmark agent later;
- or a manual value submitted after a phone-side test.

So the model is:

- `server_v7_mbps`: measured by V7 now;
- `client_direct_mbps`: future client-side/direct measurement;
- `degradation_pct`: calculated only when both values exist.

This avoids fake precision and keeps the dashboard honest.

## Validation

- Admin API service remained active.
- Admin API still listens only on:
  - `127.0.0.1:7080`
- Config details endpoint returned redacted config.
- Private key pattern was not leaked in the config endpoint response.
- `user-disable` dry-run through admin API returned OK and did not modify users.
- User history endpoint returned OK.
- Manual speedtest for `awg2` returned:
  - `server_v7_mbps=56.24`
  - `http_code=200`
  - `ok=true`
- Final users stayed unchanged:
  - `10.0.0.2 current=awg2 table=100 enabled=1`
  - `10.0.0.3 current=awg2 table=101 enabled=1`
- Admin overview summary:
  - `users_total=2`
  - `users_registry_total=2`
  - `egress_total=2`
  - `egress_healthy=2`
  - `route_ok=2`
  - `route_leak_risk=false`
  - `killswitch_ok=true`
  - `stale_ok=true`
- `v7-system-check` result:
  - `V7_RESULT=OK`
- `v7-killswitch-check` result:
  - `V7_KILLSWITCH_CHECK=OK`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-201129.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-201129.tar.gz.sha256`

## Next Logical Step

Build the client-side measurement path:

1. Add a simple user page speed test while connected through V7.
2. Add a direct/off-V7 measurement input or agent.
3. Store per-device benchmark history.
4. Show degradation trend per egress and per user.
5. Keep all speed tests manual or rate-limited to avoid unnecessary load.
