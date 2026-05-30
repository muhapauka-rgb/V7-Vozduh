# E33.A Final Foundation Decision

routing_intelligence_foundation_defined=true
required_services_integrated=true

## Decision Summary

E33.A defines Routing Intelligence Foundation.

Routing Intelligence answers why a movement should be proposed. Governance Control Plane answers whether the proposal can be safely executed.

## Certification Markers

```text
governance_intake_loaded=true
signal_model_defined=true
required_services_model_defined=true
service_health_model_defined=true
target_quality_model_defined=true
user_specific_health_model_defined=true
degradation_detection_defined=true
proposal_boundary_defined=true
required_services_integrated=true
governance_compatible=true
routing_intelligence_foundation_defined=true
```

## Core Decisions

- required_services are first-class Routing Intelligence input.
- Target quality must be evaluated per user and per required service.
- Global target OK does not imply user-specific OK.
- SERVICE_UNKNOWN is not OK.
- Missing required_services produces USER_TARGET_UNKNOWN, not OK.
- Routing Intelligence may propose but cannot mutate runtime.
- Every proposal must enter Governance Control Plane.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- required_services_storage_schema
- canonical_service_catalog_owner
- service_probe_methodology
- service_health_freshness_ttl
- confidence_scoring_formula
- operator_feedback_schema
- proposal_storage_backend
- routing_intelligence_observability_schema
```

## Remaining Open Questions

- Who owns canonical service identifiers?
- What freshness TTL is required per service category?
- How are service probes performed without creating provider side effects?
- How should operator feedback affect confidence over time?
- Which proposal confidence threshold requires human review?

## Final Decision

routing_intelligence_foundation_defined=true

recommended_next_block=E33.B_ROUTING_DECISION_OPERATIONS
