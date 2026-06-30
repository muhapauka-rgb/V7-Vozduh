# Autonomous Execution Discovery

Status: research artifact
Owner: evidence only; canonical rules live in `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md`
Date: 2026-06-30

## Executive Summary

Mature production systems do not treat autonomous execution as "run without humans."

They treat it as bounded control-loop execution:

```text
intent / desired state
  -> observed state
  -> policy and safety gates
  -> bounded action
  -> continuous verification
  -> rollback / containment / suspension
  -> learning
```

The strongest reusable ideas for V7 are:

1. autonomous circuit breakers and automatic suspension;
2. explicit execution budgets and execution windows;
3. separated decision, execution, verification, rollback, and learning confidence;
4. health-check quorum and consecutive-failure thresholds;
5. reconciliation/idempotency contracts;
6. operator override and kill-switch contracts;
7. metric-driven promotion abort;
8. all-targets-degraded fallback semantics;
9. drift detection between desired state and production reality;
10. compact autonomy health read-models.

Most of these concepts already exist in V7 partially under Runtime Model, Decision Model, OMP, Movement Protection, Work Placement Law, and the Autonomous Execution Program. The research therefore recommends strengthening the existing autonomous execution reference, not creating new architecture.

## Industry Survey

| System family | Production pattern | Key lesson for V7 |
| --- | --- | --- |
| Google SRE | Automation is valuable for consistency, speed, MTTR reduction, and scale, but thoughtless automation can make problems worse; scoped automation and autonomous systems are the target. | V7 should certify scope before execution and add automatic suspension when automation degrades safety. |
| Google Borg | Desired-state scheduling, automatic restart/rescheduling, production-scale control loops. | V7 should preserve desired-state reconciliation and idempotent control-loop behavior. |
| Kubernetes | Controllers reconcile desired and observed state; probes/readiness/self-healing separate health from execution. | V7 should keep Runtime thin and ensure readiness/liveness gates remain live before mutation. |
| Envoy | Outlier detection ejects unhealthy upstreams with thresholds and ejection timers; circuit breaking limits damage. | V7 should model autonomy circuit breakers, ejection-like cooldown, and confidence decay. |
| Istio | Traffic shifting and routing rules support progressive migration. | V7 should keep canary/promotion ladders and metric-based abort semantics. |
| Linkerd | Retries/timeouts are policy-bounded and observable. | V7 should treat retry/rollback/recovery as bounded safety behaviors, not hidden loops. |
| AWS Route 53 / ARC | Health checks, routing controls, failover, CloudWatch alarms, and operator-controlled recovery routing. | V7 should separate health evidence from routing authority and preserve operator kill switches. |
| Azure Traffic Manager | Configurable probes, tolerated failures, endpoint states, DNS TTL, multiple probe locations, degraded endpoint removal, and all-degraded fallback. | V7 should use health quorum/failure thresholds and explicit all-targets-degraded behavior. |
| Cloudflare Load Balancing | Steering policies, health monitors, pool/origin selection, traffic steering. | V7 should separate target selection policy from live health verification. |
| Argo Rollouts / Flagger | Progressive delivery with analysis metrics and automatic abort/rollback. | V7 should add metric-driven promotion abort for autonomous action classes. |
| HashiCorp Consul | Service discovery, health checks, resolvers, failover policy, service intentions. | V7 should preserve policy-bound target selection and service suitability as gates. |
| Cilium | Policy-enforced service mesh/Gateway API, eBPF datapath, Envoy integration, observability. | V7 should keep enforcement points explicit and read models compact. |
| Cisco / Juniper / Arista / VMware NSX | Intent-based networking, assurance, config transaction/change control, rollback, validation, closed-loop operations. | V7 should keep intent, policy, assurance, transaction, and rollback separate but connected. |
| Netflix | Chaos engineering and progressive delivery emphasize resilience validation, automated rollback, and confidence before broad rollout. | V7 should use production evidence and rollback learning to mature autonomy. |
| Meta / large control planes | Large-scale systems favor incremental state, compact read models, and operational guardrails. | V7 should avoid exhaustive enumeration as a permanent autonomy blocker. |

## Concept Catalog

| Concept | Problem solved | Implementation pattern | Strengths | Weaknesses / failure modes | V7 classification |
| --- | --- | --- | --- | --- | --- |
| Autonomous circuit breaker | Automation can amplify bad decisions. | Disable or downgrade autonomy after failure rate, rollback rate, or incident threshold. | Prevents runaway automation. | Over-sensitive breaker may block useful repair. | DIRECTLY REUSABLE |
| Automatic suspension | A certified action class may become unsafe after production drift. | OMP/autonomy health marks class suspended until review. | Keeps certification live, not permanent fantasy. | Requires accurate health read-model. | DIRECTLY REUSABLE |
| Execution budget | Prevents too much automation in a window. | Max actions/users/blast/risk per time window. | Bounds damage and load. | Too low budget slows recovery. | DIRECTLY REUSABLE |
| Execution window | Limits autonomous action to safe periods or incident windows. | Only execute during approved temporal/incident context. | Reduces business risk. | May delay repair. | REUSABLE WITH ADAPTATION |
| Confidence decomposition | One confidence number hides risk. | Separate decision, execution, verification, rollback, learning confidence. | Explains why stop happened. | More fields to maintain. | DIRECTLY REUSABLE |
| Health quorum | Single probe can lie. | Multiple probes/thresholds/consecutive failures. | Reduces false positives. | Slower detection. | DIRECTLY REUSABLE |
| Consecutive failure threshold | Avoids reacting to transient noise. | N failures before unhealthy. | Stable detection. | Increases detection latency. | ALREADY PRESENT / STRENGTHEN |
| Canary analysis abort | Promotion should stop on bad metrics. | Analysis metrics fail -> abort/rollback/suspend. | Prevents scaling bad actions. | Needs reliable metrics. | DIRECTLY REUSABLE |
| Kill switch | Human must be able to stop automation immediately. | Global/class/policy disable gate. | Simple safety backstop. | Can become permanent manual dependency. | DIRECTLY REUSABLE |
| Operator override | Operator can reject/override recommendation/action state. | Override recorded as learning signal. | Human risk judgment preserved. | Can conflict with autonomy metrics. | DIRECTLY REUSABLE |
| Desired-state drift detection | Production can drift from policy. | Compare desired state to observed state continuously. | Detects silent divergence. | Requires clean desired-state model. | ALREADY PRESENT / STRENGTHEN |
| Idempotent reconciliation | Repeated control-loop runs should not duplicate action. | Same intent + same material state -> same no-op or same decision. | Safe retries. | Requires stable identity. | ALREADY PRESENT / STRENGTHEN |
| All-targets-degraded fallback | Sometimes no good target exists. | Best safe target, acceptable target, restore minimum service, stay, incident. | Avoids worse moves. | Hard to score "less bad" safely. | ALREADY PRESENT / STRENGTHEN |
| No hidden retries | Automation loops can create oscillation. | One execution attempt per transaction unless certified retry class exists. | Prevents runaway movement. | May require human follow-up. | DIRECTLY REUSABLE |
| Incident automation state | Actions during incident need separate context. | Incident mode can alter escalation/reporting without expanding authority. | Better operator visibility. | Could become hidden authority if misused. | REUSABLE WITH ADAPTATION |
| Risk score / safety score split | Risk and confidence are different. | Risk score blocks; confidence informs. | Prevents high-confidence unsafe action. | Requires clear semantics. | ALREADY PRESENT / STRENGTHEN |
| Adaptive autonomy downgrade | Certification can decay after evidence worsens. | Health metrics downgrade action class state. | Keeps autonomy honest. | Needs explicit thresholds. | DIRECTLY REUSABLE |
| Promotion hold | Metrics are good but insufficiently fresh/representative. | OMP holds promotion pending evidence. | Prevents premature autonomy. | Can feel slow. | ALREADY PRESENT |
| Service intent isolation | Service policy must constrain routing. | Intentions/policies before target selection. | Prevents technically valid but product-wrong moves. | Policy errors can block recovery. | ALREADY PRESENT |
| Read-model compaction | Runtime must not scan long histories. | Store raw once; consume summaries. | Scales. | Summaries may hide anomalies. | ALREADY PRESENT |

## Comparison Matrix

| Production practice | Common systems | V7 current state | Gap |
| --- | --- | --- | --- |
| Desired-state reconciliation | Kubernetes, Borg, intent-based networking | Present in Runtime/Decision Model | Strengthen autonomy-specific wording |
| Progressive canary | Istio, Argo, Flagger, Cloudflare, AWS/Azure routing | Present in OMP ladder | Add metric-driven abort wording |
| Health thresholds/quorum | AWS, Azure, Envoy, Kubernetes | Present but scattered | Strengthen as autonomy health input |
| Circuit breaker/auto suspension | Envoy, SRE practice, rollout systems | Partial through STOP_SAFE/downgrade | Add explicit autonomy suspension rule |
| Execution budgets | Cloud control planes, rollout systems | Partial via blast radius | Add time/window/action budget language |
| Kill switch/operator override | AWS ARC, SRE, networking change control | Partial through authority/operator | Add explicit override/kill-switch contract |
| Idempotent reconciliation | Kubernetes/controllers/Borg | Present in Decision Commit work | Add as autonomy rule |
| All-degraded fallback | Azure Traffic Manager, LB systems | Present as graceful degradation | Keep and strengthen |
| Learning loop | SRE, Netflix, V7 | Present | No new owner needed |

## Gap Analysis

Real gaps or under-specified areas:

1. Autonomous circuit breaker and automatic suspension are not yet explicit enough in the Autonomous Execution Program.
2. Execution budgets exist semantically through blast radius, but the program should name action/time/risk budgets.
3. Confidence is currently captured, but the program should separate decision confidence from execution, verification, rollback, and learning confidence.
4. Operator override and kill switch should be first-class safety contracts.
5. Metric-driven promotion abort should be explicit.
6. Health quorum/failure threshold should be named as a source of autonomy health, not authority.

Non-gaps:

1. V7 already has Runtime/Planner/Decision separation.
2. V7 already has OMP certification and action-class promotion.
3. V7 already has graceful degradation.
4. V7 already has terminal outcome learning.
5. V7 already has Work Placement Law and thin Runtime.
6. V7 already has progressive blast-radius ladder.

## Concepts Already Present In V7

- certified action classes;
- OMP certification;
- Runtime execute-or-stop;
- thin Runtime;
- Work Placement Law;
- Decision != Execution;
- terminal outcome classification;
- rollback/no-rollback semantics;
- Engineering Intelligence as recommendation-only;
- production maturity;
- representative production evidence;
- graceful degradation;
- autonomy health read-models;
- no duplicate owners;
- no synthetic evidence.

## Missing Concepts

Missing as explicit autonomous execution rules:

- autonomous circuit breaker;
- automatic suspension/downgrade;
- execution budgets beyond blast radius;
- execution windows;
- confidence decomposition;
- operator override/kill switch;
- metric-driven promotion abort;
- health quorum/failure-threshold interpretation.

## Potential Improvements

| Improvement | V7 owner mapping | Architecture impact |
| --- | --- | --- |
| Add automatic suspension rule | OMP + Autonomous Execution Program + Production Maturity | None |
| Add execution budgets | OMP + Policy 006 + Runtime Model | None |
| Add confidence decomposition | Engineering Intelligence + Production Maturity | None |
| Add operator override/kill switch | OMP + Authority policy | None |
| Add metric-driven promotion abort | OMP + Engineering Intelligence + certification | None |
| Add health quorum wording | Runtime Model + evidence/read-model owners | None |

## Architecture Compatibility

All recommended additions are compatible with current V7 architecture because they:

- reuse OMP for certification and promotion;
- reuse Runtime Model for execute-or-stop;
- reuse Decision Model for decision semantics;
- reuse Engineering Intelligence for prediction/recommendation;
- reuse Production Maturity for health and maturity;
- reuse Policy 004/005/006/007/008/009 for authority, promotion, blast radius, rollback, freshness, and anti-flap;
- do not create a new Runtime, Planner, Governance layer, authority owner, truth source, or policy system.

## OMP Compatibility

Compatible. OMP already owns:

- certification;
- promotion;
- stop conditions;
- capability maturity;
- production maturity;
- current next action.

The additions strengthen OMP's ability to downgrade/suspend autonomy and reject promotion when metrics are unsafe.

## Runtime Compatibility

Compatible. Runtime remains thin.

Runtime consumes:

- certified action class;
- authority envelope;
- execution budget status;
- kill-switch/override state;
- health/freshness/readiness gates;
- prepared confidence read-models.

Runtime does not compute broad confidence, grant authority, or perform research.

## Decision Model Compatibility

Compatible. Confidence decomposition extends explanation of decisions without changing decision semantics.

## Engineering Intelligence Compatibility

Compatible. Engineering Intelligence may:

- compute confidence components;
- detect bad trends;
- recommend suspension;
- recommend promotion abort;
- explain operator override impact.

Engineering Intelligence still may not grant authority or certification.

## Recommended Additions

Add to `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md`:

1. Industry-Derived Safety Additions.
2. Autonomous Circuit Breaker and Suspension.
3. Execution Budgets and Windows.
4. Confidence Decomposition.
5. Operator Override and Kill Switch.
6. Metric-Driven Promotion Abort.
7. Health Quorum and Failure Threshold Rule.
8. Reconciliation and Idempotency Rule.

## Recommended Rejections

| Concept | Reason rejected |
| --- | --- |
| Copying vendor controller architecture | Would duplicate V7 Runtime/Planner/OMP owners. |
| Always-on autonomous daemon as default | Violates current certification and authority gates. |
| ML-only autonomous decision making | Not explainable enough and would duplicate planner/decision owners. |
| Exhaustive user-channel enumeration as certification | Contradicts Product Scale Objectives and representative evidence model. |
| Automatic authority expansion | Violates Policy Authority and OMP certification rules. |
| Hidden multi-step retries inside Runtime | Risks oscillation and violates one-transaction/terminal-outcome semantics. |

## References

- Google SRE, "The Evolution of Automation at Google": https://sre.google/sre-book/automation-at-google/
- Google Borg paper: https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/
- Kubernetes Pod Lifecycle / self-healing concepts: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Envoy outlier detection: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier
- Istio traffic shifting: https://istio.io/latest/docs/tasks/traffic-management/traffic-shifting/
- Linkerd retries and timeouts: https://linkerd.io/2.18/features/retries-and-timeouts/
- AWS Route 53 health checks and DNS failover: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
- Azure Traffic Manager endpoint monitoring: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Cloudflare Load Balancing traffic steering: https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/
- Argo Rollouts analysis: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
- HashiCorp Consul service resolver: https://developer.hashicorp.com/consul/docs/connect/config-entries/service-resolver
- Cilium Gateway API / policy-enforced service mesh: https://docs.cilium.io/en/stable/network/servicemesh/gateway-api/gateway-api/
