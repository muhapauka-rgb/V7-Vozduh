# E32.2.2 Capacity And Runtime Integration

capacity_runtime_integration_defined=true

## Capacity References

Batch metadata references capacity through:

```text
capacity_class
capacity_status
capacity_confidence
certified_capacity
effective_batch_cap
available_capacity
capacity_validation_evidence
capacity_expiration
```

Forward eligibility requires:

```text
capacity_status == CERTIFIED
capacity_not_expired=true
movement_budget <= effective_batch_cap
movement_budget <= available_capacity
capacity_confidence >= required_confidence
```

## Runtime Gate References

Batch metadata references runtime through:

```text
runtime_checkers_status
restore_settle_gate_status
selected_moves_count
hidden_movers_status
users_registry_hash
egress_registry_hash
route_table_map
target_users_count
```

Execution-time recheck must verify these values before movement.

## Drift Handling

If runtime drift appears:

```text
execution_eligibility=false
fresh_packet_required=true
```

Examples:

- users registry hash mismatch;
- egress registry hash mismatch;
- selected moves nonzero;
- hidden movers present;
- candidate user no longer on expected source target;
- target capacity no longer sufficient.

## Selected Moves And Hidden Movers

Forward execution requires:

```text
selected_moves_count == 0
hidden_movers_absent == true
```

If either fails:

```text
batch_status=FAILED_CLOSED
operator_next_action=restore_settle_or_investigate
```

## Restore-Settle

Forward execution requires:

```text
restore_settle_gate_status=GO
```

Rollback closure requires restore-settle verification after rollback.

## Integration Verdict

Batch metadata integrates with capacity and runtime gates without weakening governance.

