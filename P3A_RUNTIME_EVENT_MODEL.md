# P3.A Runtime Event Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Event Principle

P3.A normalizes existing events. It does not create a new runtime event stream and does not register runtime hooks.

## Normalized Event Fields

| Field | Meaning |
| --- | --- |
| `event_id` | Stable derived identifier from source, timestamp and source record key. |
| `source` | Original source file/API/tool family. |
| `source_ref` | Path, record key or existing event id. |
| `observed_at` | Time the source event was observed or recorded. |
| `event_type` | Normalized type. |
| `severity` | `INFO`, `WARN`, `BLOCKING`, `CRITICAL`. |
| `subject` | Service, route, candidate, approval, contract or runtime area. |
| `evidence_refs` | References to canonical evidence. |
| `source_hash` | Hash of the source payload where available. |
| `retention_class` | Retention category inherited from source. |

## Event Types

| Event type | Meaning |
| --- | --- |
| `HEALTH_CHANGE` | Service or runtime health changed. |
| `CHANNEL_DEGRADATION` | A required communication or routing channel degraded. |
| `REQUIRED_SERVICE_FAILURE` | Required service is missing, failed or stale. |
| `CAPACITY_PRESSURE` | Load/capacity indicators affect readiness. |
| `TRUST_CHANGE` | Trusted RU or runtime trust evidence changed. |
| `POLICY_CHANGE` | Policy or authority reference changed. |
| `SELECTED_MOVES_PRESENT` | Existing selected moves exist and must be considered. |
| `RESTORE_BARRIER_CHANGE` | Restore barrier or rollback safety changed. |
| `HIDDEN_MOVEMENT` | Evidence suggests movement not represented by the candidate. |
| `EXECUTION_CONTRACT_CHANGE` | Existing execution contract preview changed. |
| `AUDIT_ACTION` | Operator/admin audit action exists. |
| `ROUTING_TRUTH_CHANGE` | Route truth or user-flow evidence changed. |

## Source Mapping

| Source family | Event mapping |
| --- | --- |
| Service matrix and sentinel state | `HEALTH_CHANGE`, `REQUIRED_SERVICE_FAILURE`, `CHANNEL_DEGRADATION` |
| Egress summaries | `CAPACITY_PRESSURE`, `CHANNEL_DEGRADATION` |
| Trusted RU diagnostic/decision | `TRUST_CHANGE`, `ROUTING_TRUTH_CHANGE` |
| Audit logs | `AUDIT_ACTION`, `POLICY_CHANGE` |
| Switch history | `SELECTED_MOVES_PRESENT`, `HIDDEN_MOVEMENT` |
| Restore barrier | `RESTORE_BARRIER_CHANGE` |
| Execution contracts/events | `EXECUTION_CONTRACT_CHANGE`, `AUDIT_ACTION` |

## Runtime Event Verdict

The event model is derived-only and does not introduce a new event bus.

