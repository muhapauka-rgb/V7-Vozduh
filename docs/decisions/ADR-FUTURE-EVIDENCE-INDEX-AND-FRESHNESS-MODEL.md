# ADR-FUTURE-EVIDENCE-INDEX-AND-FRESHNESS-MODEL

Status: Accepted
Date: 2026-06-23
Commit: db161ae90e252f393ed7e3003ec4eddc31bc8a8c

## Context

V7 is currently below Production Autonomy readiness. The active blocker is not evidence scale; it is current confidence/trust/prediction/candidate outcome maturity. AUTONOMY.REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH reports `REAL_OUTCOME_MIXED`: service/channel/feedback/learning outcome paths are acceleratable, but canary remains blocked because candidate/suitability outcomes remain weak.

After Production Autonomy is certified, V7 may need to operate with `100+` channels, `1000+` users, and years of accumulated evidence. At that scale, planner and trust reads must avoid slowdown, stale-data bias, and trust distortion.

This ADR records a future scalability phase only. It does not authorize implementation now.

## Decision

Create a deferred roadmap phase:

`AUTONOMY.EVIDENCE.INDEX_AND_FRESHNESS_MODEL`

The phase will prepare a future evidence catalog, type-aware freshness model, aggregated read models, cardinality controls, and shadow validation plan.

Future evidence classes:

| Class | Name | Examples |
| --- | --- | --- |
| A | Fast Reality | Telegram, YouTube, latency, packet loss, Service Matrix, Route Readiness |
| B | Channel Behavior | Stability, speed, failure rate, recovery rate, quality trend |
| C | Outcome Evidence | Candidate outcomes, governed outcomes, manual outcomes, post-switch verification |
| D | System Safety Evidence | Blast, rollback, restore, packet validity, feedback closure, learning closure |

Possible future evidence index fields:

| Field | Purpose |
| --- | --- |
| `evidence_id` | Stable future catalog id |
| `timestamp` | Evidence observation or closure time |
| `evidence_type` | Evidence class/type |
| `channel_id` | Channel scope when applicable |
| `service_id` | Service scope when applicable |
| `owner` | Existing owner that produced the evidence |
| `quality_score` | Existing quality/correctness meaning |
| `freshness_score` | Future shadow freshness weighting |
| `confidence_score` | Existing confidence meaning |
| `weight` | Future derived weight after shadow validation |

Future aggregated read models:

- `channel_current_summary`
- `channel_service_summary`
- `channel_behavior_summary`
- `candidate_outcome_summary`
- `system_safety_summary`
- `trust_evolution_summary`

## Why Needed

Without an index/freshness model, years of evidence can create three risks:

1. Planner slowdown from repeatedly scanning raw or high-cardinality stores.
2. Trust distortion from old evidence carrying too much current weight.
3. Irrational decisions from treating fast evidence and durable safety evidence as if they age identically.

## Why Deferred

This is not a current blocker. Current V7 still needs Production Autonomy certification and real outcome maturity first. Implementing an index/freshness layer now would risk creating a premature second truth surface or tuning trust before the existing event-driven autonomy chain is certified.

## Activation Criteria

The phase may start only when:

1. Production Autonomy is certified.
2. Event-driven autonomy operates through the existing chain: regression -> planner -> packet -> restore barrier -> bounded apply -> verification -> rollback decision -> feedback -> learning.
3. Evidence scale creates real pressure, such as `100+` channels, `1000+` users, or multi-year evidence history.
4. Existing owners and truth sources are clearly mapped for every evidence class.
5. A shadow validation plan can prove no planner slowdown, no trust distortion, and no stale-data bias before promotion.

## Shadow Validation Requirement

Any future freshness/index model must first run in shadow mode.

Shadow mode means:

- no direct planner impact;
- no direct trust impact;
- no direct execution impact;
- no direct governance impact;
- compare current behavior versus freshness-weighted behavior;
- promote only after truth/convergence and scale evidence support it.

## Alternatives Considered

1. Implement evidence indexing now.
   - Rejected because Production Autonomy is not yet certified and current blockers are evidence maturity/floors, not scale.

2. Delete old evidence.
   - Rejected because old evidence remains useful history. It should lose weight rather than disappear.

3. Apply one global freshness rule to all evidence.
   - Rejected because Telegram/service probe evidence and blast/rollback safety evidence age differently.

4. Create a new trust engine.
   - Rejected. Future implementation must reuse existing owners, truth sources, planner, governance, and execution path.

## Consequences

- The future scale idea is preserved in canonical project memory.
- Current work remains focused on evidence maturity and Production Autonomy certification.
- Future implementers have explicit rules against new planners, new governance, new execution, new truth sources, and new trust engines.
- Any future implementation must be shadow-first.

## Affected Modules

Current phase:

- Documentation only.
- No runtime modules affected.
- No code files changed.

Future phase must reuse existing owners, likely including:

- `admin_core/intelligence_workers.py`
- `admin_core/intelligence_platform.py`
- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-intelligence-snapshot-refresh`
- `tools/v7-autonomy-trust-evidence-inventory`
- existing planner/governance/execution owners

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_PROJECT_MAP.md`

## Related Reports

- `docs/reports/AUTONOMY_SOURCE_CONFIDENCE_REALITY_AUDIT_REPORT.md`
- `docs/reports/AUTONOMY_REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_REAL_SOURCE_CONFIDENCE_COLLECTION_REPORT.md`
- `docs/reports/AUTONOMY_CANARY_1D_CONFIDENCE_TRUST_PREDICTION_FLOOR_CLOSURE_REPORT.md`
- `docs/reports/EVENT_CONSUMER_READONLY_2_REPORT.md`
