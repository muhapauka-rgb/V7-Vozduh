# E33.B Final Operations Decision

routing_decision_operations_defined=true
required_services_influence_preserved=true
governance_compatible=true

## Decision Summary

E33.B defines Routing Decision Operations.

Routing Intelligence can now produce structured decisions, service-affinity rankings, proposals, confidence levels, human-review requirements, observability outputs, and failure-mode outcomes.

Routing Intelligence remains non-authoritative for execution. It may propose but cannot mutate runtime.

## Certified Operations

```text
routing_decision_model_defined=true
service_affinity_model_defined=true
proposal_engine_defined=true
confidence_model_defined=true
flapping_protection_defined=true
human_review_model_defined=true
routing_observability_defined=true
routing_failure_modes_defined=true
required_services_influence_preserved=true
governance_compatible=true
routing_decision_operations_defined=true
```

## Core Rules

- required_services remain first-class inputs.
- Service affinity can rank targets but cannot move users.
- A target must be evaluated per user and per required service.
- Unknown service health is not OK.
- Low confidence produces OBSERVE or REVIEW_REQUIRED.
- Every executable proposal must become a governed batch.
- Governance Control Plane remains the only path toward execution.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- exact_confidence_scoring_formula
- service_affinity_storage_backend
- proposal_storage_backend
- proposal_expiration_ttl
- flapping_cooldown_defaults
- operator_review_workflow_schema
- routing_observability_schema
```

## Remaining Open Questions

- What exact numeric confidence formula should be used?
- Which service categories require longer observation before movement?
- How long should duplicate proposals be coalesced?
- Which proposal types require dual confirmation?
- How should operator feedback decay over time?

recommended_next_block=E33.C_ROUTING_INTELLIGENCE_CERTIFICATION
