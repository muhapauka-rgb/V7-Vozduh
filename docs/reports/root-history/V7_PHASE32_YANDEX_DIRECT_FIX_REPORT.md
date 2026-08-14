# V7 Phase 32 Report: Yandex/RU Direct Dependency Fix

Date: 2026-05-07
Server: 195.2.79.116

## Issue

Some RU services such as Yandex Weather reported that VPN was enabled, even though `.ru` direct routing was already configured.

## Root cause

The main `.ru` domains were routed directly, but Yandex pages also load required resources from non-`.ru` domains. One confirmed example:

- `yastatic.net`

Before the fix, `yastatic.net` was not in the direct nft set and therefore followed the user's default egress route through `vless/tun0`.

## Changed

Added Yandex dependency domains to `/etc/v7/direct/domains.conf`:

- `yandex.com`
- `yandex.net`
- `yastatic.net`
- `yandex.st`
- `yandexadexchange.net`
- `yandexcloud.net`

`dnsmasq` was restarted and recovered after a temporary systemd start-rate-limit caused by several rapid restarts during bulk additions.

## Validation

Services active:

- `dnsmasq`: active
- `v7-killswitch`: active
- `v7-api`: active
- `v7-health`: active
- `v7-benchmark`: active
- `v7-admin-api`: active

Direct checks:

- `yastatic.net`: `DIRECT_READY`
- `pogoda.yandex.ru`: `DIRECT_READY`
- `yandex.ru`: `DIRECT_READY`
- `ozon.ru`: `DIRECT_READY`

System checks:

- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-system-check`: `V7_RESULT=OK`

## Note

Users are currently assigned to `vless`, but direct-whitelisted traffic is still routed via table `70` and `ens3` when marked by DNS/nft. Non-whitelisted dependencies still follow the user's default egress and may trigger VPN detection. Add those domains to direct whitelist as they are discovered.
