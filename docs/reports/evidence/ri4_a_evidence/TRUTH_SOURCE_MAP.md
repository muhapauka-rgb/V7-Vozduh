# Truth Source Map

| Domain | Canonical truth source | Derived source | Owner | Ambiguity |
|---|---|---|---|---|
| channel quality | `egress-quality-summary.json`, `egress-quality-ring.json`, `v7-state.json`, `egress-speed.json` | `channel-service-scores.json` | quality compact + workers | low |
| service quality | `service-matrix.json` | `service-scores.json`, `channel-service-scores.json` | service matrix tools + workers | low |
| service history | service matrix + quality summary | `ServiceHistoryStore` read model | RI.1 | low if no new store is created |
| user preferences | `service-preferences.json`, policy/org policy | `UserServiceWeights`, future `user-service-scores.json` | RI.1 / policy owners | medium, user-service snapshot not production-confirmed |
| risk | derived from service/channel snapshots and quality/route reality | `risk-summaries.json` | PERF.3 risk worker | low |
| trust | audit/switch/rollback records | `trust-summaries.json` | `ExecutionTrustModel` + worker | low |
| blast radius advice | runtime active/affected counts + trust/risk | `blast-radius-summaries.json` | `DynamicBlastRadiusModel` + worker | low |
| candidate ranking | `tools/v7-users-autoswitch` | RI score part as bounded advice | runtime planner | no ambiguity: planner owns final decision |
| selected moves | `tools/v7-users-autoswitch` | none | runtime planner | no new writer allowed |
| snapshot generation | `tools/v7-intelligence-snapshot-refresh`, `admin_core/intelligence_workers.py` | snapshot files | Heavy Brain producers | systemd trigger missing |
| execution authorization | governance/operator approval packet flow | none | governance modules | RI has no authority |
| runtime execution | `tools/v7-users-autoswitch` through movement primitive | none | runtime owner | RI has no authority |

## Ambiguities To Carry Into RI.4

1. `user-service-scores.json` contract exists, but production-confirmed CONV.2 snapshot set does not include it.
2. `capacity-forecast-summaries.json` contract exists, but PERF.4 intentionally did not integrate it.
3. `prediction-summaries.json` contract exists, but prediction foundation is disabled and no production producer is confirmed.
4. Snapshot refresh CLI exists and works, but production systemd service/timer is missing.

