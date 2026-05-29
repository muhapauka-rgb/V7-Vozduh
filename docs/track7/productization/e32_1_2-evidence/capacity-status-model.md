# E32.1.2 Capacity Status Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_status_model_defined=true

## Status Values

### UNKNOWN

Meaning: no reliable capacity metadata exists.

Allowed actions:

- inspect;
- collect evidence;
- run read-only modeling;
- prepare validation.

Forbidden actions:

- approval packet for movement;
- class promotion;
- production-pool scheduling.

### CANDIDATE

Meaning: target has potential capacity but not complete certification.

Allowed actions:

- target-local probes;
- long-window validation;
- candidate-pool preparation;
- approval packet draft with `execution_allowed_now=false`.

Forbidden actions:

- live execution based on candidate capacity;
- autoswitch/rebalance consumption.

### VALIDATING

Meaning: validation is actively being collected or reviewed.

Allowed actions:

- read-only or target-local validation;
- evidence generation;
- metadata draft.

Forbidden actions:

- movement unless a separate already-certified class covers the requested batch;
- using in-progress evidence as certified capacity.

### CERTIFIED

Meaning: target has complete evidence for the active class and freshness is valid.

Allowed actions:

- approval packet generation up to `effective_batch_cap`;
- execution-time recheck;
- governed movement if all gates pass.

Forbidden actions:

- exceeding effective batch cap;
- bypassing execution-time recheck;
- production-pool assignment unless production-pool policy is also certified.

### STALE

Meaning: historical certification remains valid as a record, but operational freshness is insufficient for new execution.

Allowed actions:

- refresh validation;
- lower capacity;
- generate non-executable draft plans.

Forbidden actions:

- new movement approval;
- production-pool scheduling;
- capacity promotion.

### DEGRADED

Meaning: target shows quality, readiness, checker, or isolation degradation.

Allowed actions:

- remediation;
- rollback;
- diagnostics;
- downgrade.

Forbidden actions:

- new forward movement;
- capacity promotion;
- production-pool scheduling.

### EXPIRED

Meaning: validation evidence exceeded hard expiration or was invalidated by a major change.

Allowed actions:

- full revalidation;
- downgrade;
- replacement target planning.

Forbidden actions:

- approval packet generation for movement;
- treating old class as active capacity.

## Transition Rules

```text
UNKNOWN -> CANDIDATE
CANDIDATE -> VALIDATING
VALIDATING -> CERTIFIED
CERTIFIED -> STALE
CERTIFIED -> DEGRADED
CERTIFIED -> EXPIRED
STALE -> VALIDATING
DEGRADED -> VALIDATING
EXPIRED -> VALIDATING
ANY -> DEGRADED on safety failure
ANY -> EXPIRED on major incompatible change
```

## Fail-Closed Defaults

The following statuses imply:

```text
current_capacity=0
effective_batch_cap=0
execution_allowed=false
```

Statuses:

- `UNKNOWN`
- `CANDIDATE`
- `VALIDATING`
- `STALE`
- `DEGRADED`
- `EXPIRED`

Only `CERTIFIED` with fresh validation may expose nonzero execution capacity.

