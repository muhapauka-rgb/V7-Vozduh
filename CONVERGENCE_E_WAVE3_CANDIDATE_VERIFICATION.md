# Convergence E Wave 3 Candidate Verification

Project: V7 Vozduh
Block: Convergence E

## Candidate Workflow Layer

Verified Wave 3 surfaces:

- candidate model
- candidate readiness
- candidate risks
- candidate explanation
- candidate timeline
- candidate approval
- candidate governance
- candidate rehearsal
- candidate workflow

## API Routes

- `/api/execution/candidates`
- `/api/execution/candidates/`
- `/api/execution/candidates/readiness`
- `/api/execution/candidates/risks`
- `/api/execution/candidates/explain`
- `/api/execution/candidates/timeline`
- `/api/execution/candidate-approval`
- `/api/execution/candidate-governance`
- `/api/execution/candidate-rehearsal`
- `/api/execution/candidate-workflow`

## Verification

- Candidate remains a derived read model.
- No candidate store was introduced.
- No candidate queue was introduced.
- Candidate approval maps to existing `operator_approval_preview`.
- Candidate governance maps to existing `operator_execution_governance_preview`.
- Candidate rehearsal maps to existing `operator_execution_rehearsal_preview`.
- No parallel approval workflow was introduced.

## Truth Source

- Canonical source: proposal and preview models
- Derived source: candidate model, candidate lifecycle, candidate risk, candidate timeline
- Presentation source: candidate and candidate-workflow APIs
- Runtime source: none beyond read-only runtime stores used by existing preview models

wave3_verified=true
