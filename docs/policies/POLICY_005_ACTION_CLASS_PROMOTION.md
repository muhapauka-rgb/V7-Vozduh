# POLICY_005_ACTION_CLASS_PROMOTION

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: action class promotion
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for action class promotion.

Action class promotion means moving a repeated operational capability from manual/governed use toward broader automation only after evidence proves it is safe at the next scope.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Production systems should not jump from one successful action to broad autonomy.

They promote behavior through stages: preview, test, canary, limited rollout, monitored rollout, broader rollout, certification, and rollback-ready operation.

The difficulty is deciding how much evidence is enough, what failure stops promotion, and how to demote after bad outcomes.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Operational capabilities should be promoted progressively from small bounded exposure to broader scope. | `STRONG` | Google SRE, Kubernetes Deployments, Argo Rollouts, Flagger, AWS CodeDeploy, Azure safe deployment, Cloudflare edge practice, network pilots | `HIGH`: broad across SRE, cloud, orchestrator, progressive delivery, and network operations | None for high-risk production change. |
| Promotion requires verification evidence and stop/rollback/abort criteria before expansion. | `STRONG` | Google SRE, AWS CodeDeploy alarms/rollback, Kubernetes rollout status, Argo analysis, Azure rings | `HIGH`: strong production case and platform evidence | None for mature systems. |
| One successful canary is not sufficient proof for unbounded promotion. | `STRONG` | Google SRE canarying, progressive delivery controllers, Azure rings, network staged rollout | `HIGH`: broad safe-deployment practice | None for high-risk production systems. |
| Canary, ring, or small-batch stages are common promotion mechanisms. | `MEDIUM` | Google SRE, Argo, Flagger, AWS CodeDeploy, Azure, Cloudflare, network pilots | `MEDIUM_HIGH`: widespread but terminology and mechanics differ | Some systems use blue/green or all-at-once for low-risk changes. |
| Automated promotion from metrics is common when metrics are reliable and rollback is ready. | `MEDIUM` | Argo Rollouts, Flagger, AWS CodeDeploy alarms, Kubernetes controllers | `MEDIUM`: strong in deployment systems, less universal in network operations | Human review remains common for authority expansion. |
| Deployment all-at-once is valid only for low-risk or already isolated scopes. | `WEAK` | AWS CodeDeploy supports all-at-once, some simple deployment systems | `MEDIUM`: documented, but contrary to safety-first high-risk patterns | Progressive systems prefer canary/linear/rings. |

### Industry Consensus Research

#### Google SRE / Release Engineering

SRE release practices use canaries, progressive rollout, monitoring, error budgets, and rollback. Promotion is evidence-driven and tied to production health.

- Purpose: expose changes to small blast radius before broad rollout.
- Existing production approaches: canary, staged rollout, SLO/error-budget monitoring, rollback, postmortem learning.
- Known patterns: start small, measure real impact, expand gradually, stop on regression.
- Known failure patterns: canary misses hidden segment, metrics lag, rollback is not fast enough.
- Known recovery patterns: halt rollout, rollback, learn from incident.
- Known tradeoffs: slow rollout reduces risk but delays benefit.
- Known limitations: canary quality depends on representative traffic.

#### Kubernetes Deployments

Kubernetes Deployments use desired state, rollout status, rolling update, max unavailable, max surge, progress deadline, pause/resume, and rollback.

- Purpose: promote new ReplicaSet gradually while preserving service.
- Existing production approaches: rolling updates, rollout history, rollback, readiness gates.
- Known patterns: bounded unavailable capacity, progress monitoring, declared desired state.
- Known failure patterns: rollout stuck, unavailable Pods, bad readiness.
- Known recovery patterns: rollout undo, pause, fix manifest.
- Known tradeoffs: rollout parameters shape risk and speed.
- Known limitations: Deployment success is infrastructure-level, not full product correctness.

#### Argo Rollouts / Flagger / Progressive Delivery

Progressive delivery controllers automate canary or blue-green promotion with analysis runs, metrics checks, and rollback/abort behavior.

- Purpose: make promotion explicit and measurable.
- Existing production approaches: canary steps, weight increments, automated analysis, abort, rollback.
- Known patterns: promotion gate, metric analysis, stepwise traffic increase.
- Known failure patterns: analysis inconclusive, metric source stale, bad canary cohort.
- Known recovery patterns: abort rollout and return traffic to stable version.
- Known tradeoffs: automation depends on correct metric selection.
- Known limitations: controller can automate promotion mechanics, not guarantee policy correctness.

#### AWS CodeDeploy

CodeDeploy supports in-place, blue/green, canary, linear, all-at-once, CloudWatch alarm integration, automatic rollback, and deployment lifecycle events.

- Purpose: promote deployments through controlled traffic shift and alarms.
- Existing production approaches: deployment configurations, alarms, automatic rollback, blue/green.
- Known patterns: alarm-gated promotion, rollback on failure, deployment lifecycle hooks.
- Known failure patterns: failed alarm, bad hook, unhealthy replacement.
- Known recovery patterns: rollback and redeploy.
- Known tradeoffs: canary/linear safer than all-at-once but slower.
- Known limitations: alarm quality defines promotion quality.

#### Azure Safe Deployment Practices

Azure public safe-deployment guidance emphasizes rings, health signals, telemetry, gradual exposure, rollback, and stopping on unexpected signals.

- Purpose: reduce customer impact by staged exposure.
- Existing production approaches: deployment rings, health gates, telemetry, rollback.
- Known patterns: internal, canary, region/ring expansion.
- Known failure patterns: regional difference, latent regression, telemetry gap.
- Known recovery patterns: stop rollout, rollback, isolate affected ring.
- Known tradeoffs: many rings increase operational complexity.
- Known limitations: public guidance is broad; exact internal thresholds vary.

#### Cloudflare / Edge Rollout Practice

Cloudflare production systems commonly emphasize gradual rollout, edge observability, per-colo impact control, and quick rollback in public engineering material.

- Purpose: reduce global-edge blast radius.
- Existing production approaches: staged edge rollout, observability, feature flags, rollback.
- Known patterns: small-scope test before global exposure.
- Known failure patterns: region/colo-specific behavior.
- Known recovery patterns: disable feature or rollback.
- Known tradeoffs: worldwide networks require geography-aware promotion.
- Known limitations: public details vary by product.

#### Service Mesh / Load Balancers

Envoy/Istio/Linkerd and LBs support traffic splitting, route weights, canary releases, retries, circuit breakers, and metric-driven promotion when integrated with controllers.

- Purpose: shift traffic by policy and observe outcomes.
- Existing production approaches: weighted routing, route-level metrics, outlier detection, retries/timeouts.
- Known patterns: traffic weight increments and metric checks.
- Known failure patterns: hidden user segment, stateful traffic mismatch.
- Known recovery patterns: shift traffic back to stable route.
- Known tradeoffs: route-level promotion is powerful but needs compatible app semantics.
- Known limitations: L7 routing cannot solve every lower-layer failure.

#### Network Operations / SD-WAN

Network promotion often means moving from lab to maintenance window, pilot site, limited region, wider estate, and default policy. SD-WAN policies are often rolled out by site, application, transport, or risk class.

- Purpose: avoid fleet-wide routing incidents.
- Existing production approaches: pilot group, staged site rollout, configuration validation, rollback config.
- Known patterns: limit first exposure, observe, expand, retain rollback.
- Known failure patterns: site-specific underlay, provider differences, route leak.
- Known recovery patterns: config rollback or route withdrawal.
- Known tradeoffs: network changes need careful blast-radius boundaries.
- Known limitations: vendor tooling differs.

#### Academic / Safety Engineering

Control theory and distributed systems favor staged rollout and feedback loops when system response is uncertain. Promotion without feedback can destabilize a system.

- Purpose: learn system response before expanding control.
- Existing production approaches: feedback control, bounded experiments, guardrails.
- Known patterns: observe, decide, act, verify, adjust.
- Known failure patterns: positive feedback loop, unmodeled state.
- Known recovery patterns: stop, revert, lower authority.
- Known tradeoffs: exploration is useful only inside bounded risk.
- Known limitations: academic abstractions require operational evidence.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Manual promotion vs automated promotion | Evidence quality and risk tolerance differ. | Manual review catches context; automation reduces latency and toil. | Manual for authority expansion; automated for certified bounded stages with strong metrics. |
| Time-based soak vs metric-based advancement | Some risks appear only over time; others are visible in health metrics. | Soak is simple but slow; metrics are faster but can miss hidden failures. | Combine for high-risk action classes. |
| Canary vs blue/green vs ring rollout | Systems expose traffic differently. | Canary is gradual; blue/green is fast rollback; rings handle geography/cohorts. | Choose based on traffic control and blast-radius unit. |
| Promotion after success vs repeated success | Single success may not generalize. | Faster promotion gains value; repeated evidence lowers risk. | Repeat evidence before expanding authority or blast radius. |

### Industry Disagreement Research

1. Manual promotion versus automated promotion.
   Some environments require human approval per stage; progressive-delivery controllers can promote automatically based on metrics.

2. Time-based soak versus metric-based advancement.
   Some systems wait for fixed windows; others advance on explicit health/error signals.

3. Canary representativeness.
   A canary may be safe for one cohort but not the full population.

4. Promotion after success versus promotion after repeated success.
   Most mature systems require repeated or broad evidence for larger blast radius.

5. Demotion rules.
   Some systems automatically rollback; others freeze and require human review.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: OMP, `build_action_class_runtime_enablement_model`, `tools/v7-autonomy-trust-evidence-inventory`, governed dry-run, trust/learning stores;
- evidence: action-class ladder exists, current first class `GOVERNED_ONLY`, next state `CERTIFIED_FOR_CLASS_APPROVAL`, runtime automation `NO`, missing evidence list is explicit.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: promote progressively from small bounded exposure. | `FULLY_IMPLEMENTED` | OMP, action-class ladder. | Ladder covers one-user, two-user, five-user, class-specific and pool-level stages. | Reuse ladder and OMP promotion evaluation. | `CONFIGURATION_ONLY`: keep state current. |
| CS2: promotion requires verification and stop/rollback/abort criteria. | `PARTIALLY_IMPLEMENTED` | Runtime eligibility, rollback, verification, learning. | Required evidence is modeled; real class-level certification is missing. | Reuse eligibility and rollback owners. | `MODERATE_EXTENSION`: close real outcomes and certify. |
| CS3: one canary is not proof for unbounded promotion. | `FULLY_IMPLEMENTED` | OMP promotion rules. | Runtime enablement blocks promotion with missing evidence and authority boundary. | Reuse current blocker model. | None. |
| CS4: canary/ring/small-batch stages are common. | `PARTIALLY_IMPLEMENTED` | Action-class ladder. | Small-batch stages exist as states; broader ring mechanics are not implemented. | Reuse ladder if V7 needs small-batch. | `SMALL_EXTENSION`: implement next class when evidence exists. |
| CS5: automated metric promotion when metrics reliable and rollback ready. | `PARTIALLY_IMPLEMENTED` | Trust/confidence, freshness, rollback, eligibility. | Metrics/readiness are exposed but policy is not approved and runtime apply disabled. | Reuse trust/evidence inventory. | `MODERATE_EXTENSION`: certify metric reliability. |
| CS6: all-at-once valid only for low-risk/isolated scopes. | `FULLY_IMPLEMENTED` | OMP, blast-radius gates. | V7 does not permit unbounded all-at-once promotion; authority expansion is explicit. | Reuse blast-radius gates. | None. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `70%` |
| Reuse potential | `95%` |
| Missing coverage | `30%` |
| Complexity of remaining work | `MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `REUSE`.

Action-class promotion directly matches V7's authority evolution model. The implementation need is not a new promotion owner; it is real outcome closure, certification evidence, and OMP authority recommendations.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Progressive promotion from small bounded exposure. | `YES` | `REUSE` | OMP already owns action-class ladder and one-user governed canary. | OMP, action-class ladder. | Keep state current in OMP/backlog. | `NONE` | Very high: path to autonomy. | `A6` |
| Promotion requires verification and stop/rollback/abort criteria. | `YES` | `REUSE` | Evidence model exists; class-level certification is missing. | Runtime eligibility, rollback, verification, learning. | Close real outcomes and certify per class. | `MODERATE_EXTENSION` | Very high: unlocks safe promotion. | `A3` |
| One canary is not proof for unbounded promotion. | `YES` | `REUSE` | Existing blockers prevent broad promotion. | OMP promotion rules. | Preserve representativeness rule. | `NONE` | High: prevents overfitting to one success. | `A4` |
| Canary/ring/small-batch stages. | `YES` | `ADAPT` | V7 should express rings as action classes/user counts, not deployment rings. | Action-class ladder. | Implement next class only after evidence. | `SMALL_EXTENSION` | High: supports scale progression. | `B12` |
| Automated metric promotion. | `YES_LATER` | `ADAPT` | Metrics can recommend promotion after reliability certification; they cannot grant authority alone. | Trust/confidence, freshness, rollback, eligibility. | Certify metric reliability and stop at authority boundary. | `MODERATE_EXTENSION` | High: reduces operator workload over time. | `B13` |
| All-at-once only for low-risk isolated scopes. | `YES` | `REUSE_DONE_READ_ONLY` | V7 forbids unbounded promotion without authority expansion and now verifies the boundary through C4. | OMP, blast-radius gates, `admin_core.autonomy_trust_acceleration`. | `all_at_once_promotion_unavailable_verification` keeps all-at-once/direct promotion unavailable for current classes. | `NONE` | Medium: preserves safety. | `C4` |

Need New Owner: `FALSE`.

## V7 Adaptation

`RESEARCH_PENDING`.

## Why V7 Differs

`RESEARCH_PENDING`.

## Runtime Behavior

`RESEARCH_PENDING`.

## Authority Behavior

`RESEARCH_PENDING`.

## Safety

`RESEARCH_PENDING`.

## Verification

`RESEARCH_PENDING`.

## Rollback

`RESEARCH_PENDING`.

## Learning

`RESEARCH_PENDING`.

## Implementation Owner

Existing V7 owners must be reused.
Potential owner mapping must be proven during later lifecycle stages.

## Certification State

`RESEARCH_PENDING`.

World research is complete.
Consensus detection is pending.
V7 adaptation is pending.
Implementation is forbidden until later lifecycle stages permit it.

## References

- Google SRE, Release Engineering: https://sre.google/sre-book/release-engineering/
- Google SRE, Canarying Releases: https://sre.google/workbook/canarying-releases/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Argo Rollouts: https://argoproj.github.io/argo-rollouts/
- Flagger progressive delivery: https://docs.flagger.app/
- AWS CodeDeploy deployment configurations: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html
- AWS CodeDeploy rollback: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
- Azure safe deployment practices: https://learn.microsoft.com/en-us/devops/operate/safe-deployment-practices
- Istio traffic management: https://istio.io/latest/docs/concepts/traffic-management/
- Envoy traffic splitting via routing: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_routing

## Open Questions

- Which promotion stages survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which metrics qualify as promotion evidence versus observation only?
- Which failure causes demotion rather than temporary stop?
