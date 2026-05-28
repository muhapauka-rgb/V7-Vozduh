# E10.1 AWG0/AWG3 Remediation Analysis

Mode: read-only target remediation planning only.

Source evidence:

- `docs/track7/control-plane/e10_1-evidence/current-target-pool-snapshot.txt`
- `docs/track7/control-plane/e10_1-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e10_1-evidence/current-state/`

## Current State

| Target | Zero User | Interface | Diagnose | Avg Mbps | Min Mbps | Stability | Current Exclusions | Missing Exclusions | Current Verdict |
|---|---:|---|---|---:|---:|---:|---|---|---|
| `awg0` | true | UP/LOWER_UP | OK | 26.8167 | 22.43 | 0.836419 | none | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | NO-GO |
| `awg3` | true | UP/LOWER_UP | OK | 23.9337 | 16.0 | 0.668513 | none | `TRUSTED_RU_SENSITIVE,DIRECT_RU` | NO-GO |

Both targets are currently blocked by target-readiness policy only because route-class exclusions are missing. Both are zero-user by registry and load-state.

## Candidate Comparison

`awg0` is the better remediation candidate:

- higher average throughput: `26.8167` vs `23.9337`;
- higher minimum throughput: `22.43` vs `16.0`;
- higher stability: `0.836419` vs `0.668513`;
- same zero-user status;
- same diagnose status (`OK`);
- same remediation type: add route-class exclusions.

`awg3` remains a viable fallback remediation candidate but has weaker current quality metrics.

## Would Adding Exclusions Make Target Clean?

Yes, for `awg0`, based on current E10.1 evidence.

Expected readiness after metadata remediation:

```text
target=awg0
users_count_from_registry=0
users_count_from_load_state=0
interface_up_lower_up=true
diagnose_status=OK
avg_mbps=26.8167
min_mbps=22.43
stability=0.836419
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
expected_status=GO
```

The same metadata remediation would likely make `awg3` clean as well, but `awg0` is preferred because its current quality margin is larger.

## Prior Bad History

E9.3.4/E9.3.5 saw planner suggestions involving `awg3` during a transient restore sequence. That history does not prove `awg3` is unsafe, but it makes `awg0` preferable for a fresh second-canary target remediation because `awg0` avoids the previously controversial target.

## Decision

```text
remediation_candidate=awg0
fallback_candidate=awg3
remediation_required=true
remediation_safe=true_for_metadata_only_under_separate_approval
expected_target_after_remediation=awg0
expected_second_canary_readiness_after_remediation=GO_if_restore_settle_gate_remains_GO_and_checks_remain_OK
execution_allowed_now=false
```

