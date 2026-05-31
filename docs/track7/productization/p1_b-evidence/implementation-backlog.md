# P1.B Implementation Backlog

implementation_backlog_defined=true

## P0 — Required

| Item | Outcome |
| --- | --- |
| Proposal Store | Durable proposal metadata, lifecycle, evidence links and closure records. |
| Proposal API | Admin can list proposals, open one proposal and query by current object. |
| Proposal Drawer Component | Shared drawer for overview, routes, users and channels. |
| Evidence Link Requirement | Proposal cannot be created without Evidence Bundle reference. |
| Proposal Chips / Row Indicators | Existing tables can show proposal availability and status. |
| Governance Path Summary | Drawer explains how proposal enters batch/policy/capacity/concurrency/scheduling. |
| Expiration/Freshness Contract | Stale proposals fail closed and cannot execute. |

## P1 — Production

| Item | Outcome |
| --- | --- |
| Proposal Refresh Flow | Evidence or runtime drift can refresh/supersede proposals. |
| Proposal Closure Workflow | Operators can close/reject proposals with reason and audit. |
| Proposal Search | Search by user, target, service, status, confidence, severity. |
| Batch Conversion API | Role-gated conversion from active proposal to governed batch. |
| Required Services Integration | Proposals explain service satisfaction explicitly. |
| Policy Trace Integration | Proposal drawer shows policy allow/deny/review reason. |
| Proposal Timeline | Lifecycle and governance references are visible. |

## P2 — Future

| Item | Outcome |
| --- | --- |
| Proposal Correlation | Related proposals are grouped to reduce operator noise. |
| Multi-Target Alternatives | Drawer compares candidate targets. |
| Operator Feedback Loop | Accepted/rejected proposals improve future confidence. |
| Production Pool Proposals | Proposal System supports multi-target production pool scheduling. |
| AI-Drafted Rationale | Optional draft explanation, never authority. |

## Backlog Verdict

P0 makes proposals visible and evidence-linked. P1 makes them production-grade and governable. P2 improves scale and operator ergonomics.
