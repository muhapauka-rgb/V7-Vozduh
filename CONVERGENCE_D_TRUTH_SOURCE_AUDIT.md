# Convergence D Truth Source Audit

Project: V7 Vozduh
Block: Convergence D

## Canonical Truth Sources

| Domain | Truth source | Branch behavior | Duplication verdict |
|---|---|---|---|
| Execution contracts | `EXECUTION_CONTRACTS_FILE` | Existing runtime contract store is read and normalized. | No duplicate store. |
| Execution events | `EXECUTION_EVENTS_FILE` | Existing runtime event log is read and normalized. | No duplicate event stream. |
| Admin audit | `AUDIT_FILE` | Existing admin audit tail is reused. | No duplicate audit log. |
| Proposals | Existing proposal read models | Execution drafts and candidates derive from proposals. | No duplicate proposal store. |
| Draft contracts | Derived from proposals and previews | Drafts are transient read models. | No draft persistence introduced. |
| Readiness | Preview gates and validation adapters | Derived from existing state and preview checks. | No readiness store introduced. |
| Candidate | Derived candidate model | Candidate ids and lifecycle are computed from draft/proposal state. | No candidate store introduced. |
| Approval | `operator_approval_preview()` | Candidate approval maps to existing Approval Center preview. | No approval queue introduced. |
| Governance | `operator_execution_governance_preview()` | Candidate governance maps to existing governance preview. | No governance store introduced. |
| Rehearsal | `operator_execution_rehearsal_preview()` | Candidate rehearsal maps to existing rehearsal preview. | No rehearsal store introduced. |
| Rollback | Rollback preview and rollback impact models | Rollback remains preview-only. | No rollback executor introduced. |
| Routing | Existing route registry/state | Execution surfaces read routing-related state only. | No routing apply path introduced. |
| Users | Existing user/channel state | Execution surfaces count and explain affected users only. | No user movement path introduced. |

## Truth Source Boundaries

- Candidate is a bridge read model, not a system of record.
- Approval remains the existing operator approval preview, not a new queue.
- Governance and rehearsal remain existing preview functions, not a new workflow engine.
- Execution event history comes from the existing event log plus synthetic derived timelines for display.
- Simulation/outcome data is derived internally and not yet promoted to public API truth source in the branch.

## Findings

- Truth sources are explicit in returned lineage fields.
- The branch repeatedly marks derived surfaces as `read_only`, `non_authoritative`, or `preview_only`.
- No hidden authoritative source was found for candidate approval, governance, rehearsal, or dry-run execution.

truth_source_audit_complete=true
