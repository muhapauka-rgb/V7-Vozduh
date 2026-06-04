# Runtime Shadow Dry-Run Evidence

## Command

```text
ssh v7-vps '/usr/local/bin/v7-users-autoswitch --pretty'
```

This command is read-only without `--apply`.

## Observed Result

```text
operation_owner=tools/v7-users-autoswitch
operation_type=runtime_autoswitch
terminal_state=DRY_RUN
terminal_reason=dry_run_intelligence_snapshot_stop_required
selected_move_count=0
apply_requested=false
apply_result.applied=false
```

## Existing Ownership

```text
planner_decision_owner=tools/v7-users-autoswitch
governance_authority=unchanged
execution_authority=none for recommendation layer
selected_moves_write_authority=none for recommendation layer
rollback_owner=existing runtime rollback owner
audit_closure_owner=existing audit/closure path
```

## Recommendation Evidence

The production dry-run already exposes candidate rows with:

- service suitability;
- quality decision;
- routing intelligence;
- blocked reasons;
- service status;
- explanation;
- selected moves.

The new recommendation model reuses those fields and remains shadow-only.

