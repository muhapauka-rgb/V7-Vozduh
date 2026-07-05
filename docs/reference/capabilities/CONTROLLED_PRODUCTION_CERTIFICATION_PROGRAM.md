# Controlled Production Certification Program

Status: `CANONICAL PROGRAM DOCUMENT`
Mode: `DOCUMENTATION ONLY`
Runtime impact: `NONE`
Authority impact: `NONE`
Production impact: `NONE`
Users moved: `NO`

Owner: OMP / Production Maturity / existing V7 capability certification owners.

This document defines the controlled production certification program for governed V7 autonomous evacuation. It does not create a Runtime, Planner, Authority, Restore Barrier owner, Wake owner, execution path, truth source, or automation system.

The program certifies the adaptive governed evacuation ladder:

```text
1 -> 5 -> 10 -> 25 -> 50 -> FULL_INCIDENT
```

All certification must use existing V7 owners:

```text
Observation / Wake
  -> Incident
  -> Planner
  -> Authority
  -> Approved Plan Lock
  -> Restore Barrier
  -> Runtime Apply
  -> Verification
  -> Rollback / No-Rollback Closure
  -> Learning / Feedback
  -> Production Restoration
  -> Capability Earned
  -> Consumer Synchronization
```

## 1. Executive Summary

V7 must prove that governed automation can safely evacuate users from a failed production source at increasing authorized batch sizes. Waiting for random production incidents with exactly 5, 10, 25, or 50 affected users is operationally inefficient and slows certification.

The solution is controlled production certification groups. V7 uses real production owners, real authority, real restore barriers, real runtime apply, real verification, real rollback, and real learning, but applies them to dedicated certification users rather than ordinary paying users. This produces real production evidence without turning customers into experiments and without weakening safety gates.

## 2. Scope

In scope:

- L3 governed emergency evacuation.
- Adaptive batch ladder certification.
- Dedicated certification users and groups.
- Controlled failed-source incidents.
- Controlled production environment certification.
- Temporary certification incidents.
- Production restoration after certification.
- Real incident preemption.
- Batch Runtime Apply through existing owners.
- Per-user verification.
- Per-user rollback or no-rollback closure.
- Promotion, demotion, and hold decisions.
- Learning, feedback, OMP, and Production Maturity evidence.

Out of scope:

- Sandbox certification.
- Simulation certification.
- Fake production.
- Isolated test environment certification as production proof.
- New Runtime.
- New Planner.
- New Authority.
- New Restore Barrier owner.
- New Wake owner.
- Broad automation.
- Unbounded movement.
- Cross-incident batching.
- Ordinary customer experiments.
- Synthetic production success.
- Mock-only or sandbox-only certification.

## 3. Definitions

Controlled Production Certification: A governed production certification run using real V7 owners and real production execution contracts against dedicated certification users.

Controlled Production Environment: Real production environment used for certification with real V7 owners and temporary controlled certification users/incidents. It is not a sandbox, simulation, mock runtime, fake production, or isolated test environment.

Certification Group: A named set of dedicated users prepared for certification at a specific stage or partition of the ladder.

Certification User: A non-paying, internal, or otherwise explicitly designated user identity that is safe to move and rollback during certification.

Certification Pool: The set of real production Certification Users and Certification Groups maintained by existing user, registry, policy, OMP, and Production Maturity owners for controlled production certification.

Certification Pool Sufficiency: The condition that the Certification Pool contains enough eligible Certification Users to execute the target certification stage without using ordinary customers or synthetic identities.

Certification Pool Decision: Mandatory decision made before a certification stage enters HOLD because Certification Users are insufficient. It determines whether the pool is already sufficient, can be legally expanded, is blocked by policy, is blocked by missing implementation, or is canonically impossible.

Controlled Incident: A real V7 incident opened through legal production mechanisms for a controlled failed source and certification users.

Temporary Certification Incident: A real controlled incident used only for certification and removed during cleanup after evidence is preserved.

Incident Source: The failed production source that opened the L3 incident. It remains the source identity for continuation until recovery, containment, canonical impossibility, or no affected users remain.

Authority Budget: The current maximum user count permitted by existing Authority and governance state for a governed execution cycle.

Batch Stage: A certification step with a specific authorized maximum user count.

Batch Ladder: The evidence-based sequence of increasing authority scopes: CANARY, SMALL_BATCH, MEDIUM_BATCH, LARGE_BATCH, XLARGE_BATCH, FULL_INCIDENT.

FULL_INCIDENT: All remaining affected users assigned to the same active failed-source incident after prior stages are certified and Authority explicitly allows this scope.

Promotion: A governance decision that permits a higher batch stage after the prior stage produced complete successful evidence.

Demotion: A governance decision that reduces or freezes authority after failure, missing evidence, rollback, instability, or policy risk.

Partial Success: A batch outcome where at least one selected user succeeds and at least one selected user fails apply, verification, or rollback/no-rollback closure.

Rollback Closure: The completed decision and evidence record showing rollback was either not required, completed successfully, failed, or containment was applied.

Certification Evidence: Persisted production evidence proving what was selected, authorized, applied, verified, rolled back or closed, learned, restored, earned as capability, and synchronized to consumers.

Controlled Evidence Generation: Legal creation of missing certification evidence through the Controlled Production Environment, Certification Groups, Controlled Incidents, Authority, and existing governed production owners.

Certification Evidence Decision: Mandatory decision made before a certification stage enters HOLD because required evidence is unavailable. It determines whether sufficient real production evidence already exists, whether Controlled Production can legally generate it, whether safety owners forbid it, whether implementation is missing, or whether canonical impossibility is proven.

Certification History: Append-only historical record of every certification attempt and its evidence, stored through the existing Engineering Report lifecycle and consumed by OMP / Production Maturity.

Certification Coverage: Current proven status of each certification capability and stage, represented as a V7 Certification Passport view rather than a separate truth source.

V7 Certification Passport: Production Maturity / Current Program State view over Certification History showing what V7 has actually proven in production. It is not a standalone owner or truth source.

Capability Earned: Rule that a capability becomes usable only after governed production certification and Authority recognition, not because a developer changed a constant or configuration value.

Capability Producers: Existing production owners whose successful completion creates certified capability evidence: Observation, Wake, Incident, Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime Apply, Verification, Rollback / No-Rollback, Production Restoration, and any existing safety owner required by the stage.

Capability Consumers: Existing evidence, governance, and projection owners that consume already-produced capability evidence: Certification History, Passport, OMP, Production Maturity, Current Program State, Coverage Matrix, Engineering Reports, Dashboard projections, Automation Debt views, and Workflow Debt views.

Consumer Synchronization: Post-capability synchronization of consumer views, reports, history, maturity, passport, dashboard, and current-state projections with already-earned production evidence.

Synchronization Debt: A consumer synchronization task that has not yet synchronized with already-earned capability evidence.

Capability Evolution: Evidence-driven progression from collected evidence to proven stability, earned capability, Authority recognition, and production use.

Continuous Automation Evolution: Rule that every certification execution also audits manual work and creates evidence for reducing future operator and engineering effort when automation is justified.

Certification Mission: Explicit mission definition for one certification run, reusing Execution Mission Protocol mission discipline and this program's certification contracts.

Automation Gap: A manual action encountered during certification that must be classified as already automated, intentionally manual, not automatable, or a candidate for automation through existing owners.

Automation Debt: Any manual action that has not yet reached a terminal Automation Audit classification.

Automation Candidate: Owner-mapped record describing a justified future automation improvement, its current manual owner, desired owner, safety impact, value, cost, priority, and required certification before use.

Manual Workflow: A sequence of manual actions performed to reach one engineering objective.

Workflow Debt: A repeated manual workflow that has not yet reached a terminal Workflow Audit classification.

Pipeline Candidate: Owner-mapped record describing a justified future governed pipeline that can replace unnecessary manual workflow orchestration.

Regression Certification: Deterministic re-certification required after changes to owners, contracts, evidence, or safety gates.

Blast Radius: The maximum number of users permitted to be affected by one governed certification execution under the current Authority Budget.

Owner Mapping: The bridge from this program document to existing implementation, evidence, OMP, Current Program State, and Production Maturity owners.

Blocking Owner: Existing owner that stops certification execution, evidence generation, pool expansion, controlled production, producer execution, recovery, restoration, or consumer synchronization.

Owner Resolution: Mandatory investigation of a Blocking Owner until the block is classified as policy, missing implementation, missing invocation, implementation defect, or canonical impossibility.

Reality Preservation: Certification law requiring real production execution and forbidding fake Planner, Runtime, Verification, Rollback, Learning, Authority, Restore Barrier, Incident, or evidence success.

Production Restoration: Cleanup contract requiring temporary certification state to be removed and logical production topology restored after certification.

Real Incident Preemption: Rule that real customer recovery takes priority over certification when a real production incident appears during certification.

## 4. Certification Philosophy

The numbers are checkpoints, not the goal. The goal is to prove safe operation under any authorized Authority Budget while preserving the same governed execution chain.

Certification must demonstrate that V7 can evacuate users when a source fails, constrain execution to the failed incident, verify every selected user, rollback or contain failures, learn from outcomes, and stop safely when evidence or authority is insufficient.

No stage may be certified by mocks, synthetic success, report-only claims, or planner-only dry runs. Dry runs may prepare or explain, but only real controlled production execution can certify.

The certification target is the Authority Budget capability, not any single numeric value. The current production ladder uses 1, 5, 10, 25, 50, and FULL_INCIDENT as the canonical checkpoints, but the underlying rule is future-proof: V7 must prove it can safely execute any future authorized budget while preserving the same owners, identity, verification, rollback, and learning contracts.

## 5. Capability Earned Law

A capability is never enabled because a developer changes a constant.

A capability is enabled only after the system has earned it through governed production certification and Authority approval.

Examples:

- V7 does not receive `SMALL_BATCH = 5` because someone configured it.
- V7 earns `SMALL_BATCH` after proving it through governed production certification and Authority recognition.
- The same rule applies to every future Authority Budget.

Certification creates capability. Configuration alone never creates capability.

Numeric values are checkpoints. The capability is the certified behavior: the system can legally select, authorize, apply, verify, rollback or close, learn, restore production state, and preserve evidence at that Authority Budget.

## 5.1 Execution Priority Law

Execution must always prioritize real capability advancement.

Documentation exists to synchronize reality.

Reality never waits for documentation.

Capability producers must never be blocked by documentation consumers unless an existing safety owner explicitly proves that synchronization is required to preserve Reality First, Authority, Verification, Rollback, Production Restoration, or another existing safety contract.

Canonical execution order:

```text
Reality
  -> Capability Producers
  -> Capability Earned
  -> Consumer Synchronization
  -> Authority Recognition
  -> Next Certification Mission
```

This order is mandatory.

### Capability Producers

Capability Producers are the owners whose successful completion creates a new certified capability.

At minimum:

- Observation.
- Wake.
- Incident.
- Planner.
- Authority.
- Approved Plan Lock.
- Restore Barrier.
- Runtime Apply.
- Verification.
- Rollback / No-Rollback.
- Production Restoration.

When these owners successfully complete their contracts, Capability Earned occurs.

### Capability Consumers

Capability Consumers consume capability. They do not create capability.

Consumers include:

- Certification History.
- Passport.
- OMP.
- Production Maturity.
- Current Program State.
- Coverage Matrix.
- Engineering Reports.
- Dashboard projections.
- Automation Debt views.
- Workflow Debt views.

### Consumer Synchronization

Consumer synchronization should normally execute automatically after Capability Earned.

If synchronization is temporarily incomplete, the system must determine:

```text
Does this prevent safe capability progression?
```

If the answer is `NO`, record Synchronization Debt and continue execution according to Authority and safety rules.

If the answer is `YES`, identify the exact existing safety owner requiring synchronization and block only for that safety reason.

Documentation alone is never a sufficient blocker.

### Synchronization Debt

If a consumer has not yet synchronized with an already-earned capability, classify it as Synchronization Debt.

Every Synchronization Debt must terminate as exactly one of:

- `SYNCHRONIZED`.
- `INTENTIONALLY_DELAYED`.
- `BLOCKED_BY_SAFETY_OWNER_REQUIRES_OWNER_RESOLUTION`.
- `CANONICAL_IMPOSSIBILITY`.

No synchronization task may remain unexplained.

### Execution Safety Rule

Consumer synchronization may block progression only when an existing safety owner proves that synchronization is required to preserve:

- Reality First.
- Authority.
- Verification.
- Rollback.
- Production Restoration.
- Another existing safety contract.

Otherwise synchronization is post-capability work.

## 6. Capability Evolution Model

The capability evolution model is:

```text
System
  -> collects evidence
  -> proves stability
  -> earns capability
  -> Authority recognizes capability
  -> Production may use capability
```

Certification proves capability, not merely numeric batch sizes.

The batch ladder values are certification checkpoints. The true target is evidence that the governed production system can operate safely at the corresponding Authority Budget while preserving all producers, safety gates, verification, rollback/no-rollback closure, Production Restoration, and post-capability consumer synchronization.

Capability Evolution reuses OMP, Authority, Production Maturity, Current Program State, Engineering Reports, and existing capability owners. It does not create a separate promotion engine.

Capability Evolution follows the Execution Priority Law. Production capability is produced by Capability Producers. OMP, Production Maturity, Current Program State, Passport, Engineering Reports, and Dashboard projections synchronize after the capability is earned unless an existing safety owner proves synchronization is a safety prerequisite.

## 6.1 Continuous Automation Evolution

Every certification execution must also audit automation.

The certification mission has two simultaneous goals:

1. Certify the requested capability.
2. Reduce future manual work inside V7 when automation is justified and safe.

Every certification run is therefore both Capability Certification and Automation Evolution.

Continuous Automation Evolution reuses OMP, Production Maturity, Execution Mission Protocol, Execution Completion Protocol, SYSTEM_MAP, Current Program State, Reality First, Engineering Reports, and existing V7 owners. It does not create a separate automation program, automation owner, Runtime, Planner, Authority, truth source, or execution path.

### Automation Audit Loop

Every manual action automatically enters this loop:

```text
Manual Action
  -> Automation Audit
  -> Root Cause
  -> Existing Owner Investigation
  -> Automation Decision
  -> Automation Candidate, if justified
  -> Implementation
  -> Certification
  -> Capability Earned
  -> Automation Gap Closed
```

No manual action may bypass this loop.

The manual action itself is never terminal. It is the beginning of an automation investigation.

### Automation Gap Law

Every manual action performed by Codex during certification must immediately trigger the question:

```text
Why is this manual?
```

The answer must receive exactly one classification:

| Classification | Meaning |
| --- | --- |
| `ALREADY_AUTOMATED` | Existing owner already automates the action; the manual step used the wrong path or the automation was not invoked. |
| `CANNOT_BE_AUTOMATED` | Automation would contradict Reality First, safety, authority, rollback, verification, or production constraints. |
| `SHOULD_BE_AUTOMATED` | Automation is valuable, safe in principle, and owner-mappable through existing V7 owners. |
| `AUTOMATION_EXISTS_UNUSED` | Automation exists but the certification path did not consume it. |
| `BLOCKED_BY_MISSING_CAPABILITY` | Automation is justified but depends on a not-yet-certified capability. |
| `BLOCKED_BY_SAFETY` | Automation is valuable but current safety evidence is insufficient. |
| `BLOCKED_BY_ARCHITECTURE` | Existing owners cannot currently own the action; OMP and SYSTEM_MAP must prove whether extension is needed. |
| `BLOCKED_BY_MISSING_OWNER` | No existing owner is currently mapped; SYSTEM_MAP / Owner Mapping must resolve ownership before implementation. |
| `INTENTIONALLY_MANUAL` | The action is deliberately manual because policy, authority, risk, or economics requires it. |

No manual action may remain unexplained.

Every unexplained manual action is Automation Debt.

### Automation Investigation

When a manual action is encountered, Codex must not simply perform it and move on. Codex must investigate:

- Why does this require a human now?
- Which owner currently performs it?
- Could an existing owner perform it?
- Would automation violate Reality First, safety, authority, verification, rollback, or Production Restoration?
- Would automation reduce engineering effort?
- Would automation reduce operator effort?
- Would automation reduce production risk?
- Would automation increase production risk?
- Would automation improve production behavior?
- Would automation increase unacceptable risk?
- Would automation provide meaningful long-term value?

The investigation result becomes engineering evidence inside the certification report.

### Automation Decision

If automation is justified, the certification report must create an Automation Candidate.

If automation is not justified, the report must record the reason and classify the manual action as intentionally manual, not automatable, blocked, or already automated.

No manual step may remain unexplained.

### Automation Candidate Contract

Every Automation Candidate must contain:

| Field | Required meaning |
| --- | --- |
| Manual Action | Exact manual action performed. |
| Current Owner | Existing owner or operator currently responsible. |
| Desired Owner | Existing owner that should own automation if justified. |
| Reason Manual Today | Why the action was manual during this run. |
| Reason Automation Valuable | Engineering, operator, production, or safety value. |
| Safety Impact | Safety improvement, no-change, or risk introduced. |
| Frequency | How often the action appears across certification or production operation. |
| Engineering Cost | Estimated implementation and maintenance cost. |
| Operator Benefit | Expected operator effort reduction. |
| Production Benefit | Expected production reliability, speed, or quality improvement. |
| Priority | OMP / Production Maturity priority recommendation. |
| Certification Required | Certification stage or regression required after implementation. |

Automation Candidates are evidence records and OMP inputs. They are not authority grants, production enablement, or implementation approval.

### Automation Completion Law

Automation work follows the same completion philosophy as V7:

```text
Automation Gap
  -> Owner Mapping
  -> Implementation
  -> Certification
  -> Capability Earned
  -> Automation Gap Closed
```

No Automation Candidate may terminate without one of these terminal states:

- `AUTOMATED`.
- `INTENTIONALLY_MANUAL`.
- `CANONICAL_IMPOSSIBILITY`.
- `NOT_COST_EFFECTIVE`.
- `BLOCKED_BY_FUTURE_CAPABILITY`.

### Automation Debt Law

Every unexplained manual action is Automation Debt.

Automation Debt must always terminate as exactly one of:

- `AUTOMATED`.
- `INTENTIONALLY_MANUAL`.
- `BLOCKED_BY_FUTURE_CAPABILITY`.
- `NOT_COST_EFFECTIVE`.
- `CANONICAL_IMPOSSIBILITY`.

There may never exist:

```text
UNCLASSIFIED_MANUAL_WORK
```

Blocked, unsafe, missing-owner, missing-capability, and unused-automation classifications are investigation states. They must be reduced to one terminal Automation Debt state by OMP / Production Maturity / SYSTEM_MAP ownership review.

### Automation Debt Metric

Every certification mission must report:

| Metric | Meaning |
| --- | --- |
| Current Automation Debt | Manual actions still open at the end of the mission. |
| Automation Debt Closed | Manual actions that reached a terminal Automation Debt state. |
| Automation Debt Created | Manual actions newly discovered during the mission. |
| Automation Debt Remaining | Manual actions not yet terminal after the mission. |
| Trend | Improving, flat, or worsening compared with prior certification evidence. |

The metric reuses Engineering Reports for evidence, OMP for next-action scheduling, Production Maturity for maturity impact, and Current Program State / Passport views for current status. It does not create a new metric owner.

### Every Project Has Two Outputs

Every certification mission must produce:

1. Capability Evolution.
2. Automation Evolution.

If capability is certified but unnecessary manual work remains unclassified, the project is incomplete. It becomes complete only when every manual action has either been automated or formally classified into a terminal Automation Debt state.

### Workflow Evolution Law

The system must investigate not only manual actions. It must also investigate manual workflows.

A workflow is a sequence of manual actions performed to reach one engineering objective. The workflow itself becomes an object of investigation.

Workflow Evolution is the next layer of Continuous Automation Evolution. It reuses OMP, Execution Mission Protocol, Execution Completion Protocol, SYSTEM_MAP, Current Program State, Production Maturity, Reality First, Automation Evolution, Owner Mapping, Engineering Reports, and existing owners. It does not create a new orchestration program, pipeline owner, Runtime, Planner, Authority, OMP, truth source, or execution path.

### Workflow Audit Loop

Every manual workflow automatically enters this loop:

```text
Workflow
  -> Workflow Investigation
  -> Root Cause
  -> Existing Owner Investigation
  -> Pipeline Decision
  -> Pipeline Candidate
  -> Implementation
  -> Certification
  -> Capability Earned
  -> Workflow Closed
```

No manual workflow may bypass this loop.

### Workflow Root Cause Analysis

Whenever Codex executes multiple manual actions toward one goal, Codex must automatically ask:

- Why does this workflow exist?
- Why are multiple manual commands required?
- Can one existing owner execute the whole workflow?
- Can multiple owners already cooperate automatically?
- Does this workflow represent an Orchestration Gap?
- Would a single pipeline be safer?
- Would a single pipeline reduce engineering effort?
- Would a single pipeline reduce operator effort?
- Would a single pipeline improve production reliability?
- Would a single pipeline increase unacceptable risk?

This analysis becomes certification evidence.

### Pipeline Candidate Contract

Every Pipeline Candidate must contain:

| Field | Required meaning |
| --- | --- |
| Workflow | Engineering objective and workflow name. |
| Current Manual Steps | Ordered manual actions currently required. |
| Current Owners | Existing owners or operators for each step. |
| Desired Owner | Existing owner that should own the governed pipeline if justified. |
| Desired Pipeline | Proposed owner-coordinated workflow path. |
| Reason Workflow Exists | Why the workflow is manual today. |
| Reason Pipeline Valuable | Engineering, operator, production, or reliability value. |
| Safety Impact | Safety improvement, no-change, or risk introduced. |
| Engineering Cost | Estimated implementation and maintenance cost. |
| Operator Benefit | Expected operator effort reduction. |
| Production Benefit | Expected reliability, speed, or quality improvement. |
| Priority | OMP / Production Maturity priority recommendation. |
| Certification Required | Certification stage or regression required after implementation. |
| Relationship to Automation Candidates | Linked manual actions and Automation Candidates inside the workflow. |

Pipeline Candidates are evidence records and OMP inputs. They are not authority grants, production enablement, implementation approval, or a new pipeline owner.

### Workflow Debt Law

A repeated manual workflow is Workflow Debt.

Workflow Debt must terminate as exactly one of:

- `PIPELINE_IMPLEMENTED`.
- `INTENTIONALLY_MANUAL`.
- `CANONICAL_IMPOSSIBILITY`.
- `NOT_COST_EFFECTIVE`.
- `BLOCKED_BY_FUTURE_CAPABILITY`.

No workflow may remain unexplained.

### Command Minimization

Whenever Codex executes:

```text
A
  -> B
  -> C
  -> D
```

the certification mission must investigate:

- Why are there four commands?
- Why is there not one command?
- Why is there not one owner?
- Why is there not one governed pipeline?

The goal is not simply to automate commands. The goal is to eliminate unnecessary manual orchestration.

### Automation And Workflow Outputs

Every certification mission improves both:

1. Automation.
2. Workflow Orchestration.

Capability certification should continuously reduce:

- manual actions;
- manual workflows;
- manual orchestration.

Every certification mission should leave the engineering system simpler than before unless Reality First, safety, Authority, cost, or canonical impossibility proves that the workflow must remain manual.

### Automation Is Not A Goal

Automation exists only when it improves V7.

Examples:

| Automation idea | Rule |
| --- | --- |
| Automatically creating fake failures | Forbidden. |
| Automatically degrading production channels | Normally not justified unless legal controlled production owners and authority explicitly allow it for certification users. |
| Automatically executing governed Runtime after legal Wake | Expected when inside certified authority and live gates. |
| Automatically continuing incident evacuation | Expected when incident continuity and authority are certified. |
| Automatically creating certification reports | Expected when existing report owners can preserve accurate evidence. |
| Automatically updating Passport view | Expected when Production Maturity / Current Program State owners can consume Certification History safely. |

Automation must always pass the same Reality First, safety, authority, verification, rollback, Production Restoration, and evidence rules as capability certification.

### Final Automation Review Question

At the end of every certification mission, the report must ask:

```text
What manual work still exists?
```

Every answer must become either:

- Automation Candidate; or
- Intentionally Manual / not automatable / blocked classification with evidence.

No unanswered manual work may remain.

## 7. Certification Mission Contract

Every certification run is a Mission.

Certification Missions reuse the Execution Mission Protocol mission discipline. This document specializes that discipline for controlled production certification; it does not create a new mission owner or execution engine.

No certification may execute without an explicit Mission definition.

Every Certification Mission must define:

| Field | Required meaning |
| --- | --- |
| Mission Name | Human-readable mission identity. |
| Mission Goal | Capability or stage outcome being certified. |
| Target Capability | Capability to be earned, such as CANARY, SMALL_BATCH, MEDIUM_BATCH, LARGE_BATCH, XLARGE_BATCH, or FULL_INCIDENT. |
| Authority Budget | Current authorized user budget for the run. |
| Entry Criteria | Readiness checklist and stage entry criteria. |
| Evidence Source Decision | `ALREADY_HAVE_REAL_EVIDENCE`, `CONTROLLED_PRODUCTION_SELECTED`, `OWNER_RESOLUTION_REQUIRED`, `CANONICAL_IMPOSSIBILITY`, or `MISSING_IMPLEMENTATION`. |
| Success Criteria | Stage exit criteria, producer completion, verification, rollback/no-rollback closure, Production Restoration, evidence preservation, and consumer synchronization requirements. |
| Failure Criteria | Stage fail criteria, blocker conditions, identity violations, verification failures, rollback failures, restoration failures, and preemption conditions. |
| Abort Criteria | Conditions that require immediate pause, hold, containment, or operator decision. |
| Evidence Required | Required production evidence and Engineering Report artifacts. |
| Cleanup Required | Production Restoration requirements. |
| Promotion Decision | PROMOTED, HOLD, DEMOTED, FROZEN, REJECTED, or NOT_APPLICABLE. |
| Automation Gap Review | Manual actions, classifications, Automation Candidates, and intentionally manual decisions. |
| Automation Debt Metrics | Current, created, closed, remaining, and trend values. |
| Workflow Audit Review | Manual workflows, root causes, Pipeline Candidates, and terminal Workflow Debt classifications. |
| Workflow Debt Metrics | Current, created, closed, remaining, and trend values. |
| Owner Resolution Review | Blocking Owner, Owner Investigation, terminal classification, Required Resolution, and reason no further investigation is necessary. |

Reports are mission evidence. Reports do not complete the Mission unless the Mission reaches PASS with complete evidence or a canonical terminal state defined by this program.

## 8. Reality Creation Law

Certification must never wait for reality.

Certification must be able to create controlled real production conditions using the existing production system.

Certification users are temporarily placed into controlled production conditions. The governed production system must react naturally. No production owner may know that certification is occurring as a special execution mode. Only certification users participate.

The production execution chain must remain identical to ordinary customer recovery:

```text
Observation / Wake
  -> Incident
  -> Planner
  -> Authority
  -> Approved Plan Lock
  -> Restore Barrier
  -> Runtime Apply
  -> Verification
  -> Rollback / No-Rollback Closure
  -> Learning / Feedback
  -> Production Restoration
  -> Capability Earned
  -> Consumer Synchronization
```

Reality Creation does not mean fake incidents, fake production, synthetic success, or bypassed owners. It means controlled real production conditions created through existing legal owners and applied only to certification users.

## 8.1 Controlled Evidence Generation Law

Certification must not depend on random production conditions.

Whenever a certification stage requires production evidence that current production reality does not already provide, the system must determine whether the missing evidence can be legally produced through Controlled Production Certification.

If Controlled Production can legally create the required evidence while preserving Reality First, Authority, Restore Barrier, Runtime, Verification, Rollback, Learning, Production Restoration, OMP, and Production Maturity, then Controlled Production becomes the default execution path.

Waiting for a random production incident is no longer the default strategy. Waiting is permitted only after the Certification Evidence Decision proves that Controlled Production is forbidden, impossible, blocked by missing implementation, or explicitly rejected by an existing safety owner.

Controlled Production is scheduled evidence. Random production is opportunistic evidence. Both are valid only when they use real production owners and preserved evidence.

### Certification Evidence Decision

Whenever the next certification stage cannot begin because required evidence is unavailable, execute this decision chain:

```text
Required Evidence
  -> Does real production already provide it?
  -> YES: Use real production.
  -> NO: Can Controlled Production legally generate it?
  -> YES: Prepare Controlled Certification Environment.
  -> Execute Certification Mission.
  -> Restore Production.
  -> Continue Certification Program.
  -> NO: Run Owner Resolution for any Blocking Owner, then enter HOLD only with a terminal Owner Resolution classification, or CANONICAL_IMPOSSIBILITY when no legal path exists.
```

Certification evidence source decisions:

| Situation | Required action |
| --- | --- |
| Real production already provides sufficient evidence | Use it. |
| Real production is insufficient and Controlled Production is possible | Create a Controlled Certification Mission through existing owners. |
| Controlled Production is forbidden by safety owners | Run Owner Resolution for the Blocking Owner, then enter `HOLD` only with the terminal Owner Resolution classification. |
| Controlled Production is impossible through current architecture | Enter `CANONICAL_IMPOSSIBILITY`. |
| Controlled Production requires missing implementation | Create an implementation task through existing owners and enter `HOLD` with `MISSING_IMPLEMENTATION`. |

Every HOLD caused by missing certification evidence must answer:

`Why is Controlled Production not being used?`

The answer must terminate as exactly one of:

- `ALREADY_HAVE_REAL_EVIDENCE`;
- `CONTROLLED_PRODUCTION_SELECTED`;
- `OWNER_RESOLUTION_REQUIRED`;
- `CANONICAL_IMPOSSIBILITY`;
- `MISSING_IMPLEMENTATION`.

No HOLD may exist only because the system is waiting for an unknown future incident.

## 8.1.1 Owner Resolution Law

Whenever certification execution is blocked by an existing owner, the blocking owner is not the terminal explanation.

The certification program must continue investigation until the blocking owner itself is classified.

The goal is to identify the real terminal root cause and the next concrete engineering action, policy decision, or canonical impossibility.

This law reuses Execution Completion Protocol, Reality First, OMP, Production Maturity, SYSTEM_MAP, Owner Mapping, Certification Recovery, Certification Evidence Decision, Certification Pool Decision, Engineering Reports, and Current Program State. It does not create a new owner, Runtime, Planner, Authority, Restore Barrier owner, Wake owner, truth source, execution path, or certification system.

Owner Resolution loop:

```text
Execution Block
  -> Blocking Owner
  -> Owner Investigation
  -> Root Cause
  -> Resolution Classification
  -> Implementation
     or Policy Decision
     or Canonical Impossibility
  -> Continue Certification Program
```

### Owner Investigation

Whenever an owner blocks execution, the certification mission must automatically determine:

- Why did this owner block?
- Is this expected policy?
- Is implementation missing?
- Is owner invocation missing?
- Is the implementation defective?
- Is the behavior intentionally forbidden?
- Is the behavior canonically impossible?

The investigation continues until exactly one terminal classification exists.

### Owner Resolution Terminal States

Every Blocking Owner must terminate as exactly one of:

| Terminal state | Meaning | Required next action |
| --- | --- | --- |
| `POLICY_PROHIBITION` | Existing policy intentionally forbids the requested execution. | Record the policy owner and decision; certification may enter HOLD, demote, or prove canonical impossibility according to OMP / Production Maturity. |
| `IMPLEMENTATION_MISSING` | Existing owners can legally own the behavior, but implementation does not exist. | Create implementation work through the existing owner; certification enters HOLD until implemented and certified. |
| `OWNER_INVOCATION_MISSING` | Implementation exists, but certification is not invoking the correct existing owner or path. | Create invocation work; certification resumes from the same phase after invocation is corrected. |
| `IMPLEMENTATION_DEFECT` | Existing implementation should allow or handle the case but behaves incorrectly. | Create implementation correction through the existing owner; certification resumes after fix, tests, and certification evidence. |
| `CANONICAL_IMPOSSIBILITY` | No legal execution path exists through the current architecture. | Terminate according to canonical impossibility rules. |

No Blocking Owner may remain with only:

- `BLOCKED_BY_SAFETY_OWNER`;
- `BLOCKED`;
- `STOP_SAFE`;
- `OWNER_REQUIRED`;
- `UNKNOWN_OWNER_BLOCK`.

These are valid intermediate observations only. They are not terminal explanations.

### Owner Resolution Decision

Owner Resolution follows this decision table:

| If investigation proves | Required decision |
| --- | --- |
| Policy prohibits execution | Record `POLICY_PROHIBITION`. |
| Existing implementation is missing | Record `IMPLEMENTATION_MISSING` and create implementation work through the existing owner. |
| Existing owner invocation is missing | Record `OWNER_INVOCATION_MISSING` and create owner invocation work. |
| Existing implementation is defective | Record `IMPLEMENTATION_DEFECT` and create implementation correction. |
| Canonical impossibility is proven | Record `CANONICAL_IMPOSSIBILITY`. |
| Classification is not yet proven | Continue Owner Investigation. |

No certification phase may enter terminal HOLD due to an owner block until Owner Resolution has produced one terminal classification.

## 8.2 Certification Infrastructure Sufficiency Law

The certification program must maintain sufficient certification infrastructure to execute every certification stage.

Certification capability must never depend on accidental availability of Certification Users.

Certification infrastructure is part of the production platform. It is governed by the same Reality First, Authority, OMP, Production Maturity, user registry, group policy, assignment, routing, verification, rollback, and restoration owners that govern other production objects.

### Certification Infrastructure Responsibility Principle

The certification program is responsible not only for certifying capabilities.

The certification program is also responsible for maintaining, growing, preparing, and preserving the certification infrastructure required to certify future capabilities.

Certification Users, Certification Groups, Certification Pools, Controlled Production readiness, and Certification Infrastructure are permanent production assets of the certification program.

They are maintained continuously, not created only when certification begins.

Certification Users are production objects. They are not fake users, mock users, synthetic identities, or temporary fabricated objects. They are real production identities explicitly designated for controlled certification. They participate in real Runtime, real Planner, real Authority, real Verification, real Rollback, real Learning, OMP, and Production Maturity.

### Proactive Certification Readiness

Certification infrastructure should normally remain ahead of certification demand.

Whenever possible, Certification Pool expansion, Certification User preparation, Certification Group preparation, and Controlled Production readiness should occur before they become blocking requirements.

The certification program should proactively maintain readiness rather than reactively create infrastructure after a certification stage has already stopped.

### Certification Pool Sufficiency Rule

Before beginning a certification stage, the system must determine:

```text
Does a sufficiently large Certification Group already exist?
  -> YES: Use it.
  -> NO: Can additional Certification Users be legally created?
  -> YES: Create additional Certification Users through existing owners.
  -> Register them through existing owners.
  -> Assign them to the Certification Pool.
  -> Continue the certification program.
  -> NO: Run Owner Resolution for the blocking owner, then enter HOLD only with a terminal Owner Resolution classification, or CANONICAL_IMPOSSIBILITY when no legal path exists.
```

Certification Pool decisions:

| Situation | Required action |
| --- | --- |
| Pool already sufficient | Execute certification. |
| Pool insufficient and expansion allowed | Expand Certification Pool through existing owners. |
| Pool insufficient but expansion forbidden | Run Owner Resolution; enter `HOLD` only after `POLICY_PROHIBITION` is proven. |
| Pool expansion requires missing implementation | Run Owner Resolution; enter `HOLD` only after `IMPLEMENTATION_MISSING` or `OWNER_INVOCATION_MISSING` is proven. |
| Pool expansion impossible through current architecture | Enter `CANONICAL_IMPOSSIBILITY`. |

Before entering HOLD because of insufficient Certification Users, the system must answer:

`Why does the Certification Pool not already contain enough users?`

The answer must terminate as exactly one of:

- `POOL_ALREADY_SUFFICIENT`;
- `POOL_EXPANDED`;
- `POLICY_PROHIBITION`;
- `IMPLEMENTATION_MISSING`;
- `OWNER_INVOCATION_MISSING`;
- `IMPLEMENTATION_DEFECT`;
- `CANONICAL_IMPOSSIBILITY`.

No insufficient-pool HOLD may remain unexplained. Waiting for ordinary production users is not the default strategy.

## 9. Production Certification Principle

The goal is not to wait for random incidents.

The goal is not to fabricate incidents.

The goal is to create controlled, fully real production conditions using certification users so the entire governed production execution path can be certified repeatedly without risking ordinary customers.

Controlled production certification is the middle path:

- it avoids using ordinary customers as experiments;
- it avoids fake success;
- it avoids sandbox-only proof;
- it preserves real production execution semantics;
- it allows repeatable certification without waiting for random incident shape.

Waiting for random incidents is not a certification strategy. Controlled production certification is.

## 10. Controlled Production Environment

The Controlled Production Environment is the real production environment under controlled certification participation.

It is not:

- sandbox;
- simulation;
- mock runtime;
- fake production;
- isolated test environment.

It is:

- real production;
- real Runtime;
- real Planner;
- real Authority;
- real Approved Plan Lock;
- real Restore Barrier;
- real Runtime Apply;
- real Verification;
- real Rollback;
- real Learning;
- real OMP;
- real Production Maturity.

The only controlled elements are:

- certification users;
- temporary certification incident.

For every downstream owner, certification must look like ordinary governed production execution. Runtime must not receive a special certification-only shortcut, Planner must not invent a certification-only decision, and Authority must not issue fake authority.

## 11. Reality Preservation Law

Certification must never create artificial success.

Allowed:

- assign certification users;
- prepare certification source;
- legally degrade certification source;
- open certification incident;
- execute governed Runtime;
- observe Verification;
- observe Rollback;
- restore original assignments;
- close certification incident;
- persist evidence.

Forbidden:

- fake Planner decisions;
- fake Runtime Apply;
- fake Verification PASS;
- fake Rollback;
- fake Learning;
- fake Production evidence;
- fake Authority;
- fake Restore Barrier;
- fake Incident.

Certification must always execute the same production path used by ordinary users. Dry runs, fixtures, simulations, and report-only evidence may prepare or explain certification, but they cannot certify production behavior.

Certification must leave production logically identical to its pre-certification state.

Only engineering evidence may remain.

Mandatory restoration:

- restore user assignments;
- restore routing;
- restore temporary authority state;
- restore temporary incident state;
- restore production topology;
- persist historical evidence only.

Certification success is impossible without successful Production Restoration.

## 12. Temporary Certification Incident

Certification incidents are temporary.

The production system itself never enters a special certification mode. Only certification users participate. For Runtime, the incident is indistinguishable from a real production incident.

After certification completes:

- restore user assignments;
- restore source assignments;
- close certification incident;
- remove temporary certification state;
- preserve only engineering evidence.

The logical production state after cleanup must match the pre-certification state, except for append-only Engineering Reports, Certification History, consumer synchronization records, and other historical evidence records.

Temporary Certification Incident rules:

- The incident must use legal Wake / Incident mechanisms.
- The incident must use the same Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime, Verification, Rollback, Learning, OMP, and Production Maturity path as ordinary governed production execution.
- Temporary state must not leak into future ordinary incidents.
- Certification identity must remain traceable in evidence, even after temporary operational state is cleaned up.

## 13. Production Restoration Contract

Certification is complete only when cleanup is complete.

Mandatory cleanup:

- all temporary assignments restored;
- all certification users returned;
- all temporary routing removed;
- all temporary incident state removed;
- all temporary authority state removed;
- production topology restored;
- only historical evidence remains.

Production Restoration is a certification invariant. A certification run that passes Runtime Apply and Verification but leaves temporary routing, assignment, incident, or authority state behind is not complete.

Restoration must preserve evidence. Cleanup must not delete Engineering Reports, Certification History, OMP consumption records, Production Maturity decisions, or per-user verification / rollback closure evidence.

## 14. Real Incident Preemption

Real customer recovery takes priority over certification.

If a real production incident begins while certification is running:

- pause certification immediately;
- preserve certification state;
- release certification resources if required;
- allow the real incident to take priority.

Certification may resume only after:

- the real incident closes; or
- the operator authorizes restart.

No certification may interfere with real customer recovery. If certification and real production recovery compete for Authority Budget, Restore Barrier attention, Runtime execution, healthy target capacity, service-matrix resources, verification capacity, or operator attention, real production recovery wins.

## 15. Certification Environment Lifecycle

The controlled production certification lifecycle is:

```text
Determine Required Evidence
  -> Certification Evidence Decision
  -> Certification Pool Decision
  -> Prepare Certification Group
  -> Prepare Controlled Source
  -> Open Controlled Incident
  -> Governed Production Execution
  -> Verification
  -> Rollback / No-Rollback
  -> Cleanup
  -> Restore Production State
  -> Capability Earned
  -> Evidence Collection
  -> Update Certification History
  -> Update Passport
  -> Update OMP
  -> Update Production Maturity
  -> Authority Recognition
  -> Next Certification Mission
```

Lifecycle requirements:

- A stage that lacks current production evidence must run the Certification Evidence Decision before entering HOLD.
- If Controlled Production can legally create the required evidence, preparation becomes the next step.
- Waiting for a random production incident is a fallback only when Controlled Production is forbidden, impossible, blocked by missing implementation, or rejected by an existing safety owner after Owner Resolution reaches a terminal classification.
- A stage that lacks sufficient Certification Users must run the Certification Pool Decision before entering HOLD.
- If Certification Pool expansion is legal, the pool must be expanded through existing owners before certification stops.
- Waiting for ordinary production users is not a certification infrastructure strategy.
- Certification infrastructure should be maintained proactively so Certification Pool expansion, Certification User preparation, Certification Group preparation, and Controlled Production readiness normally happen before a stage is blocked.
- Preparation must use existing owners.
- Execution must use existing governed production owners.
- Verification and Rollback / No-Rollback must complete before certification success.
- Cleanup and Production Restoration must complete before certification completion.
- Certification History, Passport view, OMP, and Production Maturity updates happen only from preserved real evidence.
- Consumer synchronization follows Capability Earned. A consumer projection delay becomes Synchronization Debt unless an existing safety owner proves it must block progression.

## 16. Canonical Batch Ladder

The canonical governed evacuation ladder is:

| Stage | Authority class | Maximum users |
| --- | --- | --- |
| Stage 0 | CANARY | 1 |
| Stage 1 | SMALL_BATCH | 5 |
| Stage 2 | MEDIUM_BATCH | 10 |
| Stage 3 | LARGE_BATCH | 25 |
| Stage 4 | XLARGE_BATCH | 50 |
| Stage 5 | FULL_INCIDENT | All remaining affected users on the same active failed-source incident |

`FULL_INCIDENT` is not broad automation. It applies only to users still assigned to the same `incident_source` for the same active incident. It does not permit unrelated users, unrelated sources, unrelated incidents, rebalance, optimization, or cross-incident batching.

## 17. Certification Pool Design

V7 must maintain certification users or certification groups large enough to exercise every stage. These users must be dedicated non-paying, internal, or otherwise explicitly approved for controlled movement.

The Certification Pool is production infrastructure, not an optional convenience. It must be intentionally maintained so that certification capability does not depend on accidental production scale.

Certification Pool maintenance is continuous. It is not a one-time preparation task.

The pool should evolve together with the certification ladder. As higher certification stages become available, the Certification Pool should also evolve so future stages are executable without unnecessary preparation delay.

Certification users must be:

- Clearly marked in registry, group policy, or an equivalent existing owner-readable field.
- Safe to move between production egresses.
- Safe to rollback.
- Excluded from ordinary customer-impact metrics where certification movement would distort customer experience.
- Included in production evidence where the evidence represents real owner behavior, Runtime Apply, Verification, Rollback, Learning, OMP, and Production Maturity.

Minimum pool shape:

- One pool of 5 certification users for SMALL_BATCH.
- One pool of 10 certification users for MEDIUM_BATCH.
- One pool of 25 certification users for LARGE_BATCH.
- One pool of 50 certification users for XLARGE_BATCH.
- Or one scalable certification pool that can be partitioned into stage cohorts without overlapping active certification runs.

Certification groups must not share users with ordinary customer experiments. A certification user can be reused only after prior rollback/no-rollback closure, learning, Production Restoration, and consumer synchronization are complete or recorded as non-safety Synchronization Debt.

Before any stage enters HOLD because the pool is too small, V7 must run the Certification Pool Decision:

| Pool condition | Required action |
| --- | --- |
| Existing pool is sufficient for the target stage | Use the existing Certification Group. |
| Existing pool is insufficient and expansion is allowed | Create, register, and assign additional Certification Users through existing owners. |
| Expansion is forbidden by policy, Authority, OMP, or Production Maturity | Run Owner Resolution and enter HOLD only after `POLICY_PROHIBITION` is proven. |
| Expansion is blocked by missing owner invocation or implementation | Run Owner Resolution and enter HOLD only after `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_MISSING`, or `IMPLEMENTATION_DEFECT` is proven. |
| No legal production path can create sufficient Certification Users | Enter `CANONICAL_IMPOSSIBILITY`. |

Certification Pool expansion must not create fake users, mock users, synthetic identities, or hidden shortcuts. New Certification Users must be real production identities, visible to existing owners, and safe to restore.

## 18. Controlled Incident Design

A controlled incident must use real production mechanisms. It must not fake Runtime outcome, fake Verification, synthesize success, or directly write success records.

Allowed:

- Assign certification users to a controlled source through existing legal assignment owners.
- Degrade or mark the controlled source through an existing legal owner.
- Use existing service checks, observation, wake, and diagnosis owners.
- Run the existing governed L3 owner with the authorized budget.
- Let Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime, Verification, Rollback, and Learning produce their normal artifacts.

Disallowed:

- Directly writing fake success.
- Bypassing Wake.
- Bypassing Planner.
- Bypassing Authority.
- Bypassing Approved Plan Lock.
- Bypassing Restore Barrier.
- Bypassing Runtime.
- Bypassing Verification.
- Bypassing Rollback.
- Bypassing Learning or required consumer synchronization when an existing safety owner proves it is required for safe progression.
- Moving ordinary customer users as certification subjects.

The controlled source must be isolated enough that certification can run without hiding risk, but real enough that V7 observes it through the same production truth and service mechanisms used for ordinary incidents.

## 19. Certification Readiness Checklist

Every certification run must complete this checklist before execution. The checklist is executable: each row must be answered `PASS`, `FAIL`, or `NOT_APPLICABLE` with an evidence object or owner.

| Check | PASS condition | Failure action |
| --- | --- | --- |
| Certification Mission defined | Mission Name, Goal, Target Capability, Authority Budget, criteria, evidence, cleanup, and promotion decision fields are present. | Stop as `MISSION_NOT_DEFINED`; do not run. |
| Authority budget valid | Current Authority budget is present, fresh, and at least the requested stage budget. | Stop as `NOT_AUTHORIZED`; do not run. |
| Certification group exists | The stage has enough marked certification users or a documented smaller remaining-user condition. | Run Certification Pool Decision before any HOLD. |
| Certification Pool sufficient | The pool is already sufficient or legal expansion has completed through existing owners. | Stop only after Owner Resolution reaches a terminal classification, or as `CANONICAL_IMPOSSIBILITY`. |
| Certification users healthy | Users are enabled, internally approved, safe to move, and safe to rollback. | Remove unhealthy users or stop. |
| Controlled failed source prepared | The controlled source is assigned to the certification group and can legally open an incident. | Stop before Wake. |
| Production restoration ready | Original user assignments, source assignments, routing state, authority state, and cleanup owner are known before execution. | Stop as `RESTORATION_NOT_READY`. |
| Real incident preemption ready | Certification can pause and release resources if ordinary customer recovery requires them. | Stop as `PREEMPTION_NOT_READY`. |
| Healthy targets available | At least one target passes service, route, load, quality, policy, and suitability checks. | Stop as `NO_SAFE_TARGET`. |
| Planner healthy | Planner can produce selected move candidates with stable identity. | Stop as `PLANNER_NOT_READY`. |
| Runtime healthy | Runtime Apply, Verification, Rollback, and Learning owners are available. | Stop as `RUNTIME_NOT_READY`. |
| Restore Barrier healthy | Restore Barrier can validate the committed selected move identity. | Stop as `RESTORE_BARRIER_NOT_READY`. |
| Heartbeat active or governed owner callable | The existing governed owner can run through the approved path for the stage. | Stop; do not invoke alternate path. |
| Incident not already running | No conflicting certification incident is active for the same users/source. | Resume existing incident or stop; do not fork identity. |
| Operator approval present | Required operator approval exists when policy demands it. | Stop as `AUTHORITY_REQUIRED`. |
| Current stage authorized | The requested stage is the current authorized stage, not a future stage. | Stop as `STAGE_NOT_AUTHORIZED`. |

Readiness does not certify the stage. It only permits a governed certification attempt.

## 20. CANARY Stability Program

CANARY stability is the readiness bridge between one-user governed production execution and SMALL_BATCH certification.

SMALL_BATCH certification must not begin immediately after a single successful CANARY if CANARY evidence is unstable, incomplete, or recently regressed. CANARY must demonstrate repeated bounded governed success through the same owners that later stages will use.

CANARY stability entry criteria:

- CANARY stage is certified.
- Authority Budget remains CANARY or explicitly allows SMALL_BATCH review.
- The same governed L3 execution chain remains active: Wake, Incident, Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime Apply, Verification, Rollback / No-Rollback Closure, Learning, OMP, and Production Maturity.
- No unresolved regression exists for Wake, Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime, Verification, Rollback, Learning, OMP, or Production Maturity.
- Incident Source Continuity and Retry Budget behavior remain certified.

CANARY stability evidence:

| Requirement | Required evidence |
| --- | --- |
| Multiple governed one-user incidents | More than one successful real governed CANARY outcome, unless OMP / Production Maturity explicitly accepts a smaller evidence set. |
| No incident continuity regression | Incident remains open while affected users remain and closes only through Incident Completion Contract. |
| No retry regression | Retry-exhausted semantic attempts are excluded without resetting or bypassing retry budget. |
| No Runtime regression | Runtime Apply executes only committed selected moves. |
| No Restore Barrier regression | Restore Barrier validates committed identity without synthetic clearance. |
| No Verification regression | Verification finishes for the moved user and required services. |
| No Rollback regression | Rollback or no-rollback closure is complete for every touched user. |
| Consumer synchronization | OMP and Production Maturity consume, no-change, block with explicit safety reason, or record Synchronization Debt. |

CANARY stability exit criteria:

- `CANARY_STABLE`: all producer requirements pass, consumer synchronization is complete or recorded as non-safety Synchronization Debt, and no unresolved safety blocker remains.
- `CANARY_HOLD`: evidence is valid but Authority or an existing safety owner requires more review.
- `CANARY_REGRESSION_REQUIRED`: any owner, contract, evidence, or production behavior changed in a way covered by Regression Certification.
- `CANARY_UNSTABLE`: verification, rollback, identity, authority, or incident continuity fails.

Only `CANARY_STABLE` can make SMALL_BATCH certification ready for review.

## 21. Stage Certification Matrix

| Stage | Entry criteria | Required Authority budget | Required users | Procedure placeholder | Expected selected users | Expected selected moves | Required verification | Rollback requirement | Learning requirement | Consumer synchronization requirement | Pass criteria | Fail criteria |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANARY | Controlled incident open; 1 certification user on incident source; safe target exists; Authority allows CANARY. | 1 | At least 1 | Run existing governed L3 owner with max users 1. | 1 user where `current_egress == incident_source`. | 1 | Verify route, target, and required services for selected user. | Close rollback or no-rollback for selected user. | Materialize per-user feedback. | Consumers synchronize after Capability Earned or record Synchronization Debt. | Apply succeeds, verification passes, closure and Production Restoration complete. | Any producer gate blocks, verification fails without safe closure, rollback fails, restoration fails, or producer evidence is missing. |
| SMALL_BATCH | CANARY certified; 5 certification users on incident source; no unresolved safety blockers; Authority allows SMALL_BATCH. | 5 | At least 5 | Run existing governed L3 owner with max users 5. | Up to 5 users from same incident source. | `1..5`, expected 5 when enough users exist. | Verify every moved user. | Close rollback or no-rollback per user. | Materialize feedback per user. | Consumers synchronize Stage 1 evidence after Capability Earned or record Synchronization Debt. | All selected users apply and verify, or fewer selected only because fewer eligible users remain. | Any selected user fails verification, rollback/containment incomplete, unrelated user selected, restoration failure, or producer evidence missing. |
| MEDIUM_BATCH | SMALL_BATCH certified; 10 certification users on incident source; Authority allows MEDIUM_BATCH. | 10 | At least 10 | Run existing governed L3 owner with max users 10. | Up to 10 users from same incident source. | `1..10`, expected 10 when enough users exist. | Verify every moved user. | Close rollback or no-rollback per user. | Materialize feedback per user. | Consumers synchronize Stage 2 evidence after Capability Earned or record Synchronization Debt. | All selected users apply and verify with complete closure and Production Restoration. | Partial success, rollback failure, target degradation without closure, unrelated user, restoration failure, or producer evidence missing. |
| LARGE_BATCH | MEDIUM_BATCH certified; 25 certification users on incident source; Authority allows LARGE_BATCH. | 25 | At least 25 | Run existing governed L3 owner with max users 25. | Up to 25 users from same incident source. | `1..25`, expected 25 when enough users exist. | Verify every moved user. | Close rollback or no-rollback per user. | Materialize feedback per user. | Consumers synchronize Stage 3 evidence after Capability Earned or record Synchronization Debt. | All selected users apply and verify with no unresolved producer blocker. | Any failed user without complete rollback/containment, authority drop, restore barrier block, restoration failure, or producer evidence missing. |
| XLARGE_BATCH | LARGE_BATCH certified; 50 certification users on incident source; Authority allows XLARGE_BATCH. | 50 | At least 50 | Run existing governed L3 owner with max users 50. | Up to 50 users from same incident source. | `1..50`, expected 50 when enough users exist. | Verify every moved user. | Close rollback or no-rollback per user. | Materialize feedback per user. | Consumers synchronize Stage 4 evidence after Capability Earned or record Synchronization Debt. | All selected users apply and verify with complete closure and Production Restoration. | Partial or total failure, rollback failure, budget drop, restoration failure, producer evidence missing, or cross-incident selection. |
| FULL_INCIDENT | XLARGE_BATCH certified; same active failed-source incident has remaining affected users; Authority explicitly allows FULL_INCIDENT. | Remaining users on same incident | All remaining affected certification users for the same incident | Run existing governed L3 owner with FULL_INCIDENT-authorized scope. | All remaining users where `current_egress == incident_source`. | Remaining affected users for that incident only. | Verify every moved user. | Close rollback or no-rollback per user. | Materialize feedback per user and incident-level closure. | Consumers synchronize FULL_INCIDENT evidence after Capability Earned or record Synchronization Debt. | All remaining same-incident users are legally evacuated, or incident closes because no users remain or source recovered. | Any unrelated user selected, cross-incident batching, verification failure without closure, restoration failure, or producer evidence missing. |

## 22. Certification Exit Criteria

Every stage must reach a deterministic exit verdict. A stage cannot be treated as certified until every PASS row is true and every FAIL row is false.

### Universal PASS Criteria

| Area | PASS condition |
| --- | --- |
| Authority PASS | Authority budget is valid for the requested stage, the authority envelope matches the batch, and no unexpected Authority mutation occurred. |
| Planner PASS | Planner selected only eligible users from the same `incident_source`, preserved selected move identity, excluded retry-exhausted semantic attempts, and selected no unrelated users. |
| Wake PASS | Wake was produced by a legal confirmed incident or incident continuation source, not timer/cron/blind polling alone. |
| Approved Plan Lock PASS | Approved Plan Lock is valid, fresh, matches selected users/source/target/hash, and is consumed through the governed path. |
| Restore Barrier PASS | Restore Barrier validates the committed selected move count/hash/generation without bypass or synthetic clearance. |
| Runtime Apply PASS | Runtime Apply executes only the committed batch and records per-user apply results. |
| Verification PASS | Verification runs for every moved user and every selected required service using the canonical verification owner. |
| Rollback / No-Rollback closed | Every selected user has rollback completed, no-rollback accepted, containment completed, or a documented terminal closure state. |
| Production Restoration complete | Temporary certification assignments, routing, incident state, and authority state are removed or restored while historical evidence remains preserved. |
| Learning complete | Per-user feedback and learning records are materialized or the existing learning owner records a canonical no-change. |
| Capability Earned | Capability Producers completed their contracts and producer evidence is preserved. |
| Consumer Synchronization | OMP, Production Maturity, Passport, Current Program State, Engineering Reports, and Dashboard projections synchronize or record Synchronization Debt. |
| No unresolved producer blocker | No safety, identity, authority, verification, rollback, learning, Production Restoration, or producer-evidence blocker remains open. |
| Promotion permitted | Existing Authority / OMP / Production Maturity owners agree the next stage may be considered for promotion, or explicitly record Synchronization Debt that does not block safe progression. |

### Universal FAIL Criteria

| Area | FAIL condition |
| --- | --- |
| Verification failure | Any selected user fails verification and the stage was expected to certify success. |
| Rollback failure | Required rollback fails or containment does not close. |
| Restoration failure | Temporary certification assignment, routing, incident, authority, or topology state remains after the run. |
| Real incident interference | Certification blocks, delays, consumes resources needed by, or otherwise interferes with ordinary customer recovery. |
| Wrong incident | Selected move belongs to a different incident. |
| Wrong source | Any selected user's `current_egress` differs from `incident_source` unless the incident closed before execution. |
| Wrong target | Target differs from the approved target set or fails required target suitability. |
| Unexpected Runtime mutation | Runtime mutates users, source, target, route, or state outside the committed batch. |
| Unexpected Authority mutation | Authority budget, class, or envelope changes during the run without canonical owner approval. |
| Unexpected Restore Barrier mutation | Restore Barrier generation/hash/count changes outside its owner contract. |
| Unexpected Planner mutation | Planner selected move identity changes after approval or selected unrelated users. |
| Promotion forbidden | Any producer PASS prerequisite is missing, any safety blocker remains after Owner Resolution, Authority refuses promotion, or a consumer synchronization gap is blocked by a safety owner after Owner Resolution. |

### Stage-Specific Exit Criteria

| Stage | PASS | FAIL |
| --- | --- | --- |
| CANARY | Exactly one eligible user is governed, applied, verified, closed, learned, restored, and preserved as producer evidence. | Any selected user mismatch, failed verification, missing closure, failed restoration, or missing producer evidence. |
| SMALL_BATCH | Up to 5 same-incident users are governed with complete per-user verification, closure, learning, and evidence. | Any unrelated user, partial failure, missing closure, or selection above 5. |
| MEDIUM_BATCH | Up to 10 same-incident users pass the universal PASS criteria after SMALL_BATCH certification. | Any partial failure, target degradation without closure, missing evidence, or selection above 10. |
| LARGE_BATCH | Up to 25 same-incident users pass with stable authority, restore, verification, rollback, learning, and producer evidence. | Any Runtime/Authority/Restore mutation, rollback failure, missing producer evidence, or selection above 25. |
| XLARGE_BATCH | Up to 50 same-incident users pass with complete incident continuity and no unresolved producer blocker. | Any cross-incident selection, partial failure, producer evidence gap, or selection above 50. |
| FULL_INCIDENT | All remaining eligible users on the same active incident source pass or the incident closes canonically because none remain or source recovered. | Any unrelated user, multiple incidents, broad automation, failed closure, or missing producer evidence. |

## 23. Failure Scenario Matrix

| Scenario | Expected system behavior |
| --- | --- |
| All users PASS | Complete apply, verification, no-rollback closure, learning, Production Restoration, and producer evidence. Capability Earned occurs; consumer synchronization and authority recognition follow. |
| One user verification FAIL | Execute existing rollback or containment path for failed user, stop ladder, do not promote, preserve evidence for every user. |
| Partial success | Keep successful users only if existing rollback/no-rollback rules permit; rollback or contain failed users; stop ladder; do not promote. |
| Target degrades during apply | Stop or rollback according to Runtime and Verification outcome; do not continue larger batch; record target degradation evidence. |
| Source recovers during incident | Stop new failover selection for recovered source; close incident only through canonical incident closure rules. |
| Authority budget drops | Runtime or governed owner must cap or stop according to current Authority; do not execute above budget. |
| Restore Barrier blocks | Stop before Runtime Apply; preserve selected move and blocker evidence; do not bypass barrier. |
| Runtime Apply partially fails | Record per-user apply result; rollback or contain failed users; stop ladder; do not promote. |
| Rollback succeeds | Record rollback closure; preserve failed certification evidence; do not promote failed stage. |
| Rollback fails | Enter containment/escalation path through existing owners; freeze or demote according to Authority / OMP rules. |
| Retry budget exhausted for one user | Exclude exhausted semantic attempt from continuation; select only eligible remaining users if the same stage continues under authority. |
| Incident has fewer remaining users than stage budget | Select only remaining eligible users from the same incident source; pass only if this is expected and all selected users complete successfully. |
| Real production incident starts during certification | Pause certification, preserve state, release resources if required, and let real customer recovery take priority. |
| Cleanup fails | Hold certification, preserve evidence, restore production state through existing owners, and forbid promotion until cleanup closes. |

## 24. Promotion Contract

Promotion is evidence-based, not time-based. A stage can promote only after:

- Required evidence was obtained either from sufficient real production evidence or through a legal Controlled Production Certification Mission.
- Successful batch apply.
- Verification completed for every selected user.
- Rollback or no-rollback closure completed for every selected user.
- Outcome recorded.
- Learning and feedback materialized.
- Production Restoration completed.
- Consumer synchronization is complete, intentionally delayed, or recorded as non-safety Synchronization Debt.
- No unresolved safety blocker remains.
- Authority explicitly records or accepts the promotion.

Runtime execution does not promote itself. Planner selection does not promote authority. Reports alone do not promote. Promotion belongs to existing governance, OMP, Authority, and Production Maturity owners. Consumer synchronization may delay Authority Recognition only when an existing safety owner proves the synchronization gap affects safe progression.

Promotion state transitions:

| From | To | Required evidence |
| --- | --- | --- |
| NOT_CERTIFIED | READY_FOR_REVIEW | Stage run reached Capability Earned and producer evidence is persisted. |
| READY_FOR_REVIEW | PROMOTED | Authority approval, OMP readiness, Production Maturity readiness, and no unresolved safety blocker. |
| READY_FOR_REVIEW | HOLD | Evidence is valid but an owner requires review, residency, operator approval, or additional non-time-based evidence. |
| READY_FOR_REVIEW | REJECTED | Any owner rejects promotion or a blocker is discovered during review. |
| READY_FOR_REVIEW | SYNCHRONIZATION_DEBT | Consumer views are incomplete but no safety owner proves they block safe progression. |
| PROMOTED | NEXT_STAGE_READY | Current policy exposes the next authorized stage without changing runtime behavior beyond the approved budget. |

Promotion must not depend on elapsed time alone. Residence or cooldown may prevent immediate promotion, but cannot prove promotion by itself.

## 25. Demotion Contract

If a stage fails:

- Do not promote.
- Stop the ladder.
- Demote, freeze, or hold according to existing Authority and OMP rules.
- Preserve incident state.
- Record the blocker.
- Do not retry exhausted semantic attempts.
- Do not continue with a larger batch.
- Do not switch to another incident to preserve a positive result.

Failure evidence is still production evidence. It may improve diagnosis and maturity understanding, but it cannot certify the failed stage.

Deterministic demotion rules:

| Failure | Required action |
| --- | --- |
| Verification failure | Stop ladder, rollback or contain failed users, hold current stage. |
| Rollback failure | Freeze ladder until containment and owner review close. |
| Partial failure | Hold current stage; do not promote; preserve successful and failed per-user evidence. |
| Unexpected Runtime failure | Freeze or demote according to Runtime / Authority owner decision; do not retry blindly. |
| Authority rejection | Stop before apply or hold after run; do not execute above current budget. |
| Restore Barrier rejection | Stop before apply; preserve selected move evidence; do not bypass. |
| Planner inconsistency | Stop before apply; hold stage; require Planner evidence correction or rerun from same incident identity. |
| Wrong incident/source/target | Fail certification, freeze promotion, preserve mutation evidence. |
| Missing OMP or Production Maturity consumption | Record Synchronization Debt; do not block already-earned capability unless an existing safety owner blocks safe progression and Owner Resolution reaches a terminal classification. |
| Production Restoration failure | Hold stage and route to cleanup owner; do not promote until production topology matches pre-certification state. |
| Real incident preemption | Pause certification and preserve state; resume only after real incident closure or operator-authorized restart. |

Allowed demotion outcomes:

- Repeat the same stage only after the blocker is closed and retry budget permits a new semantic attempt.
- Hold the stage without promotion.
- Return to the previous certified stage.
- Freeze the ladder until containment or owner review closes.

## 26. Incident Completion Contract

An incident remains open while:

```text
remaining affected users > 0
```

If affected users remain on `incident_source`, the incident MUST remain OPEN. One successful batch must not close the incident if eligible affected users remain assigned to the failed source.

Allowed incident close conditions:

- `remaining_users == 0`.
- `incident_source` recovered and no longer satisfies the confirmed failure condition.
- Canonical containment requires closure or suspension.
- Canonical impossibility proves no legal execution path can complete.

No other closure is permitted. In particular, the incident must not close because one batch succeeded, one report was created, a blocker was found, the timer stopped, a different candidate appeared, or a new unrelated incident exists.

Temporary certification incident closure must also satisfy the Production Restoration Contract. Closing a certification incident is not enough if temporary assignments, routing, authority, or topology state remains.

## 27. Batch Invariants

The certification program must preserve these invariants:

- No broad automation.
- Same incident throughout one certification run.
- Same `incident_source` throughout one certification run.
- Same authority envelope for the committed batch unless the existing Authority owner stops execution.
- Same Restore Barrier semantics as normal governed execution.
- Same Verification semantics as normal governed execution.
- Same Rollback semantics as normal governed execution.
- Retry budget remains enforced.
- No cross-incident batching.
- No unrelated users.
- No Authority bypass.
- No Approved Plan Lock bypass.
- No Restore Barrier bypass.
- No Runtime bypass.
- No Verification bypass.
- No Rollback bypass.
- No silent `incident_source` switch.
- No retry-exhausted attempt reuse.
- No FULL_INCIDENT before certified promotion.
- No customer experiment hidden as certification.
- No synthetic success.
- No artificial certification success.
- No fake production evidence.
- No incomplete Production Restoration.
- No certification interference with real customer recovery.
- Real incident preemption must pause certification when required.

These invariants are certification invariants. Violating any of them makes the run `FAIL` or `INCOMPLETE_EVIDENCE`.

## 28. Blast Radius Contract

Blast Radius is mathematical:

```text
Blast Radius = maximum users legally affected by one governed certification execution
```

For the canonical ladder:

| Stage | Blast Radius |
| --- | --- |
| CANARY | 1 |
| SMALL_BATCH | 5 |
| MEDIUM_BATCH | 10 |
| LARGE_BATCH | 25 |
| XLARGE_BATCH | 50 |
| FULL_INCIDENT | Remaining users of one active incident |

Mandatory rules:

- Blast Radius never increases without certification.
- Blast Radius never exceeds the current Authority Budget.
- Blast Radius never crosses incidents.
- Blast Radius never includes users outside the active `incident_source`.
- Blast Radius never bypasses Runtime.
- Blast Radius never bypasses Verification.
- Blast Radius never bypasses Rollback.
- Blast Radius never bypasses Restore Barrier.
- Blast Radius never bypasses Approved Plan Lock.
- Blast Radius never bypasses Authority.

`FULL_INCIDENT` has a bounded Blast Radius: all remaining eligible users of one active failed-source incident. It is not broad automation and does not authorize unrelated users, unrelated incidents, or cross-incident movement.

## 29. Evidence Requirements

Every certification run must persist:

- `incident_key`.
- `incident_source`.
- Authority budget and authority class.
- Selected users.
- Selected sources.
- Selected targets.
- `selected_move_hash`.
- Approved Plan Lock identity and validity.
- Restore Barrier generation and hash.
- Runtime operation id.
- Apply result per user.
- Verification result per user.
- Rollback or no-rollback closure per user.
- Remaining users before and after.
- Original assignments and restored assignments.
- Temporary certification state cleanup result.
- Real incident preemption status, if applicable.
- Automation Gap Review.
- Automation Debt Metrics.
- Workflow Audit Review.
- Workflow Debt Metrics.
- Pipeline Candidates or terminal workflow classifications.
- Automation Candidates or intentionally manual classifications.
- Learning and feedback records.
- Consumer synchronization status and any Synchronization Debt.
- Engineering report link.

If any Capability Producer object is not persisted, the certification result is incomplete until the missing object is either produced or the existing safety owner formally declares it not applicable.

If a Capability Consumer object is not synchronized after Capability Earned, the result is Synchronization Debt unless an existing safety owner proves that synchronization is required for safe progression.

## 30. Certification History

Certification History is a permanent production artifact. Every certification attempt must become historical engineering evidence.

History is owned by the existing Engineering Report lifecycle and consumed by OMP and Production Maturity. It is not a new owner and not a new truth source. Storage is the append-only set of certification engineering reports plus any existing report index or OMP / Current Program State pointer that references them.

History must be append-only. Existing rows must never be rewritten, deleted, edited for convenience, or replaced by later conclusions. If a historical row was wrong or incomplete, a later correction row must be appended with its own date, evidence, owner, and engineering report.

Canonical history table:

| Field | Required meaning |
| --- | --- |
| Stage | Certification stage attempted, such as CANARY, SMALL_BATCH, MEDIUM_BATCH, LARGE_BATCH, XLARGE_BATCH, or FULL_INCIDENT. |
| Date | Timestamp of the certification attempt. |
| Authority Budget | Authority Budget active at execution time. |
| Commit | Source commit or equivalent deployed artifact identity. |
| Deploy ID | Production deployment identity used for the attempt. |
| Incident | Incident key and incident source. |
| Certification Group | Certification group or cohort used. |
| Users | Selected users and moved users. |
| PASS / FAIL | Deterministic certification verdict. |
| Rollback | Per-user rollback or no-rollback closure result. |
| Verification | Per-user verification result and service outcome. |
| Regression | Whether this was initial certification or regression certification. |
| Promotion Decision | PROMOTED, HOLD, DEMOTED, FROZEN, REJECTED, or NOT_APPLICABLE. |
| Engineering Report | Link or path to the evidence report. |
| OMP Consumption | OMP consumed, rejected, no-change, or pending. |
| Production Maturity Consumption | Production Maturity consumed, rejected, no-change, or pending. |
| Restoration | Production Restoration completed, failed, or not applicable. |
| Preemption | Whether a real incident preempted certification. |
| Automation Gap Review | Manual actions classified and Automation Candidates created or closed. |
| Automation Debt Metric | Current, created, closed, remaining, and trend values. |
| Workflow Audit Review | Manual workflows classified and Pipeline Candidates created or closed. |
| Workflow Debt Metric | Current, created, closed, remaining, and trend values. |
| Synchronization Debt | Consumer synchronization gaps and terminal state. |

Retention rules:

- Certification History is retained permanently.
- Each certification report is retained with the history row that references it.
- History retention must outlive individual incident artifacts when operational retention differs.
- A missing historical row means the stage is not certified unless another canonical history row proves the same stage.
- A failed certification row must remain visible; failure evidence is part of production maturity.
- Regression rows must reference the change that triggered re-certification.

## 31. Regression Certification

Regression Certification defines which certification stages become invalid or require re-certification after implementation, contract, evidence, owner, or production-behavior changes.

Regression governance reuses OMP and Production Maturity. OMP decides the next certification action and Production Maturity decides whether evidence remains acceptable, is blocked, or requires re-certification. This section only specializes those existing owners for governed batch certification.

Deterministic regression matrix:

| Change | Minimum required re-certification |
| --- | --- |
| Wake changed | CANARY and every stage whose legal wake source or incident continuation can be affected. |
| Planner changed | CANARY and SMALL_BATCH; higher stages if ranking, batching, incident continuity, retry filtering, or selected move identity can be affected. |
| Authority changed | Every certified stage. |
| Approved Plan Lock changed | CANARY, SMALL_BATCH, and every stage whose selected move identity or approval envelope can be affected. |
| Restore Barrier changed | CANARY, SMALL_BATCH, MEDIUM_BATCH, and every stage whose batch identity or clearance can be affected. |
| Runtime Apply changed | Every certified stage. |
| Verification changed | Every certified stage. |
| Rollback changed | Every certified stage. |
| Learning / Feedback changed | Every certified stage whose maturity or promotion evidence depends on learning output. |
| OMP consumption changed | Every stage whose promotion or next action depends on OMP. |
| Production Maturity consumption changed | Every stage whose certification maturity state depends on Production Maturity. |
| Incident Source continuity changed | CANARY, SMALL_BATCH, and every incident-continuation stage. |
| Retry Budget changed | CANARY, SMALL_BATCH, and every stage that can continue after rollback or semantic attempt exhaustion. |
| Batch size / Authority Budget mapping changed | Every affected stage and every higher stage. |
| Observability or persistence changed | Re-certify the affected evidence path before using it for promotion. |
| Production Restoration changed | CANARY and every stage whose cleanup, assignment restoration, incident closure, or authority cleanup can be affected. |
| Real Incident Preemption changed | CANARY and every stage that can overlap with ordinary customer recovery. |
| Certification automation changed | Re-certify every stage whose evidence creation, owner invocation, Passport update, report generation, or consumer synchronization can be affected. |

Rules:

- Regression certification is deterministic, not optional.
- Re-certification scope is the highest risk scope among all changed owners.
- If a change touches a shared contract used by every stage, every certified stage returns to `REGRESSION_REQUIRED`.
- If a change is documentation-only and does not affect owner behavior, evidence, or certification contracts, the Certification Passport may remain unchanged, but the engineering report must say why.
- A stage with `REGRESSION_REQUIRED` is not certified for promotion until a new PASS row is appended to Certification History.

## 32. Certification Coverage Matrix

Certification Coverage is the tabular view inside the V7 Certification Passport. It should not live as an independent canonical artifact unless Owner Mapping later proves that Production Maturity and Current Program State cannot expose it.

Certification Coverage shows which capabilities are implemented and which are certified. It must distinguish status precisely:

- `IMPLEMENTED`: code or document exists, but production certification evidence is incomplete.
- `CERTIFIED`: production certification evidence exists in Certification History and the Certification Passport.
- `NOT_CERTIFIED`: the capability or stage is known but lacks required certification evidence.
- `UNKNOWN`: no reliable persisted evidence exists.

Permanent coverage table:

| Capability / Stage | Coverage state | Required evidence |
| --- | --- | --- |
| Wake | CERTIFIED | Legal confirmed production wake and incident continuation evidence. |
| Planner | CERTIFIED | Same-incident selected move evidence with stable identity. |
| Incident Continuity | CERTIFIED | Incident remains open while affected users remain. |
| Incident Source Continuity | CERTIFIED | Continuation selected users remain on `incident_source`. |
| Retry Budget | CERTIFIED | Exhausted semantic attempts are excluded without bypassing retry budget. |
| Approved Plan Lock | CERTIFIED | Valid lock matches committed selected moves. |
| Restore Barrier | CERTIFIED | Restore Barrier validates committed selected move identity. |
| Runtime | CERTIFIED | Runtime Apply executes committed moves only. |
| Verification | CERTIFIED | Verification runs and records per-user outcomes. |
| Rollback | CERTIFIED | Rollback or no-rollback closure is recorded per user. |
| CANARY | CERTIFIED | One-user governed production certification PASS. |
| SMALL_BATCH | NOT_CERTIFIED | Stage 1 governed batch certification PASS. |
| MEDIUM_BATCH | NOT_CERTIFIED | Stage 2 governed batch certification PASS. |
| LARGE_BATCH | NOT_CERTIFIED | Stage 3 governed batch certification PASS. |
| XLARGE_BATCH | NOT_CERTIFIED | Stage 4 governed batch certification PASS. |
| FULL_INCIDENT | NOT_CERTIFIED | Stage 5 same-incident evacuation certification PASS. |

Coverage must not be inferred from implementation alone. If production evidence is missing, the status is `IMPLEMENTED` or `NOT_CERTIFIED`, not `CERTIFIED`.

## 33. V7 Certification Passport

The V7 Certification Passport is the Production Maturity / Current Program State view of what V7 has actually proven in production.

It is not:

- An engineering report.
- OMP.
- Current Program State.
- Production Maturity.
- A runtime artifact.
- A planner artifact.
- A replacement for Certification History.
- A standalone owner.
- A new truth source.

The Passport summarizes Certification History and current regression state into a production maturity view. Production Maturity owns maturity acceptance, Current Program State may display current volatile passport status, and OMP owns next-action scheduling.

Canonical passport fields:

| Field | Meaning |
| --- | --- |
| Capability / Stage | Owner capability or ladder stage. |
| Status | CERTIFIED, IMPLEMENTED, NOT_CERTIFIED, REGRESSION_REQUIRED, SUSPENDED, or UNKNOWN. |
| Last PASS | Timestamp and report for the latest passing certification. |
| Last FAIL | Timestamp and report for the latest failing certification, if any. |
| Regression State | Current regression requirement, if any. |
| Authority Scope | Highest Authority Budget proven for this capability or stage. |
| Evidence | Certification History row or report path. |
| Owner | Existing owner responsible for the evidence. |
| OMP State | OMP consumed, rejected, no-change, or pending. |
| Production Maturity State | Production Maturity consumed, rejected, no-change, or pending. |
| Automation Debt | Current, created, closed, remaining, and trend values for the capability or stage. |
| Workflow Debt | Current workflows, Pipeline Candidates, terminal classifications, and trend values for the capability or stage. |
| Synchronization Debt | Consumer synchronization gaps for already-earned capabilities. |

Passport update rules:

- Update only from Certification History, Regression Certification, OMP, and Production Maturity evidence.
- Do not update from implementation claims alone.
- Do not update from dry-run evidence alone.
- A PASS certification can move the Passport view to `CERTIFIED` only when OMP and Production Maturity can consume the evidence or record a non-safety Synchronization Debt. This is a Passport synchronization rule, not proof that Capability Producers failed.
- A Passport update lag after Capability Earned is Synchronization Debt, not proof that Capability Producers failed.
- A relevant owner change can move a status from `CERTIFIED` to `REGRESSION_REQUIRED`.
- A failed certification can move a status to `SUSPENDED`, `NOT_CERTIFIED`, or `REGRESSION_REQUIRED` according to existing governance.
- If evidence is missing or contradictory, use `UNKNOWN` or `REGRESSION_REQUIRED`, never optimistic certification.

Current initial passport snapshot:

| Capability / Stage | Passport status |
| --- | --- |
| Incident Continuity | CERTIFIED |
| Retry Budget | CERTIFIED |
| Incident Source Continuity | CERTIFIED |
| Wake | CERTIFIED |
| Planner | CERTIFIED |
| Approved Plan Lock | CERTIFIED |
| Restore Barrier | CERTIFIED |
| Runtime | CERTIFIED |
| Verification | CERTIFIED |
| Rollback | CERTIFIED |
| CANARY | CERTIFIED |
| SMALL_BATCH | NOT_CERTIFIED |
| MEDIUM_BATCH | NOT_CERTIFIED |
| LARGE_BATCH | NOT_CERTIFIED |
| XLARGE_BATCH | NOT_CERTIFIED |
| FULL_INCIDENT | NOT_CERTIFIED |

The Passport must represent proven production capability only.

## 34. Observability Contract

Operators must always be able to see the current certification state without reading raw logs. The required minimum view is:

- Current Stage.
- Current Authority Budget.
- Current Incident.
- Incident Source.
- Remaining Users.
- Current Batch.
- Selected Users.
- Verification Summary.
- Rollback Summary.
- Promotion State.
- Current Blocker.
- Next Planned Batch.
- Certification Progress.
- Production Restoration Status.
- Real Incident Preemption Status.
- Current Automation Debt.
- Automation Debt Trend.
- Current Workflow Debt.
- Workflow Debt Trend.

The observability surface should map naturally into Admin UI, but this document does not require a new UI. If the current UI cannot expose a field, the engineering report must name the missing field and owner.

## 35. Operational Procedure

The high-level procedure for each stage is:

1. Determine required evidence for the target stage.
2. Run the Certification Evidence Decision.
3. Use sufficient real production evidence if it already exists.
4. Run the Certification Pool Decision for the target stage.
5. If the pool is insufficient and legal expansion is allowed, expand the Certification Pool through existing owners.
6. Verify that certification infrastructure already satisfies future planned stages whenever practical. This is a readiness improvement, not a runtime execution requirement.
7. If real production evidence is insufficient and Controlled Production is legal, prepare the certification group.
8. Prepare the controlled source.
9. Verify baseline assignment, target health, rollback readiness, and service evidence.
10. Open the controlled incident through existing legal owners.
11. Confirm Authority budget for the target stage.
12. Confirm Production Restoration readiness and Real Incident Preemption readiness.
13. Run the existing governed L3 owner with the authorized budget.
14. Observe selected users and selected move identity.
15. Verify Approved Plan Lock and Restore Barrier.
16. Let Runtime Apply execute through the existing path.
17. Verify every moved user.
18. Close rollback or no-rollback per user.
19. Cleanup temporary certification state.
20. Restore production state.
21. Record learning and feedback.
22. Run the Automation Audit Loop for every manual action.
23. Classify Automation Debt and calculate Automation Debt Metrics.
24. Run the Workflow Audit Loop for every manual workflow.
25. Classify Workflow Debt and calculate Workflow Debt Metrics.
26. Generate Automation Candidates, Pipeline Candidates, or terminal manual-work / workflow records.
27. Run Owner Resolution for every owner block before terminal HOLD.
28. Record Capability Earned when producers completed their contracts and producer evidence is preserved.
29. Generate the certification report and synchronize Certification History, Passport, OMP, Production Maturity, Current Program State, and dashboard consumers.
30. Record Synchronization Debt for any consumer that has not synchronized, unless an existing safety owner blocks progression.
31. Promote, hold, or demote according to existing governance.

Exact commands are intentionally placeholders unless already canonical for the current production deployment. A certification procedure may reference current tools, but it must not embed destructive shell commands or bypass existing owners.

## 36. Certification Reports

Report path:

```text
docs/reports/engineering/<timestamp>_controlled_production_certification_<stage>.md
```

Required sections:

- Summary.
- Mission Name.
- Mission Goal.
- Target Capability.
- Stage.
- Authority budget.
- Users before.
- Selected users.
- Users moved.
- Verification.
- Rollback.
- Production restoration.
- Real incident preemption.
- Automation Gap Review.
- Automation Audit Loop.
- Automation Debt Metrics.
- Automation Candidates.
- Workflow Audit Review.
- Workflow Debt Metrics.
- Pipeline Candidates.
- Blocking Owner.
- Owner Investigation.
- Owner Resolution terminal classification.
- Required Resolution.
- Reason no further owner investigation is necessary.
- Intentionally manual actions.
- Remaining users.
- Pass/fail.
- Promotion decision.
- Next action.

Reports must distinguish:

- `PASS`.
- `FAIL`.
- `STOP_SAFE`.
- `NOT_AUTHORIZED`.
- `INCOMPLETE_EVIDENCE`.
- `CANONICAL_IMPOSSIBILITY`.

Only `PASS` with complete evidence can support promotion.

Whenever execution is blocked by an owner, the report must not stop at `BLOCKED_BY_SAFETY_OWNER`, `BLOCKED`, or `STOP_SAFE`. It must include the Blocking Owner, investigation evidence, terminal Owner Resolution classification, Required Resolution, and the reason no further investigation is currently necessary.

## 37. Certification Recovery Contract

Certification Recovery defines what happens when certification stops mid-stage. It reuses the Execution Mission Protocol recovery law and specializes it for certification stages. It does not replace Execution Mission recovery, Runtime rollback, OMP continuation, or Production Maturity consumption.

Recovery must never be implicit.

For every interrupted or failed certification, the report must record:

- Current stage.
- Certification Evidence Decision and why Controlled Production is or is not being used.
- Incident key and incident source.
- Selected users.
- Users applied.
- Users verified.
- Users rolled back or closed.
- Users not yet touched.
- Current Authority Budget.
- Current blocker.
- Blocking Owner.
- Owner Investigation.
- Owner Resolution terminal classification.
- Required Resolution.
- Reason no further owner investigation is necessary.
- Required recovery action.
- Promotion state.
- Production Restoration state.
- Real Incident Preemption state.

Recovery matrix:

| Case | Required recovery |
| --- | --- |
| Stage fails after user 3 of 5 | Stop stage, close rollback/no-rollback for touched users, preserve untouched users, promotion forbidden. |
| Verification fails after user 4 | Rollback or contain failed user through existing owner, close successful users according to policy, hold stage. |
| Rollback succeeds for one user | Record rollback closure, keep failure evidence, hold or repeat stage only after blocker closure and retry budget permits. |
| Rollback fails | Enter containment, freeze stage, promotion forbidden until containment closes. |
| Authority revoked during stage | Stop before any further apply, preserve evidence, hold or demote according to Authority / OMP. |
| Runtime interrupted | Preserve apply state, determine touched users, run existing rollback/containment if required, freeze until closure. |
| Incident source recovered during stage | Stop new selection, complete closure for touched users, close incident only through Incident Completion Contract. |
| Restore Barrier blocks mid-stage | Stop before Runtime Apply for blocked moves, preserve selected move evidence, run Owner Resolution for Restore Barrier, do not bypass. |
| Planner identity changes mid-stage | Stop before apply or freeze the run, preserve mutation evidence, promotion forbidden. |
| OMP / Production Maturity cannot consume evidence | Record Synchronization Debt; if an existing safety owner blocks progression, run Owner Resolution before HOLD. |
| Production Restoration fails | Hold certification, preserve evidence, restore production topology through existing owners, and promotion remains forbidden. |
| Real incident begins during certification | Pause certification, preserve state, release resources if required, and resume only after closure or operator authorization. |
| Any owner blocks execution | Run Owner Resolution until `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, or `CANONICAL_IMPOSSIBILITY` is proven. |

Allowed recovery outcomes:

- `CONTINUE`: only when the same incident, authority, identity, and safety evidence remain valid.
- `HOLD`: stop progression while preserving current certified state.
- `REPEAT_STAGE`: rerun the same stage only after blockers close and retry budget permits legal semantic attempts.
- `ROLLBACK`: execute existing rollback owner for affected users.
- `CONTAINMENT`: enter existing containment path when rollback cannot safely close.
- `DEMOTION`: reduce certified operating scope according to existing Authority / OMP rules.
- `PROMOTION_FORBIDDEN`: default outcome for any unresolved safety blocker, failed verification, failed rollback, missing producer evidence, or authority/safety owner rejection.
- `PREEMPTED_BY_REAL_INCIDENT`: certification paused because real customer recovery has priority.
- `RESTORATION_REQUIRED`: certification cannot complete until temporary state is cleaned up.

No certification may remain in an undefined recovery state.

## 38. Certification State Machine

The certification lifecycle is deterministic:

```text
NOT_READY
  -> EVIDENCE_DECISION
  -> POOL_DECISION
  -> READY
  -> RUNNING
  -> VERIFYING
  -> RESTORING
  -> CAPABILITY_EARNED
  -> CONSUMER_SYNCHRONIZATION
  -> PASS
  -> PROMOTION_REVIEW
  -> PROMOTED
  -> NEXT_STAGE_READY
```

Failure path:

```text
READY
  -> RUNNING
  -> FAILED
  -> ROLLBACK_OR_CONTAINMENT
  -> OWNER_RESOLUTION
  -> HOLD
  -> RETRY_ALLOWED or DEMOTED or FROZEN
```

State transition rules:

| From | To | Condition |
| --- | --- | --- |
| NOT_READY | EVIDENCE_DECISION | Target stage requires production evidence or entry readiness evaluation. |
| EVIDENCE_DECISION | POOL_DECISION | Sufficient real production evidence exists or Controlled Production can legally generate the required evidence through existing owners. |
| EVIDENCE_DECISION | OWNER_RESOLUTION | Controlled Production is blocked by a safety owner, policy owner, missing implementation, missing invocation, or suspected owner defect. |
| EVIDENCE_DECISION | CANONICAL_IMPOSSIBILITY | No legal real or controlled production path can produce the required evidence through the current architecture. |
| POOL_DECISION | READY | Certification Pool is sufficient or legal expansion completed through existing owners. |
| POOL_DECISION | OWNER_RESOLUTION | Pool expansion is blocked by policy, Authority, OMP, Production Maturity, missing implementation, missing invocation, or suspected owner defect. |
| POOL_DECISION | CANONICAL_IMPOSSIBILITY | No legal production path can create or designate enough Certification Users for the target stage. |
| READY | RUNNING | Existing governed owner starts with authorized budget. |
| RUNNING | VERIFYING | Runtime Apply completed enough to verify selected users. |
| VERIFYING | RESTORING | Every selected user passed verification and rollback/no-rollback closure is ready for cleanup. |
| RESTORING | CAPABILITY_EARNED | Production Restoration, learning, and producer evidence are complete. |
| CAPABILITY_EARNED | CONSUMER_SYNCHRONIZATION | Consumer owners begin Certification History, Passport, OMP, Production Maturity, Current Program State, Engineering Report, Dashboard, Automation Debt, and Workflow Debt synchronization. |
| CONSUMER_SYNCHRONIZATION | PASS | Consumers synchronize or record non-safety Synchronization Debt. |
| CONSUMER_SYNCHRONIZATION | OWNER_RESOLUTION | An existing safety owner blocks progression because synchronization is required for safety. |
| VERIFYING | FAILED | Verification, rollback, identity, authority, runtime, restore, or evidence condition fails. |
| RESTORING | FAILED | Production Restoration, cleanup, evidence preservation, or producer evidence fails. |
| FAILED | ROLLBACK_OR_CONTAINMENT | Existing rollback or containment owner is required. |
| ROLLBACK_OR_CONTAINMENT | OWNER_RESOLUTION | Closure evidence exists but an owner block prevents promotion, retry, demotion, or safe continuation. |
| OWNER_RESOLUTION | HOLD | Blocking Owner reached `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, or `IMPLEMENTATION_DEFECT`, and certification cannot legally continue until the Required Resolution is complete. |
| OWNER_RESOLUTION | CANONICAL_IMPOSSIBILITY | Blocking Owner investigation proves no legal execution path exists through the current architecture. |
| OWNER_RESOLUTION | RETRY_ALLOWED | Blocking Owner investigation proves invocation can continue legally without implementation or policy change. |
| HOLD | RETRY_ALLOWED | Blocker closed and retry budget permits a legal semantic attempt. |
| HOLD | DEMOTED | Existing Authority / OMP owner lowers the stage. |
| HOLD | FROZEN | Containment, evidence, or owner review is unresolved. |
| PASS | PROMOTION_REVIEW | Capability is earned and consumer synchronization is complete or classified as non-safety Synchronization Debt. |
| PROMOTION_REVIEW | PROMOTED | Existing owners approve promotion. |
| PROMOTION_REVIEW | HOLD | Evidence is valid but promotion is not approved. |

No state transition may skip Authority, Restore Barrier, Runtime, Verification, Rollback, Learning, or Production Restoration when those producers are required. No state transition may silently drop OMP, Production Maturity, Passport, Current Program State, Engineering Reports, or Dashboard synchronization; incomplete consumer synchronization must be recorded as Synchronization Debt unless an existing safety owner blocks progression. No state may enter HOLD for missing evidence until the Certification Evidence Decision has determined why Controlled Production is not being used. No state may enter HOLD for insufficient Certification Users until the Certification Pool Decision has determined why the pool cannot be expanded. No state may enter terminal HOLD for an owner block until Owner Resolution has produced a terminal classification and Required Resolution.

## 39. FULL_INCIDENT Contract

`FULL_INCIDENT` means all remaining eligible users belonging to one active `incident_source`, under the current Authority Budget, using the existing governed execution path.

It explicitly does not mean:

- All production users.
- Multiple incidents.
- Broad automation.
- Cross-incident movement.
- Rebalance.
- Optimization.
- Movement outside the current failed-source incident.

FULL_INCIDENT is allowed only after XLARGE_BATCH certification and explicit Authority approval. It must preserve the same incident completion contract: the incident closes only when no affected users remain, the source recovered, containment requires closure, or canonical impossibility is proven.

## 40. Certification Automation Model

Future certification automation should follow this high-level workflow:

```text
Prepare
  -> Validate Readiness
  -> Execute Stage
  -> Verification
  -> Cleanup
  -> Restore Production State
  -> Capability Earned
  -> Collect Evidence
  -> Consumer Synchronization
  -> Record Synchronization Debt, if needed
  -> Review Automation Gaps
  -> Run Automation Audit Loop
  -> Classify Automation Debt
  -> Run Workflow Audit Loop
  -> Classify Workflow Debt
  -> Create Automation Candidates or Intentionally Manual Records
  -> Create Pipeline Candidates or Terminal Workflow Records
  -> Record Automation Debt Metrics
  -> Record Workflow Debt Metrics
  -> Classify Synchronization Debt
  -> Generate Engineering Report
  -> Update OMP
  -> Update Production Maturity
  -> Authority Recognition / Promotion Decision
  -> Next Stage
```

This is documentation only. It is not an implementation design and does not create a certification engine. Any future implementation must reuse existing owners or first prove why an existing owner cannot own the step.

Every project must improve automation when justified. A certification project should not merely certify capability if it also exposes safe, owner-mapped manual work that can be reduced. The automation improvement remains subordinate to certification safety: no automation candidate may bypass Reality First, Authority, Restore Barrier, Runtime, Verification, Rollback, Learning, OMP, Production Maturity, or Production Restoration.

Every project must also improve workflow orchestration when justified. A certification project should not leave repeated manual workflows unexplained. Workflow improvement remains subordinate to the same safety and certification constraints as automation improvement.

## 41. Integration With Existing V7 Canon

OMP: Owns program progression, next action, stop/continue decisions, and certification governance.

Production Maturity: Consumes real certification evidence and decides maturity impact. Synthetic evidence must not increase maturity.

Capability Producers: Existing production owners that create certified capability evidence before consumer synchronization.

Capability Consumers: Certification History, Passport, OMP, Production Maturity, Current Program State, Coverage Matrix, Engineering Reports, and Dashboard projections consume capability after Capability Earned. They do not create capability.

Execution Priority Law: Reality and Capability Producers come before consumer synchronization. Documentation and projections synchronize reality; they do not make reality wait unless an existing safety owner proves synchronization is required.

Runtime Model: Defines runtime execution, verification, rollback, learning, and safety responsibilities.

Decision Model: Preserves Planner/Runtime decision separation and prevents Runtime from inventing Planner decisions.

Authority Budget: Defines the current authorized user budget. Certification may not exceed it.

Restore Barrier: Preserves pre-apply safety boundary and committed selected move identity.

Execution Mission Protocol: Governs live execution continuation until success or canonical impossibility.

V7 Execution Completion Protocol: Prevents investigations from stopping at blockers when the mission is to complete execution.

SYSTEM_MAP: Maps existing owners and prevents duplicate architecture.

Current Program State: Records the current status, next step, blockers, and certified capability state.

Engineering Reports: Preserve append-only Certification History evidence for every certification attempt.

Reality First: Requires certification to use real production execution, real production owners, and preserved evidence, never fake success.

Capability Earned Law: Capability is earned through governed production certification and Authority recognition, never by configuration alone.

Capability Evolution Model: OMP / Authority / Production Maturity consume evidence and decide when a certified capability may be recognized and used.

Consumer Synchronization: OMP, Production Maturity, Passport, Current Program State, Engineering Reports, Dashboard projections, Automation Debt views, and Workflow Debt views synchronize after Capability Earned and record Synchronization Debt when incomplete.

Continuous Automation Evolution: Every certification mission must audit manual work, classify automation gaps, and feed justified Automation Candidates back into OMP / Production Maturity without creating a parallel automation program.

Automation Debt: Engineering Reports preserve manual-work evidence, OMP schedules next action, Production Maturity records maturity impact, SYSTEM_MAP resolves missing ownership, and Current Program State / Passport views expose current debt state.

Workflow Evolution: Engineering Reports preserve workflow evidence, OMP schedules pipeline investigation, Production Maturity records maturity impact, SYSTEM_MAP resolves owner orchestration, and Current Program State / Passport views expose current Workflow Debt.

Certification Mission Contract: Reuses Execution Mission Protocol mission discipline for each controlled production certification run.

Reality Creation Law: Extends Reality First by requiring V7 to create controlled real production conditions rather than wait for random incidents.

Controlled Evidence Generation Law: Extends Reality Creation and Controlled Production Environment by making Controlled Production the default path when required certification evidence is unavailable from current production and existing safety owners allow it.

Certification Infrastructure Sufficiency Law: Extends Certification Pool Design, Controlled Production Environment, OMP, and Production Maturity by requiring sufficient real Certification Users before a stage can enter execution or HOLD.

Certification Infrastructure Responsibility Principle: Extends Certification Infrastructure Sufficiency by making Certification Users, Certification Groups, Certification Pools, Controlled Production readiness, and Certification Infrastructure permanent production assets maintained by the certification program.

Owner Resolution Law: Extends Execution Completion Protocol, Certification Recovery, Certification Evidence Decision, Certification Pool Decision, Owner Mapping, OMP, Production Maturity, SYSTEM_MAP, Engineering Reports, and Current Program State so every Blocking Owner is investigated until policy prohibition, missing implementation, missing invocation, implementation defect, or canonical impossibility is proven.

V7 Certification Passport: Production Maturity / Current Program State view that summarizes proven production capability from history and regression state without replacing OMP, Production Maturity, Current Program State, or Engineering Reports.

Regression Certification: OMP / Production Maturity decision that determines when certified capabilities return to `REGRESSION_REQUIRED` after owner or contract changes.

## 42. Canonical Owner Review

Every program addition must pass Discover -> Reuse -> Extend -> Create Only If Necessary.

| Addition | Existing owner searched | Reuse / extend decision | New artifact created? | Reason |
| --- | --- | --- | --- | --- |
| Certification History | Engineering Reports, OMP, Production Maturity, Current Program State. | Reuse Engineering Reports as append-only evidence; OMP / Production Maturity consume; CPS may point to current state. | NO | Existing report lifecycle already owns historical evidence. |
| Regression Certification | OMP, Production Maturity, Current Program State, Engineering Reports. | Reuse OMP for next action and Production Maturity for evidence acceptance/blocking. | NO | Regression is a certification governance decision, not a new owner. |
| Certification Coverage Matrix | Production Maturity, Current Program State, OMP dashboard/read models. | Merge into V7 Certification Passport view. | NO | Coverage is a view over maturity/history, not a separate truth source. |
| Blast Radius Contract | OMP A5 historical blast-radius certification, B14 service/pool/cohort blast-radius scope, Authority Budget. | Extend existing blast-radius and Authority Budget semantics for controlled certification. | NO | Existing owners already define blast-radius constraints. |
| Certification Recovery Contract | Execution Mission Protocol, Runtime rollback, OMP continuation, Production Maturity. | Reuse Execution Mission recovery and specialize for certification stages. | NO | Recovery law already exists; certification only adds stage-specific cases. |
| V7 Certification Passport | Production Maturity, Current Program State, OMP dashboard/read models, Engineering Reports. | Keep as Production Maturity / CPS view over Certification History. | NO | Standalone Passport would duplicate maturity/CPS truth; view is sufficient. |
| Program Roadmap | OMP, Current Program State, Production Maturity. | Reuse OMP-style phase progression inside this program only. | NO | The roadmap is certification sequence, not a product roadmap. |
| Owner Mapping | SYSTEM_MAP, Current Program State, OMP. | Extend SYSTEM_MAP-style owner/consumer discipline inside this program. | NO | It maps remaining work to existing owners. |
| Controlled Production Environment | Certification Philosophy, Controlled Incident Design, Reality First, Production Maturity. | Extend this program's environment semantics; no separate environment owner. | NO | Environment is real production with controlled participants. |
| Reality Preservation Law | Reality First, Production Maturity, Engineering Principles, Execution Completion Protocol. | Extend existing Reality First law for certification. | NO | Existing law already forbids synthetic production proof. |
| Temporary Certification Incident | Controlled Incident Design, Incident Completion Contract, Certification Recovery. | Extend controlled incident semantics with cleanup. | NO | Temporary incident is a constrained incident type, not a new Incident owner. |
| Production Restoration Contract | Rollback / No-Rollback closure, Incident Completion Contract, Certification Recovery. | Extend cleanup and closure requirements. | NO | Cleanup belongs to existing assignment/routing/incident/authority owners. |
| Real Incident Preemption | OMP, Runtime safety, Authority Budget, Execution Mission recovery. | Extend recovery and operational procedure. | NO | Preemption is priority policy, not a new scheduler. |
| Certification Environment Lifecycle | Operational Procedure, Certification Automation Model, OMP, Production Maturity. | Extend existing lifecycle/procedure. | NO | Lifecycle sequences existing owners only. |
| Capability Earned Law | OMP, Authority, Production Maturity, Certification History. | Extend promotion semantics so configuration alone cannot enable capability. | NO | Existing owners already own certification, authority recognition, and maturity acceptance. |
| Capability Evolution Model | OMP Capability Production Contract, Authority Evolution, Production Maturity, Current Program State. | Extend existing capability progression for governed batch certification. | NO | Existing OMP/Authority/Maturity loop owns evolution. |
| Execution Priority Law | OMP, Production Maturity, Current Program State, Certification History, Passport, Engineering Reports, Execution Mission Protocol, Execution Completion Protocol. | Extend capability progression so Capability Producers create capability before consumer synchronization. | NO | This corrects execution order and creates no new owner. |
| Consumer Synchronization | OMP, Production Maturity, Current Program State, Passport, Engineering Reports, Dashboard projections. | Treat consumer updates as post-capability synchronization unless a safety owner blocks. | NO | Consumers consume reality; they do not create capability. |
| Synchronization Debt | OMP, Production Maturity, Current Program State, Passport, Engineering Reports. | Extend debt semantics to consumer synchronization gaps. | NO | Synchronization Debt is an evidence classification, not a new work owner. |
| Certification Mission Contract | Execution Mission Protocol, Certification Reports, OMP. | Reuse mission discipline and specialize required fields for certification. | NO | Execution Mission already owns mission continuity. |
| Reality Creation Law | Reality First, Controlled Production Environment, Controlled Incident Design. | Extend Reality First to require controlled real production conditions. | NO | Existing production owners can create legal controlled conditions. |
| Controlled Evidence Generation Law | Reality Creation Law, Controlled Production Environment, Controlled Incident Design, Certification Mission Contract, OMP, Authority, Production Maturity. | Extend existing controlled certification semantics so missing stage evidence triggers a legal controlled evidence decision before HOLD. | NO | It is a decision rule over existing owners, not a new evidence owner or certification system. |
| Certification Infrastructure Sufficiency Law | Certification Pool Design, Certification Users, Certification Groups, Controlled Production Environment, Reality First, OMP, Production Maturity. | Extend existing pool semantics so insufficient Certification Users trigger legal pool expansion or explicit HOLD before stage execution. | NO | It is a sufficiency rule over existing user/pool owners, not a new user owner or certification infrastructure. |
| Certification Infrastructure Responsibility Principle | Certification Infrastructure Sufficiency Law, Certification Pool Design, OMP, Production Maturity, Owner Mapping. | Extend the sufficiency law so infrastructure maintenance is continuous and proactive, not only stage-start preparation. | NO | It clarifies permanent responsibility inside the existing certification program. |
| Owner Resolution Law | Execution Completion Protocol, Reality First, OMP, Production Maturity, SYSTEM_MAP, Owner Mapping, Certification Recovery, Certification Evidence Decision, Certification Pool Decision, Engineering Reports, Current Program State. | Extend existing recovery and owner-mapping discipline so a Blocking Owner is investigated until terminal classification. | NO | It is a continuation rule over existing owners, not a new owner or execution path. |
| Production Certification Principle | Certification Philosophy and Controlled Production Environment. | Merge as the permanent principle behind controlled production certification. | NO | It is philosophy, not a new owner or artifact. |
| Certification Philosophy Summary | This document, OMP, Production Maturity, Authority, Engineering Reports. | Summarize existing laws and contracts. | NO | Summary creates no new behavior. |
| Continuous Automation Evolution | OMP, Production Maturity, Execution Mission Protocol, Execution Completion Protocol, SYSTEM_MAP, Current Program State, Reality First, V7 Autonomous Execution Program. | Extend each certification mission with mandatory Automation Gap review and owner-mapped Automation Candidates. | NO | Automation evolution is a property of certification evidence, not a separate program or owner. |
| Automation Debt Metric | OMP, Production Maturity, Current Program State, Passport view, Engineering Reports. | Extend existing evidence and maturity views with current/created/closed/remaining/trend fields. | NO | The metric is a view over manual-work evidence, not a new metric owner. |
| Workflow Evolution | OMP, Production Maturity, Execution Mission Protocol, Execution Completion Protocol, SYSTEM_MAP, Current Program State, Reality First, Automation Evolution, Owner Mapping. | Extend Continuous Automation Evolution with workflow-level audit and Pipeline Candidates. | NO | Workflow evolution is a property of certification evidence, not a separate orchestration program. |
| Pipeline Candidate | OMP, Production Maturity, SYSTEM_MAP, Engineering Reports, Current Program State. | Extend Automation Candidate semantics to workflow orchestration. | NO | Pipeline Candidates are evidence and next-action inputs, not authority grants or a new owner. |

No new canonical owner is created by this document.

## 43. Program Roadmap

This is a certification roadmap, not a product roadmap. It describes the certification path for this program and remains subordinate to OMP, Authority, Production Maturity, and existing owner evidence.

Capability evolution and Certification Infrastructure evolution progress together. The certification ladder should never significantly outgrow the Certification Pool. As each stage approaches readiness, the program must verify that Certification Users, Certification Groups, Certification Pools, Controlled Production readiness, and restoration capacity are already evolving toward the next planned stages whenever practical.

| Phase | Meaning | Entry criteria | Exit criteria | Required evidence |
| --- | --- | --- | --- | --- |
| Phase 0: Program complete | The canonical certification program document is structurally complete. | Document reviewed; no unresolved structural gaps. | Program accepted as canonical certification reference. | This document and final engineering review report, including Automation Audit and Workflow Audit readiness. |
| Phase 1: Owner Mapping | Every remaining implementation bridge is mapped to an existing owner. | Program complete. | Every open item has Owner, Artifact, Consumer, and Status. | Owner Mapping table with no ownerless item, including Automation Debt and Workflow Debt ownership. |
| Phase 2: CANARY Stability | One-user governed execution remains stable enough for Stage 1 review. | CANARY certified; no regression required. | `CANARY_STABLE`. | Multiple governed one-user outcomes or owner-accepted evidence set; no incident/retry/runtime/restore/verification/rollback regression; manual work classified; Automation Debt and Workflow Debt evidence recorded. |
| Phase 3: SMALL_BATCH Certification | Certify Stage 1 governed batch. | CANARY_STABLE; Authority allows SMALL_BATCH; Certification Evidence Decision selects sufficient real evidence or legal Controlled Production; Certification Pool Decision confirms enough users or legal expansion. | SMALL_BATCH `PASS` or deterministic `FAIL/HOLD`. | Stage 1 producer evidence, per-user verification, rollback/no-rollback closure, Certification Evidence Decision, Certification Pool Decision, Automation Audit output, Workflow Audit output, and consumer synchronization or Synchronization Debt. |
| Phase 4: MEDIUM_BATCH Certification | Certify Stage 2 governed batch. | SMALL_BATCH certified; Authority allows MEDIUM_BATCH; Certification Evidence Decision selects sufficient real evidence or legal Controlled Production; Certification Pool Decision confirms enough users or legal expansion. | MEDIUM_BATCH `PASS` or deterministic `FAIL/HOLD`. | Stage 2 report, complete batch evidence, Certification Evidence Decision, Certification Pool Decision, Automation Audit output, and Workflow Audit output. |
| Phase 5: LARGE_BATCH Certification | Certify Stage 3 governed batch. | MEDIUM_BATCH certified; Authority allows LARGE_BATCH; Certification Evidence Decision selects sufficient real evidence or legal Controlled Production; Certification Pool Decision confirms enough users or legal expansion. | LARGE_BATCH `PASS` or deterministic `FAIL/HOLD`. | Stage 3 report, complete batch evidence, Certification Evidence Decision, Certification Pool Decision, Automation Audit output, and Workflow Audit output. |
| Phase 6: XLARGE_BATCH Certification | Certify Stage 4 governed batch. | LARGE_BATCH certified; Authority allows XLARGE_BATCH; Certification Evidence Decision selects sufficient real evidence or legal Controlled Production; Certification Pool Decision confirms enough users or legal expansion. | XLARGE_BATCH `PASS` or deterministic `FAIL/HOLD`. | Stage 4 report, complete batch evidence, Certification Evidence Decision, Certification Pool Decision, Automation Audit output, and Workflow Audit output. |
| Phase 7: FULL_INCIDENT Certification | Certify same-incident full evacuation. | XLARGE_BATCH certified; Authority explicitly allows FULL_INCIDENT; Certification Evidence Decision selects sufficient real evidence or legal Controlled Production; Certification Pool Decision confirms enough users or legal expansion where controlled users are required. | FULL_INCIDENT `PASS` or deterministic `FAIL/HOLD`. | All remaining same-incident users handled through governed path with complete closure, Certification Evidence Decision, Certification Pool Decision, Automation Audit output, and Workflow Audit output. |
| Phase 8: Routine Production Operation | Certified governed evacuation is routine under current authority. | FULL_INCIDENT certified and Authority recognizes the maturity state. | Ongoing operation with regression controls. | Certification History, Passport view, regression checks, Synchronization Debt state, Automation Debt trend, Workflow Debt trend, and production outcomes. |

Each phase can stop only through this document's exit, demotion, recovery, evidence-decision, pool-decision, or regression rules. No phase may promote on elapsed time alone. A phase may not enter HOLD for missing evidence until it has first determined whether Controlled Production can legally generate that evidence. A phase may not enter HOLD for insufficient Certification Users until it has first determined whether the Certification Pool can be legally expanded.

## 44. Owner Mapping

The program requires these implementation bridge items to be verified or implemented through existing owners:

| Item | Owner | Artifact | Consumer | Status |
| --- | --- | --- | --- | --- |
| Certification Group representation | Existing user registry, group/org policy owner, Planner policy gate. | Certification group marker or existing policy field. | Planner, Authority, OMP, Production Maturity. | NEEDED_IMPLEMENTATION |
| Certification Pool Decision | Existing user registry, group/org policy owner, assignment owner, OMP, Production Maturity. | Decision record proving pool sufficient, pool expanded, Owner Resolution required, or canonical impossibility. | Program Roadmap, Certification Reports, Current Program State, Passport view. | NEEDED_IMPLEMENTATION |
| Certification Pool expansion procedure | Existing user registry, account provisioning, group/org policy, assignment, routing, OMP, Production Maturity. | Legal procedure to create/register/designate real Certification Users and assign them to Certification Groups. | Certification Readiness, Controlled Incident Design, Certification Reports. | NEEDED_IMPLEMENTATION |
| Controlled source setup procedure | Existing assignment owner, egress registry owner, Wake/Observation owners. | Controlled source setup runbook or owner invocation. | Wake, Incident, Planner, Certification Reports. | NEEDED_IMPLEMENTATION |
| Legal controlled source degradation procedure | Existing observation/egress health owner and policy owner. | Legal degradation or failure materialization procedure. | Wake, Incident, OMP, Production Maturity. | NEEDED_OWNER_DECISION |
| Owner Resolution record | OMP, Production Maturity, SYSTEM_MAP, Owner Mapping, Engineering Reports, Current Program State. | Blocking Owner, investigation evidence, terminal classification, Required Resolution, and reason no further investigation is necessary. | Certification Recovery, Certification Reports, Program Roadmap, Current Program State, Passport view. | NEEDED_IMPLEMENTATION |
| Certification Evidence Decision | OMP, Authority, Production Maturity, Controlled Production Environment, Certification Mission Contract. | Decision record selecting sufficient real production evidence, legal Controlled Production, Owner Resolution required, missing implementation, or CANONICAL_IMPOSSIBILITY. | Program Roadmap, Certification Reports, Current Program State, Passport view. | NEEDED_IMPLEMENTATION |
| Authority promotion command or procedure | Existing Authority owner and OMP. | Stage promotion decision record or command. | Governed owner, Planner, Runtime, Certification Passport view. | NEEDED_IMPLEMENTATION |
| Stage certification owner invocation | Existing governed L3 owner. | Documented invocation for each authorized stage. | Runtime Apply, Verification, Rollback, Reports. | NEEDED_DOCUMENTATION |
| Batch feedback and learning shape | Existing Learning / Feedback owner. | Per-user feedback record and incident-level summary. | OMP, Production Maturity, Passport view. | NEEDED_IMPLEMENTATION |
| Consumer synchronization record | OMP, Production Maturity, Current Program State, Passport view, Engineering Reports. | Synchronized, intentionally delayed, blocked by safety owner requiring Owner Resolution, no-change, or invalid-evidence decision. | Current Program State, Passport view, Program Roadmap. | NEEDED_IMPLEMENTATION |
| Admin UI visibility | Existing Admin UI / OMP dashboard/read-model owners. | Certification status view if needed. | Operators, OMP, CPS. | OPTIONAL_NEEDED_IF_UI_GAP_EXISTS |
| Fewer remaining users than stage budget | Planner / Authority / OMP policy owners. | Rule confirming smaller same-incident batch can certify when fewer users remain. | Planner, Authority, Certification Reports. | NEEDED_OWNER_DECISION |
| FULL_INCIDENT authorization representation | Authority owner and OMP. | Explicit FULL_INCIDENT authority envelope. | Governed owner, Restore Barrier, Runtime, Certification Reports. | NEEDED_IMPLEMENTATION |
| Certification History storage location | Engineering Report lifecycle; OMP report index if present. | Append-only certification report set and optional index pointer. | OMP, Production Maturity, Passport view. | OWNER_REUSED_STORAGE_TO_DEFINE |
| V7 Certification Passport storage/update | Production Maturity and Current Program State. | Passport view / maturity projection over Certification History. | Operators, OMP, Dashboard read models. | OWNER_REUSED_VIEW_TO_DEFINE |
| Regression Certification trigger mapping | OMP, Production Maturity, deployment/report lifecycle. | Regression trigger matrix bound to owner changes. | Passport view, Program Roadmap, Certification Reports. | PARTIALLY_DEFINED |
| Coverage Matrix publication | Production Maturity / Current Program State read model. | Coverage table inside Passport view. | OMP, operators, Dashboard. | OWNER_REUSED_VIEW_TO_DEFINE |
| Certification source preparation | Existing egress registry / assignment / observation owners. | Preparation procedure for controlled source. | Wake, Incident, Planner, Reports. | NEEDED_IMPLEMENTATION |
| Production Restoration cleanup | Existing assignment, routing, incident, authority, and report owners. | Cleanup procedure and restoration evidence. | Certification Reports, OMP, Production Maturity. | NEEDED_IMPLEMENTATION |
| Real Incident Preemption handling | OMP, Authority, Runtime safety, governed owner. | Pause/resume/release-resource rule and evidence. | Operators, OMP, Certification Recovery. | NEEDED_OWNER_DECISION |
| Automation Gap Review | OMP, Production Maturity, Execution Mission Protocol, Engineering Reports. | Manual-action classification table in every certification report. | OMP, Production Maturity, Current Program State. | NEEDED_DOCUMENTATION |
| Automation Candidate tracking | OMP, Production Maturity, SYSTEM_MAP, Engineering Reports. | Owner-mapped candidate rows with terminal states. | OMP roadmap, Production Maturity, future certification missions. | NEEDED_IMPLEMENTATION |
| Automation Debt Metric | OMP, Production Maturity, Current Program State, Certification Passport view, Engineering Reports. | Current, created, closed, remaining, and trend projection over manual-work evidence. | OMP, Production Maturity, operators, future certification missions. | NEEDED_IMPLEMENTATION |
| Workflow Audit Review | OMP, Production Maturity, Execution Mission Protocol, Engineering Reports. | Manual workflow classification table in every certification report. | OMP, Production Maturity, Current Program State. | NEEDED_DOCUMENTATION |
| Pipeline Candidate tracking | OMP, Production Maturity, SYSTEM_MAP, Engineering Reports. | Owner-mapped pipeline candidate rows with terminal states. | OMP roadmap, Production Maturity, future certification missions. | NEEDED_IMPLEMENTATION |
| Workflow Debt Metric | OMP, Production Maturity, Current Program State, Certification Passport view, Engineering Reports. | Current, created, closed, remaining, and trend projection over workflow evidence. | OMP, Production Maturity, operators, future certification missions. | NEEDED_IMPLEMENTATION |
| Synchronization Debt | OMP, Production Maturity, Current Program State, Certification Passport view, Engineering Reports. | Consumer synchronization gap table with terminal states. | OMP, Authority, Production Maturity, operators, future certification missions. | NEEDED_IMPLEMENTATION |

These items are not new architecture by default. Each must remain mapped to existing owners before any implementation is proposed.

## 45. Certification Philosophy Summary

The permanent philosophy of the program is:

- Reality First: only real controlled production execution can certify production behavior.
- Discover -> Reuse -> Extend -> Create: every concept must reuse existing owners unless impossibility is proven.
- Capability Earned: capability is earned through certification and Authority recognition, not configuration.
- Execution Priority: real capability producers create capability before documentation, Passport, Current Program State, OMP, or Production Maturity projections synchronize.
- Controlled Production: certification creates controlled real production conditions for certification users only.
- Reality Creation: V7 must create repeatable real production certification conditions rather than wait for random incidents.
- Controlled Evidence Generation: missing stage evidence first triggers a decision to use real evidence or legally generate controlled evidence; waiting for random incidents is fallback only after safety, impossibility, or missing implementation is proven.
- Certification Infrastructure Sufficiency: missing Certification Users first trigger a pool sufficiency decision and legal pool expansion when allowed; waiting for ordinary production scale is not a certification strategy.
- Certification Infrastructure Responsibility: the program maintains both certified capabilities and the Certification Infrastructure required to certify future capabilities; infrastructure evolves together with capability evolution.
- Owner Resolution: no Blocking Owner is a final explanation; every owner block must terminate as policy prohibition, missing implementation, missing invocation, implementation defect, or canonical impossibility.
- Reality Preservation: production must return logically to its pre-certification state, with only historical evidence remaining.
- Evidence Before Promotion: no stage can promote without complete persisted production evidence.
- Authority Before Scale: Authority Budget controls every batch size and blast radius.
- Production Restoration: cleanup is required before certification can complete.
- Blast Radius Control: certification never crosses incidents, users, or current Authority Budget.
- No Artificial Success: fake Planner, Runtime, Verification, Rollback, Learning, Authority, Restore Barrier, Incident, or production evidence is forbidden.
- Certification History: every attempt is append-only historical engineering evidence.
- Passport: proven capability is exposed as a Production Maturity / Current Program State view, not a new truth source.
- Regression: certified stages return to regression-required when owner, contract, evidence, or safety changes require it.
- Capability Evolution: the system collects evidence, proves stability, earns capability, receives Authority recognition, and only then may production use it.
- Continuous Automation Evolution: every certification mission must classify manual work and create owner-mapped Automation Candidates when automation is justified.
- Automation Debt: no manual action may remain unclassified, and no certification mission is fully complete while unnecessary manual work remains unexplained.
- Workflow Evolution: every certification mission must classify manual workflows and create owner-mapped Pipeline Candidates when orchestration can be safely simplified.
- Command Minimization: repeated command chains must be investigated as workflow debt, not accepted as permanent operator practice.

## 46. Final Engineering Review

Quality assessment:

```text
9 / 10
```

Final quality assessment:

| Area | Score | Reason |
| --- | ---: | --- |
| Architecture Quality | 10 / 10 | No new Runtime, Planner, Authority, owner, execution path, truth source, or architecture is created. |
| Engineering Quality | 9 / 10 | Contracts are explicit and owner-mapped; remaining gaps are implementation bridge details. |
| Canonical Quality | 10 / 10 | Concepts are defined, integrated, and tied to existing canon. |
| Long-term Maintainability | 9 / 10 | History, Passport view, regression, owner mapping, and mission contracts provide durable maintenance paths. |
| Future Extensibility | 10 / 10 | Capability Earned and Capability Evolution generalize beyond current numeric ladder values. |
| Overall | 9.6 / 10 | Document is canonical; remaining work is production certification and concrete owner invocation, not document structure. |

Real remaining weaknesses:

- Owner Mapping still contains implementation bridge items that need concrete owner invocation, storage, or command shape.
- Certification Evidence Decision is canonical but still needs concrete owner invocation and report projection.
- Certification Pool Decision and pool expansion procedure are canonical but still need concrete owner invocation and report projection.
- Owner Resolution is canonical but still needs concrete report projection, owner invocation shape, and Current Program State / Passport view fields.
- Certification History storage is owner-reused but the exact index or pointer location still needs definition.
- The Passport is correctly scoped as a Production Maturity / CPS view, but its exact rendered location still needs definition.
- Production Restoration and Real Incident Preemption now have canonical rules but still need concrete owner invocation.
- Automation Gap Review is now canonical but still needs concrete report indexing and consumer synchronization shape.
- Automation Debt Metric is canonical but still needs concrete Passport / Current Program State projection shape.
- Workflow Audit Review and Pipeline Candidate tracking are canonical but still need concrete report indexing and consumer synchronization shape.
- Workflow Debt Metric is canonical but still needs concrete Passport / Current Program State projection shape.
- Synchronization Debt is canonical but still needs concrete report indexing and Passport / Current Program State projection shape.
- Stage 1 and higher certification remain `NOT_CERTIFIED` until real controlled production evidence exists.

No meaningful structural weakness remains in the document itself. Remaining work is implementation bridge and production certification, not canonical program design.

## 47. Final Rule

The program is complete only when V7 can certify controlled production evacuation up to FULL_INCIDENT without operator hand-holding, while preserving all existing owners and safety gates.

Until then, each stage remains uncertified unless real controlled production evidence proves it through the canonical governed execution path.
