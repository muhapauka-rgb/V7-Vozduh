# E11.7 Fresh Candidate Selection

Result: no candidate selected for approval.

Reason: Phase 1 abort condition is active. The intended target
`wireguard-1779454504-c43409` is no longer a zero-user target in current runtime
truth.

Current user distribution:

```text
wireguard-1779454504-c43409 users=12
1 users=4
awg0 users=0
awg3 users=0
openvpn-1779388847-d2ad7c users=0
```

Strict target readiness:

```text
approval_status=NO-GO
selected_target=NONE
second_canary_readiness=NO-GO
wireguard_blocker=occupied by registry users + load-state users=12
```

Candidate review:

| Candidate | Current Egress | Table | Route State | Current Finding |
| --- | --- | --- | --- | --- |
| `10.7.0.14` | `1` | `1012` | route_get OK via `v7e356a192b79` | previously useful canary user, but old rollback/current assumptions are stale and target is occupied |
| `10.7.0.10` | `1` | `1008` | route_get OK via `v7e356a192b79` | target occupied; not selected |
| `10.7.0.11` | `1` | `1009` | route_get OK via `v7e356a192b79` | target occupied; not selected |
| `10.7.0.15` | `1` | `1013` | route_get OK via `v7e356a192b79` | target occupied; not selected |
| users already on WireGuard | `wireguard-1779454504-c43409` | mixed | route_get OK via `v7e06a394c478` | cannot be candidate because current egress equals target |

Fresh candidate decision:

```text
candidate_user=NONE
current_egress=NONE
rollback_target=NONE
candidate_selection_status=DEFERRED_TARGET_NO_GO
```

If WireGuard is returned to zero-user/reserved state in a future governed
target-pool block, `10.7.0.14` can be reconsidered with current egress `1` and
rollback target `1`, subject to fresh switch-history and route checks.
