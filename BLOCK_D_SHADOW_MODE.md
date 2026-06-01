# Block D Shadow Mode

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Command

Shadow mode was run without `--apply`:

```text
v7-users-autoswitch --mode guarded --service telegram --route-class GLOBAL_STABLE --pretty
```

## Shadow Output

- `apply_requested=false`
- `mode=guarded`
- `candidate_moves=12`
- `candidate_moves_total=12`
- `selected_moves=0`
- `rebalance_candidates=0`
- `reconnect_rotation_candidates=0`
- `users_total=18`
- `healthy_egress_total=2`

Action counts:

- `keep=6`
- `switch=12`

Move type counts:

- `failover=12`
- `none=6`

Recommended egress counts:

- `awg3=15`
- `awg0=3`

## WOULD Classifications

`WOULD_MOVE`:

- Raw planner produced `12` failover recommendations.

`WOULD_BLOCK`:

- Actual selected moves remained `0`.
- Safety review was `critical`.
- Execution target is full and current D0 recommendation requires a new execution target before expansion.

`WOULD_REVIEW`:

- All raw failover recommendations require operator review because scope is wider than a bounded approved packet.

`WOULD_ROLLBACK`:

- No rollback action was proposed or executed.

## Verdict

`shadow_mode_certified=true`

