# V7 Autonomous Operations Research

Status: `PERMANENT_CUMULATIVE_RESEARCH_KB`
Research program: `R2_LARGE_SCALE_AUTONOMOUS_OPERATIONS_SRE_INCIDENT_CHANGE_PRODUCTION_GOVERNANCE`
Created: 2026-07-05
Mode: `RESEARCH_ONLY`

Rules:

- Never rewrite this file from scratch.
- Never delete previous knowledge.
- Extend, refine, correct, supersede, and version conclusions in place.
- If a conclusion becomes invalid, mark it `SUPERSEDED` and explain why.
- This document is research evidence and owner-mapped guidance. It does not grant V7 runtime capability.

Scope boundary:

- Runtime code modified: `NO`
- Planner code modified: `NO`
- Authority code modified: `NO`
- OMP code modified: `NO`
- Production code modified: `NO`
- Deployment files modified: `NO`
- Canonical docs modified: `NO`
- Users moved: `NO`

## 1. Summary

Research Program R2 studies how large, commercially successful, high-reliability organizations run production operations at scale and how they convert repeated human work into governed automation without weakening safety.

The strongest external pattern is not "automate everything." The strongest pattern is:

```text
ownership
  -> detection
  -> incident command
  -> severity / priority
  -> runbook
  -> bounded automation
  -> safe change / rollout
  -> verification
  -> rollback / containment
  -> postmortem
  -> engineering work
  -> maturity improvement
```

For V7, this maps cleanly onto existing owners:

```text
Reality
  -> Observation / Wake / Incident
  -> Planner / Authority
  -> Approved Plan Lock / Restore Barrier / Runtime
  -> Verification / Rollback / Learning
  -> Engineering Report
  -> OMP
  -> Production Maturity
  -> Current Program State
  -> next mission
```

R2 conclusion:

V7 should adopt operations discipline as an owner-mapped control system, not as a new operations architecture. The external evidence reinforces V7's current laws: Reality First, Existing Owner, Authority before scale, Evidence before autonomy, Verification before promotion, Rollback before closure, and no duplicate Runtime/Planner/Authority/OMP/truth source.

## 2. Research History

| Date | Research program | Scope | Sources added | Organizations added | Sections changed | Conclusions changed | Open questions added | Files changed |
|---|---|---:|---:|---|---|---|---|---|
| 2026-07-05 | R2 Large-Scale Autonomous Operations, SRE, Incident Management, Change Management, Production Governance | Initial permanent KB creation | 41 | Google, AWS/Amazon, Microsoft Azure, Cloudflare, Netflix, Meta, Stripe, GitHub, Uber, LinkedIn, Atlassian, PagerDuty, Kubernetes/CNCF | Sections 1-34 created | Initial conclusions created; none superseded | 12 | `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md` |

## 3. Scope

In scope:

- autonomous operations;
- SRE;
- incident management;
- production ownership;
- change management;
- runbooks/playbooks;
- on-call and escalation;
- production governance;
- SLO/error-budget governance;
- progressive rollout;
- rollback and recovery;
- automation guardrails;
- toil reduction;
- postmortems and learning;
- operational maturity;
- V7 owner mapping.

Out of scope:

- modifying V7 runtime code;
- modifying V7 Planner;
- modifying V7 Authority;
- changing OMP code;
- deployment;
- production mutation;
- user movement;
- new owners;
- duplicate execution path.

## 4. Sources

Sources reviewed:

1. Google SRE, The Evolution of Automation at Google: https://sre.google/sre-book/automation-at-google/
2. Google SRE, Eliminating Toil: https://sre.google/sre-book/eliminating-toil/
3. Google SRE, Being On-Call: https://sre.google/sre-book/being-on-call/
4. Google SRE, Managing Incidents: https://sre.google/sre-book/managing-incidents/
5. Google SRE, Emergency Response: https://sre.google/sre-book/emergency-response/
6. Google SRE, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
7. Google SRE, Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
8. Google SRE Workbook, Error Budget Policy: https://sre.google/workbook/error-budget-policy/
9. AWS Builders Library, Going Faster with Continuous Delivery: https://aws.amazon.com/builders-library/going-faster-with-continuous-delivery/
10. AWS Well-Architected Reliability Pillar: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
11. AWS Systems Manager Incident Manager overview: https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html
12. AWS Incident Manager incident creation: https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-creation.html
13. AWS Incident Manager contacts: https://docs.aws.amazon.com/incident-manager/latest/userguide/contacts.html
14. AWS Incident Manager runbooks: https://docs.aws.amazon.com/incident-manager/latest/userguide/runbooks.html
15. AWS Builders Library, Timeouts, Retries, Backoff, Jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
16. AWS Builders Library, Load Shedding: https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/
17. Microsoft Azure Well-Architected Operational Excellence: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/
18. Microsoft Azure Well-Architected Reliability: https://learn.microsoft.com/en-us/azure/well-architected/reliability/
19. Microsoft Azure Safe Deployment Practices: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments
20. Microsoft Azure Incident Management Process: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/incident-response
21. Microsoft Azure Automation Guidance: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/enable-automation
22. Microsoft Azure Reliability Testing Strategy: https://learn.microsoft.com/en-us/azure/well-architected/reliability/reliability-test
23. Cloudflare outage caused by bad software deploy: https://blog.cloudflare.com/cloudflare-outage/
24. Cloudflare detailed July 2 2019 outage postmortem: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
25. Cloudflare outage on June 21 2022: https://blog.cloudflare.com/cloudflare-outage-on-june-21-2022/
26. Cloudflare control plane and analytics outage postmortem: https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/
27. Netflix Chaos Engineering Upgraded: https://netflixtechblog.com/chaos-engineering-upgraded-878d341f15fa
28. Netflix API Resilience: https://netflixtechblog.com/making-the-netflix-api-more-resilient-a8ec62159c2d
29. Netflix Adaptive Concurrency Limits: https://netflixtechblog.com/performance-under-load-3e6fa9a60581
30. Netflix Automated Canary Analysis with Kayenta: https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69
31. Meta October 4 outage details: https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/
32. Meta DrP automated investigations paper: https://arxiv.org/abs/2512.04250
33. Stripe Online Migrations at Scale: https://stripe.com/blog/online-migrations
34. Stripe API Versioning: https://stripe.com/blog/api-versioning
35. Stripe Idempotency: https://stripe.com/blog/idempotency
36. GitHub Load Balancer: https://github.blog/engineering/infrastructure/introducing-glb/
37. Uber Domain-Oriented Microservice Architecture: https://www.uber.com/blog/microservice-architecture/
38. Uber Failover Architecture paper: https://arxiv.org/abs/2603.07345
39. LinkedIn School of SRE: https://linkedin.github.io/school-of-sre/
40. Atlassian Incident Management Handbook: https://www.atlassian.com/incident-management/handbook
41. PagerDuty Incident Response Documentation: https://response.pagerduty.com/

Source quality note:

- Google, AWS, Microsoft, Cloudflare, Netflix, Meta, Stripe, GitHub, Uber, LinkedIn, Atlassian, and PagerDuty sources are official or primary-adjacent engineering sources.
- Arxiv sources are used only when authored as large-scale production system papers or when official engineering material is unavailable.
- Shallow marketing content was not used as authority.

## 5. Organizations Reviewed

| Organization/source family | Reviewed for | R2 confidence |
|---|---|---|
| Google SRE / Production Engineering | automation, toil, SLOs, on-call, incidents, postmortems | High |
| AWS / Amazon | continuous delivery, incident manager, operational readiness, rollback/guardrails | High |
| Microsoft Azure | operational excellence, safe deployment, incident response, automation, reliability testing | High |
| Cloudflare | postmortems, progressive deployment failure, global incidents, rollback | High |
| Netflix | chaos engineering, circuit breakers, adaptive concurrency, canary analysis | High |
| Meta | global incident response, storm drills, automated investigation platform | High |
| Stripe | online migrations, idempotency, API/version compatibility | Medium/high |
| GitHub | load-balancer reliability, graceful drain, testable layers | Medium |
| Uber | ownership/domain boundaries, dependency complexity, failover architecture | Medium |
| LinkedIn | SRE onboarding, SLA/SLO mapping, foundational SRE skills | Medium |
| Atlassian | incident roles, severity, communication, post-incident process | Medium |
| PagerDuty | incident response lifecycle, roles, postmortems | Medium |
| Kubernetes/CNCF patterns | liveness/readiness/probes, controller/reconciliation patterns | Medium |

## 6. Large-Scale Operations Principles

Common principles:

1. Production ownership must be explicit.
2. Detection does not equal diagnosis.
3. Diagnosis does not equal authority to act.
4. Execution requires bounded permission and rollback path.
5. Automation is valuable when well-scoped, tested, observable, and reversible.
6. Runbooks are transitional artifacts: repeated runbooks should become automation or be classified as intentionally manual.
7. Error budgets and SLOs connect user impact to change velocity.
8. Progressive rollout and bake time reduce blast radius.
9. Recovery must be verified, not assumed.
10. Postmortems must produce engineering work, not just narrative.

V7 mapping:

- These principles align with AOS/OMP/Production Maturity.
- No new V7 owner is required by this research.

## 7. Production Ownership Models

External models:

- Google: service ownership by SRE/product engineering, with SRE focused on engineering solutions to operations.
- Amazon: small service-owning teams own consequences of production defects.
- Uber: domain boundaries and gateways reduce ownership ambiguity at thousands-of-service scale.
- LinkedIn: SRE sits at software/systems intersection and converts business requirements to SLAs.

V7 interpretation:

- Every capability must have an existing owner.
- "Blocking owner" is not enough; owner resolution must classify why the owner blocked.
- Ownership should follow the object: Observation, Wake, Incident, Planner, Authority, Runtime, Verification, Rollback, Learning, OMP, Production Maturity.

Classification: `ADOPT_NOW`

## 8. Incident Detection Models

External models:

- Google uses meaningful monitoring and paging around user-impacting conditions.
- AWS Incident Manager creates incidents from CloudWatch alarms and EventBridge events.
- Cloudflare uses synthetic tests, global traffic drop alerts, CPU telemetry, and PoP reports.
- Azure incident guidance separates detection, containment, triage, recovery, RCA, and postmortem.

V7 interpretation:

- Observation can detect facts.
- Wake must materialize a legal incident trigger.
- Timer/cron alone remains non-authoritative.

Classification: `ADOPT_NOW`

## 9. Severity And Priority Models

External models:

- Cloudflare declared P0 when alert patterns indicated global serious impact.
- Atlassian/PagerDuty incident guides commonly separate severity, urgency, role assignment, and communication cadence.
- SLO/error budget systems connect severity to user impact and allowed downtime.

V7 interpretation:

- Severity should be derived from affected users, service criticality, source/target impact, rollback exposure, and Authority scope.
- Severity must not directly bypass Authority.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`

Existing owners:

- Incident;
- Authority;
- Current Program State;
- Production Maturity;
- Engineering Reports.

## 10. Incident Command And Escalation Models

External models:

- Google incident management separates command, operations, communications, and planning roles.
- AWS Incident Manager response plans define responders, runbooks, collaboration tools, contacts, on-call schedules, and escalation paths.
- Azure incident guidance requires defined roles such as incident manager, technical lead, and communications lead.
- PagerDuty formalizes incident commander style response and post-incident review.

V7 interpretation:

- OMP is the execution engine for engineering continuation.
- Authority owns risk/approval boundary.
- Current Program State records current blocker and next action.
- Codex must not become permanent incident command.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`

## 11. Runbook And Playbook Models

External models:

- AWS Incident Manager runbooks combine automated actions with manual steps.
- Google automation hierarchy shows runbooks/scripts should evolve into system-owned automation or designed-away operations.
- Meta DrP codifies investigation playbooks as analyzers.

V7 interpretation:

- Runbooks map to Workflow Candidates.
- Repeated runbook execution maps to Workflow Debt.
- Safe, repeated, well-scoped runbooks should become owner-owned automation.

Classification: `ADOPT_NOW`

## 12. Automation Guardrail Models

External models:

- Google: automation is a force multiplier, not a panacea; domains must be well-defined.
- AWS: pipelines use tests, alarms, deployment windows, metric gates, and override paths.
- Azure: automation needs safe deployment practices, health models, halt/recovery on issue detection.
- Netflix: circuit breakers and adaptive concurrency stop cascading failures.

V7 interpretation:

- Automation guardrails are already split across Authority, Restore Barrier, Runtime, Verification, Rollback, and Production Maturity.
- V7 should add explicit automation suspension/circuit breaker language to AOS/OMP as a proposed future canonical addition.

Classification: `ADOPT_NOW`

## 13. Change Management Models

External models:

- AWS pipelines standardize release paths, encode best practice checks, and prioritize availability before speed.
- Azure treats every production deployment as risky and requires standard patterns, prechecks, progressive exposure, and rollback/roll-forward instructions.
- Stripe online migrations show multi-phase change, dual writes, offline backfill, production comparisons, and incremental cutover.
- Cloudflare's WAF outage shows why global one-shot deploys for high-impact changes are dangerous.

V7 interpretation:

- V7 safe deploy must stay owner-governed and evidence-producing.
- Documentation cannot substitute for production verification.
- Emergency changes may accelerate gates only through explicit Authority.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`

## 14. Progressive Rollout Models

External models:

- AWS deploys through cells and canaries, watching for errors and positive data points.
- Azure recommends progressive exposure, canary/blue-green patterns, bake time, health gates, and feature flags.
- Netflix Kayenta-style automated canary analysis compares metrics before promotion.
- V7 already uses a governed certification ladder.

V7 interpretation:

- V7's 1 -> 5 -> 10 -> 25 -> 50 -> FULL_INCIDENT ladder is aligned with industry.
- Promotion must remain evidence-based and Authority-bound.

Classification: `ADOPT_NOW`

## 15. Rollback And Recovery Models

External models:

- AWS deployment engines roll back when they can detect failure.
- Azure requires rollback, roll-forward, last-known-good config, and state/data rollback guidance.
- Cloudflare used global termination/rollback, then tested and re-enabled in controlled scope.
- Stripe uses reversible incremental migrations and idempotency to make retries safe.

V7 interpretation:

- V7 must keep rollback/no-rollback closure as a first-class terminal owner.
- Verification and rollback evidence must be persisted per selected move or batch item.

Classification: `ADOPT_NOW`

## 16. SLO / Error Budget Governance

External models:

- Google SRE uses SLOs and error budgets to balance reliability and release velocity.
- AWS/Azure reliability frameworks require reliability targets, monitoring, recovery strategy, and proven failure recovery.
- LinkedIn School of SRE describes converting business requirements into SLAs for system components and monitoring adherence.

V7 interpretation:

- V7 should define user-visible SLOs for routing availability, service reachability, recovery time, verification correctness, rollback correctness, and automation safety.
- Error budget should feed Authority and Production Maturity as input, not bypass runtime safety.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`

## 17. Toil Reduction Models

External models:

- Google defines toil as manual, repetitive, automatable, tactical, low enduring value, and O(n) with service growth.
- Google targets at least 50% engineering work for SREs and uses toil reduction to scale operations sublinearly.
- Meta DrP reduces on-call toil through automated investigations.

V7 interpretation:

- V7 already has Automation Debt and Workflow Debt concepts.
- R2 strengthens the rule: every repeated manual Codex/engineer workflow must become a Workflow Candidate or intentionally manual.

Classification: `ADOPT_NOW`

## 18. Postmortem And Learning Models

External models:

- Google blameless postmortems turn failure into system learning.
- Cloudflare publishes detailed technical postmortems and concrete process corrections.
- AWS Incident Manager post-incident analysis creates follow-up action items.
- Azure requires blameless postmortems in safe deployment process.

V7 interpretation:

- Engineering Reports must not become terminal.
- Reports feed Learning, OMP, Production Maturity, and Current Program State.
- Repeated report classes should become analyzers.

Classification: `ADOPT_NOW`

## 19. Operational Maturity Models

External models:

- AWS Well-Architected measures foundations, resilient architecture, change management, and failure recovery.
- Azure Well-Architected defines operational excellence and reliability maturity.
- Google SRE maturity is visible in toil ratio, automation depth, SLOs, incident handling, and launch/release discipline.

V7 interpretation:

- V7 already separates Engineering Maturity from Production Maturity.
- R2 supports keeping research/model completion separate from production-autonomous capability.

Classification: `ADOPT_NOW`

## 20. Human Boundary Models

External models:

- Google: manual operations may be unavoidable, but normal operations requiring human touch indicate a bug as systems grow.
- AWS/Azure: overrides exist but are explicit and should be logged.
- Incident command systems assign human roles for judgment, communication, and emergency approval.

V7 interpretation:

- Humans remain responsible for policy, exceptional approval, business risk, and architecture changes.
- Routine diagnosis, evidence gathering, regression, deploy orchestration, and report synchronization should become automation candidates.

Classification: `ADOPT_NOW`

## 21. Production Freeze / Safety Halt Models

External models:

- AWS pipelines halt on alarms, known bad artifacts, time windows, or metric changes, with explicit override for urgent fixes.
- Azure says rollout must halt immediately when health changes or user-impact alerts appear.
- Google error budget policy slows/freeze launches when reliability budget is exhausted.

V7 interpretation:

- V7 should map safety halt to OMP/Authority HOLD.
- HOLD is not a final root cause; Owner Resolution must classify the block.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`

## 22. Autonomous Operations Patterns

Patterns:

1. Automated detection -> incident creation.
2. Response plan -> responders/runbook/collaboration.
3. Runbook -> automation where safe.
4. Safe deploy pipeline -> gates/alarms/rollback.
5. Canary -> metrics -> promotion/abort.
6. Circuit breaker -> fail fast/fallback/containment.
7. Investigation analyzer -> reduced MTTR.
8. Postmortem -> action item -> engineering mission.
9. Maturity model -> next capability decision.

V7 interpretation:

- All patterns are compatible if implemented through existing owners.
- None justify a new OMP, new Runtime, or new Authority.

## 23. Anti-Patterns

Anti-patterns for V7:

1. Timer/cron treated as authority.
2. Report-only completion.
3. Runbook forever with no automation audit.
4. Manual workflow forever with no pipeline audit.
5. Global rollout without staged certification.
6. Automation without rollback.
7. Alert without owner.
8. Owner block without Owner Resolution.
9. Postmortem without engineering work.
10. SLO/error budget used to bypass safety gates.
11. Opaque AI/SRE agent mutating production.
12. Codex as permanent production dependency.

## 24. Comparison Against V7 Autonomous Operating System

| External operating practice | Current V7 alignment | Gap / caution |
|---|---|---|
| Automation as force multiplier with scoped domains | Strong | Add explicit external benchmark in AOS. |
| Toil reduction discipline | Strong | Quantify Automation/Workflow Debt trends. |
| Incident command roles | Partial | Map incident command roles to OMP/Authority/CPS boundaries. |
| Response plans and runbooks | Partial | Convert repeated runbooks into Workflow Candidates. |
| Progressive rollout | Strong | Continue evidence through certification ladder. |
| Error budget governance | Partial | Define V7 SLOs before using budgets in Authority input. |
| Safe deployment practices | Strong in principle | Keep safe deploy pipeline owner-mapped and evidence-backed. |
| Automated canary analysis | Partial | Use only as advisory until V7 metric reliability is certified. |
| Automated investigation platform | Partial | Build analyzers read-only first, backtest, then certify. |
| Human approval boundaries | Strong | Preserve human policy authority; reduce routine human toil. |
| Production freeze / halt | Partial | Make OMP/Authority HOLD semantics explicit for instability. |

## 25. Practices V7 Should Adopt

1. Toil definition and measurement.
2. Runbook-to-automation conversion rule.
3. Incident response role mapping.
4. Response plan object for serious incidents.
5. Postmortem action-item-to-OMP mission rule.
6. Progressive rollout with health gates and rollback.
7. Safety halt when metrics or verification fail.
8. Automation suspension / circuit breaker after bad outcomes.
9. Owner Resolution before accepting any blocker as terminal.
10. Production Maturity consuming evidence but not granting authority.

## 26. Practices V7 Should Adapt Through Existing Owners

1. SLO/error-budget governance.
   - Existing owners: OMP, Production Maturity, Authority.

2. Incident command roles.
   - Existing owners: OMP, Authority, Current Program State.

3. Runbook automation.
   - Existing owners: OMP, Engineering Automation, Workflow Debt.

4. Safe deployment acceleration for emergencies.
   - Existing owners: Authority, safe deploy owner, OMP.

5. Automated canary analysis.
   - Existing owners: Production Maturity, metric reliability, certification ladder.

6. Automated diagnosis analyzers.
   - Existing owners: Engineering Reports, Owner Resolution, OMP.

7. Controlled chaos / drills.
   - Existing owners: Controlled Production Certification Program, Authority, Production Maturity.

## 27. Practices V7 Should Reject

1. Automation without explicit owner.
2. Production mutation by AI/SRE agent without Authority.
3. Global rollout without progressive exposure.
4. Postmortem closure without action item disposition.
5. Error budget used as runtime apply permission.
6. On-call/Codex manual intervention as normal operating model.
7. Runbook steps that remain manual forever without classification.
8. Safety halt bypass because a fix is urgent.
9. Synthetic-only production certification.
10. New owner creation before existing-owner discovery.

## 28. Practices V7 Should Defer

1. Full AI-driven incident commander.
2. Autonomous production hotfix generation.
3. Fully automated chaos experiments.
4. SLO-based Authority expansion without production evidence.
5. Cross-capability global automation freeze/thaw engine.
6. Network-scale regional failover playbooks not tied to current V7 owners.
7. Advanced predictive rollout tuning.
8. Customer-facing direct telemetry integration if not yet owner-mapped.

## 29. Proposed Additions To V7_AUTONOMOUS_OPERATING_SYSTEM.md

This mission does not modify `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`. Proposed additions only:

1. Autonomous Operations Law
   - V7 autonomous operations must preserve separate owners for detection, diagnosis, decision, execution, verification, rollback, review, and learning.

2. Toil Classification Law
   - Manual work tied to production, repetitive, automatable, tactical, low enduring value, or O(n) with growth must be Automation Debt or Workflow Debt until classified.

3. Runbook Evolution Law
   - A repeated runbook must become automation, a workflow/pipeline candidate, intentionally manual, blocked by future capability, not cost-effective, or canonically impossible.

4. Incident Command Boundary
   - OMP coordinates engineering continuation, Authority owns risk approval, Current Program State records volatile state, and Codex cannot be permanent incident command.

5. Automation Suspension Law
   - Any autonomous action class must be suspendable after verification failure, rollback failure, repeated incident, stale evidence, or Authority withdrawal.

6. Production Freeze / Safety Halt Law
   - Instability may halt promotion or deployment, but a halt must be owner-resolved and classified.

## 30. Proposed Additions To OMP

Proposed additions:

1. Operations Practice Intake
   - External operations practices are classified as `ADOPT_NOW`, `ADAPT_THROUGH_EXISTING_OWNER`, `RESEARCH_MORE`, `DEFER_UNTIL_CAPABILITY_EXISTS`, or `REJECT_FOR_V7`.

2. Runbook Conversion Queue
   - Repeated runbooks become OMP-owned Workflow Candidates unless intentionally manual.

3. Postmortem Action Routing
   - Every postmortem action item must route to an existing owner, policy decision, automation candidate, workflow candidate, or canonical impossibility.

4. Production Freeze Resolver
   - HOLD/freeze must run Owner Resolution rather than staying at "blocked."

5. Operations Health Review
   - OMP should track automation debt, workflow debt, manual incident count, repeated runbook count, rollback correctness, and verification correctness.

## 31. Proposed Additions To Current Program State / Autonomy Inventory

Proposed consumer fields:

- current incident owner;
- current severity;
- current incident command boundary;
- current response plan status;
- active safety halt/freeze state;
- active manual runbooks;
- repeated runbook count;
- automation debt current;
- workflow debt current;
- owner resolution state;
- current SLO/error-budget posture;
- current rollback readiness;
- current verification readiness;
- current postmortem action state.

These fields must remain volatile consumer state. They must not approve Runtime Apply or expand Authority.

## 32. Proposed Additions To Production Maturity

Proposed maturity inputs:

- incident response evidence;
- postmortem action closure;
- runbook automation progress;
- toil reduction trend;
- safe deploy gate evidence;
- rollback verification evidence;
- SLO/error budget evidence;
- automation suspension evidence;
- workflow/pipeline certification evidence.

Proposed maturity outputs:

- `OPERATIONS_MATURITY_ACCEPT`;
- `OPERATIONS_MATURITY_PARTIAL_ACCEPT`;
- `OPERATIONS_MATURITY_BLOCK`;
- `OPERATIONS_MATURITY_NO_CHANGE`;
- `OPERATIONS_MATURITY_INVALID_EVIDENCE`.

These are proposed semantic refinements only. Production Maturity must remain a consumer and must not become Authority.

## 33. Open Questions

1. What are V7's first production SLOs for user connectivity, service reachability, recovery time, verification correctness, and rollback correctness?
2. Which owner should maintain the canonical V7 response plan template?
3. Which repeated engineering workflows should become the first certified Pipeline Candidates?
4. Which incident classes require human incident commander vs OMP-only continuation?
5. What is the minimum evidence for automating a currently manual runbook?
6. How should V7 record intentionally manual work without letting it become hidden toil?
7. What should trigger automation suspension for each action class?
8. How should V7 express production freeze/HOLD in Authority terms?
9. Which postmortem action item classes must block promotion?
10. Can controlled production drills safely create incident response evidence without ordinary customer impact?
11. What direct customer-experience telemetry is required before higher autonomy levels?
12. Should V7 create read-only automated analyzers for object identity continuity, first divergence, lock ownership, retry budget lineage, and owner resolution?

## 34. Final Engineering Verdict

Verdict: `R2_AUTONOMOUS_OPERATIONS_KB_CREATED`

R2 found no reason to create a new Runtime, Planner, Authority, OMP, truth source, execution path, or production owner.

The strongest external lesson is that production autonomy is earned by operational discipline:

```text
clear ownership
  -> alert/incident discipline
  -> runbooks
  -> bounded automation
  -> progressive rollout
  -> verified rollback
  -> postmortem action
  -> maturity feedback
```

V7 is architecturally aligned with this model, but should strengthen the operations layer by adding:

- toil/runbook classification;
- incident command boundary mapping;
- response plan semantics;
- automation suspension;
- production freeze/HOLD owner resolution;
- postmortem action routing;
- SLO/error-budget integration;
- read-only automated investigation analyzers.

All additions should be routed through existing owners:

- OMP;
- Authority;
- Current Program State;
- Production Maturity;
- Engineering Reports;
- Controlled Production Certification Program;
- existing execution/verification/rollback/learning owners.

No runtime, Authority, production, deployment, or canonical document changes were made by this research mission.

## Appendix A. Practice Classification Matrix

| Practice | Organization/source | Problem solved | Mechanism | Benefits | Risks | Required telemetry | Required authority or approval | Required rollback/containment | Required maturity level | V7 compatibility | Existing V7 owner mapping | Recommended V7 classification | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Explicit production ownership | Google, Amazon, Uber, LinkedIn | Ownerless incidents and unclear responsibility | Service/domain/team ownership | Faster triage, less confusion | Bad ownership boundaries can create silos | service/component map, incident owner | OMP/owner assignment | escalation/containment owner | Basic | Strong | SYSTEM_MAP, OMP, CPS | `ADOPT_NOW` | V7 already requires existing owner mapping. |
| Incident response plan | AWS Incident Manager, Azure, Atlassian, PagerDuty | Ad hoc incident response | predefined responders, channels, runbooks | faster coordination | stale plan | alert, incident object, contact/on-call | OMP/Authority for V7 | rollback owner and communications | Medium | Strong | OMP, CPS, Engineering Reports | `ADAPT_THROUGH_EXISTING_OWNER` | Needs V7-specific owner boundary mapping. |
| Severity model | Cloudflare, Atlassian, PagerDuty | all incidents treated equally | impact/urgency classification | prioritizes response | wrong severity can over/underreact | affected users, service impact, scope | Authority for scale | containment by severity | Medium | Strong | Incident, Authority, CPS | `ADAPT_THROUGH_EXISTING_OWNER` | V7 has affected-user/Authority concepts but needs explicit severity vocabulary. |
| SLO/error-budget governance | Google SRE, Azure, AWS | unreliable change velocity | SLI/SLO/error budget controls | balances reliability and speed | bad SLOs distort behavior | SLIs, availability, latency, recovery, errors | Authority/Production Maturity | freeze/halt/rollback | Medium/high | Strong | OMP, Production Maturity, Authority | `ADAPT_THROUGH_EXISTING_OWNER` | Must not grant runtime apply directly. |
| Toil classification | Google SRE | manual repetitive work scales linearly | toil definition and engineering allocation | reduces operational load | over-automation of judgment work | manual action logs, workflow history | OMP classification | none unless automation acts | Basic | Strong | Automation Debt, Workflow Debt, OMP | `ADOPT_NOW` | Directly matches V7 Automation/Workflow Debt. |
| Runbook-to-automation | Google, AWS, Meta DrP | repeated runbook execution | codify as automation/analyzer | faster MTTR, consistency | brittle automation if untested | runbook execution history, outcomes | owner approval before mutation | rollback/containment per action | Medium | Strong | OMP, Engineering Automation, Owner Resolution | `ADOPT_NOW` | Repeated runbooks should become Workflow Candidates. |
| Automated incident creation | AWS Incident Manager | humans must notice/create incident | CloudWatch/EventBridge -> incident | faster response | noisy incidents | alert source, dedupe key, response plan | Wake/Incident legality | no direct mutation | Medium | Strong | Observation, Wake, Incident | `ADAPT_THROUGH_EXISTING_OWNER` | Legal wake source required in V7. |
| Safe deployment pipeline | AWS, Azure | inconsistent production changes | standardized pipeline, gates, checks | lower deployment risk | pipeline can hide wrong assumptions | build, tests, health, alarms | safe deploy owner, Authority for risky ops | rollback/roll-forward | Medium | Strong | safe deploy, OMP, Production Maturity | `ADOPT_NOW` | V7 already uses safe deploy; strengthen reporting. |
| Progressive rollout / canary | AWS, Azure, Netflix | large blast radius | canary/cells/bake time/metrics | catches defects early | false confidence if metrics weak | health metrics, customer impact, errors | Authority budget | abort/rollback | Medium/high | Strong | Certification Program, Authority | `ADOPT_NOW` | V7 ladder already implements this shape. |
| Automated canary analysis | Netflix Kayenta | manual metric interpretation | statistical canary comparison | faster promotion/abort | bad metric selection | baseline/canary metrics | Production Maturity/Authority | automatic abort/rollback only if certified | High | Partial | Metric Reliability, Production Maturity | `DEFER_UNTIL_CAPABILITY_EXISTS` | Use advisory first until metrics certified. |
| Circuit breaker/fallback | Netflix | cascading dependency failure | trip circuit, fallback/fail fast | protects system | hides broken dependency | rolling window errors, latency, queue saturation | policy owner for behavior | fallback/containment | Medium | Strong for advisory/execution guard | Planner, Runtime, Verification, Rollback | `ADAPT_THROUGH_EXISTING_OWNER` | Maps to semantic attempt suspension and service containment. |
| Adaptive concurrency/load shedding | Netflix, AWS | overload cascades | admission limit, reject excess | preserves latency/availability | may reject useful work | latency, inflight, queue, utilization | Runtime/Authority policy | fail fast/contain | High | Partial | Planner load gate, Runtime, Authority | `ADAPT_THROUGH_EXISTING_OWNER` | Must not become broad automation. |
| Controlled chaos/drills | Netflix, Meta, Azure | unknown recovery weakness | controlled failure exercises | validates resilience | can harm users if uncontrolled | steady-state metrics, blast scope | Certification/Authority | rollback/restoration | High | Partial | Controlled Certification Program | `DEFER_UNTIL_CAPABILITY_EXISTS` | Use only controlled production certification first. |
| Blameless postmortem | Google, Cloudflare, Azure, AWS | incidents repeat | structured review and action items | learning, prevention | action items can rot | incident timeline, impact, root/contributing causes | OMP routing | action owner/containment | Basic | Strong | Engineering Reports, Learning, OMP | `ADOPT_NOW` | Reports must feed engineering work. |
| Automated investigations | Meta DrP | slow manual diagnosis | analyzers/playbooks/code | MTTR and toil reduction | analyzer can mislead | logs, metrics, traces, incident data | read-only first; Authority if action | no mutation until certified | Medium/high | Strong read-only | OMP, Owner Resolution, Engineering Automation | `ADAPT_THROUGH_EXISTING_OWNER` | Build analyzers through existing report/owner system. |
| Online migrations | Stripe | large changes without downtime | dual write, compare, incremental switch | availability and correctness | dual-write inconsistency | consistency checks, read/write diffs | change owner | revert/cutover plan | High | Conceptual | safe deploy, Verification, Rollback | `ADAPT_THROUGH_EXISTING_OWNER` | Useful for state/data changes, not direct routing action. |
| Idempotency | Stripe, AWS | unsafe retries | idempotency keys/semantic identity | safe retry/replay | wrong identity can suppress legitimate action | request/attempt identity, outcome | Runtime/packet owner | duplicate detection | Medium | Strong | Approved Plan Lock, Restore Barrier, Runtime | `ADOPT_NOW` | V7 already needed semantic attempt identity. |
| Domain ownership/gateways | Uber | microservice dependency complexity | domains, gateways, extension points | clearer ownership, lower blast radius | wrong abstraction can hide failures | dependency map, owner map | architecture/owner approval | local rollback | Medium/high | Conceptual | SYSTEM_MAP, OMP | `ADAPT_THROUGH_EXISTING_OWNER` | Supports V7 owner map discipline. |
| SRE onboarding curriculum | LinkedIn | inconsistent operator capability | structured SRE skills path | faster productive engineers | not a production control | training progress | none | none | Basic | Strong for people/process | OMP / docs / onboarding | `ADAPT_THROUGH_EXISTING_OWNER` | Codex replacement requires human/operator capability too. |
| Production freeze/safety halt | Google error budget, AWS, Azure | unsafe change during instability | halt pipeline/promotions on alarms/budget | protects production | can block urgent fixes | alarms, SLO budget, health | Authority/OMP override | rollback/containment | Medium | Strong | OMP, Authority, CPS | `ADAPT_THROUGH_EXISTING_OWNER` | HOLD must run Owner Resolution. |
| AI/agent production mutation | Emerging AI SRE content | faster remediation | AI diagnoses and changes systems | speed | high risk, hallucination, accountability | full observability, audit, policy | strict Authority | rollback and kill switch | Very high | Weak today | OWNER_MAPPING_REQUIRED | `REJECT_FOR_V7` | Reject production mutation; allow read-only analyzers only after backtesting. |
