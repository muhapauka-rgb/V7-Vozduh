# Convergence C Wave 3 Candidate Inventory

## Inventory

| Domain | Purpose | Truth Source | Storage | Dependencies | Consumers |
| --- | --- | --- | --- | --- | --- |
| Candidate Model | Derived representation of a proposal-derived draft contract. | Proposal store plus draft preview | Derived; no new store | Draft contracts, validation, readiness forecast | Candidate APIs |
| Candidate Readiness | Shows lifecycle and forecast state. | Wave 2 readiness preview | Derived | Validation preview, readiness forecast | `/api/execution/candidates/readiness` |
| Candidate Risks | Aggregates blocker/review risks. | Validation, service impact, blast radius, rollback impact | Derived | Wave 2 helpers | `/api/execution/candidates/risks` |
| Candidate Explanation | Explains why a candidate exists and what blocks it. | Candidate plus readiness explain | Derived | Readiness explain | `/api/execution/candidates/explain` |
| Candidate Timeline | Derived candidate lifecycle events. | Candidate model | Derived | Candidate state | `/api/execution/candidates/timeline` |
| Candidate APIs | Read-only access to candidate and workflow bridge. | Derived candidate model | Derived | Wave 2 and operator previews | Admin/UI later |
| Candidate Admin Views | Local dirty worktree has drawer UI. | Admin UI layer | Deferred | Candidate APIs | Wave 4 |
| Candidate Events | Synthetic preview timeline only. | Candidate model | Derived | Candidate state | Timeline API |
| Candidate Lifecycle | DISCOVERED, CANDIDATE, VALIDATING, READY_FOR_REVIEW, BLOCKED, READY_FOR_CONTRACT, ARCHIVED, EXPIRED. | Candidate model | Derived | Validation and forecast | Candidate summary |

## APIs Integrated

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

## Verdict

candidate_inventory_complete=true
