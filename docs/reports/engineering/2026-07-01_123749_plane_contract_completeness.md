# Plane Contract Completeness Audit

Date: 2026-07-01
Workspace: `/Users/ponch/Documents/New project`
Mode: platform-level architecture proof

## Summary

V7 has canonical architectural planes and has strong behavior-closure rules.

However, V7 does not yet have a complete universal contract for what information must be carried across every adjacent plane boundary.

The L3 issue is the first visible symptom of that incomplete plane handoff contract:

```text
Observation / Planning knew the hard-failure evidence,
but the downstream Runtime wake/eligibility consumer required the same truth
without a complete canonical handoff payload from the producer plane.
```

Verdict: `PLANE_CONTRACT_INCOMPLETE`.

## Semantic Duplicate Audit

Searched semantically across canonical references, OMP, policies, reports, capability specs, and source surfaces for:

- planner;
- runtime;
- observation;
- authority;
- execution;
- verification;
- rollback;
- learning;
- production maturity;
- OMP;
- CPS;
- incident;
- packet;
- restore barrier;
- execution pipeline;
- service matrix;
- truth;
- convergence;
- capability;
- decision;
- transition;
- producer;
- consumer.

Existing equivalent concepts found:

1. `V7_RUNTIME_MODEL` defines the Runtime Time Architecture:
   - Observation Plane;
   - World Model Plane;
   - Planning Plane;
   - Execution Plane;
   - Verification Plane;
   - Feedback / Learning Plane;
   - OMP / Certification Plane.
2. `SYSTEM_MAP` maps those planes to existing owners.
3. `OPERATIONAL_MATURITY_PROGRAM` defines Execution Closure, Verified Consumption, Behavior Enforcement, and State Transition Law.
4. `V7_SYSTEM_ARCHITECTURE` defines subsystem inputs, outputs, consumers, and end-to-end information flow.
5. `V7_AUTONOMOUS_RUNTIME_MODEL` defines the autonomous control loop and execution contracts.
6. `V7_PRODUCTION_MATURITY_MODEL` and `V7_CURRENT_PROGRAM_STATE` define downstream maturity and volatile-state behavior contracts.

Missing equivalent:

No single canonical rule requires each plane handoff to transmit the full minimum semantic payload required by the next plane, including truth provenance, identity, evidence, freshness, authority, and consumer obligation.

This is not a missing owner or missing plane. It is an incomplete cross-plane handoff contract.

## All Existing Planes

| Plane | Canonical owner | Purpose | Current completeness |
| --- | --- | --- | --- |
| Observation Plane | Service matrix, quality compact, sentinel, route/runtime truth owners | Observe production reality and evidence freshness. | Complete as plane. |
| World Model Plane | Knowledge Plane, intelligence snapshots, Current Program State, read-model owners | Maintain compact current state/read models. | Complete as plane. |
| Planning Plane | Planner/autoswitch, operator decision surface, A5/A6/B13 owners | Produce candidate universe, selected moves, target readiness, blocker explanations. | Complete as plane, partial as handoff producer. |
| Authority Plane | OMP, Policy 004, delegated authority owners | Confirm scope/action/blast/policy authority. | Complete as plane, partial in cross-plane payload binding. |
| Execution Plane / Runtime Plane | Runtime Model, execution pipeline, packet/lease, restore barrier, autoswitch apply owners | Execute or STOP_SAFE in a short deterministic path. | Complete as plane, partial as consumer contract. |
| Verification Plane | Verification/runtime readiness owners, truth/convergence where applicable | Prove mutation result and trigger rollback/containment. | Complete as plane, partial in universal handoff fields. |
| Rollback / Containment Plane | Restore/rollback owners, Policy 007 | Recover or contain failed mutation. | Complete as plane, partial in universal handoff fields. |
| Feedback / Learning Plane | Feedback, learning, evidence inventory, trust/read-model owners | Convert terminal reality into feedback, trust, evidence, and learning. | Complete as plane, partial in propagation contract. |
| OMP / Certification Plane | OMP, CPS, Backlog, Production Maturity Model | Decide maturity, certification, authority progression, next work. | Complete as plane. |
| Current Program State Plane | CPS owner | Store volatile current bottleneck, stage, stop reason, next action. | Complete as plane. |
| Production Maturity Plane | Production Maturity Model | Consume certified maturity impact and produce maturity decisions. | Complete as plane. |
| Truth / Convergence Plane | Truth/convergence owners | Verify repo/runtime/deploy alignment and production truth. | Complete as plane. |
| Incident / Operator Visibility Plane | Runtime/incident/report lifecycle, Admin UI/operator surfaces | Expose incident/action state to operator. | Complete as plane, partial in universal handoff fields. |

No new plane is required.

## Plane Contract Matrix

| Contract | Producer | Consumer | Information transferred | Completeness |
| --- | --- | --- | --- | --- |
| Observation -> World Model | Observation owners | Knowledge/read-model owners | health, service matrix, quality, route/runtime truth, timestamps/freshness | Complete |
| World Model -> Planning | Knowledge/read models | Planner/autoswitch | users, channels, policies, service fit, capacity, trust, suitability | Partial |
| Planning -> Authority | Planner/autoswitch | Authority/OMP/policy owners | action class, subject, source, target, blast scope, reason, selected move hash | Partial |
| Planning -> Runtime/Execution | Planner/autoswitch | Runtime/execution owners | selected move, blockers, target, source, identity, evidence context | Incomplete |
| Authority -> Runtime/Execution | Authority owners | Runtime/execution owners | authority generation, envelope, scope, allowed action, expiry | Partial |
| Execution -> Verification | Execution owners | Verification owners | operation id, mutation result, subject, source, target, verification plan | Partial |
| Verification -> Rollback | Verification owners | Rollback/containment owners | verification result, failed dimensions, rollback trigger | Partial |
| Verification/Rollback -> Feedback/Learning | Verification/rollback owners | Feedback/learning owners | terminal state, outcome classification, rollback result, root cause | Partial |
| Feedback/Learning -> OMP/Production Maturity | Learning/evidence owners | OMP / Production Maturity | terminal learning, evidence impact, maturity impact | Complete enough |
| OMP/Production Maturity -> CPS | OMP / Production Maturity | CPS | current phase, blocker, maturity, next action, no-change reason | Complete |
| CPS -> Runtime/OMP | CPS | Runtime / OMP | current stop reason, next action, volatile state pointer | Complete enough |

## Contract Completeness

| Contract | Complete | Partial | Missing | Duplicated | Overlapping |
| --- | --- | --- | --- | --- | --- |
| Observation -> World Model | YES | NO | NO | NO | NO |
| World Model -> Planning | NO | YES | NO | NO | YES |
| Planning -> Authority | NO | YES | NO | NO | YES |
| Planning -> Runtime/Execution | NO | NO | YES as universal contract | YES in practice | YES |
| Authority -> Runtime/Execution | NO | YES | NO | NO | YES |
| Execution -> Verification | NO | YES | NO | NO | YES |
| Verification -> Rollback | NO | YES | NO | NO | YES |
| Verification/Rollback -> Feedback/Learning | NO | YES | NO | NO | YES |
| Feedback/Learning -> OMP/Production Maturity | YES | NO | NO | NO | NO |
| OMP/Production Maturity -> CPS | YES | NO | NO | NO | NO |

The critical gap is not that planes are unnamed.

The critical gap is that adjacent plane contracts do not require a complete, canonical handoff payload that prevents downstream consumers from rediscovering producer facts.

## Information Completeness

| Boundary | Does producer transmit everything consumer needs? | Consumer rediscovery risk |
| --- | --- | --- |
| Observation -> Planning | Mostly yes through service matrix/read models. | Medium: hard-failure classification can be recomputed in planner and runtime. |
| Planning -> Runtime | No. Selected move identity exists, but full evidence/provenance requirements are not universally required. | High: Runtime may require wake/failure truth already implied by planner. |
| Authority -> Runtime | Partial. Authority exists, but exact binding to action/evidence/identity can depend on separate artifacts. | Medium. |
| Execution -> Verification | Partial. Verification plan exists but terminal verification semantics have required later fixes. | Medium. |
| Verification -> Learning | Partial. Terminal state classification was previously wrong when apply succeeded but verification failed and rollback completed. | Medium. |
| Learning -> OMP | Mostly yes through OMP behavior and Production Maturity contracts. | Low. |
| OMP -> CPS | Yes. CPS behavior contract is explicit. | Low. |

## Truth Source Audit

Detected duplicated-truth risk:

| Duplicated truth | Producer plane | Consumer plane reconstructing it | Risk |
| --- | --- | --- | --- |
| Current channel failed | Observation / Planning | Runtime wake gate | Runtime asks for `CONFIRMED_L3_WAKE` after Planner already selected failover. |
| Required service failure | Observation / Planning | Runtime wake / eligibility | Same service matrix fact can become separate wake truth. |
| Selected move identity | Planning / packet owner | Execution / restore barrier | Hash/lock/packet artifacts can diverge if handoff does not bind all identity fields. |
| Terminal outcome | Verification / rollback | Learning | Learning may classify from intermediate apply result unless terminal-state handoff is explicit. |
| Maturity impact | OMP/certification | CPS/dashboard | Mostly controlled by Production Maturity and CPS contracts. |

The L3 wake problem is therefore not isolated. It belongs to a broader class:

```text
Producer plane proves a fact.
Consumer plane requires the fact.
Contract does not force the fact to cross the boundary in canonical form.
Consumer either reconstructs it or requires a parallel artifact.
```

## Contract Minimality

| Contract | Minimality verdict |
| --- | --- |
| Observation -> World Model | Minimal enough. |
| World Model -> Planning | Partial; needs explicit evidence/provenance obligation for planning outputs. |
| Planning -> Runtime/Execution | Incomplete; current selected move contract is underspecified. |
| Authority -> Runtime/Execution | Partial; authority binding should include consumed subject/source/target/action/evidence identity. |
| Execution -> Verification | Partial; needs terminal-state input contract, not apply-result-only. |
| Verification/Rollback -> Learning | Partial; needs terminal-state handoff as mandatory. |
| Learning -> OMP | Minimal enough after OMP Execution Closure/Verified Consumption. |
| OMP/Production Maturity -> CPS | Minimal enough. |

## L3 Replay As Plane Contract Failure

L3 incident chain:

```text
Observation Plane
  -> Service Matrix proves channel service failure
  -> Planning Plane selects failover candidate
  -> Runtime/Execution Plane asks for CONFIRMED_L3_WAKE
  -> Wake truth not present as handoff payload
  -> STOP_SAFE
```

Missing information between planes:

1. Observation -> Planning:
   - raw service failure exists;
   - planning can use it;
   - evidence/provenance must be preserved in selected move.
2. Planning -> Runtime:
   - selected move must carry action class, user, source, target, reason, failed required services, evidence owner, freshness/generation, and selected move hash.
   - current contract does not universally require all fields.
3. Runtime -> Incident:
   - Runtime cannot open/advance L3 incident without confirmed failure context.
4. Runtime -> Authority:
   - authority can exist, but cannot safely execute without the failure evidence handoff.

This is a plane contract issue, not an L3-only bug.

## Generalization

The same incomplete handoff class would affect future capabilities:

| Capability | Would be affected? | Why |
| --- | --- | --- |
| L4 Degraded Channel Autonomy | YES | Runtime would need degradation severity/provenance from Planning/Observation without recomputing metrics. |
| L5 Recovery Autonomy | YES | Runtime would need recovery-admission evidence, stable window, and source/target provenance. |
| L6 Bounded Rebalance | YES | Runtime would need optimization intent, state-change cost, blast/capacity evidence, and anti-flap rationale. |
| L7 Full Routing Autonomy | YES | All certified classes require complete plane payloads to avoid duplicated runtime truth. |
| Future capabilities | YES | Any action class can fail if producer facts are not carried to consumer plane. |

## Root Cause

One statement:

```text
V7 has named planes and verified-consumption laws, but the universal cross-plane handoff payload contract is incomplete.
```

## Universal Plane Handoff Contract

Every adjacent plane handoff must define and transmit, or explicitly mark not applicable:

| Field family | Required content |
| --- | --- |
| Producer identity | Plane, owner, generation, output id, timestamp. |
| Consumer identity | Plane, owner, expected consumption method. |
| Semantic object | Action class, capability, subject, source, target, reason, desired/current delta. |
| Evidence bundle | Evidence facts, evidence owners, freshness, confidence/quality where relevant, source hashes/generation. |
| Decision identity | Decision id, selected move hash, candidate id, packet/lease id where relevant. |
| Authority binding | Authority object, authority generation, allowed action, blast/risk scope, expiry/revocation state. |
| Safety readiness | Freshness, rollback, verification, restore barrier, anti-flap, movement protection, budget, circuit breaker. |
| Terminal contract | Expected next output, legal terminal consumer, STOP_SAFE reason if blocked. |
| Consumption proof | Consumer read/accepted/used output, behavior changed, next output produced. |
| Non-duplication proof | Consumer did not recompute or replace producer-owned truth except for live safety revalidation. |

Rule:

```text
A plane consumer may revalidate live safety facts,
but it must not reconstruct producer-owned truth as a competing truth source.
```

## Minimal Canonical Extension

Add the universal Plane Handoff Contract to the existing canonical owner:

- primary owner: `docs/reference/V7_RUNTIME_MODEL.md`
- integration owner: `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- mapping owner: `docs/reference/SYSTEM_MAP.md`

No new plane, owner, roadmap, runtime, planner, or architecture is required.

The extension should strengthen existing Work Placement Law and OMP Behavior Enforcement rather than create a new lifecycle.

## Verdict

`PLANE_CONTRACT_INCOMPLETE`
