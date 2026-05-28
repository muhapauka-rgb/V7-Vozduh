# Block E10.1 - Zero-User Target Remediation Approval Packet

Mode: read-only / target remediation planning only.

No canary was executed. No user movement, routing mutation, policy apply, Direct/RU mutation, Trusted RU mutation, systemd mutation, registry mutation, or runtime file mutation was performed by this block.

## 1. Current Target Pool Truth

Fresh evidence was collected into:

- `docs/track7/control-plane/e10_1-evidence/current-target-pool-snapshot.txt`
- `docs/track7/control-plane/e10_1-evidence/current-state/`
- `docs/track7/control-plane/e10_1-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e10_1-evidence/current-restore-settle.json`

Runtime checks in the fresh snapshot:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Restore-settle gate remains clean from the E10 sample set:

```text
restore_settle_gate_status=GO
selected_moves_by_sample=[0,0,0]
telegram_hard_blocked_by_sample=[false,false,false]
egress_1_eligible_by_sample=[true,true,true]
execution_allowed_now=false
```

## 2. Current Target Readiness

Fresh target readiness for `candidate_user=10.7.0.11`:

```text
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
```

Target pool:

| Target | Current status | Blocker |
|---|---|---|
| `1` | NO-GO | occupied by `10.7.0.14` and `10.7.0.15`; load users=2 |
| `awg0` | NO-GO | missing `TRUSTED_RU_SENSITIVE,DIRECT_RU` exclusions |
| `awg3` | NO-GO | missing `TRUSTED_RU_SENSITIVE,DIRECT_RU` exclusions |
| `openvpn-1779388847-d2ad7c` | NO-GO | diagnose `SUSPECT` |
| `wireguard-1779454504-c43409` | NO-GO | diagnose `SUSPECT` |

## 3. AWG0/AWG3 Remediation Analysis

Both `awg0` and `awg3` are currently zero-user, UP/LOWER_UP, and diagnose OK. The blocker is metadata-only target-readiness policy:

```text
missing_exclusions=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Current quality:

```text
awg0 avg_mbps=26.8167 min_mbps=22.43 stability=0.836419
awg3 avg_mbps=23.9337 min_mbps=16.0 stability=0.668513
```

Verdict:

```text
remediation_candidate=awg0
fallback_candidate=awg3
```

`awg0` is preferred because it has better current average throughput, minimum throughput, and stability.

## 4. Direct/RU And Trusted RU Risk

Adding exclusions means:

```text
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Risk classification:

```text
direct_ru_risk=LOW_METADATA_EXCLUSION_ONLY
trusted_ru_risk=LOW_METADATA_EXCLUSION_ONLY_WITH_STALE_STATE_AWARENESS
kill_switch_risk=LOW_RECHECK_REQUIRED_AFTER_MUTATION
policy_apply_required=false
runtime_route_mutation_required=false
```

This is not a Direct/RU domain mutation and not a Trusted RU refresh. It is egress metadata that narrows route-class eligibility for `awg0`.

Trusted RU state remains stale/sensitive:

```text
trusted_ru_decision_overall=NEEDS_ATTENTION
route_class_status=NEEDS_TRUSTED_PATH
```

The proposed metadata exclusion is compatible with that risk because it prevents `awg0` from being treated as eligible for Trusted RU sensitive canary semantics.

## 5. Remediation Preview

Preview only:

```text
target_file=/opt/v7/egress/state/egress.registry
egress_id=awg0
operation=append metadata
add=exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Expected result after a separately approved bounded mutation:

```text
expected_target_after_remediation=awg0
expected_second_canary_readiness_after_remediation=GO_if_restore_settle_gate_remains_GO_and_runtime_checks_remain_OK
```

Rollback preview:

```text
rollback=restore timestamped egress.registry backup or remove awg0 exclude_route_classes metadata
policy_apply_required=false
route_or_datapath_mutation_required=false
```

## 6. Approval Decision

```text
remediation_candidate=awg0
remediation_approval_status=GO
expected_target_after_remediation=awg0
expected_second_canary_readiness_after_remediation=GO_if_fresh_checks_remain_OK
mutation_required=true
mutation_scope=/opt/v7/egress/state/egress.registry awg0 metadata only
policy_apply_required=false
direct_ru_risk=LOW_METADATA_EXCLUSION_ONLY
trusted_ru_risk=LOW_METADATA_EXCLUSION_ONLY_WITH_STALE_STATE_AWARENESS
kill_switch_risk=LOW_RECHECK_REQUIRED_AFTER_MUTATION
execution_allowed_now=false
```

This GO is not approval to mutate now. It is approval to prepare a future bounded mutation block for one metadata field on `awg0`.

## 7. Exact Next Recommended Step

Prepare a bounded runtime metadata mutation packet:

1. backup `/opt/v7/egress/state/egress.registry`;
2. update only the `awg0` row to add `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`;
3. do not run policy apply;
4. do not change routes, ip rules, nftables, Direct/RU, or Trusted RU;
5. rerun target readiness for `10.7.0.11`;
6. rerun reconcile/user-route/kill-switch/provisioning checks;
7. only then prepare a fresh second-canary approval packet.

## 8. Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```

