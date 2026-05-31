# E35.0.1 Capacity Policy Audit

## Scope

Audit question: how capacity participates in selection.

## Capacity Inputs

capacity_policy_audited=true

Autoswitch capacity uses:

- active user count
- healthy egress count
- policy load mode
- `soft_limit`
- `hard_limit`
- `failover_hard_limit`
- per-egress `capacity_users`
- reserve ratio
- soft/hard/failover multipliers
- current users per egress

## Dynamic Load Model

In dynamic mode, autoswitch computes:

- healthy working channel pool
- reserve channel count
- average load
- dynamic soft/hard/failover limits

Per-egress `capacity_users`, if present, caps soft/hard limits.

## Hard Capacity Blocks

Capacity can hard-block:

- planned movement when target users >= hard limit
- failover when target users >= failover hard limit
- projected move selection when target would exceed hard limit

In non-dynamic/static mode, existing hard full can also block planned movement unless `--allow-hard-full`.

## Soft Capacity Preferences

Capacity also affects ranking:

- load score is higher when a channel has fewer users relative to hard limit.
- rebalance logic can move users from crowded channels to less loaded alternatives.
- projected move picker ranks lower projected target user count first.
- normal planned/rebalance/reconnect movement cannot exceed soft limit during selection.
- failover can be allowed over soft limit, but not over hard/failover hard limit.

## Can Capacity Override Speed and Service Fitness?

capacity_can_override_speed=true
capacity_can_override_service_fitness=true

Capacity hard gates run before score. A fast/service-fit channel can still be rejected if hard-full or failover-full. Projected selection can also redirect a move away from the initially recommended target to a lower-load eligible target.

## Audit Verdict

capacity_hard_gate=true
capacity_score_component=true
capacity_projection_exists=true
failover_can_over_soft=true
planned_cannot_over_soft_when_selecting=true
