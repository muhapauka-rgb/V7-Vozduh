# Engineering Report: User Entity / Subject Binding Audit

## Summary

Проведен semantic audit роли concrete user identity в V7 без реализации, редизайна, runtime apply, user movement, authority expansion, новых owners или новых backlog items.

Вывод:

```text
Concrete user identity is not the durable authority object.
Concrete user identity is the runtime subject and selected-move component.
In current GOVERNED_ONLY fallback, exact user identity is intentionally bound into exact packet approval.
In target class/policy authority, approval must bind to action class, policy envelope, blast-radius unit, cohort/group/org constraints, and business objective constraints.
Need New Owner: FALSE.
Need New Backlog Item: FALSE.
```

Final verdict:

```text
USER_ENTITY_MODEL_COMPLETE
```

## Action Performed

Прочитаны существующие владельцы и накопленные знания:

- Product Specification;
- Business Objectives;
- OMP;
- Full Implementation Backlog;
- Current Program State;
- Runtime Model;
- Decision Model;
- Canonical Reference;
- SYSTEM_MAP;
- Policy 004 Authority;
- Policy 005 Action-Class Promotion;
- Policy 006 Blast Radius;
- Policy 007 Rollback;
- Policy 009 Anti-Flap;
- ADR-V7-DELEGATED-AUTONOMY-POLICY;
- ADR-V7-ACTION-CLASS-AUTHORITY;
- ADR-V7-SAFETY-BOUNDED-AUTHORITY;
- Movement Protection Model;
- World Equivalence Model;
- user / cohort / group / org routing policy references in backlog and policies;
- latest Packet Approval Exit Audit;
- Master Decision Model audit.

Код не менялся. Runtime не менялся. Backlog не менялся. Канонические владельцы не менялись.

## User Entity Classification

| Layer | Is concrete user identity part of it? | Classification |
| --- | --- | --- |
| Product object | `NO` as exact id; `YES` as user experience / user connectivity class. | Product cares that users stay online, not that operator approves `10.7.0.5` forever. |
| Business Objective | `NO` as exact id. | Business objectives express stability, recovery, disruption, availability, risk, SLA, and operator workload. |
| Policy object | `PARTIAL` through subject eligibility, cohorts, groups, orgs, service requirements, blast radius. | Policy should bind classes/scopes, not one short-lived user packet. |
| Authority object | `CURRENT YES for GOVERNED_ONLY exact packet`; `TARGET NO as durable authority`. | Exact user identity is a temporary proof boundary only. |
| Runtime subject | `YES`. | Runtime must know the exact subject before execute/stop. |
| Transient selected move component | `YES`. | Selected move includes concrete user/source/target. |
| Learning/evidence dimension | `YES`. | Outcomes must record real user/service impact, but identity may later generalize by equivalent risk segment. |

## Current vs Target Binding

### Current

Current A4 governed production flow is still:

```text
GOVERNED_ONLY
  -> exact packet approval
  -> concrete user is part of packet identity
  -> user change invalidates approval
```

This is correct for the current fallback because authority is intentionally bounded to one exact production action:

- exact user;
- exact source;
- exact target;
- exact selected move hash;
- exact rollback/no-rollback basis;
- exact verification/outcome/learning path.

### Target

Target model:

```text
Business Objectives
  -> Canonical Policies
  -> Action-Class Authority
  -> Delegated Autonomy Policy
  -> Runtime selects current eligible subject
  -> Fresh packet
  -> Execute or Stop
```

In the target model, approval binds to:

- action class;
- delegated policy envelope;
- blast-radius unit;
- cohort/group/org constraints;
- authority tier/generation;
- rollback/no-rollback certification;
- freshness;
- verification;
- anti-flap;
- learning/outcome closure;
- business risk appetite.

Concrete user id is selected at runtime as the current eligible subject inside that envelope.

## Why Current Approval Invalidates When User Changes

Current approval invalidates on user change because exact packet approval is still the fallback authority object.

The packet identity includes the concrete selected move. A changed user means the selected move changed. Under `GOVERNED_ONLY`, the operator did not approve a class or policy envelope; the operator approved exactly one bounded production action.

Therefore user change is a material identity change today.

This is correct for current `GOVERNED_ONLY` safety.

It is not intended to remain true after class/policy authority is certified and approved.

## Representative Evidence Role

User identity is a material evidence dimension when:

- user has unique required services;
- user has unique SLA/business priority;
- user belongs to a special group/org/cohort;
- user is pinned/manual/frozen or subject to explicit policy;
- user has recent movement/rollback/anti-flap history;
- current channel/source state is materially different;
- target eligibility differs for that user;
- verification would prove a different service/user outcome;
- blast-radius or authority scope changes.

User identity can generalize safely when:

- users share the same action class;
- same policy envelope applies;
- same service/SLA/risk profile applies;
- same source/target class and failure/recovery reason applies;
- same rollback/no-rollback model applies;
- same verification model applies;
- same blast-radius unit applies;
- no per-user `PINNED` / `MANUAL` / special policy exists;
- learning evidence shows comparable outcomes across the segment.

## Interaction Model

| Concept | User identity interaction |
| --- | --- |
| Cohort | Groups comparable users so evidence can generalize within a safe segment. |
| Group/org | Defines policy and isolation boundaries. Owned by B11 and related identity/policy owners. |
| Required services | Determines whether a user can use a channel safely. User identity may remain material if services differ. |
| Routing policy | Filters eligible users/targets; target model should use policy constraints rather than exact-user authority. |
| Blast radius | Converts exact user movement into bounded scope: one user, two users, cohort, pool, service, org, group. |
| Movement protection | Uses per-user history, stickiness, cooldown, freeze, pair reversal, target block, and state-change cost. |
| Anti-flap | User history can make a user ineligible even when class/policy is approved. |
| Rollback | Requires per-user rollback/no-rollback readiness for the exact runtime subject. |
| Learning | Stores observed real user/service outcome, then promotes only when representative class/segment evidence exists. |
| Production evidence | User identity is raw evidence dimension; class/cohort abstraction is the promotion model. |

## Full Backlog Trace

| Item | Relevant role in removing packet/user-level approval | Classification |
| --- | --- | --- |
| `A1` | Hard-failure classification gives event/failure basis for subject selection. | runtime eligibility / production autonomy |
| `A2` | Freshness windows prevent stale user/target evidence. | runtime eligibility |
| `A3` | Rollback/no-rollback class evidence for governed candidate movement. | learning reliability / rollback |
| `A4` | Representative real outcome evidence for first action class; begins generalizing beyond one packet/user. | learning reliability / authority promotion |
| `A5` | Class-level blast-radius evidence; converts exact-user proof into bounded scope proof. | blast radius control |
| `A6` | Runtime eligibility arbitration over subject, policy, freshness, authority, rollback, blast radius, anti-flap, verification, learning. | runtime eligibility / policy delegation |
| `B1` | Liveness evidence aggregation affects when subjects need movement. | runtime eligibility |
| `B2` | Hard-failure timer/risk class affects when subject movement is safe. | movement protection / runtime eligibility |
| `B3` | Soft-degradation thresholds affect user movement justification. | movement protection |
| `B4` | Signal-to-policy mapping makes degradation evidence consumable by policy. | policy delegation |
| `B5` | Degradation attribution improves evidence quality for subject movement. | learning reliability |
| `B6` | Circuit-breaker/outlier mapping informs channel/pool action classes. | blast radius control |
| `B7` | Service objectives to policy thresholds maps user service needs into policy. | user abstraction / policy delegation |
| `B8` | Recovery admission certification prevents unsafe movement to recovered channels. | runtime eligibility |
| `B9` | Post-admission observation windows reduce user-level recovery risk. | movement protection |
| `B10` | Slow-start recovery defines staged user/action-class re-entry. | cohort abstraction / blast radius control |
| `B11` | Org/cohort isolation and identity policy integration. | cohort abstraction / group-org policy |
| `B12` | Next action-class stage after certification evidence. | authority promotion |
| `B13` | Metric reliability for automated promotion recommendations. | learning reliability / authority promotion |
| `B14` | Service/pool/cohort blast-radius scope. | cohort abstraction / blast radius control |
| `B15` | Containment/forward-fix classification. | observability / rollback |
| `B16` | Automatic rollback authority after reliable verification. | rollback / authority promotion |
| `B17` | Stale-read reporting while blocking mutation. | observability / runtime eligibility |
| `B18` | Owner-issued version/lease patterns. | runtime eligibility / freshness |
| `B19` | Centralized hysteresis and State Change Cost. | movement protection |
| `B20` | Hard-failure override for anti-flap arbitration. | movement protection / runtime eligibility |
| `B21` | Explicit per-user `AUTO` / `PINNED` / `MANUAL` mode. | user abstraction / movement protection / operator experience |
| `C1` | Fail-open/fail-closed behavior per action class. | runtime eligibility |
| `C2` | Probabilistic suspicion as advisory evidence only. | learning reliability |
| `C3` | Break-glass authority as exceptional audited operator policy. | authority promotion |
| `C4` | Keeps all-at-once promotion unavailable. | blast radius control / authority promotion |
| `C5` | Rollback as operational compensation. | rollback |
| `C6` | Bounded stale allowance by action class. | runtime eligibility |
| `C7` | Pool max-ejection/minimum-health semantics. | blast radius control / movement protection |
| `D1`-`D6` | Optional future substrate/scope revisits only if product scope changes. | optional / no current blocker |

## Capability Responsible For Removing Exact-User Approval

No single item removes exact-user approval alone.

Primary chain:

```text
A4
  -> A5
  -> B13
  -> A6
  -> Action-Class Authority
  -> Delegated Autonomy Policy
```

Full path must also include:

```text
B11
  -> B14
  -> B21
  -> B19 / B20
  -> B16
  -> B12
  -> C3 / C4
```

Reason:

- A4 proves representative class evidence.
- A5 proves bounded blast radius.
- B13 proves promotion metrics are reliable.
- A6 decides runtime execute/stop.
- B11/B14 provide cohort/org/service/pool scope so approval can bind to scope rather than exact user.
- B21 distinguishes users that are automatic, pinned, or manual.
- B19/B20 prevent unstable per-user movement.
- B16 handles rollback authority.
- B12 moves to next action-class stage only after evidence.
- C3/C4 prevent exceptional or all-at-once authority misuse.

## Existing Owner Mapping

| Concern | Existing owner |
| --- | --- |
| Product/user meaning | Product Specification, Business Objectives |
| Authority semantics | OMP, Policy 004, ADR Action-Class Authority, ADR Delegated Autonomy Policy |
| Action-class promotion | OMP, Policy 005 |
| Runtime subject and packet semantics | Runtime Model, Execution Packet owner |
| Decision subject vocabulary | Decision Model, Decision Object Model in Canonical Reference |
| Blast-radius subject/scope | Policy 006, A5, B11, B14, C7 |
| Per-user routing control | B21, user registry, group/organization policy, planner gates, admin UI |
| Movement protection | MOVEMENT_PROTECTION_MODEL, `tools/v7-users-autoswitch`, B19, B20 |
| Anti-flap | Policy 009, anti-flap read model, B19, B20 |
| Rollback/no-rollback | Policy 007, A3, B16 |
| Learning/evidence | Feedback/learning owners, A4, B13 |
| Current volatile packet/user approval | Current Program State |
| Durable truth | Canonical Reference, SYSTEM_MAP |

Need New Owner:

```text
FALSE
```

Need New Backlog Item:

```text
FALSE
```

## Architecture Consistency

Architecture already supports:

```text
Authority object != execution object != runtime subject
```

Concrete user identity is:

- not the permanent product authority object;
- not the permanent policy approval object;
- not the permanent class approval object;
- required as runtime subject;
- required as selected-move identity before mutation;
- required as learning/evidence dimension after observed outcome.

No architecture extension is required.

## Impact

Runtime behavior changed: `NO`.

Authority expanded: `NO`.

Users moved: `NO`.

Backlog changed: `NO`.

Canonical owners changed: `NO`.

## Capability Progress

No maturity increase. This was an audit only.

Current known progress remains:

- Engineering Maturity: `100.0%`.
- Tier A: `3 / 6` complete, `50.0%`.
- Overall actionable backlog: `3 / 34` complete, `8.8%`.
- Authority Evolution: `40.0%`.
- Runtime Eligibility: `28.6%`.
- Production Readiness: `24.0%`.
- Production Autonomy: `0.0%`.

## Next Step

Minimal safe next step:

```text
Continue A4 through existing owners.
Do not remove exact-user approval now.
Do not enable runtime automation.
Do not lower thresholds.
Do not synthesize evidence.
If a fresh governed production action is required, stop at OPERATIONAL_AUTHORITY.
```

The stale user/packet loop is broken only after class/policy authority can approve an envelope and Runtime can select the current eligible subject inside it.

## Re-audit Rule

Do not re-audit user entity / subject binding unless:

- Product Specification changes user/authority semantics;
- Runtime Model changes subject/packet validation;
- OMP changes Action-Class Authority or Delegated Autonomy progression;
- B11/B14/B21 materially redefine cohort/user policy;
- production evidence proves user identity generalization unsafe;
- operator explicitly requests re-audit.

