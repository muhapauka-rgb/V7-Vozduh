# P2.8.4 Feature Convergence Map

Project: V7 Vozduh
Block: P2.8.4

| Feature | Runtime Version | Local Version | GitHub Version | Target Version | Migration Method |
| --- | --- | --- | --- | --- | --- |
| Authority | operator/governance surfaces present | present | `Updatesystem` baseline | shared source on convergence branch | verify no drift, carry forward |
| Candidate | partial/absent P2.7 | full P2.7 candidate workflow | absent | reviewed local candidate workflow | feature package 4 |
| Execution | read-only execution APIs | read APIs plus extensions | absent from `Updatesystem` | runtime read APIs preserved, local extensions reviewed | package 1 then packages 2-4 |
| Simulation | limited/absent | outcome/blast-radius/service-impact/readiness forecast | absent | reviewed local simulation previews | package 3 |
| Readiness | general readiness | execution readiness suite | partial/general | reviewed local readiness with fail-closed behavior | package 2/3 |
| Approval Center | operator approval preview | candidate approval center | operator baseline | local candidate approval plus shared operator preview | package 4 |
| Governance Preview | present | present | present | shared | preserve baseline |
| Rehearsal Preview | present | present | present | shared | preserve baseline |
| Execution Contracts | read model | read model plus drafts | absent from `Updatesystem` | runtime read model plus reviewed draft model | package 1 then 2 |
| Execution Events | read model | read model | absent from `Updatesystem` | runtime read model preserved | package 1 |
| Validation Preview | absent | present | absent | reviewed local validation preview | package 2 |
| Rollback Preview | rollback read/explain | rollback preview/impact | partial/operator rollback | merged rollback read and preview model | package 3 |
| Operator Workflow | operator overview/timeline/evidence | expanded candidate workflow | `Updatesystem` baseline | merged workflow | package 5 |

feature_convergence_complete=true
