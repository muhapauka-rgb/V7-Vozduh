# PROGRAM RI4-A - Reality Discovery, Reuse And Readiness Audit Report

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-04

Mode: read-only discovery/audit

Evidence folder: `ri4_a_evidence`

## 1. Executive Verdict

RI.4 is ready to begin implementation, but only as an extension of existing V7 Routing Intelligence, Heavy Brain snapshot, and runtime planner hooks.

RI.4 must not create:

- a new Routing Intelligence system;
- a new service history store;
- a new snapshot root;
- a new planner;
- a new governance path;
- a new execution path;
- a new selected move writer.

The current system already contains most RI.4 building blocks:

- `admin_core/routing_intelligence.py`;
- `admin_core/routing_brain.py`;
- `admin_core/intelligence_workers.py`;
- `admin_core/intelligence_snapshots.py`;
- `tools/v7-routing-intelligence-shadow`;
- `tools/v7-intelligence-snapshot-refresh`;
- `tools/v7-users-autoswitch` runtime fast path.

Production convergence is already certified by CONV.2:

```text
perf4_deployed=true
snapshot_subsystem_verified=true
truth_check_pass=true
local_github_production_aligned=true
safe_to_begin_RI4=true
```

No implementation, runtime mutation, deploy, user movement, governance change, autoswitch apply, route mutation, state mutation, config mutation, service restart, commit, or push was performed in RI4-A.

## 2. Safety Statement

Performed:

- repository code audit;
- existing report audit;
- dependency/ownership/truth-source mapping;
- documentation/evidence creation only.

Not performed:

- runtime mutation;
- deploy;
- user movement;
- governance changes;
- autoswitch apply;
- route mutation;
- state/config mutation;
- service restart;
- RI.4 implementation;
- commit;
- push.

Documentation files were created because the prompt requires report/evidence outputs. No runtime or application code was modified.

## 3. Phase 1 - Routing Intelligence Reality Audit

Output: `ri4_a_evidence/RI_REALITY_MAP.md`

Discovered components:

| Component | Purpose | Classification |
|---|---|---|
| `admin_core/routing_intelligence.py` | RI.1 read models: service history, service scoring, user weights, trust, blast radius, disabled prediction, shadow replay | REUSE / EXTEND |
| `admin_core/routing_brain.py` | RI.2/RI.3 advisory contract and candidate score part | REUSE / EXTEND |
| `admin_core/intelligence_workers.py` | Heavy Brain snapshot producers | REUSE / EXTEND |
| `admin_core/intelligence_snapshots.py` | snapshot root, envelope, families, freshness/confidence/stop model | REUSE |
| `tools/v7-routing-intelligence-shadow` | read-only shadow replay CLI | REUSE |
| `tools/v7-intelligence-snapshot-refresh` | snapshot refresh CLI | REUSE / EXTEND |
| `tools/v7-users-autoswitch` | runtime planner/executor and snapshot fast path | DO_NOT_TOUCH authority; EXTEND only through existing hooks |

Primary finding:

RI.4 must be built on existing RI and snapshot architecture. Creating another model layer would duplicate truth and authority.

## 4. Phase 2 - Service Intelligence Audit

Output: `ri4_a_evidence/SERVICE_INTELLIGENCE_REALITY_MAP.md`

Existing service intelligence:

- service catalog in `tools/v7-service-matrix-test`;
- service matrix refresh in `tools/v7-service-matrix-refresh-all`;
- service truth in `/opt/v7/egress/state/service-matrix.json`;
- service history read model in `ServiceHistoryStore`;
- service scoring in `ServiceIntelligenceEngine`;
- user service weights in `UserServiceWeights`;
- service/channel snapshots in `service-scores.json` and `channel-service-scores.json`;
- native runtime service suitability in `tools/v7-users-autoswitch`;
- admin service views in `admin_core/service_views.py`.

RI.4 classification:

```text
service matrix: REUSE
service history: EXTEND
service scores: EXTEND
user service weights: EXTEND
new service truth source: DO_NOT_CREATE
```

## 5. Phase 3 - Channel Quality Audit

Output: `ri4_a_evidence/CHANNEL_QUALITY_REALITY_MAP.md`

Existing channel quality logic:

- service reachability and latency from service matrix checks;
- speed/throughput from runtime state and speed state;
- stability/fail rate/latency quality compaction in `tools/v7-egress-quality-compact`;
- quality summary in `/opt/v7/egress/state/egress-quality-summary.json`;
- bounded quality ring in `/opt/v7/egress/state/egress-quality-ring.json`;
- RI service scoring uses availability, latency, throughput, error rate, stability, confidence and freshness.

RI.4 verdict:

Channel quality measurement and summary already exist. RI.4 should reuse those stores and extend existing scoring only where needed.

## 6. Phase 4 - Channel History Audit

Output: `ri4_a_evidence/CHANNEL_HISTORY_REALITY_MAP.md`

Existing historical intelligence:

- quality EMA windows: `5m`, `1h`, `24h`, `7d`;
- bounded ring retention: default max 2000 samples;
- RI service history windows: `1h`, `24h`, `7d`, `30d`;
- bounded audit/switch/rollback reads in snapshot workers;
- service matrix refresh event JSONL.

Missing/partial:

- production-confirmed `prediction-summaries.json`;
- production-confirmed `capacity-forecast-summaries.json`;
- production-confirmed `user-service-scores.json`.

RI.4 verdict:

No new channel history store should be created.

## 7. Phase 5 - Risk Model Audit

Output: `ri4_a_evidence/RISK_REALITY_MAP.md`

Risk already exists through:

- `RoutingBrain` service risk/degradation risk;
- `DynamicBlastRadiusModel` risk input;
- `admin_core/intelligence_workers.py::build_risk_snapshot`;
- `risk-summaries.json`;
- runtime snapshot gate in `tools/v7-users-autoswitch`.

Active runtime consumption:

`risk-summaries.json` is runtime-required for intelligence apply. Unsafe risk snapshot truth can stop selected moves when the snapshot gate is active.

RI.4 verdict:

Extend existing risk worker/snapshot. Do not create a second risk authority.

## 8. Phase 6 - Trust Model Audit

Output: `ri4_a_evidence/TRUST_REALITY_MAP.md`

Trust already exists through:

- `ExecutionTrustModel`;
- bounded audit/switch/rollback history reads;
- `trust-summaries.json`;
- runtime snapshot gate.

Trust scoring rewards:

- successful executions;
- successful rollbacks.

Trust scoring penalizes:

- failed executions;
- failed rollbacks;
- governance violations;
- blast radius expansions;
- high median blast radius.

Active runtime consumption:

`trust-summaries.json` is runtime-required and STOP-class when unsafe.

Governance consumption:

No evidence found that trust owns or changes governance authority. Trust remains advisory/runtime guard input only.

## 9. Phase 7 - Snapshot Architecture Audit

Output: `ri4_a_evidence/SNAPSHOT_ARCHITECTURE_MAP.md`

Canonical snapshot root:

```text
/opt/v7/egress/state/intelligence
```

Snapshot contract families:

- `service-scores.json`
- `channel-service-scores.json`
- `user-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `capacity-forecast-summaries.json`
- `prediction-summaries.json`
- `overview-summary.json`

Production-confirmed by CONV.2:

- `service-scores.json`
- `channel-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

Not production-confirmed:

- `user-service-scores.json`;
- `capacity-forecast-summaries.json`;
- `prediction-summaries.json`.

Known infrastructure gap:

The refresh CLI works, but production systemd service/timer are missing:

- `v7-intelligence-snapshot-refresh.service`;
- `v7-intelligence-snapshot-refresh.timer`.

## 10. Phase 8 - Planner Integration Audit

Output: `ri4_a_evidence/PLANNER_INTEGRATION_MAP.md`

Planner owner:

```text
tools/v7-users-autoswitch
```

Existing RI hooks:

- `--intelligence-snapshot-root`;
- `_load_intelligence_snapshots()`;
- `_intelligence_snapshot_gate()`;
- `_snapshot_candidate_advisory_scores()`;
- `_routing_intelligence_scores_for_user()`;
- `_routing_intelligence_candidate_advice()`;
- `_snapshot_routing_brain_advisory()`;
- `_routing_brain_advisory()`;
- `_score_parts(..., routing_intelligence=...)`.

Existing planner support:

- compact snapshot reads;
- bounded RI score part;
- snapshot-backed advisory context;
- fail-closed selected move suppression;
- legacy RoutingBrain fallback when snapshots are absent.

Planner not yet consuming:

- capacity forecast snapshots;
- prediction snapshots;
- user-service snapshots as production-confirmed input.

RI.4 verdict:

Planner integration exists. RI.4 must merge through existing hooks only.

## 11. Phase 9 - Duplication Audit

Output: `ri4_a_evidence/DUPLICATION_AUDIT_REPORT.md`

Critical duplication risks if RI.4 is implemented incorrectly:

| Risk | Severity |
|---|---|
| New planner | CRITICAL |
| New governance authority | CRITICAL |
| New snapshot root/envelope | CRITICAL |
| New selected move writer | CRITICAL |
| New service history store | HIGH |
| New channel quality history | HIGH |
| New service scoring authority | HIGH |
| New trust/risk authority | MEDIUM/HIGH |

Allowed new work only inside existing contracts:

- user-service snapshot producer;
- capacity forecast snapshot producer;
- prediction snapshot producer, advisory-only;
- service history/scoring extensions in existing classes.

## 12. Phase 10 - Truth Source Audit

Output: `ri4_a_evidence/TRUTH_SOURCE_MAP.md`

Canonical sources:

| Domain | Canonical source |
|---|---|
| channel quality | `egress-quality-summary.json`, `egress-quality-ring.json`, `v7-state.json`, `egress-speed.json` |
| service quality | `service-matrix.json` |
| service history | service matrix + quality summary, via `ServiceHistoryStore` |
| user preferences | `service-preferences.json`, policy/org policy |
| risk | `risk-summaries.json` derived from service/channel/quality/route reality |
| trust | audit/switch/rollback records -> `trust-summaries.json` |
| candidate ranking | `tools/v7-users-autoswitch` |
| selected moves | `tools/v7-users-autoswitch` |
| snapshot generation | `tools/v7-intelligence-snapshot-refresh` + `admin_core/intelligence_workers.py` |
| execution authorization | governance/operator approval packet flow |
| runtime execution | `tools/v7-users-autoswitch` |

Ambiguities:

1. `user-service-scores.json` is contracted but not production-confirmed.
2. `capacity-forecast-summaries.json` is contracted but intentionally not integrated in PERF.4.
3. `prediction-summaries.json` is contracted but prediction is disabled/foundation-only.
4. snapshot refresh systemd service/timer are missing.

## 13. Phase 11 - RI.4 Readiness Certification

Output: `ri4_a_evidence/FINAL_CERTIFICATION_VERDICT.md`

### A. Already Exists

- Routing Intelligence foundation.
- Routing Brain advisory contract.
- Candidate advisory score contract.
- Service history model.
- Service intelligence scoring.
- User service weights model.
- Execution trust model.
- Dynamic blast radius model.
- Disabled predictive foundation.
- Snapshot envelope/freshness/confidence/stop model.
- Heavy Brain workers for six current snapshots.
- Snapshot refresh CLI.
- Runtime fast path snapshot reader/gate.
- Production-confirmed six snapshot files.
- Production-confirmed PERF.4 convergence.

### B. Partially Exists

- user-specific service score snapshots;
- capacity forecast snapshots;
- prediction snapshots;
- snapshot refresh systemd service/timer;
- deeper trend/prediction model.

### C. Missing

- production-certified `user-service-scores.json`;
- production-certified `capacity-forecast-summaries.json`;
- production-certified `prediction-summaries.json`;
- production-certified snapshot refresh systemd unit/timer;
- RI.4 implementation plan, intentionally not created in this audit.

### D. Reuse Plan

| RI.4 Area | Plan |
|---|---|
| service history | REUSE / EXTEND `ServiceHistoryStore` |
| service scoring | REUSE / EXTEND `ServiceIntelligenceEngine` |
| user weights | REUSE / EXTEND `UserServiceWeights` |
| trust | REUSE / EXTEND `ExecutionTrustModel` |
| risk | EXTEND existing risk worker/snapshot |
| blast radius | REUSE / EXTEND `DynamicBlastRadiusModel` |
| prediction | EXTEND disabled `PredictiveFoundation` only as advisory-only |
| snapshots | REUSE existing snapshot root/envelope/families |
| planner | MERGE only through existing `v7-users-autoswitch` hooks |
| governance | DO_NOT_TOUCH |
| execution | DO_NOT_TOUCH |

### E. Performance Review

RI.4 readiness complies with:

```text
Brain may be heavy.
Runtime may not be heavy.
```

Evidence:

- PERF.3 workers compute snapshots outside runtime.
- PERF.4 runtime reads compact snapshot files.
- PERF.4 benchmark: legacy mean `2.7198 ms`, snapshot mean `1.1775 ms`.
- Snapshot gate validates freshness/confidence/source hashes and suppresses selected moves on STOP conditions.

### F. Architecture Compliance

Current architecture matches:

```text
Heavy Brain
  -> Workers
  -> Snapshots
  -> Fast Runtime
  -> Governance
  -> Execution
  -> Audit
  -> Closure
  -> Feedback
```

Feedback exists as a defined/read input and not as autonomous learning.

### G. Final Verdict

```text
ri4_ready=true
safe_to_begin_ri4_implementation=true
runtime_mutation_performed=false
new_truth_sources_created=false
duplicate_systems_created=false
planner_changes_performed=false
governance_changes_performed=false
deploy_performed=false
commit_performed=false
```

## 14. Recommended RI.4 Implementation Boundary

The safest RI.4 implementation scope is:

1. Extend existing service history/scoring, not replace it.
2. Extend existing workers, not create new worker families outside the snapshot contract.
3. If user-specific service intelligence is needed, implement it through the existing `user-service-scores` family.
4. If prediction is needed, keep it advisory-only through `prediction-summaries`.
5. If capacity forecast is needed, keep it separate from runtime capacity authority until a dedicated PERF/capacity certification.
6. Do not touch governance, execution, rollback, selected moves, or runtime apply.

Recommended first implementation target:

```text
RI.4 should extend service intelligence depth and/or user-service scoring using existing RI models and snapshot contracts.
```

Do not mix RI.4 with:

- snapshot refresh systemd installation;
- API.6;
- admin action handler extraction;
- runtime orchestrator implementation;
- governance mutations;
- autoswitch apply.

