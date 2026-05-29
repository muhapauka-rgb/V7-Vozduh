# E32.1.7 Failure Mode Inventory

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

failure_mode_inventory_defined=true

## Failure Modes

### CAPACITY_STALE

Meaning: historical certification exists, but operational freshness is past `capacity_stale_after`.

Default impact:

- forward denied;
- refresh required;
- rollback remains allowed if exact scope is known.

### CAPACITY_DEGRADED

Meaning: target quality, readiness, restore-settle, runtime checkers, or isolation has degraded.

Default impact:

- forward denied;
- remediation required;
- rollback/containment may remain allowed.

### CAPACITY_EXPIRED

Meaning: certification evidence exceeded hard expiry or a major target/schema/profile change invalidated active eligibility.

Default impact:

- forward denied;
- full recertification required;
- historical certification remains audit truth.

### CAPACITY_REVOKED

Meaning: certification is invalidated by a serious governance or safety defect.

Examples:

- replay accepted;
- rollback failure not contained;
- unauthorized movement;
- audit contradiction;
- blast radius breach.

Default impact:

- forward denied;
- incident review required;
- target must re-enter certification through CANDIDATE.

### CAPACITY_UNKNOWN

Meaning: capacity state cannot be evaluated.

Default impact:

- forward denied;
- discovery/inspection required.

### CAPACITY_CONFLICT

Meaning: authoritative capacity fields conflict.

Examples:

- `capacity_class=CLASS_10` but `hard_limit=4`;
- packet-bound capacity differs from live metadata;
- evidence class conflicts with current registry metadata.

Default impact:

- forward denied;
- operator review and metadata reconciliation required.

### CAPACITY_EVIDENCE_MISSING

Meaning: required evidence reference is missing or unreadable.

Default impact:

- forward denied;
- evidence reconstruction or recertification required.

### CAPACITY_CONFIDENCE_DROP

Meaning: confidence level falls below required threshold.

Examples:

- incident found;
- repeated validation failures;
- evidence invalidated;
- production-pool controls missing.

Default impact:

- forward denied for affected class;
- recertification or downgrade required.

### CAPACITY_POLICY_CAP_EXCEEDED

Meaning: requested batch exceeds active policy cap.

Default impact:

- packet creation/execution denied;
- operator may lower batch size or request policy decision.

### CAPACITY_RESERVATION_CONFLICT

Meaning: capacity reservation ledger or active packet state conflicts with requested movement.

Examples:

- requested batch exceeds available capacity after reservation;
- duplicate active reservation;
- expired packet still reserving capacity;
- reservation ledger and audit disagree.

Default impact:

- scheduler admission denied;
- human review if ledger/audit disagree.

