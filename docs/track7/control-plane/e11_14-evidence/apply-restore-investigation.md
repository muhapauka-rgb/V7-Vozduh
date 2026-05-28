# BLOCK E11.14 Apply-Restore Investigation

investigation_completed=true

## Current State Snapshot

- Apply timer is held: `v7-users-autoswitch.timer=inactive`.
- Planner timer remains active: `v7-autoswitch-planner.timer=active`.
- Health service remains active.
- Current dry-run autoswitch plan: `candidate_moves_total=0`, `selected_moves=0`.
- Current registry state: 10.7.0.9, 10.7.0.10, 10.7.0.13 remain on `awg0`; mini-cohort users 10.7.0.11 and 10.7.0.12 remain on target `1`.
- WireGuard target remains canary-reserved and has zero production users.

## Apply-Restore Findings

1. Restore-settle was clean before apply restore.
   Evidence: `restore-settle.json` shows `gate_status=GO`, `sample_count=3`, `apply_timer_intervals_covered=3.45`, `selected_moves_by_sample=[0,0,0]`.

2. Apply restore did not immediately move users.
   Evidence: apply timer runs at 13:16:38, 13:17:00, 13:17:23, 13:17:43, and 13:18:04 all had `selected_moves=0`.

3. The delayed movement came from a later fresh apply recompute.
   Evidence: 13:18:24 apply run had `candidate_moves_total=5`, `selected_moves=3`, `apply_requested=true`, `applied=true`.

4. The selected users were non-cohort users.
   Evidence: selected moves were 10.7.0.9, 10.7.0.10, 10.7.0.13, all from `1` to `awg0`.

5. The immediate trigger was target `1` transient Telegram hard ineligibility.
   Evidence: selected move details show current target `1` blocked by `telegram_required_telegram_down_14s`; `awg0` was eligible and WireGuard was blocked by `canary_reserved_production_assignment_blocked`.

6. Reservation enforcement held.
   Evidence: WireGuard remained blocked for production by `canary_reserved_production_assignment_blocked`; no delayed move selected WireGuard.

7. Rebalance and reconnect were not the movement class.
   Evidence: `rebalance_candidates=0`, `reconnect_rotation_candidates=0`, selected move type was `failover`.

8. Hidden mover theory is not supported.
   Evidence: systemd journal invocation is `python3 /usr/local/bin/v7-users-autoswitch --apply`; process scans after containment and post-fix samples show no hidden `v7-user-switch` or `v7-routing-sync`.

## Fix Applied

bounded_runtime_fix=true
fix_scope=v7-users-autoswitch restore-barrier failover quarantine support
runtime_backup=/usr/local/bin/v7-users-autoswitch.e11_14_backup_20260527T105151Z
installed_sha=10e87444c6f522bdeca0a3d21f02e8819e6d4f5797653546deeb89f92bed0e60
restore_barrier_file=/opt/v7/egress/state/autoswitch-restore-barrier.json
restore_barrier_active=true
restore_barrier_expires_at=2026-05-28T10:52:27.369480+00:00

## Operational Impact

The old lifecycle treated pre-restore settle GO as sufficient for restoring a 20-second apply timer. That was insufficient because a later apply cycle can encounter fresh failover pressure and move non-cohort production users. The v2 fix adds an explicit restore barrier that suppresses failover selection during the bounded restore window.
