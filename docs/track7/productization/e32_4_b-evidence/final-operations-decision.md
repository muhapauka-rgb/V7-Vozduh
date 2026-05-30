# E32.4.B Final Operations Decision

concurrency_operations_defined=true

## Decision Summary

E32.4.B defines the operational behavior of concurrency controls.

The operations model covers:

- runtime impact;
- scheduler admission impact;
- batch execution impact;
- rollback exception behavior;
- packet consumption behavior;
- reservation ownership behavior;
- operator observability;
- owner transfer;
- failure modes;
- fail-closed matrix;
- production-pool compatibility.

## Certification Markers

```text
concurrency_operations_defined=true
concurrency_runtime_impact_defined=true
concurrency_observability_defined=true
owner_transfer_model_defined=true
concurrency_failure_modes_defined=true
concurrency_fail_closed_matrix_defined=true
production_pool_compatible=true
```

## Core Operational Rules

- Locks gate eligibility, not authority.
- Reservations claim planned capacity, not movement authority.
- Packet consumption is single-use and protected.
- Owner transfer is explicit, audited, and fenced.
- Every concurrency failure mode denies forward movement.
- Rollback remains allowed only for exact known scope.
- Unknown owner, unknown scope, stale lock, stale reservation, or audit uncertainty requires fail-closed behavior.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- lock_observability_schema
- reservation_observability_schema
- owner_heartbeat_backend
- stale_lock_recovery_workflow
- packet_consumption_ledger_backend
- reservation_conflict_operator_workflow
- audit_lock_vs_native_sequence_decision
- scheduler_executor_transfer_protocol
```

## Remaining Open Questions

- Should stale reservation refresh be automatic or operator-driven?
- How long should scheduler-owned locks remain valid before transfer?
- Which component owns lock and reservation dashboards?
- Should audit sequencing block terminal state finalization or only certification?
- How should batch observability group multiple blocked users?

## Final Decision

concurrency_operations_defined=true

recommended_next_block=E32.4.C_CONCURRENCY_CERTIFICATION
