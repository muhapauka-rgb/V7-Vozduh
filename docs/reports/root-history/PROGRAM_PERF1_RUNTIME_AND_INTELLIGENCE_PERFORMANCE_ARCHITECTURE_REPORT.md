# PROGRAM PERF.1 - Runtime and Intelligence Performance Architecture Report

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: Updatesystem

## Result

PASS.

No proven blocker was found. The performance architecture can proceed to PERF.2 before RI.4.

PERF.1 was read-only. No deploy, runtime mutation, service restart, user movement, autoswitch apply, merge, push, or cleanup was performed.

## Human Explanation

The system is moving toward a heavier intelligence layer: service history, predictive routing, execution trust, dynamic blast radius, and service-aware routing. That is fine only if runtime never has to think deeply at the moment it must decide or execute.

The rule for the next architecture is simple:

Brain may be heavy. Runtime may not be heavy.

Heavy calculations should happen before runtime decisions. Runtime should consume compact summaries with freshness, confidence, and source hashes.

## Current Runtime Path

The current runtime owner is `tools/v7-users-autoswitch`.

The planner currently:

- reads runtime truth files and policy inputs
- reads service matrix and quality summary
- reads restore barrier and safety state
- computes active user decisions
- selects bounded moves
- computes selected move hashes
- builds operation context
- asks Routing Brain for advisory context

Execution remains gated by `--apply`; dry-run is read-only.

Runtime execution, rollback, audit, and closure ownership remains outside Routing Intelligence.

## Current Intelligence Path

Current RI path:

`service-matrix.json` + `egress-quality-summary.json` + `service-preferences.json` + bounded audit records

-> `RoutingBrain.candidate_advisory_scores`

-> bounded advisory `score_part`

-> existing planner ranking after hard gates

The current RI contract is advisory-only:

- no user movement
- no selected move writes
- no governance authority
- no runtime mutation
- no execution authority

## Measurement

Static audit found the expensive zones:

- `admin/v7-admin-api` still contains many runtime reads, command reads, SQLite summaries, JSONL reads, and action paths.
- `tools/v7-service-matrix-test` owns network/service probes.
- `tools/v7-egress-quality-compact` owns bounded quality compaction.
- `admin_core/routing_brain.py` is pure in-memory but can become expensive if called per user at large scale.

Synthetic Routing Brain measurement:

- 50 candidate channels
- 10 required services
- 200 audit records
- 2000 total users supplied as model input
- single call: about 46.5 ms
- average over 20 calls: about 47.3 ms/call

Conclusion:

Routing Brain is acceptable for bounded advisory batches. It must not run per user x channel x service inside live runtime for 2000 users.

## Fast Runtime Architecture

Runtime may do:

- bounded file reads
- compact summary reads
- policy hard gates
- selected move hashing
- restore barrier and generation validation
- governance packet validation
- bounded execution/rollback
- terminal audit/closure metadata

Runtime must not do:

- service matrix refresh
- curl/socket probe batches
- full JSONL history scans
- SQLite traffic aggregation
- predictive modeling
- per-user service intelligence recomputation
- hidden admin overview recomputation

Runtime complexity target:

- O(users + channels) over compact summaries
- not O(users x channels x services x history)

## Heavy Brain Architecture

Heavy Brain owns:

- service testing
- service history aggregation
- service intelligence
- user service weight aggregation
- risk scoring
- execution trust scoring
- prediction
- capacity forecasting
- adaptive probe scheduling
- log/history compaction

Heavy Brain outputs compact snapshots only. It must never move users, approve execution, bypass governance, write selected moves, mutate runtime state, or restart services.

## Snapshot Architecture

PERF.2 should introduce an Intelligence Snapshot Store, likely under:

- `/opt/v7/egress/state/intelligence/`

Required snapshot families:

- `service-scores.json`
- `channel-service-scores.json`
- `user-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `capacity-forecast-summaries.json`
- `prediction-summaries.json`
- `overview-summary.json`

Every snapshot needs:

- schema
- generated_at
- expires_at
- ttl_seconds
- freshness_state
- confidence
- source_hashes
- generator
- item_count
- warnings

If runtime-required freshness is UNKNOWN, live apply must STOP.

## Load Budget Model

Runtime targets:

- planner decision: <= 250 ms target, 500 ms ceiling
- single-user execution overhead: <= 2 s target, 5 s ceiling excluding external command delay
- governance validation: <= 150 ms target, 300 ms ceiling
- rollback preparation: <= 250 ms target, 500 ms ceiling
- audit append: <= 100 ms target, 250 ms ceiling
- snapshot read: <= 50 ms target, 150 ms ceiling

Admin targets:

- overview from snapshot: <= 200 ms target
- service summary read: <= 150 ms target
- diagnostics shell: <= 250 ms target
- explicit diagnostics: user-triggered or async

Heavy Brain budgets:

- service history aggregation: <= 2 CPU seconds/run
- trust aggregation: <= 1 CPU second/run
- prediction summary: <= 5 CPU seconds/run
- log compaction: <= 2 CPU seconds/run
- light probes: <= 50 probes/min total
- heavy probes: <= 5 probes/min total

## Adaptive Testing Model

Probe classes:

- L0 file freshness
- L1 light health
- L2 light network
- L3 service matrix
- L4 heavy diagnostics
- L5 emergency verification

Rules:

- healthy channels tested less
- suspicious channels tested more
- failed channels quarantined
- heavy tests rare
- light tests frequent
- runtime consumes status/freshness/confidence only
- runtime does not schedule probes

## Log Architecture

Raw logs remain evidence, not runtime decision inputs.

Aggregation outputs:

- audit -> trust summaries
- switch history -> execution history summaries
- service matrix + quality ring -> service scores
- route probes -> route reality summaries
- traffic SQLite/raw -> traffic summaries
- capacity state -> capacity forecasts

Runtime must not scan large history directly.

## Scaling Analysis: 2000 Users / 50 Channels

Safe pattern:

- group users by service requirements and policy class
- precompute channel/service scores
- precompute user/group weights
- keep dynamic blast radius as compact formula over risk/trust/platform health
- keep runtime selected move count bounded by policy and governance

Unsafe pattern:

- 2000 users x 50 channels x 50 services x 4 history windows inside planner
- service probe matrix during planner or admin overview
- full audit scan during execution
- traffic SQLite rollup on every overview request

## PERF.2 Recommendation

Begin PERF.2 next.

PERF.2 should create the snapshot store contract before RI.4 expands intelligence. The first implementation should be schema/read-path only unless explicitly approved:

- define snapshot envelope
- define freshness/confidence semantics
- define runtime STOP conditions
- define bounded snapshot readers
- define source hash model
- define snapshot families and ownership

## Evidence

- `docs/reports/evidence/perf1_evidence/discovery_inventory.md`
- `docs/reports/evidence/perf1_evidence/static_measurement.md`
- `docs/reports/evidence/perf1_evidence/runtime_path_map.md`
- `docs/reports/evidence/perf1_evidence/intelligence_path_audit.md`
- `docs/reports/evidence/perf1_evidence/duplication_audit.md`
- `docs/reports/evidence/perf1_evidence/fast_runtime_architecture.md`
- `docs/reports/evidence/perf1_evidence/heavy_brain_architecture.md`
- `docs/reports/evidence/perf1_evidence/snapshot_architecture.md`
- `docs/reports/evidence/perf1_evidence/load_budget_model.md`
- `docs/reports/evidence/perf1_evidence/adaptive_testing_model.md`
- `docs/reports/evidence/perf1_evidence/log_history_architecture.md`
- `docs/reports/evidence/perf1_evidence/performance_risk_analysis.md`
- `docs/reports/evidence/perf1_evidence/implementation_roadmap.md`

## Final Verdicts

runtime_path_audited=true

intelligence_path_audited=true

fast_runtime_architecture_defined=true

heavy_brain_architecture_defined=true

snapshot_architecture_defined=true

load_budget_model_defined=true

adaptive_testing_model_defined=true

log_architecture_defined=true

performance_budgets_defined=true

safe_to_begin_PERF2=true
