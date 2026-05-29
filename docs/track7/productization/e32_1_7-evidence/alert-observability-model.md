# E32.1.7 Alert And Observability Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

alert_observability_model_defined=true

## Alert Mapping

| Failure Mode | Alert | Severity | Operator Copy |
| --- | --- | --- | --- |
| CAPACITY_STALE | CAPACITY_STALE | Warning | "Capacity is stale. Forward movement blocked until refresh." |
| CAPACITY_DEGRADED | CAPACITY_DEGRADED | Critical | "Capacity degraded. Forward movement blocked; rollback/containment may remain available." |
| CAPACITY_EXPIRED | CAPACITY_EXPIRED | Critical | "Capacity expired. Full recertification required." |
| CAPACITY_REVOKED | CAPACITY_REVOKED | Critical | "Capacity revoked. Incident review required; no forward movement." |
| CAPACITY_UNKNOWN | CAPACITY_UNKNOWN | Warning | "Capacity unknown. Inspect metadata before use." |
| CAPACITY_CONFLICT | CAPACITY_CONFLICT | Critical | "Capacity metadata conflict. Reconcile before execution." |
| CAPACITY_EVIDENCE_MISSING | CAPACITY_EVIDENCE_MISSING | Critical | "Certification evidence missing. Reconstruct or recertify." |
| CAPACITY_CONFIDENCE_DROP | CONFIDENCE_DROP | Warning/Critical | "Confidence dropped below required threshold." |
| CAPACITY_POLICY_CAP_EXCEEDED | POLICY_CAP_EXCEEDED | Warning | "Requested batch exceeds active policy cap." |
| CAPACITY_RESERVATION_CONFLICT | RESERVATION_CONFLICT | Critical | "Capacity reservation conflict. Scheduler admission denied." |

## Display Requirements

Every alert must show:

- failure mode;
- current status;
- blocked action;
- allowed containment action;
- next safe action;
- evidence/source link.

## Alert Suppression

Alerts that block execution must not be suppressed. They may be grouped by target but must remain visible in target details and scheduler admission decisions.

