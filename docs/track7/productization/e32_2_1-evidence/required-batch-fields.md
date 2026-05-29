# E32.2.1 Required Batch Fields

required_batch_fields_defined=true

## Minimal Required Fields

```text
batch_id
batch_type
batch_generation
batch_status
allowed_users
source_targets
destination_target
rollback_targets
rollback_manifest
movement_budget
blast_radius
approval_packet_id
execution_window
capacity_requirements
operator_context
audit_lineage_id
created_at
expires_at
```

## Field Definitions

### batch_id

Unique identifier for the batch.

Authority:

```text
AUTHORITATIVE
```

### batch_type

One of:

```text
OPERATOR_MOVEMENT_BATCH
ROLLBACK_BATCH
EVACUATION_BATCH
CAPACITY_REBALANCE_BATCH
STAGED_MIGRATION_BATCH
CONTAINMENT_BATCH
```

Authority:

```text
AUTHORITATIVE
```

### batch_generation

Monotonic generation for preventing stale plan reuse.

### batch_status

Lifecycle state of the batch:

```text
DRAFT
READY_FOR_APPROVAL
APPROVED
AUTHORIZED
EXECUTING
OBSERVING
ROLLING_BACK
COMPLETED
DENIED
EXPIRED
REVOKED
```

### allowed_users

Exact user set allowed by the batch.

No wildcard users are allowed.

### source_targets

Expected source target per user.

For movement batches, execution-time recheck must verify all users still match this mapping.

### destination_target

Exact target allowed for forward movement.

For rollback-only batches this may be null or marked not applicable.

### rollback_targets

Allowed rollback targets by user or by cohort.

### rollback_manifest

Executable rollback contract:

```text
user -> rollback_target
route_table
source_before_forward
verification_rule
```

### movement_budget

Maximum number of users allowed to move forward.

### blast_radius

Maximum number of users who may be affected by the batch.

Invariant:

```text
blast_radius >= movement_budget
movement_budget == len(allowed_users) for exact movement batches
```

### approval_packet_id

Identifier of the packet that authorizes this batch.

### execution_window

Start and expiration boundaries.

### capacity_requirements

Required capacity state:

```text
required_class
required_capacity
required_confidence
required_effective_batch_cap
required_available_capacity
```

### operator_context

Human-readable reason, program block, and approval context.

### audit_lineage_id

Identifier connecting batch, packet, forward events, rollback events, replay denial, and evidence paths.

## Field Verdict

Required batch fields are defined and separate scope, authority, rollback, capacity, and audit lineage.

