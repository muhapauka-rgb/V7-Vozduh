# BLOCK E9.2.5 - OpenVPN Waiver Canary Approval Packet

Mode: read-only / waiver approval packet only.

## Summary

E9.2.5 prepares a conditional approval packet for the OpenVPN target. It does not execute canary.

```text
candidate_user=10.7.0.14
current_egress=vless
target_egress=openvpn-1779388847-d2ad7c
rollback_target=vless
waiver_name=openvpn_idle_suspect_mechanics_canary
waiver_required=true
waiver_acceptable=true
approval_status=CONDITIONAL
target_zero_user=true
target_health_status=CONDITIONAL_IDLE_SUSPECT
target_diagnose_status=SUSPECT
rollback_feasible=true
blast_radius=one_user
should_E9_3_execute_now=false
execution_allowed_now=false
```

This packet explicitly avoids:

- occupied target `1`;
- `awg0` / `awg3` below quality floor;
- any clean-GO claim for OpenVPN.

## Evidence

| Artifact | Path |
|---|---|
| OpenVPN target snapshot | `docs/track7/control-plane/e9_2_5-evidence/openvpn-target-snapshot.txt` |
| candidate refresh | `docs/track7/control-plane/e9_2_5-evidence/candidate-refresh.md` |
| waiver definition | `docs/track7/control-plane/e9_2_5-evidence/waiver-definition.md` |
| forward preview | `docs/track7/control-plane/e9_2_5-evidence/forward-preview.json` |
| rollback preview | `docs/track7/control-plane/e9_2_5-evidence/rollback-preview.json` |

## Waiver

```text
waiver_name=openvpn_idle_suspect_mechanics_canary
waiver_scope=one_user_only
target=openvpn-1779388847-d2ad7c
accepted_risk=diagnose SUSPECT caused by idle/stale handshake, not proven live failure
```

This is not a clean target canary. It is a mechanics + target-diversity canary under explicit idle-SUSPECT waiver.

The waiver only accepts this condition:

```text
target_zero_user=true
interface_state=UP,LOWER_UP
quality_floor=acceptable
diagnose=SUSPECT
diagnose_detail=handshake_age_seconds=999999
```

The waiver does not accept kill-switch failure, route-check failure, reconcile failure, provisioning failure, hidden user-switch/routing-sync, target interface down, registry drift, other user movement, rollback uncertainty, or any target diagnose change from idle `SUSPECT` to a non-stale failure.

## Forward Preview

Future command, not executed in E9.2.5:

```text
v7-user-switch 10.7.0.14 openvpn-1779388847-d2ad7c
```

Expected forward changes:

```text
users.registry: 10.7.0.14 current=vless -> current=openvpn-1779388847-d2ad7c
table 1012: default dev tun0 -> default dev v7edb0c189291
switch-history: one entry for 10.7.0.14 vless -> openvpn-1779388847-d2ad7c
blast_radius=one_user
```

Preview artifact reports:

```text
mutation=false
runtime_commands_executed=false
target_interface=v7edb0c189291
table=1012
errors=[]
```

## Rollback Preview

Future command, not executed in E9.2.5:

```text
v7-user-switch 10.7.0.14 vless
```

Expected rollback changes:

```text
users.registry: 10.7.0.14 current=openvpn-1779388847-d2ad7c -> current=vless
table 1012: default dev v7edb0c189291 -> default dev tun0
switch-history: one rollback entry for 10.7.0.14
```

## Future E9.3 Gates

Before any live switch:

- `v7-reconcile-check OK`;
- `v7-user-route-check OK`;
- `v7-killswitch-check OK`;
- `v7-provisioning-reconcile-check OK`;
- candidate still `current=vless table=1012 enabled=1`;
- target OpenVPN zero-user by registry/load-state;
- target interface present and `UP,LOWER_UP`;
- OpenVPN diagnose may remain `SUSPECT` only if stale-idle reason is unchanged;
- no active `v7-user-switch`, `v7-routing-sync`, or autoswitch process;
- autoswitch planner/apply authority held;
- rollback command prepared;
- operator explicitly accepts `openvpn_idle_suspect_mechanics_canary`.

## Approval Status

```text
approval_status=CONDITIONAL
clean_target=false
waiver_required=true
waiver_acceptable=true
execution_allowed_now=false
```

This packet makes E9.3 discussable as a waiver canary. It does not make E9.3 executable.

## Exact Next Recommended Step

Request a bounded live E9.3 approval explicitly naming:

```text
candidate_user=10.7.0.14
target_egress=openvpn-1779388847-d2ad7c
rollback_target=vless
accepted_waiver=openvpn_idle_suspect_mechanics_canary
```

That future request must include fresh pre-canary read-only evidence and the same quiet-window hold model used in E9.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
