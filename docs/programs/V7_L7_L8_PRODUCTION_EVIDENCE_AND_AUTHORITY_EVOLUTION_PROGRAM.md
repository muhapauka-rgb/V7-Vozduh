# V7 L7/L8 Production Evidence and Authority Evolution Program

Status: APPROVED_EXECUTION_PLAN

Activation state owner: CPS

This file must not be used to determine whether the program is active, paused, terminal or waiting.

Program ID: `V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM_V1`

Historical execution milestone: `V7_POLYGON_DRIVEN_L7_CONTROLLED_EVIDENCE_ACQUISITION_CALIBRATION_FLOOR_V1` consumed immutable set `outset_428a4e2ff440ed64bde5cb56` with five eligible controlled Passports. M6/M7 remain `INSUFFICIENT_EVIDENCE`, M8 is `MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT`, and current live state remains owned only by CPS.

Current evidence-cycle terminal: `CURRENT_L7_L8_EVIDENCE_CYCLE_RECONCILED_ACTION_CLASS_AUTHORITY_RECOMMENDATION_DECIDED_AND_REVIEW_HANDOFF_RESOLVED`

This is a cycle terminal, not a claim that L7 controlled sufficiency, L8 natural representativeness or the permanent evidence program is complete. `CURRENT` means that every presently available qualifying opportunity and material outcome has been classified, reconciled and consumed, rejected or preserved with an exact owner-backed gap. `REVIEW_HANDOFF_RESOLVED` means Mission 8 is either not required by the Mission 7 verdict or its independent review packet is prepared; it does not mean approval occurred. If evidence remains insufficient, CPS must preserve the exact missing coverage cells and separate reentry conditions: a controlled lane may wait only after Polygon opportunity engineering reaches a genuine policy, owner, substrate or Engineering Authority boundary; a natural L8 lane may stop at `REAL_WORLD_LIMIT` only after its passive capture chain is ready.

## Objective

Convert fresh, owner-backed production situations into complete, replayable and representative evidence for the current `single-user governed candidate failover` action class, then let the existing Production Maturity and Authority owners decide whether that class remains `GOVERNED_ONLY`, is held/demoted, or becomes `CERTIFIED_FOR_CLASS_APPROVAL`.

The program does not grant class Authority, bounded autonomy or autonomous Runtime. It produces the exact evidence and recommendation that an independent Authority decision may consume.

The closed chain is:

`QUALIFYING PRODUCTION OPPORTUNITY -> SITUATION AND PRE-SNAPSHOT -> INTERPRETATION -> DECISION TRACE + PREDICTION + ALTERNATIVES -> CANDIDATE -> PACKET -> LEASE/AUTHORITY -> APPLY OR SAFE NO-ACTION -> TERMINAL ACTIVATION ACKNOWLEDGEMENT -> IMMEDIATE + DELAYED + STEADY-STATE VERIFICATION -> ROLLBACK/NO-ROLLBACK -> OUTCOME PASSPORT -> LEARNING + REPLAY -> CALIBRATION/REPRESENTATIVENESS -> PRODUCTION MATURITY DECISION -> AUTHORITY RECOMMENDATION -> CPS/OMP NEXT FRONTIER`

## Current boundary

The Permanent Polygon is a completed design-time engineering substrate with explicit residuals. It remains a parallel permanent producer and must not be rerun ceremonially. Its L1-L6 engineering evidence cannot close L7 controlled production field validity or L8 natural production representativeness.

Current CPS truth at plan creation:

- action class: `single-user governed candidate failover`;
- action-class state: `GOVERNED_ONLY`;
- approved production scope: at most one user and one serial transaction;
- material owner-backed outcomes: two unique outcomes, one `SUCCESS` and one `ROLLBACK_SUCCESS`;
- Decision Trace, input binding, deterministic production replay and representative Learning remain incomplete;
- Production Maturity remains owner-recorded at `66.9/100`; Production Autonomy remains `0`;
- Authority recommendation remains blocked by real-world evidence;
- no fresh Candidate, Packet or lease exists;
- no production action is authorized by this plan.

The terms `L7` and `L8` in this program are evidence-fidelity levels. They are not autonomy-ladder levels and must never be displayed or consumed as such.

## Discover, reuse, extend, implement decision

### Reuse unchanged

- CPS as the only live program-state owner.
- OMP as Mission/frontier and evidence-consumption coordinator.
- Production Maturity as the only maturity decision owner.
- Authority policy and action-class promotion policy as Authority owners.
- `action_class_authority_decision_reconciliation()` as the existing machine-readable action-class criterion audit.
- `phase6_evidence_classification()` as the existing scenario/controlled/natural evidence-separation rule.
- `build_real_outcome_source_inventory()` as the existing source-level production outcome inventory.
- Controlled Production Certification Program, Certification History and V7 Certification Passport view.
- Existing Situation, Decision, Planner, Candidate, packet, lease, Runtime, Verification, Rollback, feedback, Learning and replay owners.
- Permanent Polygon for design-time differential, counterexample, calibration and risk-obligation production.

### Extend the last responsible owners

The existing source inventory is source-level, while L7/L8 and Authority eligibility require material outcome-level proof. Extend the existing outcome/Certification History/Passport read path with an `Outcome Evidence Passport` projection. It is a normalized view, not a new truth source, database owner, Runtime or promotion engine.

Extend existing verification and learning consumers with temporal observations, intent-drift classification, eligibility decisions, evidence invalidation bindings and coverage denominators. Extend the existing action-class reconciliation with those owner-backed results.

### Do not duplicate

Do not create a second outcome store, Certification Passport, Production Maturity calculator, Authority ladder, Planner, Runtime, replay engine, OMP, CPS, production watcher or Polygon. A new adapter is legal only after a semantic search proves that no existing owner can expose the required projection.

## Industry-derived engineering requirements

The requirements below adapt established network-automation practice without importing vendor architecture as a new V7 owner.

| Industry practice | Primary source | Required V7 application |
| --- | --- | --- |
| Transactional configuration, dry-run, rollback and commit queues; asynchronous acceptance can precede actual network activation. | Cisco NSO Basic Operations and Rollbacks | Do not count an accepted request as an outcome. Require terminal activation acknowledgement, final device/runtime state and canonical verification before evidence is eligible. |
| Continuous comparison of telemetry with intent and anomaly production over time. | Juniper Apstra Intent-Based Analytics and anomaly documentation | Verify intended versus actual state at immediate, delayed and sustained horizons; preserve deviations as evidence, not only endpoint PASS. |
| Change controls with pre/post snapshots, staged execution, health checks, review/approval and network rollback. | Arista CloudVision Advanced Change Control and approval documentation | Bind pre/post/delayed snapshots, stage identity, health verdicts, rollback evidence and independent approver identity to every Authority-eligible outcome. |
| Intent audit distinguishes misaligned attributes, missing objects and undesired objects, and separates synchronize from reconcile. | Nokia NSP intent audit and intent-management framework | Classify drift and approved exceptions so topology/configuration drift is not mislabelled as algorithm success or failure; continuously reconcile actual state with declared intent. |

Primary sources:

- https://developer.cisco.com/docs/nso/guides/basic-operations/
- https://developer.cisco.com/docs/nso/guides/rollbacks/
- https://www.juniper.net/documentation/us/en/software/apstra6.1/apstra-custom-telemetry-collection-guide/topics/concept/apstra-telemetry-and-intent-based-analytics.html
- https://www.juniper.net/documentation/us/en/software/apstra6.1/apstra-user-guide/topics/concept/anomalies-blueprint.html
- https://www.juniper.net/documentation/us/en/software/apstra6.1/apstra-user-guide/topics/topic-map/event-log.html
- https://labguides.testdrive.arista.com/2025.1/cloudvision_portal/cvp_adv_cc/
- https://www.arista.com/en/support/toi/cvp-2021-1-0
- https://www.arista.com/assets/data/pdf/Whitepapers/CloudVision_WP.pdf
- https://documentation.nokia.com/nsp/24-4/Network_Automation/What-is-an-intent-audit.html
- https://documentation.nokia.com/nsp/24-8/NSP_System_Architecture_Guide/Intent-management-framework.html

## Permanent laws

### Evidence-class separation

- Scenario and Polygon evidence may close only declared engineering criteria.
- L7 requires a fresh, safe, controlled production situation through the normal production chain.
- L8 requires a fresh, non-synthetic natural production situation.
- Historical evidence may support current reasoning but cannot satisfy freshness without an explicit still-valid owner binding.
- Evidence cannot be upgraded by naming, copying, replaying or projecting it into a higher class.
- Evidence class is determined by situation and trigger provenance, not by whether the affected subject is labelled an ordinary or certification user.
- One material outcome may have exactly one primary L7/L8 evidence class. A controlled execution arising from a natural incident must preserve both attributes but cannot receive duplicate L7 and L8 credit.

### Polygon-driven evidence opportunity law

The Polygon eliminates avoidable evidence waiting; it does not upgrade simulation into production evidence.

- When an exact L7 cell is missing, the existing OMP/Polygon consumer must actively select the highest-value missing cell, build the safest reproducible condition, resolve the existing Controlled Production owner and certification pool, prepare a fresh Situation, Decision Trace, Candidate, Packet, verification and rollback contract, and carry the opportunity to the production boundary.
- A real L7 Outcome Evidence Passport is earned only by an owner-authorized bounded production transaction and its real verification/rollback/no-rollback closure. Scenario or dry-run output remains Engineering Evidence.
- An ordinary customer must never be moved solely to manufacture evidence. A genuine independently justified production Candidate may use an ordinary customer only inside the already-approved delegated policy. Deliberate certification conditions require an existing owner-authorized certification user and source contract.
- Missing certification users, a disabled certification source, or a deliberate fault/degradation outside current policy must produce the exact `ENGINEERING_AUTHORITY` boundary. The Polygon must still complete every independent preparation and capture-readiness criterion before returning that boundary.
- L8 incidents remain natural and cannot be created. The Polygon must nevertheless audit and repair existing passive event discovery, Situation/Trace/snapshot binding, outcome, rollback/no-rollback, Learning and replay consumption so the next natural event is completely captured.
- A generic `WAIT_FOR_QUALIFYING_L7_L8_OWNER_BACKED_EVIDENCE` is illegal while L7 opportunity preparation or L8 capture-consumer repair can continue safely.

### Production opportunity denominator

Every qualifying opportunity must enter an append-only opportunity projection, including `ACTION`, `STAY`, `STOP_SAFE`, blocked, missed, superseded and no-candidate windows. Selection criteria and exclusion reasons are required. Promotion analysis must use both consumed outcomes and the opportunity denominator so positive-only evidence cannot create survivorship bias.

The opportunity projection must be derived from or appended through an existing event, outcome or certification owner. It must not become an independent durable registry, truth source, watcher, database, queue or scheduling owner.

If existing owners do not durably preserve missed, `STAY`, `STOP_SAFE`, blocked and no-candidate opportunities, Mission 0 must classify the exact producer/consumer gap and route the smallest last-responsible-owner extension through BDP/OMP.

### Material identity and deduplication

Every material outcome receives a deterministic identity derived from situation, incident, action class, source snapshot, policy generation, plan/Candidate identity, selected subject, target, execution generation and terminal closure. Reports, dashboards and retries that project the same outcome are duplicates, not new evidence.

### Outcome completeness

An Authority-eligible Outcome Evidence Passport must bind:

- provenance and real/synthetic classification;
- controlled/natural classification and opportunity identity;
- situation, incident and canonical input snapshot;
- interpretation and confidence;
- Decision Trace ID, prediction, alternatives including `STAY`, and selected decision;
- Candidate, packet, lease/Authority and approved-plan identities where applicable;
- apply/no-action/STOP_SAFE terminal and terminal activation acknowledgement;
- immediate, delayed and sustained verification;
- rollback, no-rollback, containment or safe non-action closure;
- before, after and delayed state snapshots;
- expected-versus-actual and intent-drift classification;
- feedback, Learning consumption and deterministic replay result;
- source/deploy/policy/topology/owner/verification bindings and invalidation state;
- Production Maturity and Authority eligibility decisions;
- exact capability criteria consumed and exact next frontier.

Missing required fields produce `SUPPORTING_ONLY_INCOMPLETE`, never optimistic L7/L8 or Authority credit.

### Temporal validity

Success requires all applicable horizons:

1. activation acknowledgement;
2. immediate safety and service verification;
3. delayed post-admission observation;
4. sustained/steady-state intent alignment for the criterion-defined window.

A later contradiction changes the evidence state to `REGRESSION_REQUIRED`, `SUSPENDED` or owner-defined failure; it does not erase history.

### Intent drift and approved exception

Every intended-versus-actual mismatch must classify as one of:

- expected declared delta;
- misaligned attribute;
- missing required object/state;
- undesired extra object/state;
- approved exception;
- observation/telemetry defect;
- owner/source drift;
- action/decision defect;
- unresolved.

The classification must say whether the safe operation is synchronize evidence to accepted reality, reconcile actual state to intent through an authorized owner, hold, rollback, contain or do nothing. This program cannot perform that mutation by itself.

### Representativeness and calibration

Five fresh material outcomes are only a calibration floor, never a promotion threshold. Coverage must span the relevant matrix of terminal result, action versus stay, success/failure/recovery mode, rollback/no-rollback, service/protocol/channel, source/target/topology, subject/cohort, confidence band, time window and controlled/natural class. Missing relevant cells remain explicit. Statistical uncertainty, calibration error and sample dependence must be reported honestly.

### Negative evidence, demotion and freeze

Failures, STOP_SAFE, missed opportunities, rollback, containment and drift are first-class evidence. They may hold, freeze, demote or narrow an action class. No pipeline may discard negative evidence or switch incidents to preserve a positive result.

### Change invalidation

A source, policy, topology, protocol, owner, verification or execution-contract change invalidates only the bound evidence criteria it affects. The invalidation graph must preserve unaffected evidence and produce the exact revalidation frontier.

### Authority separation

The evidence producer, recommendation producer, approval owner and Runtime enablement owner remain separate roles.

The only legal ladder is:

`GOVERNED_ONLY -> CERTIFIED_FOR_CLASS_APPROVAL -> INDEPENDENT CLASS APPROVAL -> CERTIFIED_FOR_BOUNDED_AUTONOMY -> EXPLICIT POLICY/RUNTIME ENABLEMENT -> AUTONOMOUS_RUNTIME`

This program may reach an evidence-backed recommendation for `CERTIFIED_FOR_CLASS_APPROVAL`. It may not perform independent class approval, grant bounded autonomy, enable Runtime automation, expand blast radius or increase Production Maturity directly.

### Dynamic Mission compression

Missions are capability stages, not ceremonial containers. After every Mission, OMP recalculates remaining criteria. Fully consumed stages become `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`; partially consumed stages shrink to their exact residual. Missions may merge only when owner, isolation, evidence class, completion contract and terminal semantics remain explicit.

### Conditional Mission sequencing

- Mission 0 is mandatory and read-only.
- Missions 1-3 execute only for exact residuals proven by Mission 0. Their acceptance criteria are mandatory, but separate execution containers are not.
- Mission 4 opportunity engineering starts whenever an exact L7 cell is missing. Its real transaction substage starts only on a legal owner-authorized controlled opportunity.
- Mission 5 capture-readiness audit starts whenever an exact L8 cell is missing. Its evidence-consumption substage remains passive/event-driven and starts only on a qualifying natural event.
- Mission 6 may perform calibration only when enough owner-backed Outcome Evidence Passports exist for meaningful analysis. Otherwise it emits the exact missing coverage cells and an immutable `INSUFFICIENT_EVIDENCE` eligibility set.
- Mission 7 may start only after Mission 6 emits one immutable eligibility set, including an insufficient set.
- Mission 8 may start only after Mission 7 returns `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`; otherwise it terminates as `MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT`.
- No Mission may be opened merely because it appears next in this document.

## Missions

### Mission 0 — Current-state and semantic reuse reconciliation

Reconcile CPS, OMP, Production Maturity, Certification History/Passport, existing source inventory, action-class reconciliation, reports and source owners. Produce the material-outcome inventory, duplicate map, exact field completeness matrix, valid/expired evidence bindings and exact L7/L8/Authority residual. This Mission is read-only and must reuse existing owners.

Completion: every current claim points to an owner-backed record; the two known material outcomes are individually classified; no duplicate projection is counted; exact extension points and the smallest next executable Mission are consumed by OMP.

### Mission 1 — Outcome Evidence Passport and opportunity denominator

Extend the existing outcome/Certification History/Passport read path with deterministic record-level material identity, provenance, evidence class, terminal class, completeness, freshness, eligibility and consumption fields. Add the opportunity denominator projection covering action, stay, STOP_SAFE, blocked, missed and no-candidate windows.

Activation condition: `M0_EXACT_RESIDUAL_REQUIRES_RECORD_LEVEL_PROJECTION_OR_DENOMINATOR_EXTENSION`.

Completion: a fresh non-test caller proves real source records are consumed; duplicates collapse deterministically across processes; no new truth owner exists; output reaches action-class reconciliation and OMP.

### Mission 2 — Terminal activation and temporal verification contract

Bind accepted requests to actual activation, immediate verification, delayed observation and steady-state intent alignment. Reuse existing B9 observation, Verification, Runtime and report owners. Add before/after/delayed snapshots and terminal acknowledgement fields where absent.

Activation condition: `M0_EXACT_RESIDUAL_REQUIRES_TEMPORAL_OR_ACTIVATION_BINDING_EXTENSION`.

Completion: an accepted-but-not-activated case cannot earn evidence; late regression changes eligibility; every terminal has a deterministic temporal closure and consumer.

### Mission 3 — Intent drift, exception and production replay

Extend existing interpretation, Decision Trace and replay owners with the intent-drift taxonomy, approved-exception identity, expected-versus-actual comparison and deterministic replay from the exact bound snapshot. Preserve action, stay, STOP_SAFE and rollback alternatives.

Activation condition: `M0_EXACT_RESIDUAL_REQUIRES_DRIFT_OR_REPLAY_EXTENSION`.

Completion: each current material outcome either replays deterministically or carries an exact missing-input blocker; drift is not confused with decision quality; Learning consumes the classification.

### Mission 4 — L7 controlled field-validity acquisition

Opportunity-engineering activation condition: `EXACT_L7_CELL_IS_MISSING`.

Production-transaction activation condition: `LEGAL_OWNER_AUTHORIZED_CONTROLLED_OPPORTUNITY_EXISTS_AND_EXACT_L7_CELL_IS_MISSING`.

Use the existing Polygon to select the exact missing coverage cell and prepare the highest-value safe reproducible situation through existing Situation, Decision Trace, Candidate, Packet, Controlled Production, Verification and Rollback owners. Use existing Controlled Production Certification only when it can legally create the exact missing L7 evidence. Never move an ordinary customer solely to manufacture certification evidence. An ordinary customer may participate only when a genuine qualifying production need exists and the action is independently justified inside the approved delegated policy. Designated certification users may be used only through their existing owner-authorized controlled-production contract. Evidence class follows situation/trigger provenance and cannot be double-counted. No fake incident, fake success, bypassed owner or expanded Authority is allowed.

Completion: a fresh safe governed controlled outcome reaches a complete Outcome Evidence Passport, temporal verification, Learning, replay, Production Maturity decision and OMP consumer; otherwise every safe preparation criterion is consumed and the Mission terminates at the exact owner/substrate/Authority blocker without manufacturing evidence. `ENGINEERING_AUTHORITY_REQUIRED_FOR_CERTIFICATION_POOL_OR_DELIBERATE_CONDITION` is a legal conditional terminal, not permission to relabel an ordinary customer or mutate the pool.

### Mission 5 — L8 natural representativeness capture

Capture-readiness activation condition: `EXACT_L8_CELL_IS_MISSING`.

Evidence-consumption activation condition: `QUALIFYING_NATURAL_EVENT_OBSERVED_BY_EXISTING_OWNER`.

Audit and, where necessary, extend the existing event/wake/outcome consumer path so its actual producer filenames and partitions are discovered and qualifying natural events are passively and durably captured without synthetic triggering or forced user movement. Record both selected and non-selected opportunities and apply the same completeness contract.

Completion: the existing capture chain proves event discovery, Situation/Trace/snapshot, outcome, rollback/no-rollback, Learning and replay readiness before waiting. Fresh natural outcomes are consumed as L8 only when complete; missing opportunity coverage and natural diversity remain explicit; no controlled result is relabelled natural.

### Mission 6 — Coverage, calibration and representative Learning

Activation condition: `CURRENT_OWNER_BACKED_PASSPORT_SET_FROZEN_FOR_ELIGIBILITY_RECONCILIATION`; the frozen set may be empty and must then produce an explicit insufficient-evidence result.

Build the action-class evidence coverage matrix and calibration view over the Outcome Evidence Passports and opportunity denominator. Compare predictions with actuals, quantify uncertainty and dependence, exercise negative evidence, and let the existing Learning/B13 owners change a future recommendation or retain a documented no-change.

Completion: when at least five fresh material outcomes exist, run calibration and explicitly decide whether the required diversity matrix is sufficient; five is never a promotion threshold. When meaningful calibration is not yet possible, emit the exact missing coverage cells without manufacturing a score. In both branches, Learning/B13 consumes the evidence or records an owner-backed no-change, and Mission 6 emits one immutable eligibility set for Mission 7.

### Mission 7 — Action-class Authority recommendation decision

Activation condition: `M6_IMMUTABLE_ELIGIBILITY_SET_AVAILABLE`.

Extend `action_class_authority_decision_reconciliation()` to consume the complete eligibility, calibration, drift, temporal and representativeness decisions. Produce exactly one owner-consumable verdict:

- `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL` — evidence supports independent class-approval review; no approval is granted;
- `RETAIN_CURRENT_SCOPE` — current governed envelope remains justified without promotion or hold;
- `RECOMMEND_NARROW_SCOPE` — recommend a smaller blast radius, fewer failure classes, stricter evidence floors, longer cooldown or temporary exclusion of an exact source/target family while retaining the current ladder state;
- `HOLD_GOVERNED_ONLY` — keep current scope but block progression pending a named review or criterion;
- `FREEZE` — temporarily prohibit the affected action class according to the existing safety owner;
- `DEMOTE_ACTION_CLASS` — recommend a transition to a lower enablement state, potentially `NOT_CERTIFIED`;
- `INSUFFICIENT_EVIDENCE` — retain no optimistic inference and emit exact missing coverage cells and reentry conditions.

`RECOMMEND_NARROW_SCOPE` is not `DEMOTE_ACTION_CLASS`. Recommendation is not mutation: every scope reduction, freeze or demotion remains an independent existing-owner Authority/policy action.

Completion: Production Maturity and Authority owners consume the same immutable evidence set; CPS records the recommendation and exact next action atomically; no Authority is granted by the evidence producer.

### Mission 8 — Independent Authority review boundary

Activation condition: `M7_VERDICT_RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`.

Prepare, but do not execute, the independent class-approval packet if Mission 7 recommends approval. The packet must identify approver separation, exact action class, blast radius, policy generation, expiry, rollback/demotion rules, Runtime-disabled state and explicit next decision.

Completion: when activated, the review packet is ready for a separately authorized Authority decision. For every other Mission 7 verdict, Mission 8 is `MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT`. `CERTIFIED_FOR_BOUNDED_AUTONOMY` and `AUTONOMOUS_RUNTIME` are outside this program unless separately activated by their existing owners.

## Verification and completion contract

Every implementation Mission must prove, in proportion to its effects:

- focused tests and failure-path tests;
- fresh non-test caller and real consumer evidence;
- evidence-class non-interchangeability;
- cross-process duplicate suppression;
- deterministic replay where inputs exist;
- negative, delayed-regression and invalidation cases;
- no forbidden Runtime/Authority/maturity effects;
- `tools/v7-truth-check --all --json`;
- `tools/v7-convergence-status --json`;
- local, GitHub and production snapshot consistency after any required safe deploy;
- a compact saved Engineering Report.

The current evidence-cycle terminal may be emitted only when:

- all current material outcomes are record-level reconciled;
- every currently available L7 and L8 opportunity is independently classified and consumed, rejected or preserved with an exact gap;
- completeness, temporal, drift, replay and coverage decisions exist for the current set;
- meaningful calibration ran when possible; otherwise exact missing coverage cells were emitted without a synthetic score;
- Learning/B13 has a real downstream effect or an owner-backed no-change decision;
- Production Maturity made an owner decision without manual score editing;
- the existing Authority owner consumed an evidence-backed recommendation;
- Mission 8 is either `MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT` or its independent review handoff is prepared;
- CPS and OMP expose one exact next frontier;
- no second truth source or duplicate execution owner was created.

The cycle terminal does not assert L7 sufficiency, L8 sufficiency, class approval, Authority expansion, bounded autonomy or permanent-program completion. When Mission 7 returns `INSUFFICIENT_EVIDENCE`, `HOLD_GOVERNED_ONLY` or another non-promotion verdict with open evidence cells, CPS must retain an event-driven program state and exact reentry conditions.

## Forbidden effects without separate authorization

- Runtime apply or routing mutation;
- ordinary-user movement or forced natural incidents;
- packet execution, restore-barrier write or rollback apply;
- daemon/timer enablement;
- Authority expansion, class approval or bounded-autonomy grant;
- Runtime automation enablement;
- direct Production Maturity score change;
- relabelling synthetic, scenario, historical or controlled evidence as natural production evidence.

## Initial Mission after plan approval

`V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_M0_CURRENT_STATE_RECONCILIATION_V1`

It is audit-only and read-only. It must shrink itself to the exact residual already not provided by the existing source inventory, Certification Passport and action-class reconciliation.
