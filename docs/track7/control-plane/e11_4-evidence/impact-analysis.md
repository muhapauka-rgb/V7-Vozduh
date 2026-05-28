# E11.4 Impact Analysis

## Runtime Impact

```text
diagnose_affects_real_runtime=false
diagnose_affects_target_readiness_only=false
```

The diagnose state does not directly prove datapath failure. It does, however, affect more than the second-canary readiness checker:

- strict target readiness rejects `diagnose=SUSPECT`;
- autoswitch planner eligibility rejects `severity_SUSPECT`;
- dynamic healthy-channel accounting can treat the target as unavailable.

So the impact is control-plane eligibility, not direct packet-plane failure.

## Operational Risk

```text
stale_handshake_operational_risk=LOW_DATAPATH_MEDIUM_GOVERNANCE_ATTRIBUTION
```

Datapath risk is low when all waiver preconditions are freshly true:

- target is zero-user;
- interface is `UP,LOWER_UP`;
- live `wg show` handshake is fresh;
- route evidence is sane;
- quality remains above floor;
- Direct/RU and Trusted RU exclusions are present;
- restore-settle gate is `GO`;
- reconcile/user-route/kill-switch/provisioning checks pass.

Governance risk is medium because a strict checker and autoswitch planner still see the target as `SUSPECT`. A canary on this target without either a fix or a documented waiver would blur attribution: any failure could be argued as knowingly bypassing a control-plane red signal.

## Production User Risk

WireGuard is currently reserved and zero-user. Production users are not assigned there. Because autoswitch also treats `severity_SUSPECT` as an eligibility blocker, the current bug is more likely to prevent WireGuard from being used than to move users onto it.

If the diagnose is wrong and a one-user canary is executed under waiver, the blast radius remains one approved user with explicit rollback. The failure mode would be target datapath failure for that one user, not broad autoswitch movement, provided staged restore and restore-settle gates are preserved.

## Target Readiness Impact

Current strict readiness remains:

```text
selected_target=NONE
second_canary_readiness=NO-GO
wireguard_blocker=diagnose SUSPECT
```

Expected readiness outcomes:

```text
after_diagnose_fix=GO_IF_FRESH_RUNTIME_GATES_REMAIN_OK
with_explicit_stale_handshake_waiver=CONDITIONAL
without_fix_or_waiver=NO-GO
```

