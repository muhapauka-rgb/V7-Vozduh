# V7 Autonomous Runtime Model

Status: canonical autonomous-runtime reference
Owner: Runtime Model / OMP / Autonomous Execution Program composition
Mode: documentation-only
Runtime impact: NONE
Authority impact: NONE
User movement: NONE

## 1. Purpose

The V7 Autonomous Runtime Model defines how autonomous Runtime lives.

It answers:

```text
How does Autonomous Runtime wake, observe, decide, execute, verify, rollback, learn, suspend, and sleep?
```

It is a specialized extension of `docs/reference/V7_RUNTIME_MODEL.md`.

It is not a replacement for the Runtime Model. The Runtime Model owns executable runtime semantics, time architecture, Work Placement, decision lifecycle, live/precompute boundaries, fail-closed behavior, and runtime laws. This document narrows those rules to the future certified autonomous runtime loop.

It is the operational layer between:

```text
Product Specification
  -> OMP
  -> Autonomous Execution Program
  -> Autonomous Runtime Model
  -> Existing Runtime Owners
  -> Production Runtime
```

It consumes `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md`, which answers:

```text
When is V7 allowed to execute without an operator?
```

This document does not grant that permission. It only defines how Runtime must behave after OMP, authority, policy, certification, readiness, and live gates already allow execution.

This document does not implement daemon/timer behavior, runtime apply, restore-barrier writes, rollback apply, authority expansion, synthetic evidence, user movement, production automation, new Runtime, new Planner, new Authority, new OMP, new Governance, new Truth Source, or a roadmap.

## 1.1. Runtime Operating System

Autonomous Runtime behaves like an operating system for production routing actions.

It owns orchestration.

Existing owners own implementation.

Autonomous Runtime is not another Runtime.

Autonomous Runtime is not another Planner.

Autonomous Runtime is not another Authority.

Autonomous Runtime is the orchestration layer that coordinates existing owners:

```text
Event
  -> Dispatch to existing owner
  -> Consume owner result
  -> Execute / STOP_SAFE / Sleep
```

Runtime owns:

- lifecycle orchestration;
- state transitions;
- event dispatch;
- readiness aggregation;
- execute-or-stop decision point;
- terminal closure coordination;
- sleep/wake discipline.

Runtime does not own:

- planner logic;
- authority policy;
- evidence generation;
- policy design;
- execution implementation;
- verification implementation;
- rollback implementation;
- learning implementation;
- OMP certification;
- truth source.

## 2. Runtime Operating Principles

Autonomous Runtime follows these laws:

1. Observe reality.
2. Never assume.
3. Wake only for real events.
4. Reuse existing owners.
5. Execute only inside certified authority.
6. Verify every mutation.
7. Roll back before expansion.
8. Roll back or contain on failure.
9. Fail closed.
10. Learn only from terminal reality.
11. Sleep when nothing is needed.
12. Stop on stale, missing, contradictory, or unsafe evidence.

Permanent growth law:

```text
Autonomous Runtime never grows by adding Runtime behavior.
Autonomous Runtime grows by orchestrating additional certified action classes.
Runtime remains stable.
Certified capability set grows.
```

Autonomous Runtime is a bounded control loop, not independent intelligence.

It consumes prepared knowledge from existing owners, applies live safety gates, and chooses only:

```text
EXECUTE
STOP_SAFE
ASK_OPERATOR
SUSPEND
INCIDENT
SLEEP
```

Runtime confidence is not runtime authority.

Runtime speed is not runtime safety.

Runtime recommendation is not runtime execution.

## 3. Autonomous Control Loop

The Autonomous Control Loop is the primary Runtime law.

Runtime must be understood as a loop, not as a collection of components.

Canonical loop:

```text
Sleep
  -> Wake
  -> Observe
  -> Need Action?
  -> No
  -> Sleep
  -> Yes
  -> Classify
  -> Build Current World
  -> Need Existing Plan?
  -> Need Fresh Evidence?
  -> Planner
  -> Authority
  -> Execution Eligibility
  -> Execute OR STOP_SAFE
  -> Verify
  -> Rollback / Contain
  -> Learn
  -> Update Read Models
  -> Report
  -> Sleep
```

| Step | Purpose | Inputs | Outputs | Owner | Stop condition | Forbidden behavior |
| --- | --- | --- | --- | --- | --- | --- |
| Sleep | End safe cycle and wait for approved wake source. | Terminal state, no eligible action, or closed incident. | `IDLE`. | Runtime Model / CPS. | None. | Hidden polling movement or blind autoswitch. |
| Wake | Start runtime review from approved source. | Approved wake event or resume marker. | `WAKE`. | Runtime Model / existing event owner. | Unknown, stale, synthetic, or unauthorized wake source. | Cron-based movement without event. |
| Observe | Read current reality. | Runtime state, service, route, channel, user, policy, freshness evidence. | Observation evidence. | Observation Plane owners. | Missing required reality source. | Mutation, planning replacement, synthetic evidence. |
| Need Action? | Decide whether observed state requires any certified response. | Observation evidence, desired state, policy, current incident state. | `YES`, `NO`, or `STOP_SAFE`. | Runtime Model / Decision Model / OMP. | No certified action exists or evidence is not actionable. | Busy loop or synthetic action creation. |
| Classify | Classify event/action family. | Detection signal, policies, action-class registry. | Action class candidate or `NO_ACTION`. | OMP / Policy owners / Decision Model. | Unknown failure mode or uncertified class. | Invent new class in Runtime. |
| Build Current World | Build compact current-state view. | Prepared read models and live observations. | Current world snapshot. | World Model Plane owners. | Required state missing or stale beyond class allowance. | Broad historical scans in Runtime. |
| Need Existing Plan? | Decide whether an existing plan/decision can be reused. | Current world, decision id, lease/packet state, material state. | Reuse, refresh, or STOP_SAFE. | Decision Model / packet/lease owners. | Material change or missing idempotency key. | Silent plan replacement. |
| Need Fresh Evidence? | Decide whether prepared knowledge is fresh enough. | Freshness, owner version, TTL/window, evidence source. | Use existing evidence, refresh read-only evidence, or STOP_SAFE. | Freshness / evidence owners. | Missing or stale mandatory evidence. | Runtime heavy recomputation. |
| Planner | Select bounded candidate or stop. | Delta, candidates, gates, movement protection. | Decision/proposal candidate. | Existing planner/autoswitch owners. | No safe target or no net benefit. | Planner rerun after committed execution identity. |
| Authority | Confirm current authority envelope. | Action class, policy, subject, target, blast, risk, authority generation. | `AUTHORITY_PASS` or authority stop. | OMP / Policy 004 / delegated authority. | Missing, stale, changed, or exceeded authority. | Runtime grants authority. |
| Execution Eligibility | Combine live gates. | Freshness, rollback, verification, anti-flap, blast, restore barrier, budget, suspension. | `EXECUTION_READY` or `STOP_SAFE`. | Runtime Model + existing gate owners. | Any mandatory live gate fails. | Confidence overrides failed readiness. |
| Execute or STOP_SAFE | Mutate only if all gates pass. | Execution contract, lease, packet/transaction, restore barrier. | Apply result or safe stop. | Execution owners. | Identity mismatch, material change, budget exhausted, kill switch, suspension. | Apply outside certified envelope. |
| Verify | Prove result. | Verification plan, route/service checks, timeout. | Verification result. | Verification owners. | Verification unavailable or failed. | Treat apply success as terminal success. |
| Rollback / Contain | Recover or contain failed action. | Rollback/no-rollback contract, rollback target, containment policy. | Rollback result or containment state. | Rollback / restore owners. | Rollback unavailable or failed. | Silent failure or unverified recovery. |
| Close Terminal Outcome | Classify final state. | Apply, verification, rollback/containment. | `SUCCESS`, `ROLLBACK_SUCCESS`, `ROLLBACK_FAILURE`, `APPLY_FAILURE`, `NO_EXECUTION`, or incident. | Runtime / feedback owners. | Terminal state cannot be proven. | Classify from intermediate apply state. |
| Learn | Convert terminal reality into evidence. | Terminal outcome, prediction, root cause, observed reality. | Learning delta. | Feedback / Learning / Engineering Intelligence. | Synthetic or incomplete outcome. | Improve trust from unverified evidence. |
| Update Read Models | Refresh compact consumers. | Learning delta, health, maturity, CPS changes. | Read-model updates or missing-owner record. | Read-model owners. | Missing durable owner. | Runtime writes canonical truth directly. |
| Report | Preserve historical evidence. | Action, gates, outcome, learning, blockers. | Engineering report / event report. | OMP report lifecycle. | Report owner unavailable. | Reports become backlog or canonical owner. |
| Sleep | Finish cycle. | Closed report/state. | `IDLE` or `SUSPENDED`. | Runtime Model / CPS. | Incident remains open. | Continue hidden loop after terminal closure. |

## 4. Runtime State Machine

| State | Meaning | Entry condition | Allowed transitions | Forbidden transitions | Owner | Terminal |
| --- | --- | --- | --- | --- | --- | --- |
| `IDLE` | Runtime is asleep and safe. | No active authorized cycle. | `WAKE`, `SUSPENDED`. | `EXECUTING` directly. | Runtime Model / CPS. | Non-terminal. |
| `WAKE` | Approved wake source arrived. | Event/resume/operator/OMP trigger accepted. | `OBSERVE`, `STOP_SAFE`. | `EXECUTING`. | Wake source owner. | Non-terminal. |
| `OBSERVE` | Runtime reads current reality. | Wake accepted. | `CLASSIFY`, `SLEEP`, `STOP_SAFE`. | Planning or execution without evidence. | Observation owners. | Non-terminal. |
| `CLASSIFY` | Event/action family is mapped. | Actionable signal exists. | `WORLD_READY`, `WAITING_AUTHORITY`, `STOP_SAFE`, `SLEEP`, `INCIDENT_OPEN`. | New class creation in Runtime. | Policy / OMP / Decision Model. | Non-terminal. |
| `WORLD_READY` | Current world and desired delta are available. | Observation and classification pass. | `PLAN_READY`, `WAITING_AUTHORITY`, `STOP_SAFE`, `SLEEP`, `INCIDENT_OPEN`. | Execute directly. | World Model / Decision Model. | Non-terminal. |
| `PLAN_READY` | Existing planner produced bounded candidate or no-action. | Candidate is owner-mapped and identity-stable. | `WAITING_AUTHORITY`, `READY`, `STOP_SAFE`, `SLEEP`. | Apply directly or silently replace committed plan. | Planner/autoswitch. | Non-terminal. |
| `WAITING_AUTHORITY` | Runtime lacks operational or autonomous authority. | Candidate needs approval or class is not certified for autonomous execution. | `READY`, `STOP_SAFE`, `SLEEP`, `INCIDENT_OPEN`. | Authority self-grant. | OMP / Authority. | Non-terminal. |
| `READY` | Runtime can enter one bounded execution attempt. | Readiness, authority, budget, rollback/no-rollback, verification, and circuit breaker pass. | `EXECUTING`, `STOP_SAFE`. | Planner replacement or hidden batch expansion. | Runtime Model / execution owners. | Non-terminal. |
| `EXECUTING` | Mutation is being applied through existing execution owners. | Execution contract consumed. | `VERIFYING`, `ROLLBACK`, `STOP_SAFE`, `INCIDENT_OPEN`. | Silent retry, hidden batch, or execution outside envelope. | Execution owners. | Non-terminal. |
| `VERIFYING` | Post-action proof is running. | Apply attempted or containment requires proof. | `LEARNING`, `ROLLBACK`, `INCIDENT_OPEN`, `STOP_SAFE`. | Success without verification. | Verification owners. | Non-terminal. |
| `ROLLBACK` | Rollback or containment is required or running. | Verification failed, apply failed, or containment is required. | `VERIFYING`, `LEARNING`, `INCIDENT_OPEN`, `SUSPENDED`, `STOP_SAFE`. | Mark success, hidden second apply, or unverified recovery. | Rollback / restore owners. | Non-terminal. |
| `LEARNING` | Terminal reality is consumed. | Terminal outcome exists. | `REPORTING`, `SUSPENDED`, `INCIDENT_CLOSED`. | Authority promotion by Runtime. | Learning / EI / OMP. | Non-terminal. |
| `REPORTING` | Runtime/report owners preserve terminal evidence. | Learning or STOP_SAFE requires report. | `SLEEP`, `SUSPENDED`, `INCIDENT_CLOSED`. | Report becomes authority, roadmap, or backlog. | OMP report lifecycle. | Non-terminal. |
| `STOP_SAFE` | Safe non-execution or aborted path. | Any mandatory gate failed before unsafe mutation or an execution owner failed closed. | `REPORTING`, `LEARNING`, `INCIDENT_OPEN`, `SLEEP`, `SUSPENDED`. | Apply. | Runtime Model. | Terminal or non-terminal depending on reporting/incident. |
| `SUSPENDED` | Autonomy is stopped for scope. | Circuit breaker, kill switch, OMP review, unsafe health, or unknown failure mode. | `IDLE`, `WAKE` only after review/recovery. | Autonomous execute while suspended. | OMP / Runtime. | Terminal for autonomous cycle. |
| `INCIDENT_OPEN` | Operator-visible incident exists. | Unsafe condition requires visibility or manual review. | `VERIFYING`, `ROLLBACK`, `LEARNING`, `REPORTING`, `INCIDENT_CLOSED`, `SUSPENDED`. | Silent sleep without report. | Incident/report owners. | Non-terminal. |
| `INCIDENT_CLOSED` | Incident has terminal closure. | Resolution, containment, learning, and report are recorded. | `SLEEP`, `SUSPENDED`. | Execute. | OMP / report lifecycle. | Terminal. |
| `SLEEP` | Runtime intentionally returns to idle. | No action, terminal closure, or safe suspension path is complete. | `IDLE`, `WAKE`, `SUSPENDED`. | Hidden loop or hidden movement. | Runtime Model / CPS. | Terminal for the cycle. |

Canonical deduplication rule:

```text
Every runtime state is named once.
Old aliases such as CLASSIFYING, PLANNING, READY_TO_EXECUTE, ROLLBACK_REQUIRED, and ROLLING_BACK are non-canonical synonyms and must not be used in future implementation.
```

## 5. Incident Lifecycle

| Incident state | Opens when | Advances when | Closes when | Suspends when | Operator view |
| --- | --- | --- | --- | --- | --- |
| `NO_INCIDENT` | No actionable unsafe condition. | Approved wake detects possible issue. | Already closed. | Not applicable. | No active incident. |
| `POTENTIAL_INCIDENT` | Regression, failure, or contradiction appears. | Evidence confirms service/user impact. | Evidence disproves issue. | Evidence remains contradictory. | Signal, source, freshness, uncertainty. |
| `INCIDENT_CONFIRMED` | Hard failure, degradation, recovery hazard, capacity risk, or policy risk is confirmed. | Action candidate is built. | Condition naturally clears and is verified. | Unknown failure mode appears. | Impact, affected subject, confidence, readiness. |
| `ACTION_CANDIDATE` | Existing planner/action class finds possible safe action. | Authority check begins. | No safe action exists and incident is contained/reported. | Candidate identity/material state unstable. | Candidate, target, blockers, alternatives. |
| `AUTHORITY_CHECK` | Candidate needs authority validation. | Authority passes or stops. | Authority denied and incident reported. | Authority mismatch or policy change. | Authority class, required approval, certified bounds. |
| `EXECUTION_IN_PROGRESS` | Runtime applies certified bounded action. | Apply completes. | Apply fails before mutation and stops safely. | Hidden mover/envelope mismatch. | Live execution status. |
| `VERIFYING_RECOVERY` | Apply finished and proof is required. | Verification passes/fails/times out. | Recovery verified. | Verification unknown or unstable. | Verification checks and timeout. |
| `ROLLBACK_OR_CONTAINMENT` | Verification fails or rollback needed. | Rollback/containment completes. | Containment or rollback verified. | Rollback fails or unknown failure mode. | Rollback target, status, risk. |
| `RESOLVED` | Service is restored or safe containment is proven. | Learning begins. | Learning and report complete. | Post-resolution regression. | Resolution evidence and residual risk. |
| `LEARNING` | Terminal outcome exists. | Learning delta and report are produced. | Learning recorded. | Learning owner missing. | Outcome, root cause, future recommendation. |
| `CLOSED` | Terminal outcome, learning, and report exist. | New wake source appears later. | Already closed. | Not applicable. | Closed incident summary. |
| `SUSPENDED_FOR_REVIEW` | Circuit breaker, kill switch, unknown failure, or repeated unsafe outcome occurs. | OMP review or certified recovery condition clears suspension. | OMP reopens certified scope or retires action. | Remains suspended. | Suspension reason, owner, next required review. |

## 6. Wake Sources

Approved wake sources:

- service regression;
- route regression;
- channel failure;
- hard failure;
- soft degradation;
- recovery signal;
- capacity event;
- policy event;
- operator event;
- verification event;
- rollback event;
- OMP-certified scheduled evidence refresh if read-only;
- recorded-state resume.

Rejected wake sources:

- blind timer movement;
- cron-based user movement;
- daemon movement without event;
- stale evidence wake;
- synthetic trigger;
- broad autoswitch loop.

Wake source rule:

```text
Wake may start observation.
Wake may not grant execution.
```

## 7. Readiness Model

Readiness is separate from confidence.

Confidence can be high while readiness is low.

Runtime execution requires readiness, not confidence alone.

| State | Meaning | Runtime behavior |
| --- | --- | --- |
| `NOT_READY` | Required owner/gate/evidence is missing. | Stop or continue read-only. |
| `READ_ONLY_READY` | Observation and diagnostics are safe. | Read/report only. |
| `PROPOSAL_READY` | A non-mutating candidate can be explained. | Proposal/why-card only. |
| `EXECUTION_READY` | Authority, live gates, budget, identity, and restore barrier allow one execution. | May execute only inside certified envelope. |
| `VERIFICATION_READY` | Post-action proof is available. | Verification can proceed. |
| `ROLLBACK_READY` | Rollback or containment path is available or no-rollback is certified. | Apply may proceed only if other gates pass. |
| `AUTONOMOUS_READY` | Action class, policy, authority, readiness, budget, health, and certification all pass. | Runtime may execute automatically inside bounds. |
| `STOP_SAFE` | Readiness failed. | No unsafe mutation. |

## 8. Confidence Model

Confidence informs authority and OMP review.

Confidence never grants execution by itself.

| Confidence component | Meaning | Owner |
| --- | --- | --- |
| Decision confidence | Whether selected decision matches observed reality and policy. | Decision Model / Planner / Engineering Intelligence. |
| Evidence confidence | Whether evidence is fresh, representative, and source-owned. | Evidence owners / OMP. |
| Execution confidence | Whether execution identity and live gates are stable. | Runtime Model / execution owners. |
| Verification confidence | Whether post-action proof is reliable. | Verification owners. |
| Rollback confidence | Whether rollback/containment is ready and proven. | Rollback owners / Policy 007. |
| Learning confidence | Whether terminal outcome can be learned correctly. | Feedback / Learning / EI. |
| Autonomy health confidence | Whether the action class remains safe over time. | Production Maturity / OMP / EI. |

Rule:

```text
Low confidence may block certification or trigger review.
High confidence may not override failed readiness.
```

## 9. Runtime Budgets

| Budget | Purpose | Owner | Runtime consumption | Stop condition |
| --- | --- | --- | --- | --- |
| Execution budget | Limit number of executions per scope/window. | OMP / Autonomous Execution Program. | Runtime checks remaining certified execution allowance. | Budget exhausted or unknown. |
| Blast-radius budget | Limit users/channels/cohorts/pools affected. | Policy 006 / OMP. | Runtime checks selected subject scope. | Scope exceeds certification. |
| Risk budget | Limit certified risk class. | OMP / Authority policy. | Runtime checks risk envelope. | Unknown or higher risk than authority. |
| Time budget | Limit action to valid window/latency/freshness class. | Runtime Model / Freshness owners. | Runtime checks TTL/window/staleness. | Expired or uncertified stale allowance. |
| Incident budget | Limit autonomous action during incident context. | OMP / incident owner. | Runtime checks incident state and allowed action count. | Incident budget exhausted or unclear. |
| Recovery budget | Limit recovery admission and reversals. | Recovery policy / OMP. | Runtime checks slow-start/recovery allowance. | Recovery too fast or anti-flap risk. |
| Rollback budget | Limit rollback/containment risk. | Rollback owner / Policy 007. | Runtime checks rollback capacity/path. | Rollback unavailable or too risky. |
| Operator-intervention budget | Track how often autonomy needs human override. | OMP / Production Maturity. | Runtime may continue only if class not downgraded. | Override rate triggers suspension/review. |

## 10. Circuit Breaker

Autonomous circuit breaker states:

| State | Meaning | Runtime behavior |
| --- | --- | --- |
| `CLOSED` | Certified action class may execute inside gates. | Normal autonomous eligibility may proceed. |
| `HALF_OPEN` | One bounded validation action may be allowed. | Only one certified validation action, then verify/learn/review. |
| `OPEN` | Autonomy is stopped. | Runtime must STOP_SAFE or ask operator. |

Open breaker on:

- verification failure threshold;
- rollback failure;
- repeated `STOP_SAFE` for same class;
- unknown failure mode;
- hidden mover;
- envelope mismatch;
- authority mismatch;
- operator kill switch;
- confidence/readiness collapse.

Breaker rule:

```text
Circuit breaker stops autonomy.
It does not delete observation, read-only diagnostics, reporting, or learning.
```

## 11. Suspension Model

Suspension scopes:

- global suspension;
- action-class suspension;
- channel suspension;
- target suspension;
- user/cohort suspension;
- policy suspension.

Suspension must:

- stop autonomous execution;
- preserve read-only observation;
- notify operator;
- require OMP review or certified recovery condition.

Suspension must not:

- erase evidence;
- silently expand authority;
- convert Runtime into manual planner;
- block safety reporting.

## 12. Idempotency

Canonical idempotency keys:

- event id;
- incident id;
- decision id;
- operation id;
- selected move hash;
- packet id;
- restore generation;
- authority generation;
- current state generation;
- verification result id;
- outcome id.

Rules:

```text
Same material state + same certified decision must not duplicate execution.
Repeated wake must become no-op, resume, verify, rollback, or STOP_SAFE.
Material state change requires new decision or STOP_SAFE.
```

Idempotency is required before autonomous certification.

## 13. Reconciliation

Autonomous Runtime reconciles:

```text
Observed State
  -> Desired State
  -> Delta
  -> Action Candidate
  -> Execution Eligibility
  -> Terminal Outcome
```

Runtime compares desired vs observed.

Runtime does not invent desired state.

Desired State comes from:

- Business Objectives;
- Canonical Policies;
- certified action classes;
- OMP;
- Decision Model.

If observed state already satisfies desired state, Runtime sleeps.

If delta exists but no certified action is safe, Runtime stops safely or opens incident visibility.

## 14. Execution Contracts

| Contract | Required fields | Owner | Failure behavior | STOP_SAFE behavior |
| --- | --- | --- | --- | --- |
| Wake contract | wake source, event id, timestamp, source owner, freshness. | Runtime Model / event owner. | Unknown wake rejected. | Sleep or report stale wake. |
| Observation contract | reality source, freshness, current state generation, evidence owner. | Observation owners. | Missing reality blocks action. | Read-only report. |
| Decision contract | action class, subject, source, target, reason, policy, decision id. | Decision Model / planner. | Unknown class or unstable identity blocks action. | No execution. |
| Execution contract | operation id, packet/transaction id, selected move hash, authority generation, restore generation. | Execution owners. | Identity mismatch fails closed. | No apply. |
| Verification contract | expected result, method, timeout, owner, failure action. | Verification owners. | Verification failure triggers rollback/containment. | Incident or rollback path. |
| Rollback contract | rollback target, readiness, no-rollback proof, containment path. | Rollback owners. | Rollback failure opens incident/suspension. | Stop before apply if not ready. |
| Incident contract | incident id, severity, affected scope, owner, current state. | Incident/report owners. | Missing incident owner blocks autonomous closure. | Operator-visible incident. |
| Learning contract | prediction, actual, terminal outcome, root cause, engineering delta. | Feedback / Learning / EI. | Incomplete learning cannot promote. | Report missing learning owner. |
| Reporting contract | summary, action, evidence, gates, outcome, maturity impact, next step. | OMP report lifecycle. | Missing report blocks certification evidence. | Report blocker in CPS/OMP where relevant. |

## 15. Learning Loop

Learning loop:

```text
Prediction
  -> Action
  -> Observed Reality
  -> Difference
  -> Terminal Outcome
  -> Knowledge Delta
  -> Engineering Intelligence
  -> OMP Certification / Downgrade / Promotion
```

Rules:

- Learning uses terminal outcomes only.
- Intermediate apply state is not learning.
- Synthetic evidence is forbidden.
- Rollback success is not execution success.
- `STOP_SAFE` is learning about gates, not production movement.
- Engineering Intelligence may recommend certification, downgrade, or promotion.
- Only OMP may certify, downgrade, or promote autonomy.

## 16. Runtime Health

Runtime health states:

| State | Meaning | Effect |
| --- | --- | --- |
| `HEALTHY` | Runtime can consume certified action classes safely. | Normal certified eligibility may proceed. |
| `DEGRADED` | Some evidence, confidence, readiness, or outcomes are weaker than expected. | May recommend review, smaller budget, or downgrade. |
| `RECOVERING` | Runtime/action class is returning after failure or suspension. | Half-open or validation-only behavior. |
| `SUSPENDED` | Autonomy stopped for scope. | No autonomous execution. |
| `STOPPED` | Runtime cannot safely process autonomous cycle. | Operator/OMP review required. |
| `UNKNOWN` | Health cannot be proven. | STOP_SAFE for autonomous execution. |

Health is read-only.

Health may recommend suspension, downgrade, or operator review.

Health never grants authority.

## 17. Operator Visibility

Operator/UI must see:

- current runtime state;
- current incident;
- automation level;
- action class;
- authority state;
- readiness state;
- confidence state;
- execution budget;
- circuit breaker state;
- selected users;
- target;
- verification result;
- rollback result;
- terminal outcome;
- next action.

Operator visibility is explanatory and supervisory.

It may request approval or show override controls only through existing authority owners.

It must not become Runtime, Planner, authority, or certification owner.

## 18. Integration

| Concept | Existing owner / consumer |
| --- | --- |
| Runtime laws, live gates, execute-or-stop | `docs/reference/V7_RUNTIME_MODEL.md` |
| When execution is allowed | `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` |
| Decision semantics | `docs/reference/V7_DECISION_MODEL.md` |
| Certification, promotion, downgrade, suspension review | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Production maturity and health impact | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` |
| Prediction, confidence, recommendation, learning analysis | Engineering Intelligence owners |
| Volatile runtime/program state | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Owner lookup | `docs/reference/SYSTEM_MAP.md` |
| Durable truth summary | `docs/reference/V7_CANONICAL_REFERENCE.md` |
| Policies | Canonical Policies |
| Planner / candidate owner | `tools/v7-users-autoswitch` |
| Execution owner | `admin_core/operator_execution.py` |
| Execution pipeline owner | `admin_core/operator_execution_pipeline.py` |
| Autonomy read-model owner | `admin_core/autonomy_trust_acceleration.py` |
| Operator/API visibility | `admin/v7-admin-api` |

Need New Owner: `FALSE`.

Need New Runtime: `FALSE`.

Need New Planner: `FALSE`.

Need New Authority: `FALSE`.

Need New Truth Source: `FALSE`.

## 18.1. Runtime Dispatcher

Runtime dispatches work.

Runtime should not perform heavy work itself.

Dispatcher rule:

```text
Runtime asks the owner that owns the question.
Runtime consumes the owner result.
Runtime does not become that owner.
```

| Runtime question | Dispatch target | Runtime consumes |
| --- | --- | --- |
| What happened? | Evidence Owner / Observation Plane. | Fresh observed fact or missing evidence. |
| Is there a candidate? | Planner Owner. | Candidate, no-action, or blocker. |
| Is action allowed? | Authority Owner / OMP / Policy 004. | Authority pass, ask operator, or deny. |
| Is execution safe now? | Runtime gate owners. | Execute readiness or STOP_SAFE. |
| How to mutate? | Execution Owner. | Apply result or fail-closed result. |
| Did it work? | Verification Owner. | Verification pass/fail/unknown. |
| How to recover? | Rollback Owner. | Rollback, containment, or no-rollback result. |
| What did we learn? | Learning Owner / Engineering Intelligence. | Learning delta or missing-learning blocker. |
| What must operator see? | Reporting/UI owners. | Report, incident, dashboard state. |

Existing owners remain responsible.

Runtime remains responsible for ordering, state transition, and stopping when an owner cannot prove its result.

## 18.2. Runtime Event Model

Every Runtime event defines:

- wake source;
- owner;
- priority;
- whether execution is possible.

| Event | Wake source | Owner | Priority | Execution possible |
| --- | --- | --- | --- | --- |
| Service Failure | service regression / hard failure. | Service/evidence owners + Policy 001. | Safety / Service Restoration. | Yes, only if certified failover readiness passes. |
| Recovery | recovery signal. | Recovery owners + Policy 003. | Recovery. | Yes, only through certified recovery admission. |
| Capacity Change | capacity/load event. | Capacity/load owners + Policy 006. | Optimization after safety. | Yes, only after rebalance class certification. |
| Policy Change | policy event. | Product/Policy/OMP owners. | Safety. | Usually no; may require stop/re-evaluation. |
| Verification Result | verification event. | Verification owners. | Verification. | No new action unless rollback/containment required. |
| Rollback Result | rollback event. | Rollback owners. | Rollback / Learning. | No new primary action; close or incident. |
| Operator Request | operator event. | OMP / authority owners. | Depends on requested scope. | Only inside approved authority. |
| Evidence Refresh | OMP-certified read-only refresh. | Evidence/read-model owners. | Observation. | No direct execution authority. |
| Incident Update | incident owner update. | Incident/report owners. | Safety / Reporting. | Only if linked to certified action. |

## 18.3. Runtime Scheduling

Runtime scheduling is priority ordering, not a new scheduler implementation.

Priority order:

1. Safety.
2. Recovery.
3. Service Restoration.
4. Verification.
5. Rollback.
6. Learning.
7. Reporting.
8. Optimization.

Rules:

- optimization must never preempt recovery;
- recovery must not bypass verification or anti-flap;
- rollback/containment must preempt new movement;
- reporting must not delay required rollback;
- learning must not grant new authority;
- scheduling cannot create a queue daemon or blind timer movement.

## 18.4. Runtime Performance

Runtime must remain:

- deterministic;
- bounded;
- event-driven;
- minimal;
- idempotent.

No heavy computation belongs in Runtime.

Heavy computation belongs to existing background owners:

- observation/read-model builders;
- intelligence snapshots;
- planner read models;
- Engineering Intelligence;
- OMP certification;
- reports and audits;
- Production Maturity.

Runtime performance rule:

```text
Runtime spends prepared knowledge.
Runtime does live safety work.
Runtime does not research, audit, scan long history, certify, or optimize broadly.
```

## 18.5. Industry Mapping

| Runtime Operating System concept | Equivalent production pattern | Equivalent V7 owner |
| --- | --- | --- |
| Control loop | Kubernetes controllers / Borg desired-state reconciliation. | Runtime Model + Decision Model + OMP. |
| Dispatcher | OS/system controller dispatching to subsystems. | Runtime Model over existing owners. |
| Event-driven wake | SRE automation and control-plane event loops. | Event/evidence owners + CPS. |
| Circuit breaker | Envoy outlier/circuit breaking and rollout aborts. | OMP + Production Maturity + Runtime Model. |
| Progressive execution | Istio/Argo/Cloudflare/AWS/Azure staged traffic control. | Autonomous Execution Program + OMP. |
| Health/readiness gates | Kubernetes probes, cloud health checks, service mesh readiness. | Runtime Model + verification/readiness owners. |
| Intent/policy separation | Cisco/Juniper/Arista/NSX intent/change-control systems. | Product Specification + Policies + OMP + Runtime Model. |
| Thin execution path | Service mesh / control-plane-to-data-plane separation. | Work Placement Law + Runtime Model. |
| Operator override | SRE incident controls and cloud routing controls. | OMP + Authority policy + CPS. |

## 18.6. Future Consumption

Future capabilities consume this Runtime Operating System.

Runtime itself does not change.

Only the certified action-class set grows.

| Capability | How it consumes Runtime OS |
| --- | --- |
| L3 Emergency Failover | Uses event wake, service-failure classification, one bounded execution, verification, rollback/containment, learning, suspension. |
| L4 Degraded Channel Autonomy | Uses soft-degradation event, state-change cost, anti-flap, confidence/readiness split, metric-driven stop. |
| L5 Recovery Autonomy | Uses recovery wake, slow-start, half-open validation, rollback/containment, anti-flap. |
| L6 Rebalance | Uses capacity event, execution budgets, blast-radius budget, optimization-lower-priority scheduling. |
| L7 Full Routing Autonomy | Uses all certified classes inside approved policy with circuit breaker, health, budgets, and operator override. |

Growth rule:

```text
New autonomy = new certified action-class consumption.
New autonomy != new Runtime behavior.
```

## 19. L3 Consumption Contract

L3 Emergency Autonomous Failover consumes this model only after OMP certification and authority approval.

This section defines consumption. It does not implement L3.

| Field | L3 contract |
| --- | --- |
| Wake source | Confirmed service failure / hard failure on current channel affecting assigned users. |
| State path | `IDLE -> WAKE -> OBSERVE -> CLASSIFY -> WORLD_READY -> PLAN_READY -> WAITING_AUTHORITY or READY or STOP_SAFE -> EXECUTING -> VERIFYING -> ROLLBACK or LEARNING -> REPORTING -> SLEEP or SUSPENDED`. |
| Authority mode | Certified emergency failover authority inside approved Delegated Autonomy Policy or current approved emergency envelope. |
| Readiness gates | Evidence, freshness, source/target eligibility, rollback/no-rollback, verification, restore barrier, blast radius, anti-flap, movement protection, budget, circuit breaker. |
| Execution budget | One certified bounded failover action at the current L3 certification scope unless OMP certifies expansion. |
| Verification | Immediate route and required-service verification. |
| Rollback | Rollback/containment required unless no-rollback is certified for the action class. |
| Incident visibility | Incident opens on confirmed failure and remains visible until terminal outcome and learning close. |
| Learning | Terminal outcome feeds Engineering Intelligence, Production Maturity, OMP, and future certification. |
| Suspension on failure | Verification failure threshold, rollback failure, hidden mover, envelope mismatch, unknown failure, or kill switch opens breaker/suspension. |

L3 must never:

- execute rebalance;
- optimize capacity cosmetically;
- move more users than certified;
- bypass live gates;
- retry silently;
- expand authority;
- create synthetic evidence.

## 20. Implementation Handoff

Architecture work for autonomous Runtime is complete.

Future work proceeds through OMP implementation only.

No further architecture documents are expected before L3 implementation unless a future audit proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

Implementation order:

1. Stage 1: Canonical Integration.
2. Stage 2: OMP Integration.
3. Stage 3: L3 Emergency Autonomous Failover Design.
4. Stage 4: L3 Implementation.
5. Stage 5: L3 Production Validation.
6. Stage 6: L3 Certification.
7. L4.
8. L5.
9. L6.
10. L7.

Next engineering task:

```text
Canonical Integration
```

The next task is implementation alignment, not new architecture.

## 21. Autonomy Architecture Lock

Architecture lock review:

| Contract area | Existing owner | Status |
| --- | --- | --- |
| Runtime | Runtime Model + Autonomous Runtime Model. | Complete. |
| Decision Model | Decision Model. | Complete. |
| Execution Program | Autonomous Execution Program + existing execution owners. | Complete. |
| OMP | Operational Maturity Program. | Complete. |
| Policies | Canonical Policy Library. | Complete and consumed. |
| SYSTEM_MAP | SYSTEM_MAP. | Complete ownership lookup. |
| Canonical Reference | Canonical Reference. | Complete durable truth. |
| Existing owners | Runtime, planner, authority, execution, verification, rollback, learning, OMP owners. | Sufficient. |

Need New Runtime: `FALSE`.

Need New Planner: `FALSE`.

Need New Authority: `FALSE`.

Need New OMP: `FALSE`.

Need New Governance: `FALSE`.

Need New Truth Source: `FALSE`.

Need New Roadmap: `FALSE`.

Autonomy architecture lock verdict:

```text
ARCHITECTURE_LOCKED_FOR_AUTONOMY_IMPLEMENTATION
```

## 22. Post-Lock Implementation Rule

After architecture lock, future autonomy work must not create:

- new Runtime documents;
- new Planner documents;
- new Authority documents;
- new automation roadmap;
- new execution architecture;
- new autonomy framework.

Future work proceeds only through:

```text
OMP
  -> implementation
  -> tests
  -> verification
  -> production validation
  -> certification
```

## 23. Runtime Stability Law

The Runtime Operating System remains stable.

Autonomy grows only by adding certified action classes.

Autonomy must never grow by changing Runtime OS behavior.

Runtime OS may change only if one of the following is true:

- production evidence proves a contract contradiction;
- explicit operator request requires architectural review;
- a certified audit proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 24. Runtime Evolution Policy

Runtime Operating System is intentionally stable.

Runtime OS may change only when one of the following is proven:

- production evidence contradicts an existing Runtime contract;
- certified implementation proves a fundamental architecture contradiction;
- explicit operator-approved architecture review authorizes architecture work.

Everything else must extend certified action classes.

New capabilities must not extend Runtime behavior.

Evolution rule:

```text
New capability -> certified action-class extension.
New capability != Runtime OS extension.
```

## 25. Implementation Consumers

Future autonomy levels consume the same Runtime Operating System.

The Runtime OS itself remains unchanged.

| Consumer | How it consumes the Runtime OS |
| --- | --- |
| L3 Emergency Autonomous Failover | Consumes event wake, hard-failure/service-failure classification, bounded execution, verification, rollback/containment, learning, reporting, suspension. |
| L4 Degraded Channel Autonomy | Consumes soft-degradation classification, state-change cost, anti-flap, confidence/readiness separation, metric-driven stop. |
| L5 Recovery Autonomy | Consumes recovery wake, recovery admission, slow-start, half-open validation, rollback/containment, anti-flap. |
| L6 Bounded Rebalance | Consumes capacity event, blast-radius budget, execution budget, optimization-lower-priority scheduling. |
| L7 Full Routing Autonomy | Consumes all certified action classes inside approved policy with circuit breaker, health, budgets, and operator override. |

Consumer rule:

```text
Every new capability consumes Runtime OS.
Runtime OS remains unchanged.
```

## 26. Implementation Ownership Chain

Autonomous execution implementation follows one permanent ownership chain:

```text
Architecture
  -> OMP
  -> Existing Owners
  -> Implementation
  -> Testing
  -> Production Validation
  -> Certification
  -> Promotion
```

| Level | Responsibility | Owner rule |
| --- | --- | --- |
| Architecture | Defines stable contracts and boundaries. | Closed by default after this document. |
| OMP | Selects and sequences work through the existing implementation backlog and maturity program. | OMP is the only execution program. |
| Existing Owners | Own evidence, planning, authority, execution, verification, rollback, learning, reporting, and truth. | No duplicate owners. |
| Implementation | Changes only existing owners and modules required by OMP. | No new Runtime, Planner, Authority, OMP, Truth Source, or roadmap. |
| Testing | Proves behavior, regression safety, fail-closed behavior, and owner contracts. | Tests must map to existing owners. |
| Production Validation | Uses real production evidence inside approved authority. | No synthetic evidence or hidden automation. |
| Certification | Determines whether action class/capability maturity can advance. | OMP/certification owners decide, not Runtime. |
| Promotion | Expands capability only after certification and authority allow it. | Promotion is action-class/policy capability growth, not Runtime OS growth. |

## 27. Architecture Exit Criteria

Architecture phase is complete only when all criteria are satisfied:

| Exit criterion | Status | Owner |
| --- | --- | --- |
| Product Specification exists. | PASS. | Product Specification. |
| Runtime Model exists. | PASS. | Runtime Model. |
| Decision Model exists. | PASS. | Decision Model. |
| Autonomous Execution Program exists. | PASS. | Autonomous Execution Program. |
| Autonomous Runtime Model exists. | PASS. | Autonomous Runtime Model. |
| Architecture Lock PASS. | PASS. | Autonomous Runtime Model / Canonical Reference. |
| Canonical Integration completed. | PASS for architecture references; implementation integration continues through OMP. | Canonical Reference / SYSTEM_MAP / OMP. |
| OMP consumes all autonomy documents. | PASS as architecture contract; implementation consumption continues through OMP execution. | OMP. |
| No missing architecture contracts remain. | PASS. | Architecture Lock Review. |

Architecture Phase:

```text
COMPLETE
```

## 28. Architecture Completion Declaration

Architecture work for autonomous execution is finished.

Future engineering must proceed through:

```text
OMP
  -> Implementation
  -> Testing
  -> Verification
  -> Production Validation
  -> Certification
  -> Promotion
```

No new architecture documents should normally be created.

Architecture may reopen only if future implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP` or the operator explicitly requests architecture review.

Final architecture certification verdict:

```text
AUTONOMY_ARCHITECTURE_COMPLETE
```

## 29. Final Validation

Architecture Audit: PASS. This document is an extension of existing Runtime Model and Autonomous Execution Program. It creates no architecture.

Owner Audit: PASS. All concepts map to existing owners.

Runtime Audit: PASS. Runtime behavior is unchanged; the model is documentation-only.

Runtime State Deduplication Audit: PASS. Runtime state names are canonicalized once; old duplicate aliases are non-canonical synonyms.

Control Loop Certification Audit: PASS. Every control-loop step has purpose, owner, output, stop condition, and forbidden behavior.

Decision Audit: PASS. Decision semantics remain owned by Decision Model.

OMP Audit: PASS. Certification, promotion, downgrade, and suspension review remain owned by OMP.

Execution Audit: PASS. Execution owners remain `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, packet/lease owners, restore barrier, and autoswitch owners.

Authority Audit: PASS. No authority is granted or expanded.

Engineering Intelligence Audit: PASS. Engineering Intelligence may recommend, never authorize.

Conflict Audit: PASS. No conflict found with Runtime Model, Decision Model, OMP, or Autonomous Execution Program.

Duplicate Owner Audit: PASS. No duplicate Runtime, Planner, Authority, OMP, Governance, Truth Source, or roadmap created.

Architecture Lock Review: PASS. Existing Runtime, Decision, Execution, OMP, Policy, SYSTEM_MAP, Canonical Reference, and owner contracts are sufficient for autonomy implementation.

Architecture Exit Criteria Audit: PASS. Product Specification, Runtime Model, Decision Model, Autonomous Execution Program, Autonomous Runtime Model, Architecture Lock, canonical references, OMP consumption contract, and architecture contracts are present.

Industry Compatibility Audit: PASS. The model aligns with production practices from autonomous control loops, self-healing systems, progressive delivery, circuit breakers, health-based failover, and intent-based networking while reusing V7 owners.

Truth Source Audit: PASS. Runtime reality, read models, Canonical Reference, SYSTEM_MAP, OMP, and Current Program State retain existing roles.

Final verdict:

```text
AUTONOMY_ARCHITECTURE_COMPLETE
```
