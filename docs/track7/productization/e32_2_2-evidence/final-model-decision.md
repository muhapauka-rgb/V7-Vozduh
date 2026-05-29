# E32.2.2 Final Metadata Model Decision

batch_metadata_model_defined=true

## Final Model

Batch metadata is the formal data contract for execution batches.

It separates:

- authoritative scope fields;
- derived eligibility fields;
- status and freshness;
- validation requirements;
- audit lineage;
- capacity/runtime gate references.

## Core Rule

```text
metadata_defines_scope=true
metadata_is_execution_authority=false
```

## Authoritative Fields

Defined:

- identity fields;
- type fields;
- scope fields;
- rollback fields;
- capacity requirement fields;
- timing fields;
- lineage fields;
- parent/child fields.

## Derived Fields

Defined:

- effective blast radius;
- capacity requirement views;
- risk score;
- execution eligibility;
- rollback completeness;
- runtime drift status;
- packet freshness;
- capacity gate status;
- audit lineage status.

## Status And Freshness

Defined states:

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- batch_metadata_storage_format
- batch_status_transition_table_encoding
- risk_score_formula_owner
- parent_child_batch_lineage_rules
- reservation_fields_for_concurrent_batches
```

Recommended:

- use versioned JSON for batch metadata;
- store status transitions in append-only batch ledger;
- keep risk score policy-owned, with `BLOCKED` as the only hard-coded architecture result for now;
- require child batches to reference parent id and lineage id;
- defer reservation fields to the reservation ledger architecture block.

## Remaining Open Questions

- exact JSON schema;
- exact status transition graph encoding;
- whether risk score is computed by policy engine or batch validator;
- whether rollback batches reuse original batch id or child batch id;
- how to model reservation fields before concurrency is certified.

## Decision

Batch Metadata Model is defined, consistent with E32.2.1, and production-pool compatible.

recommended_next_block=E32_2_3_BATCH_LIFECYCLE

