# Convergence D API Duplication Audit

Project: V7 Vozduh
Block: Convergence D

## API Inventory

Branch execution API paths:

- `/api/execution/summary`
- `/api/execution/contracts`
- `/api/execution/timeline`
- `/api/execution/events`
- `/api/execution/verification`
- `/api/execution/rollback`
- `/api/execution/explain`
- `/api/execution/contracts/draft`
- `/api/execution/validation-preview`
- `/api/execution/verification-preview`
- `/api/execution/rollback-preview`
- `/api/execution/readiness-preview`
- `/api/execution/gates`
- `/api/execution/readiness`
- `/api/execution/readiness/detail`
- `/api/execution/readiness/explain`
- `/api/execution/readiness/owners`
- `/api/execution/readiness/actions`
- `/api/execution/readiness/blockers`
- `/api/execution/readiness/reviews`
- `/api/execution/validation-evidence`
- `/api/execution/readiness-forecast`
- `/api/execution/rollback-impact`
- `/api/execution/candidates`
- `/api/execution/candidates/readiness`
- `/api/execution/candidates/risks`
- `/api/execution/candidates/explain`
- `/api/execution/candidates/timeline`
- `/api/execution/candidate-approval`
- `/api/execution/candidate-governance`
- `/api/execution/candidate-rehearsal`
- `/api/execution/candidate-workflow`

## Deferred Local-Only API Family

The dirty local main worktree contains three additional execution API paths that are not present in
the convergence branch:

- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`

These remain a known convergence risk because they overlap with internal branch helpers for candidate
outcome, blast radius, and service impact. They must be either migrated into the canonical execution
preview API family or explicitly retired in a later block.

## Duplication Findings

- Approval, governance, and rehearsal are exposed as candidate bridge APIs, not separate engines.
- Candidate workflow APIs reuse existing preview truth sources.
- No apply, run, execute, move, or route mutation API was added under `/api/execution`.
- No duplicate public approval queue API was found in the branch.

api_duplication_audit_complete=true
api_duplication_risk=MEDIUM
