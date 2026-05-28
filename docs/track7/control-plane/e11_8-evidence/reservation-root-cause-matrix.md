# E11.8 Reservation Root-Cause Matrix

| Path | Reservation aware before | Enforcement before | Bypass possible before | Runtime evidence | Fix complexity | Blast radius |
|---|---:|---:|---:|---|---|---|
| planner | no | no | yes | no `canary_reserved` parser/gate | low | low if destination-only |
| apply | no | indirect only | yes | apply trusts `selected_moves` | medium | low after planner gate |
| rebalance | no | no | yes | rebalance uses eligible candidates | low | low |
| fallback/failover | no | no | yes | WireGuard selected by `autoswitch_failover` | low | low |
| load balancing | no | no | yes | `_healthy_for_load()` counted reserved targets | low | low |
| target readiness | yes/partial | readiness only | no runtime authority | canary blocked after occupancy | none | none |
| routing-sync | not involved | not involved | not evidenced | no routing-sync process/history cause | none | none |
| reconcile | not involved | not involved | not evidenced | checks did not cause assignment | none | none |
| reservation parser | no | no | yes | `_load_egress()` ignored key | low | low |
| state persistence | not primary | not primary | possible but not causal | source missing key | none | none |
| cached state | not primary | not primary | possible but not causal | current source/runtime matched old behavior | none | none |
| existing-user drain semantics | missing | no | yes | 10 users remain on reserved target | separate approval | medium if drained |

Root cause classification: `MIXED`, specifically `RESERVATION_METADATA_NOT_CONSUMED + PLANNER_IGNORES_RESERVATION + APPLY_TRUSTS_PLANNER + EXISTING_USERS_NOT_DRAINED`.

Confidence: high.
