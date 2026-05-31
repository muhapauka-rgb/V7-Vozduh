# P2.9 UI Duplication Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Scope

Audited `admin-v2` static UI embedded in `admin/v7-admin-api`, UI routing helpers, operator panel,
execution drawers, and UI contract tests.

## Findings

No new top-level admin section was introduced for Candidate, Approval, Governance, Rehearsal,
Simulation, Rollback, Validation, Readiness, or Dry-Run.

Canonical UI reuse:

- Approval Center appears inside the existing `operator` section.
- Candidate workflow renders in `operatorCandidateWorkflow`.
- Governance Preview renders in `operatorExecutionGovernance`.
- Rehearsal Preview renders in `operatorExecutionRehearsal`.
- Execution details reuse the existing Execution drawer family through `openExecutionSummaryDrawer`,
  `openExecutionCandidateDrawer`, `openExecutionDraftDrawer`, `openExecutionGateDrawer`, and
  `openExecutionContractDrawer`.

Contract tests assert single drawer function occurrences for the execution summary and candidate
drawer paths.

## Risk

UI duplication risk is LOW. The UI has one admin shell, one operator section, and one execution drawer
family for convergence surfaces.

ui_duplication_risk=LOW
admin_navigation_duplication_found=false
runtime_mutation_performed=false
