# E10.3 Target Pool Matrix

Mode: read-only target-pool truth refresh.

Evidence sources:
- `fresh-global-runtime-snapshot.txt`
- `current-target-readiness.json`
- `current-restore-settle.json`
- `restore-settle-live-samples.txt`
- `process-guard.txt`

Fresh observation time:
- runtime snapshot: `2026-05-26T17:15:58Z`
- settle samples: `2026-05-26T17:19:00Z` to `2026-05-26T17:20:10Z`

## Summary

| Egress | Interface | Enabled | Registry users | Load users | Zero-user | Diagnose | Interface | Avg Mbps | Min Mbps | Stability | Load status | Exclusions | Canary target status | Remediation / waiver | Risk notes |
|---|---|---:|---:|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| `vless` | `tun0` | 1 | 10 | 11 | no | OK | UP/LOWER_UP | n/a | n/a | n/a | HARD_FULL in load-state | none | NO-GO | none | Current rollback/default pool, not a target for second canary. Load-state has one-count drift versus enabled registry summary. |
| `awg0` | `awg0` | 1 | 0 | 0 | yes | OK | UP/LOWER_UP | 27.3767 | 1.78 | 0.0650188 | OK | none | NO-GO | Metadata exclusions alone are insufficient while quality is below floor. | Missing `DIRECT_RU` and `TRUSTED_RU_SENSITIVE`; min/stability fail target-readiness floor. |
| `awg3` | `awg3` | 1 | 0 | 0 | yes | OK | UP/LOWER_UP | 35.0467 | 1.13 | 0.0322427 | OK | none | NO-GO | Metadata exclusions alone are insufficient while quality is below floor. | Missing `DIRECT_RU` and `TRUSTED_RU_SENSITIVE`; min/stability fail target-readiness floor. |
| `1` | `v7e356a192b79` | 1 | 6 | 6 | no | OK | UP/LOWER_UP | 57.9823 | 38.0 | 0.655372 | HARD_FULL in load-state; planner capacity OK | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | NO-GO | no remediation for canary target while occupied | Production egress currently holds six users: `10.0.0.2`, `10.0.0.3`, `10.0.0.6`, `10.7.0.2`, `10.7.0.3`, `10.7.0.4`. |
| `openvpn-1779388847-d2ad7c` | `v7edb0c189291` | 1 | 0 | 0 | yes | SUSPECT | UP/LOWER_UP | 53.8087 | 8.83 | 0.1641 | OK | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | NO-GO | waiver not recommended now | SUSPECT due stale handshake; current target-readiness also fails min/stability floor. |
| `wireguard-1779454504-c43409` | `v7e06a394c478` | 1 | 0 | 0 | yes | SUSPECT | UP/LOWER_UP | 46.7763 | 44.93 | 0.960529 | OK | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | NO-GO, best conditional waiver candidate if operator insists | Quality passes floor, but diagnose remains SUSPECT due stale handshake semantics. |

## Target Pool Verdict

```text
clean_zero_user_target_exists=false
selected_target=NONE
second_canary_readiness=NO-GO
execution_allowed_now=false
```

There are zero-user candidates, but none is clean:

- `awg0` / `awg3`: zero-user and diagnose OK, but target-readiness rejects both on quality floor and missing Direct/RU + Trusted RU exclusions.
- `openvpn-1779388847-d2ad7c`: zero-user but `SUSPECT`, plus current min/stability below floor.
- `wireguard-1779454504-c43409`: zero-user and quality OK, but `SUSPECT`; this is the least-bad conditional waiver candidate, not a clean GO.

