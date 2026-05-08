# V7 Phase 75 - Controlled Onboarding Test

Date: 2026-05-08

## Goal

Complete a controlled `/connect` onboarding test with one global connection password and no manual command copy-paste by the user.

## Changes

- `admin/v7-admin-api`
  - Added `V7_CONNECTION_PASSWORD_MIN_LENGTH`.
  - Default minimum is now `5`, so the requested shared connection password can be accepted.
- `admin/v7-admin-api.service`
  - Added `/root/v7-smart-clients` to `ReadWritePaths`.
  - Added `/opt/v7/admin` to explicit writable paths for Identity DB state.

## Server Actions

- Backed up the previous admin API binary and systemd unit before installing changes.
- Restarted only `v7-admin-api`.
- Set the global connection password to the requested current value.
- Created a controlled test group, organization, and allowed phone entry.

## Cleanup

The first failed `/connect` attempts created runtime WireGuard peers before smart profile delivery failed.

Cleaned with `v7-user-disable`:

- `10.0.0.4`
- `10.0.0.5`

Both users are now `enabled=0` in `users.registry`, and their WireGuard peers were removed from the live interface.

## Controlled Test Result

Successful `/connect` test created:

- device name: `u234567-iphone-dabe50`
- vpn IP: `10.0.0.6`
- route table: `104`
- client type: `karing`
- profile mode: `RU_LOCAL`

Delivery URL was generated, but token content was not printed.

## Verification

- `v7-admin-api`: active
- admin health: OK
- public gateway: active
- public `/connect`: HTTP 200
- public `/api/overview`: HTTP 404
- `10.0.0.6` route: `table 104 default dev tun0`
- `v7-system-check`: `V7_RESULT=OK`
- vless external IP: `77.110.103.131`
- awg2 external IP: `94.241.139.241`

## Next

Phase 76 should add production-friendly onboarding controls:

- allowed phone import/export;
- group and organization management polish;
- connection password settings UI;
- device limit visibility;
- clean revoke/disable flow from Identity UI.
