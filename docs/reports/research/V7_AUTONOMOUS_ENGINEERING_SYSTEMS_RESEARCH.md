# V7 Autonomous Engineering Systems Research

Status: `PERMANENT_CUMULATIVE_RESEARCH_KB`
Research program: `R3_AUTONOMOUS_ENGINEERING_SYSTEMS`
Created: 2026-07-05
Mode: `RESEARCH_ONLY`
Runtime impact: `NONE`
Planner impact: `NONE`
Authority impact: `NONE`
Production impact: `NONE`
Deployment performed: `NO`

## 1. Summary

R3 studies how mature engineering organizations automate engineering itself: repeated command chains, runbooks, documentation sync, testing, diagnosis, change governance, platform workflows, and AI-assisted engineering.

The strongest cross-industry pattern is:

```text
repeated manual work
  -> classify friction
  -> map owner
  -> create paved road / golden path
  -> encode as tested pipeline or analyzer
  -> gate by policy, telemetry, and rollback
  -> measure value and failure rate
  -> keep improving from real outcomes
```

For V7 this maps cleanly onto existing owners:

```text
Manual Action / Workflow
  -> Automation Audit / Workflow Audit
  -> Automation Debt / Workflow Debt
  -> OMP Mission
  -> SYSTEM_MAP owner lookup
  -> existing owner extension
  -> tests / regression / safe deploy when applicable
  -> Engineering Report
  -> Production Maturity / Current Program State synchronization
```

No research finding requires a new Runtime, Planner, Authority, OMP, truth source, execution path, or permanent Codex dependency.

Core conclusion:

```text
V7 should evolve from Codex-orchestrated engineering into owner-backed governed engineering pipelines.
```

## 2. Research History

| Date | Research program | Scope | Sources added | Organizations added | Sections changed | Conclusions changed | Open questions added | Files changed |
| --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| 2026-07-05 | `R3_AUTONOMOUS_ENGINEERING_SYSTEMS` | Initial cumulative research KB for engineering automation, self-improving platforms, IDP, AIOps, documentation, analyzer backtesting, AI-assisted engineering, and workflow automation. | 34 | Google, Amazon/AWS, Microsoft/Azure, Meta, Netflix, GitHub, Uber, LinkedIn, Spotify/Backstage, CNCF, Humanitec, Thoughtworks/Martin Fowler, DORA, Atlassian, PagerDuty, Stripe. | Sections 1-36 created. | Initial conclusions created; none superseded. | 14 | `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md` |

## 3. Scope

In scope:

- autonomous engineering systems;
- self-improving engineering platforms;
- internal developer platforms;
- golden paths and paved roads;
- service catalogs and ownership lookup;
- runbook-to-pipeline conversion;
- postmortem-to-mission conversion;
- automated testing and regression gates;
- safe deploy and rollback;
- automated documentation and knowledge maintenance;
- automated root cause analysis and analyzers;
- analyzer backtesting;
- AI-assisted engineering with guardrails;
- policy, compliance, and change gates;
- developer productivity and engineering intelligence;
- workflow automation and command minimization.

Out of scope:

- runtime failover implementation;
- V7 production movement;
- Authority expansion;
- new V7 owners;
- new execution paths;
- canonical document modification;
- implementation tasks.

## 4. Sources

Primary / high-value sources used:

1. Google Research, Tricorder: Building a Program Analysis Ecosystem: https://research.google/pubs/tricorder-building-a-program-analysis-ecosystem/
2. Google SRE, Automation at Google: https://sre.google/sre-book/automation-at-google/
3. Google SRE, Eliminating Toil: https://sre.google/sre-book/eliminating-toil/
4. Google SRE, Managing Incidents: https://sre.google/sre-book/managing-incidents/
5. Google SRE, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
6. Google SRE, Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
7. DORA Research Program: https://dora.dev/research/
8. DORA 2024 Report: https://dora.dev/research/2024/dora-report/
9. AWS Builders Library, Going Faster with Continuous Delivery: https://aws.amazon.com/builders-library/going-faster-with-continuous-delivery/
10. AWS Builders Library, Timeouts, Retries, and Backoff with Jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
11. AWS Builders Library, Load Shedding: https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/
12. AWS Systems Manager Incident Manager overview: https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html
13. Microsoft Azure Safe Deployment Practices: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments
14. Microsoft Azure Incident Response: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/incident-response
15. Microsoft Azure Enable Automation: https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/enable-automation
16. Meta Engineering, Facebook Infer: https://engineering.fb.com/2015/06/11/developer-tools/open-sourcing-facebook-infer-identify-bugs-before-you-ship/
17. Meta DrP automated investigations paper: https://arxiv.org/abs/2512.04250
18. Meta outage details, operational recovery lessons: https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/
19. Netflix Spinnaker continuous delivery: https://netflixtechblog.com/global-continuous-delivery-with-spinnaker-2a6896c23ba7
20. Netflix Kayenta automated canary analysis: https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69
21. Netflix Chaos Engineering Upgraded: https://netflixtechblog.com/chaos-engineering-upgraded-878d341f15fa
22. GitHub Actions concepts: https://docs.github.com/en/actions/get-started/understand-github-actions
23. GitHub Copilot productivity research: https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/
24. GitHub Copilot controlled experiment paper: https://arxiv.org/abs/2302.06590
25. GitHub Copilot longitudinal case study: https://arxiv.org/abs/2509.20353
26. Spotify Backstage overview: https://backstage.io/docs/overview/what-is-backstage/
27. Backstage Software Catalog descriptor format: https://backstage.io/docs/features/software-catalog/descriptor-format/
28. CNCF Platforms Working Group: https://tag-app-delivery.cncf.io/wgs/platforms/
29. Humanitec Internal Developer Platform definition: https://humanitec.com/blog/what-is-an-internal-developer-platform
30. Platform Engineering overview: https://platformengineering.org/blog/what-is-platform-engineering
31. Martin Fowler / Thoughtworks, platform as internal product: https://martinfowler.com/articles/talk-about-platforms.html
32. Uber Domain-Oriented Microservice Architecture: https://www.uber.com/blog/microservice-architecture/
33. LinkedIn School of SRE: https://linkedin.github.io/school-of-sre/
34. Atlassian Incident Postmortems: https://www.atlassian.com/incident-management/postmortem

Secondary or cautionary sources:

- Humanitec and PlatformEngineering.org are vendor/community sources. Use for terminology and IDP patterns, not as sole authority for V7 production semantics.
- AI productivity sources show mixed evidence and must be treated as bounded assistance evidence, not autonomy authority.

## 5. Organizations Reviewed

| Organization / source family | Relevance to R3 | V7 use |
| --- | --- | --- |
| Google | SRE automation, toil, Tricorder static analysis, DORA research. | Automation Debt, analyzer integration, engineering productivity measurement. |
| Amazon / AWS | Pipelines, mechanized best practices, single-threaded ownership, safety gates. | Safe deploy pipeline and owner-backed workflow conversion. |
| Microsoft / Azure | Safe deployments, incident response, automation guidance. | Progressive exposure, rollback, and operational readiness gates. |
| Meta | Infer static analyzer, DrP automated investigations, outage recovery. | Owner Resolution analyzers and analyzer backtesting. |
| Netflix | Spinnaker, Kayenta, controlled chaos. | Governed pipelines, canary evidence, automated judgment with visibility. |
| GitHub | Actions, reusable workflows, Copilot research. | Workflow automation and AI-assisted engineering boundaries. |
| Uber | Domain-oriented ownership, gateways, complexity reduction. | SYSTEM_MAP owner granularity and platform boundaries. |
| LinkedIn | SRE curriculum and toil reduction education. | Capability onboarding and operator curriculum. |
| Spotify / Backstage | Developer portal, catalog, templates, TechDocs. | SYSTEM_MAP-backed service catalog and docs-as-code model. |
| CNCF | Platform working group and maturity models. | Platform maturity and self-service governance. |
| Humanitec | IDP definition and platform-as-product patterns. | Secondary IDP vocabulary; owner-backed pipelines. |
| Thoughtworks / Martin Fowler | Platform as internal product, paved road constraints. | Avoid platform-as-helpdesk and start from proven needs. |
| DORA | Software delivery, platform engineering, AI, documentation, user-centricity. | Measurement model and warnings against metric misuse. |
| Atlassian / PagerDuty | Incident and postmortem workflow. | Postmortem-to-mission flow, but not direct V7 truth source. |
| Stripe | Online migrations and engineering discipline. | Incremental, reversible change and evidence-first migration mindset. |

## 6. Engineering Automation Principles

1. Automate repeated, valuable, understood work first.
2. Keep humans in business, policy, exceptional risk, and architectural boundaries.
3. Do not automate low-value activity just because it is repetitive.
4. Embed automation into the developer/operator workflow where work already happens.
5. Prefer owner-backed pipelines over personal scripts.
6. Instrument automation with success, failure, latency, rollback, and adoption metrics.
7. Backtest analyzers against historical evidence before allowing them to block or mutate.
8. Treat documentation as synchronized knowledge, not the source of execution authority.
9. Treat AI as assistant or analyzer until evidence proves a narrower certified role.
10. Make the paved road easier than the ad-hoc road, but preserve explicit exception paths.

## 7. Platform Engineering And Internal Developer Platforms

Mature platform engineering reduces engineering toil by creating an internal product for common engineering workflows. Backstage emphasizes a centralized software catalog, templates, and docs; Humanitec defines IDP as a toolchain bound together to pave golden paths; CNCF frames platforms as indirect value-stream accelerators.

For V7:

- OMP is not an IDP UI, but it is the execution program equivalent.
- SYSTEM_MAP is the current owner lookup equivalent.
- Current Program State is the volatile status equivalent.
- Production Maturity is the capability/maturity consumer.
- Engineering Reports are evidence, not a platform database.

V7 should not create an external IDP before it has owner-backed pipelines. The first IDP-like capability should be internal: a governed OMP pipeline for repeated certification/deploy/report/state synchronization workflows.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 8. Golden Path / Paved Road Models

Golden paths work when:

- they solve a frequent high-friction workflow;
- they preserve autonomy for teams that need exceptions;
- they are maintained as a product;
- they include documentation, templates, observability, ownership, and support;
- adoption is easier than custom reinvention.

For V7:

```text
Golden path = governed owner-backed workflow
Paved road = certified command-minimized pipeline
```

Examples:

- controlled certification phase execution;
- safe deploy + convergence + certification resume;
- engineering report + consumer synchronization;
- owner resolution forensic workflow;
- regression certification after existing owner changes.

Classification: `ADOPT_NOW` for identifying candidates; `ADAPT_THROUGH_EXISTING_OWNER` for implementation.

## 9. Service Catalog And Ownership Models

Backstage catalog entities include metadata, owner, lifecycle, system, relations, and status. Uber DOMA shows that ownership must be grouped around domains and gateways, not just individual microservices. SYSTEM_MAP already owns V7 owner lookup and must remain the owner for V7 service catalog semantics.

For V7:

- do not create a second service catalog;
- extend SYSTEM_MAP projections if needed;
- every Automation Candidate and Pipeline Candidate must include owner, artifact, consumer, status, and evidence;
- use Current Program State for volatile state, not SYSTEM_MAP.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 10. Runbook-To-Pipeline Models

Google SRE and AWS converge on the same principle: manual operational steps should be converted into automation when they are repeated, understood, and safe. Amazon mechanized release best practices into pipeline checks after discovering ad-hoc communication did not ensure adoption.

For V7:

```text
Runbook
  -> Workflow Audit
  -> Pipeline Candidate
  -> owner mapping
  -> tests
  -> governed pipeline
  -> certification when production-affecting
```

Do not convert a runbook into a pipeline until its owner, inputs, outputs, stop conditions, rollback/containment, and evidence are explicit.

Classification: `ADOPT_NOW` for audit; `ADAPT_THROUGH_EXISTING_OWNER` for pipeline execution.

## 11. Postmortem-To-Mission Models

Atlassian and Google SRE postmortem practice emphasizes learning and follow-up action. R3's V7 interpretation is stricter:

```text
Postmortem action
  -> OMP Mission
  -> owner mapping
  -> implementation or policy decision
  -> verification
  -> evidence
  -> maturity/state synchronization
```

A postmortem action must not remain a report-only TODO. It becomes either Automation Debt, Workflow Debt, Owner Resolution work, policy work, or canonical impossibility.

Classification: `ADOPT_NOW`.

## 12. Automated Testing And Regression Models

Mature organizations embed unit, integration, pre-production, static, security, and deployment verification into pipelines. Amazon states that every pipeline step should increase confidence; Meta Infer demonstrates high-value incremental static analysis inside review; Google Tricorder shows a scalable program-analysis ecosystem integrated into developer workflow.

For V7:

- every owner-backed pipeline needs regression tests;
- every analyzer needs historical fixture tests;
- Engineering Reports can become analyzer fixtures;
- production certification still requires real production evidence;
- synthetic tests prove code semantics, not production capability.

Classification: `ADOPT_NOW`.

## 13. Progressive Delivery Models

Amazon, Azure, Netflix, and DORA converge on progressive rollout:

```text
small exposure
  -> observe
  -> health gate
  -> promote / halt / rollback
  -> increase exposure
```

V7 already has the controlled production certification ladder:

```text
1 -> 5 -> 10 -> 25 -> 50 -> FULL_INCIDENT
```

R3 finding: engineering automation should use the same ladder mindset. A new pipeline begins as read-only or single-use, then expands only after evidence.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 14. Safe Deploy And Rollback Models

Safe deploy systems share these properties:

- build artifact identity;
- automated tests;
- deployment gates;
- alarms and metrics;
- progressive exposure;
- automatic or operator-approved rollback;
- post-deploy validation.

For V7 engineering automation:

- pipelines that modify code or production must preserve commit, artifact, command, owner, test, deploy, convergence, and rollback evidence;
- no pipeline may bypass safe deploy;
- no documentation sync may claim deploy success.

Classification: `ADOPT_NOW`.

## 15. Automated Documentation And Knowledge Models

Backstage TechDocs and docs-as-code patterns keep docs near code and catalog entries. DORA finds documentation quality amplifies technical capability. V7 already separates durable canonical owners from Engineering Reports.

For V7:

```text
Engineering Report
  -> durable conclusion extraction
  -> canonical owner sync when required
  -> Current Program State sync when volatile state changed
  -> Production Maturity sync when maturity-affecting
```

Automated documentation must not write canonical truth without owner rules. It can detect staleness, propose updates, generate diffs, and validate links.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 16. Automated Root Cause Analysis Models

Meta DrP is the strongest R3 source: automated investigation playbooks written as analyzers, integrated with alerts and incident management, executed at scale, and measured for MTTR reduction. For V7, the analog is:

```text
Owner Resolution Analyzer
  -> consumes Engineering Reports / artifacts / logs
  -> produces root cause candidate
  -> classifies owner and field
  -> remains read-only until certified
```

R3 warning: analyzer output must not become truth before backtesting and owner consumption.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 17. Analyzer Backtesting Models

Netflix Kayenta archives canary inputs and results so new judges can be run on historical data. Google Tricorder and Meta Infer emphasize developer workflow integration and high signal quality. V7 should treat Engineering Reports, production payloads, test fixtures, and historical blockers as analyzer backtesting corpora.

Required V7 analyzer backtesting fields:

- analyzer version;
- input artifact list;
- expected root cause;
- actual root cause;
- precision / false positive;
- recall / false negative;
- owner mapping correctness;
- no-mutation guarantee;
- regression result.

Classification: `ADOPT_NOW`.

## 18. AIOps / AI-Assisted Engineering Models

Credible AI evidence is mixed:

- GitHub's controlled Copilot experiment showed faster completion for a narrow coding task.
- DORA 2024 reports AI productivity benefits but warns of tradeoffs in stability and throughput.
- Later studies caution that activity metrics and subjective productivity can diverge.

V7 rule:

```text
AI may assist investigation, drafting, code review, test generation, and analyzer proposal.
AI may not grant Authority, mutate production, approve Runtime Apply, or become truth.
```

AI-assisted work must be measured by owner-consumed outcomes, not by output volume.

Classification: `ADAPT_THROUGH_EXISTING_OWNER` for assistant/analyzer roles; `REJECT_FOR_V7` for autonomous mutation authority.

## 19. Policy, Compliance, And Guardrail Models

GitHub Actions, Azure deployments, AWS pipelines, and Backstage catalogs all show guardrails embedded in workflows:

- permissions;
- approvals;
- protected environments;
- reusable workflows;
- artifact identity;
- policy checks;
- audit logs;
- rollback.

For V7:

- Authority is the policy gate for production action;
- Production Maturity consumes evidence;
- OMP routes missions;
- SYSTEM_MAP maps owners;
- pipelines may automate orchestration but not policy decisions.

Classification: `ADOPT_NOW`.

## 20. Toil Reduction Models

Google SRE's toil model is directly relevant. V7 should classify repeated manual engineering tasks by:

- manual;
- repetitive;
- automatable;
- tactical;
- no enduring value;
- grows with system size.

V7 already has Automation Debt and Workflow Debt. R3 adds the research-backed reason: debt reduction must target high-value recurring work, not simply reduce human touch for its own sake.

Classification: `ADOPT_NOW`.

## 21. Developer Productivity And Maturity Models

DORA, SPACE-like research, and platform engineering sources agree that productivity is multidimensional. Activity counts alone are unsafe.

For V7 engineering automation, useful metrics are:

- manual command count per mission;
- repeated workflow count;
- workflow lead time;
- test/regression time;
- failure/retry rate;
- rollback/correction rate;
- report-to-canonical-sync latency;
- analyzer precision/recall;
- operator interruption count;
- certification phase cycle time;
- automation debt created/closed;
- workflow debt created/closed;
- capability earned.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 22. Self-Service Infrastructure Models

Self-service is safe only when the platform owns the boundaries. Humanitec and Backstage emphasize developer self-service, RBAC, templates, environment management, and catalog-backed context.

For V7:

```text
self-service = owner-bounded command / pipeline
```

Good V7 self-service examples:

- "run Phase 4 certification" pipeline after authority and pool readiness are satisfied;
- "safe deploy requested-source fix" pipeline with tests/convergence;
- "generate Owner Resolution report from operation_id" read-only analyzer.

Bad V7 self-service examples:

- "move users now" without Authority;
- "mark maturity complete" without Production Maturity;
- "write canonical docs from report" without owner rule.

Classification: `ADAPT_THROUGH_EXISTING_OWNER`.

## 23. Self-Improving System Patterns

Self-improving systems use feedback loops:

```text
observe friction
  -> classify debt
  -> propose improvement
  -> implement through owner
  -> verify
  -> measure outcome
  -> update maturity/state
```

V7's target model already matches this. R3 adds concrete external parallels:

- Tricorder: ecosystem for program analysis in workflow.
- Infer: incremental static analysis with high fix rate.
- DrP: analyzer playbooks at incident scale.
- Kayenta: archived inputs and reusable judges.
- Backstage: catalog + templates + docs.
- AWS Pipelines: mechanized best practices.

Classification: `ADOPT_NOW`.

## 24. Anti-Patterns

| Anti-pattern | Why it fails | V7 stance |
| --- | --- | --- |
| Personal script becomes production pipeline. | No owner, test, rollback, or audit. | `REJECT_FOR_V7` |
| AI agent mutates production from chat. | No Authority, identity lock, verification, or rollback contract. | `REJECT_FOR_V7` |
| Documentation drives capability. | Reality must produce capability first. | `REJECT_FOR_V7` |
| Metrics used to punish individuals. | Gaming and burnout; DORA warns against misuse. | `REJECT_FOR_V7` |
| Platform team as helpdesk. | Bottleneck persists; no self-service product. | `REJECT_FOR_V7` |
| Portal without backend ownership. | Pretty UI over broken workflow. | `REJECT_FOR_V7` |
| Analyzer blocks execution before backtesting. | False positives become outages. | `REJECT_FOR_V7` |
| Runbooks stay manual forever. | Repeated toil remains unclassified. | `REJECT_FOR_V7` |
| Pipeline ignores rollback. | Automation amplifies failures. | `REJECT_FOR_V7` |
| Golden path is mandatory for every exception. | Blocks legitimate expert work. | `REJECT_FOR_V7` |

## 25. Comparison Against V7 Autonomous Operating System

| External pattern | V7 AOS equivalent | Status |
| --- | --- | --- |
| Internal Developer Platform | OMP + SYSTEM_MAP + CPS + existing owners | Conceptually aligned, implementation partial. |
| Golden path | Governed owner-backed workflow | Canonical concept present as Pipeline Candidate. |
| Service catalog | SYSTEM_MAP owner lookup | Present; could be projected better. |
| Engineering automation debt | Automation Debt | Present. |
| Workflow orchestration debt | Workflow Debt / Pipeline Candidate | Present. |
| Automated RCA | Owner Resolution Analyzer | Target implied, implementation future. |
| Analyzer backtesting | Regression over Engineering Reports | Needs implementation. |
| Automated docs | Report-to-canonical sync proposal | Needs implementation. |
| AI assistant | Temporary accelerator, not authority | Present in AOS law. |
| Platform maturity | Production Maturity + OMP | Present. |

## 26. Practices V7 Should Adopt

1. Toil classification using Google SRE criteria.
2. Pipeline Candidate for every repeated engineering workflow.
3. Analyzer backtesting against Engineering Reports.
4. Postmortem/action item conversion into OMP Mission.
5. Safe deploy pipeline identity and rollback evidence as mandatory.
6. Progressive rollout for engineering automation itself.
7. Service/owner catalog projection from SYSTEM_MAP.
8. DORA-style outcome metrics at workflow level, not individual scoring.
9. AI assistance only with evidence and review gates.
10. Documentation staleness detection as read-only analyzer.

## 27. Practices V7 Should Adapt Through Existing Owners

1. Backstage-like catalog: adapt through SYSTEM_MAP and CPS, not a new portal.
2. IDP: adapt through OMP and existing owners, not a new platform owner.
3. Tricorder/Infer: adapt as read-only analyzers and code review/test gates.
4. DrP: adapt as Owner Resolution analyzers.
5. Kayenta: adapt as certification/analyzer backtesting over archived evidence.
6. GitHub Actions: adapt as CI/engineering workflow execution, not production authority.
7. AWS best-practice checks: adapt as OMP/pipeline gates.
8. Azure safe deployment: adapt through safe deploy/convergence owners.
9. Uber DOMA: adapt as owner/domain grouping in SYSTEM_MAP.
10. Humanitec platform orchestrator concept: adapt as OMP pipeline orchestration only after owner boundaries are explicit.

## 28. Practices V7 Should Reject

1. New IDP/portal as a substitute for owner-backed pipeline implementation.
2. AI-generated changes deployed without existing owner review and tests.
3. AI or analyzer output treated as canonical truth.
4. Activity metrics used as productivity truth.
5. Broad self-service production mutation.
6. Platform team/helpdesk model where Codex remains permanent operator.
7. Runbook conversion without rollback/containment.
8. Documentation sync as a blocker after capability is already earned, unless a safety owner proves dependency.
9. Workflow automation that bypasses Authority, Restore Barrier, Runtime, Verification, or Production Maturity.
10. Creating new owners before SYSTEM_MAP/OMP owner discovery proves necessity.

## 29. Practices V7 Should Defer

1. Fully autonomous code-writing implementation agents.
2. Automatic canonical reference rewriting.
3. Automatic Authority expansion from analyzer output.
4. Production mutation by AI assistant.
5. Multi-repo IDP portal.
6. AI-driven architecture refactoring.
7. Self-healing engineering workflow that patches and deploys without human review.
8. Analyzer blocking of certification before backtesting matures.
9. Automatic migration of all runbooks into pipelines.
10. Full engineering intelligence dashboard until owner-backed data is reliable.

## 30. Proposed Additions To V7_AUTONOMOUS_OPERATING_SYSTEM.md

Do not update the canonical document in this research mission.

Candidate additions for future owner-approved sync:

- Define `Engineering Golden Path` as a governed owner-backed workflow.
- Define `Analyzer Backtesting` as mandatory before an analyzer can block or recommend mutation.
- Clarify that AI-assisted engineering remains `CODEX_ASSISTED` or `SCRIPTED` until owner-backed pipeline evidence exists.
- Add `Codex Exit Strategy`: repeated Codex workflows must become Pipeline Candidates or intentionally manual work.

## 31. Proposed Additions To OMP

Do not update OMP in this research mission.

Candidate additions:

- OMP should maintain an Engineering Automation backlog view derived from Automation Debt and Workflow Debt, without becoming a second implementation backlog.
- OMP should classify repeated prompt patterns as Pipeline Candidates.
- OMP should route analyzer creation through existing owners and require historical report regression.
- OMP should record whether each manual workflow ended as `PIPELINE_IMPLEMENTED`, `INTENTIONALLY_MANUAL`, `NOT_COST_EFFECTIVE`, `BLOCKED_BY_FUTURE_CAPABILITY`, or `CANONICAL_IMPOSSIBILITY`.

## 32. Proposed Additions To Current Program State / Autonomy Inventory

Do not update Current Program State in this research mission.

Candidate fields:

- current_engineering_automation_level;
- current_pipeline_candidates;
- current_analyzer_candidates;
- automation_debt_current;
- workflow_debt_current;
- synchronization_debt_current;
- codex_dependency_current;
- repeated_manual_workflows_top_5;
- next_pipeline_candidate;
- analyzer_backtesting_readiness.

## 33. Proposed Additions To Production Maturity

Do not update Production Maturity in this research mission.

Candidate maturity dimensions:

- Engineering Automation Evidence;
- Workflow Pipeline Evidence;
- Analyzer Reliability Evidence;
- Documentation Synchronization Reliability;
- Codex Dependency Reduction;
- Self-Service Governance Safety;
- AI-Assisted Engineering Safety.

Production Maturity must remain a consumer, not a producer or approver.

## 34. Proposed Additions To SYSTEM_MAP / Owner Mapping

Do not update SYSTEM_MAP in this research mission.

Candidate owner mapping rows:

| Concept | Existing owner candidate | Notes |
| --- | --- | --- |
| Engineering Golden Path | OMP + SYSTEM_MAP + existing implementation owner | No new owner unless OMP cannot represent pipeline candidate. |
| Analyzer Backtesting | Engineering Reports + OMP + affected owner tests | Needs test fixture convention. |
| Documentation Staleness Analyzer | Document Lifecycle + Canonical Reference + OMP | Read-only first. |
| Prompt-to-Pipeline Conversion | OMP + Workflow Audit + Implementation Backlog if code required | Codex dependency reduction. |
| Service Catalog Projection | SYSTEM_MAP + CPS | Projection only, not second truth. |
| Engineering Automation Metrics | Production Maturity + CPS + OMP | Consumer-only metrics. |

## 35. Open Questions

1. Which repeated V7 Codex workflow should be the first owner-backed pipeline: safe deploy, certification phase execution, owner resolution, or report synchronization?
2. What exact Engineering Report schema is stable enough to become analyzer fixtures?
3. Should analyzer fixtures live beside tests, reports, or a generated fixture index?
4. Which existing test owner should run analyzer backtesting?
5. What precision/recall threshold is required before an Owner Resolution analyzer may influence OMP decisions?
6. Which manual actions are intentionally manual due to Authority or policy?
7. What is the minimum service catalog projection V7 needs before a Backstage-like portal would add value?
8. How should V7 measure Codex dependency reduction without creating vanity metrics?
9. Which documentation staleness checks can be automated safely without writing canonical docs?
10. Can Current Program State expose an Autonomy Inventory without becoming a queue?
11. How should AI cost, latency, and hallucination risk be measured for V7 engineering automation?
12. Should V7 add an "analyzer confidence" field to Engineering Reports or keep it in test outputs?
13. What is the safe promotion ladder for engineering automation pipelines themselves?
14. Which workflow debt items are not cost-effective to automate at V7's current scale?

## 36. Final Engineering Verdict

Verdict:

```text
R3_AUTONOMOUS_ENGINEERING_SYSTEMS_KB_CREATED
```

Research conclusion:

```text
V7 should not automate engineering by creating a new AI operator or IDP.
V7 should automate engineering by converting repeated Codex/admin workflows into tested, owner-backed, evidence-preserving OMP pipelines.
```

Strongest immediate adoption:

- classify repeated manual actions using Automation Debt;
- classify repeated command chains using Workflow Debt;
- create Pipeline Candidates for certification/deploy/report/state-sync workflows;
- create read-only Owner Resolution analyzers;
- backtest analyzers on Engineering Reports;
- preserve AI as assistant, not authority.

Strongest rejection:

- AI production mutation;
- AI canonical truth writing;
- portal before owner-backed pipeline;
- metric-driven individual productivity scoring;
- analyzer decisions without backtesting;
- broad self-service that bypasses Authority or Runtime gates.

## Appendix A. Practice Classification Matrix

| Practice | Organization/source | Problem solved | Mechanism | Benefits | Risks | Required telemetry | Required evidence | Required authority or approval | Required rollback/containment | Required maturity level | V7 compatibility | Existing V7 owner mapping | Recommended V7 classification | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Toil classification | Google SRE | Repeated manual work hides as normal ops. | Classify manual/repetitive/automatable/tactical work. | Focuses automation on high-value work. | Over-automation of rare work. | Manual action log, frequency, duration. | Workflow history. | OMP classification. | Not applicable for read-only classification. | Low. | Strong. | OMP, Automation Debt. | `ADOPT_NOW` | V7 already has Automation Debt. |
| Golden path | Backstage, Humanitec, Fowler | Engineers repeat complex toolchains. | Paved owner-backed workflow with templates/docs/support. | Reduces cognitive load and drift. | Can become rigid or helpdesk. | Adoption, success/failure, exception rate. | Pipeline evidence. | OMP and affected owner. | Stop/rollback per action class. | Medium. | Strong if owner-bounded. | OMP, Workflow Debt, Pipeline Candidate. | `ADAPT_THROUGH_EXISTING_OWNER` | V7 should implement workflows, not a new portal first. |
| Service catalog | Backstage | Ownership and context are hard to find. | Catalog entities, owners, relations, lifecycle, status. | Faster routing and fewer ownerless tasks. | Second truth source. | Catalog freshness, owner coverage. | Owner map source. | SYSTEM_MAP owner. | Not applicable. | Low/medium. | Strong. | SYSTEM_MAP, CPS. | `ADAPT_THROUGH_EXISTING_OWNER` | SYSTEM_MAP already owns lookup. |
| Runbook-to-pipeline | Google SRE, AWS | Repeated runbook execution remains toil. | Convert steps into tested workflow. | Consistency and speed. | Pipeline can amplify bad operation. | Runbook frequency, failure, rollback. | Tests and dry-run evidence. | OMP + affected owner. | Required if mutating. | Medium. | Strong. | OMP, Workflow Audit. | `ADOPT_NOW` | Direct match to Workflow Debt. |
| Postmortem-to-mission | Google, Atlassian | Lessons remain documents. | Convert action items into owned missions. | Closes learning loop. | Low-value action sprawl. | Postmortem actions, closure status. | Report + owner consumption. | OMP. | Depends on mission. | Low. | Strong. | Engineering Reports, OMP. | `ADOPT_NOW` | V7 forbids report-only completion. |
| Static analysis in review | Google Tricorder, Meta Infer | Bugs found late. | Incremental analyzer comments in workflow. | Earlier defects, lower review load. | False positives slow developers. | Warning fix rate, false positive rate. | Analyzer regression fixtures. | Code owner / CI owner. | Not applicable unless auto-fix. | Medium. | Strong for code. | Tests, CI, OMP. | `ADAPT_THROUGH_EXISTING_OWNER` | Read-only first; block only after evidence. |
| Automated RCA analyzers | Meta DrP | Incidents require manual diagnosis. | Playbooks/analyzers run against artifacts. | Lower MTTR and toil. | Misclassification. | Precision, recall, latency, coverage. | Historical report backtesting. | OMP / Owner Resolution. | Read-only until certified. | Medium/high. | Strong. | Owner Resolution, Engineering Reports. | `ADAPT_THROUGH_EXISTING_OWNER` | Needs backtesting before authority. |
| Analyzer backtesting | Netflix Kayenta, Google analysis ecosystem | Analyzer quality unknown. | Replay historical inputs and compare expected outcomes. | Safe analyzer evolution. | Fixture drift. | Expected/actual, false pos/neg. | Fixture corpus. | Test owner. | Not applicable. | Medium. | Strong. | Tests, Engineering Reports. | `ADOPT_NOW` | Critical before analyzer decisions. |
| Progressive delivery | AWS, Azure, Netflix, DORA | Large changes create high blast radius. | Canary, cells, health gates, rollback. | Lower risk. | Slow if over-gated. | Metrics, alarms, canary score. | Stage evidence. | Safe deploy owner / Authority. | Required. | Medium. | Strong. | Safe deploy, Certification Program. | `ADAPT_THROUGH_EXISTING_OWNER` | V7 ladder already mirrors it. |
| Automated canary analysis | Netflix Kayenta | Manual graph judgment is slow/unreliable. | Baseline/canary metric comparison and score. | Reusable, auditable decisions. | Bad metrics cause bad judgment. | Metric coverage, score, NODATA. | Archived metric inputs. | Deploy owner. | Rollback on failed score. | High. | Medium/strong. | Certification, Production Maturity. | `DEFER_UNTIL_CAPABILITY_EXISTS` | Needs stable metric corpus. |
| Mechanized best-practice checks | AWS Pipelines | Best practices spread inconsistently. | Warnings/gates inside pipeline. | Adoption and consistency. | One-size-fits-all gates. | Check pass/fail, override, adoption. | Check rationale. | OMP / owner policy. | Depends on gate. | Medium. | Strong. | OMP, CI, safe deploy. | `ADAPT_THROUGH_EXISTING_OWNER` | Per-owner configurability required. |
| Docs-as-code / TechDocs | Backstage | Docs stale and hard to find. | Docs live with code/catalog. | Discoverability and maintenance. | Docs treated as truth. | Link freshness, last update, owner. | Source file + owner. | Canonical owner. | Not applicable. | Medium. | Strong if read-only first. | Document Lifecycle, Canonical Reference. | `ADAPT_THROUGH_EXISTING_OWNER` | Must not bypass canonical owners. |
| Documentation staleness analyzer | DORA, Backstage-inspired | Canonical docs drift from reality. | Detect outdated references, broken links, missing consumer sync. | Less manual sync. | False stale claims. | Link checks, report references, owner timestamps. | Analyzer output. | Document owner. | Not applicable. | Medium. | Strong. | Document Lifecycle, OMP. | `ADOPT_NOW` | Read-only analyzer is safe. |
| Internal developer platform | Backstage, Humanitec, CNCF | Tool sprawl and cognitive load. | Self-service platform product. | Faster, safer workflows. | Portal without backend value. | Workflow usage, lead time, failure. | Owner-backed workflow evidence. | OMP / SYSTEM_MAP. | Per action. | Medium/high. | Partial. | OMP, SYSTEM_MAP, CPS. | `DEFER_UNTIL_CAPABILITY_EXISTS` | Build pipelines first. |
| Domain/gateway ownership | Uber DOMA | Microservice/platform complexity. | Domains, layers, gateways, extension points. | Lower coupling, clearer ownership. | Over-architecture. | Dependency graph, owner churn. | SYSTEM_MAP mapping. | Architecture/owner approval. | Not applicable. | Medium. | Medium. | SYSTEM_MAP. | `RESEARCH_MORE` | Useful pattern, but V7 scale may not need full DOMA. |
| Reusable workflow automation | GitHub Actions | Repeated CI/CD commands. | YAML workflows, jobs, actions, events, runners. | Standard automation. | Secrets and runner risk. | Run history, logs, artifacts. | CI results. | Repo owner. | Workflow cancel/rollback. | Low/medium. | Strong. | CI/test owners. | `ADAPT_THROUGH_EXISTING_OWNER` | Good for engineering, not production authority. |
| AI code assistance | GitHub Copilot research | Repetitive coding burden. | AI suggestions and task assistance. | Speed, flow, lower cognitive load. | Quality, maintenance, hallucination. | Acceptance, defects, review rework, tests. | Human-reviewed commit evidence. | Code owner. | Revert/rollback via git/deploy. | Medium. | Strong as assistant. | Codex temporary assistant, CI/tests. | `ADAPT_THROUGH_EXISTING_OWNER` | Assistant only, not authority. |
| AI autonomous mutation | Vendor/agentic claims | Attempts to remove engineers from changes. | Agent writes/runs/deploys. | Potential speed. | Unsafe mutation, hidden assumptions. | Full trace, tests, rollback, owner review. | Not sufficient today. | Would need explicit Authority. | Mandatory. | Very high. | Weak. | None clear. | `REJECT_FOR_V7` | Violates No Codex Dependency and Authority laws. |
| Developer productivity metrics | DORA, SPACE-like research | Need to see bottlenecks. | Outcome, flow, quality, satisfaction metrics. | Better investment decisions. | Metric gaming. | Lead time, failure, MTTR, survey, quality. | Aggregated trends. | OMP / Production Maturity. | Not applicable. | Medium. | Strong. | Production Maturity, CPS. | `ADAPT_THROUGH_EXISTING_OWNER` | Avoid individual scoring. |
| Self-service infra | Backstage, Humanitec, GitHub Actions | Ticket ops and wait states. | Templates, RBAC, environment workflows. | Lower wait and coordination. | Unsafe self-service. | Request success, time, policy violations. | Owner-approved workflow. | Owner/RBAC/Authority. | Per workflow. | Medium/high. | Partial. | OMP, SYSTEM_MAP, safe deploy. | `DEFER_UNTIL_CAPABILITY_EXISTS` | Needs stable pipelines first. |
| Engineering intelligence dashboards | DORA, EngThrive-style research | Manual status synthesis. | Aggregate telemetry and surveys. | Finds bottlenecks. | Vanity metrics. | Multi-source metrics. | Data quality evidence. | OMP / CPS. | Not applicable. | Medium. | Partial. | CPS, Production Maturity, Dashboard. | `RESEARCH_MORE` | Useful after data reliability improves. |
