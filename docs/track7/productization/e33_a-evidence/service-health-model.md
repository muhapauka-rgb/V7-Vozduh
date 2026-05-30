# E33.A Service Health Model

service_health_model_defined=true

## Service Health Record

For each service on each target:

```text
target_id
service_id
reachable
latency_ms
error_rate
timeout_rate
status
confidence
last_checked
evidence_source
evidence_hash
```

## Service Health States

| State | Meaning | Proposal Impact |
| --- | --- | --- |
| SERVICE_OK | Service is reachable and within latency/error floors. | Can support positive fit. |
| SERVICE_DEGRADED | Service works but is below quality floor. | Lowers confidence; may trigger proposal away from current target. |
| SERVICE_FAIL | Service unreachable or unacceptable error/timeout rate. | Blocks user-target OK if service is REQUIRED. |
| SERVICE_UNKNOWN | No fresh or trustworthy evidence. | Cannot be treated as OK. |

## Evidence Sources

Allowed evidence sources:

- target-local service probes;
- synthetic service reachability checks;
- operator-confirmed incident state;
- user-specific telemetry when available;
- audit-backed prior observations.

## Confidence Rules

Confidence depends on:

- freshness;
- repeated samples;
- probe reliability;
- consistency across sources;
- incident history.

## Fail-Closed Behavior

SERVICE_UNKNOWN and stale service evidence cannot justify a positive movement proposal.

SERVICE_FAIL for a REQUIRED service blocks USER_TARGET_OK.

## Decision

service_health_model_defined=true
