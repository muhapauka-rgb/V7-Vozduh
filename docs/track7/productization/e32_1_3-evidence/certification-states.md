# E32.1.3 Certification States

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

certification_states_defined=true

## State Model

### UNCERTIFIED

Meaning: target has no accepted capacity certification.

Allowed actions:

- inspect metadata;
- collect candidate evidence;
- run architecture modeling;
- prepare validation plan.

Forbidden actions:

- forward movement approval;
- production-pool scheduling;
- batch execution.

Governance impact:

- `current_capacity=0`;
- target can only be used after entering CANDIDATE and then CERTIFIED through evidence.

### CANDIDATE

Meaning: target is plausible for a class but lacks complete evidence.

Allowed actions:

- target-local validation planning;
- evidence collection;
- draft metadata;
- non-executable packet modeling.

Forbidden actions:

- treating candidate capacity as certified;
- live forward execution based on candidate status.

Governance impact:

- may appear in preparation workflows;
- denied in execution-time recheck.

### VALIDATING

Meaning: validation is underway or evidence is being reviewed.

Allowed actions:

- collect target-local probes;
- collect long-window validation;
- verify readiness and restore-settle;
- assemble evidence package.

Forbidden actions:

- class promotion before evidence is complete;
- executable approval packet for the new class.

Governance impact:

- previous lower certified class may remain usable if still fresh;
- new class remains non-executable.

### CERTIFIED

Meaning: class evidence is complete, accepted, and fresh.

Allowed actions:

- approval packet generation up to effective cap;
- execution-time recheck;
- governed forward execution if all gates pass;
- rollback.

Forbidden actions:

- exceeding class cap;
- bypassing freshness or execution-time recheck;
- using certification as production-pool authority unless production-pool policy is also certified.

Governance impact:

- nonzero capacity may be derived.

### STALE

Meaning: historical certification remains true, but operational freshness is insufficient.

Allowed actions:

- refresh validation;
- rollback;
- diagnostics;
- downgrade.

Forbidden actions:

- new forward movement approval;
- production-pool scheduling.

Governance impact:

- `current_capacity=0`;
- certification history remains audit-valid.

### DEGRADED

Meaning: target has active quality, readiness, checker, isolation, or operational degradation.

Allowed actions:

- remediation;
- rollback;
- diagnostics;
- downgrade or revoke.

Forbidden actions:

- forward movement;
- promotion;
- production-pool scheduling.

Governance impact:

- fail closed until recovery evidence is accepted.

### EXPIRED

Meaning: certification freshness exceeded hard expiry or was invalidated by major change.

Allowed actions:

- full recertification;
- historical review;
- replacement planning.

Forbidden actions:

- forward movement based on expired proof;
- simple refresh without required evidence.

Governance impact:

- `current_capacity=0`.

### RECERTIFYING

Meaning: target is being revalidated after STALE, DEGRADED, EXPIRED, or requested promotion.

Allowed actions:

- collect required evidence for the desired class;
- compare against prior proof;
- prepare certification decision.

Forbidden actions:

- using in-progress recertification as execution authority.

Governance impact:

- previous usable class is suspended unless explicitly still fresh and not implicated by the reason for recertification.

### REVOKED

Meaning: certification is invalidated by a serious governance or safety defect.

Allowed actions:

- rollback/containment;
- audit investigation;
- full requalification from UNCERTIFIED or CANDIDATE;
- replacement target planning.

Forbidden actions:

- forward movement;
- class refresh;
- production-pool scheduling.

Governance impact:

- target has no active certification.

