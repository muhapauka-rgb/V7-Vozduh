# E32.5.B Final Operations Decision

scheduling_operations_defined=true

## Decision Summary

E32.5.B defines operational behavior for Scheduling.

The operations model covers:

- scheduler admission;
- queue ordering;
- dispatch;
- runtime impact;
- observability;
- failure modes;
- fail-closed matrix;
- production-pool compatibility;
- future Routing Intelligence separation.

## Certification Markers

```text
scheduling_operations_defined=true
scheduler_admission_defined=true
queue_ordering_defined=true
dispatch_model_defined=true
scheduler_runtime_impact_defined=true
scheduler_observability_defined=true
scheduler_failure_modes_defined=true
scheduler_fail_closed_matrix_defined=true
production_pool_compatible=true
routing_intelligence_future_compatible=true
```

## Core Operational Rules

- Queue admission is not execution.
- READY is not execution authority.
- DISPATCHED is only handoff into execution path.
- Scheduler does not choose users or targets.
- Scheduler does not bypass policy, capacity, concurrency, packet, or execution-time recheck gates.
- Every scheduler failure mode denies dispatch.
- Rollback remains allowed only for exact known moved scope.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- scheduler_queue_storage_backend
- queue_ordering_algorithm_final_weights
- schedule_observability_schema
- window_source_of_truth
- dependency_resolution_backend
- scheduler_drift_reconciliation_workflow
- double_dispatch_ledger_backend
- emergency_schedule_review_authority
```

## Remaining Open Questions

- Which backend stores authoritative queue position?
- What exact weights should weighted_priority_with_fairness_floor use?
- How often should scheduler recompute derived readiness?
- Should dependency failures cancel children automatically or require review?
- Which service owns schedule window truth?

## Final Decision

scheduling_operations_defined=true

recommended_next_block=E32.5.C_SCHEDULING_CERTIFICATION
