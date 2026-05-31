# Convergence F Deferred API Decision

Project: V7 Vozduh
Block: Convergence F

## Routes Reviewed

- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`

## Decision

Decision: Merge into the canonical execution preview API family.

## Implementation

- Added viewer role entries for all three routes.
- Added read-only response wrappers:
  - `execution_outcome_preview_response`
  - `execution_blast_radius_response`
  - `execution_service_impact_response`
- Routed all three paths through the existing authenticated GET handler.
- Reused existing derived helpers:
  - `execution_candidate_outcome_for_draft`
  - `execution_blast_radius_for_draft`
  - `execution_service_impact_for_draft`
- Added the surfaces to the existing Execution drawer family.

## Safety

No execution engine, runtime hook, user movement, routing mutation, autoswitch apply, or new store
was introduced.

deferred_api_decision_complete=true
