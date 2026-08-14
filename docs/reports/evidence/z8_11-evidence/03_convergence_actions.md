# Z8.11 Convergence Actions

## Binary replacement

Replaced because stale:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-admin-api`

Not replaced because already matching:

- `/usr/local/bin/v7-audit-log`

## Runtime provenance

Created:

- `/opt/v7/deploy-manifest.json`
- `/opt/v7/runtime-linkage.json`
- `/opt/v7/ops/deploy-z8-11-Updatesystem-ff91005-20260602T144500MSK/release-manifest.json`
- `/opt/v7/releases/current`

## Store bootstrap

Created empty required stores:

- `/opt/v7/egress/state/closure-records.jsonl`: empty JSONL
- `/opt/v7/egress/state/execution-events.jsonl`: empty JSONL
- `/opt/v7/egress/state/execution-contracts.json`: `{}`

No selected moves, restore barrier, user state, route state or policy files were modified.

## Service action

`v7-admin-api.service` was restarted once to load the newly replaced admin API binary.

Autoswitch service and timer were not started. Starting the timer would trigger `v7-users-autoswitch --apply`, which is forbidden by Z8.11.

