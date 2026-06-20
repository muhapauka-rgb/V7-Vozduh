# CURRENT CAPACITY MODEL

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Summary

Current V7 capacity is an assignment/load safety model. It is not a measured physical tunnel-capacity model.

It answers:

- how many users are currently assigned to a channel;
- whether adding or failing over users would cross configured soft, hard, or failover-hard limits;
- whether the planner should restrict new movement to that channel.

It does not answer:

- actual third-party tunnel CPU/RAM/bandwidth;
- real provider-side tunnel maximum throughput;
- whether observed traffic has saturated the underlying infrastructure;
- whether quality will degrade at a specific user count.

## Current Inputs

| Input | Current role | Owner |
| --- | --- | --- |
| Assigned users | Primary load count per egress | `tools/v7-users-autoswitch`, runtime state |
| `soft_limit` | Warning / soft-full threshold | egress registry or load policy |
| `hard_limit` | Planned-assignment block threshold | egress registry or load policy |
| `failover_hard_limit` | emergency/failover hard limit | load policy, capped by explicit capacity |
| `capacity_users` | explicit per-egress cap when present | egress registry metadata |
| Healthy working pool | denominator for dynamic average load | `_healthy_for_load` |
| Reserve ratio | removes reserve headroom from normal distribution | load policy |
| Dynamic multipliers | derive soft/hard/failover limits from average load | load policy |

## Current Calculation

`tools/v7-users-autoswitch` owns the planner-side model:

- `_load_policy`
- `_healthy_for_load`
- `_dynamic_load_summary`
- `_load_limits_for_egress`
- `_capacity_status`
- `_capacity_decision`
- `_gate_load`

`admin/v7-admin-api` renders capacity/load through:

- `channelSuitabilityCapacity`
- `channelLoad`
- `loadPosture`
- channel signals and diagnostics

## Current Semantics

| State | Meaning |
| --- | --- |
| `OK` | Current assigned users are within assignment limits. |
| `SOFT_FULL` | Current users reached soft assignment warning. |
| `HARD_FULL` | Planned new assignments are restricted. |
| `FAILOVER_FULL` | Failover-hard assignment limit reached. |

These states are policy/load states, not proof of physical saturation.

## Current Production Evidence

`docs/capacity_1/evidence/production_capacity_summary.json` captured:

| Channel | Users | Avg Mbps | Min Mbps | Stability | Load status |
| --- | ---: | ---: | ---: | ---: | --- |
| `vless` | 11 | 37.453 | 35.46 | 0.946787 | `HARD_FULL` |
| `awg3` | 8 | 46.6283 | 37.58 | 0.805948 | `HARD_FULL` |
| `awg0` | 0 | 43.4387 | 32.02 | 0.737131 | `OK` |
| `wireguard-1779454504-c43409` | 8 | 45.5093 | 38.46 | 0.845102 | `HARD_FULL` |

This proves the current model can mark working channels as full for assignment. It does not prove the channel is physically saturated.

## Audit Verdict

Current capacity model remains valid as a safety rail for assignment and failover. It is insufficient as a real practical-capacity model for third-party tunnels because it does not learn a channel's observed degradation point.
