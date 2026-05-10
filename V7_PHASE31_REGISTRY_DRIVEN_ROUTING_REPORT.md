# V7 Phase 31 Report: First Registry-Driven Routing Step

Date: 2026-05-07
Server: 195.2.79.116

## Goal

Reduce hardcoded `awg2/vless` assumptions without rewriting the orchestration core.

## Changed

- Added shared helper:
  - `/usr/local/lib/v7-egress-lib`

- Updated active scripts to read egress interface from `/opt/v7/egress/state/egress.registry`:
  - `/usr/local/bin/v7-routing-sync`
  - `/usr/local/bin/v7-user-switch`
  - `/usr/local/bin/v7-user-route-check`
  - `/usr/local/bin/v7-user-create`

## Important invariant fixed

During validation, `v7-routing-sync` initially recreated user rules with kernel auto-priorities `48/49`, which would have put user routing before direct/RU fwmark rule `50`.

Fixed immediately:

- user rule priority is now equal to user table:
  - `10.0.0.2 -> pref 100 table 100`
  - `10.0.0.3 -> pref 101 table 101`
- direct/RU rule remains:
  - `pref 50 fwmark 0x77 lookup 70`

Current order:

```text
0: local
50: fwmark 0x77 lookup 70
100: from 10.0.0.2 lookup 100
101: from 10.0.0.3 lookup 101
32766: main
32767: default
```

## Validation

- `v7-user-create registry-dry-run-test --egress awg2 --dry-run`: OK
- `v7-user-route-check`: OK
- `v7-routing-sync`: OK
- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-direct-test-domain www.gosuslugi.ru 10.0.0.3`: `DIRECT_READY`
- `v7-system-check`: `V7_RESULT=OK`

## Backups

- `/root/v7-phase31-registry-driven-routing-backup-*`
- `/root/v7-phase31-routing-priority-fix-*`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-013956.tar.gz`

## Remaining N-egress work

- Generalize `v7-state-json` from `for id in vless awg2` to registry-driven egress ids.
- Generalize `v7-users-rebalance` and `v7-users-rebalance-dry-run` beyond a two-egress model.
- Generalize `v7-users-autoswitch` validation beyond `vless|awg2`.
- Generalize `v7-killswitch-enable` egress allow interfaces from registry.
- Keep decision/rebalance behavior conservative: max one planned rebalance move per run remains.
