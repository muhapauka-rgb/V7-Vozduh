# Convergence A Package Decisions

Project: V7 Vozduh
Block: Convergence A

| Package | Decision | Reason | Migration Candidate |
| --- | --- | --- | --- |
| Runtime Read APIs | Keep Runtime + Review + Merge | deployed behavior exists only in runtime vs `Updatesystem` | Wave 1 |
| Execution Draft | Keep Local + Review | local candidate implements non-executable drafts | Wave 2 |
| Validation Preview | Keep Local + Review | local candidate implements fail-closed preview gates | Wave 2 |
| Simulation | Keep Local + Review | local candidate implements preview-only outcome models | Wave 3 |
| Rollback Preview | Merge + Review | runtime has read/explain, local has preview/impact | Wave 3 |
| Candidate Workflow | Keep Local + Review | local P2.6/P2.7 workflow is not deployed | Wave 4 |
| Approval/Governance/Rehearsal | Merge + Review | shared operator previews plus local candidate approval | Wave 4 |
| UI Integration | Merge + Review | runtime UI and local UI differ | Wave 5 |
| Tests | Review + Merge | local tests/reports need curated commit package | Wave 6 |
| Documentation | Review + Merge or Archive | many untracked reports; not all may be release docs | Wave 6 |
| Runtime Support | Merge after hash review | mixed runtime/repo ownership | later convergence wave |
| Systemd | Review, do not auto-copy | production units only partially mapped | deploy-prep wave only |
| Tools | Merge/Archive per hash | runtime has production-only tools | tools convergence wave |
| Branch/Release Governance | Keep docs + Review | required to prevent release truth drift | governance wave |

## Explicit Non-Decisions

No whole-file replacement is approved. No runtime copy is automatically canonical. No local dirty file is deploy-ready. No GitHub branch is current runtime source.

package_decisions_complete=true
