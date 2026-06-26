# POLICY_006_BLAST_RADIUS

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: blast radius
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for blast radius.

Blast radius means the maximum population, traffic share, region, service set, channel set, provider set, or operational scope that one action can affect.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Failures become incidents when one action affects too much of the system.

Mature systems reduce blast radius through cells, zones, regions, namespaces, pools, target groups, canaries, traffic weights, quotas, rate limits, RBAC scopes, failure domains, and progressive rollout.

Blast radius must be designed before automation expands.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Production actions must have a bounded blast radius before automation or broad rollout. | `STRONG` | Google SRE, AWS, Azure, GCP, Kubernetes, Envoy/Istio, Cloudflare, routing/SD-WAN, HAProxy/NGINX | `HIGH`: broad across every mature family researched | None for high-risk production action. |
| Blast radius is expressed in the system's native scope: traffic share, users, endpoints, zones, regions, namespaces, pools, routes, services, or authority scope. | `STRONG` | Cloud providers, Kubernetes, service mesh, Cloudflare, routing, load balancers, IAM/RBAC | `HIGH`: broad evidence with different units | None for scope-specific expression. |
| Progressive expansion and small initial exposure reduce production risk. | `STRONG` | Google SRE canarying, AWS CodeDeploy, Azure rings, Kubernetes, Argo, network pilots | `HIGH`: repeated safe-deployment evidence | None for risky changes. |
| Isolation domains are common safety boundaries. | `MEDIUM` | AWS AZ/region, Azure/GCP zones/regions, Kubernetes namespaces/quotas/PDBs, VRFs/areas, Cloudflare zones/pools | `MEDIUM_HIGH`: widespread but architecture-specific | Shared dependencies can cross isolation boundaries. |
| Traffic weights are common where the system can split traffic. | `MEDIUM` | Istio, Envoy, Argo, CodeDeploy, Cloudflare, LBs | `MEDIUM_HIGH`: common in L7/LB/deployment systems | Routing protocols and DNS may use different mechanisms. |
| Local repair is a specialized blast-radius reducer for network paths. | `WEAK` | MPLS FRR, routing operations | `MEDIUM`: strong network evidence only | Application/cloud systems often use pool/region/ring scopes. |

### Industry Consensus Research

#### Google SRE / Cell-Based Operation

Google SRE material emphasizes capacity isolation, overload control, cascading-failure prevention, canaries, and avoiding global impact from local failure.

- Purpose: keep local failures local.
- Existing production approaches: capacity planning, load shedding, gradual rollout, traffic isolation, canarying.
- Known patterns: small initial exposure, monitor, expand, stop on bad signals.
- Known failure patterns: cascading failure after traffic shifts to insufficient capacity.
- Known recovery patterns: reduce traffic, shed load, restore capacity gradually.
- Known tradeoffs: isolation costs capacity and complexity.
- Known limitations: shared dependencies can pierce isolation boundaries.

#### AWS

AWS uses regions, availability zones, target groups, Auto Scaling groups, IAM scopes, deployment groups, CodeDeploy traffic shifting, and service quotas to bound action scope.

- Purpose: prevent one change or failure from affecting every user.
- Existing production approaches: AZ/region isolation, target group health, canary/linear deployments, alarms, rollback.
- Known patterns: region/AZ, target group, deployment group, IAM scope.
- Known failure patterns: regional incident, AZ impairment, all-at-once deployment, overbroad IAM.
- Known recovery patterns: failover, rollback, replacement, capacity scaling.
- Known tradeoffs: multi-AZ/region improves resilience but can increase cost.
- Known limitations: shared control-plane dependencies can still cause broad impact.

#### Azure / GCP

Azure and GCP use regions, zones, resource groups/projects, managed instance groups, load-balancing backends, Traffic Manager/Cloud Load Balancing, policy scopes, and safe deployment rings.

- Purpose: constrain impact by resource and geography.
- Existing production approaches: zones/regions, projects/subscriptions, policy scopes, endpoint groups, rings.
- Known patterns: hierarchical scopes and regional failover.
- Known failure patterns: zone outage, regional degradation, bad deployment ring.
- Known recovery patterns: traffic steering, rollback, scale/replacement.
- Known tradeoffs: global services require cross-region design.
- Known limitations: DNS failover and control plane delays affect exact boundary.

#### Kubernetes

Kubernetes uses namespaces, labels, selectors, PodDisruptionBudgets, rollout parameters, quotas, taints/tolerations, topology spread constraints, and controllers.

- Purpose: bound disruption to a workload, namespace, or replica budget.
- Existing production approaches: PDBs, max unavailable, max surge, namespaces, quotas.
- Known patterns: declare allowed disruption before mutation.
- Known failure patterns: too many Pods unavailable, bad selector, cluster-wide controller error.
- Known recovery patterns: rollback Deployment, restore replicas, adjust budget.
- Known tradeoffs: strict budgets preserve availability but can block maintenance.
- Known limitations: PDBs do not protect from all voluntary/involuntary failures.

#### Envoy / Istio / Service Mesh

Service mesh systems bound impact with traffic weights, subsets, circuit breakers, outlier ejection limits, retry budgets, and route policies.

- Purpose: limit traffic exposed to a degraded route or new behavior.
- Existing production approaches: weighted routing, destination subsets, max ejection percent, min health percent, circuit breakers.
- Known patterns: traffic percentage as blast-radius control.
- Known failure patterns: retry amplification, too many ejections, bad subset.
- Known recovery patterns: shift weights back, reduce ejection, rollback policy.
- Known tradeoffs: more granular routing needs accurate service topology.
- Known limitations: shared upstream dependencies can violate local route assumptions.

#### Cloudflare / Global Edge

Cloudflare bounds impact by zone, pool, origin, region, steering policy, WAF/product configuration, and edge rollout scope.

- Purpose: keep traffic steering and product changes scoped.
- Existing production approaches: pools, monitors, fallback pools, per-zone/product config, gradual edge rollout.
- Known patterns: endpoint/pool-level health and geography-aware steering.
- Known failure patterns: fallback pool overload, monitor misconfiguration, regional edge issue.
- Known recovery patterns: revert config, change pool weight, restore monitor.
- Known tradeoffs: global edge requires multiple vantage points.
- Known limitations: all-pool unhealthy cases can force degraded choices.

#### Network Routing / SD-WAN / MPLS

Network systems use routing domains, VRFs, areas, levels, route policy, prefix limits, local repair, TE constraints, and SD-WAN policies to bound impact.

- Purpose: avoid route leaks and fleet-wide path instability.
- Existing production approaches: BGP prefix limits, OSPF/IS-IS areas/levels, MPLS FRR local repair, VRFs, route maps, SD-WAN site groups.
- Known patterns: local repair before global reconvergence, policy scopes, prefix filters.
- Known failure patterns: route leak, bad redistribution, global failover loop.
- Known recovery patterns: withdraw bad route, rollback config, reroute locally.
- Known tradeoffs: more segmentation improves safety but increases operational complexity.
- Known limitations: underlay failures can cross policy domains.

#### HAProxy / NGINX

Load balancers bound impact through server pools, weights, max connections, health checks, slow start, and traffic distribution.

- Purpose: prevent one backend or pool from receiving unsafe load.
- Existing production approaches: weights, maxconn, server groups, health checks, slow start.
- Known patterns: traffic share and connection limits.
- Known failure patterns: overload remaining servers after removing one backend.
- Known recovery patterns: reweight or slow-start recovered backend.
- Known tradeoffs: static weights may not match dynamic capacity.
- Known limitations: backend groups may share hidden dependencies.

#### Academic / Resilience Engineering

Bulkheads, circuit breakers, isolation domains, quorum systems, and bounded experiments are common resilience patterns.

- Purpose: prevent correlated failure from spreading.
- Existing production approaches: isolation boundaries, rate limits, quorum, circuit breakers.
- Known patterns: bounded scope before action.
- Known failure patterns: shared dependency collapse, retry storm, control-loop feedback.
- Known recovery patterns: isolate, shed, revert, re-admit gradually.
- Known tradeoffs: isolation can reduce efficiency.
- Known limitations: hidden coupling is hard to model.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| User count vs traffic percentage vs infrastructure scope | Systems control different units of exposure. | User counts are product-visible; traffic weights are flexible; infra scopes align with failure domains. | Pick the unit the runtime can enforce and verify. |
| Static limits vs dynamic capacity-aware limits | Current capacity changes over time. | Static limits are simple; dynamic limits are safer but need fresh evidence. | Static for first safety floors; dynamic for mature autonomy. |
| Local repair vs global coordination | Local repair is fast; global coordination sees capacity and dependencies. | Local repair minimizes outage but can hide systemic risk. | Local repair for path protection; global coordination for user/product movement. |
| Isolation vs efficiency | Strong isolation preserves safety but can strand capacity. | More isolation lowers blast radius but costs resources and complexity. | High-value production autonomy needs explicit isolation tradeoff. |

### Industry Disagreement Research

1. Geography-based versus user-based blast radius.
   Cloud and edge systems use regions/zones; product systems may use cohorts or users.

2. Traffic percentage versus entity count.
   Service meshes use traffic weight; operations may use users, hosts, pools, or services.

3. Static boundaries versus dynamic capacity-aware boundaries.
   Fixed limits are simple; dynamic limits account for current capacity but require fresher evidence.

4. Local repair versus global policy.
   MPLS FRR and routing local repair reduce latency but can hide broader system conditions.

5. Isolation versus efficiency.
   More cells/zones/quotas reduce impact but can strand capacity.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: planner/autoswitch move budgets, restore barrier, action-class ladder, blast evidence materialization, risk-tier floors;
- evidence: one-user governed blast boundary exists; blast confidence exists in trust model, but class-level certification is missing for autonomous enablement.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: production actions need bounded blast radius. | `FULLY_IMPLEMENTED` | Planner/autoswitch, restore barrier, action-class ladder. | One-user and move-count bounds exist; runtime automation disabled until certification. | Reuse blast/action-class gates. | `CONFIGURATION_ONLY`: bind canonical policy. |
| CS2: blast radius expressed in native scope. | `PARTIALLY_IMPLEMENTED` | Planner, capacity/load, action-class ladder. | Users and move-count are explicit; traffic/service/pool scopes are partial. | Reuse capacity and service owners. | `MODERATE_EXTENSION`: add service/pool/cohort scope where needed. |
| CS3: progressive expansion reduces risk. | `FULLY_IMPLEMENTED` | OMP maturity ladder, action-class promotion. | Progressive states and authority boundaries are present. | Reuse OMP. | None. |
| CS4: isolation domains are common safety boundaries. | `PARTIALLY_IMPLEMENTED` | Group policy, org policy placeholders, planner gates. | Group/user policy exists; org identity/policy integration is incomplete. | Reuse existing policy files and identity owners. | `MODERATE_EXTENSION`: complete org/cohort isolation. |
| CS5: traffic weights are common where traffic can split. | `NOT_IMPLEMENTED` | Planner/autoswitch can be extended. | V7 currently moves users/channels; weighted traffic split is not a current owner behavior. | Reuse planner only if fit analysis requires weights. | `DOCUMENTATION_ONLY`: determine applicability. |
| CS6: local repair is specialized network blast reduction. | `NOT_IMPLEMENTED` | None required for current scope. | V7 does not implement MPLS-style local repair. | Reuse route/planner owners only if needed. | `DOCUMENTATION_ONLY`: likely non-applicable. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `62%` |
| Reuse potential | `90%` |
| Missing coverage | `38%` |
| Complexity of remaining work | `MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `ADAPT`.

Blast-radius practice fits V7, but the blast unit must be V7-native: users, channels, services, cohorts, pools, provider/country scope, and authority class rather than generic traffic percentage only.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bounded blast radius for production actions. | `YES` | `REUSE` | One-user and move-count bounds already exist. | Planner/autoswitch, restore barrier, action-class ladder. | Bind canonical policy to class bounds. | `NONE` | Very high: prevents overreach. | `A5` |
| Native scope expression. | `YES` | `ADAPT` | V7 needs service/pool/cohort scope in addition to users and move count. | Planner, capacity/load, action-class ladder. | Add service/pool/cohort scope where needed. | `MODERATE_EXTENSION` | High: enables safer scale. | `B14` |
| Progressive expansion. | `YES` | `REUSE` | OMP and promotion ladder already encode this. | OMP maturity ladder, action-class promotion. | Continue via action-class promotion. | `NONE` | Very high: autonomy path. | `A6` |
| Isolation domains. | `YES` | `ADAPT` | Group/user policy exists; org/cohort isolation is incomplete. | Group policy, org policy placeholders, planner gates. | Complete org/cohort isolation. | `MODERATE_EXTENSION` | High: needed for multi-tenant scale. | `B11` |
| Traffic weights. | `PARTIAL` | `REJECT_FOR_NOW` | V7 currently moves users/channels; weighted splitting is not current owner behavior. | Planner/autoswitch can be extended if future scope requires it. | Defer until product requires split traffic. | `NONE` | Optional. | `D5` |
| Local repair. | `NO_FOR_CURRENT_SCOPE` | `REJECT` | MPLS-style local repair is outside current V7 abstraction. | None required. | Keep as future substrate option. | `NONE` | Optional. | `D1` |

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

- Google SRE, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/
- Google SRE, Canarying Releases: https://sre.google/workbook/canarying-releases/
- AWS Well-Architected Reliability Pillar: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html
- AWS CodeDeploy deployment configurations: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html
- Azure safe deployment practices: https://learn.microsoft.com/en-us/devops/operate/safe-deployment-practices
- Google Cloud architecture framework, reliability: https://cloud.google.com/architecture/framework/reliability
- Kubernetes PodDisruptionBudgets: https://kubernetes.io/docs/tasks/run-application/configure-pdb/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Envoy circuit breakers: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking
- Istio traffic management: https://istio.io/latest/docs/concepts/traffic-management/
- RFC 4090 RSVP-TE Fast Reroute: https://www.rfc-editor.org/rfc/rfc4090
- RFC 7454 BGP Operations and Security: https://www.rfc-editor.org/rfc/rfc7454

## Open Questions

- Which blast-radius units survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which limits are static and which require current capacity evidence?
- Which policies must share the same blast-radius ceiling?
