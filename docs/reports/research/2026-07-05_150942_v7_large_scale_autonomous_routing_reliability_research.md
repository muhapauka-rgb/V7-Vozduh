# V7 Large-Scale Autonomous Routing And Reliability Research

Timestamp: 2026-07-05_150942

Mode: Research only

Knowledge base status: `PERMANENT_CUMULATIVE_RESEARCH_KB`

Research program: `R1_LARGE_SCALE_ROUTING_RELIABILITY_TRAFFIC_ENGINEERING`

Maintenance rule:

- Never rewrite this file from scratch.
- Never delete prior conclusions.
- Extend, refine, correct, supersede, or version conclusions in place.
- If a conclusion becomes invalid, mark it `SUPERSEDED` and explain why.
- This file is the current repository routing/reliability research knowledge base because it already existed when R1 discovery ran.

Scope boundary:

- No runtime code modified.
- No Authority modified.
- No Planner modified.
- No Runtime modified.
- No production modified.
- No users moved.
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` was reviewed but not modified.

## 1. Summary

This report reviews large-scale commercial and open technical patterns for autonomous routing, failover, reliability, health scoring, rollout safety, verification, rollback, incident learning, and operator boundaries.

The strongest finding is that mature systems do not treat automation as a single "move traffic" function. They separate:

1. observation,
2. health classification,
3. incident materialization,
4. authority or safety admission,
5. bounded execution,
6. verification,
7. rollback or closure,
8. learning,
9. maturity promotion.

That separation is already aligned with V7's canonical direction. The external systems mostly strengthen V7's existing owner model rather than requiring a new architecture.

Primary adoption candidates for V7:

- multi-perspective health consensus before emergency action;
- typed health reason codes carried from observation through verification;
- readiness checks outside the runtime critical path;
- retry budgets and idempotency as execution safety, not as planner ranking hints only;
- progressive certification with hard blast-radius controls;
- explicit fail-open / fail-closed policy classification;
- automated investigation/backtesting of owner behavior;
- continuous measurement of automation debt and workflow debt.

Primary rejection candidates:

- blind timer/cron as execution authority;
- all-users automatic failover without Authority;
- synthetic-only certification;
- fail-open to unhealthy targets for paid user routing unless explicitly authorized;
- BGP/Anycast-style global routing without operator-grade observability and session impact analysis.

Final engineering verdict:

V7 should not copy any external platform wholesale. V7 should adapt proven reliability laws through existing owners: Observation, Wake, Incident, Planner, Authority, Approved Plan Lock, Restore Barrier, Runtime, Verification, Rollback, Learning, OMP, Current Program State, and Production Maturity.

## 2. Research Scope

Research target:

- commercial routing and failover systems;
- SRE reliability practices;
- CDN/load-balancing health checks;
- network failover and traffic steering;
- progressive rollout and blast-radius control;
- autonomous incident analysis;
- retry, overload, load shedding, rollback, and operator boundary patterns.

Reviewed organization and system families:

- Google SRE and Google Cloud Load Balancing;
- AWS Route 53, Global Accelerator, Elastic Load Balancing, Application Recovery Controller, Builders Library;
- Cloudflare Load Balancing;
- Netflix resilience systems including Hystrix, adaptive concurrency, and chaos engineering;
- Meta DrP automated diagnosis research;
- Fastly VCL backend health and director models;
- Tailscale connectivity and DERP relay fallback;
- Kubernetes liveness/readiness/startup probes;
- IETF BGP and Anycast operational RFCs.

Akamai was part of the desired research target, but primary documentation material was not reliably retrieved during this mission. Akamai-specific conclusions should therefore be classified as `RESEARCH_MORE`, not as canonical evidence.

## 3. Sources Reviewed

Sources count: 32 reviewed sources or source families.

Primary and near-primary sources:

1. Google SRE, Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
2. Google SRE, Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
3. Google Cloud Load Balancing Overview: https://cloud.google.com/load-balancing/docs/load-balancing-overview
4. Google Cloud Health Check Concepts: https://cloud.google.com/load-balancing/docs/health-check-concepts
5. Google SRE, Handling Overload: https://sre.google/sre-book/handling-overload/
6. Google SRE, Emergency Response: https://sre.google/sre-book/emergency-response/
7. Google SRE, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
8. Google SRE Workbook, Canarying Releases: https://sre.google/workbook/canarying-releases/
9. AWS Route 53 DNS Failover: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
10. AWS Elastic Load Balancing Target Health Checks: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
11. AWS Application Recovery Controller: https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route53-recovery.html
12. AWS Global Accelerator Use Cases: https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-benefits-of-migrating.html
13. AWS Builders Library, Timeouts, Retries, Backoff, Jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
14. AWS Builders Library, Load Shedding: https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/
15. Cloudflare Load Balancing Traffic Steering: https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/
16. Cloudflare Load Balancing Monitors: https://developers.cloudflare.com/load-balancing/monitors/
17. Cloudflare Load Shedding: https://developers.cloudflare.com/load-balancing/additional-options/load-shedding/
18. Netflix Technology Blog, Making the Netflix API More Resilient: https://netflixtechblog.com/making-the-netflix-api-more-resilient-a8ec62159c2d
19. Netflix Technology Blog, Performance Under Load: https://netflixtechblog.com/performance-under-load-3e6fa9a60581
20. Netflix Technology Blog, Chaos Engineering Upgraded: https://netflixtechblog.com/chaos-engineering-upgraded-878d341f15fa
21. Meta DrP Research: https://arxiv.org/abs/2512.04250
22. Kubernetes Liveness, Readiness, Startup Probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
23. Tailscale DERP Servers: https://tailscale.com/kb/1232/derp-servers
24. Tailscale NAT Traversal: https://tailscale.com/blog/how-nat-traversal-works
25. Tailscale Connection Types: https://tailscale.com/kb/1257/connection-types
26. Tailscale Troubleshooting: https://tailscale.com/kb/1023/troubleshooting
27. RFC 4786, Operation of Anycast Services: https://www.rfc-editor.org/rfc/rfc4786
28. RFC 4271, BGP-4: https://www.rfc-editor.org/rfc/rfc4271
29. RFC 7454, BGP Operations and Security: https://www.rfc-editor.org/rfc/rfc7454
30. RFC 8326, Graceful BGP Session Shutdown: https://datatracker.ietf.org/doc/html/rfc8326
31. Fastly Backend VCL Reference: https://www.fastly.com/documentation/reference/vcl/declarations/backend/
32. Fastly Director VCL Reference: https://www.fastly.com/documentation/reference/vcl/declarations/director/

## 4. Large-System Principles

### 4.1 Separate Detection From Authority

External systems distinguish detection from action. A health check, metric alarm, or failed probe is not automatically equivalent to authority to move production traffic.

V7 alignment:

- Observation produces facts.
- Wake materializes legal triggers.
- Authority authorizes bounded execution.
- Runtime executes only after existing gates pass.

Adoption classification: `ADOPT_EXISTING_OWNER_MODEL`.

### 4.2 Health Is A Matrix, Not A Boolean

Commercial systems use protocol-specific checks, thresholds, regional perspectives, reason codes, and status transitions. AWS ELB exposes target health status and reason codes. Cloudflare monitors can use multiple protocols and regional probing. Fastly probes use thresholds and windows.

V7 implication:

- V7 service matrix should preserve service-specific evidence, timestamps, probe type, region/source perspective, raw result class, and reason code.
- `eligible=false` should never be stored without its source health object and first producer.

Adoption classification: `ADAPT_THROUGH_OBSERVATION_AND_SERVICE_MATRIX`.

### 4.3 Readiness Is Not Runtime Critical Path

AWS ARC readiness checks are important for confidence and preparation but are not a substitute for critical-path runtime controls. Readiness can warn, block promotion, or hold certification, but emergency execution still needs its own authority and verification.

V7 implication:

- Production Maturity and Current Program State should consume readiness evidence.
- Runtime Apply should not depend on stale documentation readiness.
- Authority can require readiness only when an existing safety contract says so.

Adoption classification: `ADOPT_AS_READINESS_NOT_CRITICAL_PATH_LAW`.

### 4.4 Progressive Execution Beats Big-Bang Automation

Google canarying, Cloudflare load shedding increments, and V7's existing batch ladder all support progressive blast-radius expansion. Mature systems promote only when previous stages succeed.

V7 alignment:

- CANARY = 1.
- SMALL_BATCH = 5.
- MEDIUM_BATCH = 10.
- LARGE_BATCH = 25.
- XLARGE_BATCH = 50.
- FULL_INCIDENT = remaining affected users under existing Authority.

Adoption classification: `ALREADY_PRESENT_STRENGTHEN_EVIDENCE_WINDOWS`.

### 4.5 Retry Must Be Budgeted And Idempotent

AWS Builders Library emphasizes that retries can amplify overload. Netflix resilience work also emphasizes bounded failure containment. V7 already discovered this in production through duplicate semantic attempts.

V7 implication:

- semantic attempt identity must remain explicit;
- retry budget must be enforced before selection repeats;
- duplicate apply attempts must never masquerade as fresh recovery work.

Adoption classification: `ALREADY_ADOPTED_REQUIRE_CANONICAL_LAW`.

## 5. Organization Case Studies

### 5.1 Google SRE And Google Cloud Load Balancing

Observed principles:

- golden signals and meaningful monitoring;
- SLO-driven operation;
- automatic multi-region health-aware load balancing;
- canary-based rollout;
- incident response and postmortem culture.

V7 relevance:

- V7 should model routing autonomy as an SLO-protecting system, not as "always move if bad".
- V7 needs user-impact SLOs for channel quality, service availability, recovery time, rollback correctness, and automation safety.
- V7 should strengthen post-incident learning into Learning/OMP/Production Maturity rather than leaving reports as dead-end artifacts.

Adopt:

- SLO and error budget framing;
- golden-signal style telemetry;
- postmortem-to-owner learning;
- staged canary/batch certification.

Reject:

- any interpretation that Google-scale global automatic failover means V7 should skip Authority.

### 5.2 AWS Route 53, ELB, ARC, Builders Library

Observed principles:

- DNS failover is health-check driven.
- ELB routes to healthy targets and exposes health status reason codes.
- ARC separates readiness, routing controls, zonal shifts, and safety rules.
- Retries, timeouts, backoff, jitter, and load shedding are first-class reliability controls.

V7 relevance:

- V7 should keep health reason codes across all owner transitions.
- Readiness checks should be used by Certification/Production Maturity, not as hidden runtime state.
- Authority should explicitly classify routing-control safety rules.
- Retry budget and jitter should apply to owner invocation, not only network probes.

Adopt:

- reason-code propagation;
- readiness outside critical path;
- safety-rule admission;
- timeout/retry/backoff/jitter law;
- load shedding / drain classification.

Reject:

- fail-open to all unhealthy targets as a default for V7 users.

### 5.3 Cloudflare Load Balancing

Observed principles:

- traffic steering uses health and pool status;
- monitors can run from multiple regions;
- monitor groups and consensus can reduce false positives;
- load shedding can be incremental and reversible.

V7 relevance:

- V7 needs multi-perspective service evidence when possible, especially for service-specific failures such as Telegram/Google/ChatGPT/YouTube.
- V7 should distinguish source failure from target service suitability and target overload.
- Load shedding maps to bounded evacuation or drain, not broad unmanaged movement.

Adopt:

- multi-perspective health consensus;
- incremental shedding;
- endpoint/pool reason-code separation.

Defer:

- full global traffic steering unless V7 owns equivalent network infrastructure and telemetry.

### 5.4 Netflix Resilience Engineering

Observed principles:

- circuit breakers prevent cascading failures;
- fallbacks preserve degraded operation;
- dashboards expose real-time behavior;
- adaptive concurrency rejects excess traffic to protect latency;
- chaos experiments validate resilience under controlled conditions.

V7 relevance:

- A failed egress channel should become an incident with bounded recovery, not an unlimited retry loop.
- Circuit-breaker semantics are useful for per-service checks, per-target admission, and repeated failed semantic attempts.
- Chaos engineering maps to Controlled Production Certification, not random production disruption.

Adopt:

- circuit breaker for repeated failed user/source/target semantic attempts;
- adaptive concurrency / load pressure in `_gate_load`;
- real-time owner dashboards;
- controlled failure injection only through Certification Program rules.

Reject:

- uncontrolled chaos testing against real customers.

### 5.5 Meta DrP Automated Diagnosis

Observed principles:

- incident diagnosis can codify expert playbooks;
- analyzer chains can automate investigation;
- analyzers need backtesting, canarying, and ownership;
- automated investigation improves MTTR but must be tested and governed.

V7 relevance:

- V7's Engineering Automation and Workflow Evolution direction is strongly aligned.
- Owner Resolution should evolve into analyzers that can prove producers, consumers, object continuity, and first divergence.
- Automated diagnosis should not directly mutate production unless connected to Authority and Certification.

Adopt:

- codified investigation analyzers;
- backtesting against historical reports/artifacts;
- analyzer canaries;
- automated evidence graph generation.

Defer:

- ML-driven action selection until analyzer correctness and owner contracts are certified.

### 5.6 Fastly CDN Health And Backend Selection

Observed principles:

- backend health probes have windows, thresholds, intervals, expected responses, and initial states;
- directors select among backend pools;
- health-check load can be reduced through sharing.

V7 relevance:

- service matrix should avoid lock contention and duplicate expensive probes.
- Health should include threshold/window logic instead of single transient samples.
- Target selection should separate backend pool membership from current user assignment.

Adopt:

- threshold/window health model;
- shared probe result semantics;
- explicit backend pool selection contracts.

### 5.7 Tailscale Connectivity And DERP Fallback

Observed principles:

- direct path is preferred;
- relay fallback preserves connectivity when direct traversal fails;
- clients measure paths and choose low-latency relay regions;
- troubleshooting distinguishes direct, relayed, and blocked states.

V7 relevance:

- V7 should classify connection path states explicitly: direct channel, relayed/degraded, failed, unknown.
- A target being reachable does not mean it is the best target for a user or service.
- Fallback can preserve availability but may carry latency/cost tradeoffs.

Adopt:

- connection type classification;
- fallback path semantics;
- user-visible/owner-visible path diagnostics.

Defer:

- DERP-like relay construction unless it becomes a formal V7 capability.

### 5.8 Kubernetes Probes

Observed principles:

- liveness, readiness, and startup probes have different meanings;
- readiness controls traffic admission;
- liveness controls restart/self-healing;
- startup controls initialization grace.

V7 relevance:

- source failure, target readiness, service suitability, and runtime liveness must remain separate.
- Certification readiness is not the same as Runtime execution readiness.

Adopt:

- explicit probe intent taxonomy.

### 5.9 BGP, Anycast, And Carrier Operations

Observed principles:

- Anycast can provide locality and resilience but can complicate monitoring and session stability.
- BGP routing changes require careful policy, filtering, and security.
- graceful shutdown supports draining before route withdrawal.

V7 relevance:

- V7 should not treat anycast/BGP as a simple failover hammer.
- If future network-level routing control is added, V7 needs drain, session impact, convergence, and route-security ownership.

Adopt:

- drain-before-withdraw principle;
- route change safety analysis.

Reject for now:

- BGP/anycast autonomy without a certified network-control owner.

## 6. Common Architectural Patterns

Common pattern across mature systems:

```text
Observation
-> Health classification
-> Incident or routing-control candidate
-> Policy / authority admission
-> Bounded execution
-> Independent verification
-> Rollback / closure
-> Learning
-> Promotion or demotion
```

V7 already has equivalent owners:

- Observation;
- Wake;
- Incident;
- Planner;
- Authority;
- Approved Plan Lock;
- Restore Barrier;
- Runtime Apply;
- Verification;
- Rollback / No-Rollback;
- Learning;
- OMP;
- Current Program State;
- Production Maturity.

No new owner is required by this research.

## 7. Common Operational Laws

Recommended V7 operational laws:

1. Detection is not authority.
2. Health must be typed, timestamped, and attributable.
3. Every selected move must preserve identity through execution.
4. Readiness supports promotion but does not replace runtime safety.
5. Retry must be budgeted by semantic attempt.
6. Rollout expands only after evidence.
7. Rollback must be verified, not assumed.
8. Automation must be backtested before promotion.
9. Manual action becomes automation/workflow debt unless intentionally manual.
10. Documentation synchronizes capability; it does not create capability.

Most of these laws already exist in V7 documents. The missing piece is a concise external benchmark mapping that proves they are not arbitrary internal process rules.

## 8. Detection And Telemetry Patterns

External patterns:

- golden signals;
- health checks with thresholds;
- regional probe consensus;
- reason-coded target health;
- per-service probe output;
- freshness windows;
- dashboard visibility;
- incident analyzer chains.

V7 comparison:

- V7 has service matrix and production reports.
- V7 has suffered when historical raw objects were not persisted.
- V7 has already improved lock scope and evidence timing.

Adoption candidates:

- `Health Evidence Object` with:
  - producer,
  - owner,
  - timestamp,
  - freshness,
  - service,
  - probe type,
  - raw result,
  - normalized reason,
  - confidence,
  - consumer list.
- `First Divergence Evidence` requirement for every rollback.
- multi-perspective probe support where existing service owners can provide it.

## 9. Health Scoring Patterns

External patterns:

- binary health for routing admission;
- weighted health for steering;
- threshold/window health for stability;
- service-specific health for application reality;
- load pressure and latency as health dimensions.

V7 comparison:

- V7 should avoid a single opaque score for emergency movement.
- V7 should use score-like aggregates only if all constituent evidence remains inspectable.

Recommended V7 health model:

```text
source_health = interface + service + freshness + load + safety
target_health = reachability + required_services + load + identity + verification_readiness
move_health = source_failed + affected_user + target_safe + authority + rollback_ready
```

Adoption classification: `ADAPT_THROUGH_EXISTING_GATES`.

## 10. Failover And Routing Patterns

External patterns:

- DNS failover;
- load balancer backend failover;
- pool and steering policies;
- relay fallback;
- zone/region shift;
- route withdrawal/drain;
- graceful shutdown.

V7 comparison:

- V7's failover is user-assignment movement, not generic traffic routing.
- Therefore V7 must preserve user/source/target identity and rollback path more strongly than many stateless load balancers.

Adoption candidates:

- drain-before-failover for stateful or session-sensitive users;
- per-service target suitability before move;
- incident-source continuation until affected users are zero or source recovers;
- never select unrelated source users for same failed-source incident.

## 11. Blast Radius And Rollout Patterns

External patterns:

- canaries;
- progressive percentages;
- traffic shedding;
- staged rollout;
- safety halt on failed verification.

V7 comparison:

- V7's controlled certification ladder is aligned.
- The ladder should remain governed by Authority and Production Maturity.

Recommended strengthening:

- every ladder stage should record:
  - users selected;
  - users moved;
  - users verified;
  - rollback count;
  - source remaining users before/after;
  - services checked;
  - evidence freshness;
  - automation debt created/closed;
  - workflow debt created/closed.

## 12. Verification And Rollback Patterns

External patterns:

- health checks after traffic shift;
- rollback/traffic restoration;
- verification windows;
- partial failure containment;
- circuit breaker re-open on repeated failure.

V7 comparison:

- V7 already treats verification as a real owner.
- V7 should preserve verification command/probe output for every service failure and timeout.

Adoption candidates:

- verification matrix must be comparable to planner service matrix;
- rollback decision must identify exact failed check;
- `UNKNOWN` verification due to timeout should be distinct from service `FAIL`;
- lock wait should be measured separately from probe execution.

## 13. Incident Management Patterns

External patterns:

- incident response playbooks;
- postmortems;
- automated diagnosis analyzers;
- readiness and recovery controls;
- operator boundary for high-risk changes.

V7 comparison:

- V7 has strong engineering-report culture.
- V7 should ensure no report becomes terminal when execution remains incomplete.

Adoption candidates:

- convert repeated forensic report types into analyzers;
- backtest analyzers against historical reports;
- add incident "object continuity passport" to ensure investigation does not switch candidates.

## 14. Automation Guardrail Patterns

External guardrails:

- safety rules;
- circuit breakers;
- retry budgets;
- authority/approval;
- blast-radius budgets;
- readiness checks;
- canary gates;
- rollback hooks;
- post-action verification.

V7 comparison:

- V7 already encodes many of these as separate owners.
- The risk is not lack of guardrails; the risk is broken continuity between owners or missing persistence of proof objects.

Adoption candidates:

- owner contract compatibility checks before every new automation bridge;
- explicit "changed contract" matrix for each capability;
- no hidden recomputation between Approved Plan Lock, Restore Barrier, and Runtime Apply.

## 15. SLO / SLA / Error Budget Patterns

External patterns:

- SLOs define user-visible correctness.
- Error budgets decide how much risk can be spent.
- Overload/failover is managed against user impact, not only internal metrics.

V7 adoption candidates:

- Channel Availability SLO.
- Required Service Reachability SLO.
- Emergency Recovery Time Objective.
- Verification Correctness SLO.
- Rollback Correctness SLO.
- Automation Safety SLO.
- False Positive Movement Budget.
- Failed Recovery Attempt Budget.

These should be owned by OMP and Production Maturity as consumers, with evidence produced by Runtime/Verification/Learning.

## 16. Human / Operator Boundary Patterns

External patterns:

- operators approve risky automation stages;
- safety controllers enforce policy;
- dashboards make automation inspectable;
- emergency response relies on clear ownership.

V7 comparison:

- Authority is the correct owner for human/operator boundary.
- Codex should not become Authority.
- Documentation should not become Authority.

Adoption candidates:

- explicit operator boundary table:
  - what can run autonomously;
  - what requires explicit Authority promotion;
  - what is intentionally manual;
  - what is blocked by future capability;
  - what is canonically impossible.

## 17. Self-Healing And Self-Improvement Patterns

External patterns:

- Kubernetes restarts failed containers through liveness probes.
- Netflix circuit breakers and fallback keep service behavior degraded but available.
- Meta DrP automates diagnosis.
- Google SRE postmortems feed learning.

V7 comparison:

- V7 self-healing must mean legal completion through existing owners, not direct mutation.
- Self-improvement should be OMP-driven: evidence creates capability, capability earns authority, authority enables production.

Adoption candidates:

- analyzer-backed Owner Resolution;
- automatic workflow audit after repeated manual command chains;
- certification pool growth as permanent platform responsibility.

## 18. Comparison Against Current V7 Autonomous Operating System

Reviewed V7 AOS characteristics:

- AOS is target map, not implementation engine.
- Current Program State is GPS/autonomy inventory.
- OMP is execution engine/navigator.
- Existing owners implement capability.
- Authority and Runtime safety cannot be bypassed.
- Certification validates capability.
- Autonomy levels progress from manual evidence to certified autonomous production operation.

External comparison:

| External principle | V7 current alignment | Gap |
|---|---:|---|
| Detection separate from authority | Strong | Keep bridges owner-compatible |
| Progressive rollout | Strong | Continue evidence windows through FULL_INCIDENT |
| Readiness separate from runtime | Partial/strong | Add explicit readiness-not-critical-path law to AOS |
| Typed health reason codes | Partial | Require preserved health evidence object |
| Multi-perspective health | Partial | Add as target pattern, not immediate requirement |
| Retry budgets | Strong after recent fixes | Canonicalize semantic attempt budget law |
| Automated diagnosis | Partial | Convert repeated forensics into analyzers |
| SLO/error budget governance | Partial | Add OMP/Production Maturity SLO mapping |
| Operator boundary | Strong | Add explicit fail-open/fail-closed policy table |
| Anycast/BGP autonomy | Not present | Defer |

## 19. Practices V7 Should Adopt

Adopt now through existing owners:

1. Health Evidence Object preservation.
2. Health reason-code continuity from Observation to Verification.
3. Multi-stage progressive certification evidence windows.
4. Retry/idempotency budget law.
5. Explicit fail-open / fail-closed policy classification.
6. Readiness-not-critical-path law.
7. Multi-perspective service health target model.
8. Owner contract compatibility matrix for every automation bridge.
9. Analyzer/backtesting model for recurring forensic workflows.
10. SLO/error budget framing for production autonomy.

## 20. Practices V7 Should Reject

Reject:

1. Timer/cron as authority.
2. Synthetic-only production certification.
3. Direct runtime movement without Authority.
4. Broad all-user automation before ladder certification.
5. Fail-open to all bad targets as default.
6. Opaque health scores without raw evidence.
7. Hidden recomputation between locked plan and runtime apply.
8. Uncontrolled chaos testing against customers.
9. BGP/Anycast failover without a certified network-control owner.
10. Documentation synchronization as a reason to block already-earned safe capability unless an existing safety owner requires it.

## 21. Practices V7 Should Defer

Defer:

1. Anycast routing control.
2. BGP autonomous route withdrawal.
3. multi-cloud region switch automation.
4. ML-based action selection.
5. autonomous chaos experiment generation.
6. DERP-like relay infrastructure.
7. Akamai-specific adoption until primary sources are reviewed.
8. automatic FULL_INCIDENT without Authority certification.

## 22. Proposed Additions To V7_AUTONOMOUS_OPERATING_SYSTEM.md

This report does not modify `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`. Proposed additions only:

1. External Benchmark Principle
   - V7 autonomy should be measured against proven large-system reliability patterns, but only adopted through existing V7 owners.

2. Health Evidence Continuity Law
   - Every health decision must preserve producer, owner, timestamp, freshness, probe, reason, and consumer path.

3. Readiness Is Not Runtime Authority Law
   - Readiness supports certification and promotion. Runtime execution still requires Authority, Restore Barrier, Runtime, Verification, and Rollback contracts.

4. Semantic Retry Budget Law
   - Retry budget is consumed by semantic attempt identity, not by incidental command invocation identity.

5. Fail-Open / Fail-Closed Classification Law
   - Every safety gate must state whether failure mode is fail-open, fail-closed, hold, rollback, or canonical impossibility.

6. Multi-Perspective Health Target
   - Future higher autonomy should prefer multi-perspective health evidence for service-specific decisions.

7. Automation Analyzer Law
   - Repeated forensic workflows should become tested analyzers owned by existing engineering automation owners.

8. SLO/Autonomy Link
   - Autonomy level should be connected to production SLO evidence and error budget posture.

## 23. Proposed Additions To OMP

Proposed OMP additions:

1. Research Intake Classification
   - Each external practice is classified as `ADOPT`, `ADAPT`, `REJECT`, `DEFER`, or `RESEARCH_MORE`.

2. Owner Mapping For External Practices
   - No external practice may enter implementation until mapped to an existing V7 owner or proven to require a new owner.

3. Analyzer Backtesting Queue
   - Recurring investigation patterns should enter an analyzer backlog with historical report fixtures.

4. SLO/Error Budget Workstream
   - OMP should connect certification outcomes to user-visible SLOs.

5. External Benchmark Review Cycle
   - Periodically compare V7 autonomy against large-system reliability patterns.

## 24. Proposed Additions To Current Program State / Autonomy Inventory

Proposed inventory fields:

- capability name;
- current autonomy level;
- certified ladder stage;
- current Authority budget;
- health evidence maturity;
- multi-perspective telemetry status;
- verification maturity;
- rollback maturity;
- retry/idempotency maturity;
- operator boundary;
- automation debt;
- workflow debt;
- synchronization debt;
- external benchmark status;
- next certification mission;
- next automation mission;
- current blocker owner;
- owner resolution state.

These fields should remain consumer state. They must not approve Runtime Apply.

## 25. Open Questions

1. Which V7 owner should maintain the canonical Health Evidence Object schema?
   - Candidate: Observation/service matrix owner.

2. Should multi-perspective probes be mandatory for higher certification stages?
   - Candidate: Production Maturity and Authority decision.

3. What are the initial user-visible SLOs for V7?
   - Candidate: OMP plus Production Maturity.

4. Which repeated forensic workflows should become analyzers first?
   - Candidate: object identity continuity, lock ownership, first divergence, retry budget lineage.

5. Should fail-open ever be permitted for user routing?
   - Candidate: Authority policy decision. Default recommendation is no.

6. What is the minimum evidence window for promotion from XLARGE_BATCH to FULL_INCIDENT?
   - Candidate: Controlled Production Certification Program plus Authority.

7. Can V7 safely create controlled failure drills without harming users?
   - Candidate: Certification Program, not Runtime.

8. Akamai-specific practices remain unreviewed from primary sources.
   - Classification: `RESEARCH_MORE`.

## 26. Final Engineering Verdict

Verdict: `RESEARCH_COMPLETE_OWNER_MAPPED`

The external evidence supports V7's current architectural direction: autonomous production recovery should be governed, owner-based, evidence-preserving, progressively certified, verified, rollback-capable, and continuously improved.

No new Runtime, Planner, Authority, Wake, Restore Barrier, Packet owner, OMP, or architecture is required by this research.

V7 should improve by strengthening existing canonical documents and owners with:

- health evidence continuity;
- multi-perspective telemetry targets;
- typed reason-code propagation;
- SLO/error budget framing;
- retry/idempotency budget law;
- fail-open/fail-closed classification;
- analyzer backtesting;
- readiness-not-critical-path semantics.

V7 should reject shortcuts that bypass Authority, Runtime, Verification, Rollback, or Reality First.

Production impact: none.

Runtime impact: none.

Authority impact: none.

Files changed by this research mission:

- `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`

## 27. Knowledge Base Version History

### R1 Update 2026-07-05_151847

Reason:

Research Program R1 formalized this file as the permanent cumulative knowledge base for large-scale routing, reliability, and traffic engineering.

Discovery result:

- Existing routing/reliability research document found.
- No new permanent research document created.
- Existing document extended in place.

Knowledge preservation result:

- Prior conclusions preserved.
- No prior conclusion deleted.
- No prior conclusion superseded in this update.
- AWS Global Accelerator added as an explicit source family.
- Practice registry and research-question answers added.

Current versioned conclusion:

`R1_CONCLUSION_2026_07_05`: V7's current owner-based architecture remains compatible with large-scale routing and reliability practices. The strongest external systems reinforce V7's separation of Observation, Wake, Incident, Planner, Authority, Runtime, Verification, Rollback, Learning, OMP, Current Program State, and Production Maturity. The most important R1 improvement is not a new owner; it is a permanent practice registry and owner-mapped intake discipline.

## 28. R1 Practice Registry

Classification vocabulary:

- `ADOPT_NOW`: V7 should incorporate the practice through existing owners now, usually as documentation, evidence requirement, test requirement, or owner-mapped implementation task.
- `ADAPT`: practice is valid but must be translated to V7's user-routing model and existing safety owners.
- `RESEARCH_MORE`: high-value area but insufficient primary evidence or insufficient V7 owner mapping in this research pass.
- `DEFER`: valid practice but not urgent, not yet mature enough, or dependent on future capability.
- `REJECT`: practice conflicts with V7 safety, Reality First, Authority, production constraints, or user protection.

| Practice | Classification | Why | Benefits | Risks | Scalability | Safety | Operational Complexity | Production Maturity | V7 Compatibility | Existing Owner Mapping |
|---|---|---|---|---|---|---|---|---|---|---|
| Separate observation from execution | `ADOPT_NOW` | Universal large-system pattern and already central to V7. | Prevents facts from becoming unauthorized actions. | Risk if owner boundaries are undocumented. | High. | High. | Medium. | Mature. | Strong. | Observation, Wake, Authority, Runtime. |
| Typed health evidence with reason codes | `ADOPT_NOW` | AWS ELB, Cloudflare, Fastly, and V7 forensics all show opaque health causes break debugging. | Better decisions, better rollback proof, lower false diagnosis. | Schema drift if unmanaged. | High. | High. | Medium. | Ready. | Strong. | Service matrix, Observation, Verification, Engineering Reports. |
| Multi-perspective health consensus | `ADAPT` | Cloudflare regional monitors and global load balancers reduce local false positives. | Reduces false positives and target misclassification. | More probes, lock pressure, inconsistent regional truth. | High if shared/cached. | High if not used as sole authority. | Medium/high. | Partial. | Compatible through existing evidence owners. | Observation, service matrix, Production Maturity. |
| Threshold/window health classification | `ADOPT_NOW` | Fastly probes and load balancers use windows/thresholds instead of single samples. | Reduces flapping. | Slower reaction if windows too long. | High. | High. | Medium. | Ready for documentation and tests. | Strong. | Observation, Planner gates, Verification. |
| SLO/error-budget framing | `ADAPT` | Google SRE uses SLOs to decide acceptable risk and urgency. | Aligns routing automation with customer experience. | Bad SLOs can incentivize wrong actions. | High. | High if owners preserve evidence. | Medium. | Partial. | Strong with OMP. | OMP, Production Maturity, Current Program State. |
| Progressive canary/batch ladder | `ADOPT_NOW` | Google canaries, Cloudflare incremental shedding, V7 certification ladder align. | Limits blast radius. | Slow if authority windows too conservative. | High. | High. | Medium. | Already active. | Strong. | Controlled Production Certification Program, Authority. |
| AWS Global Accelerator-style static entry and anycast regional failover | `DEFER` | Useful for global app networks but V7 currently controls user egress assignment, not global edge routing. | Stable client entry, faster regional failover. | Anycast/session effects, network owner absent. | High at provider scale. | Medium without network-control owner. | High. | Not current. | Conceptually useful, not directly applicable. | Future network-control owner if ever created; currently OMP research only. |
| AWS ARC-style readiness outside critical path | `ADOPT_NOW` | Readiness should inform promotion and disaster readiness, not silently mutate runtime. | Better certification without unsafe hidden gates. | Operators may overtrust readiness. | High. | High. | Medium. | Ready. | Strong. | Production Maturity, Current Program State, Authority. |
| Retry budget by semantic attempt | `ADOPT_NOW` | AWS retries and V7 duplicate-apply production evidence both show retry amplification risk. | Avoids repeated bad moves. | Can skip a user that later recovers unless retry state is well-scoped. | High. | High. | Medium. | Already proven in V7. | Strong. | Runtime, Planner candidate selection, Approved Plan Lock, Rollback/Learning. |
| Backoff and jitter for repeated owner invocation | `ADAPT` | AWS Builders Library treats retries and periodic work as load sources. | Reduces synchronized pressure and lock contention. | Can delay urgent incident work if misapplied. | High. | Medium/high. | Medium. | Partial. | Compatible. | Wake, governed heartbeat, service-matrix refresh owners. |
| Load shedding / traffic shedding | `ADAPT` | Cloudflare and AWS use shedding to protect overloaded systems. | Protects targets and prevents cascades. | May reduce service for some users. | High. | High if governed. | Medium/high. | Partial. | Must map to bounded user routing, not blind drop. | Planner load gate, Authority, Runtime, Verification. |
| Circuit breakers | `ADAPT` | Netflix uses them to stop cascading failures and fall back. | Prevents repeated bad calls/actions. | Incorrect breaker can suppress valid recovery. | High. | High if transparent. | Medium. | Partial. | Compatible for semantic attempt and service checks. | Planner, Runtime, Rollback, Learning. |
| Controlled chaos / failure injection | `DEFER` | Netflix validates resilience through controlled experiments. | Finds hidden defects before incidents. | Dangerous without certification pool and authority. | High when mature. | Low until controlled environment is strong. | High. | Future. | Compatible only through Certification Program. | Controlled Production Certification Program. |
| Automated diagnosis analyzers | `ADAPT` | Meta DrP shows playbook automation can reduce MTTR when tested. | Reduces week-long manual forensics. | Wrong analyzer may misclassify root cause. | High. | High if read-only/backtested. | Medium/high. | Partial. | Strong with Engineering Automation. | OMP, Engineering Automation, Owner Resolution, Engineering Reports. |
| DERP-like relay fallback | `DEFER` | Tailscale uses relays when direct paths fail. | Preserves connectivity under NAT/path failures. | New infrastructure, cost, latency, policy implications. | High with investment. | Medium. | High. | Not current. | Future capability only. | Future capability through OMP, not Runtime shortcut. |
| Kubernetes-style probe taxonomy | `ADOPT_NOW` | Liveness/readiness/startup separation prevents semantic confusion. | Clearer gates and fewer false blockers. | Naming churn if not mapped carefully. | High. | High. | Low. | Ready. | Strong. | Observation, Runtime Model, Production Maturity. |
| Graceful drain before route withdrawal | `ADAPT` | RFC 8326 and traffic engineering practices avoid abrupt disruption. | Safer transitions and fewer customer-visible drops. | Slower emergency action. | High. | High if bounded. | Medium/high. | Partial. | Strong for non-immediate failures; emergency cases need policy. | Planner, Authority, Runtime, Rollback. |
| BGP/Anycast autonomous routing control | `RESEARCH_MORE` | Important at carrier scale but needs dedicated network-control evidence. | Potentially powerful global failover. | High blast radius and session instability. | High. | Low without new certified owner. | High. | Not ready. | Weak today. | OMP research only. |
| Fail-open to unhealthy targets | `REJECT` | Some load balancers fail open, but user-routing systems must protect customers. | May preserve partial availability when all targets unknown. | Can move users into known bad state. | Medium. | Low by default. | Medium. | Not acceptable default. | Conflicts unless explicit Authority policy exists. | Authority would need explicit exception. |
| Timer/cron as execution authority | `REJECT` | Timers can schedule evaluation but cannot prove incident truth or authorization. | Simple implementation. | Caused previous V7 automation block. | Medium. | Low. | Low but unsafe. | Rejected. | Conflicts with V7. | Wake/Authority must own legality. |
| Synthetic-only certification | `REJECT` | Reality First requires real production evidence for certification. | Easy to run. | Certifies fantasies. | Low. | Low. | Low. | Rejected. | Conflicts with V7. | Certification Program rejects. |
| Opaque aggregate health score | `REJECT` | Scores without raw evidence hide first divergence. | Simple UI. | Breaks root cause proof. | Medium. | Low. | Low. | Rejected as authority input. | Only acceptable as read-only summary. | Current Program State / Dashboard consumer only. |
| Akamai GTM / CDN-specific transfer | `RESEARCH_MORE` | Primary source retrieval was insufficient in this pass. | Likely relevant. | Unsafe to infer. | Unknown. | Unknown. | Unknown. | Not ready. | Unknown. | OMP research backlog. |

## 29. R1 Research Question Answers

### How do they detect failures?

Large systems combine active probes, passive metrics, target status, routing control-plane state, service-level metrics, and customer-impact signals.

V7 conclusion:

- Detection should remain in Observation/service matrix owners.
- Wake may consume confirmed detection but must not fabricate it.
- Classification: `ADOPT_NOW`.

### How do they measure health?

They measure health using protocol checks, thresholds, windows, reason codes, regional probes, latency, errors, saturation, reachability, and sometimes direct customer experience.

V7 conclusion:

- V7 should preserve both raw probe evidence and normalized health result.
- A single `eligible=false` is insufficient unless the first health producer is preserved.
- Classification: `ADOPT_NOW`.

### How do they classify health?

Common classifications include healthy, unhealthy, draining, initial, unknown, degraded, overloaded, and reason-coded failure states.

V7 conclusion:

- V7 should classify source, target, service, load, safety, and freshness separately.
- Classification: `ADAPT`.

### How do they prevent false positives?

Patterns include multi-region probe consensus, consecutive threshold windows, passive/active comparison, backoff, readiness separation, and canary verification.

V7 conclusion:

- The strongest fit is threshold/window health plus multi-perspective evidence when available.
- Classification: `ADAPT`.

### How do they route traffic?

Patterns include DNS failover, load balancer pool selection, anycast edge routing, custom routing accelerators, CDN request mapping, BGP/IGP policy, and relayed fallback.

V7 conclusion:

- V7 routes users by assignment and egress selection, not by generic packet-level routing.
- V7 should adapt pool/endpoint health and policy ideas but reject direct network-control copying.
- Classification: `ADAPT`.

### How do they reroute traffic?

They reroute through health-aware steering, endpoint weights, traffic dials, routing controls, failover records, pool failover, zonal/region shift, or route withdrawal.

V7 conclusion:

- Reroute means governed user movement through Authority, Restore Barrier, Runtime, Verification, and Rollback.
- Classification: `ADAPT`.

### How do they verify reroute success?

They verify backend health, customer-facing availability, error rates, latency, and post-shift probe results.

V7 conclusion:

- Verification must compare the actual moved user's required services against Planner evidence and Runtime result.
- Classification: `ADOPT_NOW`.

### How do they rollback?

They rollback by restoring routing weights, shifting traffic back, disabling endpoints, reopening circuit breakers, or reverting deployment/routing controls.

V7 conclusion:

- Rollback must be per selected move or per governed batch with exact identity.
- Classification: `ADOPT_NOW`.

### How do they avoid routing oscillation?

They use hysteresis, thresholds, cooldowns, backoff, health windows, circuit breakers, route dampening, and progressive recovery.

V7 conclusion:

- V7 should continue using incident cooldown, retry budgets, and certification ladders; add explicit oscillation evidence in reports.
- Classification: `ADAPT`.

### How do they perform graceful drain?

They reduce traffic, lower preference, withdraw gradually, use graceful BGP shutdown, or mark backends draining before removal.

V7 conclusion:

- For non-immediate emergency movement, V7 should consider drain-before-move semantics through Authority.
- For confirmed hard failure, emergency failover may skip long drain but must document why.
- Classification: `ADAPT`.

### How do they handle overloaded targets?

They use load shedding, adaptive concurrency, endpoint weights, capacity-aware routing, admission control, and fallback pools.

V7 conclusion:

- `_gate_load` and Authority should treat target overload as an execution safety condition.
- Classification: `ADAPT`.

### How do they perform capacity planning?

They use utilization, saturation, regional capacity, historical demand, traffic distribution, and planned failover capacity.

V7 conclusion:

- V7 certification ladder should record remaining users, target capacity, service load, and failover headroom per stage.
- Classification: `ADAPT`.

### How do they perform traffic engineering?

They steer traffic by policy, topology, capacity, performance, business constraints, and route safety. At carrier scale this can involve BGP, segment routing, MPLS/SR, IGP metrics, and TE controllers.

V7 conclusion:

- V7 should learn traffic engineering vocabulary but not implement network-level TE without a certified owner.
- Classification: `RESEARCH_MORE`.

### How do they separate observation from execution?

Mature systems preserve a control boundary: monitors detect, controllers decide, policy/authority admits, executors change production, verifiers confirm.

V7 conclusion:

- This is a core V7 invariant and should remain non-negotiable.
- Classification: `ADOPT_NOW`.

### How do they perform health consensus?

They use multiple probes, multiple regions, majority/threshold rules, passive telemetry, and freshness bounds.

V7 conclusion:

- V7 should target multi-perspective consensus for higher autonomy but not block current certified owner paths on missing future telemetry unless Authority requires it.
- Classification: `ADAPT`.

### How do they structure telemetry?

They structure telemetry around metrics, logs, traces, reason codes, probe results, health histories, dashboards, and incident artifacts.

V7 conclusion:

- V7 needs persistent object continuity for candidate identity, health evidence, selected move, verification, rollback, and learning.
- Classification: `ADOPT_NOW`.

### How do they structure routing policies?

Policies encode endpoint eligibility, weights, priorities, locality, failover targets, safety rules, health requirements, and operator controls.

V7 conclusion:

- V7 policies should remain Authority-owned and action-class aware.
- Classification: `ADAPT`.

### How do they structure failover policies?

Failover policies usually define health trigger, alternate target, priority, safety gate, blast radius, rollback, and recovery conditions.

V7 conclusion:

- V7 L3 policies should continue using incident source, affected users, authority budget, selected move identity, verification, rollback, and closure conditions.
- Classification: `ADOPT_NOW`.

### How do they classify routing decisions?

They classify decisions by health, locality, capacity, cost, priority, failover, recovery, drain, and overload state.

V7 conclusion:

- V7 should keep `move_type`, `action`, `reason`, `action_class`, `execution_class`, and `terminal_reason` separate and auditable.
- Classification: `ADOPT_NOW`.

### How do they protect users?

They limit blast radius, verify health, use canaries, preserve rollback, isolate failures, avoid cascades, and expose operator controls.

V7 conclusion:

- User protection is V7's primary routing safety invariant.
- Classification: `ADOPT_NOW`.

### How do they verify customer experience?

They use external probes, application metrics, direct client telemetry, error rates, latency, support signals, and synthetic checks.

V7 conclusion:

- V7 currently has stronger server-side/service-side verification than direct client telemetry.
- Direct client telemetry is a future improvement, not a blocker for current governed production execution.
- Classification: `DEFER`.

### How do they learn from incidents?

They use postmortems, automated diagnosis, playbook codification, backtesting, analyzer systems, and maturity promotion/demotion.

V7 conclusion:

- V7 should turn repeated report patterns into analyzers and feed results into OMP/Production Maturity.
- Classification: `ADAPT`.

## 30. R1 Source Family Notes

### AWS Global Accelerator

Key observed pattern:

AWS Global Accelerator uses static client-facing entry points and anycast edge routing to direct users toward regional endpoints, and it can reroute when an application endpoint fails in a primary Region.

V7 interpretation:

- Useful conceptually for stable entry points, health-aware regional failover, and endpoint groups.
- Not directly transferable to V7's current model because V7 moves user egress assignments rather than owning a global anycast edge network.

Classification: `DEFER`.

Existing owner mapping:

- OMP research intake;
- future network-control capability only if V7 later owns global routing infrastructure;
- Current Program State can track this as future benchmark, not current runtime requirement.

### Major ISP / Carrier Traffic Engineering

Key observed pattern:

Carrier traffic engineering uses BGP policy, route filtering, route preference, multipath, route stability, capacity, and sometimes graceful route withdrawal/drain. These systems optimize network-wide behavior and must account for convergence, policy safety, and route security.

V7 interpretation:

- V7 should borrow the concepts of capacity, convergence, drain, blast radius, and anti-oscillation.
- V7 should not attempt BGP/Anycast autonomy without a certified network-control owner.

Classification: `RESEARCH_MORE`.

Existing owner mapping:

- OMP research intake;
- Production Maturity as consumer;
- no current Runtime/Authority change.

### Akamai

R1 result:

Primary Akamai source retrieval was insufficient in this pass. No Akamai-specific architectural claim is promoted to V7 guidance.

Classification: `RESEARCH_MORE`.

Existing owner mapping:

- OMP research backlog.

## 31. R1 Compatibility With V7

R1 does not require:

- new Runtime;
- new Planner;
- new Authority;
- new Wake owner;
- new Restore Barrier owner;
- new Packet owner;
- new production behavior;
- new deployment;
- user movement.

R1 strengthens existing V7 direction:

- Observation must preserve health facts.
- Wake must materialize only legal triggers.
- Planner must not invent executable truth.
- Authority owns blast radius and promotion.
- Approved Plan Lock and Restore Barrier preserve committed identity.
- Runtime executes only legal committed objects.
- Verification proves user/service result.
- Rollback closes failures.
- Learning and OMP convert outcomes into capability.
- Current Program State and Production Maturity consume evidence but do not create capability.

## 32. R1 Final Knowledge Verdict

Verdict: `R1_RESEARCH_KB_EXTENDED`

No previous conclusion was superseded.

Permanent knowledge base file:

- `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`

R1 added:

- permanent KB status;
- version history;
- AWS Global Accelerator source;
- practice classification registry;
- research-question answers;
- source family notes for AWS Global Accelerator, carrier traffic engineering, and Akamai;
- explicit V7 compatibility statement.

Production impact: none.

Runtime impact: none.

Authority impact: none.
