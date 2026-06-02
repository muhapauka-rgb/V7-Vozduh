# P2.8.5 Truth Source Review

Project: V7 Vozduh
Block: P2.8.5

| Domain | Current canonical source | Ownership resolved | Future source | Readiness |
| --- | --- | --- | --- | --- |
| Authority | runtime behavior plus `Updatesystem` source | yes | convergence branch + runtime manifest | verified |
| Candidate | local dirty candidate | yes, as local candidate only | reviewed package Wave 4 | verified |
| Execution | runtime read APIs | yes, as deployed behavior | Wave 1 preserved source | verified |
| Proposal | proposal stores and source readers | yes | convergence branch source | verified |
| Evidence | evidence stores and source readers | yes | convergence branch source | verified |
| Users | production runtime state | yes | runtime state plus manifest, not Git content | verified |
| Channels | production runtime state | yes | runtime state plus manifest, not Git content | verified |
| Routing | live runtime route state | yes | runtime state plus source manifest | verified |
| Events | runtime event stores | yes | runtime read model plus reviewed source | verified |
| Audit | production audit/event files | yes | secret-safe runtime audit policy | verified |
| Readiness | runtime/general plus local execution readiness | yes | reviewed readiness package | verified |
| Simulation | local preview candidate | yes | reviewed simulation package | verified |

## Decision

Canonical sources exist for the purpose of beginning convergence branch work. The unresolved Admin API source lineage remains a known blocker for deployment, not a blocker for a controlled branch-preparation phase.

truth_sources_verified=true
