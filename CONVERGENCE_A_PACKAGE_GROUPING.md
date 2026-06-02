# Convergence A Package Grouping

Project: V7 Vozduh
Block: Convergence A

## Package Groups

| Package | Included functionality | Source mix | Notes |
| --- | --- | --- | --- |
| Runtime Read APIs | execution summary/contracts/events/timeline/verification/rollback/explain | runtime-only vs `Updatesystem`, present in local | Wave 1 preservation package |
| Execution Draft | contract draft generation/detail/list | local-only | depends on proposal/evidence readers |
| Validation Preview | validation gates, readiness detail, validation evidence | local-only | fail-closed required |
| Simulation | outcome preview, blast radius, service impact, readiness forecast | local-only | preview-only |
| Rollback Preview | rollback preview and rollback impact | hybrid | must preserve runtime rollback read APIs |
| Candidate Workflow | candidate list/detail/readiness/risks/explain/timeline/workflow | local-only | P2.6/P2.7 |
| Approval/Governance/Rehearsal | candidate approval/governance/rehearsal plus shared operator previews | hybrid | split shared vs local-only |
| UI Integration | execution/candidate/gate/draft drawers and `/admin-v2` hooks | hybrid | must avoid dead hooks |
| Tests | unit/API/fail-closed/static route tests | local untracked plus future work | needs curation |
| Documentation | P2 reports/evidence and convergence reports | local untracked | needs curation |
| Runtime Support | `tools/runtime-support/*` and runtime helpers | mixed | compare hashes before migration |
| Systemd | service/timer units and drop-ins | runtime plus partial local | source mapping required |
| Tools | `tools/v7-*` and runtime `/usr/local/bin/v7-*` | mixed | many matched, some production-only |
| Branch/Release Governance | branch roles, manifests, release/default policy | documentation | required before deploy |

package_grouping_complete=true
