# E9.4.4 Moved User Root Cause

## Per-User Matrix

| User | From | To | Table | Reason | Source Signal | Selected In Same Apply Run? | Cap Behavior |
|---|---|---|---:|---|---|---|---|
| `10.7.0.5` | `1` | `vless` | `1003` | `current_egress_not_eligible` | `telegram_required_telegram_down_14s` on egress `1` | Yes | One of first three failovers selected |
| `10.0.0.2` | `1` | `vless` | `100` | `current_egress_not_eligible` | `telegram_required_telegram_down_14s` on egress `1` | Yes | One of first three failovers selected |
| `10.0.0.3` | `1` | `vless` | `101` | `current_egress_not_eligible` | `telegram_required_telegram_down_14s` on egress `1` | Yes | One of first three failovers selected |

## Why These Three Users

The apply run saw `candidate_moves_total=16` and `selected_moves=3`. Runtime policy exposed `failover_limit=3`, so the broad candidate set was capped to three selected failover moves.

The three selected users match the safety-state incoming records:

```text
2026-05-26T07:29:08.088818+00:00 user_ip=10.7.0.5
2026-05-26T07:29:08.088941+00:00 user_ip=10.0.0.2
2026-05-26T07:29:08.088994+00:00 user_ip=10.0.0.3
```

## Target Selection

`vless` was selected because:

- it was eligible for the route classes involved;
- Telegram/service checks were OK for `vless`;
- other potential targets were rejected or deprioritized;
- current egress `1` was hard-blocked by Telegram at the apply cycle.

## Route Effect

The route changes matched registry movement and were not drift:

```text
10.0.0.2 table=100  -> tun0
10.0.0.3 table=101  -> tun0
10.7.0.5 table=1003 -> tun0
```

`v7-reconcile-check`, `v7-user-route-check`, `v7-killswitch-check`, and `v7-provisioning-reconcile-check` remained OK in E9.4.3 monitoring.

## Verdict

The three movements were expected autoswitch failover mechanics under a transient Telegram hard-block, but they were unsafe for canary attribution because they occurred after a restore that had been considered clean by immediate observation.

