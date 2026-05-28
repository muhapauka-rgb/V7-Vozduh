# E11.5 Regression Matrix

| Egress | Pre Diagnose | Post Diagnose | Interface State | Route/Quality | Blocker Before | Blocker After | Regression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WireGuard `wireguard-1779454504-c43409` | Runtime `SUSPECT`, `handshake_age_seconds=999999` | Repo fixture `OK`, fresh `wg show` age | `UP,LOWER_UP` in prior live evidence | quality OK, zero-user, exclusions present | `diagnose SUSPECT` / `severity_SUSPECT` | none in fixed fixture | no repo regression; runtime deploy still pending |
| AWG0 | Runtime/readiness `OK` but low quality | Repo tests keep AWG on `awg show` | UP in readiness fixture | below canary quality floor | quality/exclusion blockers | unchanged by protocol fix | no command-path regression observed in tests |
| AWG3 | Runtime/readiness `OK` but low quality | Repo tests keep AWG on `awg show` | UP in readiness fixture | below canary quality floor | quality/exclusion blockers | unchanged by protocol fix | no command-path regression observed in tests |
| Target `1` | `OK` | Repo fixture `OK` for AWG path | UP in readiness fixture | occupied/load-state blocker | occupied/load-state users | unchanged | no regression |
| OpenVPN | `SUSPECT`, stale/unsupported handshake semantics | Repo fixture remains non-clean (`SUSPECT` unsupported handshake) | UP in readiness fixture | quality OK but not selected | diagnose blocker | diagnose blocker | no canary readiness relaxation |
| vless | not canary target | repo fixture marks handshake unsupported | baseline proxy | not evaluated as target | baseline/current egress | unchanged for target pool | no target impact |

Summary:

```text
awg_regression_observed=false
wireguard_fix_validated_repo_side=true
runtime_regression_unknown_until_deploy=true
```

