# V7 Admin Phase 12: Service-Aware Recommendations

Date: 2026-05-06

## Goal

Use service matrix data to produce admin recommendations without automatically moving users.

The system should answer:

- which egress is best for YouTube;
- which egress is best for Telegram;
- whether a user is currently on an egress where a service is failing;
- what manual action is available.

## Implemented

Admin overview now includes:

- `service_recommendations.best_by_service`
- `service_recommendations.user_warnings`

Admin UI now shows a `Recommendations` section with:

- best egress per service;
- candidate comparison;
- user warnings;
- manual `Switch` button for recommended egress.

No automatic switching was added.

## Current Recommendations

Based on the latest service matrix:

### Best Egress By Service

- YouTube: `awg2`
- Google: `awg2`
- Apple: `awg2`
- Cloudflare: `awg2`
- WhatsApp: `awg2`
- Telegram: `vless`

### User Warnings

Both current users are on `awg2`, while Telegram currently fails there and works through `vless`.

Warnings:

- `10.0.0.2`: Telegram FAIL on `awg2`, recommend `vless`
- `10.0.0.3`: Telegram FAIL on `awg2`, recommend `vless`

Current user routing was not changed:

- `10.0.0.2 current=awg2 table=100 enabled=1`
- `10.0.0.3 current=awg2 table=101 enabled=1`

## Safety

- Recommendations are read-only.
- Manual switch remains explicit.
- Autoswitch remains failover-only.
- Manual rebalance remains manual.
- Service matrix does not trigger automatic user movement.

## Validation

- `v7-admin-api` active.
- All V7 services active:
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

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-211639.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-211639.tar.gz.sha256`

## Next Logical Step

Add service preferences per user:

- user needs YouTube;
- user needs Telegram;
- user needs RU direct/TRUSTED_RU;
- user prefers stability over speed;
- user can be recommended a switch based only on services they care about.

This prevents the admin from seeing irrelevant warnings for users who do not need a specific service.
