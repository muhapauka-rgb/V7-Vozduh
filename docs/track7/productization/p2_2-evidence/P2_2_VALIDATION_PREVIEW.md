# P2.2 Validation Preview

## Implementation

Implemented Validation Preview read model.

The preview shows what would be checked before execution.

## Gates

Validation Preview evaluates:

- Authority
- Evaluator
- Conflict Resolver
- Runtime Trust
- Release Trust
- Required Services
- Capacity
- Policy
- Concurrency
- Restore-Settle
- Selected Moves
- Hidden Movers
- Target Readiness
- Routing Mode
- Containment State

## Statuses

Supported preview statuses:

- PASS
- FAIL
- REVIEW_REQUIRED
- UNKNOWN

## Fail-Closed Behavior

Runtime blocking, release drift, missing proposal reference, missing evidence reference, missing target, or capacity hard-limit failure can make the preview fail closed.

Unknown future gates remain visible as `UNKNOWN` or `REVIEW_REQUIRED`; they do not silently pass.

## Verdict

validation_preview_implemented=true
validation_preview_only=true
runtime_mutation_performed=false
