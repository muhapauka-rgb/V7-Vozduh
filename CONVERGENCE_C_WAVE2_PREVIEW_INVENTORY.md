# Convergence C Wave 2 Preview Inventory

Project: V7 Vozduh
Block: Convergence C
Wave: 2
Date: 2026-05-31

## Inventory

| Feature | Purpose | Storage | API | UI | Dependencies | Truth source |
| --- | --- | --- | --- | --- | --- | --- |
| Draft Contracts | Derive non-executable draft contracts from proposal/evidence state. | Existing proposal/evidence/runtime state; no new write store. | `/api/execution/contracts/draft`, `/api/execution/contracts/draft/` | Local dirty worktree has Execution drawer fetches; not merged in Wave 2. | Proposals, evidence, users registry, egress registry. | Local dirty worktree |
| Validation Preview | Preview validation gates without execution. | Read-only adapters. | `/api/execution/validation-preview`, `/api/execution/validation-evidence` | Execution drawer in local dirty worktree; deferred. | Authority, evaluator, conflict, runtime trust, release trust, service/capacity/policy adapters. | Local dirty worktree |
| Verification Preview | Preview success criteria and verification expectations. | Derived from draft contract. | `/api/execution/verification-preview` | Execution drawer in local dirty worktree; deferred. | Draft contract, affected users, target. | Local dirty worktree |
| Rollback Preview | Preview rollback manifest and rollback verification expectations. | Derived from draft rollback manifest. | `/api/execution/rollback-preview` | Execution drawer in local dirty worktree; deferred. | Draft contract, users registry. | Local dirty worktree |
| Rollback Impact | Preview rollback scope and impact. | Derived from draft and helper impact model. | `/api/execution/rollback-impact` | Execution drawer in local dirty worktree; deferred. | Draft contract, affected users, target. | Local dirty worktree |
| Readiness | Summarize gate state and preview readiness. | Derived from previews and adapters. | `/api/execution/readiness`, `/api/execution/readiness-preview`, `/api/execution/readiness/detail` | Execution drawer in local dirty worktree; deferred. | Validation, verification, rollback, gate catalog. | Local dirty worktree |
| Gate Views | Explain gate states and operator ownership. | Derived from gate model. | `/api/execution/gates`, `/api/execution/gates/` | Checks/Execution drawer in local dirty worktree; deferred. | Gate operator model. | Local dirty worktree |
| Forecast Views | Preview readiness trajectory. | Derived from validation and blocker/review state. | `/api/execution/readiness-forecast` | Execution drawer in local dirty worktree; deferred. | Readiness, validation, rollback impact. | Local dirty worktree |
| Execution Health | Classify readiness as ready, degraded, blocked, or unknown. | Derived in response model. | Exposed inside readiness/explain responses. | Home/Checks candidate for later UI merge. | Readiness response. | Local dirty worktree |

## Wave 2 Public Route Set

- `/api/execution/contracts/draft`
- `/api/execution/contracts/draft/`
- `/api/execution/validation-preview`
- `/api/execution/validation-evidence`
- `/api/execution/verification-preview`
- `/api/execution/rollback-preview`
- `/api/execution/rollback-impact`
- `/api/execution/readiness-preview`
- `/api/execution/readiness`
- `/api/execution/readiness/detail`
- `/api/execution/readiness/explain`
- `/api/execution/readiness/owners`
- `/api/execution/readiness/actions`
- `/api/execution/readiness/blockers`
- `/api/execution/readiness/reviews`
- `/api/execution/readiness-forecast`
- `/api/execution/gates`
- `/api/execution/gates/`

## Verdict

preview_inventory_complete=true
