# V7 Decision Model

Status: canonical
Program: V7.WORLD_CLASS_DECISION_MODELS

## Purpose

V7 Decision Model defines how V7 should make, expose, escalate, and learn from decisions.

It is a documentation-only read model over existing V7 owners.
It does not create a planner, governance layer, execution path, truth source, storage path, runtime behavior, apply behavior, floor change, synthetic evidence, or user movement authority.

Need New Owner: FALSE

## Decision Loop

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

Runtime must spend prepared knowledge.
Background systems must build knowledge.

Decision lifecycle, decision freshness, world model ownership, desired-state chain, runtime cost, budget categories, and product evolution review gate are canonicalized in `docs/reference/V7_RUNTIME_MODEL.md` under `Decision Lifecycle And Runtime Foundation`.

Decision Model owns decision semantics.
Runtime Model owns runtime lifecycle and placement semantics.
Decision Model must not redefine packet, lease, runtime freshness, execution budget, or runtime cost requirements as a competing owner.

## Decision Inputs

World-class decision systems separate inputs before producing actions:

1. current state;
2. desired state;
3. policy constraints;
4. health and readiness;
5. evidence quality and freshness;
6. user/service relevance;
7. risk tier and blast radius;
8. execution authority;
9. rollback and verification readiness;
10. outcome history and learning.

V7 already has owners for these inputs through the operator decision surface, knowledge quality model, routing foundation, knowledge-to-decision overlay, governed canary cycle, feedback/learning, trust inventory, truth/convergence, OMP, and Safety-Bounded Authority.

## Decision Vocabulary

V7 keeps the existing action vocabulary from `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`:

| Action | Meaning |
| --- | --- |
| `KEEP` | Current assignment is acceptable; no movement. |
| `MOVE` | Move one or more users to a better eligible channel under governance. |
| `FAILOVER` | Move affected users away from a failing channel. |
| `DRAIN` | Stop new assignments and gradually move users away if safe. |
| `QUARANTINE` | Remove channel from assignment/retention until recovery admission passes. |
| `RECOVER` | Re-admit a channel gradually after sufficient recovery evidence. |
| `PROBE_ONLY` | Collect fresh evidence; no movement. |
| `ASK_OPERATOR` | Human decision required because authority, confidence, policy, or ambiguity blocks autonomy. |
| `NO_ACTION` | No useful or safe action exists now. |

This vocabulary is the decision interface.
Scores, diagnostics, raw health checks, and confidence fields may explain a decision, but they must not become a second decision model.

## Universal Principles

### 1. Reconcile Desired And Current State

Mature control planes do not decide from raw events alone.
They compare current state with desired state and make bounded changes that move reality toward intent.

V7 mapping:
Existing OMP, Kernel, Ideal Routing Model, and governed canary cycle already use event/current state, policy, knowledge gates, packet preview, stop reason, and verification.

Gap classification: `ALREADY_EXISTS`

### 2. Separate Policy Decision From Enforcement

Policy decision must be separable from policy enforcement.
Decision output should be structured enough that runtime can enforce or stop without redoing broad analysis.

V7 mapping:
Existing `operator_decision_surface`, `knowledge_decision_overlay`, policy gates, execution packets, and restore/rollback owners already separate read-only decisions from apply authority.

Gap classification: `ALREADY_EXISTS`

### 3. User-Facing Symptoms Beat Internal Noise

Decision systems should start with user-visible symptoms and service impact before internal causes.
Internal signals explain the decision; they do not override the operator-facing action by themselves.

V7 mapping:
Existing Channel Decision, decision-aligned signal severity, Engineering Principles, and Knowledge Quality Model already reject raw diagnostics as an alternate planner.

Gap classification: `ALREADY_EXISTS`

### 4. Health And Readiness Are Gates, Not Suggestions

Health, freshness, readiness, and recovery state decide whether an action is eligible.
They should block, redirect, or degrade confidence before an unsafe action is exposed.

V7 mapping:
Existing routing foundation, freshness actionability, recovery admission, anti-flap, service/user/SLA fit, and knowledge-to-decision integration already perform read-only gating.

Gap classification: `ALREADY_EXISTS`

### 5. Make Before Break

When changing traffic or assignments, introduce the safe target before removing the old path.
Avoid black holes caused by sequencing gaps or missing target readiness.

V7 mapping:
Existing restore barrier, packet preview, rollback target, recovery admission, anti-flap, and verification plan partially cover this.
The principle should be named explicitly for future routing decisions.

Gap classification: `EXISTS_BUT_UNDERUSED`

### 6. Stage Risk With Blast Radius

World-class systems use canaries, staged rollouts, percentage splits, or small blast-radius actions before broad changes.

V7 mapping:
Existing Safety-Bounded Authority and governed one-user canary model already implement this principle for V7.

Gap classification: `ALREADY_EXISTS`

### 7. Escalation Is A Decision Outcome

Human escalation is not failure.
It is a valid decision when authority, ambiguity, policy, missing evidence, or risk blocks automation.

V7 mapping:
Existing `ASK_OPERATOR`, `AUTHORITY_BOUNDARY`, OMP stop rules, and Kernel stop conditions already encode this.

Gap classification: `ALREADY_EXISTS`

### 8. Preserve Decision State For Handoff

Operational decisions need a live, compact state: what is known, who owns action, what changed, what is blocked, and what must happen next.

V7 mapping:
Existing Current Program State, handoff docs, OMP, governed cycle stop reasons, and decision/outcome learning provide this in pieces.
The decision model should make the handoff requirement explicit for future decision reports.

Gap classification: `EXISTS_BUT_UNDERUSED`

### 9. Learn From Outcomes, Not Opinions

Closed outcomes should update future decision confidence and suitability.
Synthetic evidence and unverified opinions must not improve maturity.

V7 mapping:
Existing decision-to-outcome-to-learning, observed outcome primary trust, feedback contracts, trust evolution, and no-synthetic-evidence rules already cover this.

Gap classification: `ALREADY_EXISTS`

### 10. Keep Runtime Thin

Runtime should consume compact decision artifacts and enforce authority.
Broad research, audits, and long historical recomputation belong in background/read models.

V7 mapping:
Existing Engineering Principles already define background builds knowledge and runtime spends knowledge.

Gap classification: `ALREADY_EXISTS`

# Universal Engineering Laws

These laws are included only when the principle is visible across multiple mature production-system families.
They are engineering laws for V7 research and decision modeling, not vendor architecture copies.

## Law 1: Decision ≠ Execution

- Law: A system must separate choosing an action from executing that action.
- Why it exists: The decision path needs broad context, policy, and evidence; the execution path needs bounded authority, safety, rollback, and verification.
- Which systems use it: Cisco, Juniper, Cloudflare, Kubernetes, Google SRE, Envoy/Istio, OPA-style policy systems, and V7.
- How V7 implements it today: Operator decision surface, knowledge-to-decision overlay, packet preview, restore barrier, OMP authority boundary, and Safety-Bounded Authority keep decisions read-only until explicit execution authority exists.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse existing decision surfaces and execution gates; do not create a planner or execution fork.

## Law 2: Policy Before Action

- Law: Policy constraints must be evaluated before an action is exposed as safe.
- Why it exists: Policy prevents technically possible but unauthorized, noncompliant, or unsafe actions.
- Which systems use it: Cisco and Juniper policy routing/control-plane families, Cloudflare traffic steering policies, Kubernetes admission/scheduling policy patterns, Google SRE incident roles/procedures, Envoy/Istio routing policy, OPA, and V7.
- How V7 implements it today: OMP, policy gates, group/policy constraints, knowledge-to-decision blockers, and execution authority checks run before movement authority.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse existing policy gates and make policy basis explicit in decision read models.

## Law 3: Desired State Before Current Action

- Law: Current action must be judged against desired state, not raw current symptoms alone.
- Why it exists: Reactive local fixes can move the system away from global intent; desired-state reconciliation keeps decisions coherent.
- Which systems use it: Kubernetes controllers, Cisco/Juniper control-plane intent and policy models, Envoy/Istio desired routing config, Cloudflare load-balancing policy, Google SRE incident state, and V7.
- How V7 implements it today: Ideal Routing Model, OMP, governed canary cycle, policy gates, and packet/verification preview compare state, policy, and intended outcome.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Keep extending existing read models to show desired state beside current state.

## Law 4: Runtime Must Stay Thin

- Law: Runtime must consume compact prepared knowledge and enforce authority; it must not perform broad research, audits, or historical recomputation.
- Why it exists: Runtime decisions must be fast, bounded, and reliable under pressure.
- Which systems use it: Kubernetes controllers with cached desired/current objects, Envoy sidecars consuming xDS, Istio pushing routing config, Cloudflare edge routing, Cisco/Juniper control-plane-to-forwarding-plane separation, Google SRE automation principles, and V7.
- How V7 implements it today: Engineering Principles define background builds knowledge and runtime spends knowledge; governed cycle consumes existing read models.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse compact read models and keep new analysis in background/documentation layers.

## Law 5: Background Builds Knowledge

- Law: Heavy evidence collection, comparison, prediction, and learning belong in background systems.
- Why it exists: Decision quality improves through continuous evidence processing without making event-time paths expensive.
- Which systems use it: Google SRE monitoring/postmortem practice, Kubernetes controllers, Cloudflare monitors, Cisco/Juniper telemetry and policy controllers, Envoy/Istio control planes, and V7.
- How V7 implements it today: Intelligence snapshots, trust inventory, knowledge quality read model, routing foundation, prediction, feedback/learning, and reports build knowledge before runtime spends it.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse existing knowledge owners; add only read-only fields when a future task proves a missing decision input.

## Law 6: Safety Before Confidence

- Law: A system must satisfy concrete safety gates before confidence or maturity can authorize action.
- Why it exists: A high-confidence model can still be unsafe if rollback, verification, policy, or blast radius is missing.
- Which systems use it: Google SRE incident response, Kubernetes readiness/admission gates, Cloudflare health gating, Envoy/Istio routing and resilience controls, Cisco/Juniper policy and path checks, and V7.
- How V7 implements it today: Safety-Bounded Authority separates Knowledge Maturity from Execution Authority; `70/70/70` remains a progression floor, while exact actions still require safety gates.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse Safety-Bounded Authority and keep confidence as tier input, not direct apply permission.

## Law 7: Blast Radius Before Scale

- Law: Broad action must be preceded by small blast-radius action, canary, percentage rollout, or staged admission.
- Why it exists: Staging limits harm and produces real evidence before scale.
- Which systems use it: Google SRE launch/incident practices, Istio canary and percentage routing, Cloudflare traffic steering, Kubernetes rollout patterns, Cisco/Juniper controlled policy rollout, and V7.
- How V7 implements it today: Governed one-user canary, risk tiers, packet preview, restore barrier, rollback target, and explicit authority boundary.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse governed canary and risk-tier owners; do not lower floors or bypass authority.

## Law 8: Verify Every Mutation

- Law: Every mutation must have a verification path before it can be considered complete.
- Why it exists: Action without verification is not trustworthy and cannot safely feed learning.
- Which systems use it: Google SRE post-action validation, Kubernetes reconciliation, Cloudflare monitor-based health validation, Envoy/Istio traffic validation, Cisco/Juniper operational verification, and V7.
- How V7 implements it today: Packet preview, verification plan, truth/convergence, service matrix, route/runtime readiness, governed cycle, and outcome closure.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse verification owners and make verification plan mandatory in future decision outputs.

## Law 9: Rollback Before Trust

- Law: A system should not trust a risky mutation unless rollback or recovery path is known first.
- Why it exists: Reversibility turns uncertain production action into bounded learning.
- Which systems use it: Google SRE rollback practice, Istio staged routing, Envoy make-before-break sequencing, Kubernetes rollout/rollback patterns, Cloudflare pool failover, Cisco/Juniper path/policy recovery, and V7.
- How V7 implements it today: Restore barrier, rollback target, anti-flap, recovery admission, governed packet preview, and Safety-Bounded Authority.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse restore/rollback owners and keep rollback target visible in decision output.

## Law 10: Learn Only From Observed Outcomes

- Law: Decision confidence may improve only from observed outcomes, not synthetic evidence or operator wishes.
- Why it exists: Synthetic or unverified evidence creates false maturity and unsafe autonomy.
- Which systems use it: Google SRE postmortems and incident learning, Cloudflare health/event logs, Kubernetes observed state, Envoy/Istio telemetry and traffic outcomes, Cisco/Juniper telemetry-driven policy evaluation, and V7.
- How V7 implements it today: Decision-to-outcome-to-learning, observed outcome primary trust, feedback contracts, trust evolution, and no-synthetic-evidence rules.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse existing feedback and learning owners; require real closed outcomes for maturity growth.

## Law 11: Escalation Is A Valid Decision

- Law: Human escalation is a first-class decision when authority, ambiguity, policy, missing evidence, or risk blocks automation.
- Why it exists: Safe systems must stop clearly instead of guessing under uncertainty.
- Which systems use it: Google SRE incident command, Cisco/Juniper operator-controlled policy changes, Cloudflare operator controls, Kubernetes admission/approval workflows, Envoy/Istio configuration review patterns, and V7.
- How V7 implements it today: `ASK_OPERATOR`, `AUTHORITY_BOUNDARY`, OMP stop rules, Kernel stop conditions, and governed canary approval boundary.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse stop reasons and make escalation reasons explicit in decision output.

## Law 12: Reconciliation Instead Of Reaction

- Law: Mature systems reconcile toward stable intended state instead of reacting blindly to every event.
- Why it exists: Reaction amplifies noise; reconciliation makes state transitions repeatable, explainable, and safe.
- Which systems use it: Kubernetes controllers, Envoy/Istio control-plane updates, Cloudflare load balancing and health-driven steering, Cisco/Juniper control-plane policy systems, Google SRE incident state management, and V7.
- How V7 implements it today: Ideal Routing Model, OMP, Kernel loop, knowledge-gated governed cycle, decision-to-outcome-to-learning, and truth/convergence.
- Gap classification: `ALREADY_EXISTS`
- Reuse path: Reuse existing reconcile/verify/learn loops; keep event-time work bounded.

# Cross-System Comparison Matrix

This matrix is the mandatory comparison shape for future architectural research.
Each row compares production-system families, extracts the common engineering pattern, and maps V7.

| Row | Cisco | Juniper | Cloudflare | Kubernetes | Google SRE | Envoy/Istio | V7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Desired State | Policy and SD-WAN intent define desired routing behavior. | Intent/policy and path-control systems define target network state. | Load balancer and steering policy define target pool/endpoint behavior. | Declarative objects define desired cluster state. | Incident state and reliability objectives define target service state. | xDS/Istio config defines desired proxy and routing state. | Ideal Routing Model, OMP, policy gates, and governed cycle define intended assignment/action state. |
| Policy | Centralized/localized policy controls routing and application-aware behavior. | Routing/security/path policies constrain allowed decisions. | Steering policies and load-balancing rules constrain traffic. | Admission, scheduling, and object policy constrain changes. | Incident procedures and SLO/error-budget practice constrain response. | Virtual services, destination rules, and xDS config constrain routing. | OMP, group/policy gates, knowledge blockers, and authority boundaries constrain decisions. |
| Eligibility | Paths, applications, SLA, and policy determine eligible routes. | Path, topology, and policy determine eligible forwarding choices. | Healthy pools/endpoints and steering rules determine eligibility. | Schedulers/controllers evaluate eligible objects/nodes. | Incident roles and service impact determine eligible actions. | Route destinations, clusters, endpoints, subsets, and health determine eligibility. | Planner eligibility, service/user/SLA fit, recovery admission, anti-flap, and freshness actionability determine eligibility. |
| Health | Telemetry and app-aware routing health influence path choice. | Telemetry/path health influences route or failover decisions. | Monitors evaluate endpoint and pool health. | Readiness/liveness/object status informs reconciliation. | Monitoring distinguishes symptoms and causes. | Endpoint health, retries, circuit breakers, and route readiness influence traffic. | Service matrix, route/runtime readiness, freshness, recovery state, and knowledge quality gate decisions. |
| Safety | Policy, path constraints, and staged operational changes limit unsafe routing. | Policy, path constraints, and operator controls limit unsafe changes. | Pool failover and traffic steering avoid unhealthy endpoints. | Controllers/admission enforce safe transitions. | Incident command prioritizes stopping harm and preserving evidence. | Resilience controls, make-before-break sequencing, and staged routing reduce traffic loss. | Safety-Bounded Authority, restore barrier, rollback target, verification, and blast-radius gates limit action. |
| Blast Radius | Policy rollout can be scoped by site, application, or path. | Network changes can be scoped by topology, policy, or segment. | Traffic can be shifted by pool, endpoint, geography, or steering policy. | Rollouts can be staged by workload/object scope. | Incident practice prioritizes containment and limited operational change. | Canary and percentage routing stage traffic. | Governed one-user canary and risk tiers bound action before scale. |
| Rollback | Operators can revert policy/path changes. | Operators can revert config/policy/path choices. | Pools and steering can fail back or route around unhealthy origins. | Rollout history and reconciliation support returning toward prior desired state. | Rollback is a normal incident mitigation action. | Route/config changes can be reversed; make-before-break reduces rollback need. | Restore barrier, rollback target, packet preview, and anti-flap define reversible action. |
| Verification | Operational telemetry confirms policy/path effect. | Telemetry and operational checks confirm path/config effect. | Monitors and event logs validate endpoint health and steering effect. | Controllers observe status and reconcile until desired state is reached. | Post-action validation and postmortems verify impact and learning. | Proxy stats, xDS ACK/NACK, health, and traffic behavior validate config. | Truth/convergence, service matrix, verification plan, route/runtime readiness, and outcome closure verify decisions. |
| Learning | Telemetry and operational review inform future policy. | Telemetry and operational review inform future path/policy choices. | Health/event data informs future steering and failover decisions. | Observed status informs future reconciliation. | Postmortems and incident reviews create learning and prevention. | Traffic outcomes and telemetry inform future routing/config changes. | Decision-to-outcome-to-learning, trust evolution, feedback contracts, and observed outcome primary trust learn from real outcomes. |
| Runtime | Forwarding/runtime consumes prepared policy and state. | Forwarding/runtime consumes prepared policy and path state. | Edge routing consumes load-balancer policy and health state. | Controllers act from watched objects and cached state. | Incident execution uses prepared roles/procedures under pressure. | Proxies consume xDS/Istio config and act quickly. | Runtime spends compact knowledge through packet/preview/authority gates and must stay thin. |
| Background Knowledge | Controllers/management systems process telemetry and policy. | Controllers/management systems compute topology, telemetry, and policy. | Monitors and analytics build health and traffic knowledge. | Control plane stores objects/status and controllers reconcile. | Monitoring, postmortems, and reviews build operational knowledge. | Control plane computes/distributes config; telemetry builds knowledge. | Intelligence snapshots, trust inventory, knowledge quality, routing foundation, prediction, and reports build knowledge. |
| Decision Output | Policy/path decision or route steering outcome. | Policy/path decision or route steering outcome. | Pool/endpoint steering decision. | Object update, scheduling choice, or reconciliation action. | Incident action, escalation, rollback, or follow-up item. | Route/cluster/listener/endpoint config or traffic rule outcome. | `KEEP`, `MOVE`, `FAILOVER`, `DRAIN`, `QUARANTINE`, `RECOVER`, `PROBE_ONLY`, `ASK_OPERATOR`, or `NO_ACTION`. |
| Operator Escalation | Operator approval/configuration remains required for bounded changes. | Operator approval/configuration remains required for bounded changes. | Operators configure policies, monitors, and overrides. | Operators approve/apply certain policy/config changes. | Incident command escalates ownership and decisions explicitly. | Operators review/apply traffic policy and config. | `ASK_OPERATOR`, `AUTHORITY_BOUNDARY`, Kernel stop rules, and OMP approval boundaries are valid decision outcomes. |

## Matrix Row Analysis

| Row | Common engineering pattern | Where V7 already matches | Where V7 differs |
| --- | --- | --- | --- |
| Desired State | Define target intent before selecting action. | Ideal Routing Model, OMP, policy gates, governed cycle. | V7 should expose desired state more explicitly in future decision outputs. |
| Policy | Policy constrains technically possible actions. | OMP, group/policy gates, knowledge blockers. | Policy basis can be more visible in read-only decision output. |
| Eligibility | Eligible targets are filtered before action selection. | Planner eligibility, service/user/SLA fit, recovery admission, anti-flap. | Existing eligibility is spread across several read models. |
| Health | Health determines whether a target can receive traffic/action. | Service matrix, freshness, route/runtime readiness. | Health is strong but should remain decision-aligned, not raw diagnostics-as-decision. |
| Safety | Safety gates must pass before confidence or action. | Safety-Bounded Authority, restore barrier, verification, rollback. | No architecture gap; keep safety visible in every decision output. |
| Blast Radius | Start small before scaling. | Governed one-user canary and risk tiers. | Scaling beyond one-user canary remains authority/evidence-bound. |
| Rollback | Reversibility is required before trust grows. | Restore barrier, rollback target, anti-flap. | Rollback fields should be mandatory in future decision summaries. |
| Verification | Mutations are incomplete until verified. | Truth/convergence, service matrix, route/runtime readiness, outcome closure. | No architecture gap; keep verification plan attached to decisions. |
| Learning | Only observed outcomes improve future decisions. | Feedback contracts, decision-to-outcome-to-learning, trust evolution. | Current real outcome volume remains a reality limit, not architecture gap. |
| Runtime | Runtime consumes prepared state and stays bounded. | Engineering Principles and governed cycle. | No architecture gap; future implementation must avoid broad runtime reasoning. |
| Background Knowledge | Heavy analysis belongs outside runtime. | Intelligence snapshots, trust inventory, knowledge quality, reports. | Background read models should be selected by Context Resolver, not loaded wholesale. |
| Decision Output | Decisions should be structured, inspectable, and actionable. | Action vocabulary and decision output shape exist. | Some existing surfaces may need read-only field extensions later. |
| Operator Escalation | Escalation is a safe stop state, not failure. | `ASK_OPERATOR`, `AUTHORITY_BOUNDARY`, OMP stop rules. | No architecture gap; future UIs/reports should explain escalation reason clearly. |

## V7 Decision Contract

Every future V7 decision surface should answer:

1. What decision is being made?
2. What current state triggered it?
3. What desired state or policy is being applied?
4. What evidence is fresh enough to use?
5. What evidence is missing or stale?
6. What action vocabulary value is produced?
7. What gates blocked, redirected, or allowed the decision?
8. What authority tier is required?
9. What rollback and verification path exists?
10. What outcome will prove the decision right or wrong?
11. Where will learning be recorded?

## Decision Output Shape

```text
decision_id
  action
  subject
  current_state
  desired_state
  policy_basis
  evidence_basis
  blockers
  risk_tier
  blast_radius
  authority_required
  packet_preview
  rollback_target
  verification_plan
  stop_reason
  outcome_closure_plan
  learning_path
```

This is a read-model shape.
It does not require new runtime fields until a future implementation proves an existing surface cannot expose the needed value.

## Reuse Analysis

Existing owners are sufficient:

- `admin_core/operator_decision_surface.py`
- `admin_core/autonomy_trust_acceleration.py`
- `admin_core/operator_execution_pipeline.py`
- `admin_core/operator_execution_feedback.py`
- `admin_core/intelligence_workers.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tools/v7-governed-canary-dry-run-cycle`
- `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`
- `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`
- `docs/reference/V7_ENGINEERING_PRINCIPLES.md`
- OMP and Kernel stop/authority rules

No new runtime owner is required.
No new planner is required.
No new governance model is required.
No new execution path is required.
No new truth source is required.

## Extension Path

Future work should extend existing owners only when a concrete implementation task proves a missing field or disconnected read model.

Allowed extension types:

- add read-only fields to existing decision surfaces;
- add decision output summaries to existing reports;
- add documentation explaining stop reasons;
- connect real outcome fields to existing learning paths;
- expose existing authority gates more clearly.

Forbidden extension types unless a future ADR proves `FUNDAMENTAL_ARCHITECTURE_GAP`:

- new planner;
- new governance;
- new execution engine;
- new truth source;
- new synthetic evidence collector;
- new runtime apply authority;
- new user movement path.

## Source Basis

This model was derived from primary documentation and mature production systems:

- Kubernetes controller pattern: https://kubernetes.io/docs/concepts/architecture/controller/
- OPA policy decision/enforcement separation: https://www.openpolicyagent.org/docs
- Google SRE monitoring and incident management: https://sre.google/sre-book/monitoring-distributed-systems/ and https://sre.google/sre-book/managing-incidents/
- Google SRE postmortem learning: https://sre.google/sre-book/postmortem-culture/
- Envoy xDS dynamic resources and eventual consistency: https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol
- Istio traffic management and staged routing: https://istio.io/latest/docs/concepts/traffic-management/
- Cloudflare Load Balancing traffic steering and monitors: https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/ and https://developers.cloudflare.com/load-balancing/monitors/
- Cisco Catalyst SD-WAN policy guide: https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/policies/ios-xe-17/policies-book-xe.html

Research never copies vendor architecture.
It extracts shared engineering principles and maps them to existing V7 owners.

## Runtime Capability Maturation Decision Semantics

Status: `CANONICAL_REFERENCE_ONLY`.

RT2 decision semantics are owned here only as vocabulary and meaning.
OMP owns RT2 execution.
Runtime Model owns runtime consumption and live safety.

Definitions:

| Term | Meaning | Owner |
| --- | --- | --- |
| Current State | The observed and prepared present-tense system state. | Observation, World Model, read-model owners. |
| Desired Safe State | The policy/business/safety target state V7 wants reality to approach. | Product Specification, policies, OMP, Decision Model. |
| Delta | The bounded difference worth considering between current state and Desired Safe State. | Existing planner/autoswitch and decision surface owners. |
| Prepared Plan | Advisory candidate/action artifact produced before live execution. | Planner, decision surface, packet/preview owners. |
| Decision Lifetime | The period in which a decision's material assumptions remain valid. | Runtime Model freshness/lifecycle owners. |
| Runtime Eligibility | Whether Runtime may continue to execute-or-stop evaluation. | A6/runtime eligibility owners. |
| Execution Eligibility | Whether the exact bounded action may execute after live gates. | Runtime Model, execution owners, OMP authority owners. |

Canonical RT2 decision flow:

```text
Current State
  -> Desired Safe State
  -> Delta
  -> Prepared Plan
  -> Runtime Eligibility
  -> Execution Eligibility
  -> Execution
```

Rules:

1. Desired State is intent, not authority.
2. Desired State must not become a second planner.
3. Desired State must not become a second authority owner.
4. Prepared Plan is advisory until live authority, freshness, blast radius, rollback, verification, anti-flap, and runtime eligibility pass.
5. Decision remains separate from execution.
6. Runtime may consume decisions but must not invent them.
7. External models may inform decision semantics only after Research Framework and V7 Fit Analysis.
8. Delta ranking may order advisory candidates, but cannot select execution without existing planner and authority owners.
9. Prepared Plan cannot create a packet, lease, restore barrier, apply, rollback, or feedback record by itself.

RT2-S3 may mature Desired-State Delta Preparedness only through existing owners.
If a proposed delta requires a new planner, new authority model, or new runtime decision path, OMP must stop at `FUNDAMENTAL_ARCHITECTURE_GAP` unless reuse is proven impossible.
