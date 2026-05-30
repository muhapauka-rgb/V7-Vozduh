# E32.5.A Dependency Model

dependency_model_defined=true

## Dependency Types

| Type | Meaning |
| --- | --- |
| BATCH_SUCCESS | Child may run only if parent batch reaches successful terminal state. |
| ROLLBACK_COMPLETE | Child may run only after parent rollback is verified. |
| AUDIT_COMPLETE | Child may run only after parent audit lineage is complete. |
| WINDOW_CHAIN | Child inherits or follows a parent execution window. |
| MANUAL_RELEASE | Child waits for explicit operator release after parent state. |

## Dependency Behavior

Parent/child schedule rules:

- child schedule must list dependency_batch_ids;
- parent result must be terminal and auditable;
- dependency success must be recomputed at dispatch-time;
- dependency failure moves child to FAILED_CLOSED or CANCELLED according to operator intent;
- dependency timeout moves child to EXPIRED or FAILED_CLOSED;
- unknown dependency state denies dispatch.

## Cascading Behavior

If parent fails closed:

- child forward dispatch is denied;
- child may be cancelled;
- child may be regenerated with a fresh approval path;
- child must not automatically broaden scope;
- child must not bypass policy or concurrency gates.

If parent succeeds:

- child still requires all current gates;
- stale capacity, stale policy, stale locks, or expired packet still deny dispatch.

## Cycle Prevention

Dependency graph must be acyclic. Cycles fail closed at queue admission.

## Decision

dependency_model_defined=true
