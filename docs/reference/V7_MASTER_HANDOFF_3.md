# V7 Master Handoff 3.0

Status: canonical project transfer package
Purpose: allow a new ChatGPT/Codex conversation to continue V7 Vozduh without rereading the full repository.
Last reconciled: 2026-06-29

This handoff is not a roadmap, not a second OMP, not a second truth source, and not an implementation plan.

If this document conflicts with canonical owners, canonical owners win in this order:

1. Product Specification and Canonical Reference for durable product truth.
2. OMP for execution discipline and next-step selection.
3. Current Program State for volatile current state.
4. SYSTEM_MAP for owner lookup.
5. Runtime Model and Decision Model for runtime/decision semantics.
6. Production Maturity Model for maturity scoring.
7. Engineering Reports for evidence and history only.

## Document 1: Project Identity

V7 Vozduh is a production connectivity and autonomous routing control-plane project. Its purpose is to keep users online by observing real production state, selecting safe routing actions through existing owners, acting only under certified authority, verifying outcomes, and learning from real evidence.

The product is not "automation for automation's sake." The durable direction is governed autonomy: the operator supervises policy and authority boundaries, while the system matures from read-only evidence and governed execution toward certified routine autonomy.

Core philosophy:

- Reality First: production facts, tests, convergence, and observed outcomes beat opinion.
- Thin Runtime: Runtime consumes prepared knowledge, validates live gates, executes or stops, verifies, rolls back when allowed, records outcomes, and notifies OMP. Runtime must not become a planner, analytics engine, research engine, report generator, certification owner, or truth source.
- Discover -> Reuse -> Extend -> Implement: every task first proves whether a concept already exists, reuses the existing owner, extends only if partial/missing, then implements only approved scope.
- Architecture closed by default: architecture is complete and must not be reopened unless implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`, industry consensus changes, production evidence contradicts the model, or the operator explicitly requests reopening.
- Evidence before maturity: Production Maturity moves only through real implementation, deploy, tests, verification, certification, production outcomes, authority decisions, and certified autonomy.
- No synthetic evidence: forecasts, advisory scores, and design proposals cannot become certified outcomes.

Forbidden by default:

- new Runtime;
- new Planner;
- new Owner;
- new Truth Source;
- new Roadmap;
- new Master Program;
- parallel OMP;
- Runtime apply without explicit authority;
- automation enablement without certification and authority;
- authority expansion without explicit approval;
- user movement without approved governed execution;
- threshold/formula mutation hidden inside documentation or dashboard work;
- important knowledge remaining only in chat or reports when it is durable.

## Document 2: Current Canonical Architecture

### Runtime

Canonical owner: `docs/reference/V7_RUNTIME_MODEL.md`.

Runtime is a thin execution path:

```text
Event
-> Runtime Wakeup
-> Read Current Program State
-> Read Decision Snapshot
-> Policy
-> Safety
-> Action-Class / Policy Authority
-> Fresh Packet
-> Execute OR Stop
-> Verify
-> Rollback if needed
-> Outcome
-> Learning
-> Update Current Program State
-> Notify OMP
-> Sleep
```

Runtime does not invent decisions and does not promote action classes. It executes certified action classes only when OMP and authority policy have promoted the class. Runtime self-approval is allowed only inside a future approved Delegated Autonomy Policy; that policy is not currently approved.

### Decision Model

Canonical owner: `docs/reference/V7_DECISION_MODEL.md`.

Decision flow:

```text
Event / Question
-> Current State
-> Desired State / Policy
-> Evidence Quality
-> Service / User / Channel Fit
-> Risk / Blast Radius
-> Decision Vocabulary
-> Authority Gate
-> Packet / Preview / Stop
-> Verification
-> Outcome
-> Learning
```

Decision Model owns decision semantics. Runtime Model owns runtime lifecycle, freshness, work placement, and execution placement. Scores and diagnostics may explain decisions, but must not become a second decision model.

### Work Placement

Canonical owner: Runtime Model.

Every computation belongs to one primary plane:

```text
Observation
-> World Model
-> Planning
-> Execution
-> Verification
-> Feedback / Learning
-> OMP / Certification
```

Slow knowledge work should move earlier when safe. Live Runtime work must stay limited to freshness, authority, eligibility, restore/rollback, verification, anti-flap, movement protection, blast-radius checks, apply, verification, rollback, and `STOP_SAFE`.

### RT Phase 1

Status: `FULLY_COMPLETE`.

RT Phase 1 canonicalized Runtime Time Architecture, Reaction Latency Model, Thin Runtime Path Contract, Latency Ownership and Live/Precompute Matrix, Engineering Report latency requirement, Phase 2 Automation-Time Contract, Runtime Latency Engineering Review Checklist, and Phase 2 Automation Contract.

RT Phase 1 did not create a new backlog item, runtime path, queue, owner, or automation mode.

### RT2

Canonical owner: OMP plus Runtime Model.

RT2 is the Runtime Capability Maturation Program inside OMP. It is complete as read-only/advisory owner-mapped surfaces:

| Workstream | Status | Owner pattern |
| --- | --- | --- |
| `RT2-S1` Measurement & Observability | `DONE_READ_ONLY` | Runtime Model, OMP, measurement/read-model owners |
| `RT2-S2` World & Readiness | `DONE_READ_ONLY` | World/readiness owners and decision surface |
| `RT2-S3` Desired-State Delta | `DONE_READ_ONLY` | Decision Model, planner/autoswitch, OMP |
| `RT2-S4` Governed Execution Coordination | `DONE_READ_ONLY` | execution packet/lease/verification/rollback owners |
| `RT2-S5` Certified Concurrency Ladder | `DONE_READ_ONLY` | OMP, action-class, blast-radius, rollback, verification owners |
| `RT2-S6` Evidence-Based Continuous Improvement | `DONE_READ_ONLY` | OMP, Production Maturity, Research Framework, canonical owners |

RT2 recommendations are advisory. Runtime self-optimization remains forbidden.

### Engineering Intelligence

Canonicalized through Runtime Model, OMP, Production Maturity Model, SYSTEM_MAP, Canonical Reference, and Current Program State.

Engineering Intelligence is materialized at architecture/canonical level. Real evidence phase is not complete.

Lifecycle:

```text
Observation
-> Process Understanding
-> Runtime Time Understanding
-> Recommendation
-> Implementation through OMP if approved
-> Outcome
-> Prediction vs Reality
-> Confidence Update
-> Recommendation Evolution
```

### Capability Lifecycle

Certified lifecycle:

```text
Idea
-> Existing Owner Check
-> Architecture Fit
-> OMP Admission
-> Capability Classification
-> Owner Mapping
-> Canonical Integration
-> Implementation Backlog or existing owner if approved
-> Implementation
-> Verification
-> Engineering Report
-> Canonical Update
-> Current Program State
-> Continue OMP
```

No future capability should create a second lifecycle.

### Capability Transition Contract

Canonical owner: OMP.

OMP explains why a next step becomes available, what evidence unlocked it, who may consume it, what remains blocked, why the next step is safe, and why later steps remain forbidden.

Current transition: `C7 -> IMPLEMENTATION_COMPLETE`.

### Capability Production Contract

Canonical owner: OMP.

OMP owns the Capability Production Graph and producer/consumer matrix: stage -> produced capability -> evidence -> owner -> consumers -> unlocked stage -> blocked stage.

Current produced capability: C7 produced Pool Health Capacity And Blast Bounds as read-only owner-mapped evidence.

### Dashboard Model

Canonical owners:

- OMP owns the permanent read-only dashboard model and design rules.
- Current Program State owns the volatile current dashboard snapshot.
- SYSTEM_MAP owns dashboard ownership lookup.
- Canonical Reference preserves durable dashboard rules.

Dashboard is read-only. It has synchronized Executive, Operator, and Engineering views that consume the same canonical data. It must not approve, execute, rank implementation, mutate Runtime, expand authority, create a queue, replace Planner, or become a truth source.

Dashboard UI foundation says OMP lives as a separate top-level admin section, preferably `/admin/omp`, and must not replace the admin home/overview.

### SYSTEM_MAP

SYSTEM_MAP is owner/topology lookup only. It does not become a roadmap, backlog, runtime, planner, or truth source.

### Canonical Owners

Use the following owners first:

| Question | Owner |
| --- | --- |
| What is true durably? | `docs/reference/V7_CANONICAL_REFERENCE.md` plus affected reference owner |
| What happens next? | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| What is the volatile current state? | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Who owns a capability/file/concept? | `docs/reference/SYSTEM_MAP.md` |
| What is the implementation queue? | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` |
| How mature is production? | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` |
| How does Runtime work? | `docs/reference/V7_RUNTIME_MODEL.md` |
| How are decisions made? | `docs/reference/V7_DECISION_MODEL.md` |
| How does research enter V7? | `docs/programs/V7_RESEARCH_FRAMEWORK.md`, `docs/reference/V7_RESEARCH_PROCESS.md` |
| What happened historically? | `docs/reports/engineering/` as evidence only |

### Truth Ownership

Truth/convergence owners are `tools/v7-truth-check`, `tools/v7-convergence-status`, runtime fingerprint, GitHub branch `Updatesystem`, and safe deploy tooling. Documentation-only mismatch may be allowed when local/GitHub contain docs updates that do not require production deployment.

## Document 3: Current Project State

Current phase: `PRODUCT_EXECUTION`.

Architecture phase: `CLOSED_BY_DEFAULT_GRADUATED`.

Completed work:

- MASTER 1 complete: RT2 canonicalization and OMP self-drive mechanics closed.
- MASTER 2 complete: OMP completeness certified.
- MASTER 3 complete: OMP resilience certified.
- MASTER 4 complete: architecture graduation confirmed.
- Capability Lifecycle certified.
- Engineering Intelligence readiness and materialization phases 1, 2, and 3 complete at architecture/canonical level.
- RT2-S1 through RT2-S6 complete as read-only/advisory surfaces.
- Implementation backlog actionable items complete: Tier A `6 / 6`, Tier B `21 / 21`, Tier C `7 / 7`, overall actionable `34 / 34`.
- Tier D optional items remain future-scope only: `0 / 6`.

Current OMP position:

```text
Current stop: ACTIONABLE_BACKLOG_COMPLETE
Current highest leverage implementation: IMPLEMENTATION_COMPLETE
Current highest leverage action: stop actionable implementation backlog execution; report status or wait for explicit operator authority / explicit new OMP-admitted scope.
```

Current RT2 workstream:

```text
None active. RT2-S1 through RT2-S6 are complete read-only/advisory surfaces.
```

Production Maturity:

```text
Engineering Maturity: 100.0 / 100
Production Maturity: 66.9 / 100
Remaining Production Maturity: 33.1
Current Production milestone: 65% Certification Half Complete
Next Production milestone: 80% Runtime Production Ready
Current autonomy tier: TIER_1_GOVERNED
```

Engineering Intelligence maturity:

```text
MEASURED_UNDERSTOOD_RECOMMENDED_VALIDATION_MATERIALIZED_ADAPTIVE_ENGINEERING_READY
```

Real evidence phase remains incomplete; validation/adaptation need future measured implementation outcomes.

Dashboard status:

- Dashboard model: canonical.
- Dual-view model: canonical.
- Design system: canonical.
- UI foundation: OMP top-level admin section `/admin/omp`; read-only; must not replace existing admin home.
- If production UI does not show OMP, verify deployment/convergence and admin routing before redesigning anything.

Current stop gates:

- Runtime apply: blocked.
- Automation: blocked.
- Authority expansion: blocked.
- User movement: blocked.
- Blast-radius expansion: blocked.
- Threshold/formula mutation: blocked.
- Synthetic evidence: blocked.
- New owner/planner/runtime/truth source/roadmap: blocked.
- Direct implementation outside OMP: blocked.

Current blocked capabilities:

- Production Autonomy.
- Bounded production automation.
- Runtime apply for movement.
- Automatic rollback authority.
- Authority expansion.
- Concurrency beyond serial/read-only.
- Direct class promotion.
- User movement without governed authority.

Current unlocked capabilities:

- Status reporting.
- Explicit operator-approved new scope.
- Review/rewrite of non-canonical design proposals.
- Read-only evidence audits through existing owners.
- Future OMP-admitted implementation only if a new explicit scope is approved.

## Document 4: Engineering Intelligence

Engineering Intelligence is already expressed through existing architecture and has been materialized in existing owners.

Observation Intelligence:
Owned by Observation Plane owners and `RT2-S1`. It exposes read-only evidence, missing-field owner mapping, freshness, measurement reliability, and observability state.

Process Intelligence:
Owned by Runtime Model, Work Placement, Decision Lifecycle, and `RT2-S1`. It explains what happened, why, who produced/consumed evidence, who waited, who blocked, and which stage could move earlier.

Runtime Time Intelligence:
Owned by Runtime Model, `RT2-S1`, and `RT2-S6`. It understands time domains, topology, critical path, time budget, dependency weight, impact prediction, engineering recommendation, certification, and continuous runtime optimization recommendation loop.

Recommendation Intelligence:
Owned by `RT2-S6`, OMP, Backlog, Production Maturity, Engineering Reports, and canonical owners. Recommendations are advisory until OMP routes approved work to an existing owner.

Execution Intelligence:
Owned by Runtime Model and existing packet/lease/execution/verification/rollback owners. It does not create execution authority.

Prediction Intelligence:
Owned by existing Prediction Evidence / Confidence owners.

Confidence Intelligence:
Owned by Autonomy Root Confidence / Trust owners.

Adaptive Engineering Intelligence:
Owned by OMP, `RT2-S6`, Production Maturity, validation/outcome/confidence owners, and Engineering Report -> Canonical Update -> CPS -> Continue OMP loop.

Engineering Intelligence System:

```text
Recommendation
-> Implementation through OMP if approved
-> Outcome
-> Prediction vs Reality
-> Confidence Update
-> Recommendation Improvement
-> Future Recommendation
-> Engineering Learning
-> Future Engineering
```

State:

```text
Architecture/materialization complete.
Real evidence phase not yet complete.
Runtime self-improvement forbidden.
Only Engineering Intelligence evolves through OMP and existing owners.
```

## Document 5: OMP Evolution

Implementation Mode:
OMP has completed actionable implementation backlog execution. The backlog is the only live implementation queue, and it is now complete for actionable items.

Operational Mode:
OMP now acts as the permanent production operating program. It may report state, admit explicit new scope, run audits/certifications through existing owners, and govern future evidence work. It must not invent backlog items or roadmap phases.

Capability Transition Contract:
Explains why the next stage is available and why later stages remain forbidden.

Capability Production Contract:
Explains what each stage produces, who owns it, who consumes it, what it unlocks, and what remains blocked.

Producer / Consumer Matrix:
Lives in OMP. It links producers like A5, A6, B13, B16, RT2-S1 through RT2-S6, B1-B21, and C1-C7 to evidence, owners, consumers, unlocked stages, blocked stages, and production reasons.

Dashboard:
OMP Dashboard is read-only visualization of canonical state. It is a view, not authority.

Current operational maturity status:

```text
Actionable implementation complete.
Production maturity still 66.9 / 100.
Next milestone: 80% Runtime Production Ready.
The next growth path is evidence/certification/authority/outcome work, not another architecture phase.
```

## Document 6: Operational Maturity Campaigns

Source: `docs/design/OPERATIONAL_MATURITY_CAMPAIGNS.md`.

Status:

```text
STATUS: DESIGN PROPOSAL
CANONICAL: NO
OWNER: OMP after validation, not yet
IMPLEMENTATION: NOT STARTED
```

Goal:
Operational Maturity Campaigns are a proposed future mechanism for turning certified Production Maturity gaps into focused evidence campaigns.

Capability Goal:
V7 should not wait passively at `66.9 / 100`. It should eventually identify the gap to the next certified target, define required evidence, ask for operator review, collect evidence safely, certify it, update Production Maturity, then repeat gap analysis.

Capability Gap:
Production Maturity is below `100%` because real outcomes, broader certification, authority evolution, bounded autonomy, and production autonomy are not complete.

Evidence Gap:
The missing work is not another architecture document. It is certified evidence: runtime readiness, rollback/recovery evidence, STOP_SAFE proof, prediction validation, authority confidence, anti-flap evidence, Time-To-Safe-Recovery, and bounded autonomy readiness.

Operational Campaign:
Proposed model:

```text
Current Production Maturity
-> Next Certified Target
-> Certified Gap Analysis
-> Evidence Required
-> Operational Campaign
-> Operator Review
-> Evidence Collection
-> Certification
-> Production Maturity Update
-> Next Gap Analysis
```

Certification:
Campaigns may estimate Evidence Yield, but Production Maturity changes only after existing owners certify evidence.

Capability Growth:
Campaigns could produce real outcomes for Prediction vs Reality, Recommendation Confidence, Engineering Learning, and Adaptive Engineering.

Product Evolution:
Campaigns are a possible future Operational Mode of existing OMP, not a new OMP or roadmap.

Unresolved questions:

- Who generates campaign suggestions?
- How are sample thresholds defined?
- How is expected maturity gain calculated?
- Which campaign can start first after `66.9%`?
- Which evidence is safe to collect without authority expansion?
- How does operator approval work?
- When does campaign output become canonical?
- How does a campaign avoid becoming a shadow backlog?

Explicit rule:

```text
Do NOT integrate Operational Maturity Campaigns until the design matures.
```

## Document 7: Dashboard

Executive View:
Top layer inside the OMP admin section. Shows production state, current OMP stop, current maturity, current produced capability, unlocked/blocked capabilities, and next recommendation. It is not the global admin home.

Operator View:
Minimal one-minute status view. Shows overall OMP progress, progress bars, current/previous/next step, Production Maturity, RT2 stage, Engineering Intelligence stage, stop gates, produced/unlocked/blocked capabilities, risks, recommendation, and simple capability graph.

Engineering View:
Traceable technical view. Shows Capability Graph, Capability Production Graph, producer/consumer matrix, transition contracts, capability contracts, owner mapping, RT2, Engineering Intelligence, dependency graph, current produced evidence, consumers, blockers, and canonical owners.

Dashboard philosophy:
Answer immediately:

```text
Where are we?
Why are we here?
What is blocked?
What was produced?
What comes next?
Why?
What changed today?
What is the current maturity?
```

Dashboard read-model:
Consumes OMP, SYSTEM_MAP, Current Program State, Production Maturity Model, and Canonical Reference. No duplicated state. No duplicated read model. No duplicated truth.

Dashboard ownership:
OMP owns model/design; CPS owns current snapshot; SYSTEM_MAP owns owner lookup; Canonical Reference owns durable rules.

Dashboard implementation status:
Model, dual-view model, UI foundation, and design system are complete at canonical/design level. OMP Dashboard is intended as a top-level admin tab `/admin/omp`, not the default home page. If the live admin lacks it, treat that as deployment/routing verification work, not architecture redesign.

## Document 8: Workflow

Mandatory workflow:

```text
Finish what was started.
Never begin a new major branch before completing the current one.
Never create anything before proving it does not already exist.
```

Every implementation or meaningful engineering action:

```text
Verification
-> Engineering Report
-> Canonical Update
-> Current Program State
-> Continue OMP
```

Full OMP control loop:

```text
Engineering Context Resolver
-> Knowledge Consumption
-> Re-open Evaluation
-> OMP Execution
-> Implementation / Audit / Certification / Verification
-> Engineering Report
-> Knowledge Promotion
-> Current Program State Update
-> OMP Update
-> Continue OMP
```

No important durable knowledge may remain only in:

- reports;
- audits;
- research notes;
- implementation notes;
- handoffs;
- chat.

If deleting an engineering report would remove important durable truth, promote that truth into the proper canonical owner before closing the task.

## Document 9: Open Strategic Questions

Architecture:

- No current architecture gap is known.
- Reopen architecture only with new evidence, explicit operator request, or `FUNDAMENTAL_ARCHITECTURE_GAP`.

Operations:

- What safe evidence can be collected next without Runtime apply, authority expansion, or user movement?
- How should V7 move from `66.9%` to `80% Runtime Production Ready` using certified evidence?
- Which governed production operations, if any, should the operator approve next?

Engineering Intelligence:

- How will recommendation validation accumulate real outcomes?
- How will recommendation quality/confidence trends become visible without becoming authority?
- What minimum evidence is needed before Adaptive Engineering can be called operational rather than canonical-ready?

Dashboard:

- Is `/admin/omp` deployed and visible in production?
- Does dashboard wording distinguish read-only evidence from authority?
- Which future Capability Quality / Confidence / Readiness placeholders should be implemented first?

Operational Campaigns:

- Who generates campaign suggestions?
- What sample thresholds are safe?
- Which campaign can start first after `66.9%`?
- How is expected maturity gain calculated without gaming maturity?
- When does campaign output become canonical?

Future Product Evolution:

- Which next explicit product scope should be admitted through OMP?
- What real-world evidence is needed for authority evolution?
- What does the operator want V7 to optimize next: production readiness, operator UX, dashboard visibility, governed evidence collection, or runtime readiness certification?

## Document 10: Immediate Next Work

What the next chat should do first:

1. Read this handoff.
2. Run `git status --short --branch`.
3. Run or inspect `tools/v7-convergence-status --json` when network/runtime access is appropriate.
4. If the user says `Continue OMP` with no new scope, report the current stop: `ACTIONABLE_BACKLOG_COMPLETE`.
5. If the user provides new scope, resolve it through ECR -> canonical owners -> OMP -> existing owner check before changing anything.

What must not be redesigned:

- Runtime;
- Planner;
- OMP;
- Current Program State ownership;
- SYSTEM_MAP ownership;
- Production Maturity Model;
- Decision Model;
- Engineering Intelligence architecture;
- Dashboard data ownership;
- Operational Maturity Campaigns as canonical architecture.

Current design proposals requiring further iterations:

- `docs/design/OPERATIONAL_MATURITY_CAMPAIGNS.md` is Design Proposal V1 only.
- It must be reviewed/reworked before canonical integration.
- It must not be treated as active OMP or campaign execution.

Current implementation phase:

```text
Product Execution Mode active.
Actionable implementation backlog complete.
No active Runtime implementation.
No active A5/A6/B13/B16/RT2 backlog item remains.
No active operational campaign exists.
```

Safe next categories:

- status reporting;
- design proposal iteration;
- read-only audit;
- explicit operator-approved new OMP scope;
- production evidence collection only when authority and safety boundaries are explicit.

## Self Review

Cross-check result:

- No contradiction with OMP found.
- No contradiction with Current Program State found.
- No contradiction with Production Maturity Model found.
- No duplicate roadmap created.
- No duplicate architecture created.
- No duplicate owner created.
- No missing major capability identified.
- Current status included: `ACTIONABLE_BACKLOG_COMPLETE`, `34 / 34`, `66.9 / 100`, next milestone `80% Runtime Production Ready`.
- Operational Maturity Campaigns correctly marked non-canonical design proposal.
- Dashboard correctly marked read-only and separate from admin home.
- Engineering Intelligence correctly marked canonical/materialized but not real-evidence complete.

## Transfer Prompt For New Chat

Use this compact instruction when opening a new ChatGPT/Codex conversation:

```text
You are continuing V7 Vozduh. Read docs/reference/V7_MASTER_HANDOFF_3.md first.

Current state:
- Product Execution Mode active.
- Architecture closed by default.
- OMP is the single execution program.
- Actionable implementation backlog complete: 34 / 34.
- Current stop: ACTIONABLE_BACKLOG_COMPLETE.
- Production Maturity: 66.9 / 100.
- Next milestone: 80% Runtime Production Ready.
- Runtime apply, automation, authority expansion, and user movement are blocked without explicit authority.
- Engineering Intelligence is canonical/materialized, but real evidence phase remains future.
- Operational Maturity Campaigns are a non-canonical design proposal only.

Workflow:
Discover -> Verify Existing -> Reuse -> Extend -> Implement only if approved.
Every meaningful action requires verification, engineering report, canonical update when durable, CPS update when volatile state changes, then Continue OMP.

Do not create new Runtime, Planner, Owner, Truth Source, Roadmap, Master Program, or parallel OMP.
```

## Final Verdict

MASTER_HANDOFF_3_COMPLETE
