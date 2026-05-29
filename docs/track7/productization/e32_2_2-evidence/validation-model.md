# E32.2.2 Validation Model

batch_metadata_validation_defined=true

## Validation Principle

Batch metadata validation proves that the batch is exact, bounded, auditable, time-limited, and compatible with capacity and runtime gates.

Validation does not move users.

## Required Validation Checks

### Exact User Set

```text
allowed_users_non_empty=true_for_forward_batches
allowed_users_have_no_wildcards=true
allowed_users_unique=true
```

### Exact Target Set

```text
destination_target_present=true_for_forward_batches
destination_target_in_allowed_targets=true
source_targets_present_for_all_users=true
```

### Movement Budget

For exact movement:

```text
movement_budget == len(allowed_users)
```

For rollback-only or containment:

```text
movement_budget == 0_or_declared_containment_budget
```

### Blast Radius

For exact movement:

```text
blast_radius == len(allowed_users)
```

For containment:

```text
blast_radius == len(affected_users)
```

### Rollback Manifest

```text
rollback_manifest_complete=true
rollback_manifest_covers_all_allowed_users=true
rollback_targets_known=true
route_tables_known_when_routing_mutation_possible=true
```

Forward execution is denied if rollback manifest is incomplete.

### Capacity Requirements

```text
capacity_requirements_present=true
required_capacity <= effective_batch_cap
required_capacity <= available_capacity
capacity_status == CERTIFIED
```

### Approval Packet

```text
approval_packet_id_required_before_execution=true
approval_packet_non_expired=true
approval_packet_generation_matches_batch_generation=true
```

### Audit Lineage

```text
audit_lineage_id_present=true
audit_lineage_unique=true
evidence_paths_planned=true
```

### Execution Window

```text
created_at < expires_at
now <= expires_at_before_forward
```

## Failure Behavior

Any validation failure produces:

```text
execution_eligibility=false
batch_status=FAILED_CLOSED_or_EXPIRED
operator_next_action=repair_metadata_or_generate_fresh_batch
```

## Validation Verdict

Batch metadata validation is defined.

