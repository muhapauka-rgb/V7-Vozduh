# V7 Master Project Handoff

Status: `CANONICAL ENTRY POINT`
Owner: OMP / Canonical Reference / Current Program State
Last updated: 2026-07-03
Current branch: `Updatesystem`
Latest known production-aligned code commit: `66a276e9d805b12871f37e6fcc92d9376a4a45b3`
Latest known local/GitHub handoff commit before this operating-system update: `baddbbe8`

This document is the canonical first document for any future Codex instance
working on V7.

Assume all previous conversations are lost. Read this document first. Then use
the referenced canonical owners and current evidence to resume the project
without inventing a parallel architecture, roadmap, Runtime, Planner, Authority,
truth source, or execution path.

## 1. Project Purpose

V7 is no longer merely "a VPN".

V7 is a governed production routing platform. Its product purpose is to keep
users online by detecting failed or degraded connectivity, selecting legal
targets, moving users through bounded authority, verifying outcomes, rolling
back or closing safely, learning from the result, and increasing certified
automation only after production evidence proves that the next capability is
safe.

The core product is invisible reliable routing. The user should not need to
understand whether their traffic uses OpenVPN, WireGuard, VLESS, or another
channel. V7's responsibility is to observe reality, make a safe governed
decision, execute through existing owners, verify the outcome, and improve.

The project now revolves around:

- real production evidence;
- safety-bounded authority;
- controlled production certification;
- capability earned through execution, not configuration;
- no duplicate owners;
- continuous automation evolution;
- workflow orchestration evolution;
- engineering automation that improves how V7 itself is built.

## 2. Project Philosophy

These principles are permanent unless a canonical owner changes them through
the existing architecture process.

### Reality First

Real production reality overrides synthetic examples, guesses, report-only
claims, stale artifacts, and planner-only assumptions. Mocks and dry runs can
explain or prepare. They cannot certify production capability.

### Discover -> Reuse -> Extend -> Create Only If Necessary

Every change starts by discovering the existing owner. Reuse that owner if it
can express the capability. Extend it if a minimal owner-bounded extension is
enough. Create a new owner only after proving no existing canonical owner can
own the behavior.

### Capability Earned

Capability is not granted by a constant, a config value, or a document. It is
earned when production execution proves that the existing chain can perform the
capability safely and Authority recognizes it.

### Execution Priority

Reality and capability producers come first. Documentation, Passport, OMP,
Production Maturity, Current Program State, dashboards, and reports synchronize
with earned reality afterward unless an existing safety owner proves that
synchronization is required before safe continuation.

### Owner Resolution

A blocking owner is never the final explanation. If an owner blocks execution,
investigate until the block is classified as:

- `POLICY_PROHIBITION`
- `IMPLEMENTATION_MISSING`
- `OWNER_INVOCATION_MISSING`
- `IMPLEMENTATION_DEFECT`
- `CANONICAL_IMPOSSIBILITY`

All states except canonical impossibility become the next engineering mission.

### Controlled Production

Certification uses real production owners and real production execution
contracts, but against dedicated Certification Users and controlled incidents
when ordinary production incidents are unavailable or unsafe to use.

### Controlled Evidence Generation

If required certification evidence is missing, V7 must decide whether it can
legally create real controlled production evidence. Waiting for random
production incidents is a fallback, not the default strategy.

### Certification Infrastructure

Certification Users, Certification Groups, Certification Pools, controlled
source readiness, and restoration readiness are permanent production assets of
the certification program. The certification ladder must not outgrow the
Certification Pool.

### Automation Evolution

Every manual action triggers an Automation Audit. Unexplained manual work is
Automation Debt until it becomes automated, intentionally manual, blocked by
future capability, not cost effective, or canonically impossible.

### Workflow Evolution

Every repeated manual workflow triggers a Workflow Audit. Unexplained manual
orchestration is Workflow Debt until it becomes a governed pipeline,
intentionally manual, blocked by future capability, not cost effective, or
canonically impossible.

### Engineering Reports

Engineering Reports preserve evidence. They do not become roadmaps, truth
sources, or owners. Reports are consumed by OMP, Production Maturity, Current
Program State, canonical owners, and future investigations.

### Canonical Knowledge

Durable rules live in exactly one canonical owner. `SYSTEM_MAP` is an ownership
lookup, not a second truth source. Engineering Reports are historical evidence.

### OMP

OMP is the operating program. It decides continuation, consumes capability and
evidence, maps work to existing owners, and prevents duplicate roadmaps,
parallel queues, and ownerless work.

### No Duplicate Owners

Do not create duplicate Runtime, Planner, Authority, Restore Barrier, Wake,
Packet, Truth Source, Event Bus, OMP, or execution path.

### Continuous Process

Every process ends by becoming input to another process:

```text
Reality -> Evidence -> Capability -> Authority -> Production
  -> Certification -> Automation Audit -> Workflow Audit -> Next Mission
```

## 3. System Architecture

The current architecture is an evidence-driven governed routing control plane.

Canonical production chain:

```text
Observation
  -> Wake
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
  -> Authority Recognition
  -> Next Certification Mission
```

### Major Owners

| Owner | Responsibility |
| --- | --- |
| Observation | Produce real evidence about egress state, service health, quality, route state, and source failure. |
| Wake | Convert legal real evidence into an allowed execution wake source. Timer, cron, blind polling, and synthetic wake are not authority by themselves. |
| Incident | Materialize the failed-source incident and preserve `incident_source` while the source remains failed and affected users remain. |
| Planner | Select eligible users and targets under incident, service, quality, load, safety, policy, retry, and identity constraints. |
| Authority | Bound blast radius, approve class/budget, promote/demote capability, and reject unauthorized execution. |
| Approved Plan Lock | Preserve the committed selected move identity that Authority approved. |
| Restore Barrier | Validate committed move identity, generation, source, target, count, and hash before Runtime Apply. |
| Runtime Apply | Mutate production routing only for the committed approved batch. |
| Verification | Verify route and required service success for every moved user. |
| Rollback / No-Rollback | Roll back, contain, or close no-rollback for every touched user. |
| Learning / Feedback | Materialize outcome, trust, prediction, recommendation, and closure evidence. |
| Production Restoration | Restore temporary certification topology and preserve historical evidence. |
| OMP | Drive continuation, owner mapping, maturity consumption, capability progression, and no-duplication discipline. |
| Production Maturity | Consume certified evidence and update production-readiness state. |
| Current Program State | Preserve volatile current state and next action. |
| Engineering Reports | Preserve historical proof, not live authority. |
| SYSTEM_MAP | Own lookup and relationships, not implementation or truth. |

### Capability Producers

Capability Producers are owners whose successful production completion creates
capability evidence: Observation, Wake, Incident, Planner, Authority, Approved
Plan Lock, Restore Barrier, Runtime Apply, Verification, Rollback /
No-Rollback, Production Restoration, and any required existing safety owner.

### Capability Consumers

Capability Consumers consume earned capability. They do not create it:
Certification History, Passport view, OMP, Production Maturity, Current Program
State, Coverage Matrix, Engineering Reports, dashboards, Automation Debt views,
and Workflow Debt views.

### Runtime Path

Runtime is not a planner and not a truth source. Runtime consumes committed
approved identity and either applies it safely or stops. It must not recompute
a different selected move, bypass Authority, bypass Restore Barrier, or mutate
outside the approved batch.

### Authority Path

Authority is the blast-radius and capability boundary. It owns the current
allowed budget, promotion rules, evidence windows, confirmation requirements,
demotion/hold behavior, and policy prohibitions.

### Certification Path

Certification proceeds through controlled production stages:

```text
CANARY=1 -> SMALL_BATCH=5 -> MEDIUM_BATCH=10
  -> LARGE_BATCH=25 -> XLARGE_BATCH=50 -> FULL_INCIDENT
```

Each stage must use the same production chain. Larger stages do not create new
execution paths; they increase authorized maximum users only after evidence
supports promotion.

### Automation And Workflow Paths

Manual actions and repeated workflows are not ignored. They become Automation
Debt or Workflow Debt and feed future automation/pipeline work through existing
owners.

### Engineering Path

Engineering work is:

```text
Breakpoint
  -> Owner Resolution
  -> Implementation Mission
  -> Patch existing owner
  -> Tests
  -> Regression
  -> Safe Deploy
  -> Truth / Convergence
  -> Resume interrupted certification phase
```

## 4. Project Evolution

The project evolved conceptually, not simply chronologically.

### Initial VPN

The first shape was a connectivity system with users assigned to channels. That
was not enough: a VPN can carry traffic, but it does not by itself prove safe
automatic restoration when channels fail.

### Governed Runtime

V7 introduced bounded execution through existing owners: selected moves,
authority envelopes, packets, approved locks, restore barriers, runtime apply,
verification, rollback, and learning. This solved the problem of unsafe
mutation and made execution auditable.

### Capability Certification

The system then needed proof that capabilities are real. Certification replaced
"configuration means capability" with "production evidence earns capability".
This made Authority expansion evidence-based.

### Controlled Production

Waiting for random incidents at exact sizes was too slow and unsafe. Controlled
Production lets V7 create real production conditions with dedicated
Certification Users and controlled failed-source incidents while preserving
Reality First.

### Automation Evolution

As manual operator work appeared, V7 made each manual action evidence for
future automation. The goal is to reduce unnecessary manual effort without
weakening safety.

### Workflow Evolution

Repeated sequences of manual commands became workflow objects. The goal is not
just automating commands; it is replacing unnecessary orchestration with one
governed pipeline when safety and ownership permit.

### Engineering Automation

Engineering itself is becoming a governed pipeline. Every breakpoint, fix,
test, deploy, convergence check, report, audit, and certification resume should
make both V7 and the V7 engineering system stronger.

Obsolete ideas:

- "V7 is a VPN."
- "A report is enough to complete work."
- "Finding a blocker is the mission."
- "A configured value grants authority."
- "Timer or cron is legal wake authority by itself."
- "A new owner is acceptable before existing-owner proof."

## 5. Current Certification State

Current canonical certification ladder:

| Stage | Capability | Max users | Current state |
| --- | --- | ---: | --- |
| Stage 0 | CANARY | 1 | CERTIFIED |
| Stage 1 | SMALL_BATCH | 5 | CERTIFIED |
| Stage 2 | MEDIUM_BATCH | 10 | CERTIFIED |
| Stage 3 | LARGE_BATCH | 25 | CERTIFIED |
| Stage 4 | XLARGE_BATCH | 50 | HOLD |
| Stage 5 | FULL_INCIDENT | all remaining same-incident affected users | NOT REACHED |

### Already Proven

- Observation -> Wake bridge can create legal `confirmed_current_channel_failure` from real failed source evidence.
- Governed trigger and heartbeat path can invoke the existing governed L3 owner.
- Incident source continuity preserves the failed-source identity across cycles.
- Retry-aware continuation excludes exhausted semantic attempts and selects remaining eligible users.
- Approved Plan Lock, packet identity, Restore Barrier, and Runtime Apply can preserve committed selected move identity.
- Telegram sentinel lock scope was reduced enough to avoid prior verification timeout behavior.
- Verification and no-rollback closure work for bounded governed execution.
- CANARY, SMALL_BATCH, MEDIUM_BATCH, and LARGE_BATCH controlled production certifications have passed.
- Phase 4 MEDIUM_BATCH moved 10 users from `wireguard-1779454504-c43409` with verification PASS.
- Phase 5 LARGE_BATCH moved 25 users from `wireguard-1779454504-c43409` with verification PASS.
- A second 25-user LARGE_BATCH evidence run for Phase 6 moved users `10.7.0.51` through `10.7.0.75` with verification PASS and no rollback.
- The latest Authority owner continuity fix is deployed and converged at commit `66a276e9d805b12871f37e6fcc92d9376a4a45b3`.
- The latest handoff/report commit before this document is `91ec1e2b`.

### Not Yet Proven

- `XLARGE_BATCH=50` execution has not yet certified.
- `FULL_INCIDENT` execution has not yet certified.
- Routine production operation after FULL_INCIDENT is not yet reached.
- The repeated manual Phase 6 preparation/readiness workflow is not yet a single governed pipeline.

### Current Phase And Blocker

Current Phase:

```text
Phase 6: XLARGE_BATCH Certification
```

Current terminal state:

```text
HOLD
```

Current hold reason:

```text
Authority requires a 3600 second no-regression window before promotion from
canonical LARGE_BATCH=25 to XLARGE_BATCH=50.
```

At the latest readiness check:

- Run 1 operation: `runtime_autoswitch_d2fc48ffe5590c23e2ac8950`
- Run 1 users: `10.7.0.26` through `10.7.0.50`
- Run 1 observed stability: 1717s / 3600s
- Run 2 operation: `runtime_autoswitch_ffddc0afb57b4b2a6cd4e560`
- Run 2 users: `10.7.0.51` through `10.7.0.75`
- Run 2 observed stability: 183s / 3600s
- Both runs had complete feedback and closure.
- The remaining blocker was `xlarge_batch_evidence_validation_failed` because
  the stability window was immature.
- The diagnostic also reported `missing_explicit_authority_promotion_confirmation`,
  which is expected for a readiness probe.

Current next action:

Re-check Authority promotion readiness after both evidence operations have
`stability_window_observed_seconds >= 3600`. If no regression appears, use the
existing Authority owner with explicit confirmation to promote to
`XLARGE_BATCH`, then resume Phase 6 and run the existing governed L3 owner with
`--max-users 50` against the controlled incident source.

## 6. Engineering Program

Engineering work now follows the execution-completion shape:

```text
Breakpoint
  -> freeze exact state
  -> identify producer
  -> identify consumer
  -> identify owner
  -> identify exact condition
  -> prove why STOP occurred
  -> classify blocker
  -> Owner Resolution
  -> Implementation Mission if needed
  -> Patch existing owner
  -> Tests
  -> Regression Certification
  -> Safe Deploy
  -> Truth / Convergence
  -> Resume interrupted phase
  -> Capability Earned
```

Implementation defects are not architecture defects by default. If a canonical
contract is clear and existing code fails to honor it, patch the existing owner.
Only if implementation proves that the architecture itself cannot express the
required legal behavior should Codex stop implementation and update the
canonical document first.

Engineering missions are created from current blockers:

- `IMPLEMENTATION_DEFECT` becomes a correction mission against the existing owner.
- `IMPLEMENTATION_MISSING` becomes a minimal extension mission.
- `OWNER_INVOCATION_MISSING` becomes an owner invocation/pipeline mission.
- `POLICY_PROHIBITION` becomes a hold or policy decision.
- `CANONICAL_IMPOSSIBILITY` is the only permanent stop.

The certification program continues after implementation. A patch is not a
terminal outcome. Tests are not terminal. Deploy is not terminal. The phase is
resumed and must reach PASS, HOLD, BLOCKED, or CANONICAL_IMPOSSIBILITY.

## 7. Engineering Operating System

The Engineering Operating System describes how V7 engineering work is
performed. It is separate from architecture, Runtime, Planner, Authority, and
Certification. It tells future Codex instances how to think, investigate,
communicate, and execute inside the existing V7 philosophy.

### Engineering Thinking Rules

Always investigate implementation before architecture. Most failures are
owner-contract implementation defects, missing invocation, missing persistence,
or policy blocks. Architecture change is the last option.

Always find the earliest producer that violates a contract. Symptoms usually
appear downstream. The root cause is the first broken invariant, not the first
visible STOP.

Never repair downstream before proving upstream is correct. If Runtime stops,
prove whether Planner, Authority, Approved Plan Lock, Restore Barrier, packet,
and committed selected move identity were correct first. If Planner looks
wrong, prove whether Observation, Wake, Incident, policy, freshness, service
matrix, load, safety, and retry evidence were correct first.

Never fix symptoms. A blocker name, rollback reason, timeout, empty selected
move list, or STOP_SAFE is a symptom until its producer, consumer, owner,
contract, and first broken invariant are proven.

Always preserve semantic identity. Keep operation id, incident source,
planner generation, selected move hash, user, source, target, authority
generation, restore generation, packet id, and report lineage stable. Do not
switch to a newer, cleaner, easier, or more complete execution unless the
current execution is canonically impossible or explicitly restarted with proof.

Minimal existing-owner extension is preferred over new owners. Smaller bounded
changes are preferred over broad rewrites. Every implementation must preserve
existing contracts unless the canonical owner is intentionally updated first.

### Root Cause Methodology

Canonical investigation order:

```text
STOP
  -> Current Program State
  -> Production Evidence
  -> Payload
  -> Capability
  -> Owner
  -> Function
  -> Producer
  -> Consumer
  -> Contract
  -> First Broken Invariant
  -> Root Cause
  -> Owner Resolution
  -> Implementation Mission
  -> Patch
  -> Regression
  -> Deploy
  -> Truth
  -> Convergence
  -> Resume Interrupted Phase
```

Root cause is always earlier than symptoms. A rollback can be caused by
verification, but verification can be caused by stale evidence, lock contention,
wrong probe attribution, wrong selected user, wrong target, wrong packet,
Authority mismatch, Restore Barrier mismatch, or an upstream continuity break.
The investigation ends only when the first factual contract violation is found
or canonical impossibility is proven.

### Completion First Law

A capability is not complete because code exists.

A capability is not complete because tests pass.

A capability is not complete because documents exist.

A capability becomes complete only when it is:

- implemented;
- integrated;
- consumed;
- used by another real owner;
- producing outputs;
- having its outputs consumed;
- participating in an end-to-end production workflow;
- enabling the next capability.

Every capability must terminate by becoming the input of another capability.
No isolated capability is considered complete. Reports, patches, tests, deploys,
and root causes are intermediate states unless they feed the next real owner and
advance the current program.

### Execution Philosophy

Every blocker automatically becomes the next engineering mission.

Implementation defects are not reasons to stop. They become implementation
work through the existing owner.

Engineering missions continue until a terminal engineering outcome exists:

- the interrupted certification phase resumes and reaches its terminal state;
- an existing owner blocks by policy after Owner Resolution;
- implementation is missing and becomes the next mission;
- owner invocation is missing and becomes the next mission;
- canonical impossibility is proven.

Do not stop at "root cause found". Do not stop at "patch ready". Do not stop at
"tests pass". Do not stop at "deployed". Resume the interrupted phase.

### Project Communication Rules

Future Codex should communicate like an execution engineer:

- Prefer concise engineering communication.
- Lead with current phase, current owner, current blocker, evidence, and next
  legal step.
- Avoid unnecessary architecture discussion.
- Avoid unnecessary section proliferation.
- Avoid proposing replacement architectures.
- Avoid creating parallel roadmaps.
- Avoid creating unnecessary documents.
- Avoid suggesting new owners without proof.
- Avoid stopping investigation prematurely.
- Avoid asking the operator to perform work that existing owners can perform.
- Complete as much engineering work autonomously as safely possible.

Request operator intervention only when required by:

- Authority;
- Reality;
- Policy;
- Safety;
- Canonical Impossibility.

### Engineering Automation Vision

Engineering Automation is not another Runtime.

Engineering Automation is not another Planner.

Engineering Automation is not another Certification system.

It is the natural evolution of the Controlled Production Certification Program.
Its purpose is to automate engineering itself while preserving existing owners.

Canonical future pipeline:

```text
Breakpoint
  -> Owner Resolution
  -> Implementation Mission
  -> Patch
  -> Tests
  -> Regression
  -> Deploy
  -> Truth
  -> Convergence
  -> Resume
  -> Capability Earned
  -> Automation Audit
  -> Workflow Audit
  -> Engineering Improvement
  -> Next Engineering Mission
```

Every engineering mission must improve both:

1. the product;
2. the engineering system that develops the product.

### Engineering Memory

Important engineering discoveries must never remain only in reports or
conversation history.

Engineering Reports preserve history.

Canonical owners preserve truth.

Future Codex should search canonical knowledge before repeating
investigations. If a durable rule exists only in a report, promote it into the
single correct canonical owner. If a fact is only historical evidence, keep it
in reports and cite it rather than turning it into a competing truth source.

### Engineering Decision Hierarchy

Preferred solution order:

1. Reuse existing capability.
2. Reuse existing owner.
3. Extend existing owner.
4. Reuse existing workflow.
5. Create Pipeline Candidate.
6. Implement through existing owner.
7. Only then consider architecture change.

Architecture change is always the final option. It is allowed only when the
current architecture cannot legally express the required behavior after
existing-owner discovery and extension have failed with proof.

## 8. Automation Evolution

Automation Evolution is intrinsic to certification.

Loop:

```text
Manual Action
  -> Automation Audit
  -> Root Cause
  -> Existing Owner Investigation
  -> Automation Decision
  -> Automation Candidate if justified
  -> Implementation
  -> Certification
  -> Capability Earned
  -> Automation Gap Closed
```

Automation Debt terminal states:

- `AUTOMATED`
- `INTENTIONALLY_MANUAL`
- `BLOCKED_BY_FUTURE_CAPABILITY`
- `NOT_COST_EFFECTIVE`
- `CANONICAL_IMPOSSIBILITY`

Automation metrics must be consumable by OMP / Production Maturity / Current
Program State / Passport views:

- Current Automation Debt
- Automation Debt Created
- Automation Debt Closed
- Automation Debt Remaining
- Trend

Manual work is allowed when justified. Unexplained manual work is not allowed
to disappear.

## 9. Workflow Evolution

Workflow Evolution audits sequences of manual actions, not only individual
commands.

Loop:

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

Workflow Debt terminal states:

- `PIPELINE_IMPLEMENTED`
- `INTENTIONALLY_MANUAL`
- `CANONICAL_IMPOSSIBILITY`
- `NOT_COST_EFFECTIVE`
- `BLOCKED_BY_FUTURE_CAPABILITY`

The repeated current workflow is:

```text
restore controlled source
  -> create Certification Users
  -> mark certification scope
  -> degrade controlled source
  -> run governed validation
  -> collect closure
  -> collect registry readback
  -> re-check Authority promotion
```

This is a Pipeline Candidate, not a reason to stop certification.

## 10. Engineering Automation

Engineering Automation is the next evolution of the certification program. It
is not a separate product and not a new architecture.

Long-term target pipeline:

```text
Breakpoint
  -> Owner Resolution
  -> Root Cause
  -> Implementation Mission
  -> Patch
  -> Tests
  -> Regression
  -> Deploy
  -> Truth
  -> Convergence
  -> Resume Interrupted Certification Mission
  -> Capability Earned
  -> Automation Audit
  -> Workflow Audit
  -> Engineering Automation Improvement
  -> Next Engineering Mission
```

Every engineering mission should improve both:

1. V7 production capability.
2. The engineering system that develops V7.

The goal is that common certification engineering flows become governed
pipelines. This must happen through existing owners and certification, not by
adding hidden automation or bypassing safety.

## 11. Current Automation Status

Already automated or owner-callable:

- safe deploy through `tools/v7-safe-deploy`;
- convergence check through `tools/v7-convergence-status`;
- governed L3 production validation through `v7-governed-canary-dry-run-cycle`;
- autoswitch planning/apply logic through `tools/v7-users-autoswitch`;
- authority promotion readiness and promotion through `tools/v7-users-autoswitch`;
- controlled egress state mutation through `v7-egress-set-state`;
- Certification User creation through `v7-user-create-from-ipam`;
- route and service verification through existing verification owners;
- closure and feedback materialization through existing feedback/learning owners.

Still manual:

- deciding when to re-run Authority promotion readiness after a stability window;
- preparing the controlled certification pool for the next stage;
- sequencing source restore, user creation, certification scope, degradation,
  governed run, readback, and readiness review;
- writing the final phase evidence report;
- updating consumer views when not yet automated.

Repeated workflows that should become governed pipelines:

- Phase certification preparation pipeline;
- Authority promotion readiness pipeline;
- controlled certification pool expansion pipeline;
- evidence collection and report skeleton pipeline;
- post-capability consumer synchronization pipeline.

## 12. Current Owner Landscape

Significantly hardened during certification:

- `tools/v7-users-autoswitch`: Planner, policy gates, Authority promotion,
  retry-aware selection, incident continuation, Runtime Apply integration.
- `v7-governed-canary-dry-run-cycle`: governed execution owner for controlled
  L3 validation and batch certification.
- Approved Plan Lock / packet / lease path: hardened around committed selected
  move identity continuity.
- Restore Barrier: hardened around source bundle, generation, selected move
  hash, and committed identity validation.
- Verification owners: hardened around service verification classification,
  timeout/lock behavior, scoped route verification, and selected-user
  attribution.
- Controlled source and certification user owners: hardened through controlled
  source degradation, marker materialization, IPAM user creation, and registry
  readback.
- Authority owner: hardened to interpret legacy `POOL=25` as canonical
  `LARGE_BATCH=25` for forward promotion only, without increasing runtime
  budget or creating a new owner.

Owners that may deserve review after FULL_INCIDENT certification:

- `tools/v7-users-autoswitch` may have excessive responsibility because it now
  carries planner, policy, authority promotion, and runtime-adjacent behavior.
  Do not split it before certification; review only after capability is earned.
- governed certification orchestration is still a manual workflow over several
  existing owners; it may become a pipeline through existing ownership.

Do not redesign the owner landscape during active certification unless an
implementation proves a canonical contradiction.

## 13. Current Project State

Current Phase:

```text
Phase 6: XLARGE_BATCH Certification
```

Current Capability:

```text
LARGE_BATCH=25 certified; XLARGE_BATCH=50 pending.
```

Current Authority:

```text
Production raw authority state is legacy POOL=25.
For forward promotion, existing Authority owner maps POOL=25 to canonical
LARGE_BATCH=25. Promotion target is XLARGE_BATCH=50.
```

Current Certification Status:

```text
CANARY, SMALL_BATCH, MEDIUM_BATCH, LARGE_BATCH certified.
XLARGE_BATCH in HOLD.
FULL_INCIDENT not reached.
```

Current Engineering Mission:

```text
Resume Phase 6 when Authority no-regression window matures.
No code patch is currently required for the known blocker.
```

Current Highest Priority:

```text
Re-check Authority promotion readiness, promote to XLARGE_BATCH if evidence is
valid and explicit confirmation is authorized, then execute 50-user governed
certification.
```

Current Hold Reason:

```text
3600 second no-regression window not yet elapsed for both LARGE_BATCH evidence
operations at the latest check.
```

Current Next Action:

```text
Run the existing Authority readiness check:

/usr/local/bin/v7-users-autoswitch --promote-authority-to XLARGE_BATCH \
  --authority-promotion-operation-id runtime_autoswitch_d2fc48ffe5590c23e2ac8950 \
  --authority-promotion-operation-id runtime_autoswitch_ffddc0afb57b4b2a6cd4e560 \
  --pretty

If evidence_valid becomes true, run the same existing owner with explicit
Authority promotion confirmation, then continue Phase 6.
```

Current Pipeline Candidates:

- Phase certification preparation pipeline.
- Authority promotion readiness pipeline.
- Certification Pool expansion pipeline.
- Evidence readback/report pipeline.
- Consumer synchronization pipeline.

Automation Debt:

- Manual Authority readiness polling.
- Manual certification pool preparation.
- Manual evidence collection.
- Manual report generation.

Workflow Debt:

- Multi-command controlled certification run orchestration.
- Multi-command owner-resolution/test/deploy/resume loop.

Synchronization Debt:

- Consumer views may lag capability evidence unless an existing safety owner
  requires synchronization before progression. Record and classify any lag.

Owner Resolution State:

- Latest implementation defect in Authority promotion continuity was resolved
  and deployed.
- Current state is policy/evidence HOLD, not implementation defect.

Production Readiness:

- Safe deploy and convergence are operational.
- Production/local/GitHub convergence was PASS at commit
  `66a276e9d805b12871f37e6fcc92d9376a4a45b3` before the Phase 6 HOLD report.
- Production certification has proven up to 25 users in one governed batch.

Engineering Automation Readiness:

- The target shape is clear.
- The repeated workflows are known.
- They are not yet implemented as single governed pipelines.

## 14. Future Roadmap

This is not a new roadmap. It is the already-approved continuation.

### Current Certification Program

1. Resume Phase 6 after Authority stability window matures.
2. Promote to `XLARGE_BATCH` through existing Authority owner if evidence is valid.
3. Run `XLARGE_BATCH=50` governed certification.
4. If PASS, proceed to Phase 7 `FULL_INCIDENT`.
5. Certify FULL_INCIDENT or prove canonical impossibility.
6. Enter routine production operation only after FULL_INCIDENT and Authority recognition.

### Engineering Automation

Implement owner-mapped pipelines for repeated certification engineering
workflows after they are justified and certified. Do not let engineering
automation bypass production safety.

### Future Runtime Autonomy

Runtime autonomy remains future until certification and Authority permit it.
Do not enable broad automation merely because batch certification improves.

### Future Production Autonomy

Production autonomy should grow from certified action classes and Authority
recognition. It must remain bounded by Reality First, Verification, Rollback,
Production Restoration, and OMP.

### Future Engineering Evolution

Use every implementation mission to improve both V7 and the engineering system.
Pipeline candidates should be converted into governed tools only when existing
owners and certification support them.

## 15. Immutable Rules

Never do the following:

- Never create a duplicate Runtime.
- Never create a duplicate Planner.
- Never create a duplicate Authority.
- Never create a duplicate Restore Barrier owner.
- Never create a duplicate Wake owner.
- Never create a duplicate Packet owner.
- Never create a duplicate OMP.
- Never create a parallel execution path.
- Never create a parallel truth source.
- Never bypass Authority.
- Never bypass Approved Plan Lock.
- Never bypass Restore Barrier.
- Never bypass Runtime.
- Never bypass Verification.
- Never bypass Rollback or closure.
- Never synthesize production evidence.
- Never treat dry run success as production certification.
- Never treat timer, cron, or blind polling as authority by itself.
- Never move ordinary customers as certification subjects.
- Never broaden automation without certification and Authority.
- Never increase max users beyond current Authority budget.
- Never restart an execution from Observation when the protocol says resume
  from the current breakpoint.
- Never switch candidate, operation, source, selected move hash, or incident
  silently.
- Never make documentation synchronization block capability producers unless an
  existing safety owner proves it must.
- Never redesign architecture to avoid an implementation defect.
- Never create a new owner before proving existing owners cannot own the need.
- Never terminate an investigation because a blocker was found.
- Never call a patch, deploy, report, or root cause the terminal project state.

## 16. Handoff: How A Future Codex Continues

If you know nothing except this document, continue like this.

### Step 1. Establish Repository State

Run:

```text
git status --short
git log --oneline -8
```

Do not revert unrelated user changes. Stage only files you intentionally change.

### Step 2. Read Current Canonical Owners

Read:

- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`
- `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md`
- `docs/reference/V7_EXECUTION_COMPLETION_PROTOCOL.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`

Use Engineering Reports only as evidence for exact facts.

### Step 3. Discover The Current Phase

Start from the latest certification report:

- `docs/reports/engineering/2026-07-03_164505_phase6_xlarge_hold_no_regression_window.md`

Current phase is Phase 6. Do not start Phase 7 until Phase 6 reaches PASS.

### Step 4. Resume The Interrupted Certification

Re-check Authority promotion readiness on production using the existing owner.
Do not patch unless the owner produces a new implementation defect.

If readiness is still blocked only by the no-regression window, remain in HOLD.
If readiness is valid and explicit confirmation is authorized, promote through
the existing Authority owner and continue Phase 6 with a 50-user governed
certification run.

### Step 5. Continue Engineering Work

For every STOP:

```text
STOP
  -> breakpoint
  -> Owner Resolution
  -> terminal classification
  -> implementation or policy route
  -> tests
  -> deploy if needed
  -> convergence
  -> resume same phase
```

Do not switch execution identity for convenience.

### Step 6. Update Knowledge Correctly

- Put historical proof in Engineering Reports.
- Put durable rules in the relevant canonical owner.
- Put volatile current state in Current Program State when required.
- Let OMP and Production Maturity consume certified evidence.
- Record Automation Debt, Workflow Debt, and Synchronization Debt when created.

### Step 7. Avoid Architectural Regression

Before adding any section, command, owner, artifact, pipeline, or automation:

```text
DISCOVER
  -> REUSE
  -> EXTEND
  -> CREATE ONLY IF NECESSARY
```

The safest future Codex is not the one that writes the most code. It is the one
that preserves identity, proves reality, reuses owners, finishes the current
phase, and leaves the next Codex with less uncertainty than it inherited.
