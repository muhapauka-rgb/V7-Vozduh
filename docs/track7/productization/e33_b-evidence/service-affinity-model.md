# E33.B Service Affinity Model

service_affinity_model_defined=true
required_services_influence_preserved=true

## Purpose

Service affinity describes which targets are preferable for a service or service category. It influences Routing Intelligence proposals but cannot directly move users.

## Affinity Inputs

| Input | Meaning | Authority |
| --- | --- | --- |
| required_services | User-specific mandatory service list from admin/policy sources. | User/service preference metadata. |
| service_health | Per-service, per-target health and quality. | Service matrix and probes. |
| target_quality | Global target performance and stability. | Capacity/quality telemetry. |
| route_class | Service-derived or policy-derived route category. | Policy and RI derivation. |
| operator_feedback | Manual signal that a service-target pairing is good or bad. | Operator evidence, never direct execution authority. |
| incident_history | Prior service or target failures. | Audit/incident store. |

## Affinity States

| State | Meaning | Proposal Impact |
| --- | --- | --- |
| AFFINITY_STRONG | Target repeatedly performs well for service. | Raises confidence and expected benefit. |
| AFFINITY_WEAK | Target has limited but positive evidence. | May support review-required proposals. |
| AFFINITY_NEGATIVE | Target repeatedly fails or degrades service. | Blocks high-confidence proposal for users requiring service. |
| AFFINITY_UNKNOWN | Evidence missing or stale. | Observation or review, not direct positive proposal. |
| AFFINITY_CONFLICT | Signals disagree. | REVIEW_REQUIRED. |

## Required Services Influence

For a user with required_services:

```text
user_required_services + service_affinity + service_health -> user_specific_target_fit
```

Rules:

- REQUIRED service failure blocks target fit for that user.
- IMPORTANT service degradation lowers confidence and may require review.
- OPTIONAL service degradation may lower score but should not block alone.
- If a service is unknown for a target, the target cannot receive USER_TARGET_OK for a user requiring that service.
- Service affinity can prefer one target over another only after governance compatibility remains intact.

## Aging and Invalidation

Affinity ages independently per service and target.

Invalidate or downgrade affinity when:

- service probe freshness expires;
- target quality becomes STALE, DEGRADED, EXPIRED, or REVOKED;
- incident history shows unresolved failure;
- operator marks service-target pairing as unsafe;
- repeated movement/rollback evidence contradicts affinity.

## Boundary

Affinity may:

- increase proposal confidence;
- explain why a target is preferred;
- rank candidate targets.

Affinity may not:

- execute autoswitch;
- bypass policy;
- bypass capacity;
- bypass execution-time recheck;
- override required_services failure.

service_affinity_model_defined=true
