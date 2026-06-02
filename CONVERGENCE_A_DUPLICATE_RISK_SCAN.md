# Convergence A Duplicate Risk Scan

Project: V7 Vozduh
Block: Convergence A

This is a pre-scan only, not a full duplication audit.

| Potential Duplicate Candidate | Risk | Priority | Notes |
| --- | --- | --- | --- |
| Approval vs Candidate Approval | High | P1 | operator approval preview and P2.7 candidate approval can diverge |
| Simulation vs Rehearsal | Medium/High | P1 | simulation outcome previews and rehearsal preview may duplicate readiness semantics |
| Execution Events vs Audit Events | High | P1 | execution event store and audit/event logs need clear ownership |
| Readiness vs Validation | High | P1 | readiness APIs and validation preview gates can conflict |
| Authority vs Governance | High | P1 | authority source and governance preview must not both claim final truth |
| Rollback Read APIs vs Rollback Preview | Medium/High | P2 | runtime rollback read model and local rollback impact preview need merge rules |
| Evidence vs Proposal Timeline | Medium | P2 | evidence timeline and proposal timeline may duplicate event views |
| Runtime Trust vs Release Trust | Medium | P2 | runtime hash truth and release branch truth need separate roles |
| Admin UI drawers vs API route groups | Medium | P2 | local UI may reference APIs absent from runtime or branch baseline |

duplicate_risk_scan_complete=true
