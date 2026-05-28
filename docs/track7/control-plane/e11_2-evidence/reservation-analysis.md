# E11.2 WireGuard Reservation Analysis

Reservation target:

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
proposed_canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

## Feasibility

```text
reservation_feasible=true
reservation_requires_mutation=true
mutation_scope=/opt/v7/egress/state/egress.registry WireGuard metadata only
policy_apply_required=false
routing_mutation_required=false
users_registry_mutation_required=false
kill_switch_recheck_required=true
```

WireGuard already has the required Direct/RU and Trusted RU exclusions:

```text
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Fresh runtime evidence confirms zero production users:

```text
wireguard_registry_users=0
wireguard_load_users=0
```

## Autoswitch Impact

Reservation is intended to make governance and readiness tooling treat the
egress as a canary target and prevent future production assignment once the
autoswitch/readiness semantics recognize the reservation metadata.

The reservation metadata alone should not move users, edit routes, restart
services, or apply policy. It does require post-mutation read-only checks
because it changes an authoritative runtime registry file.

## Approval Position

```text
reservation_approval_status=GO_FOR_SEPARATE_BOUNDED_METADATA_MUTATION_PACKET
direct_ru_risk=LOW_EXISTING_EXCLUSION
trusted_ru_risk=LOW_EXISTING_EXCLUSION
runtime_risk=LOW_METADATA_ONLY_WITH_CHECKER_REVALIDATION
```

The next block may prepare a bounded mutation for the single WireGuard row, but
it must not combine reservation with canary execution.
