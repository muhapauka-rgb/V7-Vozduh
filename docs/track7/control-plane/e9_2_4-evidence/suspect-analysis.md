# E9.2.4 OpenVPN / WireGuard SUSPECT Analysis

Mode: read-only diagnostics only.

Targets:

- `openvpn-1779388847-d2ad7c` / interface `v7edb0c189291`
- `wireguard-1779454504-c43409` / interface `v7e06a394c478`

## Observed State

| Target | Interface State | Registry Users | Load Users | Diagnose | Detail | Avg Mbps | Min Mbps | Stability | Route-Class Exclusions |
|---|---|---:|---:|---|---|---:|---:|---:|---|
| `openvpn-1779388847-d2ad7c` | `UP,LOWER_UP` | 0 | 0 | `SUSPECT` | `handshake_age_seconds=999999` | 66.6473 | 64.50 | 0.967781 | `TRUSTED_RU_SENSITIVE,DIRECT_RU` |
| `wireguard-1779454504-c43409` | `UP,LOWER_UP` | 0 | 0 | `SUSPECT` | `handshake_age_seconds=999999` | 51.648 | 48.01 | 0.929562 | `TRUSTED_RU_SENSITIVE,DIRECT_RU` |

## Source/Gate Semantics

`tools/v7-users-autoswitch` blocks any candidate with diagnose severity outside `OK`/`WARN`:

```text
if egress.severity and egress.severity.upper() not in ("OK", "WARN"):
    block severity_<severity>
```

`tools/v7-egress-quality-compact` also treats non-OK/WARN diagnose severity as failed quality input:

```text
severity_ok = severity in ("", "OK", "WARN")
if not health_ok or not severity_ok:
    fail_rate = 1.0
```

Therefore `SUSPECT` is a hard blocker for clean target readiness even when interface state and throughput history look good.

## Interpretation

The available evidence points to stale/idle handshake semantics, not a proven dead datapath:

- interfaces are present and `UP,LOWER_UP`;
- registry and load-state both show zero users;
- throughput/stability history is strong;
- route-class exclusions are appropriate for a generic non-Direct/Trusted-RU canary;
- the only observed blocker is diagnose `SUSPECT` with sentinel-like `handshake_age_seconds=999999`.

The evidence does not prove the targets are currently safe for a live canary because:

- no live traffic is assigned to them;
- no fresh route_get for candidate `10.7.0.14` through those interfaces was captured in E9.2.4;
- no fresh peer transfer/counter evidence was captured in E9.2.4;
- diagnose state remains `SUSPECT`.

## Classification

| Target | Classification | Reason |
|---|---|---|
| `openvpn-1779388847-d2ad7c` | `IDLE_BUT_HEALTHY` + `DIAGNOSE_TOO_STRICT` | Strong throughput/stability and interface-up evidence; blocked by stale handshake only. Needs waiver or fresh diagnose OK. |
| `wireguard-1779454504-c43409` | `IDLE_BUT_HEALTHY` + `DIAGNOSE_TOO_STRICT` | Strong throughput/stability and interface-up evidence; blocked by stale handshake only. Needs waiver or fresh diagnose OK. |

## Canary Implication

These targets are not `CLEAN_READY` under current rules. They are possible `CANARY_SAFE_WITH_WAIVER` candidates if the operator explicitly accepts that stale idle handshake is not proof of datapath failure.

The best zero-user waiver candidate is `openvpn-1779388847-d2ad7c` because it has the strongest observed avg/min/stability values.
