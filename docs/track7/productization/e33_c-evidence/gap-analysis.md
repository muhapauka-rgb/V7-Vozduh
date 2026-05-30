# E33.C Gap Analysis

## Remaining Gaps

Routing Intelligence architecture is certified, but implementation and productization still need:

- exact confidence scoring formula;
- service probe methodology and safe probe intervals;
- canonical service catalog ownership;
- required_services storage schema finalization;
- service_health freshness TTLs;
- service affinity storage backend;
- proposal storage backend;
- proposal expiration TTL defaults;
- routing observability schema;
- operator review workflow schema;
- operator feedback decay model.

## Remaining Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| stale service health | MEDIUM | TTLs, fail-closed unknown handling, evidence refresh. |
| false service degradation | MEDIUM | repeated observations, confidence penalties, review. |
| flapping proposals | MEDIUM | cooldown, pair reversal memory, duplicate coalescing. |
| operator overtrust of proposal | MEDIUM | observability labels, governance path preview, non-executable proposal state. |
| ambiguous service catalog | MEDIUM | canonical catalog decision. |

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- exact_confidence_scoring_formula
- canonical_service_catalog_owner
- required_services_storage_schema
- service_probe_methodology
- service_health_freshness_ttl
- service_affinity_storage_backend
- proposal_storage_backend
- proposal_expiration_ttl
- flapping_cooldown_defaults
- operator_review_workflow_schema
- routing_observability_schema
- operator_feedback_decay_model
```

## Gap Decision

No gap invalidates certification. Gaps are implementation/product decisions for the next program.
