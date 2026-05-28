# E10 Fresh Target Selection

Mode: read-only approval packet only.

Source evidence:

- `docs/track7/control-plane/e10-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e10-evidence/current-state/egress.registry`
- `docs/track7/control-plane/e10-evidence/current-state/egress-load.state`
- `docs/track7/control-plane/e10-evidence/current-state/egress-diagnose.state`
- `docs/track7/control-plane/e10-evidence/current-state/stability.state`
- `docs/track7/control-plane/e10-evidence/current-state/interface-state.state`

## Fresh Target Matrix

| Target | Users by registry | Users by load | Interface | Diagnose | Quality | Route-class safety | Verdict |
|---|---:|---:|---|---|---|---|---|
| `1` | 2 | 2 | UP/LOWER_UP | OK | OK | has Direct/RU and Trusted RU exclusions | NO-GO: occupied and hard/full by load-state |
| `awg0` | 0 | 0 | UP/LOWER_UP | OK | above floor | missing Direct/RU and Trusted RU exclusions | NO-GO under strict rules |
| `awg3` | 0 | 0 | UP/LOWER_UP | OK | above floor | missing Direct/RU and Trusted RU exclusions | NO-GO under strict rules |
| `openvpn-1779388847-d2ad7c` | 0 | 0 | UP/LOWER_UP | SUSPECT | above floor | has Direct/RU and Trusted RU exclusions | NO-GO without explicit idle-SUSPECT waiver |
| `wireguard-1779454504-c43409` | 0 | 0 | UP/LOWER_UP | SUSPECT | above floor | has Direct/RU and Trusted RU exclusions | NO-GO without explicit idle-SUSPECT waiver |

## Current Readiness Tool Result

```text
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
target_1_current_user=10.7.0.14,10.7.0.15
zero_user_targets=awg0,awg3,openvpn-1779388847-d2ad7c,wireguard-1779454504-c43409
```

## Waiver Review

Possible waiver paths exist, but none should be silently promoted by E10.

| Waiver path | Current blocker | E10 decision |
|---|---|---|
| `awg0` route-class waiver | zero-user and diagnose OK, but missing Direct/RU and Trusted RU exclusions | not acceptable without explicit route-class waiver approval |
| `awg3` route-class waiver | zero-user and diagnose OK, but missing Direct/RU and Trusted RU exclusions | not acceptable without explicit route-class waiver approval |
| OpenVPN idle-SUSPECT waiver | zero-user and exclusions present, but diagnose SUSPECT | stale E9.2.5 waiver cannot be reused; needs fresh explicit waiver packet |
| WireGuard idle-SUSPECT waiver | zero-user and exclusions present, but diagnose SUSPECT | not approved in E10 |
| occupied target `1` | currently has `10.7.0.14` and `10.7.0.15` | not acceptable for fresh isolation canary |

## Target Verdict

```text
selected_target=NONE
target_status=NO-GO
waiver_required=true
waiver_acceptable=false
rollback_feasible=false_without_target
execution_allowed_now=false
```

The fresh second canary cannot be approved until either:

1. a clean target appears; or
2. a separate explicit waiver packet approves one exact target and risk class.
