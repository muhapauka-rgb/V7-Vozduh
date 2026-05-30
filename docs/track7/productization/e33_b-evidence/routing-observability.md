# E33.B Routing Observability

routing_observability_defined=true

## Operator Questions

Operators need to answer:

- Which users are affected?
- Which services are degraded?
- Which current targets are failing?
- Which candidate targets look better?
- Why is Routing Intelligence proposing action or no action?
- What confidence does the proposal have?
- What evidence is missing?
- What is the next safe action?

## Required Views

| View | Contents |
| --- | --- |
| Active Degradations | target, service, affected users, severity, age, confidence. |
| User-Specific Health | per user required_services, current target status, candidate target status. |
| Proposal Queue | proposals, status, confidence, review requirement, expiration. |
| Evidence Drawer | service probes, target quality, incident history, affinity, flapping state. |
| Governance Path Preview | batch/policy/capacity/concurrency/scheduling/recheck status placeholders. |
| Failure Mode Panel | unknowns, stale data, conflicts, false-positive risk. |

## Display Semantics

| State | Operator Meaning | Safe Action |
| --- | --- | --- |
| USER_TARGET_OK | User's required services are healthy on target. | No action or monitor. |
| USER_TARGET_DEGRADED | Some important or global quality signals are degraded. | Observe or review proposal. |
| USER_TARGET_FAIL | Required service or target fails. | Review evacuation/movement proposal. |
| USER_TARGET_UNKNOWN | Required evidence missing or stale. | Collect evidence; do not approve as OK. |

## Auditability

Every visible proposal must expose:

- evidence version;
- confidence rationale;
- required_services used;
- service health freshness;
- proposal generation time;
- expiration time;
- governance compatibility status.

routing_observability_defined=true
