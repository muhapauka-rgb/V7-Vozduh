# Convergence A Feature Lineage

Project: V7 Vozduh
Block: Convergence A

| Subsystem | Runtime Version | Local Version | GitHub Version | Origin | Known Lineage | Unknown Lineage | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Authority | runtime/operator surfaces | local expanded | `Updatesystem` baseline | P2/E governance | partial | exact runtime deploy commit | High |
| Candidate | partial/absent | full P2.7 workflow | absent | local P2.6/P2.7 work | local functions/docs | deploy status | High |
| Execution | read APIs present | read + draft/preview | absent from `Updatesystem` | runtime-only patch + local P2 | runtime path/hash known | runtime source commit | Critical |
| Execution Contracts | read model | read + drafts | absent/partial | runtime/local split | runtime APIs and local draft helpers | runtime commit | High |
| Execution Events | read model | read model | absent/partial | runtime-only patch | runtime APIs known | source commit | High |
| Simulation | absent/limited | local preview | absent | local P2.5 | local code/docs | runtime status | Medium/High |
| Readiness | general | local execution readiness | partial | local P2.3 plus runtime baseline | local code/docs | runtime equivalence | High |
| Approval Center | operator preview | candidate approval center | operator baseline | P2.7 local | local docs/tests | deployment lineage | High |
| Governance Preview | present | present | present | `Updatesystem` lineage | known in source | none material | Medium |
| Rehearsal Preview | present | present | present | `Updatesystem` lineage | known in source | none material | Medium |
| Validation Preview | absent | present | absent | local P2.3 | local code/docs | none in runtime | Medium |
| Rollback Preview | read/explain | preview/impact | partial | hybrid | runtime/local split known | replacement safety | High |
| Operator Workflow | present | expanded | baseline | hybrid | source baseline known | runtime patch source | High |
| Evidence | present | present | present | `Updatesystem` | mostly known | runtime store content | Medium |
| Proposal | present | present | present | `Updatesystem` | mostly known | runtime store content | Medium |
| Runtime Trust | present | present | present | P1 trust work | mostly known | runtime store content | Medium |
| Release Trust | present | present | present | P1 trust work | mostly known | release/default policy | Medium |
| Users | runtime live | readers only | source readers | production runtime | runtime state known as truth | no Git truth for live users | High |
| Channels | runtime live | readers/tools | source tools | production runtime | runtime state known as truth | no Git truth for live channels | High |
| Routing | runtime live | previews/readers | source tools | production runtime | runtime state known as truth | no Git truth for live routes | High |
| Events | runtime live | readers | source partial | production/Admin | runtime state known as truth | retention/source split | Medium/High |
| Audit | runtime live | readers/search | source baseline | production/Admin | source readers known | audit data ownership | Medium |
| Admin UI | deployed runtime UI | expanded local UI | `Updatesystem` baseline | hybrid | feature diffs known | runtime source commit | High |
| APIs | deployed runtime APIs | expanded local APIs | `Updatesystem` baseline | hybrid | route diffs known | runtime source commit | High |
| Tools | deployed runtime tools | local tools | mostly `Updatesystem` | mixed | many hashes matched in P2.8.1 | production-only tools remain | High |
| Runtime Support | deployed support scripts | local support scripts | `Updatesystem` | mixed | many local paths exist | runtime-only helpers | Medium/High |
| Systemd | production units | partial local units | partial source | runtime | unit paths/hashes known | incomplete local mapping | High |

lineage_complete=true
