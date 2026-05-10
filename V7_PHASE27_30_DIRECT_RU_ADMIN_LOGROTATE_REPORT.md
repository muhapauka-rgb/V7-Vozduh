# V7 Phase 27-30 Report: Direct/RU Routing, Admin Visibility, Logrotate Fix

Date: 2026-05-07
Server: 195.2.79.116

## What changed

- Fixed direct/RU routing priority:
  - direct fwmark rule now uses priority `50`;
  - user policy rules remain after it at priorities `98/99`;
  - marked RU/direct traffic can use table `70` via `ens3`.

- Fixed DNS for RU/direct routing:
  - dnsmasq now prefers Yandex DNS for `.ru` and `.xn--p1ai`;
  - `www.gosuslugi.ru`, `esia.gosuslugi.ru`, `lk.gosuslugi.ru`, `gu-st.ru`, and `ozon.ru` resolve through V7 DNS.

- Added direct diagnostics:
  - `/usr/local/bin/v7-direct-test-domain`
  - `/usr/local/bin/v7-direct-diagnose-domain`
  - `v7-safe-run` now allows `v7-direct-diagnose-domain` as read-only diagnostics.

- Added admin visibility:
  - dashboard metric `Direct RU`;
  - Direct/RU Routing panel;
  - quick direct route test for `www.gosuslugi.ru`;
  - full direct check button;
  - admin API endpoint `/api/direct-routing`.

- Added admin whitelist management:
  - add/remove direct domains from admin UI;
  - backend actions:
    - `/api/actions/direct-domain-add`
    - `/api/actions/direct-domain-remove`
  - actions require auth, CSRF, admin role, confirmation text;
  - blocked by Safe Mode.

- Hardened direct whitelist scripts:
  - `v7-direct-add-domain` validates domains/suffixes;
  - `v7-direct-remove-domain` validates domains/suffixes and handles missing entries safely;
  - `v7-direct-status` now displays pref `50`.

- Fixed `logrotate.service`:
  - moved duplicate backup config out of `/etc/logrotate.d`;
  - backup moved to `/root/v7-logrotate-backups`;
  - `logrotate -d /etc/logrotate.conf` passes;
  - `logrotate.service` runs successfully;
  - `logrotate.timer` is active.

## Current validation

- `v7-system-check`: `V7_RESULT=OK`
- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-admin-api`: active
- `v7-api`: active
- `v7-health`: active
- `v7-benchmark`: active
- `v7-killswitch`: active
- `dnsmasq`: active
- `logrotate.timer`: active
- latest backup: `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-013121.tar.gz`

## Direct/RU result

Direct route for `www.gosuslugi.ru`:

- DNS via V7: OK
- nft direct set: OK
- marked route: OK, table `70`, dev `ens3`
- final server HTTPS from VPS public IP: timeout

Interpretation:

- V7 direct routing is working.
- For main Gosuslugi endpoints, the remaining issue is reachability from the VPS public IP/path, not the V7 routing model.
- `gu-st.ru` and `ozon.ru` are reachable through the direct path.

## Backups made during this work

- `/root/v7-phase27-direct-routing-backup-20260507-010658`
- `/root/v7-phase28-admin-direct-backup-*`
- `/root/v7-phase29-direct-whitelist-admin-backup-*`
- `/root/v7-logrotate-backups/v7.bak.hardeningfix.20260506-183827`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-013121.tar.gz`

## Remaining global items

- Simplify admin UI into an operator-first view while keeping advanced sections available.
- Generalize remaining hardcoded `awg2/vless` assumptions toward registry-driven N-egress behavior.
- Add safer egress onboarding wizard later.
- Add future trusted Russian direct egress/IP option for Gosuslugi if provider/IP reachability remains blocked.
- Build installer later, after the current single-server operator workflow is stable.
