# E32.4.C Gap Analysis

## Remaining Gaps

- lock storage backend;
- reservation ledger storage backend;
- fencing token format;
- canonical user sort key implementation;
- exact lock TTL values;
- owner heartbeat source;
- stale lock recovery authority;
- audit sequence authority;
- scheduler/operator owner transfer protocol;
- lock observability schema;
- reservation observability schema;
- packet consumption ledger backend;
- reservation conflict operator workflow.

## Remaining Risks

| Risk | Severity | Mitigation Status |
| --- | --- | --- |
| Non-atomic lock backend | HIGH | Architecture requires atomic backend; implementation decision remains. |
| Reservation ledger race | HIGH | Architecture requires atomic reservation ledger. |
| Stale owner heartbeat ambiguity | MEDIUM | Forward movement denied; human review required. |
| Audit sequence ambiguity | MEDIUM | Certification denied until audit order is proven. |
| Scheduler/operator conflict | MEDIUM | Owner transfer and BATCH_LOCK address the model; implementation remains. |
| Long-running large batch locks | MEDIUM | TTL and recovery strategy defined; exact values pending. |

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- lock_storage_backend
- reservation_ledger_storage_backend
- fencing_token_format
- canonical_user_sort_key
- exact_lock_ttl_values
- owner_heartbeat_source
- stale_lock_recovery_authority
- audit_sequence_authority
- scheduler_operator_owner_transfer_protocol
- lock_observability_schema
- reservation_observability_schema
- packet_consumption_ledger_backend
- reservation_conflict_operator_workflow
```

## Certification Impact

The gaps do not block architecture certification because:

- behavioral model is complete;
- fail-closed behavior is defined;
- production-pool compatibility is defined;
- implementation-specific storage and schema decisions are explicitly deferred.
