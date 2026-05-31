# Convergence C Wave 3 API Convergence Map

| API | Runtime | Convergence | Local | GitHub | Decision | Migration Method | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/api/execution/candidates` | Missing | Integrated | Present | Missing | Merge | Derived read model | Medium |
| `/api/execution/candidates/` | Missing | Integrated | Present | Missing | Merge | Derived detail | Medium |
| `/api/execution/candidates/readiness` | Missing | Integrated | Present | Missing | Merge | Reuse Wave 2 readiness | Medium |
| `/api/execution/candidates/risks` | Missing | Integrated | Present | Missing | Merge | Reuse Wave 2 impact helpers | Medium |
| `/api/execution/candidates/explain` | Missing | Integrated | Present | Missing | Merge | Reuse readiness explain | Medium |
| `/api/execution/candidates/timeline` | Missing | Integrated | Present | Missing | Merge | Synthetic preview timeline | Low |
| `/api/execution/candidate-approval` | Missing | Integrated | Present | Missing | Merge | Map to Approval Center | High |
| `/api/execution/candidate-governance` | Missing | Integrated | Present | Missing | Merge | Map to Governance Preview | High |
| `/api/execution/candidate-rehearsal` | Missing | Integrated | Present | Missing | Merge | Map to Rehearsal Preview | High |
| `/api/execution/candidate-workflow` | Missing | Integrated | Present | Missing | Merge | Consolidated workflow | High |
| `/api/execution/outcome-preview` | Missing | Deferred | Present | Missing | Reject for Wave 3 | None | Medium |
| `/api/execution/blast-radius` | Missing | Deferred | Present | Missing | Reject for Wave 3 | None | Medium |
| `/api/execution/service-impact` | Missing | Deferred | Present | Missing | Reject for Wave 3 | None | Medium |

## Verdict

api_convergence_map_complete=true
