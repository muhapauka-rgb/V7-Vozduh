# Convergence A Truth Source Review

Project: V7 Vozduh
Block: Convergence A

| Domain | Current Canonical Source | Future Canonical Source | Migration Need | Risk |
| --- | --- | --- | --- | --- |
| Authority | runtime behavior + `Updatesystem` source | convergence source + runtime manifest | preserve behavior, review source | High |
| Candidate | local dirty candidate | reviewed Wave 4 source | tests and retention review | High |
| Execution | runtime read APIs | Wave 1 preserved source + reviewed extensions | backport/preserve runtime APIs | Critical |
| Proposal | proposal stores/source readers | convergence source | schema consistency | Medium |
| Evidence | evidence stores/source readers | convergence source | avoid duplicate evidence stores | Medium |
| Users | production runtime state | runtime state + manifest | do not copy live state to Git | High |
| Channels | production runtime state | runtime state + manifest | do not copy live state to Git | High |
| Routing | live runtime route state | runtime state + source manifest | no mutation during convergence | High |
| Readiness | runtime/general + local execution readiness | reviewed readiness package | fail-closed tests | High |
| Simulation | local preview candidate | reviewed simulation package | deterministic fixtures | Medium/High |
| Events | runtime event stores | runtime read model + reviewed source | retention/source mapping | Medium/High |
| Audit | production audit files + source readers | secret-safe audit policy + source | ownership and redaction | Medium |

truth_sources_reviewed=true
