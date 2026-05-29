# E32.1.6 Final Observability Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_observability_model_defined=true

## Final Model

Capacity observability must show:

- what is certified;
- what is currently eligible;
- what is blocked;
- why it is blocked;
- what evidence supports the state;
- what action is safe next.

## Required Dashboard Sections

- Target Summary
- Capacity Summary
- Certification Summary
- Validation Summary
- Risk Summary

## Required Status Visibility

Statuses:

- CERTIFIED
- STALE
- DEGRADED
- EXPIRED
- REVOKED
- CANDIDATE
- VALIDATING
- UNKNOWN

Only CERTIFIED may display forward eligibility, and only with "execution-time recheck required" copy.

## Required Confidence Visibility

Confidence:

- LOW
- MEDIUM
- HIGH
- VERY_HIGH

Confidence must link to evidence and must not be confused with eligibility.

## Alerts

Required alerts:

- CAPACITY_STALE
- CAPACITY_DEGRADED
- CAPACITY_EXPIRED
- CONFIDENCE_DROP
- RECERTIFICATION_FAILED

## Decision

capacity_observability_model_defined=true

Recommended next block:

```text
E32_1_7_CAPACITY_FAILURE_MODES
```

