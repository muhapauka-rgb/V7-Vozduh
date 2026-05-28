# E19 Execution Risk Review

## Scope

E19 reviews future mutating execution UX without enabling execution.

LIVE_RUNTIME_MUTATION=FORBIDDEN
REAL_EXECUTION=FORBIDDEN
USER_MOVEMENT=FORBIDDEN
ROUTING_MUTATION=FORBIDDEN
CANARY_OR_COHORT_EXECUTION=FORBIDDEN

## Execution Danger Map

danger_user_switch=true
danger_autoswitch_apply=true
danger_restore_apply=true
danger_emergency_containment=true
danger_route_sync=true
danger_service_restart=true
danger_kill_switch_mutation=true
danger_direct_ru_refresh=true
danger_trusted_ru_refresh=true

The dangerous operations remain outside the Operator namespace. E19 does not add a POST endpoint or a runtime action endpoint.

## Future UI Risks

- one-click movement could hide blast radius;
- stale selected_moves could be approved accidentally;
- generation mismatch could replay an old movement set;
- rollback manifest could drift from approved users;
- delayed movement could appear after restore/apply;
- same operator could approve and confirm without independent review;
- stale evidence could look fresh without explicit labels;
- emergency containment could become a panic button without lineage.

## Replay / Approval Weaknesses Addressed

- Execution contracts now require generation ID.
- Selected-move fingerprint is visible.
- Runtime snapshot hash is required by contract.
- Approval expiry is visible.
- Same-actor dual confirmation is explicitly forbidden.
- Scope expansion is denied by contract.
- Stale evidence invalidates future execution.
- Rollback manifest is bound to execution preview.

## Verdict

execution_risk_review_completed=true
future_ui_risks_identified=true
runtime_mutation_surface_added=false
execution_allowed_now=false
