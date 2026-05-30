# BLOCK E33.A Routing Intelligence Foundation Report

e33_a_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

routing_intelligence_foundation_defined=true

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

## Summary

E33.A defines Routing Intelligence Foundation.

Routing Intelligence answers why a movement should be proposed. It does not execute movement, mutate runtime, change route tables, apply autoswitch, bypass governance, or consume packets.

The admin-panel `required_services` list is now a first-class Routing Intelligence input. Target quality must be evaluated for each user's required services, not only as abstract global target health.

## Required Services Rule

If a user has required_services, Routing Intelligence must evaluate candidate target quality against those services.

If required_services are missing, Routing Intelligence must not assume all services are OK.

```text
required_services_integrated=true
```

## User-Specific Health Rule

A target can be globally OK but user-specific NOT_OK.

Example:

```text
user=10.7.0.11
required_services=["youtube","telegram","instagram"]
target=A
youtube=SERVICE_OK
telegram=SERVICE_FAIL
instagram=SERVICE_OK
user_specific_health=USER_TARGET_FAIL
```

## Proposal Boundary

Routing Intelligence may output:

- movement proposal;
- evacuation proposal;
- rebalance proposal;
- no-action recommendation;
- observation recommendation.

Routing Intelligence may not:

- mutate runtime;
- move users;
- change route tables;
- directly apply autoswitch;
- bypass policy;
- bypass capacity;
- bypass batch;
- bypass concurrency;
- bypass scheduling;
- bypass execution-time recheck.

## Governance Path

Every movement proposal must enter:

```text
Batch -> Policy -> Capacity -> Concurrency -> Scheduling -> Execution-Time Recheck -> Execution
```

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

recommended_next_block=E33.B_ROUTING_DECISION_OPERATIONS

## Evidence Files

- `docs/track7/productization/e33_a-evidence/governance-intake.md`
- `docs/track7/productization/e33_a-evidence/signal-model.md`
- `docs/track7/productization/e33_a-evidence/required-services-model.md`
- `docs/track7/productization/e33_a-evidence/service-health-model.md`
- `docs/track7/productization/e33_a-evidence/target-quality-model.md`
- `docs/track7/productization/e33_a-evidence/user-specific-health-model.md`
- `docs/track7/productization/e33_a-evidence/degradation-detection-model.md`
- `docs/track7/productization/e33_a-evidence/proposal-boundary-model.md`
- `docs/track7/productization/e33_a-evidence/governance-compatibility.md`
- `docs/track7/productization/e33_a-evidence/final-foundation-decision.md`
- `docs/track7/productization/e33_a-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
