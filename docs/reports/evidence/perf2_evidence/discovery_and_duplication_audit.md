# PERF.2 Discovery and Duplication Audit

Mode: read-only code discovery plus interface implementation. No runtime behavior, planner behavior, governance, execution, or deployment changes were made.

## Existing Producers

| Source | Current owner | Future snapshot producer role |
|---|---|---|
| Service matrix | `tools/v7-service-matrix-test` | service score worker input |
| Quality summaries | `tools/v7-egress-quality-compact` | channel/service score worker input |
| Service preferences | runtime state / RI read models | user-service score input |
| Execution trust | `admin_core.routing_intelligence.ExecutionTrustModel` | trust summary worker model |
| Dynamic blast radius | `admin_core.routing_intelligence.DynamicBlastRadiusModel` | blast-radius summary model |
| Routing Brain | `admin_core.routing_brain.RoutingBrain` | future snapshot consumer/producer of advisory summaries |
| Overview summaries | API.4/API.5 read views | admin overview snapshot consumer |

## Future Consumers

| Consumer | May read snapshots | Must not read |
|---|---|---|
| Runtime planner | compact snapshot families | raw history, JSONL, probes, SQLite rollups, prediction engines |
| Governance | snapshot freshness/hash metadata | heavy service calculations |
| Admin API | overview and diagnostic summaries | hidden live probes on page load |
| Heavy Brain | all raw inputs | runtime selected move authority |

## Duplication Audit

No canonical intelligence snapshot store existed before PERF.2.

Existing snapshot-like concepts are not duplicates:

- runtime truth snapshots: repository/runtime convergence and provenance
- request snapshots: API request-local registry/read aggregation
- quality summary/ring: source inputs for Heavy Brain
- service matrix: diagnostic probe output, not canonical intelligence contract

PERF.2 creates the canonical interface contract without creating a new truth source for calculations.

## Duplicate Store Risk

- service scores: no duplicate canonical store found
- trust summaries: no duplicate canonical store found
- risk summaries: no duplicate canonical store found
- blast radius summaries: current model exists, canonical snapshot did not
- planner inputs: planner currently reads raw compact inputs directly; PERF.2 does not change that behavior
