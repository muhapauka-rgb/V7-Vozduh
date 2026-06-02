# P2.8.2 Runtime Local Diff

Project: V7 Vozduh
Block: P2.8.2

## Hashes

| Source | Hash |
| --- | --- |
| Runtime `/usr/local/bin/v7-admin-api` | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` |
| Local `admin/v7-admin-api` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` |

## Diff Size

`git diff --no-index --stat --numstat /private/tmp/p2_8_2-runtime-v7-admin-api admin/v7-admin-api`:

| Insertions from runtime to local | Deletions from runtime to local |
| ---: | ---: |
| 2679 | 10 |

## What Differs

### Routes

Local contains all detected runtime routes plus 31 extra routes:

`/api/execution/blast-radius`, `/api/execution/candidate-approval`, `/api/execution/candidate-governance`, `/api/execution/candidate-rehearsal`, `/api/execution/candidate-workflow`, `/api/execution/candidates`, `/api/execution/candidates/`, `/api/execution/candidates/explain`, `/api/execution/candidates/readiness`, `/api/execution/candidates/risks`, `/api/execution/candidates/timeline`, `/api/execution/contracts/draft`, `/api/execution/contracts/draft/`, `/api/execution/gates`, `/api/execution/gates/`, `/api/execution/outcome-preview`, `/api/execution/readiness`, `/api/execution/readiness-forecast`, `/api/execution/readiness-preview`, `/api/execution/readiness/actions`, `/api/execution/readiness/blockers`, `/api/execution/readiness/detail`, `/api/execution/readiness/explain`, `/api/execution/readiness/owners`, `/api/execution/readiness/reviews`, `/api/execution/rollback-impact`, `/api/execution/rollback-preview`, `/api/execution/service-impact`, `/api/execution/validation-evidence`, `/api/execution/validation-preview`, `/api/execution/verification-preview`.

Runtime has no detected route absent from local.

### Functions And Helpers

Local-only Python functions include:

- execution contract draft helpers
- validation gate adapter/readiness helpers
- validation/verification/rollback preview helpers
- outcome preview, blast radius, service impact, readiness forecast helpers
- execution candidate lifecycle/risk/detail helpers
- P2.7 candidate approval, governance, rehearsal, and workflow helpers

Runtime-only Python execution functions: none detected.

### UI

Local-only JS/UI functions include:

`executionCandidateApprovalHtml`, `executionCandidateExplainHtml`, `executionCandidateGovernanceHtml`, `executionCandidateListHtml`, `executionCandidateReadinessHtml`, `executionCandidateRehearsalHtml`, `executionCandidateRiskHtml`, `executionCandidateWorkflowHtml`, `executionOperatorQuestionsHtml`, `executionRollbackImpactHtml`, `openExecutionCandidateDrawer`, `openExecutionDraftDrawer`, `openExecutionGateDrawer`, `renderOperatorCandidateWorkflow`.

Runtime-only execution UI functions: none detected.

### Imports

Top-level imports are the same between runtime and local.

### Execution Features

Local extends runtime. Runtime already has read-only execution summary/contracts/events/timeline/verification/rollback/explain. Local adds draft, validation preview, readiness, simulation, candidate review/approval/governance/rehearsal/workflow, and dry-run preparation surfaces.

runtime_local_diff_understood=true
