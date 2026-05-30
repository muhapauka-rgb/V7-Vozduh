# E32.5.C Gap Analysis

## Remaining Gaps

- schedule storage backend;
- authoritative queue storage;
- final queue ordering weights;
- schedule observability schema;
- window source of truth;
- maintenance window source;
- dependency resolution backend;
- scheduler drift reconciliation workflow;
- double dispatch ledger backend;
- emergency schedule review authority;
- scheduler owner identity model.

## Remaining Risks

| Risk | Severity | Mitigation Status |
| --- | --- | --- |
| queue ordering starvation | MEDIUM | Weighted priority with fairness floor selected; final weights pending. |
| stale derived readiness | MEDIUM | Dispatch requires recomputation and execution-time recheck. |
| dependency ambiguity | MEDIUM | Unknown dependency state denies dispatch and may require human review. |
| window source drift | MEDIUM | Window source of truth remains implementation decision. |
| double dispatch backend gap | HIGH | Architecture requires ledger/compare-and-set; implementation pending. |
| emergency misuse | HIGH | Emergency cannot bypass governance; review authority pending. |

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- schedule_storage_backend
- authoritative_queue_storage
- queue_ordering_algorithm_final_weights
- schedule_observability_schema
- window_source_of_truth
- maintenance_window_source
- dependency_resolution_backend
- scheduler_drift_reconciliation_workflow
- double_dispatch_ledger_backend
- emergency_schedule_review_authority
- scheduler_owner_identity_model
```

## Certification Impact

These gaps do not block architecture certification because:

- scheduling behavior is defined;
- fail-closed behavior is defined;
- dispatch boundary is explicit;
- implementation storage and schema choices are deferred as architecture decisions.
