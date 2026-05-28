# E10.3 AWG Occupation History

Mode: read-only autoswitch history analysis.

## Current Truth

The E10.2 pre-gate saw `awg0` occupied and correctly aborted metadata mutation. Fresh E10.3 runtime truth shows that this was transient:

```text
awg0 registry_users=0
awg0 load_state_users=0
awg3 registry_users=0
awg3 load_state_users=0
target_1 registry_users=6
target_1 load_state_users=6
```

Current `target 1` users:

- `10.0.0.2`
- `10.0.0.3`
- `10.0.0.6`
- `10.7.0.2`
- `10.7.0.3`
- `10.7.0.4`

## Recent Movement Pattern

Fresh autoswitch/journal evidence shows AWG egresses have been part of the production autoswitch candidate pool, not isolated canary targets:

| Approx timestamp UTC | Movement evidence | Interpretation |
|---|---|---|
| `2026-05-26T16:37:35Z` to `16:37:55Z` | incoming safety entries on `awg0` / `awg3` | Autoswitch placed users on AWG egresses during failover/rebalance. |
| `2026-05-26T17:00:32Z` | `10.0.0.3`, `10.7.0.2` incoming to `1` | Users moved away from AWG/current alternatives into egress `1`. |
| `2026-05-26T17:02:39Z` | `10.0.0.2`, `10.0.0.6`, `10.7.0.3` incoming to `1` | Timer-driven autoswitch concentrated additional users on egress `1`. |
| `2026-05-26T17:02:56Z` | `10.7.0.4` incoming to `1` | Same recovery/rebalance phase. |
| `2026-05-26T17:11:44Z` | `10.7.0.14`, `10.7.0.15`: `1 -> vless` | Later autoswitch movement away from `1`; no AWG target occupancy after E10.3 snapshot. |

## Why AWG0/AWG3 Became Occupied

The occupation was autoswitch timer-driven production behavior, not an E10.2 mutation and not manual canary movement. The planner/apply evidence shows:

- AWG targets were previously selected during failover/rebalance windows.
- Later runs moved the relevant users away from AWG targets.
- Current `selected_moves=[]` and current registry/load-state show AWG zero-user again.

## Governance Interpretation

`awg0` and `awg3` should not be treated as stable clean canary targets just because they are zero-user at one instant. They are live production autoswitch candidates with recent churn, and current target-readiness still rejects them:

- `min_mbps_below_floor`
- `stability_below_floor`
- missing `DIRECT_RU` and `TRUSTED_RU_SENSITIVE` exclusions

Metadata remediation is not the next safe action while quality floor remains failed.

