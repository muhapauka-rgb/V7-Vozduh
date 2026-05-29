# E32.1.8 Gap Analysis

## Missing Pieces

The Capacity Program is complete as an architecture model, but future implementation tracks still need:

- capacity metadata storage schema;
- capacity view-model generation;
- policy-engine integration;
- scheduler admission model;
- reservation ledger design;
- concurrent packet semantics;
- production-pool dashboard schema;
- production-pool alert retention and escalation rules;
- CLASS_20, CLASS_50, and CLASS_100 proof methodology finalization.

## Remaining Risks

| Risk | Status | Notes |
| --- | --- | --- |
| Capacity beyond CLASS_10 | Remaining | CLASS_20/50/100 are candidate classes only. |
| Production-pool concurrency | Remaining | Requires reservation ledger certification. |
| Reservation conflicts | Partially modeled | Failure mode exists; automatic resolution scope needs product decision. |
| Large audit volume | Remaining | Audit proof model exists, but stress volume is not proven. |
| Large rollback sets | Remaining | Rollback semantics defined, but >10 user rollback remains unproven. |
| Policy cap behavior | Partially modeled | Active policy cap exists; exact policy source remains future work. |
| Dashboard source of truth | Partially modeled | Generated view model recommended until policy API exists. |
| CLASS_50/CLASS_100 quality floors | Remaining | Requires production-pool SLO architecture. |

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- capacity_metadata_storage_location
- production_pool_reservation_ledger_storage
- max_concurrent_batches_for_production_pool
- automatic_reservation_conflict_resolution_scope
- capacity_dashboard_authoritative_source
- production_pool_quality_floors_for_CLASS_50_AND_CLASS_100
- large_scale_certification_authority_for_CLASS_50_CLASS_100_AND_PRODUCTION_POOL
```

## Decision Recommendations

### capacity_metadata_storage_location

Recommended:

```text
sidecar_capacity_state_file_with_schema_versioning
```

Reason:

Keeps current registry semantics stable while allowing capacity metadata to evolve.

### production_pool_reservation_ledger_storage

Recommended:

```text
append_only_reservation_ledger_with_transaction_ids
```

Reason:

Reservations affect scheduler admission and must be auditable.

### max_concurrent_batches_for_production_pool

Recommended:

```text
max_concurrent_batches=1_until_reservation_ledger_certified
```

Reason:

Avoids capacity double-spend before concurrency controls exist.

### automatic_reservation_conflict_resolution_scope

Recommended:

```text
automation_may_release_clearly_expired_reservations_only
ledger_audit_disagreement_requires_human_review
```

Reason:

Preserves safety while allowing low-risk cleanup.

### capacity_dashboard_authoritative_source

Recommended:

```text
generated_capacity_view_model_now
policy_engine_api_later
```

Reason:

Provides operator observability before policy engine exists.

### production_pool_quality_floors_for_CLASS_50_AND_CLASS_100

Recommended:

```text
define_as_part_of_production_pool_slo_track
```

Reason:

Large-scale classes need production-pool SLOs rather than extrapolated CLASS_10 floors.

### large_scale_certification_authority_for_CLASS_50_CLASS_100_AND_PRODUCTION_POOL

Recommended:

```text
policy_engine_with_operator_governance_after_staged_proofs
```

Reason:

Combines automation consistency with human accountability for large blast radius.

## Gap Verdict

No gap blocks certification of the Capacity Program as an architecture foundation.

The gaps are implementation and future-track decisions, not contradictions in the current model.

