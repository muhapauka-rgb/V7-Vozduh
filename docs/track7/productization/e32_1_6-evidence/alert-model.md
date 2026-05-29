# E32.1.6 Alert Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

alert_model_defined=true

## Alert Types

### CAPACITY_STALE

Trigger:

- now >= capacity_stale_after.

Severity: warning.

Operator action:

- run refresh validation.

### CAPACITY_DEGRADED

Trigger:

- readiness NO-GO;
- quality floor breach;
- runtime checker failure;
- restore-settle not GO;
- isolation failure.

Severity: critical.

Operator action:

- diagnose/remediate;
- block forward movement;
- consider rollback/containment if during execution.

### CAPACITY_EXPIRED

Trigger:

- now >= capacity_expiration;
- major target/profile/schema change.

Severity: critical.

Operator action:

- full recertification.

### CONFIDENCE_DROP

Trigger:

- incident;
- evidence invalidation;
- repeated validation failure;
- demotion.

Severity: warning or critical depending on cause.

Operator action:

- inspect evidence and recovery path.

### RECERTIFICATION_FAILED

Trigger:

- recertification validation fails.

Severity: critical.

Operator action:

- block forward movement;
- classify root cause;
- replacement strategy if repeated.

## Alert Suppression

Alerts may be grouped but not hidden when they affect execution eligibility.

## Alert Copy Rule

Every alert must include:

- what changed;
- what is blocked;
- what remains allowed;
- next safe action.

