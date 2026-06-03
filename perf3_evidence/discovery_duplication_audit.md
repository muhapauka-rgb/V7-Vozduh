# PERF.3 Discovery and Duplication Audit

Mode: local implementation and tests only. No runtime access, deploy, service restart, user movement, autoswitch apply, planner integration, or governance change was performed.

## Existing Logic Reused

| Area | Reused owner |
|---|---|
| service history model | `admin_core.routing_intelligence.ServiceHistoryStore` |
| service scoring | `admin_core.routing_intelligence.ServiceIntelligenceEngine` |
| user service weights | `admin_core.routing_intelligence.UserServiceWeights` |
| execution trust scoring | `admin_core.routing_intelligence.ExecutionTrustModel` |
| dynamic blast radius recommendation | `admin_core.routing_intelligence.DynamicBlastRadiusModel` |
| snapshot envelope and validation | `admin_core.intelligence_snapshots` |
| registry parsing | `admin_core.registry_readers` |

## New Producers

- `admin_core.intelligence_workers`
- `tools/v7-intelligence-snapshot-refresh`

These are producer-only. They do not integrate with runtime planner decisions.

## Duplicate Generation Audit

- duplicate service score generation: no duplicate truth source added; worker reuses RI service scoring.
- duplicate trust generation: no duplicate model added; worker reuses `ExecutionTrustModel`.
- duplicate risk generation: compact worker output derived from service/channel snapshots.
- duplicate blast radius generation: no duplicate model added; worker reuses `DynamicBlastRadiusModel`.
- duplicate overview generation: admin-only compact summary for future fast overview, not connected to API behavior.

## Producer Priority Decision

First producers created:

1. Service score worker
2. Trust worker
3. Risk worker
4. Blast radius worker
5. Overview summary worker

Not created in PERF.3:

- user-service-scores producer
- capacity-forecast producer
- prediction-summaries producer

Those remain future work after the first foundation is certified.
