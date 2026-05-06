# V7 Admin Phase 20 - Policy Systemd Intervals

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Apply saved policy intervals to systemd loop units in a staged, auditable way:

- preview unit interval changes;
- apply interval changes with confirmation;
- backup unit files before writing;
- daemon-reload and restart only the two loop services;
- verify V7 health after restart.

## Files Updated Locally

- `admin/v7-admin-api`
- `hardening/v7-safe-run`
- `hardening/v7-policy-apply-systemd`
- `hardening/v7-users-autoswitch`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-safe-run`
- `/usr/local/bin/v7-policy-apply-systemd`
- `/usr/local/bin/v7-users-autoswitch`

Restarted:

- `v7-admin-api`
- `v7-health`
- `v7-benchmark`

No VPN interfaces, routing tables, WireGuard, sing-box, AmneziaWG, kill switch, DNS, or API core service was restarted.

## Admin API Added

- `POST /api/actions/policy-systemd-preview`
- `POST /api/actions/policy-systemd-apply`

Apply requires typed confirmation:

- `APPLY_INTERVALS`

## Admin UI Added

Settings / Policy now includes:

- `Systemd Preview`
- `Apply Systemd Intervals`

## Script Added

`v7-policy-apply-systemd`

Behavior:

- reads `/etc/v7/policy.json` through `v7-policy-env`;
- validates safe ranges;
- patches only the sleep value in:
  - `/etc/systemd/system/v7-health.service`
  - `/etc/systemd/system/v7-benchmark.service`
- backs up changed unit files;
- runs `systemctl daemon-reload`;
- restarts `v7-health` and `v7-benchmark`;
- verifies both are active;
- writes structured audit.

Current policy matched current units:

- `v7-health`: `sleep 30`
- `v7-benchmark`: `sleep 300`

So the apply was a no-op for file content, but restart/verify was tested.

## Sticky Autoswitch Fix

During loop restart, the old autoswitch behavior moved `10.0.0.2` from `awg2` to `vless` because it still allowed a planned switch when current egress had `code=200`.

That contradicted the V7 production rule:

- keep sticky assignment if current egress is healthy;
- do not switch users just because another egress is faster;
- use health loop for failover/degraded current path, not routine rebalance.

Fix applied:

- `v7-users-autoswitch` now computes current egress quality using policy thresholds;
- if current egress is quality OK, it returns:
  - `ACTION=keep_current_healthy`
  - `REASON=sticky_assignment_current_quality_ok`
- planned switching is allowed only when current quality is not OK;
- failover still works when current is down.

Restored:

- `10.0.0.2` returned to `awg2`
- `10.0.0.3` remained on `awg2`

## Validation

Local validation:

- `python3 -m py_compile admin/v7-admin-api` - OK
- `bash -n v7-policy-apply-systemd` - OK
- `bash -n v7-safe-run` - OK
- `bash -n v7-users-autoswitch` - OK

VPS validation:

- `v7-policy-apply-systemd` dry-run - OK
- `v7-policy-apply-systemd --apply` - OK
- admin preview endpoint - OK
- admin apply without confirmation - HTTP 400
- units still show:
  - health `sleep 30`
  - benchmark `sleep 300`
- waited one health loop after sticky fix - no unexpected switch
- both users remained on `awg2`
- `v7-user-route-check` - OK
- `v7-system-check` - OK
- `v7-killswitch-check` - OK
- all services active - OK

Current users:

- `10.0.0.2 current=awg2 table=100 enabled=1`
- `10.0.0.3 current=awg2 table=101 enabled=1`

## Backups

Pre-install backup:

- `/root/v7-phase20-policy-systemd-backup-20260506-235542`

Sticky autoswitch fix backup:

- `/root/v7-phase20-autoswitch-sticky-fix-backup-20260506-235806`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-235906.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-235906.tar.gz.sha256`

## Notes

This phase exposed and fixed a real production risk: health autoswitch was still partly acting like automatic optimization. It is now aligned with the intended V7 behavior: sticky by default, failover/degraded recovery only, manual rebalance separately.

