# Planner Vs Wake Canonical Truth Audit

Date: 2026-07-01
Workspace: `/Users/ponch/Documents/New project`
Mode: canonical proof, no implementation

## Summary

`Planner Selected Move` and `CONFIRMED_L3_WAKE` are not two independent durable truths.

They are two lifecycle concepts over the same underlying canonical facts:

- current channel failed;
- required service failure exists for the affected user/service context;
- affected user is assigned to the failed source;
- safe target exists;
- selected action is `FAILOVER`;
- reason is `CURRENT_CHANNEL_FAILED`;
- evidence is fresh enough for L3.

Wake is canonical as a runtime lifecycle trigger: it starts observation and prevents blind timer/cron movement.

But `CONFIRMED_L3_WAKE` must not become a second truth source that competes with Planner/Observation evidence. For an L3 execution candidate, it is derivable from a complete L3 Planner decision and its evidence bundle.

Verdict: `PLANNER_CONTRACT_INCOMPLETE`.

## Semantic Duplicate Audit

Searched semantically across canonical docs, reports, implementation, and tests for:

- planner;
- selected move;
- current channel failed;
- required service failure;
- service matrix;
- wake;
- incident;
- event;
- decision;
- recommendation;
- execution;
- authority;
- runtime;
- selected move evidence;
- move evidence;
- failure evidence;
- service evidence;
- packet;
- producer;
- consumer.

Findings:

1. Runtime Model and Autonomous Runtime Model define wake as a lifecycle start from approved event/resume/operator/OMP source.
2. L3 Capability defines entry conditions separately from wake:
   - current channel failed;
   - affected users;
   - required services failed;
   - safe target exists;
   - fresh evidence;
   - authority;
   - restore/rollback readiness.
3. Planner owns candidate selection, blockers, selected move identity, and selected move explanation.
4. Observation owners own service matrix / quality / runtime evidence.
5. Runtime consumes planner output and must not replace planner.
6. Implementation currently supports two paths:
   - external wake event files;
   - inference from selected move evidence.
7. Unit tests demonstrate both concepts, but the external event test creates a separate `l3-wake-events.jsonl`, which is semantically dangerous if it becomes a second truth source instead of an observation input.

## Semantic Definitions

| Concept | Type | Meaning | Canonical owner |
| --- | --- | --- | --- |
| Planner Selected Move | Decision / prepared planning output | Planner-selected bounded candidate: user, source, target, action, reason, blockers, selected move hash, and evidence context. | Planner / Autoswitch |
| CONFIRMED_L3_WAKE | Derived runtime lifecycle state | Runtime may enter L3 observation/execution evaluation because the triggering condition is confirmed and allowed for L3. | Runtime Model consumes; truth comes from observation/planner evidence |
| Current Channel Failure | Fact / derived fact | Current assigned channel is failed for affected user/service context. | Policy 001 + service evidence + runtime truth owners |
| Required Service Failure | Fact / derived fact | Required services for affected users fail on current channel. | Service matrix + user/service policy owners |
| Emergency Candidate | Derived decision candidate | A failover candidate satisfying L3 action class constraints before final live gates. | Planner / Autoswitch |
| L3 Incident | Lifecycle/visibility object | Operator-visible state for a confirmed L3 failure/action context. | Runtime/Incident/report lifecycle owners |

Classification:

- Facts: current channel failure, required service failure, assigned users, service matrix evidence, target readiness facts.
- Derived facts: emergency candidate, current candidate ineligible, safe target exists, confirmed L3 failure context.
- Decisions: planner selected move, execution readiness, terminal outcome classification.
- Permissions: authority envelope, approved plan lock, restore barrier, rollback/verification readiness.

## Dependency Graph

```text
Service Matrix / Observation Plane
  -> Current Channel Failure
  -> Required Service Failure
  -> Planner / Autoswitch
  -> Emergency Candidate
  -> Planner Selected Move
  -> L3 failure evidence bundle
  -> CONFIRMED_L3_WAKE derived for Runtime lifecycle
  -> Incident
  -> Authority / Eligibility
  -> Execution or STOP_SAFE
```

Alternative wake sources such as incident resume or runtime resume are lifecycle resume markers, not independent proof of service failure. They must still resolve to existing incident/evidence context before execution.

## Planner Analysis

For L3, Planner selected move should exist only when these inputs are true:

- user is assigned to current source;
- current source is not eligible for the user's required service context;
- move type is `FAILOVER`;
- reason is `CURRENT_CHANNEL_FAILED` / current egress not eligible;
- target is eligible;
- target service suitability passes;
- target load/capacity passes;
- movement protection / anti-flap / policy gates pass or are explicitly allowed for hard failure;
- selected move hash preserves user/source/target/action identity.

The implementation's `_emergency_failover_move_evidence()` already expects selected moves to contain enough evidence to prove:

- failover-only action;
- current egress not eligible;
- target safe;
- required services on current are failed;
- failure evidence fresh;
- target required services ready.

That means the implementation already partially treats `CONFIRMED_L3_WAKE` as derivable from selected move evidence.

## Wake Analysis

Runtime requires `CONFIRMED_L3_WAKE` to prevent:

- blind polling movement;
- timer/cron movement;
- optimization movement masquerading as emergency;
- stale signal movement;
- movement without fresh failure evidence.

Canonical meaning:

```text
Wake may start observation.
Wake may not grant execution.
```

For execution, wake is not sufficient. Runtime still requires:

- planner selected move;
- authority;
- restore barrier;
- approved plan lock;
- selected move hash match;
- rollback readiness;
- verification readiness;
- source/target live gates.

## Truth Source Audit

Question:

```text
Is CONFIRMED_L3_WAKE already mathematically implied by Planner Selected Move?
```

Answer:

```text
PARTIALLY.
```

It is not implied by a generic selected move.

It is implied by a complete L3-qualified Planner selected move that carries:

- action class: L3 emergency failover;
- action: `FAILOVER`;
- reason: `CURRENT_CHANNEL_FAILED`;
- affected user;
- source;
- target;
- failed required services on source;
- current channel ineligible evidence;
- target eligibility evidence;
- freshness/generation evidence.

If those fields are present, no additional service-failure wake producer is needed to prove the same truth.

If those fields are absent, Runtime cannot safely derive `CONFIRMED_L3_WAKE` from the selected move.

## Duplication Test

Suppose V7 introduces `/opt/v7/events/service-failure-events.jsonl`.

This can be valid only as an Observation Plane input if it remains a raw/confirmed observation consumed before planning.

It becomes duplicated truth if Runtime requires it after Planner has already produced a complete L3 selected move from the same service matrix evidence.

Duplication risk:

```text
Service Matrix FAIL
  -> Planner says Current Channel Failed
  -> separate service-failure event says Current Channel Failed
  -> Runtime requires both
```

That creates two authorities for the same fact and can fail when one path updates before the other.

## Information Comparison

Planner selected move carries:

- user;
- source;
- target;
- action/move type;
- reason/blockers;
- candidate universe;
- target safety;
- selected move hash;
- policy/load/service/route/quality context where preserved.

Wake carries:

- lifecycle start/source;
- event id;
- timestamp;
- source owner;
- freshness;
- allowed/rejected wake-source classification.

Wake introduces information not always present in selected move:

- event identity;
- event timestamp;
- event source owner;
- resume/deduplication semantics.

Wake does not introduce unique proof of current channel failure if the L3 selected move already contains current-channel required-service failure evidence.

Therefore the correct semantic split is:

- wake/resume identity belongs to Runtime lifecycle;
- failure truth belongs to Observation Plane and Planning Plane;
- execution readiness belongs to Runtime gates.

## Canonical Owner Mapping

| Truth / Concept | Canonical owner |
| --- | --- |
| Current Channel Failure | Policy 001 + service matrix / runtime truth owners |
| Required Service Failure | Service matrix + user/service policy owners |
| Confirmed Failure Evidence | Observation Plane, then Planning Plane when attached to candidate |
| Planner Decision | Planner / Autoswitch |
| Selected Move Identity | Planner / packet / lease owners |
| Wake Lifecycle | Runtime Model / event owner / CPS |
| L3 Incident | Runtime/incident/report lifecycle owners |
| Execution Permission | OMP / Policy 004 / authority owners |

## Thought Experiment

Assume Planner selects:

```text
User A
Source X
Target Y
Action: FAILOVER
Reason: CURRENT_CHANNEL_FAILED
Evidence: required services failed on Source X for User A
Freshness: valid
```

Runtime can derive `CONFIRMED_L3_WAKE` without another service-failure producer because the selected move already contains all failure truth required for L3.

If Planner selects only:

```text
User A
Source X
Target Y
Reason: current_egress_not_eligible
```

without failed service/freshness evidence, Runtime cannot derive `CONFIRMED_L3_WAKE` safely.

## Root Cause

The canonical architecture does not require an independent durable `CONFIRMED_L3_WAKE` truth source after Planner has selected a complete L3 move.

The current semantic gap is:

```text
Planner Selected Move contract does not require the L3 failure evidence bundle strongly enough.
```

As a result, Runtime asks for `CONFIRMED_L3_WAKE` as if it were independent, while the implementation already has a derivation path from `move_evidence`.

Root answer:

```text
C. Planner contract is incomplete.
```

## Minimal Semantic Correction

Do not create a second truth source for the same failure.

Define the L3 Planner selected move contract so that any selected move eligible for L3 must carry or reference:

- current channel failed;
- required services failed;
- affected user;
- source;
- target;
- action class;
- reason;
- freshness/generation;
- evidence owner;
- selected move hash.

Then Runtime may derive `CONFIRMED_L3_WAKE` from the complete L3 selected move evidence bundle while still accepting independent wake/resume markers only as lifecycle triggers.

No new architecture, owner, runtime, planner, event bus, or durable truth source is required.

## Final Verdict

`PLANNER_CONTRACT_INCOMPLETE`
