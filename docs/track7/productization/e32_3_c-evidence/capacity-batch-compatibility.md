# E32.3.C Capacity And Batch Compatibility

capacity_program_compatible=true
execution_batches_compatible=true

## Capacity Compatibility

Policy Engine is compatible with:

- Capacity Classes
- Capacity Metadata
- Capacity Runtime Gates
- Capacity Failure Modes

Policy consumes capacity state:

```text
capacity_class
capacity_status
capacity_confidence
effective_batch_cap
available_capacity
active_policy_cap
reservation_state
```

Policy cannot certify capacity and cannot override capacity failure modes.

## Batch Compatibility

Policy Engine is compatible with:

- Execution Batch Scope
- Batch Metadata
- Batch Lifecycle
- Batch Operations

Policy consumes:

```text
batch_type
allowed_users
destination_target
rollback_manifest
movement_budget
blast_radius
batch_status
batch_failure_mode
audit_lineage
```

Policy cannot mutate batch scope or lifecycle state by itself.

## Compatibility Verdict

Policy Engine is compatible with Capacity Program and Execution Batches Architecture.
