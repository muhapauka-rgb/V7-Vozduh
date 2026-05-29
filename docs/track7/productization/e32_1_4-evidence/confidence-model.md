# E32.1.4 Confidence Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

confidence_model_defined=true

## Levels

### LOW

Meaning: target has static or partial evidence only.

Earned by:

- metadata review;
- static compatibility;
- incomplete validation.

Use:

- preparation only;
- no forward execution approval.

### MEDIUM

Meaning: target has passed target-local pressure and long-window validation but lacks class-sized governed execution proof.

Earned by:

- target-local pressure passes;
- long-window passes;
- readiness GO;
- restore-settle GO;
- runtime checkers OK.

Use:

- approval packet drafting;
- final pre-execution preparation;
- not full class certification.

### HIGH

Meaning: target has class-sized governed movement proof.

Earned by:

- all MEDIUM evidence;
- class-sized forward proof;
- rollback proof;
- delayed monitoring;
- replay denial;
- audit chain validation.

Use:

- capacity class certification;
- bounded operator execution up to class cap.

### VERY_HIGH

Meaning: target has repeated successful class-sized cycles and production-pool controls.

Earned by:

- multiple successful executions at class;
- no recent incidents;
- automated policy enforcement;
- scheduler/reservation controls;
- audit volume validation;
- recertification history.

Use:

- future production-pool authority candidate.

## Confidence Inputs

- validation count;
- successful movements;
- successful rollbacks;
- replay proofs;
- audit proof quality;
- validation age;
- incident history;
- quality margin over floors;
- runtime checker stability;
- operator intervention required.

## Current Target

For `amneziawg-exec-20260528-10-8-1-14`:

```text
capacity_confidence=HIGH
```

Reason:

- CLASS_10 target-local validation passed;
- long-window validation passed;
- ten-user governed movement passed;
- rollback passed;
- replay denial passed;
- E31 certified production-grade governance through 10 users.

