# V7 Admin Phase 10: Remote Client Speed Requests

Date: 2026-05-06

## Goal

Add the next production layer for phone-side measurements:

- show whether a client web-agent is online;
- show freshness of phone-side speed samples;
- allow admin to request a V7 speed test from a specific client;
- keep all remote execution limited to the client page that is already open inside V7.

## Implemented

### Client Agent Polling

`v7-client-speed-api` now exposes:

- `GET /api/agent/poll`

When a registered enabled VPN user opens `http://10.0.0.1:7090`, the page polls this endpoint every 5 seconds.

The server records heartbeat state in:

- `/opt/v7/egress/state/client-agents.json`

Admin overview now shows:

- online/offline client agent state;
- last seen age;
- online count.

### Remote Speed Command Queue

Admin API now supports:

- `POST /api/actions/client-speed-request`

It creates a command in:

- `/opt/v7/egress/state/client-commands.json`

Command shape:

- `type=speedtest`
- `mode=v7`
- `status=pending -> delivered -> completed`

When the client page is online, it receives the command, runs the speed test, sends the result back, and the command is marked completed.

### Freshness Model

Phone-side samples are now marked fresh/stale.

Current threshold:

- `86400` seconds, 24 hours.

Admin user rows now show:

- online/offline;
- latest phone V7 speed;
- fresh/stale/no sample;
- request speed button.

### Safety

- Unknown clients cannot poll as agents.
- Unknown clients cannot submit samples.
- Commands are tied to VPN source IP from `users.registry`.
- No private keys or configs are involved.
- No background iOS control is assumed. Safari/page must be open to receive a command.

## Validation

- `v7-admin-api` active.
- `v7-client-speed-api` active.
- Client speed service still listens only on:
  - `10.0.0.1:7090`
- Admin still listens only on:
  - `127.0.0.1:7080`
- Unregistered source `10.0.0.1` poll was rejected:
  - `403 unregistered_client`
- Admin created a remote speed command for:
  - `10.0.0.2`
  - status: `pending`
- Real phone-side samples were visible for:
  - `10.0.0.3`
- Current `awg2` client-side summary:
  - phone V7: `106.1 Mbps`
  - phone direct: `116.96 Mbps`
  - degradation: `9.3%`
- All services active:
  - `v7-api`
  - `v7-health`
  - `v7-benchmark`
  - `v7-killswitch`
  - `dnsmasq`
  - `v7-admin-api`
  - `v7-client-speed-api`
- `v7-system-check` result:
  - `V7_RESULT=OK`
- `v7-killswitch-check` result:
  - `V7_KILLSWITCH_CHECK=OK`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-205322.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-205322.tar.gz.sha256`

## Operational Note

Remote speed request works when the client page is online:

- iPhone connected to V7;
- `http://10.0.0.1:7090` open;
- page not suspended by iOS.

For true background execution later, V7 will need a native mobile app or MDM/managed profile.

## Next Logical Step

Build the service matrix layer:

- YouTube;
- Telegram;
- WhatsApp;
- Google;
- Apple;
- Cloudflare;
- RU/TRUSTED_RU checks later.

This is separate from speed because "fast" does not always mean "YouTube works".
