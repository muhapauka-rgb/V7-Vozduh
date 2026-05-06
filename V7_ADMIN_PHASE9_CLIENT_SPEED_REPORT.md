# V7 Admin Phase 9: Client-Side Speed Measurement

Date: 2026-05-06

## Goal

Add the missing client-side measurement path so the admin dashboard can eventually show:

- phone speed through V7;
- phone speed when connected directly to the selected tunnel/egress;
- percent degradation caused by routing through V7.

## Implemented

### New VPN-only Client Service

Added:

- `/usr/local/bin/v7-client-speed-api`
- `/etc/systemd/system/v7-client-speed-api.service`

Service listens only on the WireGuard server address:

- `http://10.0.0.1:7090`

It is not exposed on the public VPS interface.

### Client Page

The page provides:

- V7 speed test: phone -> V7 -> assigned egress -> Internet;
- direct speed test: intended for phone connected directly to a selected tunnel;
- local pending queue: if direct test is made while V7 is disconnected, the browser stores the sample and syncs it after reconnecting to V7.

### Sample Storage

Client samples are stored in:

- `/opt/v7/egress/state/client-speed.json`

Accepted sample modes:

- `v7`
- `direct`

The API accepts samples only from registered enabled VPN users in:

- `/opt/v7/egress/state/users.registry`

This prevents the server itself or unknown clients from polluting speed history.

### Admin Integration

Admin overview now includes:

- `client_speed`
- `client_speed_summary`

Egress rows now show:

- server-side V7 speed;
- phone through V7 speed;
- phone direct speed;
- degradation percent.

## Measurement Model

This keeps the numbers honest:

- `server_v7_mbps`: VPS measuring through egress.
- `client_v7_mbps`: phone measuring while connected through V7.
- `client_direct_mbps`: phone measuring while connected directly to that selected tunnel/egress.
- `degradation_pct`: calculated only when both phone-side numbers exist.

The VPS still cannot measure direct phone-to-egress performance by itself.

## Validation

- `v7-client-speed-api` active.
- `v7-admin-api` active.
- Listener check:
  - admin: `127.0.0.1:7080`
  - client speed: `10.0.0.1:7090`
- `GET http://10.0.0.1:7090/health` returned OK.
- Test POST from server IP `10.0.0.1` was rejected:
  - `403 unregistered_client`
- Test server sample was removed from state.
- Admin overview shows:
  - `v7-client-speed-api=active`
  - no fake `client_speed_users`
  - `client_speed_summary.awg2` prepared for users `10.0.0.2` and `10.0.0.3`
- `v7-system-check` result:
  - `V7_RESULT=OK`
- `v7-killswitch-check` result:
  - `V7_KILLSWITCH_CHECK=OK`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-203908.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-203908.tar.gz.sha256`

## How To Use

From an iPhone connected to V7:

1. Open `http://10.0.0.1:7090`.
2. Tap `Run V7 Speed Test`.
3. For direct comparison:
   - keep the page open;
   - connect the phone directly to the selected tunnel/egress;
   - tap `Run Direct Test`;
   - reconnect to V7;
   - tap `Sync Saved Result` if it did not sync automatically.

Then the admin tunnel row will be able to show the phone-side speed difference.

## Next Logical Step

Add a small button/link in the user page and admin user details:

- open client speed page;
- show last client speed sample per user;
- show stale warning when no recent phone-side measurement exists.
