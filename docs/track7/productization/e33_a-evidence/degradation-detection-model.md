# E33.A Degradation Detection Model

degradation_detection_defined=true

## Degradation Types

| Type | Detection Criteria | Evidence Required | Confidence | Proposal Eligibility | Fail-Closed Behavior |
| --- | --- | --- | --- | --- | --- |
| TARGET_DOWN | Target unreachable or no successful health check. | Recent target reachability probes. | HIGH with repeated failures. | Evacuation proposal may be eligible. | Unknown target state blocks positive target proposal. |
| TARGET_DEGRADED | Throughput/latency/loss below floor. | Recent quality window. | Depends on samples. | Movement proposal may be eligible if alternate better. | Stale evidence produces observation recommendation. |
| TARGET_OVERLOADED | Load/capacity/reservation pressure too high. | Runtime load, capacity, reservations. | HIGH with current runtime data. | Avoid target; maybe rebalance proposal. | Unknown load blocks positive proposal. |
| SERVICE_UNREACHABLE | Service probe fails through target. | Per-service probes. | HIGH with repeated failures. | Move affected users whose required_services include service. | Unknown service state is not OK. |
| SERVICE_DEGRADED | Service latency/error/timeout degraded. | Per-service quality samples. | MEDIUM/HIGH based on samples. | Observation or movement proposal depending criticality. | Stale evidence lowers confidence. |
| USER_REQUIRED_SERVICE_DEGRADED | User's REQUIRED/IMPORTANT services degraded on current route. | required_services plus service health. | Minimum input confidence. | Proposal eligible when alternate target improves required services. | Missing required_services blocks high-confidence proposal. |
| ROUTE_CLASS_MISMATCH | Current/proposed target violates route class or service needs. | policy/route class metadata. | HIGH if metadata current. | Proposal must go through policy. | Unknown class requires review. |
| UNKNOWN_HEALTH | Required evidence missing, stale, or contradictory. | Evidence inventory. | LOW. | Observation recommendation only. | No movement proposal as OK. |

## Decision

degradation_detection_defined=true
