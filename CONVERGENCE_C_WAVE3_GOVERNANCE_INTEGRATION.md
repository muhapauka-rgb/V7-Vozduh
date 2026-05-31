# Convergence C Wave 3 Governance Integration

## Mapping

Candidate maps to existing governance preview through:

- `operator_execution_governance_preview`
- `/api/operator/execution-governance-preview`

Wave 3 adds:

- `/api/execution/candidate-governance`

## Decision

Reuse Governance Preview as truth source.

No duplicate governance store or workflow was created.

## Conflicts

Candidate risk state can disagree with governance preview denial state. The API reports both and fails closed when either side blocks.

## Verdict

governance_integration_complete=true
