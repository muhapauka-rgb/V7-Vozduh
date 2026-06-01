# Program Z3.1 Reality Audit

Date: 2026-06-01
Mode: Live runtime governance

## Verdict

reality_audit_complete=true
live_runtime_used=true

## Live Runtime

- host: `v3119922.hosted-by-vdsina.ru`
- state dir: `/opt/v7/egress/state`
- live users registry hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- live egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`

## Initial Barrier State

Initial live barrier:

- file: `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- block: `E11.17`
- owner: `control_plane_governance`
- rehearsal: `expired_cleared_budget_zero`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`

Initial planner:

- unfiltered candidate moves: `12`
- unfiltered selected moves after guard: `0`
- unfiltered selected moves before guard: `3`
- guard: `restore_barrier_clearance_selected_moves_exceed_budget`

## One-User Filtered Planner

Filtered command:

`v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE --user 10.7.0.16 --target-egress awg3`

Initial filtered planner:

- candidate moves: `1`
- selected moves after guard: `0`
- selected moves before guard: `1`
- selected moves hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- candidate: `10.7.0.16 vless -> awg3`

## Runtime Mutation

Z3.1 performed one governance-only runtime mutation:

- updated `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- created backup `/opt/v7/egress/state/z3_1-backups/autoswitch-restore-barrier.20260601T174520Z.json`
- refreshed backup `/opt/v7/egress/state/z3_1-backups/autoswitch-restore-barrier.refresh.20260601T174715Z.json`
- did not run `v7-users-autoswitch --apply`
- did not run `v7-user-switch`

## Final Barrier State

Final clearance:

- block: `PROGRAM_Z3_1`
- allowed user: `10.7.0.16`
- allowed target: `awg3`
- allowed budget: `1`
- clearance max selected moves: `1`
- approved selected moves hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- clearance generation id: `af7bd1d112e0f52dafea36e5b3bdb86edd6d8fd74a1622748a463b0bf7a373fd`
- clearance expires at: `2026-06-01T17:57:15Z`

## Safety

- budget<=1
- users_moved_count=0
- scope_expanded=false
- autoswitch_apply_outside_governance=false
- routing_changed_outside_scope=false

