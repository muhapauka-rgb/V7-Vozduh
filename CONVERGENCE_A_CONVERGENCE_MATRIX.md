# Convergence A Convergence Matrix

Project: V7 Vozduh
Block: Convergence A

| Subsystem | Runtime | Local | GitHub | Canonical Candidate | Decision | Migration Wave | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Authority | present | present | `Updatesystem` | hybrid | Merge + Review | Governance | High |
| Candidate | partial/absent | present | absent | local | Keep Local + Review | Wave 4 | High |
| Execution | read APIs | expanded | absent from `Updatesystem` | hybrid | Keep Runtime + Merge Local | Waves 1-4 | Critical |
| Execution Contracts | read model | read + drafts | absent/partial | hybrid | Merge + Review | Waves 1-2 | High |
| Execution Events | read model | read model | absent/partial | runtime | Keep Runtime + Review | Wave 1 | High |
| Simulation | limited | present | absent | local | Keep Local + Review | Wave 3 | Medium/High |
| Readiness | general | expanded | partial | local/hybrid | Merge + Review | Wave 2 | High |
| Approval Center | operator preview | candidate approval | partial | local/hybrid | Merge + Review | Wave 4 | High |
| Governance Preview | present | present | present | shared | Keep Shared | Governance | Medium |
| Rehearsal Preview | present | present | present | shared | Keep Shared | Governance | Medium |
| Validation Preview | absent | present | absent | local | Keep Local + Review | Wave 2 | Medium |
| Rollback Preview | read/explain | preview/impact | partial | hybrid | Merge + Review | Wave 3 | High |
| Operator Workflow | present | expanded | baseline | hybrid | Merge + Review | Wave 5 | High |
| Evidence | present | present | present | shared/runtime stores | Keep Shared + Review | Wave 6 | Medium |
| Proposal | present | present | present | shared/runtime stores | Keep Shared + Review | Wave 6 | Medium |
| Runtime Trust | present | present | present | shared/runtime store | Keep Shared | Governance | Medium |
| Release Trust | present | present | present | Git/release store | Keep Shared | Governance | Medium |
| Users | live state | readers | source readers | runtime state | Keep Runtime State | no Git migration | High |
| Channels | live state | readers/tools | source readers/tools | runtime state | Keep Runtime State | no Git migration | High |
| Routing | live state | previews | source tools | runtime state | Keep Runtime State | no runtime mutation | High |
| Events | live stores | readers | partial source | runtime stores | Keep Runtime + Review | Wave 1/6 | Medium/High |
| Audit | live files | search/readers | baseline | runtime files + source | Keep Runtime + Review | Wave 6 | Medium |
| Admin UI | deployed | expanded | baseline | hybrid | Merge + Review | Wave 5 | High |
| APIs | deployed | expanded | baseline | hybrid | Merge + Review | Waves 1-5 | High |
| Tools | deployed | local tools | mostly source | per-hash | Merge/Archive | tools wave | High |
| Runtime Support | deployed | local support | source | per-hash | Merge/Review | tools wave | Medium/High |
| Systemd | production | partial | partial | runtime manifest | Review only | deploy-prep | High |

convergence_matrix_complete=true
