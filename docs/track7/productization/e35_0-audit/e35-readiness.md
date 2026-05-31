# E35.0 Readiness Review

## Confirmed Assumptions

- Organizations exist.
- Groups exist.
- Organizations can belong to groups.
- Groups can carry route policy.
- Required services are selectable per user in admin.
- Required services are stored and evaluated against service matrix.
- Service matrix tracks channel/service health.
- Proposals can reference required services and recommend operator review.
- Channel suitability uses more than speed.
- Current user channel is persisted in `users.registry`.

## Wrong / Unsafe Assumptions

- Selecting required services does not currently guarantee access by itself.
- Required services do not automatically move users.
- Required services are not yet a universal hard gate for all movement paths.
- `current=<egress>` is not the same as an explicit pin.
- A separate per-user AUTO/PINNED/MANUAL routing mode was not found.
- Organization/group constraints are not yet proven as universal channel allow/deny enforcement.

## Reuse Candidates

E35 should reuse:

- Identity DB organizations/groups.
- `groups.route_policy`.
- `SERVICE_PREFS_FILE` and `/api/actions/service-preferences-update`.
- Service matrix and route fitness.
- Proposal and Evidence surfaces.
- Channel metadata: role, service tags, exclude route classes, manual/reserve flags, organization scope.
- Policy and autoswitch guarded semantics.

## Required Implementation Areas

E35 should implement or formalize:

- explicit per-user routing control mode
- preferred/pinned channel semantics
- group/channel constraints as hard suitability gates
- required-service guarantee semantics
- admin copy that distinguishes recommendation from guarantee
- unified suitability verdict per user/channel pair
- execution-time recheck gate for required services and group constraints

## Readiness Verdict

e35_readiness_review_complete=true
e35_can_start=true
blockers=none_for_architecture_or_planning
implementation_gap_exists=true

## Recommended Next Block

E35_1_REQUIRED_SERVICES_AND_ROUTING_CONTROL_MODEL
