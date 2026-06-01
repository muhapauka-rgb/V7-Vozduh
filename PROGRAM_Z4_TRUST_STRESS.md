# PROGRAM Z4 Trust Stress

## Objective

Evaluate trust degradation, policy downgrade, trust recovery, route class restrictions, and autonomy response.

## Live Trust And Policy

Current live planner rejects restricted targets:

- execution-only target blocked by `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`
- canary-reserved target blocked by `canary_reserved_production_assignment_blocked`
- route-class incompatible target `1` blocked by `route_class_GLOBAL_STABLE_failed`

## Stress Probe

Live-derived copy with target policy downgrade:

- label: `trust_policy_downgrade`
- target: `awg3`
- injected condition: `manual_only=1`, `reserve_only=1`, `autoswitch_allowed=false`, `canary_reserved=true`
- target blockers: `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`
- selected_moves: `0`
- decision: `no_eligible_failover_target`

## Interpretation

The planner blocks trust and policy downgrade conditions. This certifies fail-closed trust handling, not full trust recovery.

## Verdict

- trust_degradation_evaluated=true
- policy_downgrade_blocked=true
- route_class_restrictions_enforced=true
- unsafe_trust_move_blocked=true
- trust_handling_certified=true
- trust_recovery_certified=false

