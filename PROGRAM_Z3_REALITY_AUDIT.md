# Program Z3 Reality Audit

Date: 2026-06-01
Mode: Live runtime execution audit

## Verdict

reality_audit_complete=true
live_runtime_found=true

## Live Runtime Access

Read-only SSH access to `v7-vps` succeeded.

- hostname: `v3119922.hosted-by-vdsina.ru`
- live state path: `/opt/v7/egress/state`
- live state present: `true`
- collection time: `2026-06-01T17:31:39Z`

## Fresh Live Registries

- users registry hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- active users in load summary: `18`
- total channels: `7`
- healthy channels: `2`
- capacity status: `ok`

Current live user distribution:

- `amneziawg-exec-20260528-10-8-1-14`: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`
- `1`: `0`
- `openvpn-1779388847-d2ad7c`: `0`
- `wireguard-1779454504-c43409`: `0`

## Health, Capacity, Trust

Live capacity:

- `operator_status=ok`
- `summary.status=ok`
- all per-egress capacity status values observed as `OK`

Live diagnose:

- `awg0`: `OK`
- `awg3`: `OK`
- `1`: `OK`
- `wireguard-1779454504-c43409`: `OK`
- `amneziawg-exec-20260528-10-8-1-14`: `OK`
- `vless`: `SUSPECT`
- `openvpn-1779388847-d2ad7c`: `SUSPECT`

Trust/class notes:

- `awg0` and `awg3` are `GLOBAL_STABLE`
- `amneziawg-exec-20260528-10-8-1-14` is `EXECUTION_ONLY`, `manual_only=1`, `reserve_only=1`, `autoswitch_allowed=false`
- `awg0` and `awg3` do not carry the same explicit `exclude_route_classes` metadata as dedicated execution targets

## Planner State

Fresh live planner command:

`v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE`

Result:

- updated: `2026-06-01T17:33:03.390450+00:00`
- planner generation id: `07fc79a3931bdf39b1969699d31f69b05756805a28cdfbcb9e039bcaeba010e1`
- candidate moves: `12`
- selected moves: `0`
- apply requested: `false`
- apply result: `dry_run`

## Blocking Runtime Guard

Live restore barrier:

- file: `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- owner: `control_plane_governance`
- block: `E11.17`
- rehearsal: `expired_cleared_budget_zero`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`

Planner guard result:

- `restore_active=false`
- `restore_expired=true`
- `clearance_budget_exceeded=true`
- `clearance_guard_reason=restore_barrier_clearance_selected_moves_exceed_budget`

## Safety

- runtime_mutation_performed=false
- users_moved=false
- routing_changed=false
- autoswitch_apply_outside_packet=false
- deploy_performed=false

