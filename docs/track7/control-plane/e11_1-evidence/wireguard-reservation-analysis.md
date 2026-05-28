# E11.1 WireGuard Reservation Feasibility

Mode: read-only feasibility design only.

## Feasibility Verdict

```text
wireguard_reservation_feasible=true
reservation_requires_mutation=true
mutation_scope=/opt/v7/egress/state/egress.registry wireguard metadata only
policy_apply_required=false
runtime_route_mutation_required=false
Direct_RU_risk=low_existing_exclusion
Trusted_RU_risk=low_existing_exclusion
kill_switch_recheck_required=true
```

WireGuard can be safely proposed as a reserved target because:

- it has zero assigned users by registry and load-state;
- it already excludes `DIRECT_RU` and `TRUSTED_RU_SENSITIVE`;
- interface, route, NAT/MSS, and live handshake evidence are present;
- current autoswitch planner selected no moves;
- runtime reconcile/user-route/kill-switch/provisioning checks are OK.

## What Reservation Would Change

Future reservation would add metadata only:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Expected immediate runtime effect:

```text
route_mutation=false
users.registry_mutation=false
policy_apply=false
Direct_RU_mutation=false
Trusted_RU_mutation=false
```

## Important Constraint

Reservation metadata is not enough unless the runtime and governance tools honor it:

```text
autoswitch_must_not_assign_production_users_to_reserved_target=true
target_readiness_must_prefer_reserved_zero_user_target=true
reservation_must_be_reversible=true
```

If current autoswitch does not enforce `canary_reserved=true`, then reservation is only an annotation and should not be used as a hard guard until a separate tooling/policy proof exists.

## Readiness Impact

```text
expected_target_readiness_after_reservation=CONDITIONAL_WITH_STALE_HANDSHAKE_WAIVER_OR_GO_AFTER_DIAGNOSE_SEMANTICS_FIX
expected_second_canary_readiness_after_reservation=CONDITIONAL
```

Reservation preserves clean attribution only when combined with either:

1. a diagnose semantics fix/refresh that changes WireGuard from `SUSPECT` to clean; or
2. an explicit stale-handshake waiver for one-user canary mechanics.
