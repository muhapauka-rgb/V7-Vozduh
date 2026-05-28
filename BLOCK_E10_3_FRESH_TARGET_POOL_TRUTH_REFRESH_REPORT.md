# V7 Vozduh — BLOCK E10.3 Fresh Target Pool Truth Refresh

Mode: read-only / target pool truth only.

## Executive Truth

E10.3 refreshed target-pool truth after the aborted E10.2 awg0 metadata mutation. No mutation was performed.

The E10.2 assumption `awg0_zero_user=false` was true at that pre-gate, but it is no longer true in the fresh E10.3 snapshot. Current truth:

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
selected_target=NONE
second_canary_readiness=NO-GO
execution_allowed_now=false
```

Current zero-user targets exist, but none is clean:

- `awg0`: zero-user, diagnose OK, but quality below floor and missing Direct/RU + Trusted RU exclusions.
- `awg3`: zero-user, diagnose OK, but quality below floor and missing Direct/RU + Trusted RU exclusions.
- `openvpn-1779388847-d2ad7c`: zero-user, but diagnose SUSPECT and quality below floor.
- `wireguard-1779454504-c43409`: zero-user, quality OK, but diagnose SUSPECT.

## Runtime Snapshot

Evidence:

- `docs/track7/control-plane/e10_3-evidence/fresh-global-runtime-snapshot.txt`
- `docs/track7/control-plane/e10_3-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e10_3-evidence/current-restore-settle.json`
- `docs/track7/control-plane/e10_3-evidence/process-guard.txt`

Fresh hashes:

```text
users.registry=58aaeb0d4cb2781524c573fb58080af2b5aed714c9a6ac79d0c2118bf899546d
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Runtime checks in E10.3 samples:

```text
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
autoswitch_manual_apply_observed=false
```

## Current Distribution

Registry-enabled users by egress:

| Egress | Users |
|---|---|
| `1` | `10.0.0.2`, `10.0.0.3`, `10.0.0.6`, `10.7.0.2`, `10.7.0.3`, `10.7.0.4` |
| `vless` | `10.7.0.5`, `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`, `10.7.0.11`, `10.7.0.12`, `10.7.0.13`, `10.7.0.14`, `10.7.0.15` |
| `awg0` | none |
| `awg3` | none |
| `openvpn-1779388847-d2ad7c` | none |
| `wireguard-1779454504-c43409` | none |

## Target Pool Verdict

| Target | Status | Reason |
|---|---|---|
| `awg0` | NO-GO | zero-user and diagnose OK, but `min_mbps=1.78`, `stability=0.0650188`, and missing Direct/RU + Trusted RU exclusions. |
| `awg3` | NO-GO | zero-user and diagnose OK, but `min_mbps=1.13`, `stability=0.0322427`, and missing Direct/RU + Trusted RU exclusions. |
| `1` | NO-GO | occupied by six registry/load-state users. |
| `openvpn-1779388847-d2ad7c` | NO-GO | zero-user, but `diagnose=SUSPECT`, `min_mbps=8.83`, `stability=0.1641`. |
| `wireguard-1779454504-c43409` | NO-GO clean; conditional waiver candidate | zero-user and quality OK, but `diagnose=SUSPECT`. Requires separate waiver packet before any canary. |

## Why AWG0/AWG3 Became Occupied

E10.3 evidence shows AWG occupation was transient autoswitch production behavior. The current state has both `awg0` and `awg3` at zero users, but switch-history and planner safety data show recent failover/rebalance through those egresses.

This means:

- E10.2 aborted correctly because its live pre-gate saw awg0 occupied.
- E10.3 does not resume E10.2 mutation, because target truth changed again.
- AWG targets must be treated as live production autoswitch candidates, not isolated stable canary targets.
- Metadata remediation alone is not enough while quality floor is failed.

## OpenVPN / WireGuard Review

OpenVPN remains a poor waiver candidate because it is both `SUSPECT` and currently below quality floor.

WireGuard is the best conditional target if the operator wants a target-diversity mechanics canary, because it is zero-user and quality passes floor. However:

```text
wireguard_status=ZERO_USER_CONDITIONAL_SUSPECT_QUALITY_OK_STALE_HANDSHAKE
waiver_required=true
waiver_approved_by_E10_3=false
```

## Path Selection

Safest next path:

```text
best_current_target_path=E_PAUSE_CANARY_AND_FOCUS_ON_TARGET_POOL_GOVERNANCE_OR_CAPACITY
```

Conditional alternative:

```text
prepare_wireguard_stale_handshake_waiver_packet
```

This is less safe than waiting for a clean target, but safer than using occupied target `1`, low-quality AWG targets, or OpenVPN.

Do not repeat E10.2 metadata mutation now. `awg0` is zero-user again, but it is still NO-GO due quality floor and missing exclusions; metadata-only remediation would not produce a clean target.

## Required Answers

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
best_current_target_path=E_PAUSE_CANARY_AND_FOCUS_ON_TARGET_POOL_GOVERNANCE_OR_CAPACITY
awg0_status=ZERO_USER_NO_GO_LOW_QUALITY_MISSING_EXCLUSIONS
awg3_status=ZERO_USER_NO_GO_LOW_QUALITY_MISSING_EXCLUSIONS
openvpn_status=ZERO_USER_NO_GO_SUSPECT_LOW_QUALITY
wireguard_status=ZERO_USER_CONDITIONAL_SUSPECT_QUALITY_OK_STALE_HANDSHAKE
second_canary_readiness=NO-GO
recommended_next_step=prepare_target_pool_governance_or_separate_wireguard_waiver_packet; do not execute canary
execution_allowed_now=false
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
