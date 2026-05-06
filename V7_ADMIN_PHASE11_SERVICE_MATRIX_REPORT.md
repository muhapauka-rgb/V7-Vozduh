# V7 Admin Phase 11: Service Matrix

Date: 2026-05-06

## Goal

Add service-specific egress tests because raw speed does not prove that YouTube, Telegram, Google, Apple, or other services actually work through a given VPN channel.

## Implemented

### New CLI

Added:

- `/usr/local/bin/v7-service-matrix-test`

Usage:

- `v7-service-matrix-test <egress_id> [service_id|all]`

State file:

- `/opt/v7/egress/state/service-matrix.json`

The test is manual and lightweight. It does not rebalance users, change routes, or modify assignments.

### Services In MVP Matrix

- YouTube
- Telegram
- WhatsApp
- Google
- Apple
- Cloudflare

Each test records:

- HTTP code;
- reachability;
- DNS/connect/TLS/first-byte timings;
- remote IP;
- reason/failure detail.

### Admin Integration

Admin overview now includes:

- `service_matrix`

Egress rows now show:

- service matrix status;
- `ok_count/total`;
- manual `Matrix` button;
- service matrix details in egress detail view.

Added admin action:

- `POST /api/actions/service-matrix-test`

### Safe Mode

`v7-safe-run` allowlist now includes:

- `v7-service-matrix-test`

## Validation Results

### awg2

Result:

- status: `WARN`
- ok: `5/6`

Services:

- YouTube: OK
- Google: OK
- Apple: OK
- Cloudflare: OK
- WhatsApp: OK
- Telegram: FAIL, timeout

### vless

Result:

- status: `OK`
- ok: `6/6`

Services:

- YouTube: OK
- Telegram: OK
- WhatsApp: OK
- Google: OK
- Apple: OK
- Cloudflare: OK

## Important Policy Note

Service matrix is visible in admin but is not yet used for automatic switching.

That is intentional. We should not move users automatically because one service-specific test failed until we define:

- per-user service needs;
- service priority;
- cooldown;
- minimum samples;
- failover policy;
- whether a failure is regional, temporary, or route-specific.

## Final Checks

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
- Users remained unchanged:
  - `10.0.0.2 current=awg2 table=100 enabled=1`
  - `10.0.0.3 current=awg2 table=101 enabled=1`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-210005.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-210005.tar.gz.sha256`

## Next Logical Step

Build service-aware recommendations:

- show "best egress for YouTube";
- show "best egress for Telegram";
- show mismatch warnings when a user is on an egress where a service they need is failing;
- keep actual switching manual until policy is explicit.
