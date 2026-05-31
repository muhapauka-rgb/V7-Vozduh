# Convergence D Terminology Audit

Project: V7 Vozduh
Block: Convergence D

## Canonical Terms

| Term | Canonical meaning |
|---|---|
| Execution contract | Stored runtime contract read model. |
| Draft contract | Preview-only derived contract candidate from proposal. |
| Candidate | Derived operator workflow item; not a persisted queue item. |
| Approval Center | Existing operator approval preview surface. |
| Governance Preview | Existing execution governance preview model. |
| Rehearsal Preview | Existing execution rehearsal preview model. |
| Readiness | Preview gate aggregation. |
| Rollback Preview | Non-executable rollback preparation model. |
| Dry-run architecture | Future design target, not implemented in this block. |

## Ambiguous Or Risky Terms

| Term | Risk | Required handling |
|---|---|---|
| Dry-run | Can imply execution | Use `preview` or `architecture candidate` unless execution is explicitly impossible. |
| Candidate approval | Can imply a new approval queue | State that it maps into Approval Center preview. |
| Simulation | Can imply an engine | State that branch contains derived helpers only. |
| Apply | Can imply mutation | Keep absent from execution UI/API except disabled explanatory text. |
| Rehearsal | Can imply live run | Keep marked `rehearsal_only` and `execution_allowed_now=false`. |

## Findings

Terminology is mostly consistent. The highest-risk terminology is around `dry-run` and `simulation`,
because those words can sound executable. Current branch copy and API flags keep those surfaces
preview-only.

terminology_audit_complete=true
terminology_risk=MEDIUM
