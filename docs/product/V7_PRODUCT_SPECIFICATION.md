# V7 Product Specification 1.0

Status: canonical product specification
Product: V7 Vozduh
Version: 1.0

This document defines what V7 is.

It is the product source above architecture, OMP, Runtime, research, reports, implementation, and future Codex or ChatGPT work.

It has two layers:

1. Product: plain language for product owners, operators, engineers, investors, and future sessions.
2. Technical Appendix: full technical meaning for engineers.

# Layer 1: Product

## One Sentence

V7 keeps users online by automatically finding, proving, and learning the safest working route for their internet access.

## Product Mission

V7 exists because ordinary VPN operation is too manual for real production reliability.

A normal VPN panel can show servers.
A dashboard can show health.
A script can move users.
A human operator can react to problems.

But none of those is enough when many users, services, channels, providers, countries, and policies are changing at the same time.

V7 solves the product problem:

```text
Keep users connected,
choose safe routes,
avoid unnecessary movement,
recover from failure,
and learn from what actually happened.
```

Without V7:

- users can lose access when a channel or service degrades;
- operators must manually detect problems;
- operators must guess who is affected;
- routing decisions can be late, broad, or based on stale evidence;
- rollback can be unclear;
- every incident can become a manual investigation;
- the system does not reliably learn from real outcomes.

V7 is built so that connectivity becomes a managed product outcome, not a repeated manual rescue.

## Business Objectives

Business Objectives are the canonical top-level interface between the Product Owner and V7.

Permanent product chain:

```text
Product Owner
  -> Business Objectives
  -> Policy Translation
  -> Canonical Policies
  -> OMP
  -> Runtime
  -> Users
```

The Product Owner communicates only through Business Objectives.

The Product Owner must never be required to configure or understand:

- packets;
- routing algorithms;
- action classes;
- blast radius internals;
- rollback internals;
- runtime gates;
- planner logic;
- protocol engineering.

Business Objectives are product language.
They describe what the product should achieve for users and the business.

Policies translate Business Objectives into operational rules.
OMP turns those rules into maturity, backlog, certification, and authority decisions.
Runtime executes certified decisions inside approved policy or stops safely.

### Policy Translation

Policy Translation does not create a new owner.

Canonical Policies already perform the translation from product language into engineering rules:

```text
Business Objectives
  -> Canonical Policies
  -> Operational Rules
  -> Runtime
```

Examples:

```text
Maximum Stability
  -> Movement Protection
  -> Stickiness
  -> Cooldown
  -> Anti-Flap
  -> Recovery Admission
  -> State Change Cost
  -> Runtime

Fastest Recovery
  -> Hard Failure
  -> Rollback
  -> Freshness
  -> Runtime Eligibility
  -> Runtime

Lowest User Disruption
  -> Movement Protection
  -> Minimum Improvement Threshold
  -> Blast Radius
  -> Verification
  -> Runtime
```

### Operator Language

Operator-facing language must use Business Objectives as the primary operating language.

Good operator language:

- Maximum Stability;
- Fast Recovery;
- Lowest User Disruption;
- Business Risk;
- Operator Workload;
- Service Availability;
- Invisible VPN Experience.

Bad primary operator language:

- Packet;
- Lease;
- Planner;
- Selected Move Hash;
- Rollback Manifest;
- Blast Radius Generation.

Engineering details may remain available for audit and debugging, but they must not be the first product language shown to operators.

### OMP Integration

OMP must always be able to map:

```text
Current Business Objectives
  -> Affected Policies
  -> Affected Capabilities
  -> Backlog Items
  -> Current Progress
  -> Production Maturity
```

This does not make OMP the owner of Business Objectives.
OMP consumes Business Objectives through Product Specification, Canonical Policies, the Implementation Backlog, and Current Program State.

### Initial Business Objectives

#### Maximum Stability

Purpose:
Keep users on stable working routes and prevent chaotic movement.

Success criteria:
Users do not oscillate between channels, temporary noise does not cause movement, and current state is preserved when staying is better than switching.

User value:
The user experiences steady internet access without route churn.

Policy Translation owner:
Canonical Policies for Anti-Flap, Recovery Admission, Freshness, Blast Radius, and Movement Protection knowledge in OMP / Canonical Reference.

Runtime interpretation:
Runtime may move only when the certified decision proves that `NET_BENEFIT > CHANGE_COST`; otherwise it keeps current state or stops safely.

Related capabilities:
Movement Protection, Runtime Eligibility, Recovery Admission, Observability.

Related backlog:
`A3`, `A5`, `A6`, `B3`, `B4`, `B8`, `B10`, `B19`, `B20`, `B21`, `C7`.

Completion criteria:
Movement Protection is complete and locked; anti-flap, recovery admission, freshness, state-change cost, routing mode, slow-start, and pool-health semantics are certified by real evidence.

#### Fastest Recovery

Purpose:
Restore user connectivity quickly when a route, channel, service, or target fails.

Success criteria:
Confirmed hard failures lead to bounded recovery action without waiting for manual investigation, and failed actions are verified and rolled back when needed.

User value:
Failures are short and recovery feels automatic.

Policy Translation owner:
Hard Failure, Rollback, Freshness, Recovery Admission, and Runtime Eligibility policies.

Runtime interpretation:
Runtime executes certified recovery actions only inside approved authority, with fresh evidence, rollback/no-rollback readiness, and verification.

Related capabilities:
Runtime Eligibility, Rollback, Recovery Admission, Learning, Production Autonomy.

Related backlog:
`A3`, `A4`, `A6`, `B8`, `B9`, `B10`, `B15`, `B16`, `B17`, `B18`, `C1`, `C5`, `C6`.

Completion criteria:
Hard-failure recovery, rollback/no-rollback classification, freshness, verification, and learning are certified for the relevant action classes.

#### Lowest User Disruption

Purpose:
Avoid unnecessary user movement and make required movement minimally disruptive.

Success criteria:
V7 does not move users for tiny score differences, unstable evidence, unclear benefit, or unproven targets.

User value:
The user stays connected and notices as little routing change as possible.

Policy Translation owner:
Movement Protection, Blast Radius, Verification, Anti-Flap, and State Change Cost owners.

Runtime interpretation:
Runtime requires a justified movement with measurable expected benefit greater than movement cost and bounded user impact.

Related capabilities:
Movement Protection, Rollback, Runtime Eligibility, Decision Explainability.

Related backlog:
`A3`, `A5`, `A6`, `B1`, `B4`, `B5`, `B13`, `B14`, `B19`, `B20`, `B21`, `C2`, `C7`.

Completion criteria:
Every movement has a clear reason, bounded impact, verification, rollback/no-rollback path, and user-impact explanation.

#### Highest Service Availability

Purpose:
Keep important services reachable for users, not merely keep channels technically alive.

Success criteria:
Telegram, YouTube, ChatGPT, browsing, and other important services remain reachable according to service/user/SLA fit.

User value:
Users can use the services they care about without thinking about channels or VPN routes.

Policy Translation owner:
Soft Degradation, Hard Failure, Freshness, Service/User/SLA Fit, and Recovery Admission owners.

Runtime interpretation:
Runtime treats service fit and service degradation as eligibility inputs for execute-or-stop decisions.

Related capabilities:
Knowledge System, Runtime Eligibility, Observability, Production Readiness.

Related backlog:
`B2`, `B3`, `B4`, `B5`, `B6`, `B7`, `B8`, `B9`, `B13`, `B17`, `C2`.

Completion criteria:
Service/user/SLA fit is policy-bound, observable, fresh enough for action, and validated by real outcomes.

#### Lowest Business Risk

Purpose:
Prevent a technical action from creating unacceptable product, operational, or authority risk.

Success criteria:
No action exceeds approved authority, blast radius, policy, freshness, rollback, verification, or safety boundaries.

User value:
V7 protects access without creating broad outages or unsafe surprises.

Policy Translation owner:
Authority, Blast Radius, Rollback, Freshness, Anti-Flap, and Delegated Autonomy Policy owners.

Runtime interpretation:
Runtime stops before mutation when risk exceeds approved policy or certified scope.

Related capabilities:
Authority Evolution, Rollback, Runtime Eligibility, Production Autonomy.

Related backlog:
`A3`, `A5`, `A6`, `B11`, `B12`, `B14`, `B15`, `B16`, `B17`, `B18`, `C3`, `C4`, `C5`, `C6`.

Completion criteria:
Authority expansion, blast radius, rollback/no-rollback, freshness, anti-flap, and runtime eligibility are certified and auditable.

#### SLA Priorities

Purpose:
Let product priorities express which users, services, cohorts, or contexts matter most.

Success criteria:
V7 can explain and apply service/user/SLA fit without requiring the Product Owner to understand route internals.

User value:
High-priority services and user groups receive routing decisions aligned with their expected experience.

Policy Translation owner:
Service/User/SLA Fit, Soft Degradation, Scale Evolution, and policy owners.

Runtime interpretation:
Runtime consumes SLA/service/user fit as a policy input, not as raw business text.

Related capabilities:
Knowledge System, Observability, Runtime Eligibility, Production Readiness.

Related backlog:
`B2`, `B3`, `B4`, `B7`, `B11`, `B13`, `B17`, `C2`.

Completion criteria:
SLA/service/user fit is readable, policy-bound, fresh, and usable for runtime eligibility and operator explanations.

#### Business Risk Appetite

Purpose:
Define how much operational risk V7 may take for recovery, stability, cost, and autonomy.

Success criteria:
Authority, blast radius, rollback, freshness tolerance, and automation tier match approved business risk appetite.

User value:
Automation becomes safer because V7 does not silently exceed business tolerance.

Policy Translation owner:
Authority, Blast Radius, Delegated Autonomy Policy, Action-Class Promotion, and Production Maturity owners.

Runtime interpretation:
Runtime executes only within the approved risk envelope and stops outside it.

Related capabilities:
Authority Evolution, Production Autonomy, Runtime Eligibility, Production Readiness.

Related backlog:
`A4`, `A5`, `A6`, `B11`, `B12`, `B13`, `B14`, `B16`, `C3`, `C4`, `C6`.

Completion criteria:
Delegated Autonomy Policy and action-class authority are approved and certified for bounded production operation.

#### Minimal Operator Work

Purpose:
Reduce repeated manual investigation and repetitive approval work.

Success criteria:
The operator sees clear decisions, exceptions, and authority questions instead of raw packet, route, score, and rollback details.

User value:
The product improves faster because operator attention is spent on real exceptions and policy boundaries.

Policy Translation owner:
OMP, Decision Explainability, Action-Class Promotion, Delegated Autonomy Policy, and Observability owners.

Runtime interpretation:
Runtime handles certified routine work inside policy; OMP escalates only policy, authority, safety, or evidence boundaries.

Related capabilities:
Decision Explainability, Authority Evolution, Observability, Production Autonomy, Implementation Discipline.

Related backlog:
`A3`, `A4`, `A6`, `B1`, `B4`, `B12`, `B13`, `B17`, `C2`, `C4`.

Completion criteria:
Packet approval is retired for certified classes, explanations are operator-readable, and routine certified decisions no longer require per-action approval.

#### Invisible VPN Experience

Purpose:
Make VPN routing disappear from the user's daily experience.

Success criteria:
Users use Telegram, YouTube, ChatGPT, browsing, and other services without thinking about VPN channels, routes, recovery, rollback, or failover.

User value:
The product feels like reliable internet access, not a technical VPN tool.

Policy Translation owner:
Product Specification, Canonical Policies, OMP, Runtime Model, Service/User/SLA Fit, Movement Protection.

Runtime interpretation:
Runtime preserves or restores service reachability using certified policy-bound actions and stops safely when it cannot prove safety.

Related capabilities:
Movement Protection, Runtime Eligibility, Recovery Admission, Learning, Production Autonomy, Production Readiness.

Related backlog:
`A3`, `A4`, `A5`, `A6`, `B2`, `B3`, `B4`, `B5`, `B7`, `B8`, `B10`, `B12`, `B13`, `B16`, `B17`, `C2`, `C4`, `C7`.

Completion criteria:
Production Autonomy is certified: routine routing work is invisible to users, bounded by policy, verified, reversible where required, and learned from real outcomes.

## The Ideal User Experience

A user wakes up and opens Telegram.
It works.

The user opens YouTube.
It works.

The user opens ChatGPT.
It works.

The user browses the web.
It works.

The user does not think about VPN routes, channels, providers, countries, servers, policy, failover, restore barriers, or rollback.

In the background, V7 is watching the real network.
It notices which paths are healthy, which services work, which users are affected, and which channels are becoming unsafe.

If the current path is still good, V7 keeps the user where they are.
If evidence says a path is failing, V7 looks for a safer target.
If the move is not safe enough, V7 stops and asks the operator.
If the move is authorized, V7 changes only the bounded target, verifies that it worked, rolls back if needed, and records the outcome.

The ideal experience is simple:

```text
The user stays online.
The operator sees only real decisions.
The system gets smarter.
```

## Product Principles

These are the rules that define the product.

### Reality First

V7 trusts what really happened.
It does not pretend, guess, or manufacture confidence.

### User Connectivity First

The user staying online matters more than internal scores.
Diagnostics are useful only when they help preserve or explain access.

### Minimal Operator Work

The operator should not manually inspect every route, probe, score, packet, and rollback path.
V7 prepares the decision and asks for authority only when needed.

### Safety Before Movement

Moving a user is not success by itself.
Stopping safely is better than moving unsafely.

### Learning From Reality

V7 improves from verified outcomes, not from opinions or synthetic evidence.

### Event-Driven Operation

V7 responds to meaningful events and state changes.
It does not move users just because a timer fired.

### Reuse Before Rewrite

V7 grows by improving existing owners.
It avoids duplicate planners, duplicate execution, duplicate governance, and duplicate truth.

### Simple Authority

Trust and authority are different.
Trust says how autonomous V7 may become.
Authority says which certified kind of action V7 may perform.

The durable approval object is an Action Class.
An Action Class is a repeated product capability, such as single-user failover, channel hard-fail failover, service-specific failover, rollback, verification, or learning refresh.

Packets are not the long-term approval object.
A packet is a fresh runtime execution artifact for one moment in reality.
It must match an approved Action Class, policy, safety, freshness, rollback, verification, and blast-radius boundary.

### Explainability

V7 must explain the problem, recommendation, reason, risk, rollback, and approval state.

### Reversibility

Risky action needs rollback or recovery before it can be trusted.

### Verification Before Trust

An action that was not verified cannot increase trust.

### Background Knowledge, Thin Runtime

Heavy thinking happens before runtime.
Runtime uses prepared knowledge and either acts safely or stops.

### No Duplicated Systems

V7 must stay one coherent product, not competing tools with competing truths.

### World Consensus Before Policy

Operational behavior must not come from personal opinion.
Before V7 turns a behavior into policy, it must discover how mature production systems solve the same problem, compare consensus and disagreement, audit V7 reality, reuse existing V7 owners, verify, certify, and only then integrate the policy into OMP.

The Canonical Policy Library is:

```text
docs/policies/
```

Policies start as research-required shells.
Stage 1 world research, Stage 1.5 normalization, Stage 2 industry consensus, Stage 2.5 interaction audit, and Stage 3 reality audit are complete for the initial policy library; V7 fit analysis is the next stage.
Policies become operational only after world research, V7 fit analysis, implementation, verification, certification, and OMP integration.

## What V7 Actually Does

V7 constantly does six product things.

### Observes

V7 watches what is happening now:

- which users are connected;
- which channels exist;
- which services work;
- which routes are healthy;
- which paths are full, failing, stale, or recovering.

### Understands

V7 turns raw facts into useful meaning.

It does not treat every log line or score as a decision.
It asks what the fact means for user connectivity.

### Predicts

V7 estimates which path is likely to work next.

Prediction is not authority.
It is one input into a safe decision.

### Chooses

V7 chooses a product action:

- keep the user where they are;
- move the user;
- fail over;
- drain a bad channel;
- quarantine a bad channel;
- recover a channel gradually;
- probe only;
- ask the operator;
- do nothing when no safe action exists.

### Verifies

V7 checks whether an action actually worked.

If an action cannot be verified, it is not treated as success.

### Learns

V7 learns only from observed outcomes.

Real success, failed verification, rollback, no-rollback, operator rejection with context, and real network behavior can improve future decisions.
Synthetic evidence cannot.

## What Success Looks Like

Success is not a dashboard score.
Success is not trust reaching a number.
Success is not prediction confidence by itself.

V7 succeeds when:

- users stay online;
- Telegram, YouTube, ChatGPT, browsing, and other important services remain reachable;
- switches are invisible or minimally disruptive;
- failures recover;
- wrong moves are rare;
- unsafe moves are blocked;
- rollback is available when needed;
- the operator sees clear approve/reject decisions instead of raw investigation work;
- operator workload shrinks;
- the system becomes smarter from real use;
- scale increases without multiplying operator effort.

The product outcome is:

```text
stable access
  + safe routing
  + verified learning
  + lower operator burden
```

The product does not become better because it grows.
The product becomes better because it continuously converts real operational experience into better future decisions.

## The Final Product

After years of evolution, V7 is a global autonomous connectivity control plane.

It supports:

- `100+` channels;
- `10000+` users;
- many providers;
- many countries;
- many servers;
- many service profiles;
- many user groups;
- many policies;
- different SLA classes.

At that scale, the operator does not inspect raw rows.
V7 groups reality into product decisions:

- who is affected;
- which service is degraded;
- which route is unsafe;
- which channel is recovering;
- which users or cohorts need action;
- which target is safe;
- which action is allowed;
- which action needs authority;
- what happened after the action.

The final product behaves like this:

```text
observe reality
  -> understand impact
  -> choose safe action
  -> act only with authority
  -> verify
  -> rollback if needed
  -> learn
  -> improve future decisions
```

The operator supervises.
Runtime executes certified decisions inside approved authority.
Runtime does not invent decisions.
It consumes prepared knowledge and either executes the certified action or stops safely.
Users experience working internet.

## Product Scale Model

V7 is a large-scale production control plane.

The product is designed for at least:

- `10,000+` active users;
- `100+` active and routable channels;
- millions of runtime decisions;
- long-lived telemetry, evidence, reports, and learning history.

V7 must optimize for target production scale, not only current deployment size.

Every durable product, architecture, runtime, learning, reporting, storage, and UI decision must remain efficient, maintainable, and operationally safe at target production scale.

The model requires:

- runtime path must remain thin;
- heavy computation must move to background, read-model, aggregation, index, or offline layers;
- persistent data must have clear lookup and retention strategy;
- normal UI/API paths must consume summaries and read models, not raw historical scans;
- reports must stay compact and must not duplicate large raw evidence;
- evidence and learning must prefer representative action-class confidence over non-scalable full enumeration when safety is preserved;
- bounded cost growth is preferred over cost growth proportional to users, channels, or time;
- any linear growth with users, channels, or time must be explicitly justified.

Mandatory product question:

```text
Will this remain efficient, maintainable, and operationally safe at 10,000+ users and 100+ channels?
```

### Product Scale Objectives

These objectives are the long-term optimization target for OMP.

1. Runtime Cost
   The cost of processing one bounded runtime decision should remain approximately constant as the system grows.
   Runtime complexity must not scale directly with total users whenever practical.

2. Memory
   Memory usage should grow in a controlled and bounded way.
   V7 should avoid designs that require large in-memory global state.

3. Storage
   Persistent storage growth must be predictable.
   Raw evidence should be retained once.
   Derived summaries, indexes, and read models should be preferred over durable duplication.

4. CPU
   Heavy computation belongs to background processing, aggregation, and offline analysis.
   Runtime should consume prepared knowledge.

5. Read Models
   Operator and API paths should read summarized views by default.
   Large historical scans must not be part of normal runtime or UI paths.

6. Learning
   Learning should become incremental.
   V7 should avoid full recomputation whenever equivalent incremental updates are possible.

7. Reporting
   Reports are historical evidence only.
   Reports must stay compact.
   Canonical owners store durable knowledge.

8. Scaling
   The system should evolve toward bounded cost growth rather than cost proportional to:

   - users;
   - channels;
   - history size;
   - telemetry size.

9. Architecture
   Architecture should evolve toward scale-independent operation wherever practical.
   Representative evidence is preferred over exhaustive enumeration when safety is preserved.

10. Product Goal
    Increasing deployment size should have minimal impact on the cost, latency, and operational complexity of processing one bounded runtime decision.

## What V7 Is Not

V7 is not a VPN panel.

It may show VPN-related state, but the product is not the panel.

V7 is not a dashboard.

It may show health and decisions, but dashboards do not keep users online by themselves.

V7 is not a manual router.

The product goal is to reduce manual routing work, not organize it better forever.

V7 is not a script collection.

Tools exist, but the product is the controlled outcome loop.

V7 is not a static load balancer.

It learns from real outcomes and adapts to users, services, policies, and changing network reality.

V7 is not only a monitoring system.

Monitoring observes.
V7 observes, chooses, verifies, rolls back, learns, and improves.

V7 is not a hardcoded switch engine, blind timer, planner playground, synthetic evidence machine, or duplicate set of planners and truth sources.

## Product Evolution

V7 grows continuously.

It does not evolve by rewriting the whole system every time a new problem appears.
It evolves by learning what really happened and improving existing product owners.

This matters because routing reliability is not static.
Providers change.
Services change.
Countries change.
Users change.
Failures repeat in new shapes.
Evidence gets old.
Good paths become bad.
Bad paths recover.

V7 must therefore evolve through:

- real outcomes;
- safer authority;
- better knowledge;
- clearer operator decisions;
- stronger rollback;
- better scale behavior;
- simpler operation.

The product does not chase novelty.
It compounds operational knowledge.

## Why V7 Gets Better Forever

V7 is designed to improve continuously.

It does not get better because developers constantly rewrite it.
It gets better because every real operational event may become new verified knowledge.

Examples:

- successful routing;
- failed routing;
- rollback;
- verification;
- service degradation;
- channel recovery;
- operator approval;
- operator rejection;
- real user impact.

These events become:

```text
Knowledge
  -> Better Decisions
  -> Better Product
```

Canonical learning loop:

```text
Reality
  -> Knowledge
  -> Decision
  -> Outcome
  -> Learning
  -> Better Product
  -> More Reality
```

The product compounds operational experience.
This is the primary long-term competitive advantage of V7.

## Autonomy Promotion Engine

V7 must not ask the operator to approve the same kind of safe action forever.

Packet approval was useful as the first governed proof step.
It is not the correct long-term product abstraction.

Packets become stale because reality changes faster than human review:

```text
Reality
  -> Packet
  -> Operator
  -> Packet becomes stale
  -> Packet regenerated
  -> Operator repeats approval
```

That loop does not scale to `100+` channels, `10000+` users, many providers, many services, and continuous network change.

The primary approval object is therefore:

```text
Action Class
```

The packet becomes:

```text
fresh runtime execution artifact
```

The operator approves durable capabilities:

```text
Approve Action Class
  -> Approve Authority Expansion
  -> Approve Product Policy
  -> Operator Supervision Only
```

Packet-level approval remains only as a temporary governed fallback for classes that are still `GOVERNED_ONLY`.
It is not the future operating model.

This is the job of the Autonomy Promotion Engine.

The engine does not approve runtime execution.
It does not move users.
It does not enable runtime apply by itself.

It decides whether an action class has enough real evidence to be promoted.

An action class is a repeated kind of product action, such as:

- single-user failover;
- two-user failover;
- small batch movement;
- channel hard failure;
- channel degradation;
- recovery admission;
- service failover;
- rollback;
- packet generation;
- verification;
- outcome closure;
- learning refresh.

Promotion is based only on real operational experience:

- real outcomes;
- verification;
- rollback quality;
- safety;
- blast radius;
- learning;
- trust;
- authority policy.

Reports can explain evidence.
Reports alone cannot promote a class.
Synthetic evidence cannot promote a class.

The promotion loop is:

```text
Observe
  -> Collect Outcomes
  -> Verify
  -> Measure
  -> Evaluate
  -> Recommend Promotion
  -> Operator approves CLASS
  -> Runtime capability updated
  -> Runtime generates fresh packets inside policy
  -> Future packets execute only when they match the approved class
```

Automation therefore grows continuously.
It does not arrive all at once.

The operator stops approving repetitive packets as soon as the class is certified and authority is approved.
The operator gradually approves capabilities, authority expansion, policy, new action classes, and exceptional situations.

## Delegated Autonomy Policy

The long-term product model is not packet approval.
It is also not asking the operator to approve every action class forever.

The operator defines a bounded Autonomy Policy once.
Inside that policy, V7 may make operational routing decisions automatically.
Outside that policy, V7 stops safely.

The policy says:

- which action classes are allowed;
- how many users may be affected at once;
- which failure types are covered;
- how fresh the evidence must be;
- what verification must exist;
- what rollback or no-rollback path must exist;
- what anti-flap protection must pass;
- what trust, confidence, and suitability floors must pass;
- what blast radius is allowed;
- what cooldown is required;
- which stop conditions end autonomy;
- how V7 must report after every action.

The operator approves policy boundaries.
V7 may approve individual operational decisions only inside those boundaries.

V7 may not:

- expand the policy;
- add a new action class;
- increase blast radius;
- lower safety gates;
- skip rollback, verification, freshness, or learning;
- silently turn governed learning into production autonomy.

Runtime therefore asks a simple question before any automatic action:

```text
Does this fresh packet belong to an approved action class inside an approved Autonomy Policy?
```

If yes, Runtime may continue through safety, rollback, verification, freshness, anti-flap, and blast-radius gates.
If no, Runtime stops.

Autonomy modes:

- `MANUAL_PACKET_APPROVAL`: operator approves exact packets as an early governed fallback.
- `CLASS_APPROVAL`: operator approves durable action classes, but Runtime still stops before autonomous execution.
- `DELEGATED_AUTONOMY`: operator approves bounded policy, and V7 acts inside that policy.
- `PRODUCTION_AUTONOMY`: operator supervises policy and exceptions while Runtime performs routine certified work.

Current target direction:

```text
DELEGATED_AUTONOMY
```

Current runtime automation state:

```text
NO
```

## Canonical Policy Library

V7 needs durable operational policies for failure, degradation, recovery, authority, promotion, blast radius, rollback, freshness, and anti-flap behavior.

Those policies must not be invented.
They must be discovered from mature production systems, compared, validated against V7 reality, adapted, implemented, verified, certified, and integrated into OMP.

The permanent policy source is:

```text
docs/policies/
```

Policy lifecycle:

```text
DISCOVER
  -> FULL WORLD RESEARCH
  -> KNOWLEDGE NORMALIZATION
  -> INDUSTRY CONSENSUS DETECTION
  -> INDUSTRY DISAGREEMENT DETECTION
  -> CANONICAL POLICY INTERACTION AUDIT
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> REUSE EXISTING V7 OWNERS
  -> CANONICAL POLICY
  -> IMPLEMENTATION
  -> VERIFICATION
  -> CERTIFICATION
  -> OMP INTEGRATION
```

V7 may innovate only after proving:

- no stable world consensus exists;
- or world consensus does not fit V7 architecture.

Otherwise, V7 reuses world knowledge.

Initial first policy selected for research was:

```text
POLICY_001_HARD_FAILURE
```

Current policy library state:

```text
V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY
```

Current policy implementation source:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
```

OMP now chooses policy-derived implementation work by production leverage, not by policy document order.

## Product Maturity

V7 matures in product capability, not in document count.

### Prototype

V7 can observe, preview, and explain routing decisions.
Action remains manual and learning is limited.

### Operational

V7 has production owners for observation, planning, packets, restore, rollback, feedback, learning, truth, and operator surfaces.
It prepares governed actions and stops at authority boundaries.

Current maturity:

```text
Operational
```

### Production

V7 executes certified governed actions in production, verifies outcomes, closes learning, and continuously improves.

Current direction:

```text
moving through governed Production maturity
```

### Autonomous

V7 performs certified bounded actions without per-action operator approval inside approved authority tiers.
It stops or escalates outside certification.

### Large Scale

V7 supports `100+` channels and `10000+` users through aggregated knowledge, cohort/SLA views, evidence freshness, and bounded runtime work.

### Global Scale

V7 operates across many providers, countries, server classes, service profiles, user groups, and SLA tiers.
The operator supervises policy, exceptions, and authority rather than individual route decisions.

## Evolution Domains

Evolution Domains are not roadmap phases.

They evolve simultaneously.
OMP continuously selects which domain currently offers the highest maturity gain.
OMP never executes domains sequentially.

Runtime Intelligence may advance today.
Knowledge Evolution may advance tomorrow.
Scale Evolution may advance next week.
Operational Excellence may advance next month.

All domains remain permanently active.

### Domain A: Runtime Intelligence

Purpose:
Make V7 better at responding to real events with fast, safe, bounded behavior.

Success:
Runtime can wake, understand the current approved state, execute or stop safely, verify, feed learning, and sleep.

Current maturity:
Operational design is complete; runtime behavior is governed and authority-bound.

Future direction:
Move from governed one-user actions toward certified low-risk autonomous actions while keeping Runtime thin.

### Domain B: Knowledge Evolution

Purpose:
Turn raw observations into decision-grade knowledge about users, services, channels, quality, recovery, suitability, freshness, and outcomes.

Success:
V7 knows enough to make better decisions with less operator investigation.

Current maturity:
Broad knowledge exists, but not all knowledge is autonomy-grade.

Future direction:
Improve service/user/SLA fit, passive outcomes, recovery admission, freshness, anti-flap behavior, and source confidence.

### Domain C: Progressive Autonomy

Purpose:
Increase what V7 may safely do without per-action operator approval.

Success:
Each autonomy tier and action class is backed by real outcomes, rollback, verification, blast-radius control, learning, trust, and explicit authority.

Current maturity:
TIER_1 governed operator-reviewed action is active; higher autonomy remains evidence- and authority-gated.

Future direction:
Continuously promote action classes from governed proof to class authority, bounded autonomy, operational autonomy, and production autonomy.
The goal is to permanently remove packet approval for certified classes, not make packet approval easier.

### Domain D: Scale Evolution

Purpose:
Keep V7 understandable and fast as users, channels, providers, services, and policies grow.

Success:
`100+` channels and `10000+` users do not create linear operator burden or slow runtime decisions.

Current maturity:
Architecture supports scale; aggregated cohort/SLA views and long-term evidence indexing remain future maturity.

Future direction:
Build compact read models, cohort views, SLA grouping, freshness/decay behavior, and cardinality control.

### Domain E: Operational Excellence

Purpose:
Make V7 easy to operate safely.

Success:
The operator sees clear problem, recommendation, risk, rollback, authority, and approve/reject state.

Current maturity:
Operator surfaces and governed approval flows exist; the product is still authority-bound for movement.

Future direction:
Reduce manual investigation, improve explanations, certify rollback paths, and make stops more actionable.

### Domain F: Platform Evolution

Purpose:
Keep the V7 platform coherent as it grows.

Success:
The system remains simple, reusable, verifiable, and free of duplicate planners, governance, execution, and truth sources.

Current maturity:
Architecture is complete; OMP is the production operating program; product specification is now canonical.

Future direction:
Improve performance, cost, readability, deployment safety, operability, and future integration without changing product identity.

# Layer 2: Technical Appendix

This appendix preserves the technical meaning of the original specification.

Technical terms are used here because this layer is for engineers and future implementation work.

## A. Architecture

Plain meaning:
architecture is how the product is organized so that it can act safely and learn.

V7 is one integrated production routing control plane.

It is not a chain of documents and not a set of disconnected scripts.

The control loop is:

```text
runtime reality
  -> evidence
  -> knowledge
  -> decision
  -> runtime
  -> verification
  -> feedback
  -> learning
  -> knowledge
  -> OMP
  -> sleep
```

Stable owners:

- Product Specification defines what V7 is.
- OMP decides the highest leverage work and authority boundary.
- Current Program State carries volatile state.
- Decision Model defines decision semantics.
- Runtime executes or stops on approved decision snapshots.
- Planner ranks and blocks candidate movement.
- Knowledge builds compact read models.
- Learning closes the outcome loop.
- Research Framework improves engineering knowledge.
- Context Resolver prevents unrelated context loading.
- Truth/convergence verify reality.
- Evidence and runtime reality ground every claim.
- Feedback turns execution result into learning.
- Canonical Reference and SYSTEM_MAP preserve durable meaning and ownership.

Need New Owner remains `FALSE`.

Architecture verdict:

```text
ARCHITECTURE_COMPLETE
```

Remaining architectural weaknesses:

```text
0
```

## B. Capabilities

Plain meaning:
capabilities are what V7 must be able to do as a product.

| Capability | Technical meaning |
| --- | --- |
| Observe | Detect current channel, service, route, capacity, runtime, user, and event reality. |
| Understand | Convert raw observations into user/service/channel knowledge. |
| Predict | Estimate whether a path or action is likely to work under current conditions. |
| Evaluate | Compare current state with desired connectivity, policy, safety, evidence, and risk. |
| Choose | Produce an explicit decision: keep, move, failover, drain, quarantine, recover, probe-only, ask operator, or no-action. |
| Move | Change assignment only when the action class has authority and the fresh execution packet matches certified bounds. |
| Verify | Prove whether the action worked. |
| Rollback | Return to a known safer state when verification fails or safety degrades. |
| Learn | Convert observed outcomes into better future knowledge. |
| Improve | Recalculate maturity, bottleneck, authority, and next highest leverage work. |
| Scale | Keep runtime decisions bounded while background knowledge handles large evidence volume. |
| Explain | Show the operator what V7 sees, why it recommends an action, and why it stops. |
| Self-limit | Stop on missing authority, stale evidence, unsafe action, loop risk, duplicate work, or unknown reality. |
| Self-diagnose | Identify whether the blocker is knowledge, authority, real-world evidence, implementation safety, or architecture. |
| Self-certify | Use tests, truth, convergence, verification, and outcome closure before raising maturity. |
| Self-optimize | Continuously search for production leverage, simplicity, performance, operability, and safety improvements. |

Fundamental missing product capability:

```text
NONE
```

Remaining gaps are maturity, authority, evidence, scale readiness, and implementation depth, not missing product identity.

## C. Knowledge

Plain meaning:
knowledge is reliable understanding that can help V7 make or block a decision.

V7 separates:

```text
data
  -> signal
  -> knowledge
  -> action authority
```

Rows, reports, probes, screenshots, or audits are not automatically knowledge.

High-quality routing knowledge is current, covered, correct, consistent, diverse, attributable to a reliable source, relevant to users and services, and actionable through existing V7 owners.

Knowledge loop:

```text
Observation
  -> Knowledge
  -> Decision
  -> Outcome
  -> Learning
  -> Improved Decisions
```

Knowledge objects:

- channel knowledge;
- service knowledge;
- user assignment knowledge;
- route knowledge;
- capacity knowledge;
- quality knowledge;
- failure knowledge;
- recovery knowledge;
- decision outcome knowledge;
- prediction knowledge;
- suitability knowledge;
- trust knowledge;
- policy knowledge;
- freshness knowledge;
- safety knowledge;
- event knowledge;
- operator context knowledge.

Product rule:

```text
Data is not knowledge.
Knowledge is not authority.
Authority is not success.
Only verified outcomes improve trust.
```

Current knowledge truth:

- V7 has broad knowledge.
- Safety Knowledge is the strongest class.
- Suitability, service/user/SLA fit, recovery, freshness/decay, passive outcomes, and operator context need more maturity.
- Missing real outcomes are reality limits, not permission to invent evidence.

## D. Runtime

Plain meaning:
runtime is the part of V7 that handles an approved event or action now.

Runtime is thin.

It spends prepared knowledge.
It does not become the broad thinking layer.
It executes certified decisions.
It does not invent decisions.
It either executes the certified action or stops safely.

Runtime behavior:

```text
Event
  -> Runtime Wakeup
  -> Read Current Program State
  -> Read Decision Snapshot
  -> Policy
  -> Safety
  -> Action-Class Authority
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

Runtime should:

1. wake only from an approved event, explicit operator/OMP action, governed lifecycle, or recorded-state resume;
2. read current state;
3. read prepared decision and knowledge snapshots;
4. apply policy;
5. check safety;
6. check Action-Class Authority;
7. generate or consume a fresh packet through the existing packet owner;
8. verify that the packet belongs to the approved class and current policy;
9. execute or stop;
10. verify;
11. roll back if needed and authorized;
12. close outcome;
13. feed learning;
14. update continuation state;
15. notify OMP;
16. sleep.

Runtime must not:

- invent decisions;
- rerun broad research;
- perform historical recomputation;
- create evidence;
- bypass authority;
- silently retry blocked work;
- move users because time passed;
- treat stale packet state as executable;
- treat packet approval as durable authority.

## E. Autonomy

Plain meaning:
autonomy is how much V7 may safely do without asking for every single action.

V7 autonomy is progressive, bounded, and evidence-gated.

Autonomous does not mean unrestricted movement.
Autonomous means V7 can perform certified action classes within known policy, safety, blast-radius, rollback, verification, learning, and authority boundaries.

What becomes autonomous:

- detect meaningful regressions;
- classify impact;
- prepare decisions;
- choose safe action classes;
- execute certified low-risk actions;
- verify effects;
- roll back when certified and required;
- close outcomes;
- feed learning;
- update maturity and future decisions.

What requires authority:

- action crosses the current certified tier;
- action class is not approved;
- blast radius exceeds certification;
- rollback is not certified;
- verification cannot run;
- policy or user group meaning is ambiguous;
- evidence is stale, contradictory, or insufficient;
- a novel failure mode appears;
- authority expansion is proposed;
- the packet does not match an approved action class, authority generation, policy, freshness, safety, rollback/no-rollback, verification, and blast-radius boundary.

Authority evolution:

After every certified outcome, V7 must evaluate:

- should authority remain unchanged;
- should authority shrink;
- should authority expansion be proposed.
- should the completed action class move to the next autonomy state.

Expansion is never silent.
V7 may recommend expansion, but operator approval or certified policy approval is required.

Action-class promotion is never based on reports alone.
It requires real outcomes, verification, rollback quality, safety, blast radius, learning, trust, and authority policy.

Production autonomy means:

```text
Operator supervises.
Runtime executes certified decisions.
V7 explains, verifies, rolls back, learns, and stops safely.
```

Production autonomy is reached when routine production routing actions can be performed by Runtime inside certified authority while the operator handles supervision, exceptions, approvals, and policy changes.

Current autonomy state:

- TIER_1 governed operator-reviewed action is active.
- TIER_2+ remains evidence- and authority-gated.
- Trust decides autonomy tier.
- Safety decides whether a fresh packet inside an approved class may happen now.
- Packet-level approval remains required only for `GOVERNED_ONLY` classes until class authority is explicitly approved.

## F. Scalability

Plain meaning:
scale is V7's ability to keep the product understandable and safe as the network grows.

V7 targets:

- `100+` channels;
- `10000+` users;
- many providers;
- many countries;
- many servers;
- many service profiles;
- many user groups;
- different SLA classes.

At this scale, V7 must not ask the operator to inspect raw user/channel rows.
It must turn scale into product-level decisions:

- which cohorts are affected;
- which services are degraded;
- which channels are safe, degraded, quarantined, or recovering;
- which targets are eligible;
- which movements are safe by blast radius;
- which decisions require authority;
- which outcomes changed future confidence.

Scaling behavior:

```text
large evidence volume
  -> background processing
  -> compact knowledge
  -> bounded decision artifact
  -> thin runtime action or stop
```

Adding channels, users, providers, countries, or service profiles should increase background knowledge work, not event-time runtime complexity.

V7 must preserve:

- bounded runtime latency;
- operator-readable state;
- cohort/SLA-level summaries;
- explicit stale-evidence behavior;
- progressive action size;
- rollback and verification at every tier.

## G. Product Boundaries

Plain meaning:
boundaries say what V7 owns and what it cannot control.

Inside V7:

- product decision semantics;
- routing intent and desired connectivity behavior;
- observation interpretation;
- knowledge quality;
- policy-aware recommendation;
- bounded execution authority;
- verification and rollback semantics;
- learning from observed outcomes;
- operator decision surfaces;
- maturity and authority evolution;
- truth/convergence checks for product state.

Outside V7:

- the global internet;
- third-party provider behavior;
- client device operating systems;
- every possible client telemetry source;
- physical country-level network policy;
- external service availability;
- operator business policy decisions;
- hardware or provider contracts;
- user willingness to reconnect or report issues.

Boundary relationships:

- Client UI may expose status and experience, but V7 product logic must not depend on clients alone.
- Monitoring and probes feed evidence, but they are not the product by themselves.
- External probes are supporting observations, not automatic movement authority.
- Client telemetry, when added, becomes evidence, not a truth source by itself.
- Infrastructure supplies channels and servers; V7 decides safe use of them under policy.
- The operator owns authority, policy, supervision, and exception decisions.

## H. Certification

Plain meaning:
certification says whether this product definition is complete.

Is V7 Product Specification now complete?

Yes.

Current product maturity:

```text
Operational, moving through governed Production maturity.
```

Fundamental missing product questions:

```text
NONE
```

Anything removed from product meaning:

```text
NO
```

FINAL VERDICT:

```text
PRODUCT_SPECIFICATION_COMPLETE
```
