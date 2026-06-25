# V7 Product Specification 1.0

Status: canonical product specification
Product: V7 Vozduh
Version: 1.0

## 1. Product Mission

V7 is a production connectivity product that keeps users online by making routing invisible.

Its job is not to expose VPN mechanics to the operator or user.
Its job is to maintain working internet access across many routes, channels, providers, services, countries, and user groups while continuously learning which paths actually work.

As a product, V7 is:

- an autonomous routing control plane for user connectivity;
- a safety-bounded operations system;
- a learning system based on observed network outcomes;
- an operator assistant that reduces manual routing work over time;
- a product whose final experience is that users do not need to think about VPN routing.

V7 exists so that access remains available even when channels degrade, services fail, providers change behavior, evidence becomes stale, or a route that worked yesterday no longer works today.

## 2. Core Problem

Users need stable access to the internet and to important services.

Without V7, routing is operationally fragile:

- operators must manually notice channel or service degradation;
- operators must infer which users are affected;
- operators must choose a target path under uncertainty;
- moves can be too broad, too late, or based on stale evidence;
- rollback may be unclear;
- every incident can become a manual investigation;
- the system does not reliably learn from what actually happened.

The product problem is not merely "which VPN server is up".

The product problem is:

```text
Which path should this user or cohort use now,
under current reality,
with current policy,
with bounded risk,
with rollback,
with verification,
and with learning from the result?
```

V7 exists because a static panel, a manual routing table, a timer, or a raw health dashboard cannot solve that problem at production scale.

## 3. Product Vision

The ideal V7 product behaves as an invisible reliability layer for connectivity.

In the final product experience:

- users stay online without thinking about VPN routes;
- routing changes are rare, justified, and mostly invisible;
- V7 detects service, channel, route, capacity, runtime, or user-impact regressions;
- V7 understands current state against desired service availability;
- V7 chooses the safest eligible action;
- V7 asks the operator only when authority, ambiguity, evidence, policy, or risk requires it;
- V7 executes only bounded, authorized actions;
- every mutation is verified;
- failed changes roll back or escalate safely;
- every verified outcome improves future decisions;
- the operator sees problem, recommendation, reason, risk, rollback, and approval state rather than raw implementation noise;
- the system becomes smarter every week through real observed outcomes.

The product vision is not "move users automatically".

The product vision is:

```text
available connectivity
  -> invisible routing
  -> bounded autonomy
  -> verified outcomes
  -> continuous learning
  -> lower operator workload
```

## 4. Product Principles

These principles are repeatedly supported by the certified project history and define V7 as a product.

### Reality First

Runtime reality and observed outcomes are the product's source of truth.
V7 must not improve confidence from synthetic evidence or from claims that were not observed.

### User Connectivity First

The product exists to preserve user access.
Internal diagnostics matter only when they help preserve or explain real user connectivity.

### Minimal Operator Work

The operator should not manually reason through every route, probe, score, packet, and rollback path.
V7 should prepare the safe decision context and ask for authority only when authority is genuinely required.

### Safety Before Movement

Movement is not success by itself.
V7 must prefer safe stop, ask-operator, probe-only, rollback, or no-action over unsafe movement.

### Learning From Reality

V7 becomes more autonomous only through verified outcomes: successful movement, no-rollback, rollback, failed verification, operator rejection with context, and real network behavior.

### Event-Driven Operation

V7 must react to meaningful events and state deltas.
Blind timer movement is not product intent.

### Reuse Before Rewrite

The product must evolve through existing owners whenever possible.
Duplicate planners, governance, execution, truth, and learning systems make the product harder to trust.

### Simplicity Of Authority

Trust and authority are separate.
Trust decides autonomy tier; safety and explicit authority decide whether one exact bounded action may happen now.

### Explainability

V7 must explain what problem exists, who is affected, what it recommends, why, what risk exists, what rollback exists, and what authority is required.

### Reversibility

Risky production action must have rollback or recovery semantics before it is trusted.

### Verification Before Trust

A mutation that is not verified is not a successful product outcome.
No verified outcome means no trust growth.

### Background Knowledge, Thin Runtime

Heavy knowledge building belongs in background systems.
Runtime must consume compact prepared knowledge and either execute a bounded authorized action or stop safely.

### No Duplicated Systems

V7 must not become a collection of competing planners, dashboards, scripts, truth sources, or execution paths.
The product experience depends on one coherent control loop.

## 5. Product Capabilities

V7 must eventually be able to perform the following product capabilities.

| Capability | Product meaning |
| --- | --- |
| Observe | Detect current channel, service, route, capacity, runtime, user, and event reality. |
| Understand | Convert raw observations into user/service/channel knowledge. |
| Predict | Estimate whether a path or action is likely to work under current conditions. |
| Evaluate | Compare current state with desired connectivity, policy, safety, evidence, and risk. |
| Choose | Produce an explicit decision: keep, move, failover, drain, quarantine, recover, probe-only, ask operator, or no-action. |
| Move | Change assignment only when an exact bounded action has authority. |
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

Fundamental missing product capability: none.

The remaining gaps are maturity, authority, evidence, scale readiness, and implementation depth, not missing product identity.

## 6. Autonomy Model

V7 autonomy is progressive, bounded, and evidence-gated.

Autonomous does not mean unrestricted movement.
Autonomous means V7 can perform certified action classes within known policy, safety, blast-radius, rollback, verification, learning, and authority boundaries.

### What Becomes Autonomous

V7 should eventually autonomously:

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

### What Requires Authority

V7 always requires authority when:

- action crosses the current certified tier;
- blast radius exceeds certification;
- rollback is not certified;
- verification cannot run;
- policy or user group meaning is ambiguous;
- evidence is stale, contradictory, or insufficient;
- a novel failure mode appears;
- authority expansion is proposed;
- the operator has not approved the exact packet or tier.

### Authority Evolution

Authority evolves after certified real outcomes.

After every certified outcome, V7 must evaluate:

- should authority remain unchanged;
- should authority shrink;
- should authority expansion be proposed.

Expansion is never silent.
V7 may recommend expansion, but operator approval or certified policy approval is required.

### Production Autonomy

Production autonomy means:

```text
Operator supervises.
Runtime operates.
V7 explains, verifies, rolls back, learns, and stops safely.
```

Production autonomy is reached when routine production routing actions can be performed by Runtime inside certified authority while the operator handles supervision, exceptions, approvals, and policy changes.

## 7. Knowledge Model

V7 knowledge evolves through a closed product loop:

```text
Observation
  -> Knowledge
  -> Decision
  -> Outcome
  -> Learning
  -> Improved Decisions
```

Observation is raw reality.
Knowledge is observation that is fresh, covered, correct, consistent, attributable, relevant, and actionable.
Decision is the product's proposed or selected action under policy and safety.
Outcome is what actually happened after action, stop, rollback, or operator choice.
Learning is the conversion of verified outcome into better future behavior.

V7 knowledge includes:

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

The product rule is:

```text
Data is not knowledge.
Knowledge is not authority.
Authority is not success.
Only verified outcomes improve trust.
```

## 8. Runtime Model

The product runtime behavior is:

```text
Event
  -> Analysis
  -> Decision
  -> Packet
  -> Verification
  -> Learning
  -> Continuous improvement
```

Runtime is thin.

Runtime should:

1. wake only from an approved event, explicit operator/OMP action, governed lifecycle, or recorded-state resume;
2. read current state;
3. read prepared decision and knowledge snapshots;
4. apply policy;
5. check safety;
6. check authority;
7. consume the exact packet;
8. execute or stop;
9. verify;
10. roll back if needed and authorized;
11. close outcome;
12. feed learning;
13. update continuation state;
14. notify OMP;
15. sleep.

Runtime must not:

- invent decisions;
- rerun broad research;
- perform historical recomputation;
- create evidence;
- bypass authority;
- silently retry blocked work;
- move users because time passed;
- treat stale packet state as executable.

## 9. Scalability Model

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

The scaling behavior is:

```text
large evidence volume
  -> background processing
  -> compact knowledge
  -> bounded decision artifact
  -> thin runtime action or stop
```

Adding channels, users, providers, countries, or service profiles should increase background knowledge work, not event-time runtime complexity.

The product must preserve:

- bounded runtime latency;
- operator-readable state;
- cohort/SLA-level summaries;
- explicit stale-evidence behavior;
- progressive action size;
- rollback and verification at every tier.

## 10. Success Definition

V7 succeeds when:

- users stay online;
- important services remain reachable;
- routing changes are invisible or minimally disruptive;
- wrong moves are rare;
- unsafe moves are blocked before impact;
- rollback is available and trusted;
- verified outcomes improve future decisions;
- operator workload decreases;
- the operator receives clear approval/rejection decisions instead of raw investigation burden;
- V7 becomes more accurate through real-world use;
- scale increases without multiplying operator effort;
- the product can explain why it acted or why it stopped.

V7 success is not a single internal metric.

Metrics matter only because they support the product outcome:

```text
stable access
  + safe routing
  + verified learning
  + lower operator burden
```

## 11. Product Maturity Ladder

### Prototype

V7 can observe, preview, and explain routing decisions, but action remains manual and learning is limited.

Product state:
useful for diagnosis and operator assistance.

### Operational

V7 has production owners for observation, planner, packet, restore, rollback, feedback, learning, truth, and operator surfaces.
It prepares governed actions and stops at authority boundaries.

Product state:
safe supervised operation.

### Production

V7 executes certified governed actions in production, verifies outcomes, closes learning, and continuously improves through OMP.

Product state:
reliable product operation under explicit authority.

### Autonomous

V7 performs certified bounded actions without per-action operator approval inside approved authority tiers.
It stops or escalates outside certification.

Product state:
bounded autonomy.

### Large Scale

V7 supports `100+` channels and `10000+` users through aggregated knowledge, cohort/SLA views, evidence freshness, and bounded runtime work.

Product state:
production autonomy at scale.

### Global Scale

V7 operates across many providers, countries, server classes, service profiles, user groups, and SLA tiers.
Operator supervision becomes policy, exception, and authority management rather than per-route intervention.

Product state:
global autonomous connectivity control plane.

Current maturity level: `Operational`, moving through governed `Production` maturity.

## 12. What V7 Is Not

V7 is not:

- a manual routing tool;
- a static load balancer;
- a hardcoded switch engine;
- a timer-driven mover;
- a planner playground;
- a monitoring dashboard only;
- a raw VPN panel;
- a collection of scripts without product semantics;
- a system that manufactures confidence;
- a system that learns from synthetic evidence;
- a system that moves users because a score changed;
- a system that creates duplicate planners, governance, execution, or truth sources;
- a system that hides risk from the operator;
- a system that optimizes metrics while users lose connectivity.

V7 may contain dashboards, planners, probes, packets, restore barriers, runtime tools, and reports.
But the product is the controlled outcome loop, not any single tool.

## 13. Product Boundaries

### Inside V7

V7 owns:

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

### Outside V7

V7 does not own:

- the global internet;
- third-party provider behavior;
- client device operating systems;
- every possible client telemetry source;
- physical country-level network policy;
- external service availability;
- operator business policy decisions;
- hardware or provider contracts;
- user willingness to reconnect or report issues.

### Boundary Relationships

Client UI may expose status and experience, but V7 product logic must not depend on clients alone.
Monitoring and probes feed evidence, but they are not the product by themselves.
External probes are supporting observations, not automatic movement authority.
Client telemetry, when added, becomes evidence, not a truth source by itself.
Infrastructure supplies channels and servers; V7 decides safe use of them under policy.
The operator owns authority, policy, supervision, and exception decisions.

## 14. Future Programs

These are long-lived product programs, not roadmap phases.
They may run forever as the product evolves.

| Program | Purpose | Success | Completion criteria |
| --- | --- | --- | --- |
| Operational Maturity | Keep V7 moving toward highest production leverage while preserving safety and authority. | V7 always knows the next safe action or exact stop condition. | Never permanently complete; remains operating program. |
| Operational Experience | Make operator work smaller, clearer, and more decision-oriented. | Operator sees concise approve/reject/why/risk/rollback state. | Complete for a tier when operator can supervise that tier without raw investigation. |
| Progressive Autonomy | Move from governed canary to bounded autonomous action classes. | Each tier is certified through real outcomes and explicit authority. | Complete for a tier when action class, blast radius, rollback, verification, and learning are certified. |
| Authority Evolution | Evaluate whether authority should remain, shrink, or expand after certified outcomes. | Authority matches proven safety and product maturity. | Never silently complete; runs after every certified outcome. |
| Knowledge Evolution | Improve observation, freshness, suitability, service/user/SLA fit, prediction, recovery, and outcome quality. | More decisions can be made from autonomy-grade knowledge. | Complete for a knowledge object when it is autonomy-grade for the target tier. |
| Scale Evolution | Keep product behavior understandable and bounded as users/channels/providers grow. | `100+` channels and `10000+` users do not increase runtime complexity or operator burden linearly. | Complete for a scale tier when cohort/SLA/read-model behavior is certified. |
| Performance Evolution | Reduce latency, runtime cost, evidence processing cost, and operator wait time. | Faster decisions without weakening safety or explainability. | Never permanently complete; continuous product optimization. |
| Reliability Evolution | Improve rollback, verification, recovery admission, anti-flap, and failure survival. | Failures become smaller, clearer, and more reversible. | Complete for an action class when failure paths are certified. |
| Explainability Evolution | Improve how V7 explains problem, decision, stop, risk, authority, and learning. | Operator trusts V7's reasoning and sees fewer ambiguous states. | Complete for a tier when every action/stop has a clear operator-facing explanation. |

Next product program: `Progressive Autonomy`.

## 15. Certification

Is V7 Product Specification now complete?

Yes.

Fundamental missing product questions:

None.

FINAL VERDICT:

`PRODUCT_SPECIFICATION_COMPLETE`
