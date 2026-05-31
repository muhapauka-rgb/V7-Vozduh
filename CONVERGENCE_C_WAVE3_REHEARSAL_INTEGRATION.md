# Convergence C Wave 3 Rehearsal Integration

## Mapping

Candidate maps to existing rehearsal preview through:

- `operator_execution_rehearsal_preview`
- `/api/operator/execution-rehearsal-preview`

Wave 3 adds:

- `/api/execution/candidate-rehearsal`

## Decision

Reuse Rehearsal Preview.

No dry-run engine, execution engine, runtime hook, or rehearsal store was created.

## Missing

UI drill-down is deferred to Wave 4.

## Verdict

rehearsal_integration_complete=true
