# P2.8.3 Feature Lineage Matrix

Project: V7 Vozduh
Block: P2.8.3

| Subsystem | Runtime Version | Local Version | GitHub Version | Canonical Candidate |
| --- | --- | --- | --- | --- |
| Authority | present through operator/governance views | present plus P2 local additions | `origin/Updatesystem` baseline | Hybrid: runtime behavior plus `Updatesystem` source |
| Candidate | partial/absent P2.7 workflow | full candidate review/approval/governance/rehearsal/workflow | absent from `origin/Updatesystem` | Local after review |
| Execution | read-only summary/contracts/events/timeline/verification/rollback/explain | runtime read APIs plus draft/preview extensions | absent from `origin/Updatesystem` | Hybrid: preserve runtime read APIs, review local extensions |
| Simulation | limited or absent | outcome/blast-radius/service-impact/readiness forecast | absent | Local after review |
| Readiness | general readiness surfaces | execution readiness suite | partial/general | Local after review |
| Approval Center | operator approval preview | candidate approval center | operator preview baseline | Local candidate plus shared operator preview |
| Governance Preview | present | present | present in `Updatesystem` | Shared baseline |
| Rehearsal Preview | present | present | present in `Updatesystem` | Shared baseline |
| Execution Contracts | runtime read model | read model plus draft model | absent from `Updatesystem` | Runtime read model preserved; local draft reviewed |
| Execution Events | runtime read model | present | absent from `Updatesystem` | Runtime preserved |
| Validation Preview | absent | present | absent | Local after review |
| Rollback Preview | partial rollback/explain read model | rollback preview and impact preview | partial/operator rollback baseline | Hybrid |
| Operator Workflow | operator observability present | expanded with candidate workflow | `Updatesystem` baseline | Hybrid |

## Lineage Interpretation

Runtime is canonical for current deployed behavior. `origin/Updatesystem` is canonical for committed development baseline. Local dirty work is canonical only as a candidate design/implementation patch. No single file is currently canonical for all subsystems.

feature_lineage_complete=true
