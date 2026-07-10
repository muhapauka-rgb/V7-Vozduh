# V7 Behaviour Surface Discovery

Status: `INDEPENDENT_RESEARCH`
Question: Does V7 have a real Behaviour Surface level?
Date: `2026-07-08`

## 1. Purpose

This research answers one question:

```text
Does Behaviour Surface exist in V7 as a real engineering reality, or is it only a convenient classification?
```

This report does not:

- change AEP;
- change AOS;
- change Behaviour Discovery Program;
- change Current Autonomous Behaviour Reality;
- change `LOCKED_ARCHITECTURE`;
- change `LOCKED_KNOWLEDGE`;
- execute Discovery;
- create a new architecture;
- create a new entity;
- create a new owner;
- create a new truth source.

## 2. Method

The research used existing project evidence:

- AEP;
- AOS;
- Current Autonomous Behaviour Reality;
- Behaviour Discovery Program;
- Behaviour Reality Validation;
- Function Graph;
- SYSTEM_MAP;
- Runtime Model;
- Decision Model;
- policies;
- implementation source;
- reports;
- Canonical Knowledge.

No new Behaviour Discovery execution was performed.

## 3. Surface Definition Test

A Behaviour Surface exists only when a group of Behaviours has a stable shared engineering shape:

- common engineering purpose;
- common sources;
- common boundaries;
- common Runtime or read/runtime path;
- common Decision model;
- common Verification path;
- common Learning or continuation path;
- common Consumers;
- common Owners.

If these are missing, the candidate is `CONCEPTUAL_ONLY`.

If evidence shows stable implementation/source/owner/consumer boundaries, the candidate is `OBSERVED_ENGINEERING_SURFACE`.

## 4. Observed Surfaces

| Surface | Status | Evidence Summary | Reason |
| --- | --- | --- | --- |
| Routing / Decision Surface | `OBSERVED_ENGINEERING_SURFACE` | `admin_core/operator_decision_surface.py`, `admin_core/routing_brain.py`, `admin_core/routing_intelligence.py`, Decision Model, Function Graph, routing tests. | Stable behaviour cluster around candidate evaluation, policy filtering, service validation, trust/prediction scoring, best-pool recommendation, operator proposal. |
| Runtime / Execution Guard Surface | `OBSERVED_ENGINEERING_SURFACE` | `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, Runtime Model, execution lease, restore barrier, governed canary evidence/tests. | Stable cluster around admission, lease/version readiness, restore barrier, dry-run/apply selection, execution guard, STOP_SAFE. |
| Verification / Truth Closure Surface | `OBSERVED_ENGINEERING_SURFACE` | truth/convergence reports, `tools/v7_sync_lib.py`, verification policies, runtime read diagnostics, terminal classification tests. | Stable cluster around runtime convergence, terminal classification, read diagnostics, scoped verification, certification truth closure. |
| Rollback / Restore Surface | `OBSERVED_ENGINEERING_SURFACE` | rollback policy, restore barrier clearance, rollback authority certification, rollback tests/reports. | Stable safety surface around rollback readiness, authority review, restore clearance, post-rollback verification/learning. |
| Learning / Outcome Surface | `OBSERVED_ENGINEERING_SURFACE` | `admin_core/operator_execution_feedback.py`, `admin_core/intelligence_workers.py`, trust evolution, prediction feedback, decision-to-outcome reports. | Stable cluster around outcome quality, learning records, trust evolution, prediction feedback, recommendation confidence. |
| Authority / Policy Surface | `OBSERVED_ENGINEERING_SURFACE` | OMP, Decision Model, policies, `admin_core/autonomy_trust_acceleration.py`, action-class runtime enablement, delegated autonomy eligibility, blast-radius evidence. | Stable cluster around authority requirement, action-class classification, blast-radius boundary, approval, runtime eligibility. |
| Deployment / Convergence Surface | `OBSERVED_ENGINEERING_SURFACE` | `tools/v7_sync_lib.py`, deploy manifests, runtime linkage, safe-deploy evidence, post-deploy truth/convergence reports. | Stable cluster around manifest production, safe deploy, runtime linkage, post-deploy convergence, deploy hold/rollback decision. |
| Operator / Admin Visibility Surface | `OBSERVED_ENGINEERING_SURFACE` | `admin_core/operator_observability.py`, `admin_core/overview_views.py`, `admin_core/runtime_read_views.py`, `admin_core/diagnostic_views.py`, admin/API tests. | Stable read-only surface around overview, runtime diagnostics, decision preview, audit/evidence search, governance/execution preview. |
| Production Certification / Maturity Surface | `OBSERVED_ENGINEERING_SURFACE` | Production Maturity Model, controlled production certification reports, CPS, SYSTEM_MAP, engineering reports. | Stable owner/consumer surface around production evidence consumption, certification review, maturity decision, CPS state recording. |
| Knowledge / Canonical Sync Surface | `OBSERVED_ENGINEERING_SURFACE` | Stage 2 Knowledge program/reports, Canonical Knowledge, Knowledge Lock, AEP foundation synchronization. | Stable documentation/program surface around knowledge detection, owner evaluation, canonical sync, foundation synchronization, no-change recording. |
| Engineering / Report Surface | `OBSERVED_ENGINEERING_SURFACE` | Engineering reports, certification sections, review gates, State Transition Law, Behaviour Discovery Program. | Stable engineering behaviour surface around command interpretation, report production, review, evidence recording, next-action explanation. |

## 5. Conceptual Surfaces

| Candidate Surface | Status | Reason |
| --- | --- | --- |
| Experience Surface | `CONCEPTUAL_ONLY` | Outcome/user/service evidence exists, but the stable surface is currently Learning / Outcome or Production Maturity. A standalone Experience Surface lacks proven owner, consumer, and verification boundary. |
| General Autonomy Surface | `CONCEPTUAL_ONLY` | Too broad. Autonomy is the system goal and AEP route, not a bounded engineering surface with one shared runtime/decision/verification path. |
| Whole Runtime Surface | `CONCEPTUAL_ONLY_AS_SINGLE_SURFACE` | Runtime-related behaviour exists, but one broad Runtime Surface would combine execution guard, read diagnostics, convergence, deployment, and authority. Observed surfaces are narrower. |
| Whole Production Surface | `CONCEPTUAL_ONLY_AS_SINGLE_SURFACE` | Production behaviour exists, but as certification/maturity, deployment/convergence, and runtime evidence surfaces. A single broad Production Surface hides independent behaviours. |
| Whole Engineering Surface | `CONCEPTUAL_ONLY_AS_SINGLE_SURFACE` | Engineering/report surface exists, but all engineering behaviour as one surface would be too broad. |

## 6. Rejected Surfaces

| Candidate | Result | Reason |
| --- | --- | --- |
| Behaviour Surface as new architecture layer | `REJECTED` | Observed surfaces exist, but they do not require a new architecture level, owner, truth source, storage, or program route. |
| Function Graph Surface | `REJECTED` | Function Graph is a discovery/evidence index, not a Behaviour Surface. |
| Repository Surface as Behaviour Surface | `REJECTED` | Repository is a discovery surface/source area, not engineering Behaviour. |
| AOS Surface | `REJECTED` | AOS is an ideal target model, not current observed Behaviour Surface. |
| Architecture Surface | `REJECTED` | Architecture explains Reality but does not define observed Behaviour Surface by itself. |

## 7. Surface Evidence

| Evidence Family | Surface Evidence |
| --- | --- |
| AEP | Provides Behaviour Definition / Behaviour Instance model and confirms behaviour is not file/function based. |
| Behaviour Discovery Program | Already defines discovery passes by evidence surfaces, but not as architecture surfaces. |
| Current Autonomous Behaviour Reality | Shows stable behaviour clusters: routing, authority, runtime guard, verification, learning, production, deployment, visibility, knowledge sync. |
| Behaviour Reality Validation | Confirms many observed independent behaviours cluster naturally under stable purposes and owners. |
| Function Graph | Proves implementation-level producers, consumers, mutation/read-only paths, tests, and Domain 11 addendum. |
| SYSTEM_MAP | Provides owner/consumer relationships and module surfaces. |
| Decision Model | Explicitly mentions decision surfaces and separates decision from execution/runtime. |
| Runtime Model | Provides runtime, verification, rollback, and thin-runtime boundaries. |
| Policies | Provide authority, rollback, freshness, anti-flap, blast-radius, degradation boundaries. |
| Implementation | Provides source-code surfaces for routing, execution, verification, learning, deployment, diagnostics. |
| Reports | Provide certification, production, deployment, engineering, and knowledge-sync evidence. |

## 8. Surface Validation

| Surface | Common Purpose | Common Sources | Common Boundaries | Common Decision | Common Verification | Common Learning / Continuation | Common Consumers | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Routing / Decision | Candidate/action recommendation | decision surface, routing brain, intelligence | read-only advisory, no authority | recommend/block/no-action/proposal | tests, decision surface validation | confidence/trust feedback | operator, execution guard, OMP | `PASS` |
| Runtime / Execution Guard | Governed execution or STOP_SAFE | execution pipeline, Runtime Model | authority/runtime gates | dry-run/apply/hold/stop | lease, restore, terminal checks | execution feedback | verification, rollback, operator | `PASS` |
| Verification / Truth Closure | Prove state/action truth | truth tools, runtime read, reports | verification target boundaries | pass/fail/unknown/timeout | truth/convergence/terminal classification | maturity/learning handoff | OMP, Production Maturity, reports | `PASS` |
| Rollback / Restore | Preserve recovery safety | rollback policy, restore barrier, authority cert | no automatic rollback authority | rollback/hold/manual review | rollback readiness, restore clearance | post-rollback feedback | execution guard, authority, learning | `PASS` |
| Learning / Outcome | Convert outcomes to future evidence | feedback, intelligence snapshots | observed outcomes only | update/no-change | feedback tests, outcome quality | trust/prediction/confidence | routing, OMP, dashboards | `PASS` |
| Authority / Policy | Bound action legality | policies, OMP, action class, authority | authority/action-class/blast gates | approve/deny/hold/narrow | authority reviews/tests | maturity/OMP state | runtime guard, operator, OMP | `PASS` |
| Deployment / Convergence | Prove deployed state | deploy tooling, manifests, reports | safe deploy/runtime linkage | deploy/hold/rollback/no-op | post-deploy convergence | reports/maturity handoff | production, OMP, CPS | `PASS` |
| Operator / Admin Visibility | Read-only visibility | admin views, observability, runtime reads | no mutation/no authority | display/preview/search/export | UI/API tests | operator context | operator, engineering, OMP | `PASS` |
| Production Certification / Maturity | Accept or block production advancement | Production Maturity, CPS, reports | maturity owner only | accept/partial/block/no-change | certification evidence | CPS/OMP continuation | CPS, OMP, operator | `PASS` |
| Knowledge / Canonical Sync | Preserve durable knowledge | Stage 2, canonical docs, AEP | knowledge owner path | sync/hold/no-change | acceptance/lock reports | OMP/future knowledge evolution | canonical owners, AEP | `PASS` |
| Engineering / Report | Record engineering evidence and next action | reports, reviews, State Transition Law | no execution by report alone | pass/hold/explain | reviews/certification | owner consumption/next action | operator, OMP, future phases | `PASS_WITH_MINOR_RISK` |

Minor risk: Engineering / Report surface is real, but can become too broad if treated as one implementation target.

## 9. Relationship With Behaviour

Behaviour Surface is not a replacement for Behaviour.

Correct relationship:

```text
Behaviour Surface
  -> groups related observed Behaviours
  -> exposes shared evidence, owners, consumers, boundaries
  -> helps validation and refinement
```

Incorrect relationship:

```text
Behaviour Surface
  -> owns behaviour truth
  -> creates behaviour
  -> authorizes implementation
  -> replaces Behaviour Definition
```

Behaviour remains the engineering behaviour unit. Surface is a grouping lens only.

## 10. Relationship With Behaviour Instance

Behaviour Instance remains the concrete observed occurrence.

Surface does not execute. Surface does not have instances by itself.

Correct chain:

```text
Behaviour Instance
  -> Behaviour Definition
  -> optional Behaviour Surface grouping
  -> Reality / Coverage / Graph analysis
```

Surface may help answer:

- which owner family is involved;
- which verification family is required;
- which runtime/authority boundary applies;
- which learning path is relevant.

## 11. Relationship With Function Graph

Function Graph is not a Behaviour Surface.

Function Graph can prove surface existence when it shows:

- stable producers;
- stable consumers;
- call/relationship paths;
- read-only or mutation boundaries;
- tests;
- systemd/tool entrypoints;
- closure status.

Function Graph remains an evidence/discovery index.

## 12. Relationship With Reality

Current Autonomous Behaviour Reality may use surface labels as a view or index only.

Surface labels must not:

- create new Reality entries;
- admit hypothesized behaviours;
- hide independent behaviours;
- replace evidence;
- replace validation;
- become architecture.

Valid use:

```text
Observed Behaviour
  -> Evidence
  -> Validation
  -> Behaviour Definition
  -> Surface label for navigation / coverage / graph
```

Invalid use:

```text
Surface label
  -> assumed behaviour
  -> Reality admission
```

## 13. Need For Behaviour Surface

Need verdict:

```text
BEHAVIOUR_SURFACE_NEEDED_AS_ANALYTICAL_GROUPING
```

Not needed as:

- architecture layer;
- owner;
- truth source;
- storage;
- program stage;
- Runtime/Planner concept;
- mandatory canonical entity.

Needed as:

- discovery navigation lens;
- validation grouping;
- coverage/reporting index;
- graph clustering aid;
- way to prevent overly broad Behaviour Definitions from hiding independent decisions/verification/learning paths.

## 14. Needless Complexity Assessment

| Option | Complexity | Value | Verdict |
| --- | --- | --- | --- |
| Add Behaviour Surface as architecture level | `HIGH` | Low; duplicates existing owner/source maps | `REJECT` |
| Add Behaviour Surface as new entity/model | `HIGH` | Low; risks new owner/truth source drift | `REJECT` |
| Use Surface labels inside reports/BDP as optional grouping | `LOW` | High; improves navigation and validation | `ACCEPT_AS_ANALYTICAL_LENS` |
| Ignore surface pattern entirely | `MEDIUM` | Low; loses useful grouping evidence | `REJECT` |

## 15. Independent Certification

| Review | Result | Notes |
| --- | --- | --- |
| Architecture Review | `PASS` | No architecture change proposed; new layer rejected. |
| Reality Review | `PASS` | Observed surfaces are tied to evidence-backed behaviours. |
| Evidence Review | `PASS` | Surface conclusions use implementation, reports, Function Graph, SYSTEM_MAP, runtime/decision/policy evidence. |
| Behaviour Surface Review | `PASS` | Some surfaces are observed engineering surfaces; others are conceptual/rejected. |
| Need Review | `PASS` | Surface is useful as analytical grouping, not architectural entity. |
| Complexity Review | `PASS` | New architecture/entity would be needless complexity. |
| Duplication Review | `PASS` | Surface does not duplicate OMP, Runtime, Function Graph, Knowledge Graph, or owners. |
| Quality Review | `PASS` | Criteria and verdicts are explicit. |
| Self Review | `PASS` | No Discovery execution, no architecture mutation, no forbidden document mutation. |

## 16. Final Answer

Engineering answer:

```text
Behaviour Surface exists in V7 as an observed engineering grouping pattern, but not as a separate architecture level or standalone system entity.
```

Final verdict:

```text
BEHAVIOUR_SURFACE_IS_REAL_AS_ANALYTICAL_ENGINEERING_SURFACE
BEHAVIOUR_SURFACE_IS_NOT_REQUIRED_AS_NEW_ARCHITECTURE_LEVEL
```

Therefore:

- observed surfaces may be used as labels/views in future Behaviour Discovery, Reality Refinement, Coverage, and Graph reports;
- Behaviour Surface must not be added as a new architecture layer, owner, truth source, Runtime concept, Planner concept, or canonical storage system.
