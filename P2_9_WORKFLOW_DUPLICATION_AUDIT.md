# P2.9 Workflow Duplication Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Canonical Workflow

The current workflow remains:

Proposal -> Draft Contract Preview -> Candidate -> Approval Center Preview -> Governance Preview -> Rehearsal Preview -> Runtime Dry-Run Architecture Candidate

Execution is not part of this workflow.

## Reuse Map

| Step | Current owner | Duplication result |
|---|---|---|
| Proposal | Existing proposal store/read model | Reused |
| Draft Contract Preview | Execution preview helpers | Derived |
| Candidate | `execution_candidate_*` read model | Derived |
| Approval | `operator_approval_preview()` | Reused |
| Governance | `operator_execution_governance_preview()` | Reused |
| Rehearsal | `operator_execution_rehearsal_preview()` | Reused |
| Dry-run preparation | preview models only | Not executable |

## Findings

No candidate workflow engine, approval workflow engine, governance workflow engine, rehearsal engine,
runtime dry-run executor, routing apply hook, or user movement flow was found in the convergence
workflow layer.

workflow_duplication_risk=LOW
dangerous_parallel_workflows_found=false
execution_engine_implemented=false
runtime_hooks_implemented=false
