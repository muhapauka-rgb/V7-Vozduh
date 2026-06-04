# RI Reality Map

Program: RI4-A reality discovery, reuse and readiness audit

Mode: read-only repository/report audit

## Discovered RI Components

| Component | Owner | Purpose | Inputs | Outputs | Runtime consumers | Classification |
|---|---|---|---|---|---|---|
| `admin_core/routing_intelligence.py` | RI.1 read model owner | Service history, service intelligence, user weights, execution trust, dynamic blast radius, disabled prediction foundation, shadow replay | `service-matrix.json`, `egress-quality-summary.json`, `service-preferences.json`, audit/switch history | non-authoritative read models and advisory scores | Routing Brain, shadow CLI, workers | REUSE / EXTEND |
| `admin_core/routing_brain.py` | RI.2/RI.3 advisory owner | Connect RI.1 models to planner advisory context and bounded candidate score parts | service matrix, quality summary, service preferences, audit records | `ri2.routing-brain-advisory.v1`, `ri3.candidate-advisory-scores.v1` | `tools/v7-users-autoswitch` fallback path | REUSE / EXTEND |
| `admin_core/intelligence_snapshots.py` | PERF.2 snapshot contract owner | Snapshot family contracts, envelope, freshness/confidence/stop model, bounded readers | snapshot root files | `SnapshotReadResult`, runtime read contract | `tools/v7-users-autoswitch`, tests, truth/deploy tooling | REUSE |
| `admin_core/intelligence_workers.py` | PERF.3 Heavy Brain producer owner | Builds compact intelligence snapshots | service matrix, quality summary, preferences, audit/switch/rollback records, registries, runtime state | six currently produced snapshots | `tools/v7-intelligence-snapshot-refresh` | REUSE / EXTEND |
| `tools/v7-routing-intelligence-shadow` | RI.1 CLI owner | Read-only shadow replay | runtime state dir/event dir or explicit files | RI shadow JSON | operator/developer evidence only | REUSE |
| `tools/v7-intelligence-snapshot-refresh` | PERF.3 CLI owner | Builds/writes intelligence snapshots, dry-run supported | `/opt/v7/egress/state`, `/opt/v7/events` | snapshot refresh result and snapshot files | production snapshot subsystem | REUSE / EXTEND |
| `tools/v7-users-autoswitch` | runtime planner owner | Runtime planning/execution owner; consumes RI advice/snapshots only as bounded input | runtime truth, policy, service matrix, quality summary, snapshots, restore barrier | selected moves, safety gates, terminal runtime result | production runtime | DO_NOT_TOUCH decision authority; EXTEND only through existing hooks |

## Existing Contracts

Routing Brain advisory contract forbids:

- moving users;
- bypassing planner;
- bypassing governance;
- directly writing selected moves;
- approving execution;
- mutating runtime state.

Snapshot runtime gate forbids:

- snapshot write authority inside runtime;
- execution authority inside snapshots;
- selected move write authority inside snapshots;
- hard gate override;
- reservation override.

## Primary Finding

RI.4 should not create a new RI system.

RI.4 must reuse:

- `ServiceHistoryStore`;
- `ServiceIntelligenceEngine`;
- `UserServiceWeights`;
- `ExecutionTrustModel`;
- `DynamicBlastRadiusModel`;
- `RoutingBrain`;
- snapshot envelope/family contracts;
- snapshot worker/refresh CLI;
- `tools/v7-users-autoswitch` fast path.

## Evidence

- `admin_core/routing_intelligence.py`
- `admin_core/routing_brain.py`
- `admin_core/intelligence_snapshots.py`
- `admin_core/intelligence_workers.py`
- `tools/v7-users-autoswitch`
- `tools/v7-routing-intelligence-shadow`
- `tools/v7-intelligence-snapshot-refresh`
- `PROGRAM_RI1_ROUTING_INTELLIGENCE_FOUNDATION_REPORT.md`
- `PROGRAM_RI2_ROUTING_BRAIN_INTEGRATION_REPORT.md`
- `PROGRAM_RI3_ADVISORY_DECISION_INTEGRATION_AND_ROUTING_INTELLIGENCE_CERTIFICATION_REPORT.md`
- `PROGRAM_PERF4_RUNTIME_FAST_PATH_INTEGRATION_AND_PERFORMANCE_CERTIFICATION_REPORT.md`

