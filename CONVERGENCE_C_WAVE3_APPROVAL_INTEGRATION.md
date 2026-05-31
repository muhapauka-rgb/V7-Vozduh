# Convergence C Wave 3 Approval Integration

## Mapping

Candidate maps to existing Approval Center through:

- `operator_approval_preview`
- `/api/operator/approval-preview`
- `/api/operator/approval-contracts`

Wave 3 adds:

- `/api/execution/candidate-approval`

## Decision

Reuse Approval Center.

No candidate approval store, approval queue, or approval event stream was created.

## Missing

UI drawer integration remains deferred to Wave 4.

## Verdict

approval_integration_complete=true
