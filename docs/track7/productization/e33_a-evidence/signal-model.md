# E33.A Signal Model

signal_model_defined=true

## Signal Types

| Signal | Purpose | Source | Freshness | Confidence | Fail-Closed Behavior |
| --- | --- | --- | --- | --- | --- |
| TARGET_REACHABILITY | Determine whether target is reachable at all. | target-local probes, health checks. | Short TTL. | HIGH when recent and repeated. | UNKNOWN blocks positive recommendation. |
| TARGET_THROUGHPUT | Estimate target capacity/performance. | probe windows, quality samples. | Short to medium TTL. | Depends on sample count and age. | Stale throughput cannot justify movement. |
| TARGET_LATENCY | Detect latency degradation. | ping/probe telemetry. | Short TTL. | HIGH with repeated samples. | Unknown latency lowers confidence. |
| TARGET_PACKET_LOSS | Detect packet loss and instability. | probe telemetry. | Short TTL. | HIGH with repeated samples. | Unknown packet loss lowers confidence or blocks high-risk proposal. |
| SERVICE_REACHABILITY | Determine whether a service is reachable through target. | service probes per target. | Short TTL per service. | Depends on service probe reliability. | UNKNOWN service cannot be treated as OK. |
| SERVICE_LATENCY | Evaluate service-specific performance. | service probes per target. | Short TTL per service. | Depends on repeated measurements. | Stale service latency cannot justify improvement claim. |
| USER_REQUIRED_SERVICE_HEALTH | Evaluate target against user's required_services. | join of required_services and service health. | Derived from freshest inputs. | Minimum confidence of required service signals. | Missing required_services or UNKNOWN service health blocks full OK. |
| TARGET_LOAD | Avoid overloaded target. | load subsystem, target users count, capacity ledger. | Short TTL. | HIGH when sourced from current runtime state. | Unknown load blocks capacity-positive proposal. |
| INCIDENT_HISTORY | Avoid targets with recent failures. | incident log, audit records, operator notes. | Medium TTL. | MEDIUM unless incident source is authoritative. | Recent unresolved incident lowers confidence or blocks proposal. |
| OPERATOR_FEEDBACK | Include observed operator reality. | admin panel notes, operator review. | Operator-defined TTL. | Depends on source and recency. | Negative feedback blocks automatic positive recommendation. |

## Signal Aggregation Rules

- User-specific service health is mandatory when required_services exist.
- Unknown required service health is not OK.
- Global target quality cannot override required service failure.
- Stale inputs reduce confidence.
- Conflicting inputs require REVIEW_REQUIRED or observation recommendation.

## Decision

signal_model_defined=true
