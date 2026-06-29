# Operational Maturity Campaigns

STATUS: DESIGN PROPOSAL
CANONICAL: NO
OWNER: OMP after validation, not yet
IMPLEMENTATION: NOT STARTED

## Purpose

Operational Maturity Campaigns are a proposed mechanism for turning certified production maturity gaps into focused evidence work after implementation completion.

V7 has completed the actionable implementation backlog, but Production Maturity remains below `100%` because production readiness depends on certified testing, real outcomes, authority evolution, and bounded autonomy evidence. Campaigns exist so V7 does not wait passively for these percentages to improve.

Campaigns would make the gap between current Production Maturity and the next certified target visible, measurable, reviewable, and evidence-driven.

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

## Non-Goals

Operational Maturity Campaigns do not replace OMP.

They do not create a new OMP, roadmap, backlog, planner, Runtime, owner, truth source, or authority model.

They do not enable automation, expand authority, mutate Runtime, move users, approve Runtime apply, bypass certification, or create synthetic evidence.

They do not change Production Maturity directly. Maturity changes only after evidence is certified through existing owners.

They do not execute campaigns. This proposal defines a future design language only.

## Definitions

Production Maturity Gap:
The measurable difference between the current Production Maturity state and the next certified target, such as `66.9 / 100` toward `80% Runtime Production Ready`.

Certified Gap Analysis:
An owner-reviewed analysis that identifies which maturity categories, evidence types, gates, or certifications prevent reaching the next target.

Evidence Requirement:
A specific missing evidence class required to close a maturity gap, including source owner, sample need, quality bar, certification owner, and stop gates.

Operational Campaign:
A proposed, bounded evidence effort generated from a certified maturity gap. A campaign may collect evidence and recommend action, but it cannot execute Runtime behavior or grant authority.

Evidence Yield:
The estimated maturity value of evidence collected by a campaign before certification. Evidence Yield is advisory only and cannot update Production Maturity.

Campaign Completion:
The state where required evidence has been collected, stop gates remain respected, and the campaign is ready for certification review.

Campaign Certification:
The existing-owner review that decides whether campaign evidence is valid enough to update Production Maturity, authority readiness, runtime readiness, or another certified maturity surface.

Campaign Stop Gate:
A hard boundary that prevents campaign progress, such as missing operator approval, Runtime apply requirement, authority expansion requirement, user movement requirement, synthetic evidence risk, unsafe production action, or uncertified owner.

## Campaign Generation Rule

Campaigns may be suggested only from measurable gaps between current maturity and the next certified target.

No campaign may be invented manually without:

- current Production Maturity value;
- next certified target;
- maturity category gap;
- missing evidence;
- existing evidence owner;
- existing certification owner;
- stop gates;
- expected maturity gain estimate.

If a proposed campaign cannot trace back to a measured gap, it must be rejected or rewritten as an open question.

## Campaign Lifecycle

```text
Gap Detected
-> Campaign Suggested
-> Operator Reviewed
-> Campaign Approved
-> Evidence Collected
-> Evidence Certified
-> Maturity Updated
-> Campaign Closed
-> Next Gap Analysis
```

Gap Detected:
Production Maturity and target delta reveal a measurable gap.

Campaign Suggested:
OMP or a future OMP-owned read model proposes a campaign from the gap. The suggestion is non-authorizing.

Operator Reviewed:
The operator reviews purpose, evidence, allowed actions, forbidden actions, stop gates, and expected gain.

Campaign Approved:
The operator approves only the campaign scope, not Runtime apply, automation, authority expansion, or user movement.

Evidence Collected:
Evidence is collected through existing owners. Collection may include observation, read-only snapshots, governed outcomes, or approved operational evidence.

Evidence Certified:
Existing certification owners validate the evidence.

Maturity Updated:
Production Maturity changes only if certification passes.

Campaign Closed:
Campaign state is closed as certified, rejected, blocked, or superseded.

Next Gap Analysis:
OMP recalculates the next measurable gap.

## Campaign Types

Initial candidate campaign types:

| Campaign Type | Purpose | Example Evidence | Primary Risk |
| --- | --- | --- | --- |
| Prediction Validation Campaign | Compare predictions with real outcomes. | Prediction vs Reality rows, forecast accuracy, confidence updates. | Treating predicted yield as certified maturity. |
| Rollback Evidence Campaign | Prove rollback/no-rollback and compensation behavior. | Governed rollback/no-rollback outcomes, containment/forward-fix closure. | Executing rollback without authority. |
| Recovery Evidence Campaign | Prove recovered channel readiness and slow-start safety. | Recovery admission, observation windows, successful readiness evidence. | Admitting traffic without certification. |
| Authority Confidence Campaign | Build evidence for future action-class or delegated authority review. | Certified class evidence, operator decisions, outcome stability. | Silent authority expansion. |
| Runtime Readiness Campaign | Prove Runtime can consume prepared gates safely. | Eligibility, freshness, blast, rollback, anti-flap, verification, learning gates. | Treating readiness as apply permission. |
| Bounded Autonomy Readiness Campaign | Prepare evidence for future bounded autonomy certification. | Governed outcomes, STOP_SAFE proof, readiness, rollback evidence. | Enabling automation before approval. |
| STOP_SAFE Evidence Campaign | Prove unsafe paths stop correctly. | Stop reason distribution, blocked action traces, no-mutation proof. | Creating synthetic negative evidence. |
| Anti-Flap Evidence Campaign | Prove oscillation prevention and state-change cost behavior. | Cooldown, hysteresis, target block/quarantine, pair reversal evidence. | Changing thresholds or formulas. |
| Time-To-Safe-Recovery Campaign | Measure time from issue detection to safe recovery state. | Observation time, readiness time, decision time, verification time, recovery closure. | Optimizing time by weakening safety. |

## Campaign Data Model

Proposed fields:

| Field | Meaning |
| --- | --- |
| `campaign_id` | Stable campaign identifier. |
| `source_gap` | Measured maturity gap that generated the campaign. |
| `maturity_target` | Next certified target the campaign supports. |
| `current_score` | Current score for the relevant maturity category or overall Production Maturity. |
| `target_score` | Target score required for the maturity step. |
| `missing_evidence` | Evidence required but not yet certified. |
| `required_sample_count` | Required sample threshold, if known. |
| `collected_sample_count` | Current collected evidence count. |
| `evidence_owner` | Existing owner that produces or stores evidence. |
| `certification_owner` | Existing owner that certifies evidence. |
| `expected_maturity_gain` | Estimated gain if evidence is certified. Advisory until certification. |
| `stop_gates` | Boundaries that stop the campaign. |
| `allowed_actions` | Actions permitted inside the campaign scope. |
| `forbidden_actions` | Actions forbidden even if they could produce evidence faster. |
| `completion_criteria` | Conditions for campaign completion before certification. |
| `certification_result` | Result after certification review. |

Example shape:

```text
campaign_id: OMC-RUNTIME-READINESS-001
source_gap: Production Maturity 66.9 -> 80.0
maturity_target: 80% Runtime Production Ready
current_score: 66.9
target_score: 80.0
missing_evidence: certified runtime consumption readiness evidence
required_sample_count: TBD
collected_sample_count: 0
evidence_owner: existing Runtime Eligibility / OMP read-model owners
certification_owner: existing OMP / Production Maturity certification owners
expected_maturity_gain: TBD, advisory only
stop_gates: Runtime apply, authority expansion, user movement, automation
allowed_actions: read-only evidence review, approved governed evidence collection
forbidden_actions: runtime mutation, automation, authority expansion, synthetic evidence
completion_criteria: required evidence collected and stop gates respected
certification_result: NOT_REVIEWED
```

## Evidence Yield

Evidence Yield estimates how much maturity a campaign may unlock if certification succeeds.

Evidence Yield is not Production Maturity.

Evidence Yield may be displayed as:

- expected maturity gain;
- confidence range;
- missing evidence count;
- certified evidence count;
- blocker reduction;
- readiness movement toward the next target.

Production Maturity may change only after campaign evidence is certified by existing owners.

Uncertified campaign progress must remain advisory.

## Safety Rules

Campaigns may:

- collect evidence through existing owners;
- recommend operator-reviewed action;
- expose missing evidence;
- estimate expected maturity gain;
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
- write Production Maturity directly.

## Dashboard Integration

OMP Dashboard should eventually display campaigns as read-only operational maturity views.

Suggested dashboard fields:

- active campaigns;
- campaign type;
- source gap;
- next certification target;
- progress bars;
- missing evidence;
- collected evidence;
- expected maturity gain;
- blockers;
- stop gates;
- certification status;
- next operator review.

Dashboard display must remain read-only and consume canonical owners only after canonicalization.

## Relationship To Engineering Intelligence

Campaigns would create structured real outcomes for Engineering Intelligence.

They can feed:

- Prediction vs Reality: campaigns compare expected evidence yield and actual certification outcome.
- Recommendation Confidence: campaign recommendations become measurable against certified results.
- Engineering Learning: successful, blocked, or rejected campaigns teach future placement and evidence strategy.
- Adaptive Engineering: repeated campaign outcomes can improve future recommendations without Runtime self-modification.

Campaigns do not make Engineering Intelligence autonomous. They provide certified evidence for existing learning owners.

## Relationship To OMP

Campaigns are a proposed future Operational Mode of existing OMP.

They are not a new OMP.

They are not a backlog replacement.

They are not a roadmap.

If validated later, OMP would own campaign suggestion rules, stop gates, operator review, certification flow, and maturity update routing.

Until canonicalized, this document is only an editable design proposal.

## Open Questions

1. Who generates campaign suggestions?
2. How are sample thresholds defined?
3. How is expected maturity gain calculated?
4. Which campaign can start first after `66.9%`?
5. Which evidence is safe to collect without authority expansion?
6. How does operator approval work?
7. When does campaign output become canonical?
8. Can campaign suggestions be purely read-only at first?
9. Which maturity categories may be affected by one campaign?
10. How should blocked campaigns be represented in CPS?
11. Should campaign IDs be stable before canonicalization?
12. How should optional Tier D future-scope items interact with campaigns?
13. What prevents a campaign from becoming a shadow backlog?
14. How should campaign evidence be expired or refreshed?

## Future Canonicalization Plan

If validated, parts of this proposal may later move into existing owners:

| Destination | Possible Future Content |
| --- | --- |
| OMP | Campaign lifecycle, generation rule, stop gates, operator review flow. |
| Production Maturity Model | How certified campaign outcomes affect maturity categories. |
| SYSTEM_MAP | Owner lookup for campaign evidence, certification, and dashboard display. |
| Current Program State | Current active campaign state, if campaigns become active. |
| Canonical Reference | Durable conclusions only, such as campaign safety rules and non-goals. |
| Dashboard | Read-only campaign visibility, progress, blockers, expected gain, and certification target. |

Canonicalization must happen only after review.

Until then:

```text
STATUS: DESIGN PROPOSAL
CANONICAL: NO
IMPLEMENTATION: NOT STARTED
```
