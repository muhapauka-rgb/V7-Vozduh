# V7 Service Failure Automation Evolution Program

Version: `1.3`

Status: `PROPOSED_EXECUTION_PLAN`

Activation state owner: `CPS`

This file defines capability stages and completion contracts. It must not be
used to infer live execution, wait, stop, Authority or Production Maturity.

## Program identity

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Target

Close the existing production loop:

```text
Service Failure
-> durable incident
-> OMP consumption
-> incident-bound safe decision
-> ACTION / STAY / STOP_SAFE
-> mandatory STOP_SAFE responsibility classification
-> existing BDP/OMP repair or exact Authority boundary
-> bounded shadow decision
-> controlled action only when independently authorized
-> verification and rollback/no-rollback
-> real Outcome Passport
-> replay and Learning
-> affected capability reconciliation
-> next incident or exact legal terminal
```

The target is not a new Automation Gap Engine, Decision Engine, Shadow system,
Planner, Runtime, queue, registry or Authority owner. The target is to connect
the already implemented owners so that a production `STOP_SAFE` cannot end as
only a recorded event, dashboard warning or email.

## Discovery result

The pre-implementation audit proved that most requested capabilities already
exist:

| Capability | Existing owner | Current result |
| --- | --- | --- |
| failure persistence, episode identity, recovery/expiry | service Matrix lifecycle | `IMPLEMENTED_PRODUCTION_CALLED` |
| passive Situation/Decision/Outcome/replay/Learning capture | `tools/v7-users-autoswitch --consume-passive-events-only` | `IMPLEMENTED_PRODUCTION_CALLED` |
| multi-lane engineering action classes | OMP/Permanent Polygon | `5/5 COMPLETE_CONSUMED` |
| capacity, suitability, policy, confidence, rollback and safety gates | `tools/v7-users-autoswitch` | `IMPLEMENTED_TESTED` |
| bounded emergency failover | `emergency_failover_autonomy` in `tools/v7-users-autoswitch` | `IMPLEMENTED_CERTIFIED_INACTIVE` |
| shadow MOVE/KEEP model and durable decision history | `admin_core/shadow_autonomy.py` and existing JSONL owner | `IMPLEMENTED_UNDERFED_MANUAL_CALLER_ONLY` |
| outcome, feedback, replay, Learning and calibration | existing execution/feedback/trust owners | `IMPLEMENTED` |
| STOP/Intent Gap classification and BDP routing law | OMP Automation Gap Closure Cycle | `CONTRACT_COMPLETE_RUNTIME_BINDING_MISSING` |
| Authority recommendation and action-class evolution | existing delegated-policy and L7/L8 owners | `IMPLEMENTED_HOLD_GOVERNED_ONLY` |

The exact current broken link is:

```text
service Matrix timer
-> passive event consumer
-> transient Incident/STOP_SAFE product frontier in latest summary
-> NO PROVEN DURABLE OMP CONSUMER
```

An idempotent later Matrix run overwrites the summary with
`NO_NEW_MATERIAL_INCIDENT_OR_ALREADY_CONSUMED`, so a material frontier is not a
durable unconsumed obligation. Production passive records remain durable, but
their next OMP responsibility is not consumed. This applies equally to a
failure that should lead to safe action and a `STOP_SAFE` / correct-`STAY`
terminal that must explain why no action was legal.

## Existing-owner law

1. Discover -> Reuse -> Extend -> Implement.
2. No new service-failure automation architecture may be created.
3. Incident obligations must be derived from or appended through existing
   event, decision, outcome, closure, CPS or certification owners.
4. `service-matrix-refresh-summary.json` is a latest-run projection, not a
   durable work queue or truth source.
5. Shadow history remains the existing shadow owner. Real outcome history
   remains the existing outcome/feedback owner. Neither may replace the other.
6. OMP Automation Gap Closure remains the only STOP/Intent Gap law.
7. The existing autoswitch planner remains the only route decision producer.
8. The existing emergency failover path remains the only bounded failover
   execution capability considered by this Program.
9. CPS remains the only volatile program and Authority state owner.
10. `Incident Frontier` and `Product Evolution Frontier` are two projections
    of the existing OMP product-engineering frontier. They are not new owners,
    registries, queues or schedulers.

### Mandatory semantic discovery and connection law

Before every implementation, repair, Mission transition or proposed new
artifact, the executing owner must first prove the current semantic topology:

```text
required outcome
-> existing producer
-> durable artifact / identity
-> existing consumer
-> verification
-> terminal / successor
```

The audit must search by behavior and data-flow, not only by filename or
feature name. It must identify all already implemented or deployed owners,
their input/output identities, freshness and one-use constraints, Authority
boundary, caller, consumer, verification and terminal semantics.

The mandatory order is:

1. discover the existing implementation and its live/deployed state;
2. trace every relevant producer -> consumer link and prove the exact broken,
   absent, stale, duplicate or unreachable link;
3. reuse the existing owner when it already provides the required capability;
4. connect or minimally extend the existing owner when capability exists but
   its handoff, invocation, identity binding or consumption is incomplete;
5. implement new code only for the smallest proven residual that no existing
   owner can supply;
6. verify that the resulting output is consumed by a real downstream owner and
   changes an exact successor, legal terminal or product capability projection.

No Mission may create a parallel owner, queue, registry, watcher, Planner,
Runtime, Authority path, Packet path or evidence store merely because an
existing capability was not discovered or connected correctly. A report,
test, deploy or JSON artifact alone is not completion: the intended output
must reach and be consumed by its declared next owner.

## Evidence and authority law

1. Passive capture, synthetic Polygon results and shadow decisions are
   Engineering Evidence only.
2. `EXTERNAL_UNATTRIBUTED`, `OPERATOR_INDUCED`, controlled and natural
   provenance remain separate.
3. A shadow projection such as “N affected users could move” is impact
   analysis, not executable scope.
4. Any actionable recommendation must be bounded by the current delegated
   action-class policy; current default scope is at most one user and one
   transaction.
5. A legacy runtime policy projection cannot override current CPS/OMP
   `GOVERNED_ONLY`.
6. Runtime apply, routing mutation, user movement, Packet execution,
   restore-barrier write and rollback apply are forbidden unless an exact
   current owner-issued one-use contract independently authorizes them.
7. This Program may recommend `HOLD`, `FREEZE`, `DEMOTE`,
   `RECOMMEND_NARROW_SCOPE` or `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`. It
   cannot grant Authority.
8. Production Maturity is unchanged unless its independent canonical owner
   consumes qualifying real evidence.

## Progressive blast-radius expansion contract

The current one-user limit is a certified safety boundary, not a permanent
technical limit. This Program must mature the existing failover action class
through the following evidence-gated ladder:

```text
1 user
-> 2 users
-> 5 users
-> 10 users
-> bounded cohort
-> bounded incident scope
```

The ladder defines maximum authorized scope, not a requirement to move that
many users. Every decision must still select the smallest necessary cohort.

Promotion to the next tier requires:

- real owner-backed outcomes at the current tier;
- correct target selection and sufficient target capacity;
- successful immediate and temporal verification;
- representative rollback and no-rollback behavior;
- acceptable false-positive, false-negative, STOP_SAFE and missed-opportunity
  rates;
- anti-flap, cooldown, retry-budget and correlated-failure protection;
- Shadow comparison against actual outcomes;
- no unresolved source/target/protocol/provider concentration risk;
- an immutable evidence set and independent Authority recommendation;
- CPS consumption of the exact approved tier.

Any failed verification, rollback failure, drift, capacity loss, correlated
incident or confidence regression must hold, narrow, freeze or demote the
current tier. A numeric limit must never be increased directly in policy.

The legacy production projection `XLARGE_BATCH/50` is historical evidence, not
current Service Failure Authority. It must be reconciled with current
`GOVERNED_ONLY` before any tier above one can become executable.

### Current action-class contract binding

The existing `/etc/v7/policy.json` authority owner must carry a fresh,
explicitly scoped `current_action_class_contract` for every runtime Authority
above `CANARY`. This is a policy field and gate inside the existing
`tools/v7-users-autoswitch` owner; it is not a second Authority, registry,
queue or CPS replacement.

The contract must contain:

- schema `v7.current-action-class-contract.v2` (the former v1 is legacy
  compatibility only and can never be emitted by this Program);
- `contract_id`, `contract_hash`, `issuing_owner`, `active_program` and legal
  action class;
- exact `subject.user_ip`, source/target scope, `max_users=1` and
  `max_concurrent_transactions=1`;
- `incident_generation` and the fresh `source_generation` identity
  (`planner_generation_id`, source/snapshot bundle hashes and selected-move
  hash), plus the exact pre-decision policy generation hash and Authority
  ceiling;
- `issued_at`, short unexpired `expires_at`, verification contract,
  rollback/containment contract, cooldown and anti-flap contract;
- immutable `authority_decision` provenance: the exact request id/hash,
  `APPROVE_ONCE_AS_SCOPED`, decision timestamp, decision id and accountable
  actor provenance;
- a one-use consumption state (`ISSUED -> CONSUMED/EXPIRED`) with exactly one
  allowed use and no retry under the same decision.

`admin_core/operator_execution.py` is the existing Authority decision owner
for this issuance. Its explicit issue surface verifies the fresh request,
expected request id/hash and `APPROVE_ONCE_AS_SCOPED`, then alone writes the
policy field. Neither a hand-edited JSON object nor the read-only autoswitch
request template is an Authority decision or an executable contract. The
autoswitch owner only consumes and independently revalidates a v2 contract.
The request itself expires after five minutes; it is not a standing approval
and an expired reconciliation must be produced again from fresh snapshots.
Immediately before its sole forward mutation, it calls back into the same
existing Authority owner to atomically transition `ISSUED -> CONSUMED`, binding
the exact user, source/target and source generation. A failed or interrupted
later apply remains consumed and therefore requires a new reconciliation and
new Authority decision; no retry can silently reuse the previous contract.

The owner holds an interprocess policy-file lock across read, validation and
atomic replace, so competing consumers cannot both observe `ISSUED`. The
already-owned append-only `/opt/v7/audit/operator-execution-audit.jsonl`
records exactly one `APPROVE_ONCE_AS_SCOPED` or `DECLINE` decision with actor
provenance, and records the one-use consumption. The lock is only a transient
coordination primitive; it is not an additional durable owner. Issuance fails
closed if the current policy generation no longer equals the request binding,
the incident identity/generation is incomplete, Authority exceeds its actual
ceiling, required stop conditions are missing, or verification/rollback
contracts do not name their required owner and verifier-triggered behavior.

The autoswitch gate must cap selection by that scope. A missing, malformed,
expired, lower-than-certified or zero-budget contract is
`STOP_SAFE/FROZEN/0` before restore-barrier snapshot or apply. Historical
promotion evidence, including `XLARGE_BATCH/50`, can never substitute for this
contract. Issuing or refreshing a contract remains the exact existing
owner-issued Authority action; this Program cannot issue one itself.

M5a ordering is strict: the absence of an exact fresh Packet or packet-bound
restore barrier must block only the later M5c Operational Authority path. It
must never block a fresh M5a Action Class request when Situation, Decision,
scope, L3 evidence and all contract-specific preconditions are fresh. A valid
contract then causes M5b fresh planner revalidation; it does not create a
Candidate, Packet or lease and it is not consumed by their preparation. Its
single atomic consumption remains immediately before the sole forward Runtime
mutation. Only a later exact fresh Packet may form an
`OPERATIONAL_AUTHORITY_RESTORE_BARRIER_READY` package through the existing
operator-execution owner.

### Authority-boundary re-entry loop

An `ENGINEERING_AUTHORITY` terminal must not become a manual dead end. The
existing `tools/v7-users-autoswitch --action-class-contract-reconciliation-only`
producer emits a read-only, deterministic request template from the current
Shadow/action-boundary projection. It never writes policy or creates
Authority. Its closed loop is:

`STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`
`->` read-only request template
`->` existing coherent observe lifecycle holds the shared service-matrix lock,
invokes `v7-intelligence-snapshot-refresh`, and re-runs the planner on the
same source bundle (a standalone refresh followed by an unlocked read is not
sufficient while the Telegram sentinel is a live writer)
`->` existing `/etc/v7/policy.json` authority owner independently issues or
declines a short one-use scoped contract only after the request preflight is
fresh and ready, through the existing `admin_core/operator_execution.py`
Authority decision surface and an exact `APPROVE_ONCE_AS_SCOPED` request/hash
binding
`->` existing event-driven Service Matrix/autoswitch invocation re-reads and
validates that contract
`->` existing action-class boundary returns either another exact `STOP_SAFE`,
`NO_ACTION`, or `PACKET_MATERIALIZATION_ELIGIBLE`
`->` existing Service Failure obligation/OMP consumer.

The request template is intentionally non-durable and cannot substitute for
fresh Situation, Decision Trace, selected-move/snapshot identities, policy
owner confirmation, Candidate, Packet, lease, verification or rollback. A
policy update alone grants no Runtime apply; the same existing consumer must
revalidate every gate against fresh owner-backed inputs.

## Dynamic Mission compression

`M0` is mandatory and is complete through the associated fresh audit.

After every Mission, OMP must recompute exact residuals:

- skip fully consumed criteria as `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`;
- reduce partially consumed Missions to their exact missing producer-consumer
  links;
- merge Missions only when owner, evidence class, isolation, verification and
  terminal semantics remain explicit;
- do not continue ceremonially after a legal program terminal;
- a lane-local Authority or real-world wait cannot block independent safe
  engineering work.

## Automatic successor continuation contract

Every non-terminal result in this Program must close through the existing
owner chain:

```text
verified result
-> existing OMP consumer
-> atomic CPS projection
-> residual recomputation
-> durable exact successor
-> existing event-driven Continue OMP re-entry
```

Transaction terminals, focused repair completion, tests, safe deploy,
production caller verification, replay, Learning, Outcome consumption and an
M6/M7 recommendation are not operator-return points while a safe successor
exists. The existing event-driven Codex Automation Platform owner must receive
one deterministic wake after the atomic successor projection; the watchdog is
fallback only. Consumption and successor publication are interprocess
exact-once through the existing closure owner.

The wake is suppressed only for an exact independent `ENGINEERING_AUTHORITY`
or `OPERATIONAL_AUTHORITY` decision, a fully reconciled `REAL_WORLD_LIMIT`, an
external owner/access input, or an irreducible safety boundary. These terminals
must preserve the exact re-entry condition. They may not be converted into an
approval or bypassed by this Program.

### Auto-safe continuation execution policy

`CODEX_AUTOMATION_PLATFORM` is the existing watchdog fallback owner for this
Program. It must re-enter the active OMP task on the configured heartbeat when
the task is idle or interrupted; an ended response, connection loss, context
compaction or a completed intermediate tool call is never a Program terminal.

On each wake it must read fresh CPS and use the existing OMP re-entry owner.
When CPS exposes a safe executable successor, it must continue without an
operator message through the complete existing-owner chain: discovery,
smallest repair, focused verification, commit/push, passing safe-deploy
manifest, authorised safe deploy, production caller/consumer verification,
affected replay/Learning, truth/convergence, atomic CPS/OMP/report projection,
residual recomputation and successor dispatch.

The continuation is strictly bounded:

- it must re-read CPS before every successor and preserve the existing
  exact-once lease, duplicate suppression and source-generation checks;
- it must not retry an unchanged failed successor indefinitely; after three
  wakes without owner-backed progress it records the exact
  producer-to-consumer blocker and stops without churn;
- it must not create a new watcher, queue, registry, Planner, Runtime or
  Authority system;
- it must not treat this policy as consent for `ENGINEERING_AUTHORITY`,
  `OPERATIONAL_AUTHORITY`, restore-barrier write, Packet execution, routing
  mutation, user movement, rollback apply, Authority expansion, Production
  Maturity change, external owner/access input or Natural L8 evidence.

At any such independent boundary the heartbeat may perform read-only discovery
and prepare the exact existing-owner request, but must preserve the re-entry
condition and stop. A new safe successor or a separately owner-issued scoped
contract is required before it continues.

After each owner-backed controlled outcome, replay and Learning, the existing
M6/M7 owners recompute the progressive blast-radius ladder. `HOLD`, `FREEZE`,
`DEMOTE` and insufficient-evidence decisions remain exact legal outputs. An
independently approved next tier produces a durable successor for the same
existing execution lifecycle. At most one tier may advance per independently
certified generation: `1 -> 2 -> 5 -> 10 -> bounded cohort`. No policy number
may be raised directly and no historical evidence may substitute for the
current owner decision.

## Parallel frontier and arbitration law

V7 has two simultaneous, existing-owner work projections:

| Projection | Input | Legal outputs |
| --- | --- | --- |
| `INCIDENT_FRONTIER` | real production Situation, incident, ACTION/STAY/STOP_SAFE, recovery or expiry | safe repair, correct-STAY/STOP terminal, exact data/caller/code/Authority/external-owner gap |
| `PRODUCT_EVOLUTION_FRONTIER` | capability residual, Polygon result, replay/coverage gap, valid incident-derived engineering gap | existing BDP -> Candidate -> OMP Mission -> affected verification -> next residual |

Arbitration rules:

1. A material current production incident has safety priority.
2. A correct `STAY` or `STOP_SAFE` closes that incident action only; it does
   not suppress independent Product Evolution work.
3. Product Evolution work cannot relabel, erase or bypass an open production
   incident.
4. Every consumed output recomputes both projections.
5. A `STOP_SAFE` creates a deterministic classification obligation, but BDP
   admission occurs only for a proven automatable engineering gap.
6. Both projections are derived and consumed through existing OMP/CPS owners;
   neither is a durable second backlog.

## Mission map

### M0 — Existing capability and production binding reconciliation

Status in this plan: `DISCOVERY_COMPLETE_AWAITING_CPS_ADMISSION`.

Required result:

- prove current CPS/OMP, repository and production caller state;
- inventory capability owners by semantics, not filenames;
- distinguish implemented, tested, deployed, production-called, consumed and
  Authority-active states;
- identify the last responsible producer-consumer link.

Completion contract:

`EXISTING_AUTOMATION_INVENTORIED_AND_EXACT_RESIDUAL_PROVEN`

### M1 — Durable Situation / Incident / STOP_SAFE obligation and real OMP consumer

Extend the existing passive records so every material Situation, incident,
ACTION, `STAY`, `STOP_SAFE`, recovery or expiry exposes one deterministic
obligation identity through an existing durable owner. Do not create an
opportunity store, queue or registry.

The existing OMP continuation consumer must:

1. discover the unconsumed durable Situation/Incident/STOP_SAFE obligation;
2. verify source identity, provenance, freshness and generation;
3. consume it exactly once across processes;
4. preserve recovery/expiry links;
5. classify every `STOP_SAFE` before selecting a successor;
6. emit the exact Incident and Product Evolution projection outputs;
7. preserve an unconsumed obligation when a later Matrix run has no new event.

The mandatory first classification is:

```text
STOP_SAFE
-> CORRECT_SAFE_TERMINAL
or DATA_OR_EVIDENCE_GAP
or EXISTING_CAPABILITY_NOT_CALLED
or ENGINEERING_IMPLEMENTATION_GAP
or AUTHORITY_REQUIRED
or EXTERNAL_OWNER_REQUIRED
```

`CORRECT_SAFE_TERMINAL` is a successful safety outcome, not a BDP Candidate.
Only a proven automatable engineering gap enters the existing BDP -> Candidate
-> OMP path.

The durable obligation must also preserve affected-user count, current
certified blast-radius tier, requested tier, target-capacity snapshot and the
exact evidence cell blocking the next tier. These are projections through
existing owners, not a new Authority registry.

Required production proof:

```text
real Matrix timer
-> passive consumer
-> durable obligation
-> independent OMP caller
-> consumer behavior change
-> successor or legal terminal
```

Completion contract:

`PRODUCTION_SITUATION_STOP_SAFE_OBLIGATION_DURABLE_AND_OMP_CONSUMED`

### M2 — Incident-bound Decision Matrix and early Automation Gap adapter

Do not build another Decision Matrix. Bind the durable incident to the existing
autoswitch planner and its current gates in read-only mode.

For the exact source and affected scope, calculate:

- source hard/partial failure classification;
- healthy target availability;
- target service suitability and capacity;
- policy eligibility;
- evidence freshness;
- confidence;
- anti-flap and cooldown;
- verification and rollback feasibility;
- current action-class Authority;
- bounded executable scope and separate aggregate impact scope.

For every incident, the adapter must calculate:

- the smallest necessary cohort;
- the maximum capacity-safe cohort;
- the current Authority-safe cohort;
- the effective cohort as the minimum of those bounds;
- why the next ladder tier is allowed or blocked.

The legal decision taxonomy is:

- `MOVE_READY_WITHIN_EXISTING_AUTHORITY`;
- `STAY_CORRECT_CURRENT_ROUTE`;
- `STOP_SAFE_NO_SAFE_TARGET`;
- `STOP_SAFE_DATA_OR_EVIDENCE_GAP`;
- `STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED`;
- `STOP_SAFE_ENGINEERING_IMPLEMENTATION_GAP`;
- `STOP_SAFE_AUTHORITY_REQUIRED`;
- `STOP_SAFE_EXTERNAL_OWNER_REQUIRED`.

Every STOP must include:

- `last_responsible_link`;
- owner;
- exact missing artifact;
- existing consumer;
- reentry condition;
- whether Polygon can close the engineering part;
- forbidden effects.

Before any MOVE-capable output, reconcile the current CPS delegated policy with
the older production runtime authority projection. A broader legacy batch
budget must fail closed and cannot become current action-class Authority.

M2 consumes the early classification emitted by M1. It must not postpone
Automation Gap Closure until a later implementation Mission. M4 only routes,
repairs and revalidates a gap that M1/M2 already proved.

Completion contract:

`INCIDENT_BOUND_SAFE_DECISION_AND_RESPONSIBILITY_CLASSIFICATION_CONSUMED`

### M3 — Automatic bounded Shadow production and outcome reconciliation

Reuse `admin_core/shadow_autonomy.py` and its current durable owner. Remove
dependence on an operator opening an admin endpoint as the only producer.

The event-driven OMP incident consumer must produce:

- one deduplicated bounded shadow recommendation for the exact current
  delegated scope;
- a separate aggregate affected-user impact projection;
- MOVE/STAY/STOP_SAFE reason and gate snapshot;
- source, target, Situation, Decision Trace and incident identities;
- zero apply, zero movement and zero Authority effect.

Shadow must evaluate the ladder without granting it: current-tier behavior,
counterfactual `2/5/10/bounded cohort` behavior, capacity pressure, rollback
exposure and correlated-failure risk. Only the current certified tier may be
presented as potentially executable; all higher tiers remain counterfactual.

The existing outcome/feedback owner must automatically compare a later
owner-backed outcome with the matching shadow decision. Observed outcomes are
primary evidence. Human comparison remains secondary supervised evidence and
must not be fabricated to fill a threshold.

Completion requires more than model invocation:

- a real non-test incident produces a durable shadow record;
- duplicate invocations append zero duplicates;
- a matching controlled or natural outcome, when present, reaches the existing
  comparison/Learning consumer;
- the next capability state changes or the exact evidence gap is emitted.

Completion contract:

`EVENT_DRIVEN_SHADOW_DECISION_AND_REAL_OUTCOME_RECONCILIATION_PRODUCTION_CONSUMED`

### M4 — Existing Automation Gap Closure routing, repair and revalidation

Consume the M1/M2 classification through the missing real caller/consumer for
the OMP V4.7-V4.10 contract. Do not repeat classification or create a second
gap engine.

Routing by classification:

| Classification | Existing route |
| --- | --- |
| correct STOP/no safe target | close as legal safety terminal and monitor the same incident generation |
| missing/stale data | responsible producer repair -> tests -> deploy -> affected replay |
| existing capability not called | repair the producer-consumer binding |
| engineering implementation gap | existing BDP -> Candidate -> OMP Mission |
| Authority required | exact action-class recommendation/request; no implicit grant |
| external owner required | owner-bound terminal with exact reentry event |

If the current tier succeeds but the next tier is blocked, Automation Gap
Closure must classify the exact reason as evidence, capacity, implementation,
consumer binding, Authority or external-owner gap. It must not reduce every
promotion blocker to generic `AUTHORITY_REQUIRED`.

A repair closes only when the original incident is replayed and the original
STOP/Intent Gap changes to its expected state. Tests or reports alone do not
close it.

Completion contract:

`STOP_SAFE_AUTOMATION_GAP_ROUTED_AND_ORIGINAL_INTENT_REVALIDATED`

### M5 — Conditional bounded controlled automation

Do not rebuild emergency failover. Reuse the existing
`emergency_failover_autonomy` gates and one-use operation-scoped contract.

M5 has three non-interchangeable sub-stages. They are not a new Program,
Authority, Planner, queue, registry or execution path.

#### M5a — Action-class contract reconciliation

The existing policy, CPS and OMP owners must state the legal action class for
the exact failure family before any Packet-capable output. A contract above
`CANARY` must bind source and target egress, maximum users, freshness,
verification, rollback, cooldown, anti-flap, expiry and concrete stop
conditions. A missing or stale contract is `STOP_SAFE/FROZEN/0`; historical
promotion evidence is never a substitute.

#### M5b — Shadow versus allowed-action boundary

Every Shadow recommendation must be compared with the action class actually
allowed now. The read-only output is exactly one of:

- `NO_ACTION_NO_SHADOW_CANDIDATE`;
- `STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`;
- `STOP_SAFE_OTHER_EXECUTION_GATE_REQUIRED`;
- `PACKET_MATERIALIZATION_ELIGIBLE`.

`PACKET_MATERIALIZATION_ELIGIBLE` is not `MOVE_READY` and grants no execution
permission. It means only that a fresh Candidate, Packet, lease, verification
and rollback gate may be prepared by their existing owners.

#### M5c — Execution-boundary preparation

Candidate, Packet and lease preparation may occur only after M5a/M5b, using
fresh Situation and Decision Trace identities. Runtime apply remains a
separate one-use operational contract. `ENGINEERING_AUTHORITY` may prepare or
validate the boundary but cannot silently become `OPERATIONAL_AUTHORITY`.

This Mission runs only when M1-M4 prove:

- a genuine production need;
- a safe target;
- fresh service evidence;
- current action-class Authority;
- exact one-user/one-transaction budget;
- fresh Candidate, Packet, lease and snapshots;
- verification and rollback readiness;
- accepted event-driven wake;
- no legacy-policy/CPS conflict.

Controlled progression is one tier per independently certified evidence
generation. A Mission may skip a nominal tier only when existing owner-backed
evidence already proves every completion criterion for that tier; the skip
must be recorded as `TIER_NOT_REQUIRED_ALREADY_CERTIFIED`.

Every controlled tier run must preserve:

- one operation-scoped cohort identity;
- per-user and cohort-level verification;
- target capacity before, during and after execution;
- partial-apply handling;
- cohort rollback semantics;
- circuit breaker and immediate demotion path;
- exact evidence separation from ordinary production and Natural L8.

The inactive periodic autoswitch timer must not be enabled merely to satisfy
automation. The existing event-driven incident/OMP path should invoke one
bounded run. Timer/cron/blind polling remain rejected wake sources unless a
separate Authority program changes that contract.

If Authority is absent, the legal terminal is an exact
`ENGINEERING_AUTHORITY`, not a fake execution and not a global engineering
stop.

The Authority terminal itself has the explicit re-entry loop above. It closes
only when the existing policy owner either declines/lets the request expire
(which returns a fresh `STOP_SAFE`) or issues a valid short one-use contract
that the existing autoswitch boundary consumes and revalidates. No new
Authority owner, registry, queue, watcher or timer is introduced.

Completion contract:

`BOUNDED_SERVICE_FAILURE_ACTION_REAL_OUTCOME_CONSUMED`

or, when legitimately blocked:

`BOUNDED_SERVICE_FAILURE_ACTION_EXACT_AUTHORITY_BOUNDARY_PROVEN`

### M6 — Learning, capability maturation and Authority recommendation

Reuse Outcome Passport, temporal verification, deterministic replay, Learning,
calibration and action-class Authority owners.

After every new incident outcome:

1. reconcile the affected CAP-U criteria only;
2. preserve provenance and action-class separation;
3. compare shadow recommendation with actual outcome;
4. recalculate false-positive, false-negative, correct-STAY, STOP_SAFE,
   rollback/no-rollback and missed-opportunity coverage;
5. recompute confidence and risk by action class;
6. emit exactly one of:
   - `HOLD_GOVERNED_ONLY`;
   - `FREEZE`;
   - `DEMOTE`;
   - `RECOMMEND_NARROW_SCOPE`;
   - `INSUFFICIENT_EVIDENCE`;
   - `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`.

The recommendation must include an exact blast-radius result:

- `HOLD_CURRENT_TIER`;
- `DEMOTE_TO_<N>`;
- `RECOMMEND_TIER_<N>`;
- `RECOMMEND_BOUNDED_COHORT`;
- `RECOMMEND_BOUNDED_INCIDENT_SCOPE`;
- `INSUFFICIENT_TIER_EVIDENCE`.

It must bind the maximum users per transaction, maximum concurrent
transactions, source/target families, failure classes, capacity reserve,
cooldown, rollback trigger, circuit breaker, demotion rule and expiry.

Unrelated whole capabilities must not advance.

Completion contract:

`CURRENT_SERVICE_FAILURE_EVIDENCE_CONSUMED_AND_ACTION_CLASS_AUTHORITY_RECOMMENDATION_DECIDED`

### M7 — Separate Authority-owned activation

This Mission is conditional and outside any implicit continuation.

It starts only if M6 emits
`RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`. Activation must use a distinct
existing-owner Program identity, fresh CPS admission and independent Authority
decision. It must define blast radius, event classes, evidence floors,
cooldowns, rollback, circuit breakers, demotion and kill conditions.

Activation may grant only the exact recommended ladder tier. Approval of tier
`N` does not approve a larger cohort, another action class, another
source/target family, parallel execution or full-incident automation.

After activation, the next real qualifying incident must verify the granted
tier in production. Its outcome returns to M6; success may form the next-tier
recommendation, while failure automatically holds, narrows, freezes or demotes
the class through the existing Authority owner.

`HOLD`, `FREEZE`, `DEMOTE`, `RECOMMEND_NARROW_SCOPE` and
`INSUFFICIENT_EVIDENCE` legally skip M7.

Completion contract:

`ACTION_CLASS_AUTHORITY_DECISION_INDEPENDENTLY_CONSUMED`

## Verification campaign

Every implementation Mission must run:

1. focused unit tests for the changed owner;
2. the exact service-failure episode and passive consumer tests;
3. the exact incident-bound planner/shadow replay;
4. duplicate and cross-process idempotency tests;
5. forbidden-effects verification;
6. affected Permanent Polygon scenarios;
7. commit and push;
8. `tools/v7-safe-deploy` only for the exact approved manifest;
9. a fresh non-test production caller and consumer;
10. affected incident replay;
11. `tools/v7-truth-check --all --json`;
12. `tools/v7-convergence-status --json`;
13. local/GitHub/production commit and runtime snapshot reconciliation.

No Mission may claim `COMPLETE_CONSUMED` from tests, reports, deploy or an
in-process probe alone.

## Forbidden shortcuts

- a second event/opportunity store;
- a second decision or automation-gap engine;
- treating latest-run summary as a queue;
- `continue-on-error`, skipped gates or weakened assertions;
- enabling a timer to manufacture independent automation evidence;
- bulk executable shadow recommendations outside delegated scope;
- directly changing `max_users_per_run`, `max_users_per_channel` or a legacy
  batch budget without current-tier evidence and independent Authority;
- promoting more than one unproven blast-radius tier at once;
- reusing Candidate, Packet, lease, nonce or Authority;
- directly invoking rollback to manufacture a terminal;
- moving ordinary customers solely to create certification evidence;
- relabeling synthetic, operator-induced or unattributed events as Natural L8;
- using legacy runtime policy as current CPS Authority;
- changing Production Maturity from Engineering or shadow evidence.

## Program terminal

`SERVICE_FAILURE_AUTOMATION_EVOLUTION_LOOP_PRODUCTION_CONSUMED_AND_CERTIFIED_BLAST_RADIUS_TIER_DECIDED`

This terminal means the current Incident and Product Evolution projections are
both reconciled: the incident-to-OMP-to-decision-to-gap-to-shadow-to-outcome-to-
Learning loop is production-consumed, all independent product residuals are
either consumed or explicitly owned, and the current action-class Authority
recommendation, including the exact certified blast-radius tier, has been
independently decided.

It does not necessarily mean autonomous routing is enabled, Natural L8 is
sufficient, Authority expanded or Production Maturity increased.

## Exact first executable frontier

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_M1_DURABLE_INCIDENT_FRONTIER_AND_OMP_CONSUMER_V1`
