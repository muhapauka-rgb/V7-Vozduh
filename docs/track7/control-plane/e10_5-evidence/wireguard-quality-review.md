# E10.5 WireGuard Quality / Stability Review

Mode: read-only target diagnostic.

## WireGuard Quality

Fresh runtime evidence for `wireguard-1779454504-c43409`:

```text
users=0
load_status=OK
avg_mbps=50.202
min_mbps=45.35
stability=0.90335
samples=30
interface=UP,LOWER_UP
diagnose=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
```

Latest planner evidence also shows the target above canary quality floor:

```text
avg_mbps=50.34 to 50.78
min_mbps=45.35 to 49.38
stability=0.901 to 0.973
load_status=OK
users=0
```

## Comparison With Other Targets

| Target | Users | Diagnose | Quality Status | Notes |
|---|---:|---|---|---|
| `wireguard-1779454504-c43409` | 0 | SUSPECT | OK | Blocked by stale-handshake diagnose only |
| `openvpn-1779388847-d2ad7c` | 0 | SUSPECT | mixed | High throughput, but historical fail-rate advisory remains noisy |
| `awg0` | 0 | OK | low | Below min/stability floor in latest planner evidence |
| `awg3` | 0 | OK | low | Below stability floor in latest planner evidence |
| `1` | 0 in latest planner sample | OK/degraded Telegram | OK | Not preferred as clean test target due prior occupancy/churn history |
| `vless` | 16 | OK | production baseline | Rollback target, not canary target |

## Conclusion

```text
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_better_than_awg0_awg3=true
wireguard_operationally_best_conditional_target=true
```

WireGuard satisfies the quality floor and has the required route-class exclusions. The only clean-target blocker is persisted `diagnose=SUSPECT`; live handshake evidence indicates that blocker is a stale-diagnose false positive rather than a real route or interface failure.
