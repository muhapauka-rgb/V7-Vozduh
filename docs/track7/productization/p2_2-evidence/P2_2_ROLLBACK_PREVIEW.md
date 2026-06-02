# P2.2 Rollback Preview

## Implementation

Implemented Rollback Preview read model.

Rollback Preview is derived from the draft contract and current proposal state.

## Rollback Model

Rollback Preview shows:

- rollback scope
- rollback manifest
- rollback validation requirements
- rollback verification steps
- rollback risks

Each affected user maps to a rollback target derived from current registry state or proposal current target.

## Risks

If a rollback target is unknown, the preview marks the contract as requiring review or failing closed.

## Verdict

rollback_preview_implemented=true
rollback_preview_only=true
runtime_mutation_performed=false
