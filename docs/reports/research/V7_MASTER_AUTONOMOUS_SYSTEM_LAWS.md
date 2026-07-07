# V7 Master Autonomous System Laws

Status: `PERMANENT_CUMULATIVE_RESEARCH_KB`
Research program: `R4_MASTER_AUTONOMOUS_SYSTEM_LAWS`
Created: 2026-07-05
Mode: `RESEARCH_ONLY`
Runtime impact: `NONE`
Planner impact: `NONE`
Authority impact: `NONE`
Production impact: `NONE`
Deployment performed: `NO`

## 1. Executive Summary

R4 extracts implementation-independent engineering laws from the existing R1, R2, and R3 research knowledge bases.

This document does not summarize companies. It removes company names, product names, and implementation details, then keeps only the engineering truths that remain stable across routing reliability, production operations, and engineering automation.

Core finding:

```text
Autonomous production systems become reliable only when autonomy is split into evidence, decision, authority, execution, verification, rollback, learning, and evolution.
```

The strongest universal law is:

```text
Reality precedes authority.
```

Every mature system independently converges on the idea that a signal, alert, probe, metric, report, AI output, timer, or document is not itself permission to mutate production. Production mutation requires evidence, owner, authority, bounded execution, verification, and rollback or closure.

## 2. Research Inputs

Primary inputs read for this synthesis:

| Input | Repository path | Note |
| --- | --- | --- |
| R1 Routing/Reliability KB | `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md` | Prompt referenced `V7_ROUTING_RELIABILITY_RESEARCH.md`; repository contains this existing R1 KB instead. |
| R2 Autonomous Operations KB | `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md` | Production operations, SRE, incident, change, governance. |
| R3 Autonomous Engineering Systems KB | `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md` | Engineering automation, IDP, analyzers, workflow evolution. |

No primary input was modified.

## 3. Extraction Method

For each candidate law:

1. Remove organization names.
2. Remove product names.
3. Remove vendor-specific technology.
4. Keep only the invariant.
5. Test whether the invariant appears in at least two research programs.
6. Identify what breaks if the invariant is violated.
7. Map the invariant to existing V7 owners.
8. Classify universality and V7 adoption.

Extraction rule:

```text
If the practice depends on a specific technology, it is not a universal law.
If the practice appears across domains and prevents a general failure mode, it may be a law.
```

## 4. Law Classification Method

Universality:

- `UNIVERSAL`: required for any large-scale autonomous production system.
- `LIKELY_UNIVERSAL`: broadly true, but implementation context changes strength.
- `ORGANIZATION_SPECIFIC`: useful in one operating model but not universal.
- `TECHNOLOGY_SPECIFIC`: tied to a concrete implementation family.

V7 adoption:

- `YES`: should become a V7 law or remain a V7 law.
- `LATER`: valid but depends on future capability, telemetry, or maturity.
- `NO`: should not be adopted as a V7 law.

Law record schema:

Each law below includes:

- law name;
- statement;
- engineering reason;
- why it exists;
- problem prevented;
- evidence from organizations/source families;
- universality;
- exceptions;
- failure if violated;
- V7 mapping;
- existing owners;
- automation, autonomy, OMP, Current Program State, and Production Maturity impact;
- future relevance;
- V7 adoption.

## 5. Universal Laws

### LAW U1: Reality Precedes Authority

Statement: Production mutation may occur only after real evidence exists and an authority owner admits the action.

Engineering Reason: A fact about the world and permission to change the world are different objects.

Why this law exists: Large systems receive noisy, stale, partial, or context-free signals. Treating any signal as permission creates unsafe automation.

Problem it prevents: Timer authority, alert-driven mutation, synthetic certification, AI mutation, and report-only capability claims.

Evidence from organizations: R1 routing systems separate health checks from routing controls; R2 operations separate incident detection from response authority; R3 engineering platforms separate workflow triggers from guarded pipelines.

Universality: `UNIVERSAL`.

Exceptions: Emergency break-glass can compress process only under explicit authority and audit.

Failure if violated: False positive movement, broad outage, wrong target selection, unaudited production mutation.

V7 mapping: Observation -> Wake -> Incident -> Planner -> Authority -> Runtime Apply.

Existing owners: Observation, Wake, Incident, Planner, Authority, Runtime, OMP.

Automation impact: Automation must produce evidence before action.

Autonomy impact: Autonomous action classes require certified authority.

OMP impact: OMP must route evidence to owners and prevent shortcut execution.

Current Program State impact: CPS records current evidence and blocker, but cannot approve action.

Production Maturity impact: Production Maturity consumes evidence, not permission.

Future relevance: Foundation for all future L3-L7 autonomy.

Should V7 adopt: `YES`.

### LAW U2: Detection Is Not Diagnosis

Statement: A failed probe or alert proves only that something was observed, not why it happened.

Engineering Reason: Symptoms can have multiple producers and consumers.

Why this law exists: Health systems often detect failure before root cause attribution is known.

Problem it prevents: Misclassifying source failure, target failure, service failure, load, freshness, or policy failure.

Evidence from organizations: R1 health matrices and reason codes; R2 incident triage stages; R3 Owner Resolution analyzers.

Universality: `UNIVERSAL`.

Exceptions: None for root-cause claims; emergency action may proceed on sufficient symptom evidence if policy allows.

Failure if violated: Planner overclassification, wrong rollback, wrong owner, repeated investigation drift.

V7 mapping: Observation produces facts; Owner Resolution proves producer/consumer/root condition.

Existing owners: Observation, service matrix, Incident, Owner Resolution, Engineering Reports.

Automation impact: Automated diagnosis must be read-only and backtested before decisions.

Autonomy impact: Autonomy may use confirmed action-class evidence without claiming root cause beyond evidence.

OMP impact: OMP must convert owner blocks into Owner Resolution, not stop at label.

Current Program State impact: CPS must expose blocking owner and terminal root cause separately.

Production Maturity impact: Maturity cannot accept unproven diagnosis as capability evidence.

Future relevance: Required for automated RCA.

Should V7 adopt: `YES`.

### LAW U3: Decision Is Not Execution

Statement: A plan, recommendation, candidate, score, or selected move is not production execution.

Engineering Reason: Planned state can become stale, invalid, unauthorized, or unsafe before apply.

Why this law exists: Large systems need a final live gate between intent and mutation.

Problem it prevents: Planner-only truth, stale candidates, hidden recomputation, bypassed safety.

Evidence from organizations: R1 routing controls and verification; R2 change gates; R3 workflow pipelines and CI gates.

Universality: `UNIVERSAL`.

Exceptions: None for production mutation.

Failure if violated: Plan drift, wrong identity applied, unauthorized blast radius.

V7 mapping: Planner -> Authority -> Approved Plan Lock -> Restore Barrier -> Runtime Apply.

Existing owners: Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime.

Automation impact: Pipelines must preserve committed identity across steps.

Autonomy impact: Autonomous execution needs locked object continuity.

OMP impact: OMP must distinguish output produced from output consumed.

Current Program State impact: CPS must not equate candidate existence with executed capability.

Production Maturity impact: Only verified execution can advance production maturity.

Future relevance: Critical for larger batches and future action classes.

Should V7 adopt: `YES`.

### LAW U4: Verification Completes Mutation

Statement: A production change is incomplete until independent verification proves its outcome.

Engineering Reason: Apply success proves only that a command ran, not that user-visible service recovered.

Why this law exists: Distributed systems often accept writes or route changes that fail service objectives.

Problem it prevents: False success, hidden partial failure, rollback omission.

Evidence from organizations: R1 post-shift health checks; R2 rollback/recovery models; R3 safe deploy and regression gates.

Universality: `UNIVERSAL`.

Exceptions: None; if verification is impossible, the outcome is unknown or contained, not success.

Failure if violated: Users remain broken while system reports success.

V7 mapping: Runtime Apply -> Verification -> Rollback / No-Rollback Closure -> Learning.

Existing owners: Runtime, Verification, Rollback, Learning, Engineering Reports.

Automation impact: Automated pipelines must wait for verification.

Autonomy impact: Autonomy cannot promote without verified outcomes.

OMP impact: OMP cannot declare phase PASS without verification evidence.

Current Program State impact: CPS must record terminal verification state.

Production Maturity impact: Maturity consumes verified outcomes only.

Future relevance: Required for FULL_INCIDENT and routine production operation.

Should V7 adopt: `YES`.

### LAW U5: Rollback Or Closure Is Mandatory

Statement: Every mutation must have rollback, containment, or certified no-rollback closure.

Engineering Reason: Not every change can be reverted, but every touched object needs a terminal safety state.

Why this law exists: Failure after apply is normal; unclosed failure expands risk over time.

Problem it prevents: Stuck users, unknown state, repeated bad retries, unsafe promotion.

Evidence from organizations: R1 rollback patterns; R2 rollback/recovery; R3 safe deploy rollback identity.

Universality: `UNIVERSAL`.

Exceptions: No rollback may be acceptable only if no-rollback closure is explicitly certified.

Failure if violated: Persistent inconsistent production state.

V7 mapping: Verification failure -> Rollback / Containment; success -> No-Rollback Closure.

Existing owners: Rollback, Verification, Runtime, Learning, OMP.

Automation impact: Pipelines must encode closure paths.

Autonomy impact: Autonomous expansion stops without closure evidence.

OMP impact: OMP keeps mission incomplete until closure.

Current Program State impact: CPS records rollback/no-rollback state.

Production Maturity impact: Maturity rejects open-ended mutation evidence.

Future relevance: Essential for batch and multi-user operations.

Should V7 adopt: `YES`.

## 6. Routing Laws

### LAW R1: Health Is A Matrix, Not A Boolean

Statement: Routing health must preserve source, target, service, freshness, load, safety, and reason evidence separately.

Engineering Reason: One boolean hides the first failing gate.

Why this law exists: Routing decisions combine independent health dimensions with different owners.

Problem it prevents: Opaque `eligible=false`, wrong failover reason, stale proof.

Evidence from organizations: R1 health reason codes and probe taxonomies; R2 severity/SLO mapping; R3 service catalog ownership.

Universality: `UNIVERSAL` for routing systems.

Exceptions: UI summaries may aggregate only if raw evidence remains inspectable.

Failure if violated: Root cause cannot be proven; automation selects wrong object.

V7 mapping: service matrix, quality, load, safety, `_candidate()` gates, Verification matrix.

Existing owners: Observation, service matrix, Planner, Verification.

Automation impact: Automation must carry full health object.

Autonomy impact: Higher autonomy requires typed evidence continuity.

OMP impact: OMP should reject ownerless health conclusions.

Current Program State impact: CPS should store blocker and source object pointer.

Production Maturity impact: Maturity needs evidence quality scoring.

Future relevance: Multi-perspective health and analyzer correctness.

Should V7 adopt: `YES`.

### LAW R2: Routing Identity Must Be Continuous

Statement: The same execution object must preserve user, source, target, action, generation, selected move hash, and incident identity through all owners.

Engineering Reason: Distributed control planes can silently switch objects between planning, approval, execution, and verification.

Why this law exists: Object continuity is the only proof that each owner evaluated the same action.

Problem it prevents: Candidate switching, selected-move loss, restore-barrier mismatch, wrong incident continuation.

Evidence from organizations: R1 route controls preserve target/pool identity; R2 incident lifecycles; R3 pipeline artifact identity.

Universality: `UNIVERSAL`.

Exceptions: Explicit restart with documented new identity.

Failure if violated: Later conclusions explain the wrong execution.

V7 mapping: operation_id, planner_generation, selected_move_hash, approved lock, restore barrier, packet.

Existing owners: Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime, Verification.

Automation impact: Pipelines must pass identity, not recompute hidden identity.

Autonomy impact: Autonomous execution requires immutable committed object.

OMP impact: OMP reports must preserve lineage.

Current Program State impact: CPS must expose current execution identity.

Production Maturity impact: Maturity rejects evidence with identity drift.

Future relevance: Batch and FULL_INCIDENT certification.

Should V7 adopt: `YES`.

### LAW R3: Failover Scope Must Follow The Incident

Statement: A failover incident remains scoped to its failed source until recovery, containment, impossibility, or no affected users remain.

Engineering Reason: Recovery objective belongs to the incident, not to whichever candidate ranks highest next.

Why this law exists: Without scope continuity, automation drifts from restoring affected users into unrelated optimization.

Problem it prevents: Unrelated source selection, incident closure after one move while users remain, wrong wake evaluation.

Evidence from organizations: R1 pool/incident source handling; R2 incident continuation; V7 production findings synthesized in R1/R2.

Universality: `LIKELY_UNIVERSAL` for incident-scoped recovery.

Exceptions: Explicit incident split/merge under authority.

Failure if violated: Remaining affected users stay broken while system moves unrelated users.

V7 mapping: incident_source continuity, failed-source candidate pool, Wake against incident_source.

Existing owners: Incident, Planner, Wake, Authority, Runtime.

Automation impact: Candidate selection must constrain to incident scope.

Autonomy impact: L3 autonomy cannot drift into rebalance.

OMP impact: OMP must treat scope drift as implementation defect.

Current Program State impact: CPS records incident source and remaining users.

Production Maturity impact: Maturity certification requires correct continuation.

Future relevance: L4-L7 incident arbitration.

Should V7 adopt: `YES`.

## 7. Reliability Laws

### LAW RL1: Retry Is A Budgeted Semantic Attempt

Statement: Retries must be bounded by semantic action identity, not by process invocation identity.

Engineering Reason: Repeating the same failed user/source/target attempt can amplify failure even if command IDs differ.

Why this law exists: Retries protect transient failure but harm systems under persistent failure.

Problem it prevents: Duplicate apply attempts, overload, infinite rollback loops.

Evidence from organizations: R1 AWS retry/backoff and Netflix circuit breakers; R2 automation suspension; R3 pipeline retry risk.

Universality: `UNIVERSAL`.

Exceptions: Explicit authority may reset budget after new evidence or changed target.

Failure if violated: System repeatedly chooses known bad attempt.

V7 mapping: semantic_attempt_signature, retry_budget_per_incident, duplicate_apply_attempt.

Existing owners: Planner, Runtime, Rollback, Learning.

Automation impact: Automation must exclude exhausted semantic attempts.

Autonomy impact: Autonomous retries need budgets and learning.

OMP impact: OMP must distinguish exhausted attempt from no remaining work.

Current Program State impact: CPS records current retry blocker.

Production Maturity impact: Maturity requires retry correctness evidence.

Future relevance: All autonomous action classes.

Should V7 adopt: `YES`.

### LAW RL2: Stability Requires Hysteresis

Statement: State changes must be dampened by thresholds, windows, cooldowns, or cost evaluation.

Engineering Reason: Large systems observe noisy signals and delayed feedback.

Why this law exists: Immediate reaction to every signal creates oscillation.

Problem it prevents: Routing flap, repeated recover/fail cycles, overload cascades.

Evidence from organizations: R1 thresholds/windows/dampening; R2 freeze/halt; R3 progressive pipeline promotion.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: confirmed hard failures may bypass long wait but still require authority and verification.

Failure if violated: Automation worsens instability.

V7 mapping: anti-flap, cooldown, recovery admission, movement protection, state-change cost.

Existing owners: Observation, Planner, Authority, Runtime, Production Maturity.

Automation impact: Automation must include backoff or halt.

Autonomy impact: Autonomous promotion requires no-regression windows.

OMP impact: OMP should record hold windows and maturity.

Current Program State impact: CPS records current window/blocker.

Production Maturity impact: Maturity consumes no-regression evidence.

Future relevance: Recovery autonomy and rebalance.

Should V7 adopt: `YES`.

### LAW RL3: Overload Protection Beats Throughput

Statement: A system must reject, shed, delay, or reduce work before accepting work that would make recovery fail.

Engineering Reason: Recovery action consumes capacity; too much recovery can become the outage.

Why this law exists: Cascading failure often comes from helpful retries or broad automation.

Problem it prevents: Lock starvation, target overload, verification timeout, cascading failure.

Evidence from organizations: R1 load shedding/adaptive concurrency; R2 safety halt; R3 pipeline queues and gates.

Universality: `UNIVERSAL`.

Exceptions: Explicit emergency policy may trade throughput for recovery only with bounded risk.

Failure if violated: Recovery path collapses under its own load.

V7 mapping: `_gate_load`, service-matrix locks, Authority budget, batch ladder.

Existing owners: Planner load gate, Authority, Runtime, Verification.

Automation impact: Automation needs concurrency and lock budgets.

Autonomy impact: Higher batch sizes require capacity evidence.

OMP impact: OMP must not promote when recovery resources are overloaded.

Current Program State impact: CPS records resource blocker.

Production Maturity impact: Maturity consumes load/capacity evidence.

Future relevance: XLARGE and FULL_INCIDENT.

Should V7 adopt: `YES`.

## 8. Authority Laws

### LAW A1: Authority Bounds Blast Radius

Statement: The number, scope, and class of production objects affected by automation must be explicitly bounded.

Engineering Reason: Good actions become dangerous when applied too broadly.

Why this law exists: Reliability improves through staged exposure, not all-at-once mutation.

Problem it prevents: Global rollout failure, all-user evacuation without proof, uncontrolled blast radius.

Evidence from organizations: R1 canary/batch/traffic shedding; R2 progressive rollout; R3 progressive engineering automation.

Universality: `UNIVERSAL`.

Exceptions: FULL_INCIDENT only after certification and authority recognition.

Failure if violated: One defect reaches all users or all systems.

V7 mapping: Authority Budget, 1 -> 5 -> 10 -> 25 -> 50 -> FULL_INCIDENT.

Existing owners: Authority, Controlled Production Certification Program, OMP.

Automation impact: Automation must read authority budget.

Autonomy impact: Autonomy expands only after certification.

OMP impact: OMP executes phases sequentially.

Current Program State impact: CPS records current authority class.

Production Maturity impact: Maturity consumes stage evidence.

Future relevance: Core production autonomy ladder.

Should V7 adopt: `YES`.

### LAW A2: Policy Exceptions Must Be Explicit

Statement: Any bypass, override, break-glass, fail-open, or emergency acceleration must be named, authorized, audited, and bounded.

Engineering Reason: Hidden exceptions become new architecture.

Why this law exists: Operators need exceptional powers, but systems need auditability.

Problem it prevents: Safety bypass disguised as urgency.

Evidence from organizations: R1 fail-open/fail-closed classification; R2 overrides/freeze; R3 self-service guardrails.

Universality: `UNIVERSAL`.

Exceptions: None; exceptions are the subject of the law.

Failure if violated: Unreviewable production mutation and policy erosion.

V7 mapping: break-glass authority, Authority policy, Engineering Reports.

Existing owners: Authority, OMP, Engineering Reports, CPS.

Automation impact: Automation cannot invent exceptions.

Autonomy impact: Autonomous system must stop when exception is needed.

OMP impact: OMP routes exception to policy owner.

Current Program State impact: CPS records exception state.

Production Maturity impact: Maturity does not treat exception as normal capability.

Future relevance: Emergency production operations.

Should V7 adopt: `YES`.

## 9. Safety Laws

### LAW S1: Fail Mode Must Be Classified

Statement: Every gate must define whether failure means fail-closed, fail-open, hold, rollback, containment, or impossibility.

Engineering Reason: Unknown failure semantics cause inconsistent downstream behavior.

Why this law exists: Different action classes tolerate uncertainty differently.

Problem it prevents: Treating timeout as service failure, treating missing evidence as success, unsafe fail-open.

Evidence from organizations: R1 fail-open/fail-closed; R2 safety halt; R3 policy guardrails.

Universality: `UNIVERSAL`.

Exceptions: None for safety gates.

Failure if violated: Unsafe or contradictory terminal states.

V7 mapping: Runtime eligibility, Verification, Rollback, Authority.

Existing owners: Runtime, Authority, Verification, Rollback.

Automation impact: Automation must branch by fail mode.

Autonomy impact: Autonomous action class needs explicit failure behavior.

OMP impact: OMP reports blocker classification.

Current Program State impact: CPS exposes terminal class.

Production Maturity impact: Maturity rejects ambiguous safety evidence.

Future relevance: All capabilities.

Should V7 adopt: `YES`.

### LAW S2: Synthetic Evidence Cannot Certify Reality

Statement: Synthetic tests, dry runs, and examples can prove semantics, but only real production evidence can certify production capability.

Engineering Reason: Simulated worlds omit hidden coupling, timing, load, and operator constraints.

Why this law exists: Certification must predict real production behavior.

Problem it prevents: False autonomy maturity.

Evidence from organizations: R1 production verification; R2 controlled production; R3 tests vs capability distinction.

Universality: `UNIVERSAL`.

Exceptions: None for production certification.

Failure if violated: Capability appears certified but fails in production.

V7 mapping: Reality First, Controlled Production Certification, Production Maturity.

Existing owners: Certification Program, OMP, Production Maturity.

Automation impact: Automation tests do not equal production certification.

Autonomy impact: Autonomy remains disabled until real evidence exists.

OMP impact: OMP must create controlled production evidence when random incidents are absent.

Current Program State impact: CPS records evidence class.

Production Maturity impact: Maturity rejects synthetic-only evidence.

Future relevance: Certification infrastructure.

Should V7 adopt: `YES`.

## 10. Verification Laws

### LAW V1: Verifier Must Check The Same Contract Planner Claimed

Statement: Verification must evaluate the same required services, user, source, target, and action class that planning and runtime used.

Engineering Reason: Independent verification is only meaningful if contract identity is preserved.

Why this law exists: Different probes or scopes can create false rollback or false success.

Problem it prevents: Verification checking a service Planner never evaluated; timeout mistaken for service failure.

Evidence from organizations: R1 verification matrix comparison; R2 rollback evidence; R3 regression gates.

Universality: `UNIVERSAL`.

Exceptions: Additional checks may run but must be labeled extra and not retroactively redefine the plan.

Failure if violated: First divergence cannot be identified.

V7 mapping: Planner service matrix vs Verification matrix.

Existing owners: Planner, Runtime, Verification, Engineering Reports.

Automation impact: Automated verification must persist raw probe output.

Autonomy impact: Promotion depends on matching contract verification.

OMP impact: OMP requires first divergence evidence.

Current Program State impact: CPS records verification result and owner.

Production Maturity impact: Maturity consumes comparable matrices.

Future relevance: Multi-service and batch verification.

Should V7 adopt: `YES`.

### LAW V2: Unknown Is Not Fail And Not Pass

Statement: Timeout, missing data, stale data, lock wait, or unpersisted object must be classified as unknown unless evidence proves pass or fail.

Engineering Reason: Absence of result is a different fact from negative result.

Why this law exists: Distributed probes fail for reasons unrelated to target health.

Problem it prevents: Rolling back healthy users because verifier timed out waiting on a lock.

Evidence from organizations: R1 verification timeout distinction; R2 incident evidence; R3 analyzer confidence.

Universality: `UNIVERSAL`.

Exceptions: Policy may fail-closed on unknown, but reason remains unknown.

Failure if violated: Wrong owner is blamed and wrong correction is made.

V7 mapping: `UNKNOWN` verification, service matrix lock owner, failed probe raw output.

Existing owners: Verification, service matrix, Engineering Reports.

Automation impact: Automation must preserve unknown reason.

Autonomy impact: Autonomy should not learn false service failure from unknown.

OMP impact: OMP routes unknown to evidence owner.

Current Program State impact: CPS records missing object / unknown state.

Production Maturity impact: Maturity treats unknown as incomplete evidence.

Future relevance: Analyzer accuracy.

Should V7 adopt: `YES`.

## 11. Rollback Laws

### LAW RB1: Rollback Is Operational Compensation, Not Time Travel

Statement: Rollback restores a safe operational state; it does not erase all side effects.

Engineering Reason: Distributed state cannot be globally rewound after production mutation.

Why this law exists: Rollback must be concrete and scoped, not assumed.

Problem it prevents: False belief that failed automation has no residue.

Evidence from organizations: R1 rollback/traffic restoration; R2 rollback closure; R3 safe deploy identity.

Universality: `UNIVERSAL`.

Exceptions: Purely local reversible changes may fully revert, but still need proof.

Failure if violated: Learning and maturity ignore residual risk.

V7 mapping: rollback operational compensation, containment, no-rollback closure.

Existing owners: Rollback, Runtime, Verification, Learning.

Automation impact: Automation must store touched objects.

Autonomy impact: Autonomous expansion requires rollback competence.

OMP impact: OMP keeps failure open until rollback closure.

Current Program State impact: CPS records rollback terminal state.

Production Maturity impact: Maturity scores rollback correctness.

Future relevance: Multi-user batch partial failure.

Should V7 adopt: `YES`.

### LAW RB2: Partial Success Is A First-Class Outcome

Statement: A batch or workflow may succeed for some objects and fail for others; the system must preserve per-object outcome.

Engineering Reason: Large-scale actions rarely fail atomically.

Why this law exists: Binary success/failure loses user-level safety.

Problem it prevents: Rolling back successful users unnecessarily or leaving failed users unclosed.

Evidence from organizations: R1 partial/verification patterns; R2 batch rollback; R3 pipeline step evidence.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Strict single-object transactions can remain binary.

Failure if violated: Incorrect incident closure and maturity evidence.

V7 mapping: per-user verification, rollback/no-rollback closure, batch ladder.

Existing owners: Runtime, Verification, Rollback, Learning, Certification.

Automation impact: Automation reports per-object status.

Autonomy impact: Batch autonomy depends on partial success handling.

OMP impact: OMP must not treat one batch state as all-user truth.

Current Program State impact: CPS records moved/failed/remaining.

Production Maturity impact: Maturity consumes per-user evidence.

Future relevance: FULL_INCIDENT.

Should V7 adopt: `YES`.

## 12. Engineering Laws

### LAW E1: Repeated Manual Work Is Debt Until Classified

Statement: Every repeated manual action or workflow is automation/workflow debt until automated, intentionally manual, not cost-effective, blocked by future capability, or impossible.

Engineering Reason: Unclassified repetition scales linearly with system growth.

Why this law exists: Human attention does not scale with production complexity.

Problem it prevents: Permanent Codex/admin dependency.

Evidence from organizations: R2 toil/runbook models; R3 golden path and workflow audit; R1 repeated forensic analyzer candidates.

Universality: `UNIVERSAL` for growing systems.

Exceptions: Rare judgment work can be intentionally manual.

Failure if violated: Engineering system cannot scale.

V7 mapping: Automation Debt, Workflow Debt, Pipeline Candidate.

Existing owners: OMP, Engineering Automation, Workflow Audit.

Automation impact: Creates automation backlog input.

Autonomy impact: Enables Codex exit strategy.

OMP impact: OMP classifies and routes debt.

Current Program State impact: CPS records debt current.

Production Maturity impact: Maturity consumes automation evolution evidence.

Future relevance: Self-improving V7.

Should V7 adopt: `YES`.

### LAW E2: Reports Preserve Evidence, Not Authority

Statement: Reports can prove history and feed owners, but cannot become live truth, roadmap, or authority.

Engineering Reason: Historical artifacts are stale by design unless consumed by canonical owners.

Why this law exists: Documentation drift and report-only completion create false capability.

Problem it prevents: Acting on stale reports or treating reports as implementation queues.

Evidence from organizations: R2 postmortem-to-work; R3 docs-as-code boundaries; V7 document lifecycle in research context.

Universality: `UNIVERSAL`.

Exceptions: None; reports may be authoritative only about their own historical content.

Failure if violated: Roadmap drift and stale production action.

V7 mapping: Engineering Reports -> OMP/Production Maturity/CPS/canonical owners.

Existing owners: Engineering Reports, OMP, Document Lifecycle, Production Maturity.

Automation impact: Report sync can be automated but not self-authorizing.

Autonomy impact: Autonomy cannot be granted by report.

OMP impact: OMP decides owner consumption.

Current Program State impact: CPS updates only for volatile state changes.

Production Maturity impact: Maturity accepts/rejects report evidence.

Future relevance: Automated documentation and analyzers.

Should V7 adopt: `YES`.

## 13. Knowledge Laws

### LAW K1: Durable Truth Has One Owner

Statement: A durable rule or semantic fact must live in exactly one canonical owner.

Engineering Reason: Multiple truth sources diverge under change pressure.

Why this law exists: Large systems need lookup and propagation without contradiction.

Problem it prevents: duplicate roadmap, duplicate planner, duplicate OMP, conflicting laws.

Evidence from organizations: R3 service catalog; R2 ownership models; R1 owner-separated control plane.

Universality: `UNIVERSAL`.

Exceptions: Projections are allowed when labeled consumers.

Failure if violated: Different components obey different truths.

V7 mapping: Canonical Reference, SYSTEM_MAP lookup, OMP, CPS.

Existing owners: Canonical owners, SYSTEM_MAP, OMP.

Automation impact: Automation must discover owner before writing.

Autonomy impact: Self-improvement cannot create hidden truth.

OMP impact: OMP prevents duplicate owners.

Current Program State impact: CPS is volatile consumer only.

Production Maturity impact: Maturity is consumer only.

Future relevance: Autonomous knowledge synchronization.

Should V7 adopt: `YES`.

### LAW K2: Knowledge Must Be Fresh Enough For Its Action Class

Statement: Evidence freshness requirements depend on the risk and reversibility of the action.

Engineering Reason: Stale data may be acceptable for analysis but unsafe for mutation.

Why this law exists: Different actions have different time sensitivity.

Problem it prevents: stale-read mutation and false STOP/GO decisions.

Evidence from organizations: R1 freshness windows; R2 readiness vs runtime; R3 docs vs execution authority.

Universality: `UNIVERSAL`.

Exceptions: Read-only analysis can tolerate older data if labeled stale.

Failure if violated: Production mutation based on obsolete state.

V7 mapping: Policy 008 freshness, Runtime eligibility, action-class windows.

Existing owners: Runtime, Authority, Observation, OMP.

Automation impact: Pipelines must validate freshness at mutation gates.

Autonomy impact: Autonomy needs per-class freshness windows.

OMP impact: OMP distinguishes stale evidence from missing evidence.

Current Program State impact: CPS records stale state.

Production Maturity impact: Maturity can reject stale evidence.

Future relevance: All automated action classes.

Should V7 adopt: `YES`.

## 14. Automation Laws

### LAW AU1: Automation Must Be Suspendable

Statement: Every autonomous or semi-autonomous action class must have a stop, hold, demotion, or suspension path.

Engineering Reason: Automation amplifies both correctness and defects.

Why this law exists: Bad automation needs a fast bounded stop.

Problem it prevents: runaway automation, repeated rollback, cascading incident.

Evidence from organizations: R1 circuit breakers; R2 safety halt/freeze; R3 automation guardrails.

Universality: `UNIVERSAL`.

Exceptions: Read-only automation may stop by disabling output consumption.

Failure if violated: Defective loop continues after evidence of harm.

V7 mapping: Authority demotion, OMP HOLD, circuit breaker, retry budget, Runtime STOP_SAFE.

Existing owners: Authority, OMP, Runtime, Verification, Rollback.

Automation impact: Every pipeline needs stop conditions.

Autonomy impact: Certified autonomy requires suspension triggers.

OMP impact: OMP classifies halt and owner resolution.

Current Program State impact: CPS records suspended capability.

Production Maturity impact: Maturity consumes suspension evidence.

Future relevance: Routine production operation.

Should V7 adopt: `YES`.

### LAW AU2: Automation Quality Must Be Backtested

Statement: An analyzer or automated judgment must be tested against historical evidence before it can block, recommend mutation, or promote capability.

Engineering Reason: Automation can be confidently wrong.

Why this law exists: Analyzer precision matters only against real past cases.

Problem it prevents: False root cause, false blocker, false promotion.

Evidence from organizations: R1 analyzer/backtesting; R2 automated investigation; R3 Tricorder/Infer/DrP/Kayenta synthesis.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Non-blocking read-only hints can run before backtesting if labeled advisory.

Failure if violated: Analyzer becomes a new source of outages.

V7 mapping: Owner Resolution analyzers, Engineering Report fixture corpus.

Existing owners: OMP, Engineering Reports, tests, affected owners.

Automation impact: Analyzer pipeline needs fixtures and metrics.

Autonomy impact: Autonomy can consume analyzer only after certification.

OMP impact: OMP routes analyzer evidence.

Current Program State impact: CPS may expose analyzer confidence.

Production Maturity impact: Maturity consumes analyzer reliability evidence.

Future relevance: Self-improving operations.

Should V7 adopt: `YES`.

## 15. Workflow Laws

### LAW W1: Paved Roads Must Be Easier Than Ad Hoc Paths

Statement: The safe, owner-backed workflow must be easier to use than repeated manual orchestration.

Engineering Reason: Developers and operators route around friction.

Why this law exists: Safety systems fail if normal work requires heroic manual steps.

Problem it prevents: shadow scripts, permanent Codex dependency, process bypass.

Evidence from organizations: R3 IDP/golden path; R2 runbook evolution; R1 repeated forensic workflows.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Rare high-risk work may intentionally remain manual.

Failure if violated: Correct process is skipped.

V7 mapping: Pipeline Candidate, Engineering Automation, OMP execution pipeline.

Existing owners: OMP, SYSTEM_MAP, Workflow Debt.

Automation impact: Create command-minimized pipelines.

Autonomy impact: Reduces human orchestration without safety bypass.

OMP impact: OMP prioritizes high-friction workflows.

Current Program State impact: CPS exposes current pipeline candidates.

Production Maturity impact: Maturity consumes workflow improvement evidence.

Future relevance: Codex removal from routine work.

Should V7 adopt: `YES`.

### LAW W2: Self-Service Must Be Owner-Bounded

Statement: Self-service is safe only when the service exposes existing owner contracts and cannot bypass policy or verification.

Engineering Reason: Self-service without boundaries is broad authority.

Why this law exists: Platforms reduce waiting, but can spread unsafe capability.

Problem it prevents: portal as production bypass, unauthorized movement, hidden ownerless mutation.

Evidence from organizations: R3 IDP/RBAC/catalog; R2 incident response plans; R1 authority gates.

Universality: `UNIVERSAL` for production-impacting self-service.

Exceptions: Read-only self-service can be broader if provenance is clear.

Failure if violated: Any user of platform can perform unsafe production action.

V7 mapping: OMP command, safe deploy pipeline, governed validation owner.

Existing owners: OMP, Authority, SYSTEM_MAP, Runtime, Verification.

Automation impact: Self-service pipelines need auth, evidence, and stop gates.

Autonomy impact: Self-service does not equal autonomous authority.

OMP impact: OMP owns mission routing.

Current Program State impact: CPS shows allowed current action.

Production Maturity impact: Maturity scores self-service governance safety.

Future relevance: Internal platform evolution.

Should V7 adopt: `YES`.

## 16. Learning Laws

### LAW L1: Terminal Outcomes Must Feed Future Decisions

Statement: Every terminal outcome must become learning evidence for future planning, authority, maturity, or automation decisions.

Engineering Reason: Systems that do not learn repeat the same incident.

Why this law exists: Production reality is the only reliable teacher of production autonomy.

Problem it prevents: repeated failed attempts, stale maturity, dead reports.

Evidence from organizations: R1 incident learning; R2 postmortems; R3 self-improving loops.

Universality: `UNIVERSAL`.

Exceptions: None; even intentionally ignored outcomes need classification.

Failure if violated: Automation repeats known bad paths.

V7 mapping: Learning, OMP, Production Maturity, Current Program State.

Existing owners: Learning, Engineering Reports, OMP, Production Maturity.

Automation impact: Pipelines update learning evidence.

Autonomy impact: Autonomy promotion/demotion depends on outcomes.

OMP impact: OMP creates next mission from outcome.

Current Program State impact: CPS records current capability/blocker.

Production Maturity impact: Maturity accepts/blocks advancement.

Future relevance: Continuous improvement and routine operation.

Should V7 adopt: `YES`.

### LAW L2: Negative Evidence Is Capability Evidence

Statement: Stops, rollbacks, unknowns, and blocks are not failures of research; they are evidence about capability boundaries.

Engineering Reason: Safe refusal is part of production capability.

Why this law exists: Large systems need to know what they cannot safely do.

Problem it prevents: ignoring STOP_SAFE, forcing unsafe progress, losing blocker root cause.

Evidence from organizations: R1 fail-closed/safety; R2 HOLD/freeze; R3 analyzer fixtures.

Universality: `UNIVERSAL`.

Exceptions: None; negative evidence still needs classification.

Failure if violated: Same blocker reappears unlearned.

V7 mapping: STOP_SAFE, HOLD, Owner Resolution, Production Maturity BLOCK.

Existing owners: OMP, Runtime, Authority, Production Maturity.

Automation impact: Automation records negative outcomes.

Autonomy impact: Demotion and suspension rely on negative evidence.

OMP impact: OMP converts blockers into missions unless impossible.

Current Program State impact: CPS exposes root cause and required resolution.

Production Maturity impact: Maturity can block capability safely.

Future relevance: Formal capability boundary management.

Should V7 adopt: `YES`.

## 17. Evolution Laws

### LAW EV1: Capability Is Earned, Not Declared

Statement: A capability exists only after implementation, evidence, verification, authority recognition, and required certification prove it.

Engineering Reason: Configuration and documentation can describe intent but cannot prove behavior.

Why this law exists: Autonomous systems fail when declared maturity outruns operational proof.

Problem it prevents: enabling automation by constant, report, or optimism.

Evidence from organizations: R1 progressive certification; R2 maturity models; R3 pipeline evidence.

Universality: `UNIVERSAL`.

Exceptions: Read-only/advisory capability can be declared after tests, but not production mutation capability.

Failure if violated: Production autonomy without production competence.

V7 mapping: Capability Earned, Certification Program, Authority recognition.

Existing owners: OMP, Authority, Production Maturity, Certification.

Automation impact: Automation capability requires evidence.

Autonomy impact: No autonomy without certification.

OMP impact: OMP continues ladder only after terminal evidence.

Current Program State impact: CPS records current capability state.

Production Maturity impact: Maturity accepts only certified capability.

Future relevance: Entire autonomous ladder.

Should V7 adopt: `YES`.

### LAW EV2: Evolution Is Incremental And Reversible Where Possible

Statement: Mature systems evolve by small, observable, reversible steps, not one-shot transformation.

Engineering Reason: Large systems have hidden dependencies.

Why this law exists: Incremental change discovers hidden coupling before broad impact.

Problem it prevents: big-bang rollout, irreversible architecture drift, uncontrolled migration.

Evidence from organizations: R1 canaries and controlled chaos; R2 change management; R3 platform evolution.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Some one-way migrations exist, but require stronger preflight and containment.

Failure if violated: Broad outage and no safe recovery.

V7 mapping: batch ladder, safe deploy, controlled production, OMP phases.

Existing owners: OMP, safe deploy, Authority, Certification.

Automation impact: Pipelines need stages.

Autonomy impact: Autonomy expands in certified stages.

OMP impact: OMP does not skip phases.

Current Program State impact: CPS records current stage.

Production Maturity impact: Maturity consumes staged evidence.

Future relevance: Scale-up to routine operation.

Should V7 adopt: `YES`.

## 18. Human Boundary Laws

### LAW H1: Humans Own Policy, Exceptions, And Architecture Boundaries

Statement: Mature autonomy removes routine toil, not human responsibility for business policy, exceptional risk, and architectural change.

Engineering Reason: Some decisions require value judgment, accountability, or risk acceptance beyond telemetry.

Why this law exists: Automation optimizes within boundaries; humans set boundaries.

Problem it prevents: AI/operator ambiguity, hidden policy expansion, architecture drift.

Evidence from organizations: R2 incident command and overrides; R3 AI boundaries; R1 Authority separation.

Universality: `UNIVERSAL`.

Exceptions: None for business/policy/architecture boundaries.

Failure if violated: System makes unapproved business-risk decisions.

V7 mapping: operator approval, Authority expansion, canonical impossibility, architecture closed by default.

Existing owners: Authority, OMP, human operator, canonical owners.

Automation impact: Automation can prepare packets, not approve policy.

Autonomy impact: Autonomy stays inside certified boundaries.

OMP impact: OMP requests explicit approval where required.

Current Program State impact: CPS records human-required boundary.

Production Maturity impact: Maturity does not override policy.

Future relevance: Delegated autonomy policy.

Should V7 adopt: `YES`.

### LAW H2: Routine Human Touch Is A Bug Or A Deliberate Policy

Statement: If normal repeated operation requires human action, it must be classified as debt or intentionally manual policy.

Engineering Reason: Unexplained manual work cannot scale.

Why this law exists: Large-scale operations need sublinear human load.

Problem it prevents: permanent manual operations and Codex dependency.

Evidence from organizations: R2 toil reduction; R3 workflow debt; R1 analyzer candidates.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Low-frequency, high-judgment, or not-cost-effective work can remain manual.

Failure if violated: System cannot grow without adding proportional operators.

V7 mapping: Automation Audit, Workflow Audit, Codex exit strategy.

Existing owners: OMP, Automation Debt, Workflow Debt.

Automation impact: Creates candidate automation.

Autonomy impact: Removes routine Codex/admin dependency.

OMP impact: OMP classifies debt.

Current Program State impact: CPS exposes debt deltas.

Production Maturity impact: Maturity consumes automation evolution.

Future relevance: Self-improving engineering platform.

Should V7 adopt: `YES`.

## 19. Platform Laws

### LAW P1: Platform Is Product, Not Helpdesk

Statement: A platform must provide maintained self-service capabilities, not become a queue of manual requests.

Engineering Reason: Centralized manual help recreates the bottleneck platform engineering is meant to remove.

Why this law exists: Platform teams scale value only when they productize common workflows.

Problem it prevents: platform as helpdesk, operator bottleneck, inconsistent commands.

Evidence from organizations: R3 IDP/golden path; R2 runbook automation; R1 certification platform needs.

Universality: `LIKELY_UNIVERSAL`.

Exceptions: Early bootstrapping may begin manually, but repeated requests must be classified.

Failure if violated: The platform becomes another manual dependency.

V7 mapping: OMP pipelines, Certification Program, SYSTEM_MAP projection.

Existing owners: OMP, SYSTEM_MAP, Workflow Debt.

Automation impact: Drives pipeline creation.

Autonomy impact: Supports Codex-free operation.

OMP impact: OMP treats repeated requests as workflow debt.

Current Program State impact: CPS records pipeline candidates.

Production Maturity impact: Maturity consumes platform evidence.

Future relevance: Internal developer platform evolution.

Should V7 adopt: `YES`.

### LAW P2: Catalogs Are Lookups, Not Truth Engines

Statement: Service catalogs and maps expose ownership and state pointers; they must not become independent truth or authority.

Engineering Reason: Catalogs improve discovery but can drift from producers.

Why this law exists: Projection layers are useful but dangerous when mistaken for source of truth.

Problem it prevents: SYSTEM_MAP or dashboard acting as authority.

Evidence from organizations: R3 Backstage catalog; R2 ownership mapping; R1 owner-separated evidence.

Universality: `UNIVERSAL`.

Exceptions: A catalog can own catalog metadata, not producer facts.

Failure if violated: stale projection controls production.

V7 mapping: SYSTEM_MAP owner lookup, CPS volatile state, dashboard read-only.

Existing owners: SYSTEM_MAP, CPS, OMP, canonical owners.

Automation impact: Automation discovers owners through catalog but validates at producer.

Autonomy impact: Autonomy cannot execute from catalog projection alone.

OMP impact: OMP uses map for routing, not proof.

Current Program State impact: CPS remains consumer.

Production Maturity impact: Maturity consumes producer evidence.

Future relevance: Service catalog projection.

Should V7 adopt: `YES`.

## 20. Contradictions Between Organizations

| Apparent contradiction | Why it appears contradictory | Abstraction that resolves it | V7 conclusion |
| --- | --- | --- | --- |
| Some systems fail open while others fail closed. | Load balancers may prefer degraded availability; user-routing systems may prefer no unsafe move. | Failure mode depends on action class, user harm, reversibility, and authority. | Classify fail-open/fail-closed per gate; default user movement fail-closed. |
| Some systems automate quickly while others require human approval. | Scope and blast radius differ. | Authority budget and maturity determine automation level. | Automate only inside certified class. |
| Some systems use synthetic tests heavily while V7 requires real production evidence. | Synthetic tests are good for code semantics and readiness, not final production certification. | Evidence class determines allowed conclusion. | Use tests for implementation; use controlled production for certification. |
| Some platforms encourage self-service while V7 guards Authority tightly. | Self-service can be read-only, engineering-only, or production-mutating. | Owner-bounded self-service. | Build self-service pipelines that stop at Authority/Runtime gates. |
| Some organizations use all-at-once global control for network systems. | They own global network infrastructure and operational tooling. | Capability depends on certified owner and observability. | Defer BGP/Anycast-like autonomy until owner exists. |
| AI research shows productivity gains and risks. | Task speed and system reliability are different outcomes. | AI assistance is not authority. | Use AI for assistance/analyzers; reject autonomous production mutation. |

## 21. False Laws

These appear useful but are not universal laws.

| False law | Why it is false | Correct abstraction | V7 stance |
| --- | --- | --- | --- |
| Automate everything. | Some work is policy, judgment, rare, risky, or not cost-effective. | Classify manual work before automating. | `REJECT` |
| Faster recovery is always better. | Fast wrong recovery can harm more users. | Optimize safe verified recovery. | `REJECT` |
| More telemetry always improves autonomy. | Telemetry can be stale, noisy, unactionable, or expensive. | Actionable, owned, fresh evidence improves autonomy. | `REJECT` |
| A successful dry run proves production capability. | Dry run omits real mutation and verification. | Dry run proves preparation only. | `REJECT` |
| A good score can replace raw evidence. | Opaque scores hide first divergence. | Score can summarize inspectable evidence. | `REJECT` |
| A platform portal creates automation. | UI without owner-backed pipeline is cosmetic. | Pipelines create automation; portals expose it. | `REJECT` |
| AI output reduces need for verification. | AI may hallucinate or omit context. | AI output requires stronger verification. | `REJECT` |

## 22. Practices That Depend On Scale

| Practice | Scale dependency | V7 classification |
| --- | --- | --- |
| Multi-perspective global health | More useful when users and probes span regions. | `LATER` |
| BGP/Anycast autonomy | Requires network-scale control and observability. | `LATER / RESEARCH_MORE` |
| Full internal developer portal | Valuable after many owner-backed pipelines exist. | `LATER` |
| Automated canary statistical judges | Needs stable metrics and enough samples. | `LATER` |
| Engineering intelligence dashboards | Needs reliable data pipeline and repeated workflow volume. | `LATER` |
| Chaos experiments | Needs controlled production pool and restoration maturity. | `LATER` |

## 23. Practices That Depend On Organization Size

| Practice | Organization-size dependency | V7 classification |
| --- | --- | --- |
| Incident command role separation | More formal at larger operator teams. | `LATER`, but boundary vocabulary useful now. |
| Full platform product team | Useful when many engineers consume shared workflows. | `LATER` |
| SRE curriculum | Useful when onboarding many operators/engineers. | `LATER` |
| Domain/gateway ownership model | Useful when service count and team count grow. | `RESEARCH_MORE` |
| Communities of practice | Useful when many teams repeat related work. | `LATER` |

## 24. Practices That Depend On Technology

| Practice | Technology dependency | V7 stance |
| --- | --- | --- |
| Kubernetes liveness/readiness/startup probes | Container orchestration. | Adopt taxonomy, not implementation. |
| BGP graceful shutdown | Network routing control. | Adopt drain idea; defer network control. |
| CDN backend directors | CDN/VCL edge platform. | Adopt pool selection vocabulary only. |
| DERP relay fallback | Overlay network relay infrastructure. | Defer as future capability. |
| GitHub Actions workflow syntax | GitHub CI/CD. | Use if helpful, not as V7 law. |
| Backstage catalog entity schema | Developer portal implementation. | Adopt ownership model concept, not schema as law. |

## 25. Laws V7 Should Adopt

Adopt as constitutional laws:

1. Reality Precedes Authority.
2. Detection Is Not Diagnosis.
3. Decision Is Not Execution.
4. Verification Completes Mutation.
5. Rollback Or Closure Is Mandatory.
6. Health Is A Matrix.
7. Routing Identity Must Be Continuous.
8. Failover Scope Must Follow The Incident.
9. Retry Is A Budgeted Semantic Attempt.
10. Authority Bounds Blast Radius.
11. Fail Mode Must Be Classified.
12. Synthetic Evidence Cannot Certify Reality.
13. Unknown Is Not Fail And Not Pass.
14. Repeated Manual Work Is Debt Until Classified.
15. Reports Preserve Evidence, Not Authority.
16. Durable Truth Has One Owner.
17. Automation Must Be Suspendable.
18. Capability Is Earned, Not Declared.
19. Humans Own Policy, Exceptions, And Architecture Boundaries.
20. Catalogs Are Lookups, Not Truth Engines.

## 26. Laws V7 Should Reject

Reject as laws:

1. Automate everything.
2. Fastest action is best action.
3. Timer equals wake authority.
4. AI output equals truth.
5. Report equals roadmap.
6. Score equals evidence.
7. Dry run equals production proof.
8. Portal equals platform.
9. Error budget equals Runtime permission.
10. Owner block equals terminal explanation.

## 27. Laws V7 Should Defer

Defer as future capability laws:

1. Multi-perspective health is mandatory for every decision.
2. Automated canary judges may promote production changes.
3. Full self-service IDP is required.
4. AI agents may implement and deploy without routine review.
5. Network-level global traffic control should be autonomous.
6. Controlled chaos can run routinely.
7. Direct customer telemetry is mandatory for current governed L3 certification.

## 28. Candidate Laws For V7_AUTONOMOUS_OPERATING_SYSTEM.md

Do not modify `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` in this mission.

Candidate laws for later owner-approved synchronization:

1. Reality Precedes Authority Law.
2. Detection Is Not Diagnosis Law.
3. Decision Is Not Execution Law.
4. Verification Completes Mutation Law.
5. Rollback Or Closure Law.
6. Health Evidence Matrix Law.
7. Execution Identity Continuity Law.
8. Incident Scope Continuity Law.
9. Semantic Retry Budget Law.
10. Fail Mode Classification Law.
11. Unknown Evidence Classification Law.
12. Automation Suspension Law.
13. Analyzer Backtesting Law.
14. Capability Earned Law.
15. Single Durable Truth Owner Law.
16. Human Boundary Law.
17. Owner-Bounded Self-Service Law.
18. Catalog Projection Law.

## 29. Open Questions

1. Which of these laws should be promoted first into `V7_AUTONOMOUS_OPERATING_SYSTEM.md`?
2. Should `Health Evidence Matrix Law` become a standalone canonical schema or remain owner-specific?
3. What exact threshold makes analyzer backtesting sufficient for advisory use?
4. What exact threshold makes analyzer backtesting sufficient for blocking use?
5. Which laws belong in AOS versus OMP versus Runtime Model versus Controlled Production Certification Program?
6. Should `Unknown Is Not Fail And Not Pass` be formalized in Verification or in Runtime Model?
7. Which laws should become tests against existing owners?
8. Should V7 create a law-to-owner matrix generated from SYSTEM_MAP?
9. Should CPS expose law violation state for current missions?
10. Which laws are already fully canonical and only need references, not new text?

## 30. Final Engineering Verdict

Verdict:

```text
R4_MASTER_AUTONOMOUS_SYSTEM_LAWS_CREATED
```

Number of laws extracted:

```text
35
```

Organization-independent laws:

```text
35
```

Universal laws:

```text
27
```

Likely universal laws:

```text
8
```

Organization-specific findings:

```text
0 promoted to law
```

Technology-specific findings:

```text
0 promoted to universal law
```

Strongest universal law:

```text
Reality Precedes Authority
```

Weakest proposed law:

```text
Paved Roads Must Be Easier Than Ad Hoc Paths
```

Reason weakest:

It is strongly supported for engineering organizations and platforms, but its exact force depends on organization size, workflow frequency, and cost. It remains `LIKELY_UNIVERSAL`, not `UNIVERSAL`.

Final conclusion:

```text
The constitution of autonomous production systems is not automation.
It is evidence-bounded, authority-bounded, identity-preserving, verified, rollback-capable, learning-driven autonomy.
```

No runtime, Planner, Authority, OMP, production, deployment, or canonical document changes were made.
