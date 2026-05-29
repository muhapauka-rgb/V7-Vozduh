# E25.11 Readiness, Diagnose, And Load Integration

## Result

`readiness_helper_supports_execution_only=true`

`target_readiness_final_status=GO`

`selected_moves_zero=true`

`autoswitch_assignment_still_blocked=true`

## Helper Change

`v7-second-canary-target-readiness` now supports an explicit operator execution mode:

```text
--execution-target-id <target-id>
```

Default behavior is unchanged:

- `manual_only=1` remains a default rejection reason.
- `reserve_only=1` remains a default rejection reason.
- execution-only targets are not automatically selected for canary/autoswitch-style movement.

Explicit operator execution mode permits only the requested `role=EXECUTION_ONLY` target, and only when all guard metadata is present:

- `execution_reserved=true`
- `canary_reserved=true`
- `reservation_owner=operator_execution_governance`
- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`

Quality, diagnose, load, zero-user, interface, and route-class checks are still enforced.

## Diagnose / Load / Stability State

The target was integrated into runtime state files:

- `egress-load.state`
  - `amneziawg-exec-20260528-10-8-1-14_users=0`
  - `amneziawg-exec-20260528-10-8-1-14_load_status=OK`
  - `amneziawg-exec-20260528-10-8-1-14_soft_limit=1`
  - `amneziawg-exec-20260528-10-8-1-14_hard_limit=1`
- `egress-diagnose.state`
  - `amneziawg-exec-20260528-10-8-1-14_diagnose_severity=OK`
  - `amneziawg-exec-20260528-10-8-1-14_diagnose_detail=handshake_age_seconds=3;target_local_ping_ok;curl_1mb_22mbps`
- `egress-stability.state`
  - `amneziawg-exec-20260528-10-8-1-14_avg_mbps=22.04`
  - `amneziawg-exec-20260528-10-8-1-14_min_mbps=22.04`
  - `amneziawg-exec-20260528-10-8-1-14_stability=1.0`
- `interface-state.state`
  - `v7execwg0=UP,LOWER_UP`

The helper was also fixed so `egress-quality-summary.json` remains a per-key fallback when an `egress-stability.state` file exists for only the execution target.

## Validation

Default mode:

- selected target: `wireguard-1779454504-c43409`
- execution target status: `NO-GO`
- execution target rejection reasons: `manual_only`, `reserve_only`

Explicit execution mode:

- command: `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty`
- selected target: `amneziawg-exec-20260528-10-8-1-14`
- target status: `GO`
- zero-user: `true`
- diagnose: `OK`
- avg Mbps: `22.04`
- min Mbps: `22.04`
- stability: `1.0`

## Autoswitch Safety

Execution-only metadata remains:

- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`
- `manual_only=1`
- `reserve_only=1`

This makes the target eligible only for explicit operator execution governance, not automatic assignment.
