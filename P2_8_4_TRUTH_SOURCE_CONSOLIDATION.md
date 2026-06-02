# P2.8.4 Truth Source Consolidation

Project: V7 Vozduh
Block: P2.8.4

| Domain | Current Canonical Source | Future Canonical Source | Migration Requirement |
| --- | --- | --- | --- |
| Authority | runtime behavior plus `Updatesystem` source | convergence branch source plus runtime manifest | preserve runtime behavior, review source |
| Candidate | local dirty candidate | reviewed convergence package | tests and retention review |
| Execution | runtime read APIs for live behavior | reviewed runtime-read package plus local extensions | preserve runtime APIs |
| Proposal | proposal stores and `Updatesystem` source | convergence branch source | schema consistency |
| Evidence | evidence stores and `Updatesystem` source | convergence branch source | no duplicate evidence stores |
| Users | production `/opt/v7` state | runtime state plus manifest | do not copy live user data into Git |
| Channels | production egress/channel state | runtime state plus manifest | do not copy live channel state into Git |
| Routing | live route/runtime state | runtime state plus source manifest | no routing mutation during convergence |
| Readiness | runtime/general plus local execution readiness | reviewed readiness package | fail-closed tests |
| Simulation | local preview candidate | reviewed simulation package | deterministic fixtures |
| Events | runtime execution/event stores | runtime read model plus reviewed event readers | preserve event semantics |
| Audit | production audit/event files | runtime audit source plus documentation | secret-safe audit handling |

truth_source_consolidation_complete=true
