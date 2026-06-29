# Product Evolution Through Operational Maturity Campaigns

STATUS: DESIGN PROPOSAL
CANONICAL: NO
OWNER: OMP after validation, not yet
IMPLEMENTATION: NOT STARTED

## Purpose

This proposal defines a future Product Evolution Framework for V7 based on Capability Growth.

Operational Maturity Campaigns are only one mechanism inside that framework. They are not the center of the model.

The center is:

```text
Product Evolution through certified Capability Growth.
```

V7 has completed the actionable implementation backlog, while Production Maturity remains `66.9 / 100`. The next milestone is `80% Runtime Production Ready`, but maturity should not be treated as a passive score waiting to rise. Future product growth should be driven by explicit product goals, capability goals, capability gaps, evidence gaps, operator-reviewed campaigns, certification, and measured capability advancement.

## Design Status

This document is editable design only.

It is not canonical.

It does not modify OMP, Runtime, Production Maturity, Dashboard, authority, automation, production behavior, Current Program State, SYSTEM_MAP, or any canonical owner.

It does not create an active campaign system.

It does not create a new roadmap, OMP, backlog, planner, Runtime, owner, truth source, authority model, or execution mode.

## Product Evolution Model

The proposed model is:

```text
Product Goal
-> Capability Goal
-> Capability Gap
-> Evidence Gap
-> Operational Campaign
-> Evidence
-> Certification
-> Capability Growth
-> Product Evolution
```

Expanded operating model:

```text
Goal
-> Capability Strategy
-> Capability Gap Analysis
-> Evidence Gap Analysis
-> Campaign Generator
-> Suggested Campaigns
-> Operator Review
-> Campaign Approval
-> Evidence Collection
-> Certification
-> Capability Growth
-> Product Evolution
```

This model makes campaign work subordinate to capability growth. A campaign succeeds only when it produces certifiable evidence that advances a capability. A campaign that collects data but does not advance a capability is incomplete, blocked, or mis-scoped.

## Non-Goals

This proposal does not replace OMP.

It does not create a new OMP, roadmap, backlog, planner, Runtime, owner, truth source, authority model, automation mode, or product strategy owner.

It does not enable automation, expand authority, mutate Runtime, move users, approve Runtime apply, bypass certification, or create synthetic evidence.

It does not change Production Maturity directly. Maturity changes only after evidence is certified through existing owners.

It does not execute campaigns. It defines a future design language only.

It does not make campaigns the goal. Campaigns are a means to capability advancement.

## Definitions

Product Goal:
A product-level desired outcome, such as becoming Runtime Production Ready, improving Time-To-Safe-Recovery, increasing prediction confidence, or proving bounded autonomy readiness.

Capability Goal:
The specific capability state required to serve a product goal. Examples include Runtime Readiness, Prediction Confidence, Rollback Reliability, Recovery Admission, Engineering Intelligence, Runtime Time Intelligence, Movement Protection, Authority Evolution, or a future capability admitted through OMP.

Capability Strategy:
The proposed approach for moving a capability from its current certified state toward the target state while reusing existing owners and preserving safety, authority, verification, rollback, and STOP_SAFE constraints.

Capability Gap:
The measurable distance between current capability state and target capability state. This replaces the V1 term "Production Maturity Gap" as the primary abstraction. Production Maturity gaps are only one type of capability gap.

Evidence Gap:
The missing evidence required to close or reduce a capability gap. Evidence gaps name source owner, evidence type, required sample or quality bar, certification owner, freshness/expiry rules, and stop gates.

Campaign Generator:
A proposed future design component or OMP-owned rule that converts capability gaps and evidence gaps into suggested campaigns. It is non-authorizing and does not execute anything.

Operational Campaign:
A proposed, bounded evidence effort generated from a capability gap and evidence gap. A campaign may collect evidence and recommend action, but it cannot execute Runtime behavior, grant authority, move users, or update maturity by itself.

Evidence Yield:
The advisory evidence produced by a campaign before certification. Yield may estimate possible capability growth, production impact, investment cost, and ROI, but it is not certified maturity.

Operational Investment:
The expected effort and risk profile of a campaign, including evidence cost, engineering cost, operational cost, risk, and expected ROI.

Capability Advancement:
The certified improvement of a capability after evidence is collected and validated. This replaces "Campaign Completion" as the success target.

Campaign Certification:
The existing-owner review that decides whether campaign evidence is valid enough to advance a capability, update Production Maturity, improve confidence, support authority review, or close a gap.

Campaign Stop Gate:
A hard boundary that prevents campaign progress, such as missing operator approval, Runtime apply requirement, authority expansion requirement, user movement requirement, synthetic evidence risk, unsafe production action, or uncertified owner.

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
| Future capabilities | New product capability is proposed. | Existing owner check, capability fit, missing evidence, certification owner, and safe implementation path. |

Every capability gap must name:

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
- expected capability growth if certified.

## Capability Strategy

Capability Strategy is the design step between goal and campaign.

It answers:

1. What product goal is being served?
2. Which capability must grow?
3. What is the current certified capability state?
4. What target state is needed?
5. Which existing owner owns the capability?
6. Which evidence is missing?
7. Which campaign, if any, can safely collect that evidence?
8. What operational investment is required?
9. What risk is introduced?
10. What capability growth would certification unlock?

Capability Strategy must not become a roadmap or backlog. It is a scoped analysis that may later be routed through OMP only if validated.

## Campaign Generation Rule

Campaigns must never be manually invented.

Every campaign must originate from:

```text
Capability Gap
-> Evidence Gap
-> Campaign Generator
```

A suggested campaign is invalid unless it can trace to:

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
- expected production impact;
- operational investment.

If a campaign cannot trace to a capability gap and evidence gap, it must be rejected, rewritten, or left as an open question.

## Campaign Lifecycle

Campaign lifecycle remains useful, but it is no longer the top-level lifecycle.

```text
Capability Gap Detected
-> Evidence Gap Identified
-> Campaign Suggested
-> Operator Reviewed
-> Campaign Approved
-> Evidence Collected
-> Evidence Certified
-> Capability Advanced
-> Product Evolution Updated
-> Next Capability Gap Analysis
```

Capability Gap Detected:
An existing owner shows that current capability state is below a product or maturity target.

Evidence Gap Identified:
The missing proof is named with source owner, sample or quality requirement, certification owner, and stop gates.

Campaign Suggested:
Campaign Generator proposes one or more bounded evidence campaigns. Suggestions are non-authorizing.

Operator Reviewed:
The operator reviews product goal, capability goal, evidence, allowed actions, forbidden actions, stop gates, operational investment, expected ROI, and expected capability growth.

Campaign Approved:
The operator approves only campaign scope, not Runtime apply, automation, authority expansion, rollback execution, or user movement.

Evidence Collected:
Evidence is collected through existing owners. Collection may include read-only snapshots, governed outcomes, operator-reviewed operational evidence, or certified observation.

Evidence Certified:
Existing certification owners validate the evidence.

Capability Advanced:
The capability advances only if evidence certification passes.

Product Evolution Updated:
Production Maturity, Engineering Intelligence, Dashboard, CPS, or OMP may be updated later only if their canonical owners are valid destinations and the concept has matured beyond design proposal.

Next Capability Gap Analysis:
The system identifies the next capability gap from certified state, not from campaign enthusiasm.

## Campaign Types

Initial candidate campaign types remain examples only. Each must be generated from a capability gap and evidence gap.

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

## Capability-Oriented Data Model

Suggested fields:

| Field | Meaning |
| --- | --- |
| `product_goal` | Product-level outcome the work serves. |
| `capability_goal` | Target capability state. |
| `capability_id` | Existing capability or future OMP-admitted capability. |
| `current_capability_state` | Current certified state. |
| `target_capability_state` | Desired certified state. |
| `capability_gap` | Measurable difference between current and target state. |
| `evidence_gap` | Missing evidence required to advance capability. |
| `campaign_id` | Stable campaign identifier if a campaign is generated. |
| `campaign_type` | Suggested campaign type. |
| `evidence_owner` | Existing owner that produces or stores evidence. |
| `certification_owner` | Existing owner that certifies evidence. |
| `required_sample_count` | Required sample threshold, if known. |
| `collected_sample_count` | Current collected evidence count. |
| `expected_capability_growth` | Advisory capability movement if evidence is certified. |
| `expected_production_impact` | Advisory effect on Production Maturity or product readiness. |
| `evidence_yield` | Advisory value of collected evidence before certification. |
| `evidence_cost` | Cost to gather required evidence. |
| `engineering_cost` | Cost to build or extend read-only/supporting surfaces if later approved. |
| `operational_cost` | Operator/runtime/production effort or disruption cost. |
| `risk` | Safety, authority, operational, or product risk. |
| `expected_roi` | Expected capability/production value relative to investment and risk. |
| `stop_gates` | Boundaries that stop the campaign. |
| `allowed_actions` | Actions permitted inside campaign scope. |
| `forbidden_actions` | Actions forbidden even if they could produce evidence faster. |
| `capability_advancement_criteria` | Conditions for capability growth after certification. |
| `certification_result` | Result after certification review. |

Example shape:

```text
product_goal: 80% Runtime Production Ready
capability_goal: Runtime Readiness can safely consume prepared gates
capability_id: Runtime Readiness
current_capability_state: read-only readiness surfaces complete; runtime_apply blocked
target_capability_state: certified runtime-readiness evidence for authority review
capability_gap: missing certified operational readiness evidence
evidence_gap: freshness/authority/rollback/verification/anti-flap/blast STOP_SAFE outcomes
campaign_id: OMC-RUNTIME-READINESS-001
campaign_type: Runtime Readiness Campaign
evidence_owner: existing Runtime Eligibility / OMP read-model owners
certification_owner: existing OMP / Production Maturity certification owners
required_sample_count: TBD
collected_sample_count: 0
expected_capability_growth: Runtime Readiness moves closer to Runtime Production Ready
expected_production_impact: advisory only until certified
evidence_yield: TBD, advisory only
evidence_cost: TBD
engineering_cost: TBD
operational_cost: TBD
risk: unsafe readiness interpretation, authority confusion, stale evidence
expected_roi: TBD
stop_gates: Runtime apply, authority expansion, user movement, automation
allowed_actions: read-only evidence review, approved governed evidence collection
forbidden_actions: runtime mutation, automation, authority expansion, synthetic evidence
capability_advancement_criteria: required evidence certified and stop gates respected
certification_result: NOT_REVIEWED
```

## Evidence Yield And Operational Investment

V1 treated Evidence Yield mainly as expected maturity gain.

V2 separates five advisory concepts:

| Concept | Meaning | Certification rule |
| --- | --- | --- |
| Expected Capability Growth | How far a capability might advance if evidence is certified. | Advisory until certification. |
| Expected Production Impact | Possible effect on Production Maturity or milestone readiness. | Advisory until Production Maturity owner updates score. |
| Evidence Yield | Value and coverage of collected evidence. | Cannot update maturity by itself. |
| Operational Investment | Evidence cost, engineering cost, operational cost, and risk. | Used for operator review, not authority. |
| Expected ROI | Expected value relative to investment and risk. | Advisory; cannot override safety or certification. |

Operational Investment dimensions:

- Expected Maturity Gain;
- Evidence Cost;
- Engineering Cost;
- Operational Cost;
- Risk;
- Expected ROI.

These are design concepts only.

Nothing updates Production Maturity, authority, Runtime behavior, or capability state before certification.

## Safety Rules

Campaigns may:

- collect evidence through existing owners;
- recommend operator-reviewed action;
- expose missing evidence;
- estimate expected capability growth;
- estimate expected production impact;
- estimate operational investment;
- prepare certification packets;
- update campaign progress after evidence is collected.

Campaigns may not:

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
- declare capability growth without certification.

## Dashboard Relationship

If this proposal is later canonicalized, OMP Dashboard may display Product Evolution and Capability Growth views.

Suggested read-only dashboard areas:

- product goal;
- capability goal;
- current capability state;
- target capability state;
- capability gap;
- evidence gap;
- suggested campaigns;
- active campaigns;
- expected capability growth;
- expected production impact;
- evidence yield;
- operational investment;
- expected ROI;
- missing evidence;
- blockers;
- stop gates;
- certification status;
- next operator review.

Dashboard display must remain read-only and consume canonical owners only after canonicalization.

Dashboard must not become a campaign generator, authority surface, execution surface, truth source, maturity writer, or second OMP.

## Relationship To Engineering Intelligence

Product Evolution through Capability Growth can produce structured real outcomes for Engineering Intelligence.

It can feed:

- Prediction vs Reality: compare expected capability growth / expected ROI with certified results.
- Recommendation Confidence: test whether suggested campaigns and capability strategies produce certified growth.
- Engineering Learning: learn from successful, blocked, rejected, or low-yield campaigns.
- Adaptive Engineering: improve future recommendations without Runtime self-modification.
- Recommendation Evolution: retire, revise, or strengthen capability strategies after real outcomes.

Engineering Intelligence remains advisory and OMP-governed.

Campaigns do not make Engineering Intelligence autonomous. They provide certified evidence for existing learning owners.

## Relationship To OMP

This proposal may later become a future Operational Mode of existing OMP.

It is not a new OMP.

It is not a backlog replacement.

It is not a roadmap.

If validated later, OMP may own:

- capability strategy admission;
- capability gap analysis routing;
- evidence gap analysis routing;
- campaign suggestion rules;
- operator review flow;
- stop gates;
- certification routing;
- capability growth update routing;
- product evolution update routing.

Until canonicalized, this document is only an editable design proposal.

## Open Questions

### Architecture

1. Is Capability Strategy a section of OMP, Production Maturity, or Engineering Intelligence after validation?
2. Does any part of this model require a new canonical concept, or can all mature parts fit existing owners?
3. What prevents Product Evolution Framework from becoming a parallel roadmap?

### Capability Growth

1. How is current capability state measured consistently across Runtime Readiness, Prediction Confidence, Rollback Reliability, Recovery, Engineering Intelligence, and future capabilities?
2. What is the minimum evidence required to claim Capability Advancement?
3. Can one campaign advance multiple capabilities, and how is double counting prevented?
4. Which capability should be targeted first after `66.9 / 100` Production Maturity?

### Gap Analysis

1. Who performs Capability Gap Analysis?
2. Who performs Evidence Gap Analysis?
3. How are stale, missing, contradictory, or partial evidence gaps represented?
4. How does gap analysis avoid inventing work without measured evidence?

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

### Dashboard

1. Should dashboard show Product Evolution first and campaigns second?
2. How should expected ROI be displayed without implying authority?
3. How should blocked campaigns be represented in CPS if campaigns become active?

### Engineering Intelligence

1. How should Engineering Intelligence compare expected campaign ROI with certified outcome?
2. How should recommendation confidence change after blocked or rejected campaigns?
3. Which adaptive read models are required before campaign learning becomes useful?

### Future Automation

1. Which evidence is safe to collect without authority expansion?
2. What evidence collection could later be automated without Runtime apply?
3. What certification is required before any automated campaign suggestion is trusted?
4. What hard rule prevents campaign automation from becoming action automation?

## Future Canonicalization Plan

Canonicalization is postponed.

Only mature concepts may migrate later.

Possible staged migration:

| Stage | Mature concept | Possible future destination | Migration condition |
| --- | --- | --- | --- |
| 1 | Capability Strategy vocabulary | OMP or Engineering Intelligence | Validated as non-roadmap, owner-reusing analysis. |
| 2 | Capability Gap / Evidence Gap definitions | Production Maturity, OMP, or Engineering Intelligence | Proven generic across multiple capability families. |
| 3 | Campaign Generation Rule | OMP | Proven to prevent manual campaign invention and shadow backlog creation. |
| 4 | Operational Investment / Expected ROI | Engineering Intelligence and Dashboard | Proven advisory, non-authorizing, and safety-subordinate. |
| 5 | Active campaign state | Current Program State | Only if campaigns become active and volatile state must be tracked. |
| 6 | Owner mappings | SYSTEM_MAP | Only if mature owner lookup is needed. |
| 7 | Read-only visualization | Dashboard | Only after canonical data owners exist. |
| 8 | Durable conclusions | Canonical Reference | Only final durable rules, not proposal details. |

No migration should occur until review proves the concept is stable, owner-mapped, non-duplicative, and safe.

Until then:

```text
STATUS: DESIGN PROPOSAL
CANONICAL: NO
IMPLEMENTATION: NOT STARTED
```
