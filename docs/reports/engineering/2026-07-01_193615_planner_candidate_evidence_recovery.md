# Planner Candidate Evidence Recovery

Generated: 2026-07-01 19:36:15 Asia/Bangkok

Status: READ_ONLY_AUDIT

Code modified: NO
Runtime modified: NO
Planner modified: NO
Production modified: NO
Users moved: 0
Deploy performed: NO

## Summary

The exact raw historical Planner Candidate for:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
candidate.egress: awg0
```

was not found in local historical artifacts, engineering reports, channel truth artifacts, evidence directories, state snapshots, proposal/closure/runtime trust/execution records, restore barrier snapshots, approved plan lock materializations, planner preview artifacts, operator decision-surface captures, or targeted local git history.

The gap is not explained by proven artifact deletion or rotation. The first missing capture point is durable persistence of the full Planner plan/candidate trace after `tools/v7-governed-canary-dry-run-cycle::run_l3_production_validation_plan()` receives the `tools/v7-users-autoswitch` payload and before the production-validation report reduces the result to summary fields.

Classification:

```text
ENGINEERING_OBSERVABILITY_OMISSION
```

## Inputs Read

- `docs/reports/engineering/2026-07-01_192647_local_l3_planner_patch_reverted.md`
- `docs/reports/engineering/2026-07-01_191923_eligibility_root_cause_proof.md`
- `docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md`
- `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md`
- `docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md`
- `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md`
- `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md`
- `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/SYSTEM_MAP.md`
- `tools/v7-users-autoswitch`
- `tools/v7-governed-canary-dry-run-cycle`
- `admin_core/operator_execution.py`

## Phase 1: Evidence Recovery Audit

### Required Object

Required object:

```text
decision.user_ip = 10.7.0.5
decision.current_egress = awg0
decision.recommended_egress = vless
candidate.egress = awg0
```

Required fields:

- `candidate.eligible`
- `candidate.blocked[]`
- `candidate.reasons[]`
- `candidate.quality_decision`
- `candidate.service_suitability`
- `candidate.load`
- `candidate.safety`
- `candidate.quality_history`
- `candidate.severity_classification`
- `required_services`
- `route_class`
- freshness / generation / timestamp

### Search Scope

Searches covered:

- `docs/reports/engineering/`
- `docs/channel_truth_*`
- local evidence directories matched by `evidence`
- state snapshots
- proposal records
- closure records
- runtime trust records
- execution event records
- restore barrier snapshots
- approved plan lock artifacts
- planner preview artifacts
- operator decision-surface captures
- targeted local git history since 2026-06-30

Structured scan result:

```text
candidate files containing all target tokens: 359
structured decision matches with:
  user_ip=10.7.0.5
  current_egress=awg0
  recommended_egress=vless
  candidate.egress=awg0
result: 0
```

### Non-Target Matches

Several older artifacts contain overlapping facts, but not the target object:

- May/June planner snapshots contain `10.7.0.5` and `awg0`/`vless` in unrelated historical decisions.
- Some artifacts contain `awg0 -> vless` for other users.
- Some reports contain the reconstructed July L3PV identity but not the raw `decisions[].candidates[]` row.
- Switch history contains movement events, not Planner candidate gate state.

These artifacts cannot prove the exact first `_candidate()` gate for the July L3PV target.

### Raw Candidate Found?

```text
RAW_CANDIDATE_FOUND: NO
```

## Phase 2: Persistence Path Audit

### Planner Plan Generation

`tools/v7-users-autoswitch::plan()` builds:

```text
decisions = [self._decision_for_user(user) ...]
```

The returned plan includes:

```text
"decisions": decisions
"selected_moves": selected
```

`_decision_for_user()` returns each decision with:

```text
user_ip
group
route_class
important_services
current_egress
recommended_egress
action
move_type
reason
current_score
recommended_score
candidates
explanation
```

`_candidate_json()` would have serialized the required candidate-level fields:

```text
egress
eligible
blocked
reasons
severity_classification
service_suitability
quality_decision
load
quality_history
safety
telegram
```

Therefore, the raw final candidate row was representable in the full Planner plan JSON.

### Gate Trace Generation

`_candidate()` mutates one `Candidate` through:

```text
_gate_basic()
_gate_reservation()
_gate_org()
_gate_quality()
_gate_service()
_gate_load()
_gate_safety()
```

The code serializes only the final candidate state. It does not produce an ordered per-gate before/after trace. Therefore even a recovered final candidate row would prove blockers but not a native gate-by-gate mutation log.

### Plan JSON Object

`tools/v7-users-autoswitch::main()`:

```text
plan = planner.plan()
plan["apply_result"] = planner.apply(plan)
planner.finalize_operation(plan)
print(json.dumps(plan, ...))
```

There is no `--output` path and no internal durable write for the full Planner plan. The full plan exists in process memory and stdout unless the caller persists stdout.

The only write in `plan()` itself that is relevant to normal planning is:

```text
self._persist_dynamic_load_summary()
```

This does not write decisions or candidates.

### Selected Move Object

`admin_core/operator_execution.py::selected_moves_from_plan()` consumes either:

- `plan.selected_moves`
- `restore_barrier.approved_candidate_moves_before_guard`
- fallback `plan.decisions`

It preserves selected-move semantic fields:

```text
reason
important_services
candidates
scores
service_failover
```

This owner can preserve candidate semantics only if it receives the full `plan` object. It is not a historical raw-plan store by itself.

### Approved Plan Lock

`admin_core/operator_execution.py::approved_plan_lock_from_selected()` preserves selected moves and the semantic fields listed above.

This is an execution artifact, not a complete Planner candidate trace. It should preserve the selected move semantics after materialization, but it does not own `_candidate()` gate-birth observability.

### Restore Barrier

`admin_core/operator_execution.py::build_restore_barrier_clearance()` embeds the approved plan lock into restore barrier clearance when present.

This can carry selected-move semantics forward, but it cannot recover a raw Planner plan that was never durably captured.

### Runtime Evidence Extraction

Runtime consumes selected move semantics through:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
```

The later reports prove Runtime found:

```text
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

This proves the L3 execution blocker but not the Planner gate that first flipped `current.eligible` to false.

### Closure / Reporting

`tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation()` returns a final result containing:

```text
"l3_plan_run": l3_plan_run
```

and `l3_plan_run` contains the parsed Planner payload when available. However, no persisted artifact containing:

```text
schema_version: v7.l3-production-validation-execution.v1
l3_plan_run.payload.decisions[]
```

was found outside the source code. The engineering reports preserve the summary facts and downstream blockers, not the full wrapper result.

## Phase 2 Questions

### 1. Was the raw Planner plan ever written?

Not proven. No durable local artifact containing the exact raw Planner plan for the July L3PV target was found.

The code path can emit the full plan to stdout and the wrapper can hold it in memory, but no mandatory durable write exists at the Planner or governed-cycle boundary.

### 2. Which function should have written it?

Existing-owner capture point:

```text
tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation()
```

immediately after:

```text
l3_plan_run = run_l3_production_validation_plan(...)
plan = l3_plan_run["payload"]
```

A lower-level alternative is:

```text
tools/v7-users-autoswitch::main()
```

or `AutoswitchPlanner.plan()` via an explicit observability-only `--trace-output` / `--plan-output` artifact. But the production-validation owner already has the relevant scoped operation context, so the first existing owner for this specific validation capture is the governed-cycle owner.

### 3. Was it intentionally reduced?

No intentional policy was found that says raw Planner candidates participating in L3 Production Validation may be discarded before the validation ladder completes.

There are canonical statements that packets/leases are transient execution artifacts, but the Planner candidate evidence needed for Reality First debugging is not documented as intentionally ephemeral.

### 4. Was it lost by report generation?

Partially yes. The final report preserved:

- selected user/source/target;
- `STOP_SAFE`;
- `required_service_failure_required`;
- `confirmed_l3_wake_required`;
- semantic selected-move preservation status.

It did not include or attach the full raw `l3_plan_run.payload.decisions[]` object. Because no separate durable artifact was found, report generation became the last opportunity to preserve it.

### 5. Was it lost by retention/cleanup?

No deletion, cleanup, artifact rotation, or retention rule was found that explains loss of this exact object.

Targeted git history did not show a committed raw L3PV execution artifact later removed. Local artifact searches found no rotated or archived copy of the exact raw object.

### 6. Was it never captured by design?

Yes, for durable storage. The full object is produced and passed in memory, but durable capture is not a required design step for Production Validation.

### 7. Which existing owner should own this capture?

Primary existing owner for the validation artifact:

```text
tools/v7-governed-canary-dry-run-cycle
```

Supporting owners:

```text
tools/v7-users-autoswitch
admin_core/operator_execution.py
Engineering Report lifecycle / OMP evidence discipline
```

No new owner is required.

## Phase 3: Observability Gap Classification

Classification:

```text
ENGINEERING_OBSERVABILITY_OMISSION
```

Reason:

The missing object is not a new Planner/Runtime requirement and not a routing behavior gap. It is the absence of a mandatory durable evidence artifact at the boundary where a production-validation candidate is created, packetized, locked, tested, and reported.

Secondary classification:

```text
REPORT_GENERATION_OMISSION
```

The report reduced the available final result to summary facts. But because there was no separate raw-plan persistence rule, the deeper classification remains engineering observability, not report writing alone.

Rejected classifications:

- `RAW_CANDIDATE_FOUND`: exact raw object not found.
- `INTENTIONAL_RETENTION_LIMIT`: no intentional policy found.
- `ARTIFACT_ROTATION_LOSS`: no deletion/rotation evidence found.
- `TRACE_INCONCLUSIVE`: the missing capture point is specific enough to classify.

## Why The Exact Gate Cannot Be Proven

The exact first gate cannot be proven because the following historical object was never found:

```text
Full raw Planner plan JSON for the July L3 Production Validation attempt,
including:
  decision.user_ip = 10.7.0.5
  decision.current_egress = awg0
  decision.recommended_egress = vless
  candidate.egress = awg0
  candidate.eligible
  candidate.blocked[]
  candidate.reasons[]
  candidate.quality_decision
  candidate.service_suitability
  candidate.load
  candidate.safety
  candidate.quality_history
  candidate.severity_classification
```

The stronger missing object is:

```text
ordered gate trace for the same candidate:
  gate name
  input values
  eligible before
  eligible after
  blockers added
  reasons added
  raw input refs
  freshness
  producer
  owner
  timestamp
  generation_id
  selected_move_hash
  operation_id
```

Without the final raw candidate row, the exact blocker is unknown. Without ordered gate tracing, even a candidate with multiple blockers would require source-order reconstruction rather than direct evidence.

## Phase 4: Observability-Only Patch Design

Do not implement without explicit approval.

Design goal:

```text
Persist evidence only. Change no routing, selected move, authority, Runtime, apply, or user movement behavior.
```

Minimal artifact:

```text
Full Planner Candidate Trace
```

Recommended artifact path shape:

```text
docs/reports/engineering/evidence/planner_candidate_traces/<operation_id_or_generation>/<selected_move_hash>.json
```

or, for production state-owned evidence:

```text
<state_dir>/planner-candidate-traces.jsonl
```

depending on the existing report/production evidence policy selected by OMP.

Required capture points:

1. Before `_decision_for_user()` returns:
   - full decision object;
   - user/source/target/action/move_type/reason;
   - route class;
   - required services;
   - generation.

2. After `_candidate()` builds current candidate:
   - candidate birth state;
   - `eligible=true`;
   - severity/service/routing/CTR initial objects.

3. After each `_gate_*` mutation:
   - gate name;
   - input refs;
   - eligible before/after;
   - blockers added;
   - reasons added;
   - freshness;
   - producer;
   - owner.

4. Selected move birth:
   - selected row as produced by Planner;
   - selected move hash inputs;
   - rank/selection source.

5. After `selected_moves_from_plan()`:
   - selected rows after semantic-field preservation;
   - whether fields came from `selected_moves`, `approved_candidate_moves_before_guard`, or `decisions`.

6. Inside `approved_plan_lock`:
   - selected move identity;
   - preserved semantic fields;
   - lock id/hash;
   - generation.

7. Inside `restore_barrier`:
   - approved plan lock copy;
   - restore barrier id/hash;
   - allowed users/targets;
   - clearance generation.

8. Runtime `move_evidence`:
   - source candidate used;
   - required services checked;
   - current failures found;
   - blockers.

9. Wake decision:
   - decision;
   - accepted/rejected wake sources;
   - failed sources/services.

10. Authority gate result:
   - selected moves before/after;
   - blockers;
   - final gate decision.

Hard constraints:

- no apply behavior change;
- no selected move behavior change;
- no authority behavior change;
- no Runtime behavior change;
- no user movement;
- no new Runtime, Planner, Authority, Wake, Event Bus, Truth Source, OMP, or CPS.

Existing-owner implementation direction:

- Add observability-only trace emission to `tools/v7-users-autoswitch` behind an explicit trace-output or production-validation trace flag.
- Have `tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation()` require a durable trace artifact for L3PV before proceeding from plan to packet, or include the full `l3_plan_run.payload` as an attached evidence file.
- Keep `admin_core/operator_execution.py` behavior unchanged; optionally persist selected-move semantic snapshots as evidence-only attachments when building packet/lock/barrier.

## Phase 5: Next Test Design

Run only after observability exists.

Test:

```text
L3 Production Validation in dry-run/validation mode
```

Required evidence:

- full Planner Candidate Trace persisted;
- selected move persisted after `selected_moves_from_plan()`;
- approved plan lock persisted;
- restore barrier copy persisted;
- Runtime `move_evidence` persisted;
- wake and authority results persisted.

Expected classification:

```text
first gate that flips current.eligible=true -> false
exact blocker
source object
freshness
owner
```

Then and only then decide whether to patch:

- `_decision_for_user()` classification, or
- an upstream gate that produced incorrect ineligibility.

## Final Verdict

```text
ENGINEERING_OBSERVABILITY_OMISSION
```
