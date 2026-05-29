# E32.2.1 Final Model Decision

execution_batch_model_defined=true

## Final Model

An execution batch is the formal V7 unit of governed action. It packages:

- exact users;
- exact source targets;
- exact destination target;
- exact rollback manifest;
- movement budget;
- blast radius;
- execution window;
- approval packet;
- capacity requirements;
- audit lineage.

## Core Rule

```text
batch_is_scope_container=true
batch_is_authority=false
```

Authority remains with:

- approval packet;
- execution-time recheck;
- runtime gates;
- capacity gates;
- operator confirmation where required.

## Batch Types

Defined:

- `OPERATOR_MOVEMENT_BATCH`
- `ROLLBACK_BATCH`
- `EVACUATION_BATCH`
- `CAPACITY_REBALANCE_BATCH`
- `STAGED_MIGRATION_BATCH`
- `CONTAINMENT_BATCH`

## Capacity Integration

Forward-capable batches require:

```text
capacity_status=CERTIFIED
movement_budget <= effective_batch_cap
movement_budget <= available_capacity
target_eligible=true
```

Rollback batches retain containment exception.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- batch_id_generation_format
- batch_status_storage_location
- batch_priority_model_for_scheduler
- partial_failure_policy_for_multi_user_batches
```

Recommended:

- use deterministic prefixed ids: `batch-<block>-<timestamp>-<hash>`;
- store batch status in an append-only batch ledger;
- keep scheduler priority undefined until scheduler architecture block;
- require immediate rollback/containment on partial forward failure unless a later block certifies partial-completion semantics.

## Remaining Open Questions

- exact batch JSON schema;
- whether rollback batches should reference original forward batch or create independent batch ids;
- whether staged migrations use parent/child batch ids;
- how production-pool scheduler assigns priority;
- how to represent partial execution if a multi-user command sequence fails mid-batch.

## Decision

The E32.2.1 Execution Batch Model is defined and does not contradict the certified Capacity Program.

recommended_next_block=E32_2_2_BATCH_METADATA_MODEL

