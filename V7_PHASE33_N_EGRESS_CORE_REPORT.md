# V7 Phase 33 Report: Registry-Driven N-Egress Core

Date: 2026-05-07
Server: 195.2.79.116

## Goal

Continue moving V7 away from hardcoded `vless/awg2` assumptions while preserving the current working orchestration model.

## Changed

Updated active scripts:

- `/usr/local/bin/v7-state-json`
- `/usr/local/bin/v7-decide-egress`
- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-users-rebalance`
- `/usr/local/bin/v7-users-rebalance-dry-run`
- `/usr/local/bin/v7-killswitch-enable`

## Details

- `v7-state-json` now builds the `egress` JSON object from `egress.registry`, not from a fixed `for id in vless awg2` loop.
- `v7-users-autoswitch` now validates the decision against `egress.registry`, not against a hardcoded two-egress list.
- `v7-users-rebalance` and `v7-users-rebalance-dry-run` now choose candidate egresses from enabled registry entries.
- Rebalance remains controlled:
  - max moves still comes from policy;
  - current default remains `1`;
  - dry-run remains read-only.
- `v7-killswitch-enable` now allows enabled egress interfaces from `egress.registry`.

## Regression caught and fixed

During validation, `v7-killswitch-enable` still contained a legacy cleanup line:

```text
ip rule del pref 100
```

That was safe before user rules used explicit priorities, but after Phase 31 `pref 100` belongs to user `10.0.0.2`.

Fixed:

- kill switch no longer deletes user rule priority `100`;
- it only removes/recreates the direct fwmark rule;
- user routing was restored with `v7-routing-sync`.

Current policy rule order:

```text
0: local
50: fwmark 0x77 lookup 70
100: from 10.0.0.2 lookup 100
101: from 10.0.0.3 lookup 101
32766: main
32767: default
```

## Validation

- `v7-state-json-save`: valid JSON
- `jq '.egress | keys'`: `awg2,vless`
- `jq '.users | length'`: `2`
- `v7-users-rebalance-dry-run`: suggests at most one move
- `v7-users-autoswitch`: sticky keep-current behavior preserved
- `v7-direct-test-domain yastatic.net 10.0.0.3`: `DIRECT_READY`
- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-user-route-check`: `V7_USER_ROUTE_CHECK=OK`
- `v7-system-check`: `V7_RESULT=OK`

## Backup

- `/root/v7-phase33-n-egress-core-backup-20260507-100423`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-100751.tar.gz`

## Remaining N-egress work

- Generalize benchmark/history/state merge writers where they still assume fixed egress keys.
- Generalize service matrix and admin action dropdowns to use registry ids.
- Add safer onboarding for a new egress as draft/quarantine until direct tests pass.
