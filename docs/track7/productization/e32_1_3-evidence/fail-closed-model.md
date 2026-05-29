# E32.1.3 Fail-Closed Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

fail_closed_model_defined=true

## Default Rule

When capacity state is ambiguous, forward execution is denied.

```text
unknown_or_missing_capacity => current_capacity=0
unknown_or_missing_readiness => execution_allowed=false
unknown_or_missing_restore_settle => execution_allowed=false
unknown_or_missing_runtime_checkers => execution_allowed=false
unknown_or_missing_evidence => certification_not_granted
```

## Failure Cases

### Evidence Missing

Result:

- status=UNKNOWN or EXPIRED;
- no forward approval;
- require evidence reconstruction or revalidation.

### Readiness Unknown

Result:

- no packet generation;
- no execution authorization;
- rerun readiness.

### Restore-Settle Missing

Result:

- no forward movement;
- rerun restore-settle;
- if unavailable, stop fail-closed.

### Capacity Stale

Result:

- status=STALE;
- current capacity zero for forward movement;
- refresh required.

### Confidence Low

Result:

- status=CANDIDATE or VALIDATING;
- no live execution for requested class.

### Audit Inconsistent

Result:

- status=REVOKED if certification proof depends on that audit chain;
- forward movement denied;
- incident review required.

### Replay Inconsistent

Result:

- status=REVOKED for affected class;
- no production-pool eligibility.

## Rollback Exception

Rollback remains allowed as containment even when forward movement is denied, provided rollback scope is exact and does not expand blast radius.

