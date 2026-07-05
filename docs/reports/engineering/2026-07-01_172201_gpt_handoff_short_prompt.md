# GPT Handoff Short Prompt

You are taking over V7 Vozduh in `/Users/ponch/Documents/New project`, branch `Updatesystem`.

Do not restart architecture research. Do not redesign. Do not create a new Runtime, Planner, Authority, OMP, owner, wake system, event bus, truth source, or roadmap. The current work is executable debugging inside existing owners.

V7 Vozduh is a governed autonomous routing/control-plane platform for production connectivity. It is not a simple VPN project and not just autoswitch. Its purpose is to keep users online by observing real production state, selecting safe routing actions, executing only under scoped authority, verifying results, rolling back or containing failures, learning from real outcomes, and advancing maturity through OMP.

Core philosophy:

- Reality First.
- Discover -> Reuse -> Extend -> Implement.
- No duplicate owners.
- No duplicate truth sources.
- Runtime stays thin.
- Planner selects candidates.
- Authority grants bounded permission.
- OMP owns certification and action-class progression.
- Reports are evidence, not canonical truth.
- Durable knowledge belongs in canonical docs.
- No endless read-only audits after executable evidence exists.
- Long reports go to files; chat output should be short.

Canonical sources to respect:

- Product Specification.
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- policies, especially `POLICY_001_HARD_FAILURE`, `POLICY_004_AUTHORITY`, `POLICY_008_FRESHNESS`

Current capability:

```text
L3 Emergency Autonomous Failover
```

Current goal:

```text
first legal one-user Production Validation
```

Runtime automation remains disabled. Authority has not expanded. No user was moved in the latest attempt.

L3 success requires a real one-user movement, verification, rollback/no-rollback closure, learning/evidence, and then production_proven. Certification and active autonomous capability come later.

Latest current production candidate:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
```

Current result:

```text
STOP_SAFE
apply_executed=false
users_moved=0
verification_result=NOT_RUN
rollback_result=NOT_REQUIRED
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
current_failures=[]
```

Important fixed defects:

1. L3 Production Validation bypassed canonical `admin_core/operator_execution_pipeline.py`. Fixed.
2. Fresh `approved_plan_lock` / restore barrier materialization was missing. Fixed.
3. One-user production-validation envelope was not consumed as bounded authority. Fixed.
4. `approved_plan_lock.selected_moves` stripped semantic payload. Fixed.
5. Runtime mode and wake semantics were checked. Runtime STOP_SAFE is correct when L3 evidence is missing.

Commits reported in evidence:

- `0f9502bde3ac51a0d4e4f7b50309f5d7cdf11246`: restored L3 PV through canonical pipeline/materialization path.
- `9ef40a8a1cb17a30325a9653b823ffeb5126415d`: bounded emergency envelope can be consumed for one-user L3 Production Validation without granting broad autonomy.
- `478b66f329158eb5611150c1f17dd26bf64bb6ab`: fixed semantic selected-move payload preservation.

Rejected hypotheses:

- Need new Runtime = false.
- Need new Planner = false.
- Need new Authority = false.
- Need new Owner = false.
- Need new OMP = false.
- Need new wake producer is not the current root cause.
- Planner Contract Incomplete was refuted as the primary/root explanation.
- Serialization defect is fixed.
- Authority materialization is fixed.
- Restore barrier owner missing is false.
- Execution graph unreachable is false.
- Model ambiguous at execute/stop boundary is false.

The latest high-confidence executable fact comes from:

```text
docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md
```

Good L3 path:

```text
current candidate has required-service failure row:
telegram DOWN / PERSISTENT_FAIL / FRESH
-> current_failures non-empty
-> wake accepted
-> authority gate passes
```

Production path:

```text
selected source awg0 has no Runtime-verifiable required-service failure row
-> current_failures=[]
-> required_service_failure_required
-> confirmed_l3_wake_required
-> STOP_SAFE
```

First executable difference:

```text
selected_move.candidates[current_source].service_suitability.per_service[required_service]
```

This does not yet prove whether Planner is wrong or Planner received wrong/incomplete World Model. The current open question is:

```text
Why did Planner see or derive a World Model where awg0 became current_egress_not_eligible,
but no same-subject required-service failure exists for awg0 at Runtime evidence extraction?
```

Equivalent:

```text
Was Planner input/world model wrong or incomplete?
Or did Planner overclassify a broad current_egress_not_eligible condition as L3 failover?
```

Next correct engineering task:

```text
WORLD_MODEL_PROVENANCE_TRACE
```

Trace executable values only:

```text
Observation
-> Service Matrix
-> Read Models
-> Planner Inputs
-> _decision_for_user()
-> selected move
-> _emergency_failover_move_evidence()
```

For target:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

Answer:

1. What exact input made Planner set `current_egress_not_eligible`?
2. Was that input required-service failure on `awg0`?
3. If not, what kind of ineligibility was it?
4. Did Runtime see the same fact?
5. Is the divergence in Observation, World Model, Planner normalization, selected move serialization, or Runtime extraction?
6. Is Planner input wrong/incomplete, or did Planner overclassify correct input as L3 failover?

Do not patch first. Do not move users. Do not bypass required-service failure. Do not patch Runtime to accept empty `current_failures`. Do not treat `current_egress_not_eligible` as sufficient for L3 execution.

Important reports to read:

- `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md`
- `docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md`
- `docs/reports/engineering/2026-07-01_152327_action_class_ownership_proof.md`
- `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md`
- `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`
- `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md`
- `docs/reports/engineering/2026-07-01_124517_planner_contract_falsification.md`

Every future Codex step must produce an engineering report. Implementation must include tests. Deployment must include truth and convergence. Canonical docs must update only if durable knowledge changes.

Expected next verdict:

```text
FIRST_DIVERGENCE_FOUND
or
TRACE_INCONCLUSIVE
```
