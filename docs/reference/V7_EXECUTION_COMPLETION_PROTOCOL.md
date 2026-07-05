# V7 Execution Completion Protocol

Status: canonical execution-investigation protocol
Owner: OMP / Runtime Model / Decision Model composition
Mode: documentation-only
Need New Owner: FALSE
Runtime impact: NONE
Planner impact: NONE
Production impact: NONE
User movement authority: NONE

## 1. Mission

The V7 Execution Completion Protocol defines how Codex must investigate and complete future V7 production executions.

The protocol changes the default posture from:

```text
find the next blocker
```

to:

```text
complete the execution through existing V7 owners
```

It applies to L3, L4, L5, L6, L7, and future capability levels.

It does not create a Runtime, Planner, Authority, Wake, Event Bus, Truth Source, OMP, owner, roadmap, execution path, apply path, or user-movement authority.

It composes existing owners:

- OMP owns execution program discipline and next safe action.
- Runtime Model owns execute-or-stop lifecycle semantics.
- Autonomous Runtime Model owns future certified autonomous orchestration semantics.
- Decision Model owns decision semantics.
- SYSTEM_MAP owns owner lookup.
- Production Maturity owns maturity impact from real outcomes.
- Current Program State owns volatile current execution state.
- Engineering Reports preserve historical evidence.

## 2. Completion Definition

An execution investigation is complete only when exactly one terminal state is reached:

```text
SUCCESS
```

or

```text
CANONICAL_IMPOSSIBILITY
```

Everything else is:

```text
INCOMPLETE_EXECUTION
```

Finding a blocker is not completion.

Writing a report is not completion.

Producing a recommendation is not completion.

Returning `STOP_SAFE` is not completion.

Stopping at authority, policy, missing evidence, stale evidence, wrong data, implementation defect, identity drift, or report boundary is not completion unless the protocol proves canonical impossibility.

## 3. Execution Law

Codex is forbidden to terminate an execution investigation because a blocker was found.

Every blocker is a breakpoint.

After understanding the blocker, Codex must resume the original execution from the same breakpoint through existing owners.

The execution chain is:

```text
Production reality
  -> Observation
  -> World model
  -> Planner / decision owner
  -> Authority
  -> Runtime
  -> Apply or STOP_SAFE
  -> Verify
  -> Rollback or contain if needed
  -> Outcome
  -> Learning
  -> Current Program State / OMP update
  -> Complete
```

The goal is not to prove why the system stopped.

The goal is to complete the legally allowed production execution or prove that the existing architecture cannot legally complete it.

## 4. Breakpoint Law

Every STOP, `STOP_SAFE`, blocker, authority boundary, missing evidence state, stale evidence state, wrong-data state, failed gate, or identity mismatch must trigger the breakpoint procedure:

```text
freeze state
  -> identify producer
  -> identify consumer
  -> identify owner
  -> identify exact condition
  -> prove why STOP occurred
  -> classify STOP
  -> define minimal correction if needed
  -> resume execution from the same breakpoint
```

STOP classification must be exactly one primary class:

| Class | Meaning | Next action |
| --- | --- | --- |
| `EXPECTED` | Existing canonical rule stopped correctly. | Continue through the canonical next owner, authority request, evidence refresh, or safe no-action path. |
| `IMPLEMENTATION_DEFECT` | Existing owner behavior violates its canonical contract. | Produce minimal correction direction, then resume the same execution after correction or explicit implementation approval. |
| `POLICY` | Existing policy forbids the action. | Continue to policy owner / OMP authority decision; do not bypass. |
| `AUTHORITY` | Action may be valid but lacks approved authority. | Continue to authority owner / OMP / operator approval path. |
| `MISSING_EVIDENCE` | Mandatory evidence was never persisted or produced. | Continue to evidence owner or produce observability-only persistence requirement. |
| `STALE_EVIDENCE` | Evidence exists but is no longer fresh enough. | Continue to evidence refresh owner. |
| `WRONG_DATA` | The object contains incorrect or contradictory data. | Continue to producer and truth owner; do not consume silently. |
| `IMPOSSIBLE_STATE` | Required facts are contradictory under canonical rules. | Attempt canonical impossibility proof. |

The breakpoint report must not become the terminal artifact unless it proves `SUCCESS` or `CANONICAL_IMPOSSIBILITY`.

## 5. Reality First Law

Real production execution overrides synthetic examples.

Synthetic examples may explain code behavior.

Only real production executions may certify production behavior, maturity, authority evolution, or execution completion.

Codex must prefer:

```text
current production facts
  -> persisted production artifacts
  -> owner-produced reports
  -> source code
  -> tests / fixtures
  -> synthetic examples
```

Tests and fixtures can prove possibility, regression behavior, or code semantics.

They cannot certify that a real production execution completed.

## 6. Investigation Continuation Law

Investigation must continue until:

```text
SUCCESS
```

or

```text
CANONICAL_IMPOSSIBILITY
```

If a report discovers a blocker, the next report must continue from that blocker.

If a correction is required but not approved, Codex must classify the execution as `INCOMPLETE_EXECUTION_BLOCKED_ON_APPROVAL`, preserve the breakpoint, and name the exact approval or implementation owner. That is a pause, not completion.

If evidence is missing, Codex must continue to the evidence owner and prove whether the missing object was:

- intentionally not persisted;
- omitted by engineering;
- omitted by report generation;
- deleted by artifact cleanup;
- expired by retention policy;
- never produced.

Codex must not start a new investigation from Observation unless the current execution is mathematically impossible to continue or the operator explicitly starts a new execution.

## 7. Candidate Identity Law

Once a production execution begins, Codex must preserve the candidate identity through every investigation step.

Required identity fields:

| Field | Requirement |
| --- | --- |
| `operation_id` | Must remain stable if present. |
| `planner_generation` / `planner_generation_id` | Must remain stable if present. |
| `selected_move_hash` | Must remain stable for selected executable move identity. |
| `user` | Must not change silently. |
| `source` | Must not change silently. |
| `target` | Must not change silently. |
| `action` | Must be tracked when it changes. |
| `move_type` | Must be tracked when it changes. |
| `reason` | Must be tracked when appended, overwritten, filtered, or consumed. |
| `selected_move_exists` | Must be explicit. |
| `approved_plan_lock` | Must be explicit. |
| `restore_barrier_generation` | Must be explicit when relevant. |
| artifact path | Must be named. |

Changing the investigated execution object is forbidden.

If object change is unavoidable, Codex must:

```text
stop
  -> justify the object change
  -> prove why the original object cannot continue
  -> mark the original execution INCOMPLETE_EXECUTION or CANONICAL_IMPOSSIBILITY
  -> explicitly restart under a new execution identity
```

No report may use a new candidate to explain an old candidate unless it proves identity equivalence.

## 8. Object Continuity Law

Object continuity means the same execution object is preserved across:

- reports;
- planner artifacts;
- selected moves;
- approved plan locks;
- restore barrier records;
- runtime packets;
- verification records;
- rollback records;
- learning records;
- Current Program State updates.

The object must not be replaced by:

- another user;
- another source;
- another target;
- another selected move;
- another operation id;
- another planner generation;
- another fixture;
- another production incident;
- another candidate from the same plan;
- a synthetic test object.

If any continuity field is missing, Codex must write:

```text
NOT_PERSISTED
```

or

```text
UNKNOWN_FROM_PERSISTED_EVIDENCE
```

Codex must not infer continuity from similar shape, similar reason, same code path, or same broad incident family.

## 9. Execution Continuity Law

Investigation always continues from the current breakpoint.

It must not continue from:

- the beginning;
- Observation;
- a new Planner run;
- another candidate;
- another user;
- another source;
- another target;
- another report's convenient artifact;
- a current production state replay, unless the breakpoint explicitly requires fresh state.

Allowed continuation forms:

| Breakpoint type | Continue from |
| --- | --- |
| Planner defect | The exact Planner producer and same candidate identity. |
| Authority boundary | The same candidate and authority owner. |
| Runtime STOP_SAFE | The same selected move / packet / lock / Runtime gate. |
| Missing evidence | The missing object owner and the same operation identity. |
| Stale evidence | The same evidence owner and freshness refresh path. |
| Verification failure | The same apply attempt and verification owner. |
| Rollback required | The same mutation and rollback owner. |
| Learning missing | The same outcome and learning owner. |

Restarting from Observation is allowed only when a canonical owner proves that material production reality changed enough to invalidate the current execution object. The restarted investigation must use a new explicit execution identity.

## 10. Evidence Law

Every execution investigation must preserve evidence sufficient to continue execution.

Minimum evidence per breakpoint:

- frozen candidate identity;
- object before;
- object after;
- producer;
- consumer;
- owner;
- exact function or artifact;
- exact condition;
- freshness;
- authority state;
- policy basis;
- selected move identity;
- approved plan lock state;
- restore barrier state;
- verification readiness;
- rollback readiness;
- current execution position;
- next execution step.

Evidence must distinguish:

- persisted production fact;
- current live production fact;
- historical report evidence;
- code proof;
- fixture proof;
- synthetic example;
- inference.

Inference may guide investigation.

Inference may not certify completion.

## 11. Stop Conditions

Terminal stop conditions:

| Stop | Meaning |
| --- | --- |
| `SUCCESS` | One real user legally reaches another healthy channel, verification passes, rollback state is safe, outcome is recorded, learning is preserved, and Current Program State / OMP can consume the result. |
| `CANONICAL_IMPOSSIBILITY` | A mathematical proof shows the existing architecture and canonical owners cannot legally complete the execution. |

Non-terminal pause conditions:

| Pause | Meaning |
| --- | --- |
| `OPERATIONAL_AUTHORITY_REQUIRED` | Human or certified authority is required before mutation. |
| `IMPLEMENTATION_APPROVAL_REQUIRED` | Minimal correction is known but implementation is not approved. |
| `EVIDENCE_OWNER_REQUIRED` | Mandatory evidence must be produced or recovered by an existing owner. |
| `PRODUCTION_ACCESS_REQUIRED` | Real production fact is required and not available in the current workspace. |
| `USER_ABORTED` | Operator explicitly stops the investigation. |

Pause conditions must be recorded as `INCOMPLETE_EXECUTION`, not success.

## 12. Canonical Impossibility Definition

`CANONICAL_IMPOSSIBILITY` means:

```text
No legal path exists through current canonical V7 owners,
under current policy and authority,
to complete the same execution object.
```

It requires proof of all of the following:

1. The candidate identity is frozen and preserved.
2. Every existing owner that could legally continue the execution has been checked.
3. No existing owner can produce the required evidence, authority, decision, packet, execution, verification, rollback, or learning state.
4. The missing capability cannot be represented by reuse or extension of existing owners.
5. Continuing would violate a canonical rule, policy, authority boundary, identity boundary, or safety invariant.
6. The contradiction is not caused by missing local files, stale workspace, incomplete report reading, current-state drift, or candidate switch.

Canonical impossibility is stronger than "blocked".

Canonical impossibility is stronger than "not implemented".

Canonical impossibility is stronger than "requires approval".

## 13. Implementation Defect Definition

`IMPLEMENTATION_DEFECT` means:

```text
An existing owner has a canonical responsibility,
but the implementation output violates that responsibility for the frozen execution object.
```

Examples:

- Planner emits an action class without required canonical facts.
- Runtime consumes the wrong identity.
- Authority envelope drops selected-move fields.
- Restore barrier suppresses proposal visibility when canonical execution requires review visibility.
- Report generation omits mandatory continuation evidence.
- Verification closes an outcome without proof.
- Learning improves maturity from synthetic evidence.

An implementation defect must include:

- exact owner;
- exact file or artifact;
- exact function or producer;
- exact field;
- expected canonical behavior;
- actual behavior;
- minimal correction direction;
- same-breakpoint resume plan.

## 14. Execution Completion Definition

`SUCCESS` requires all of the following:

1. Real production execution object preserved.
2. Authority legally permits the action.
3. Planner / decision owner selected a valid action for the same object.
4. Runtime consumed the same object.
5. One real user moved only if movement was authorized.
6. Target channel was healthy for the user's required services.
7. Source, target, and user identity remained stable.
8. Verification passed or a certified no-rollback/no-mutation closure was produced.
9. Rollback readiness was preserved or rollback was executed if required.
10. Outcome was recorded.
11. Learning consumed observed outcome evidence only.
12. Current Program State and OMP can consume the terminal result.

If any element is false or unknown, execution is not complete.

## 15. Engineering Report Requirements

Every breakpoint investigation report must include:

| Required section | Content |
| --- | --- |
| `summary` | What happened at this breakpoint. |
| `current breakpoint` | Exact execution position. |
| `frozen identity` | operation id, planner generation, selected hash, user, source, target, action, move type, reason, artifact. |
| `producer` | First writer of the blocking fact. |
| `consumer` | First consumer that stopped or changed behavior. |
| `owner` | Existing canonical owner. |
| `exact condition` | Boolean or field condition that stopped execution. |
| `proof` | Persisted evidence, code proof, or live production fact. |
| `classification` | Expected, implementation defect, policy, authority, missing evidence, stale evidence, wrong data, impossible state. |
| `minimal correction` | Smallest correction direction if correction is needed. |
| `current execution position` | Where to resume. |
| `next execution step` | The next owner/action required to continue. |
| `terminal status` | `SUCCESS`, `CANONICAL_IMPOSSIBILITY`, or `INCOMPLETE_EXECUTION`. |

No engineering report may terminate the investigation merely because it found a blocker.

The next report must continue from the same breakpoint unless the prior report reached a terminal stop.

## 16. When Codex Is Allowed To Stop

Codex may stop only when one of the following is true:

1. `SUCCESS` is proven.
2. `CANONICAL_IMPOSSIBILITY` is proven.
3. The operator explicitly stops, pauses, or redirects the investigation.
4. Required production authority or production access is unavailable in the current environment.
5. Required implementation approval is unavailable and Codex is forbidden to patch.

Cases 3-5 are pauses, not completion.

For pauses, Codex must preserve:

- frozen identity;
- breakpoint state;
- exact owner required next;
- exact missing approval, access, or implementation;
- next resume command.

## 17. When Codex Is Forbidden To Stop

Codex is forbidden to stop when:

- it found a blocker but has not traced producer, consumer, owner, and exact condition;
- it proved a defect but has not named the minimal correction direction;
- it wrote a report but did not identify the next execution step;
- it reached `STOP_SAFE` but did not classify why;
- it found missing evidence but did not identify the missing object and owner;
- it found stale evidence but did not identify the refresh owner;
- it found authority blockage but did not identify the authority owner and approval path;
- it changed candidates without explicit identity restart;
- it used a fixture to explain a real candidate without proving identity equivalence;
- it used current production state to replace a historical execution object without proving material restart conditions;
- it produced `NO_CHANGE` without proving state transition impossibility or next safe action.

## 18. Compatibility Matrix

| Existing canonical document | Existing rule | Protocol compatibility |
| --- | --- | --- |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | OMP is the permanent production operating program; Continue OMP means execute the Engineering Control Loop through existing owners until an allowed stop condition. | Compatible. This protocol specializes execution-investigation continuation and keeps OMP as scheduler/optimizer. |
| `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Current Program State stores volatile current reality, blockers, readiness, stop reason, and next safe action; it cannot approve apply or move users. | Compatible. This protocol requires breakpoint state to be resumable and leaves volatile state ownership to CPS. |
| `docs/reference/V7_RUNTIME_MODEL.md` | Runtime is thin; it executes, stops, verifies, rolls back, records outcomes, and feeds learning through existing owners. | Compatible. This protocol does not make Runtime a decision maker; it forces investigations to continue after Runtime stop. |
| `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | Autonomous Runtime orchestrates existing owners after authority and certification; it does not grant authority or create new owners. | Compatible. This protocol uses the same orchestration discipline for investigations. |
| `docs/reference/V7_DECISION_MODEL.md` | Decision != Execution; policy, evidence, authority, rollback, verification, and learning are explicit decision inputs. | Compatible. This protocol preserves decision identity and requires execution completion evidence. |
| `docs/reference/SYSTEM_MAP.md` | SYSTEM_MAP owns owner/topology lookup only and forbids duplicate owners. | Compatible. This protocol requires owner lookup but creates no owner. |
| `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` | Production Maturity increases only from real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy. | Compatible. This protocol states synthetic examples cannot certify completion. |
| `docs/reference/V7_RESEARCH_PROCESS.md` | Discover -> Reuse -> Extend -> Implement; reuse analysis before new architecture. | Compatible. This protocol applies reuse-first discipline to execution breakpoints. |
| `docs/reference/V7_ENGINEERING_PRINCIPLES.md` | Reality First, Behavior Propagation, State Transition, Continue OMP; no process may terminate at diagnosis or report without transition explanation. | Compatible. This protocol makes that rule concrete for production execution investigations. |
| `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | Execution follows evidence, authority, verification, rollback readiness; Runtime stops safely when mandatory gates fail. | Compatible. This protocol treats STOP_SAFE as a breakpoint unless terminal impossibility is proven. |
| Engineering Reports | Reports preserve evidence and history; reports are not roadmap or authority. | Compatible. This protocol upgrades report content requirements without making reports execution authority. |

Compatibility verdict:

```text
NO_CONFLICT_FOUND
```

## 19. Migration Plan

Existing and future investigations should migrate as follows:

1. Add a `Frozen Identity` section to every execution report.
2. Add a `Current Breakpoint` section to every STOP/blocked report.
3. Replace terminal blocker verdicts with `INCOMPLETE_EXECUTION` unless `SUCCESS` or `CANONICAL_IMPOSSIBILITY` is proven.
4. Add `Next Execution Step` to every report.
5. Require the next report to start from the prior report's breakpoint.
6. For historical investigations, audit whether the candidate identity changed between reports.
7. If identity changed, reclassify later findings as belonging only to the new identity.
8. If the raw execution object was not persisted, write `NOT_PERSISTED` and continue to the evidence owner rather than switching candidates.
9. If implementation is required, route through OMP/backlog/existing owner; do not patch inside this protocol.
10. If operational authority is required, stop as `INCOMPLETE_EXECUTION_BLOCKED_ON_AUTHORITY`, not as completed.
11. If production access is required, preserve breakpoint and exact query/object required.
12. After real execution succeeds, require verification, rollback/containment status, outcome closure, learning, and CPS/OMP consumption before `SUCCESS`.

## 20. Ambiguities Or Missing Rules

The following rules may need future owner clarification:

| Ambiguity | Existing likely owner | Needed clarification |
| --- | --- | --- |
| Exact durable storage path for full production Planner candidate traces. | OMP + Planner/autoswitch owner + Engineering Reports. | Define mandatory persistence path for execution candidate identity and gate state. |
| Whether every production validation attempt must persist selected move hash even when no selected move exists. | Runtime Model + Planner/autoswitch owner. | Define null-vs-absent semantics for candidate-without-selected-move. |
| Standard resume command format after a breakpoint report. | OMP + Current Program State. | Define a compact `resume_from_breakpoint` field. |
| How long breakpoint artifacts must be retained. | Engineering Reports + production retention owner. | Define retention period for production execution evidence. |
| Whether authority-bound pauses should update Current Program State every time. | OMP + CPS. | Define when a pause changes volatile state enough to write CPS. |
| Cross-capability identity vocabulary for L4-L7. | Decision Model + Runtime Model + capability specs. | Ensure all future capabilities have operation, generation, object, authority, verification, and learning identity fields. |

These ambiguities do not block this protocol because they are handled as `INCOMPLETE_EXECUTION` or owner-routed continuation states.

## 21. Recommended Improvements

Recommended future improvements:

1. Add a standard `Execution Breakpoint Record` schema under an existing evidence/report owner.
2. Require production validation reports to persist full candidate identity, candidate rows, selected move identity, and gate results.
3. Add a `resume_from_breakpoint` field to engineering reports.
4. Add a report linter that rejects terminal blocker reports without `SUCCESS`, `CANONICAL_IMPOSSIBILITY`, or `INCOMPLETE_EXECUTION`.
5. Add an identity-continuity checklist to Planner/Runtime/Authority investigations.
6. Add a retention rule for production execution artifacts until verification, rollback/no-rollback closure, learning, and CPS/OMP consumption complete.
7. Add a Current Program State pointer to the active production execution breakpoint when an execution is paused.
8. Add capability-level execution completion checklists for L3-L7 that inherit this protocol.

## 22. Final Rule

Codex must behave as an execution engineer.

An execution engineer does not stop at the first blocker.

An execution engineer freezes the object, proves the stop, fixes or routes the blocker through the existing owner, and resumes the same execution until:

```text
SUCCESS
```

or

```text
CANONICAL_IMPOSSIBILITY
```

Any other result is:

```text
INCOMPLETE_EXECUTION
```
