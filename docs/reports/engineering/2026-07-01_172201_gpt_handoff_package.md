# GPT Handoff Package

Status: `GPT_HANDOFF_PACKAGE_CREATED`
Purpose: seamless transfer of V7 Vozduh to a new GPT/Codex chat
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Created: `2026-07-01`

This is not an audit, implementation, architecture redesign, roadmap, or second truth source.

Canonical hierarchy:

1. Product Specification
2. `docs/reference/V7_CANONICAL_REFERENCE.md`
3. `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
4. `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
5. `docs/reference/SYSTEM_MAP.md`
6. `docs/reference/V7_RUNTIME_MODEL.md`
7. `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
8. `docs/reference/V7_DECISION_MODEL.md`
9. `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
10. Policies and ADRs
11. Engineering reports as evidence/history only

## 1. Project Identity

V7 Vozduh is a governed autonomous routing/control-plane platform for production connectivity.

It is not a simple VPN project and not just an autoswitch script. The VPN/channel layer is the substrate. The product is a control plane that observes production reality, understands users/channels/services, selects safe routing actions, applies only under valid authority, verifies results, rolls back or contains failed execution, learns from real outcomes, and advances autonomy through OMP certification.

Long-term direction:

```text
governed evidence
  -> certified action classes
  -> bounded runtime execution
  -> verified outcomes
  -> learning
  -> production maturity
  -> certified autonomous runtime
```

Current live focus:

```text
L3 Emergency Autonomous Failover
  -> first legal one-user Production Validation
  -> no broad automation
  -> no authority expansion
  -> no more than one user
```

The project's moral center is simple: keep users online, but never fake certainty. If V7 cannot prove safety, evidence, authority, rollback, and verification, it must `STOP_SAFE`.

## 2. Non-Negotiable Engineering Philosophy

### Reality First

Production state, executable traces, tests, truth, convergence, and real outcomes outrank architecture speculation, labels, dashboards, or reports.

### Discover -> Reuse -> Extend -> Implement

Every task must first search existing semantics, canonical owners, code owners, policies, ADRs, and reports.

Default order:

```text
Discover
  -> Semantic Reuse
  -> Canonical Reuse
  -> Owner Reuse
  -> Extend Existing Owner
  -> Implement only if required
```

### No duplicate owners

Do not create a new owner unless proven impossible to reuse an existing one. Current evidence says:

```text
Need New Owner = FALSE
Need New Runtime = FALSE
Need New Planner = FALSE
Need New Authority = FALSE
Need New OMP = FALSE
```

### No duplicate truth sources

Do not create a second wake truth, second service-failure truth, second planner truth, second authority truth, or second runtime truth. The current known issue must be solved through existing Observation / World Model / Planner / Runtime evidence flow.

### No speculative redesign

Architecture is mature and closed by default. New architecture is allowed only if implementation proves a fundamental contradiction. Current evidence does not prove that.

### No parallel Runtime / Planner / Authority

Runtime stays thin. Planner selects candidates. Authority grants/denies bounded permission. OMP owns class/certification state. These responsibilities must not be duplicated or silently reassigned.

### Completion-first rule

Work is complete only when its output is consumed by a real next owner, behavior changes or a legal stop is reached, and the next output or terminal consumer is verified.

Forbidden completion claims:

- read model only;
- dashboard only;
- report only;
- diagnostic only;
- placeholder;
- future work;
- orphan output;
- unconsumed recommendation.

### Engineering report rule

Every meaningful implementation, production validation, audit, or certification step must create an engineering report under `docs/reports/engineering/`.

### Durable knowledge promotion

Durable knowledge must update canonical owners when it changes system meaning. Reports remain evidence/history and do not become canonical truth by themselves.

### No endless read-only audits after executable evidence exists

The current state has enough executable evidence to proceed to a World Model / Planner input trace. Do not restart old broad architecture investigations unless new executable evidence contradicts the current trace.

## 3. Current Architecture Map

| Plane | Owner | Purpose | Producer | Consumer | Current maturity | Known risks |
| --- | --- | --- | --- | --- | --- | --- |
| Observation | service matrix, quality, sentinel, route/runtime truth owners; Policy 001 and Policy 008 | observe production reality and freshness | service refresh, health probes, route checks, user/channel state | World Model, Planner, Runtime gates | strong but still must prove same-subject evidence | stale/misaligned observation, source mismatch, missing provenance |
| World Model | Knowledge Plane, intelligence snapshots, Current Program State, read-model owners | compact current state and evidence into consumable facts | observation/read models | Planner, Runtime, OMP | mature as plane; current provenance question open | Planner may consume a broader or different fact than Runtime later checks |
| Planning | `tools/v7-users-autoswitch`, operator decision surfaces | produce candidate universe, selected moves, reasons, blockers, targets | world model, service matrix, policy, user registry | packet/lock owners, Runtime gate | executable and tested | may overclassify broad `current_egress_not_eligible` as L3 `failover` |
| Authority | OMP, Policy 004, action-class/delegated authority owners | authorize bounded scope; deny expansion | OMP stage, operator approval, policy, capability state | Runtime eligibility and execution pipeline | mature; current envelope bridge fixed | authority must not bypass L3 evidence |
| Execution | Runtime Model, `admin_core/operator_execution_pipeline.py`, `admin_core/operator_execution.py`, `tools/v7-users-autoswitch` | materialize packet/lock/barrier and execute or stop | Planner, authority, packet, restore barrier | verification, rollback, learning | reachable after fixes | must preserve identity and fail closed |
| Verification | `tools/v7-users-autoswitch` verification owners, truth/convergence where applicable | prove route/target/required services after apply | execution result | rollback, learning, OMP | implemented; not reached in latest attempt | no production proof until movement occurs |
| Rollback / containment | restore/rollback owners, Policy 007 | reverse/contain failed mutation | verification failure, runtime failure | terminal outcome, learning | implemented; not reached in latest attempt | rollback cannot be counted as success |
| Learning | feedback/outcome/trust/evidence owners | convert terminal outcome into evidence | verification/rollback/terminal state | OMP, production maturity, future Planner evidence | mature but requires real terminal outcome | no learning when no apply occurs |
| OMP / Certification | OMP, CPS, Backlog, Production Maturity | decide maturity, certification, next work, authority progression | reports, evidence, outcomes, truth/convergence | capability state, runtime readiness, operator next step | mature | must not mark read-only output as complete production proof |
| Autonomous Runtime | Autonomous Runtime Model over existing runtime owners | certified closed-loop execution after promotion | OMP/certified capability, runtime events | Runtime execution cycle | architecture complete; not certified active | broad automation must remain disabled |

## 4. OMP State

OMP is the governing program. It owns execution discipline, capability progression, certification, production promotion, and current next-step selection.

Current state:

```text
Architecture: mature / complete
Canonical integration: complete
L3 capability: implemented and deployed, but not production proven
Current work: first legal one-user L3 Production Validation
Runtime automation: disabled
Authority expansion: none
Latest production attempts: no users moved
```

No new owner is needed. No new OMP is needed. No new runtime path is needed.

Important nuance:

`L3 implementation complete` does not mean `L3 production certified`.

L3 becomes production proven only after real one-user execution succeeds or reaches a terminal rollback/no-rollback closure with verification and learning/evidence. Certification and active autonomous capability come later.

## 5. L3 Capability State

L3 Emergency Autonomous Failover is the current active capability under validation.

Goal:

```text
first legal one-user Production Validation
```

L3 exists to restore user connectivity after confirmed current-channel failure.

L3 is not:

- rebalance;
- optimization;
- preference movement;
- capacity balancing;
- cleanup;
- generic autoswitch;
- movement on weak suspicion.

Success requires:

1. one legal candidate;
2. same-subject current-channel failure evidence;
3. required services failed on the selected current channel;
4. safe target;
5. fresh evidence;
6. one-user scoped authority/envelope;
7. valid approved plan lock;
8. valid restore barrier;
9. rollback/no-rollback readiness;
10. verification readiness;
11. apply;
12. verification;
13. rollback/no-rollback closure;
14. learning/evidence;
15. production_proven transition.

Certification and `active_capability` come only after production validation and certification review.

## 6. Current Production Attempt

Exact known candidate:

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
apply_executed: false
users_moved: 0
verification_result: NOT_RUN
rollback_result: NOT_REQUIRED
```

Current blockers:

```text
required_service_failure_required
confirmed_l3_wake_required
current_failures: []
```

Known differential:

```text
Good L3 path:
  current candidate has telegram DOWN / PERSISTENT_FAIL / FRESH
  -> current_failures non-empty
  -> wake accepted
  -> gate passes

Production path:
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

## 7. Defects Already Found And Fixed

| Defect | Hypothesis | Proof | Fix | Commit / result | Status |
| --- | --- | --- | --- | --- | --- |
| L3 PV bypassed canonical execution pipeline | L3 Production Validation went directly to autoswitch consumer instead of the governed execution coordination owner | `transition_owner_audit` proved canonical owner is `admin_core/operator_execution_pipeline.py`; actual path bypassed it | route L3 PV through existing pipeline and governed CLI | `0f9502bde3ac51a0d4e4f7b50309f5d7cdf11246`; deploy/truth/convergence passed | `FIXED` |
| Fresh approved plan lock / restore barrier materialization missing | Runtime consumed stale or wrong envelope | authority materialization and conflict audits showed `build_restore_barrier_clearance()` not called for current candidate | existing materialization owner invoked through pipeline | restore barrier written for current candidate | `FIXED` |
| Production-validation envelope not consumed as bounded authority | Runtime treated first validation as if certified autonomous authority were required | final root cause experiment isolated approved envelope as valid but not accepted as one-user validation authority | narrow `CURRENT_APPROVED_EMERGENCY_ENVELOPE` bridge in `tools/v7-users-autoswitch` | `9ef40a8a1cb17a30325a9653b823ffeb5126415d`; tests/deploy/truth/convergence passed | `FIXED` |
| `approved_plan_lock.selected_moves` semantic payload stripped | Lock preserved identity only, not Planner evidence | lineage proof identified semantic loss in `approved_plan_lock.selected_moves` | preserve/enrich `reason`, `important_services`, `candidates`, `scores`, `service_failover` | `478b66f329158eb5611150c1f17dd26bf64bb6ab`; tests/deploy/truth/convergence passed | `FIXED` |
| Runtime/authority/wake semantics uncertain | Maybe Runtime applied wrong mode or too strict wake | execution mode proof and formal model showed L3 PV must still require wake/failure evidence | no weakening; keep STOP_SAFE when L3 evidence missing | latest STOP_SAFE is considered correct if evidence missing | `PROVEN` |

## 8. Hypotheses Rejected

Do not reinvestigate these unless new executable evidence appears:

| Hypothesis | Status | Why |
| --- | --- | --- |
| Need new Runtime | `REFUTED` | Existing runtime path is reachable and correct at execute/stop boundary. |
| Need new Planner | `REFUTED` | Existing planner owner exists; issue is within owner/input classification, not missing planner architecture. |
| Need new Authority | `REFUTED` | Policy 004 and envelope bridge cover current bounded authority. |
| Need new Owner | `REFUTED` | Existing owners map every relevant step. |
| Need new OMP | `REFUTED` | OMP owns progression and is sufficient. |
| Need new Wake Producer as root cause | `REFUTED AS ROOT` | Runtime can derive wake from move evidence when same-subject failures exist. |
| Planner Contract incomplete as primary explanation | `REFUTED AS PRIMARY` | Existing contract works in good path; current issue is values/provenance/classification. |
| Serialization defect remains root cause | `FIXED` | Semantic selected move payload now survives. |
| Authority materialization remains root cause | `FIXED` | Pipeline and restore barrier materialization now occur. |
| Restore barrier owner missing | `FALSE` | Owner exists: `admin_core/operator_execution.py`. |
| Execution graph unreachable | `FALSE` | Reachability proof found graph reachable. |
| Model ambiguous at execute/stop boundary | `FALSE` | Formal model is deterministic: missing mandatory fact -> STOP_SAFE. |

## 9. Important Reports And Their Meaning

| Report | Question | Proved | Did not prove | Changed implementation | Current relevance |
| --- | --- | --- | --- | --- | --- |
| `2026-06-30_232133_authority_envelope_conflict_audit.md` | Is authority layering conflicting? | No conflict; fresh concrete envelope required after OMP authority. | Did not fix caller. | No. | Historical explanation of envelope layering. |
| `2026-07-01_074532_authority_materialization_call_chain.md` | Why was restore barrier clearance not called? | L3 PV path missed the producer/caller. | Did not prove Runtime bug. | No. | Superseded by later fix but useful history. |
| `2026-07-01_075259_transition_owner_audit.md` | Who owns Production Validation -> Runtime Action? | Canonical owner is `admin_core/operator_execution_pipeline.py`; path was bypassed. | Did not patch. | No. | Basis for minimal patch. |
| `2026-07-01_010753_l3_minimal_patch.md` | Restore canonical execution chain. | L3 PV now routes through existing pipeline/materialization. | Did not solve later wake/evidence blocker. | Yes. | Fixed transition/restore path. |
| `2026-07-01_032043_execution_reachability_audit.md` | What can stop execution before movement? | Current blocker shifted into emergency failover authority gate. | Did not prove why wake/evidence absent. | No. | Historical blocker ladder. |
| `2026-07-01_033033_execution_reachability_proof.md` | Is graph theoretically reachable? | Graph reachable with `CURRENT_APPROVED_EMERGENCY_ENVELOPE`. | Did not prove current candidate safe. | No. | Supports no-new-architecture conclusion. |
| `2026-07-01_034329_minimal_safe_experiment_design.md` | Can a narrow bridge experiment be safe? | Yes, if bounded to one-user PV envelope. | Did not apply patch. | No. | Basis for final root cause experiment. |
| `2026-07-01_041410_final_root_cause_experiment.md` | Why envelope rejected? | Envelope bug fixed; next gate is wake/failure. | Did not prove Planner/world cause. | Yes. | Current authority bridge is fixed. |
| `2026-07-01_050953_execution_mode_semantics_proof.md` | Is Runtime using wrong mode? | No; L3 PV uses correct L3 gate set. | Did not explain missing evidence source. | No. | Prevents wrong-mode reinvestigation. |
| `2026-07-01_121805_confirmed_l3_wake_provenance.md` | Where does `CONFIRMED_L3_WAKE` come from? | External wake artifact missing for openvpn incident; Runtime can consume external or inferred wake. | Later evidence showed wake can derive from move evidence; do not treat missing external event as root by itself. | No. | Partially superseded by planner-contract falsification/differential trace. |
| `2026-07-01_122759_planner_vs_wake_truth_audit.md` | Is wake independent or derivable? | Wake should not become second truth source; it is derivable from complete L3 evidence. | Its `PLANNER_CONTRACT_INCOMPLETE` conclusion was later narrowed/refuted as primary root. | No. | Useful semantic context, not current root. |
| `2026-07-01_123749_plane_contract_completeness.md` | Is a universal plane handoff contract missing? | Broad plane contract incompleteness may exist. | Later executable evidence shows current issue can be traced in existing values without new architecture. | No. | Do not use as reason for redesign. |
| `2026-07-01_124517_planner_contract_falsification.md` | Try to refute Planner contract incomplete. | Refuted as primary: Runtime already derives wake from Planner move evidence in good path. | Did not identify current production value divergence. | No. | Important: use executable values, not broad contract theory. |
| `2026-07-01_125541_planner_runtime_data_lineage.md` | Where did data first break? | First broken object was serialized selected move. | Superseded after fix. | No. | Historical; root fixed. |
| `2026-07-01_144247_final_implementation_decision.md` | Was serialization intentional? | No; implementation defect fixed. | Did not solve missing required-service failure. | Yes. | Current baseline: semantic payload survives. |
| `2026-07-01_150144_system_invariant_proof.md` | Which invariant fails? | `FAILOVER_SEMANTIC_BINDING` violated. | Did not prove whether Planner input was wrong or overclassification. | No. | Current invariant framing. |
| `2026-07-01_150727_canonical_truth_proof.md` | What truth authorizes L3 execution? | Composite `EXECUTION_READY`, not Planner/wake/authority alone. | Did not patch. | No. | Prevents bypassing Runtime gates. |
| `2026-07-01_151234_formal_model_verification.md` | Is model deterministic? | Yes; missing mandatory facts -> STOP_SAFE. | Did not distinguish bad input vs overclassification. | No. | Supports Runtime correctness. |
| `2026-07-01_152327_action_class_ownership_proof.md` | Who owns Action Class? | OMP Action-Class Authority owns durable class; Planner owns candidate vocabulary. | Did not patch Planner classification. | No. | Prevents treating Planner `failover` as class authority. |
| `2026-07-01_153255_single_decision_execution_depth.md` | Where does one decision stop being same? | Identity survived; semantics changed. | Did not trace World Model provenance. | No. | Current semantic diagnosis. |
| `2026-07-01_171437_l3_differential_execution_trace.md` | Compare good path vs production path. | First executable divergence is current-source service suitability failure row. | Does not yet prove why Planner saw current not eligible. | No. | Latest highest-confidence evidence. |

Later executable evidence supersedes earlier broad hypotheses. The most current evidence is the differential trace.

## 10. Current Best Diagnosis

Confidence: `HIGH_CONFIDENCE`

Latest high-confidence executable fact:

```text
Good L3 test path:
  selected current source has required-service failure row:
    telegram DOWN / PERSISTENT_FAIL / FRESH
  -> _emergency_failover_move_evidence() returns current_failures non-empty
  -> _l3_wake_decision() accepts wake
  -> emergency_failover_authority_gate passes

Production path:
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

This does not yet prove exactly why the Planner emitted `current_egress_not_eligible`.

Open nuance:

```text
Possibility 1: Planner received wrong or incomplete World Model input.
Possibility 2: Planner received correct input but overclassified broad current_egress_not_eligible as L3 failover.
```

Do not collapse this prematurely into "Planner is wrong" without tracing Planner input provenance.

## 11. Critical Current Unresolved Question

The next unresolved question is not:

```text
Why did Runtime stop?
```

Runtime stopped because `current_failures=[]`, so L3 required-service failure and wake were not proven. That is known.

The real current question is:

```text
Why did Planner see or derive a World Model where awg0 became current_egress_not_eligible,
but no same-subject required-service failure exists for awg0 at Runtime evidence extraction?
```

Equivalent formulation:

```text
Was the Planner input/world model wrong or incomplete?
Or did Planner overclassify a broad current_egress_not_eligible condition as L3 failover?
```

## 12. Next Correct Engineering Step

Do not run another architecture audit.

Next correct step:

```text
World Model Provenance / Planner Input Trace
```

Trace this exact chain:

```text
Observation
  -> Service Matrix
  -> Read Models
  -> Planner Inputs
  -> _decision_for_user()
  -> selected move
  -> _emergency_failover_move_evidence()
```

Target candidate:

```text
user: 10.7.0.5
source: awg0
target: vless
```

For every Planner input record:

- producer;
- file/state source;
- generation;
- timestamp;
- freshness;
- value;
- why Planner saw it;
- whether Runtime saw the same fact;
- first divergence.

Expected output:

```text
FIRST_DIVERGENCE_FOUND
or
TRACE_INCONCLUSIVE
```

If found:

- first divergent fact;
- producer;
- consumer;
- owner;
- exact file/function;
- minimal correction direction.

## 13. Suggested Next Codex Prompt

Use this exact prompt in the next Codex chat:

```text
V7 CODEX TASK — WORLD MODEL PROVENANCE TRACE

Task

Do NOT redesign.
Do NOT patch first.
Do NOT create architecture.
Do NOT create owner.
Do NOT create runtime.
Do NOT create planner.
Do NOT move users.

MISSION

Find whether Planner received incorrect/incomplete World Model or Planner overclassified correct input.

Target candidate:

user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
current_failures: []

READ FIRST

- docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md
- docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md
- docs/reports/engineering/2026-07-01_151234_formal_model_verification.md
- docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md
- docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md
- docs/reference/V7_RUNTIME_MODEL.md
- docs/reference/V7_DECISION_MODEL.md
- docs/reference/SYSTEM_MAP.md

TRACE

Trace executable values only:

Observation
-> Service Matrix
-> Read Models
-> Planner Inputs
-> _decision_for_user()
-> selected move
-> _emergency_failover_move_evidence()

For each fact used by Planner for 10.7.0.5 / awg0 / vless, record:

- producer
- file/state source
- generation
- timestamp
- freshness
- raw value
- normalized value
- why Planner saw current_egress_not_eligible
- whether Runtime saw the same fact
- whether the fact can prove L3 required-service failure

QUESTIONS

1. What exact input made Planner set current_egress_not_eligible?
2. Was that input a required-service failure on awg0?
3. If not, what kind of ineligibility was it?
4. Did Runtime receive the same input?
5. Is the divergence in Observation, World Model, Planner normalization, selected move serialization, or Runtime extraction?
6. Is Planner input wrong/incomplete, or did Planner overclassify correct input as L3 failover?

OUTPUT

Create:

docs/reports/engineering/<timestamp>_world_model_provenance_trace.md

Return exactly:

FIRST_DIVERGENCE_FOUND
or
TRACE_INCONCLUSIVE

If found, return only:

- first divergent fact
- producer
- consumer
- owner
- exact file/function
- minimal correction direction

No implementation unless explicitly requested.
```

## 14. Forbidden Next Actions

Do not:

- create new wake event system;
- create new truth source;
- create new Runtime;
- create new Planner;
- create new authority model;
- create new owner;
- bypass Runtime gate;
- bypass required-service failure;
- treat `current_egress_not_eligible` as sufficient for L3 execution;
- patch Runtime to accept empty `current_failures`;
- certify L3 without movement/verification/learning;
- move more than one user;
- weaken restore barrier;
- weaken approved plan lock;
- weaken verification;
- weaken rollback;
- enable timers;
- enable broad autoswitch;
- mistake reports for canonical truth;
- restart broad architecture investigations.

## 15. Completion Rules

Every future Codex step must:

1. produce an engineering report;
2. include tests for implementation work;
3. run truth/convergence if deployed;
4. update canonical docs if durable knowledge changes;
5. close the loop into a real next consumer;
6. distinguish `PRODUCED`, `CONSUMED`, `CONSUMPTION_VERIFIED`, and `BEHAVIOR_CHANGED`;
7. preserve `STOP_SAFE` unless all required facts are proven;
8. avoid long chat output; put details in files.

## Final Status

```text
GPT_HANDOFF_PACKAGE_CREATED
Current best next task: WORLD_MODEL_PROVENANCE_TRACE
Current unresolved question: bad/incomplete Planner input vs Planner overclassification
Runtime automation enabled: NO
Authority expanded: NO
Users moved latest attempt: 0
```
