# Convergence C Wave 3 Workflow Consolidation

## Target Workflow

```text
Proposal -> Candidate -> Approval Center -> Governance Preview -> Rehearsal Preview
```

## Integrated API

- `/api/execution/candidate-workflow`

## Consolidation Decisions

| Path | Decision |
| --- | --- |
| Proposal to Draft Contract | Reuse Wave 2 draft package |
| Draft Contract to Candidate | Merge derived candidate model |
| Candidate to Approval Center | Reuse existing approval preview |
| Candidate to Governance Preview | Reuse existing governance preview |
| Candidate to Rehearsal Preview | Reuse existing rehearsal preview |
| Candidate Drawer UI | Defer |
| Execution apply path | Forbidden |

## Alternative Paths

No alternative executable path was added.

## Verdict

workflow_consolidation_complete=true
