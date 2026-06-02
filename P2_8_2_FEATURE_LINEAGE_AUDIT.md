# P2.8.2 Feature Lineage Audit

Project: V7 Vozduh
Block: P2.8.2

| Feature | Runtime | Local | GitHub | Canonical Source | Status |
| --- | --- | --- | --- | --- | --- |
| Authority | present through operator/governance read surfaces | present | `origin/Updatesystem` baseline | runtime for current behavior, `Updatesystem` for committed source | Partial |
| Candidate | not full P2.7 candidate workflow | full P2.7 candidate APIs/UI | absent from `origin/Updatesystem` | local candidate pending review | Local-only |
| Execution | read-only summary/contracts/events/timeline/verification/rollback/explain present | present plus draft/preview extensions | absent from `origin/Updatesystem`, present in runtime only | runtime for deployed read-only execution visibility | Runtime-only patch |
| Simulation | not full outcome simulation | outcome/blast-radius/service-impact/readiness forecast present | absent | local candidate | Local-only |
| Readiness | general readiness present | execution readiness suite present | partial/general only | local candidate | Local-only extension |
| Approval Center | operator approval preview present | candidate approval center present | operator preview baseline | local candidate for P2.7 approval | Partial |
| Governance Preview | operator execution governance preview present | present | `origin/Updatesystem` baseline | runtime/local/GitHub aligned enough for preview | Present |
| Rehearsal Preview | operator execution rehearsal preview present | present | `origin/Updatesystem` baseline | runtime/local/GitHub aligned enough for preview | Present |
| Execution Contracts | runtime read-only store APIs present | present plus draft preview | absent from `origin/Updatesystem` | runtime for deployed behavior | Runtime-only patch |
| Execution Events | runtime read-only event APIs present | present | absent from `origin/Updatesystem` | runtime for deployed behavior | Runtime-only patch |
| Operator Workflow | operator overview/timeline/evidence present | present plus candidate workflow | `origin/Updatesystem` baseline | runtime for live, local for next candidate | Partial |
| Validation Preview | absent | present | absent | local candidate | Local-only |
| Rollback Preview | runtime execution rollback read API and existing rollback preview helpers | rollback preview and impact preview present | partial | local candidate for P2.5/P2.6 previews | Partial |

feature_lineage_complete=true
