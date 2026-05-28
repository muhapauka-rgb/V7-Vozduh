# E24.2 Pre-Window Baseline

Collected: 2026-05-28T09:39:55Z on `v3119922.hosted-by-vdsina.ru`.

## Runtime Identity

- `hostname=v3119922.hosted-by-vdsina.ru`
- `date_utc=Thu May 28 09:39:55 UTC 2026`

## Runtime Hashes

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

## Candidate

- `ip=10.7.0.11`
- `current=1`
- `table=1009`
- `enabled=1`

Abort gate:

- candidate not on `1`: NO

## WireGuard Target

Target row:

- `id=wireguard-1779454504-c43409`
- `protocol=wireguard`
- `interface=v7e06a394c478`
- `enabled=1`
- `role=GLOBAL_FAST`
- `soft_limit=1`
- `hard_limit=2`
- `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`
- `canary_reserved=true`
- `reservation_reason=second_canary_target`
- `reservation_owner=control_plane_governance`

Users per egress:

- `1=4`
- `awg0=3`
- `awg3=9`
- `wireguard-1779454504-c43409=0`

Abort gate:

- WireGuard occupied: NO
- WireGuard reservation missing: NO

## Selected Moves

- `/opt/v7/egress/state/*selected*`: no files
- interpreted selected_moves: `0`

Abort gate:

- selected_moves > 0: NO

## Restore Barrier / Generation State

`autoswitch-restore-barrier.json`:

- `block=E11.17`
- `enabled=true`
- `expires_at=2000-01-01T00:00:00+00:00`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`
- `clearance_issued_at=2026-05-27T13:13:16.749351+00:00`

`autoswitch-safety.json` did not expose planner/apply/restore generation IDs; keys observed were `egress`, `schema_version`, `updated`, `users`.

## Timers

- `v7-users-autoswitch-planner.timer=inactive`
- `v7-users-autoswitch-apply.timer=inactive`
- systemd listed `0` timers for these units.

Sampling note:

- Apply timer is held/inactive.
- E24.2 interval coverage is nominal coverage against the restore-settle helper's configured `apply_timer_seconds=20`, not evidence of actual apply timer firings.

## Hidden Mover Scan

No active processes found:

- no `v7-user-switch`
- no `v7-routing-sync`
- no `v7-users-autoswitch --apply`

Abort gate:

- hidden mover active: NO

## Target Readiness Helper

Command:

- `v7-second-canary-target-readiness --json`

Key output:

- `state_dir=/opt/v7/egress/state`
- `candidate_still_valid=true`
- `selected_target=wireguard-1779454504-c43409`
- `approval_status=GO`
- `second_canary_readiness=GO`
- `execution_allowed_now=false`

Abort gate:

- target readiness != GO: NO

## Current Restore-Settle Helper Output

Command:

- `v7-restore-settle-gate --pre-restore --state-dir /opt/v7/egress/state --json`

Key output:

- `gate_status=CONDITIONAL`
- `sample_count=1`
- `required_samples=3`
- `apply_timer_intervals_covered=0.0`
- `selected_moves_by_sample=[0]`
- `checkers_ok=true`
- `hidden_movers_observed=false`

This is the reason E24.2 sample collection is required.

## Runtime Checkers

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`

Abort gate:

- runtime checker failure: NO

## Baseline Verdict

`pre_window_abort=false`

Sampling may proceed.
