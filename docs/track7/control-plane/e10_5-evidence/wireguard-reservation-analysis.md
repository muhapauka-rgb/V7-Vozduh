# E10.5 WireGuard Reservation Feasibility

Mode: read-only reservation feasibility only. No target reservation was applied.

## Reservation Candidate

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
zero_user=true
quality_ok=true
Direct_RU_exclusion_present=true
Trusted_RU_exclusion_present=true
restore_settle_gate_status=GO
runtime_checks_ok=true
```

## Feasibility

WireGuard is feasible as a reserved canary target, but reservation needs a future bounded metadata/tooling approval.

```text
wireguard_reservation_feasible=true
reservation_requires_mutation=true
mutation_scope=/opt/v7/egress/state/egress.registry wireguard metadata only
policy_apply_required=false
runtime_route_mutation_required=false
kill_switch_recheck_required=true
```

Reservation metadata alone is only safe if governance and autoswitch/readiness tooling explicitly honor it:

```text
canary_reserved=true
autoswitch_must_not_assign_production_users=true
target_readiness_may_prefer_reserved_zero_user_target=true
reservation_reversible=true
```

If current runtime autoswitch does not enforce `canary_reserved=true`, then the reservation field is governance documentation but not a hard production guard. In that case the next bounded mutation packet must include a tooling/runtime enforcement assessment before relying on the reserved state.

## Diagnose / Waiver Impact

Reservation does not by itself convert the target to clean `GO`, because the strict readiness checker still sees `diagnose=SUSPECT`.

```text
waiver_required=true
waiver_status=waiver_conditional
clean_target_possible=true
expected_second_canary_readiness_after_reservation=CONDITIONAL_GO_WITH_STALE_HANDSHAKE_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
```

The strongest path is:

1. Fix or refresh diagnose semantics so live fresh WireGuard handshake overrides stale `handshake_age_seconds=999999`.
2. Add reservation metadata in a separate bounded mutation block.
3. Prove target readiness is `GO` or explicit `CONDITIONAL` with stale-handshake waiver.
4. Generate a fresh second-canary approval packet.

## Reservation Preview

Proposed future metadata fields:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Expected rollback:

```text
remove canary_reserved/reservation_* fields from only wireguard-1779454504-c43409 row
rerun target readiness, restore-settle, reconcile, user-route, kill-switch, provisioning checks
```
