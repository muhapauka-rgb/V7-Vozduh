# E32.2.C Gap Analysis

## Remaining Gaps

Execution Batch Architecture is complete as architecture, but future tracks still need:

- exact batch JSON schema;
- batch ledger storage implementation;
- status transition allowlist encoding;
- production-pool reservation ledger;
- scheduler priority model;
- production-pool batch observability schema;
- policy-engine ownership of risk score;
- retained production-pool completion semantics;
- partial forward and partial rollback automation policy;
- audit reconstruction authority.

## Remaining Risks

| Risk | Status | Notes |
| --- | --- | --- |
| Concurrent batch double-spend | Remaining | Requires reservation ledger certification. |
| Partial forward automation | Deferred | Current recommendation is rollback/containment, human-aware. |
| Audit inconsistency recovery | Remaining | Requires audit reconstruction authority. |
| Production-pool retained movement | Remaining | Proof-style batches still default to rollback. |
| Scheduler priority | Remaining | Deferred to scheduler architecture. |
| Batch schema drift | Remaining | Needs versioned JSON schema. |

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- batch_id_generation_format
- batch_status_storage_location
- batch_metadata_storage_format
- batch_status_transition_table_encoding
- risk_score_formula_owner
- parent_child_batch_lineage_rules
- retained_production_pool_completion_semantics
- reservation_release_timing_for_concurrent_batches
- production_pool_batch_reservation_ledger
- production_pool_batch_observability_schema
- partial_forward_automated_rollback_policy
- audit_reconstruction_authority
```

## Gap Verdict

No remaining gap invalidates the architecture.

The gaps are implementation and future production-pool policy decisions, not contradictions in the current model.
