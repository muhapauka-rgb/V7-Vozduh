# Convergence D Responsibility Audit

Project: V7 Vozduh
Block: Convergence D

## Responsibility Map

| Responsibility | Owner in branch | Notes |
|---|---|---|
| Runtime execution contract reading | Execution read API layer | Reads existing execution contract store. |
| Runtime execution event reading | Execution read API layer | Reads existing execution event log. |
| Draft generation | Execution preview layer | Derived from proposal state. |
| Validation preview | Execution preview layer | Read-only, fail-closed. |
| Verification preview | Execution preview layer | Read-only. |
| Rollback preview | Execution preview layer | Read-only. |
| Candidate derivation | Candidate workflow layer | Derived from drafts and proposal references. |
| Candidate approval bridge | Approval Center preview | Reuses existing approval model. |
| Candidate governance bridge | Governance preview | Reuses existing governance model. |
| Candidate rehearsal bridge | Rehearsal preview | Reuses existing rehearsal model. |
| Operator UI | Existing admin-v2 surfaces | No new top-level section. |
| Retention | Existing P2.5 retention architecture | No cleanup was executed in this audit. |

## Separation Of Duties

- Read APIs own presentation and normalization, not mutation.
- Candidate layer owns derivation, not authority.
- Approval Center remains the approval truth source.
- Governance preview remains the governance truth source.
- Rehearsal preview remains the rehearsal truth source.
- Runtime dry-run architecture remains future work.

responsibility_audit_complete=true
responsibility_risk=LOW
