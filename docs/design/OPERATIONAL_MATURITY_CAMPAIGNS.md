# Product Evolution Framework

STATUS: DESIGN PROPOSAL
CANONICAL: NO
OWNER: OMP after validation, not yet
IMPLEMENTATION: NOT STARTED

## Purpose

This proposal defines a future Product Evolution Framework for V7.

The primary subject is Product Evolution.

Operational Maturity Campaigns are one possible mechanism inside the framework. They are not the center of the model, not a roadmap, not an OMP replacement, and not an implementation queue.

The framework asks:

```text
How does V7 observe product reality, identify capability growth needs, collect certified evidence, and evolve the product for many years without creating new architecture?
```

Current context:

- actionable implementation backlog is complete;
- Production Maturity is `66.9 / 100`;
- next milestone is `80% Runtime Production Ready`;
- architecture is closed by default;
- Product Execution Mode is active.

This proposal remains design-only. It does not change OMP, Runtime, Production Maturity, Dashboard, SYSTEM_MAP, canonical owners, implementation, automation, authority, or user movement.

## Design Status

This document is editable design only.

It is not canonical.

It does not create an active Evolution Engine, campaign generator, campaign system, dashboard model, automation mode, Runtime path, OMP mode, owner, truth source, roadmap, backlog, or authority model.

It does not execute Runtime, move users, expand authority, approve automation, change production behavior, change thresholds, change formulas, or write Production Maturity.

## Continuous Product Evolution Cycle

V2 used a linear model. V3 replaces it with a continuous cycle:

```text
Current Product Reality
-> Product Observation
-> Product Goal
-> Capability Strategy
-> Capability Goal
-> Capability Gap
-> Evidence Gap
-> Evolution Engine
-> Campaign Generator
-> Suggested Campaigns
-> Operator Review
-> Evidence Collection
-> Certification
-> Capability Growth
-> New Product Reality
-> Product Observation
```

The cycle is continuous because product reality changes after every certified outcome, blocked campaign, operator decision, production observation, or capability advancement.

Campaigns are not the success condition.

Success is:

```text
Certified Capability Advancement
-> New Product Reality
-> Better Product Evolution
```

## Target-Driven Product Evolution

V3 explains how V7 evolves.

This extension explains how V7 decides which Product Goal is currently active.

Target-Driven Product Evolution adds a management layer above Capability Strategy:

```text
Vision
-> Product Intent
-> Target Catalog
-> Current Active Target
-> Target Gap Analysis
-> Capability Strategy
-> Capability Gap
-> Evidence Gap
-> Evolution Engine
-> Operational Campaign
-> Evidence
-> Certification
-> Capability Advancement
-> Target Completion
-> Target Selection
-> Next Product Evolution Cycle
```

Target Management remains design-only.

It does not create a roadmap, backlog, implementation queue, campaign list, authority model, automation mode, or second OMP.

It answers:

1. Which product target is active now?
2. Why is it active?
3. Which capability goals belong to it?
4. Which capability gaps block it?
5. Which evidence gaps must be closed?
6. Which campaigns, if any, belong to that target?
7. What proves target completion?
8. How is the next target selected after completion?

## Target Catalog

Target Catalog is the ordered set of certified Product Goals that define long-term product evolution.

Target Catalog is not:

- backlog;
- roadmap;
- implementation queue;
- campaign list;
- authority approval list;
- dashboard task list;
- replacement for OMP.

Target Catalog is:

- a design concept for organizing Product Goals;
- a way to explain which target V7 is trying to advance;
- a way to prevent campaigns from being invented without a target;
- a way to keep Product Evolution goal-driven instead of campaign-driven.

Example target catalog:

| Target | Meaning | Status in this proposal |
| --- | --- | --- |
| `80% Runtime Production Ready` | Runtime readiness, safety gates, certification, and evidence become production-ready enough for the next milestone. | Example based on current Production Maturity milestone. |
| `90% Authority Ready` | Authority evidence is mature enough for bounded authority review. | Future example only. |
| `95% Production Autonomy` | Bounded routine autonomy has strong certified evidence and operator governance. | Future example only. |
| `100% Production Certified` | Production autonomy is certified. | Future example only. |

Future goals remain examples only until admitted and validated through existing owners.

## Current Active Target

Only one Product Target should normally be active.

The Current Active Target is the product-level focus that organizes capability strategy, gaps, evidence, and campaigns.

The framework must always explain:

- why this target is active;
- which product observation or product intent supports it;
- which capability goals belong to it;
- which capability gaps belong to it;
- which evidence gaps belong to it;
- which campaigns belong to it;
- which stop gates prevent target completion;
- which certification owner can declare target completion.

Current design example:

```text
Current Active Target:
80% Runtime Production Ready

Why active:
Production Maturity is 66.9 / 100 and the next Production Maturity milestone is 80%.

Capability goals:
Runtime Readiness, Rollback Reliability, Recovery, STOP_SAFE Evidence, Runtime Time Intelligence, Prediction Confidence, Authority Evidence.

Target not achieved because:
certified capability advancement is still missing across production readiness, authority, autonomy, and real evidence dimensions.
```

This example does not activate work. It is a design illustration only.

## Target Gap Analysis

Target Gap Analysis happens before Capability Gap Analysis.

The sequence becomes:

```text
Current Active Target
-> Target Gap Analysis
-> Capability Gap Analysis
-> Evidence Gap Analysis
```

Target Gap Analysis answers:

```text
Why is the target not yet achieved?
```

It must identify:

- current target;
- current certified target progress;
- missing capability goals;
- incomplete capability advancement;
- missing evidence families;
- stop gates;
- certification blockers;
- target completion owner;
- next analysis step.

Target Gap Analysis must not generate campaigns directly.

It routes to Capability Gap Analysis first.

## Target Completion

Target Completion is not campaign completion.

Target Completion is not capability completion.

Target Completion means:

```text
Enough certified capability advancement exists to declare the Product Target achieved.
```

Target Completion requires:

- Current Active Target;
- target completion criteria;
- certified capability advancements;
- certification owner;
- Production Maturity or affected owner review when relevant;
- safety review;
- authority review when relevant;
- evidence preservation;
- new product reality statement;
- explicit next target selection trigger.

Only after Target Completion can the framework proceed to Next Target Selection.

## Target Selection

After Target Completion, the framework starts the next cycle:

```text
Current Product Reality
-> Product Observation
-> Target Selection
-> Current Active Target
-> New Evolution Cycle
```

Target Selection chooses the next Current Active Target from validated Product Goals.

Target Selection must be advisory until canonicalized.

It must consider:

- Product Vision;
- Product Intent;
- Current Product Reality;
- Production Maturity;
- operator direction;
- certified capability state;
- unresolved safety or authority blockers;
- expected capability growth;
- expected product evolution;
- operational investment;
- risk;
- expected ROI.

Target Selection must not silently skip an unfinished active target.

If priority changes before completion, the framework must explain why the target changed, what evidence changed, who approved it, and what remains blocked.

## Product Observation

Product Observation is the Reality First entry point for future product evolution.

It explains how new goals appear.

Product goals must not be invented from taste, speculation, or campaign enthusiasm. They must come from observed reality, operator need, production behavior, evidence gap, or explicit product direction.

Observation examples:

| Observation source | What it may reveal | Design status |
| --- | --- | --- |
| Production behavior | Unsafe stop frequency, recovery limits, stale evidence, routing friction, degraded channels, capacity limits. | DESIGN |
| Operator workload | Too many manual reviews, unclear blocker reasons, repeated approval friction, dashboard confusion. | DESIGN |
| Recovery quality | Slow recovery, unsafe recovery admission, missing observation windows, weak slow-start evidence. | DESIGN |
| Prediction quality | Prediction vs Reality mismatch, confidence drift, weak recommendation accuracy. | DESIGN |
| Engineering outcomes | Recommendations succeed, fail, drift, remain unvalidated, or produce low ROI. | DESIGN |
| Runtime cost | Too much live work, duplicate computation, expensive reads, slow safe recovery path. | DESIGN |
| Customer experience | Connectivity loss, unstable routing, poor service fit, unnecessary movement, delayed restoration. | DESIGN |
| Dashboard signals | Blocked gates, missing evidence, stale read models, unclear current product state. | DESIGN |

Product Observation must follow Reality First:

- source must be named;
- freshness must be known or marked unknown;
- owner must be known or marked missing;
- observation must not imply authority;
- observation must not update maturity;
- observation must not create a campaign directly;
- observation must pass through Capability Strategy before any proposed campaign.

## Capability Hierarchy

The framework distinguishes four levels.

They must not be collapsed into one vague "gap."

```text
Product Goal
-> Capability Goal
-> Capability Gap
-> Evidence Gap
```

Product Goal:
The product-level outcome V7 wants to reach. Examples: `80% Runtime Production Ready`, lower Time-To-Safe-Recovery, clearer operator control, safer recovery, higher prediction confidence, or future bounded autonomy readiness.

Capability Goal:
The capability state required to serve the product goal. Examples: Runtime Readiness, Prediction Confidence, Rollback Reliability, Recovery Admission, Runtime Time Intelligence, Engineering Intelligence, Movement Protection, Authority Evolution, Dashboard Clarity.

Capability Gap:
The measurable difference between current certified capability state and target capability state.

Evidence Gap:
The missing proof required to close or reduce the capability gap. Evidence gaps name source owner, certification owner, evidence type, quality requirement, sample requirement if known, freshness/expiry, stop gates, and forbidden shortcuts.

Example:

```text
Product Goal:
80% Runtime Production Ready

Capability Goal:
Runtime can safely consume prepared eligibility, rollback, verification, anti-flap, freshness, and blast gates.

Capability Gap:
Read-only readiness surfaces exist, but certified operational runtime-readiness evidence remains insufficient.

Evidence Gap:
Missing certified STOP_SAFE / readiness / rollback / verification / freshness outcomes across required action classes.
```

## Evolution Engine

Evolution Engine is the central design concept in V3.

It replaces Campaign Generator as the center of the proposal.

The Evolution Engine is advisory only.

It does not execute Runtime, approve campaigns, update maturity, certify evidence, expand authority, move users, automate work, create a queue, create a roadmap, or become a truth source.

Possible responsibilities:

| Responsibility | Meaning | Authority |
| --- | --- | --- |
| Product Observation | Convert product reality into candidate product goals. | Advisory only. |
| Capability Strategy | Identify which capability must grow and why. | Advisory only. |
| Capability Gap Analysis | Compare current capability state with target capability state. | Advisory only. |
| Evidence Gap Analysis | Identify missing evidence required for capability advancement. | Advisory only. |
| Campaign Generation | Suggest bounded evidence campaigns from evidence gaps. | Advisory only. |
| Recommendation | Explain possible next product-evolution action. | Advisory only. |
| Evolution Planning | Sequence suggested evidence work by product goal, capability impact, investment, risk, and certification path. | Advisory only. |

The Evolution Engine is not a planner.

It may later recommend work to OMP, but OMP remains the execution program.

It may later feed Dashboard, but Dashboard remains read-only.

It may later feed Engineering Intelligence, but Engineering Intelligence remains advisory and OMP-governed.

## Capability Strategy

Capability Strategy is the design step between observation and gap analysis.

It answers:

1. What product reality was observed?
2. What product goal follows from that reality?
3. Which capability must grow?
4. What is the current certified capability state?
5. What target capability state is needed?
6. Which existing owner owns the capability?
7. Which consumers need the capability?
8. Which evidence is missing?
9. Which stop gates apply?
10. Which safety/authority/verification/rollback/STOP_SAFE rules constrain the work?
11. Which campaign, if any, could safely collect the evidence?
12. What investment and risk would the campaign require?
13. What capability advancement would count as success?
14. How would new product reality be observed after certification?

Capability Strategy must not become a roadmap or backlog.

It is a design-stage analysis that may later be routed through OMP only after validation and canonical readiness.

## Capability Gap Model

Capability Gap is generic.

It can describe any future product evolution need:

| Capability area | Example capability gap | Example evidence gap |
| --- | --- | --- |
| Runtime Readiness | Runtime can consume prepared gates, but apply remains blocked. | Certified runtime-readiness outcomes across freshness, authority, rollback, verification, anti-flap, and blast gates. |
| Prediction Confidence | Predictions exist, but confidence is below operational usefulness. | Prediction vs Reality samples with certified difference and confidence update. |
| Rollback Reliability | Rollback/no-rollback evidence exists, but automatic rollback authority is not approved. | Certified rollback, no-rollback, containment, and forward-fix outcomes. |
| Recovery | Recovery admission is read-only complete, but production recovery maturity is not certified. | Repeated recovery admission, observation-window, slow-start, and no-regression evidence. |
| Engineering Intelligence | Architecture/materialization is complete, but real evidence phase is incomplete. | Recommendation -> implementation -> outcome -> prediction-vs-reality -> confidence update records. |
| Runtime Time Intelligence | Time model is canonical, but operational time evidence is future. | Measured domains, topology, critical path, Time-To-Safe-Recovery, and optimization recommendation outcomes. |
| Dashboard Clarity | Dashboard model exists, but product-evolution visibility is not canonical or implemented. | Read-only visualization needs owner-mapped product reality, goals, gaps, campaigns, ROI, and certification state. |
| Future capabilities | New product capability is proposed. | Existing owner check, capability fit, missing evidence, certification owner, and safe implementation path. |

Every capability gap must name:

- current product reality;
- product observation source;
- product goal;
- capability goal;
- current capability state;
- target capability state;
- existing owner;
- consumers;
- missing evidence;
- certification owner;
- stop gates;
- forbidden shortcuts;
- expected capability growth if certified;
- expected new product reality after advancement.

## Evidence Gap Analysis

Evidence Gap Analysis prevents vague strategy from turning into invented campaigns.

It must answer:

1. What evidence is missing?
2. Which existing owner can produce it?
3. Which existing owner can certify it?
4. Is the evidence observational, operational, verification, rollback, authority, prediction, confidence, runtime-time, dashboard, or engineering evidence?
5. Does evidence require Runtime apply?
6. Does evidence require user movement?
7. Does evidence require authority expansion?
8. Can evidence be collected read-only?
9. Can evidence be collected through governed operator review?
10. What makes the evidence synthetic or invalid?
11. When does evidence expire?
12. What proves capability advancement?

Evidence Gap Analysis must happen before campaign generation.

## Operational Campaigns

Operational Campaigns remain useful, but their importance is reduced.

They are generated mechanisms, not the framework itself.

Campaigns must originate from:

```text
Product Observation
-> Capability Strategy
-> Capability Gap
-> Evidence Gap
-> Evolution Engine
-> Campaign Generator
-> Suggested Campaign
```

Campaigns must never be manually invented.

A suggested campaign is invalid unless it can trace to:

- current product reality;
- product observation;
- product goal;
- capability goal;
- capability gap;
- evidence gap;
- existing evidence owner;
- existing certification owner;
- stop gates;
- allowed actions;
- forbidden actions;
- expected capability growth;
- expected product evolution;
- expected ROI;
- operational investment.

Campaign lifecycle:

```text
Campaign Suggested
-> Operator Reviewed
-> Campaign Approved
-> Evidence Collected
-> Evidence Certified
-> Capability Advanced or Not Advanced
-> New Product Reality Observed
```

Campaign completion is not success.

Campaign success is not the objective.

The objective is:

```text
Capability Advancement
-> Product Evolution
```

## Campaign Types

Campaign types remain examples only.

| Campaign Type | Capability Growth Target | Example Evidence | Primary Risk |
| --- | --- | --- | --- |
| Prediction Validation Campaign | Prediction Confidence / Engineering Intelligence | Prediction vs Reality rows, forecast accuracy, confidence updates. | Treating predicted yield as certified maturity. |
| Rollback Evidence Campaign | Rollback Reliability | Governed rollback/no-rollback outcomes, containment/forward-fix closure. | Executing rollback without authority. |
| Recovery Evidence Campaign | Recovery / Runtime Readiness | Recovery admission, observation windows, successful readiness evidence. | Admitting traffic without certification. |
| Authority Confidence Campaign | Authority Evolution | Certified class evidence, operator decisions, outcome stability. | Silent authority expansion. |
| Runtime Readiness Campaign | Runtime Production Ready | Eligibility, freshness, blast, rollback, anti-flap, verification, learning gates. | Treating readiness as apply permission. |
| Bounded Autonomy Readiness Campaign | Production Autonomy | Governed outcomes, STOP_SAFE proof, readiness, rollback evidence. | Enabling automation before approval. |
| STOP_SAFE Evidence Campaign | Safety / Runtime Eligibility | Stop reason distribution, blocked action traces, no-mutation proof. | Creating synthetic negative evidence. |
| Anti-Flap Evidence Campaign | Movement Protection / Recovery | Cooldown, hysteresis, target block/quarantine, pair reversal evidence. | Changing thresholds or formulas. |
| Time-To-Safe-Recovery Campaign | Runtime Time Intelligence / Recovery | Observation time, readiness time, decision time, verification time, recovery closure. | Optimizing time by weakening safety. |

## Capability Advancement

Capability Advancement is the success condition.

It is the certified improvement of a capability after evidence has been collected, verified, and reviewed by existing owners.

Campaign completion alone is not advancement.

Evidence collection alone is not advancement.

Expected ROI alone is not advancement.

Dashboard progress alone is not advancement.

Capability Advancement requires:

- named capability;
- current certified state;
- target state;
- certified evidence;
- certification owner;
- affected consumers;
- safety review;
- authority review if relevant;
- verification/rollback/STOP_SAFE review if relevant;
- declared result: advanced, partially advanced, not advanced, blocked, or invalid evidence;
- new product reality to observe.

## Evolution Metrics

Evolution Metrics are future design concepts only.

They must not be implemented, scored, displayed as canonical, or used for authority until canonicalized.

Possible metrics:

| Metric | Meaning | Current status |
| --- | --- | --- |
| Product Evolution Rate | Rate at which certified product reality improves. | DESIGN |
| Capability Advancement Rate | Rate at which capabilities advance after certification. | DESIGN |
| Evidence Yield | Value and coverage of collected evidence before certification. | DESIGN |
| Campaign Success Rate | Fraction of campaigns that produce certified capability advancement. | DESIGN |
| Certification Throughput | Rate of evidence packets certified by existing owners. | DESIGN |
| Mean Time To Capability Growth | Time from observation to certified advancement. | DESIGN |
| Operational Investment | Operator/production effort and risk. | DESIGN |
| Engineering Investment | Engineering effort required to support evidence collection or read-only surfaces. | DESIGN |
| Evidence Investment | Cost of collecting, refreshing, validating, and preserving evidence. | DESIGN |
| Expected ROI | Expected product/capability value relative to investment and risk. | DESIGN |

All metrics are advisory until certified.

No metric may override Safety, Authority, Verification, Rollback, or STOP_SAFE.

## Product Evolution Data Model

Suggested design fields:

| Field | Meaning |
| --- | --- |
| `vision` | Long-term product direction the target serves. |
| `product_intent` | Product intent that justifies target admission. |
| `target_catalog_entry` | Product Target from the future Target Catalog. |
| `current_active_target` | The normally single active Product Target. |
| `target_gap` | Why the active target is not yet achieved. |
| `target_completion_criteria` | Certified conditions required to declare the target complete. |
| `target_completion_result` | Complete, partial, blocked, invalid, or not reviewed. |
| `next_target_candidate` | Possible next Product Target after completion. |
| `current_product_reality` | Observed current state of the product. |
| `product_observation` | Source and summary of observed reality. |
| `product_goal` | Product-level outcome the work serves. |
| `capability_strategy` | Proposed approach for capability growth. |
| `capability_goal` | Target capability state. |
| `capability_id` | Existing capability or future OMP-admitted capability. |
| `current_capability_state` | Current certified state. |
| `target_capability_state` | Desired certified state. |
| `capability_gap` | Measurable difference between current and target state. |
| `evidence_gap` | Missing evidence required to advance capability. |
| `evolution_engine_recommendation` | Advisory recommendation from the future Evolution Engine. |
| `campaign_id` | Stable campaign identifier if a campaign is generated. |
| `campaign_type` | Suggested campaign type. |
| `evidence_owner` | Existing owner that produces or stores evidence. |
| `certification_owner` | Existing owner that certifies evidence. |
| `expected_capability_growth` | Advisory capability movement if evidence is certified. |
| `expected_product_evolution` | Advisory product reality change if capability advances. |
| `evidence_yield` | Advisory value of collected evidence before certification. |
| `operational_investment` | Operational effort, risk, and cost. |
| `engineering_investment` | Engineering support cost. |
| `evidence_investment` | Evidence collection and preservation cost. |
| `expected_roi` | Expected value relative to investment and risk. |
| `stop_gates` | Boundaries that stop the work. |
| `allowed_actions` | Actions permitted inside scope. |
| `forbidden_actions` | Actions forbidden even if they could produce evidence faster. |
| `capability_advancement_criteria` | Conditions for capability growth after certification. |
| `certification_result` | Result after certification review. |
| `new_product_reality` | Product reality after certification or blocked outcome. |

## Safety Rules

The Product Evolution Framework may eventually:

- observe product reality;
- suggest product goals;
- analyze capability strategy;
- identify capability gaps;
- identify evidence gaps;
- suggest campaigns;
- estimate evolution metrics;
- recommend operator-reviewed evidence work;
- prepare certification packets;
- learn from certified outcomes.

It may not:

- execute Runtime;
- enable automation;
- expand authority;
- move users;
- approve Runtime apply;
- approve rollback execution;
- create synthetic evidence;
- change thresholds or formulas;
- bypass certification;
- create a new owner;
- create a new roadmap;
- replace OMP;
- write Production Maturity directly;
- declare capability growth without certification;
- treat campaign completion as success;
- become a planner or truth source.

## Dashboard Evolution

Dashboard should eventually visualize Product Evolution, not just campaigns.

Dashboard remains read-only.

Future dashboard areas may include:

- Vision;
- Current Active Target;
- Progress toward Target;
- Target Gap;
- Target Completion;
- Next Target;
- Current Product Reality;
- Current Product Goal;
- Current Capability Goals;
- Current Capability Gaps;
- Current Evidence Gaps;
- Current Campaigns;
- Expected Capability Growth;
- Expected Product Evolution;
- Expected ROI;
- Evolution Metrics;
- stop gates;
- certification status;
- next operator review.

Dashboard must not become:

- Evolution Engine;
- Campaign Generator;
- authority surface;
- execution surface;
- truth source;
- maturity writer;
- second OMP;
- campaign approval system.

Dashboard should show campaigns as a child view of Product Evolution.

## Relationship To Engineering Intelligence

Product Evolution Framework can provide structured evidence for Engineering Intelligence.

It can feed:

- Prediction vs Reality: compare expected product evolution with certified new product reality.
- Recommendation Confidence: test whether Evolution Engine recommendations produce capability advancement.
- Engineering Learning: learn from successful, blocked, rejected, invalid, or low-ROI evolution attempts.
- Adaptive Engineering: improve future recommendations without Runtime self-modification.
- Recommendation Evolution: retire, revise, or strengthen capability strategies after real outcomes.

Engineering Intelligence remains advisory and OMP-governed.

The Evolution Engine must not become autonomous engineering authority.

## Relationship To OMP

This proposal may later become a future operational capability of existing OMP.

It is not a new OMP.

It is not a backlog replacement.

It is not a roadmap.

If validated later, OMP may own:

- product evolution admission;
- capability strategy routing;
- capability gap analysis routing;
- evidence gap analysis routing;
- Evolution Engine boundaries;
- campaign suggestion rules;
- operator review flow;
- stop gates;
- certification routing;
- capability advancement update routing;
- product reality update routing.

Until canonicalized, this document is only an editable design proposal.

## Open Questions

### Product Evolution

1. What product goals should be allowed to enter the framework?
2. How does V7 prevent Product Evolution from becoming a second roadmap?
3. Which product reality changes are important enough to trigger evolution analysis?
4. How should new product reality be recorded after failed or blocked evolution attempts?

### Target Management

1. How are Product Targets admitted?
2. Can several Product Targets be active?
3. Who approves Current Active Target?
4. Can Target priority change?
5. How does OMP choose the next Target?
6. How is Target Completion certified?
7. What prevents Target Catalog from becoming a roadmap?
8. Which owner records Current Active Target before canonicalization?

### Observation

1. Which owners may produce Product Observation?
2. How should observation freshness be represented?
3. How should conflicting observations be reconciled?
4. Which observations are too weak to create product goals?

### Capability Strategy

1. Is Capability Strategy later owned by OMP, Engineering Intelligence, or Production Maturity?
2. What is the minimum strategy packet required before gap analysis?
3. How does strategy remain non-roadmap and non-authorizing?

### Gap Analysis

1. Who performs Capability Gap Analysis?
2. Who performs Evidence Gap Analysis?
3. How are stale, missing, contradictory, or partial evidence gaps represented?
4. How does gap analysis avoid inventing work without measured evidence?

### Evolution Engine

1. Is Evolution Engine a future OMP rule, Engineering Intelligence read model, or dashboard-backed advisory model?
2. What inputs may it consume?
3. What outputs may it produce?
4. How is it prevented from becoming a planner?
5. How is it prevented from becoming automation?

### Campaign Generation

1. Who generates campaign suggestions?
2. Should the first generator be manual/operator-authored, read-only computed, or OMP-owned after validation?
3. How are sample thresholds defined?
4. What prevents a campaign from becoming a shadow backlog?
5. Should campaign IDs be stable before canonicalization?

### Certification

1. Which owner certifies capability advancement for each capability family?
2. How is Expected Capability Growth compared with certified growth?
3. When does campaign output become canonical?
4. How should campaign evidence expire or be refreshed?
5. How is new product reality certified after capability advancement?

### Dashboard

1. Should dashboard show Product Evolution before capability gaps and campaigns?
2. How should expected ROI be displayed without implying authority?
3. How should blocked campaigns be represented in CPS if campaigns become active?
4. How should cyclic evolution be visualized without becoming a roadmap?

### Engineering Intelligence

1. How should Engineering Intelligence compare expected evolution with actual new product reality?
2. How should recommendation confidence change after blocked or rejected campaigns?
3. Which adaptive read models are required before evolution learning becomes useful?
4. Can Evolution Metrics become Engineering Intelligence inputs without becoming authority?

### Automation

1. Which evidence is safe to collect without authority expansion?
2. What evidence collection could later be automated without Runtime apply?
3. What certification is required before any automated campaign suggestion is trusted?
4. What hard rule prevents Evolution Engine automation from becoming action automation?

## Canonical Readiness

This section classifies major V3 concepts.

Classification values:

- `DESIGN`: useful concept but not validated.
- `READY`: ready for focused discovery/validation.
- `CANONICAL`: already canonical elsewhere.
- `NOT_READY`: too vague, risky, or immature for migration.

| Concept | Classification | Reason |
| --- | --- | --- |
| Product Observation | `READY` | Reality First already exists; observation-to-goal routing needs validation. |
| Product Goal | `CANONICAL` | Product goals exist through Product Specification, OMP, and Production Maturity, but this framework's use is design-only. |
| Target Catalog | `DESIGN` | Useful organizing concept, but high roadmap-confusion risk until validated. |
| Current Active Target | `READY` | Current milestone already exists through Production Maturity / CPS, but target-management semantics are not canonical here. |
| Target Gap Analysis | `DESIGN` | Required before capability gaps, but owner and packet shape need validation. |
| Target Completion | `DESIGN` | Completion semantics must be certified before migration. |
| Target Selection | `DESIGN` | Important cyclic concept, but high priority/roadmap risk until constrained. |
| Capability Strategy | `DESIGN` | Useful abstraction, but owner and packet shape are not validated. |
| Capability Goal | `READY` | Capability lifecycle exists; goal vocabulary needs validation across capability families. |
| Capability Gap | `READY` | Gap model is generic and aligns with Production Maturity / Engineering Intelligence, but not canonical here. |
| Evidence Gap | `READY` | Evidence-gap thinking exists, but framework-level use needs validation. |
| Evolution Engine | `DESIGN` | Central V3 concept; high risk of becoming planner if not constrained. |
| Campaign Generator | `DESIGN` | Valid only as Evolution Engine subsystem; not ready as owner. |
| Operational Campaign | `DESIGN` | Mechanism exists in proposal only; no active system. |
| Capability Advancement | `READY` | Matches certified capability lifecycle; needs exact result classes. |
| Evolution Metrics | `DESIGN` | Useful future concepts; not ready for dashboard or scoring. |
| Dashboard | `READY` | Dashboard model exists, but Product Evolution visualization is design-only. |
| Engineering Intelligence relationship | `READY` | Existing EI owners can likely consume outcomes, but integration is not canonical. |
| OMP relationship | `READY` | OMP is the likely future owner after validation, but no migration yet. |

## Future Canonicalization

Canonicalization is postponed.

Only mature concepts may migrate.

Staged migration path:

```text
Design
-> Discovery
-> Validation
-> Canonical Readiness
-> OMP
-> Current Program State
-> Production Maturity
-> Dashboard
-> SYSTEM_MAP
-> Canonical Reference
```

Migration rules:

1. Design remains editable and non-canonical.
2. Discovery proves whether each concept already exists under another owner.
3. Validation proves the concept does not create a new roadmap, planner, owner, truth source, or authority path.
4. Canonical Readiness classifies each concept before migration.
5. OMP may receive only operating rules that belong to execution discipline, including target selection rules if validated.
6. Current Program State may receive only volatile Current Active Target state if target management becomes active.
7. Production Maturity may receive only target/maturity impact rules after certification semantics are proven.
8. Dashboard may receive only read-only visualization after canonical data owners exist.
9. SYSTEM_MAP may receive only ownership lookup.
10. Canonical Reference may receive only durable conclusions.

Target concepts may later migrate into:

| Target concept | Possible future destination | Migration condition |
| --- | --- | --- |
| Target Catalog | OMP / Production Maturity | Proven not to be a roadmap or backlog. |
| Current Active Target | Current Program State / OMP | Proven as volatile execution focus, not a queue. |
| Target Gap Analysis | OMP / Production Maturity | Proven to route to capability gaps before campaigns. |
| Target Completion | Production Maturity / OMP | Certification semantics and completion owner validated. |
| Target Selection | OMP | Proven advisory until existing owners certify next target. |

No migration should occur until review proves the concept is stable, owner-mapped, non-duplicative, and safe.

Until then:

```text
STATUS: DESIGN PROPOSAL
CANONICAL: NO
IMPLEMENTATION: NOT STARTED
```
