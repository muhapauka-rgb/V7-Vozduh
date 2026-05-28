# E11.11 Reservation Enforcement Review

reservation_review_completed=true

reservation_enforcement_complete=true

## Coverage Matrix

| Path | Evidence | Verdict |
|---|---|---|
| Planner destination selection | `current-autoswitch-plan.pretty.json` shows WireGuard candidate blocked with `canary_reserved_production_assignment_blocked` for production decisions | PASS |
| Apply selection | `summary.selected_moves=0`; apply has no selected moves to execute | PASS |
| Failover | `v7-users-autoswitch` gates reservation for every non-current candidate purpose, including failover | PASS |
| Planned move | Same reservation gate blocks canary-reserved targets outside explicit user-switch | PASS |
| Rebalance | Rebalance candidates are built through the same candidate gate; canary-reserved targets are ineligible | PASS |
| Current user already on reserved target | Code holds current reserved user and marks separate drain approval; E11.9 drain already cleared existing users | PASS |
| Dynamic load pool | `_healthy_for_load` excludes `egress.canary_reserved` from working pool | PASS |
| Target readiness | Readiness allows reserved target as clean canary target, not production target | PASS |
| Restore cycles | E11.10 rollback plus E11.11 live state retained `canary_reserved=true` and zero WireGuard users | PASS |
| Hidden assignment paths | E11.11 process scan found no `v7-user-switch`/`v7-routing-sync`; governance still forbids these without approval | PASS_WITH_LINEAGE_WATCH |

## Current Reserved Target State

- target: `wireguard-1779454504-c43409`
- users: `0`
- registry: `canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance`
- readiness: `GO` for governed canary target use
- production assignment: blocked

## Remaining Gaps

No runtime reservation enforcement gap remains in `v7-users-autoswitch`.

The remaining risk is operational, not logic: direct manual tools such as `v7-user-switch` can still bypass reservation by design when explicitly invoked. This is required for governed canary movement, but mini-cohort must use an exact movement manifest and must not invoke routing-sync or autoswitch apply.
