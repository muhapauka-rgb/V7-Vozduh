# V7 Admin Phase 19 - Settings And Policy

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Move production policy values out of hardcoded scripts and into an audited config path managed from V7 Admin.

## Files Updated Locally

- `admin/v7-admin-api`
- `hardening/v7-policy-env`
- `hardening/v7-users-autoswitch`
- `hardening/v7-users-rebalance`
- `hardening/v7-users-rebalance-dry-run`
- `hardening/v7-egress-load`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-policy-env`
- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-users-rebalance`
- `/usr/local/bin/v7-users-rebalance-dry-run`
- `/usr/local/bin/v7-egress-load`

Restarted:

- `v7-admin-api`

No VPN interface, routing table, WireGuard, sing-box, AmneziaWG, health, benchmark, or kill switch service was restarted.

## Policy File

Policy is stored at:

- `/etc/v7/policy.json`

The admin writes it atomically and backs up the old file before replacement.

Current production defaults:

- `switch.cooldown_seconds=180`
- `switch.autoswitch_max_planned_per_run=1`
- `switch.autoswitch_max_failover_per_run=25`
- `quality.min_avg_mbps=15`
- `quality.min_floor_mbps=10`
- `quality.min_stability=0.45`
- `load.soft_limit=1`
- `load.hard_limit=2`
- `load.rebalance_max_moves_per_run=1`
- `intervals.health_seconds=30`
- `intervals.benchmark_seconds=300`

## Admin API Added

- `GET /api/policy`
- `POST /api/actions/policy-update`

Policy updates:

- require auth and CSRF;
- validate and clamp values;
- enforce cooldown minimum `180`;
- enforce `hard_limit >= soft_limit`;
- write structured audit event `admin_action_policy_update`;
- return the active policy and backup path.

## Admin UI Added

New `Settings / Policy` section with controls for:

- cooldown seconds;
- planned autoswitch per run;
- failover autoswitch per run;
- quality thresholds;
- load soft/hard limits;
- rebalance max moves;
- stored health/benchmark intervals.

Note: health/benchmark intervals are now stored in policy, but applying them to systemd loop units remains a separate safe step.

## Runtime Integration

New script:

- `v7-policy-env`

It emits shell exports consumed by:

- `v7-users-autoswitch`
- `v7-users-rebalance`
- `v7-users-rebalance-dry-run`
- `v7-egress-load`

This means policy now affects:

- autoswitch cooldown;
- autoswitch planned/failover batch limits;
- rebalance quality threshold;
- rebalance max moves;
- egress load soft/hard status.

## Validation

Local validation:

- `python3 -m py_compile admin/v7-admin-api` - OK
- `bash -n v7-policy-env` - OK
- `bash -n v7-users-autoswitch` - OK
- `bash -n v7-users-rebalance` - OK
- `bash -n v7-users-rebalance-dry-run` - OK
- `bash -n v7-egress-load` - OK

VPS validation:

- `v7-admin-api` active - OK
- `GET /api/policy` - OK
- `POST /api/actions/policy-update` - OK
- clamp test: cooldown `60` became `180` - OK
- clamp test: hard limit lower than soft became equal to soft - OK
- restored production defaults - OK
- `v7-policy-env` reads `/etc/v7/policy.json` - OK
- `v7-egress-load` reads policy soft/hard limits - OK
- `v7-users-rebalance-dry-run` reads quality thresholds and max moves - OK
- `v7-users-autoswitch` reads cooldown - OK
- `v7-system-check` - OK
- `v7-killswitch-check` - OK

## Backups

Pre-install backup:

- `/root/v7-phase19-policy-backup-20260506-234851`

Load policy fix backup:

- `/root/v7-phase19-load-policy-fix-backup-20260506-235038`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-235112.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-235112.tar.gz.sha256`

## Notes

The policy layer is now ready for future controller/backend migration: the shell-core remains intact, but policy values are centralized and audited.

Next safe step is applying policy intervals to systemd loop units through a staged service-unit update with backup, daemon-reload, restart, and health verification.

