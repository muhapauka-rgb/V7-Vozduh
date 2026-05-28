# E9.2.2 Target Candidate Matrix

Mode: read-only target selection only.

Selection target: `candidate=10.7.0.14`, current `vless`, rollback `vless`.

Quality floor used for canary target selection:

```text
diagnose_severity must be OK
avg_mbps should be >= 15
min_mbps should be >= 10
stability should be >= 0.45
zero users required by registry/load-state
```

| Egress ID | Interface | Enabled | Role | Registry Users | Load Users | Interface UP | Diagnose | Avg Mbps | Min Mbps | Stability | Manual Only | Reserve Only | Exclude Route Classes | Direct/RU/Trusted RU Risk | Zero User | Safe For Second Canary | Rejection Reason |
|---|---|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| `1` | `v7e356a192b79` | 1 | `GLOBAL_FAST` | 1 | 1 | yes | OK | 59.868 | 51.33 | 0.857386 | 0 | 0 | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | low for generic canary, excludes sensitive classes | no | no | occupied by real user `10.7.0.5`; static load `SOFT_FULL` |
| `awg0` | `awg0` | 1 | `GLOBAL_STABLE` | 0 | 0 | yes | OK | 11.909 | 4.17 | 0.350155 | not set | not set | none declared | unknown; no explicit sensitive-class exclusion | yes | no | below quality floor: avg/min/stability too low |
| `awg3` | `awg3` | 1 | `GLOBAL_STABLE` | 0 | 0 | yes | OK | 5.62633 | 4.39 | 0.78026 | not set | not set | none declared | unknown; no explicit sensitive-class exclusion | yes | no | below quality floor: avg/min too low; E9 governance already avoids awg3 |
| `openvpn-1779388847-d2ad7c` | `v7edb0c189291` | 1 | `GLOBAL_FAST` | 0 | 0 | yes | SUSPECT | 66.6473 | 64.50 | 0.967781 | 0 | 0 | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | low for generic canary, excludes sensitive classes | yes | no | diagnose is SUSPECT because handshake is stale |
| `wireguard-1779454504-c43409` | `v7e06a394c478` | 1 | `GLOBAL_FAST` | 0 | 0 | yes | SUSPECT | 51.648 | 48.01 | 0.929562 | 0 | 0 | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | low for generic canary, excludes sensitive classes | yes | no | diagnose is SUSPECT because handshake is stale |

## Matrix Verdict

```text
safe_zero_user_target_exists=false
selected_target=NONE
approval_status=NO-GO
```

There is no target that simultaneously has zero users, OK diagnose, acceptable quality floor, non-sensitive route-class behavior, and clean readiness.
