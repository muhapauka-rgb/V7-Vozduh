# POLICY_002_SOFT_DEGRADATION

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: soft degradation
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for soft degradation.

Soft degradation means a channel, endpoint, server, route, service, or provider still works, but quality has fallen enough that the system may need to reduce traffic, shift traffic, slow actions, or stop before the degradation becomes a hard failure.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Mature systems must react to partial failure before users experience full outage, but soft degradation is harder than hard failure because evidence is noisy.

Latency spikes, packet loss, intermittent probe failures, elevated 5xx rate, overloaded backends, capacity exhaustion, DNS instability, regional saturation, and partial service failure can look like temporary noise.

If the system reacts too early, it can move traffic away from a usable path and overload alternatives. If it reacts too late, it can become a user-visible outage.

Therefore production systems usually treat degradation as a trend and threshold problem rather than a single-event decision.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Soft degradation must be treated as a quality trend or threshold problem, not as a single binary event. | `STRONG` | Google SRE, Cloudflare, AWS, Azure, GCP, Kubernetes, Envoy, Istio, HAProxy, NGINX, SD-WAN, academic failure detectors | `HIGH`: repeated across SRE, clouds, proxies, orchestrators, and academic work | None for noisy degradation requiring thresholds. |
| Quality evidence commonly includes latency, error rate, timeout, packet loss, jitter, saturation, unhealthy target state, and service-level response failure. | `STRONG` | Google SRE, cloud LBs, service mesh, HAProxy/NGINX, SD-WAN, routing probes | `HIGH`: broad production evidence | Routing-only systems may expose less application quality detail. |
| Degradation reaction must be safety-bounded because moving traffic can create cascading failure or overload alternatives. | `STRONG` | Google SRE, Envoy/Istio, Cloud LBs, HAProxy/NGINX, SD-WAN | `HIGH`: production case studies and platform controls | None for the need to bound reaction. |
| Active probes and passive observation are both common and complementary. | `MEDIUM` | Envoy, Istio, HAProxy, NGINX, cloud LBs, Google SRE | `MEDIUM_HIGH`: widespread but not universal | Some systems rely mostly on one evidence family. |
| Circuit breakers, outlier ejection, retry controls, load shedding, and graceful degradation are common degradation responses. | `MEDIUM` | Envoy, Istio, Google SRE, Netflix resilience patterns, HAProxy/NGINX | `MEDIUM_HIGH`: common in service/app architectures | Routing and DNS systems usually steer rather than degrade features. |
| SLA/SLO-based degradation thresholds are appropriate when service objectives are explicit. | `MEDIUM` | Google SRE, SD-WAN, cloud monitoring, service mesh metrics | `MEDIUM`: broad practice but threshold values are domain-specific | Systems without service objectives use simpler health states. |
| Probabilistic suspicion scoring is useful but architecture-specific. | `WEAK` | Academic failure detector literature, some distributed systems | `MEDIUM`: strong academic basis, less direct operational policy evidence | Most production LBs use simpler thresholds. |

### Industry Consensus Research

#### Cloudflare

Cloudflare Load Balancing monitors health from multiple regions and supports endpoint and pool steering based on health status, consecutive up/down checks, monitor intervals, timeouts, and pool health thresholds.

- Purpose: detect partial endpoint or pool quality loss before total outage.
- Existing production approaches: monitor HTTP/TCP behavior from distributed locations; aggregate status into endpoint and pool health.
- Known patterns: multi-vantage checks, consecutive failure thresholds, pool thresholds, fallback pools, event logs.
- Known failure patterns: single-region probe failure, origin overload, bad monitor configuration, all-pool unhealthy state.
- Known recovery patterns: continuous monitors restore endpoint eligibility after consecutive successful checks.
- Known tradeoffs: broader probe geography improves decision quality but increases latency before state changes.
- Known limitations: health checks can miss user-specific path degradation or service-specific problems.

#### Google SRE

Google SRE treats overload and cascading failure as first-class production risks. Degradation is not just endpoint liveness; it includes latency, error rate, deadline misses, overload, retry amplification, and capacity exhaustion.

- Purpose: stop partial failure from becoming cascading failure.
- Existing production approaches: SLOs, error budgets, overload protection, load shedding, backoff, graceful degradation, alerting, and capacity planning.
- Known patterns: reduce offered load, shed low-priority work, use client backoff and jitter, prevent retry storms.
- Known failure patterns: one cluster fails, traffic shifts to another, the receiving cluster overloads, clients retry, and the system collapses.
- Known recovery patterns: controlled traffic restoration after capacity and error rate return inside bounds.
- Known tradeoffs: aggressive failover may protect a local user path but harm the global system.
- Known limitations: degradation signals often lag real user impact.

#### AWS

AWS exposes degradation handling through ELB target health, Route 53 health checks, Auto Scaling health, CloudWatch alarms, CodeDeploy alarms, circuit-breaker-like service features, and managed replacement.

- Purpose: remove unhealthy or impaired resources before failure spreads.
- Existing production approaches: target health checks, status checks, alarms, deployment circuit breakers, DNS failover, instance replacement.
- Known patterns: consecutive health-check failures, alarm-driven rollback, target draining, replacement of impaired capacity.
- Known failure patterns: unhealthy target, impaired instance, failed deployment, degraded AZ or dependency.
- Known recovery patterns: healthy thresholds, replacement, or alarm clearing.
- Known tradeoffs: fail-open behavior exists in some load-balancer states when all targets are unhealthy.
- Known limitations: managed health is scoped to the configured resource and health-check semantics.

#### Azure

Azure Traffic Manager, Load Balancer, Application Gateway, Monitor, and deployment guidance use endpoint health, probe intervals, tolerated failures, routing methods, and safe deployment practices.

- Purpose: steer new traffic away from degraded endpoints or regions.
- Existing production approaches: endpoint monitoring, probe success criteria, multi-region routing, alerting, and safe deployment rings.
- Known patterns: timeout and tolerated failure thresholds, DNS TTL, route selection by monitor status.
- Known failure patterns: endpoint returns wrong status, timeout, regional issue, deployment regression.
- Known recovery patterns: continued monitoring and staged re-admission.
- Known tradeoffs: DNS-level reaction is not instantaneous for existing connections.
- Known limitations: endpoint monitor status can be healthy while a service-specific function is degraded.

#### GCP

Google Cloud Load Balancing uses health-check resources and backend health to decide whether backends receive traffic. Cloud Monitoring and SRE principles add latency/error/capacity signals.

- Purpose: stop sending traffic to backends that do not satisfy health criteria.
- Existing production approaches: explicit health checks, backend health state, configurable thresholds, observability.
- Known patterns: failed probe count, successful probe count, protocol-specific checks, backend eligibility.
- Known failure patterns: bad probe path, backend overload, regional degradation.
- Known recovery patterns: sequential successful probes restore eligibility.
- Known tradeoffs: health check configuration must match real service behavior.
- Known limitations: infrastructure health may not equal service quality.

#### Kubernetes

Kubernetes separates liveness, readiness, startup probes, Pod conditions, EndpointSlices, and controller reconciliation. Soft degradation appears as not-ready state, probe failures, resource pressure, restart backoff, or controller-observed inability to maintain desired state.

- Purpose: keep degraded Pods out of Service traffic while allowing recovery.
- Existing production approaches: readiness probes, liveness probes, startup probes, resource requests/limits, Pod conditions, backoff.
- Known patterns: readiness gates remove traffic before restart; liveness restarts stuck containers; startup probes prevent premature liveness failure.
- Known failure patterns: bad probes, CPU/memory pressure, restart loops, dependency slowness.
- Known recovery patterns: Pod becomes Ready only after probes pass.
- Known tradeoffs: aggressive probes can cause self-inflicted outage.
- Known limitations: Kubernetes knows container/pod signals, not every user-level service symptom.

#### Envoy / Istio / Linkerd

Service mesh systems use outlier detection, circuit breakers, retries, timeouts, ejection, endpoint health, and route metrics to react to degradation observed in request traffic.

- Purpose: protect callers from degraded upstreams.
- Existing production approaches: Envoy active health checking, passive outlier detection, Istio DestinationRule outlier detection, retries/timeouts, Linkerd route metrics.
- Known patterns: consecutive 5xx, local-origin failures, ejection time, maximum ejection percent, minimum health percent.
- Known failure patterns: upstream returns elevated errors, connection timeouts, overloaded service, retry amplification.
- Known recovery patterns: ejection expiry, successful requests, or health checks restore traffic.
- Known tradeoffs: ejection can shrink capacity and make remaining endpoints worse if bounded poorly.
- Known limitations: proxy-visible errors may not capture all business-level degradation.

#### HAProxy / NGINX

Load balancers handle degradation with active and passive health checks, rise/fall counters, slow start, max fails, fail timeout, and protocol-specific expected responses.

- Purpose: prevent degraded backends from receiving full traffic.
- Existing production approaches: TCP/HTTP checks, custom expected responses, passive failure detection, slow start.
- Known patterns: consecutive fail thresholds and consecutive success thresholds.
- Known failure patterns: timeout, connection refused, wrong status, intermittent backend errors.
- Known recovery patterns: pass enough checks, then re-enter rotation sometimes with slow start.
- Known tradeoffs: active checks create synthetic traffic; passive checks require user traffic to detect.
- Known limitations: bad health-check path can misclassify a backend.

#### Cisco / Juniper / Arista / BFD / Routing Protocols

Routing systems are stronger for hard failure than soft degradation, but mature operators combine liveness, interface errors, SLA probes, object tracking, BFD timers, damping, route metrics, and policy to avoid unstable paths.

- Purpose: detect path quality or reachability loss.
- Existing production approaches: IP SLA/RPM probes, object tracking, BFD, route metrics, damping, hold-down timers.
- Known patterns: missed probe thresholds, path metrics, policy-based failover.
- Known failure patterns: packet loss, delay, jitter, route adjacency instability.
- Known recovery patterns: object/session recovery and route reconvergence.
- Known tradeoffs: routing protocols often see topology, not application service quality.
- Known limitations: fast timers can flap under congestion.

#### Netflix

Netflix service discovery and cloud-native operation use registration leases, client-side load balancing, regional isolation, caches, and resilience patterns such as timeouts and circuit breakers.

- Purpose: avoid sending traffic to degraded or disappeared instances.
- Existing production approaches: Eureka leases, client caches, service discovery, load balancing, timeout/circuit-breaker practices.
- Known patterns: heartbeat renewal, stale registry tolerance, regional isolation.
- Known failure patterns: stale membership, dependency slowness, regional pressure.
- Known recovery patterns: re-registration and renewed lease.
- Known tradeoffs: cached data improves resilience but can keep stale choices.
- Known limitations: public Eureka material is stronger on membership than detailed degradation policy.

#### SD-WAN / Operator Best Practices

SD-WAN systems commonly classify path degradation through SLA probes, loss, latency, jitter, tunnel health, and application class policies.

- Purpose: keep application traffic on paths that satisfy quality requirements.
- Existing production approaches: path probes, SLA classes, tunnel health, application-aware routing, transport preference.
- Known patterns: loss/latency/jitter thresholds, policy steering, hold-down, path preference.
- Known failure patterns: brownouts, jitter spikes, intermittent internet path loss.
- Known recovery patterns: re-admit path after stable probe window.
- Known tradeoffs: too much steering can oscillate traffic.
- Known limitations: vendor-specific algorithms differ.

#### Academic And Distributed Systems

Academic failure-detector work shows that partial failure and slow communication cannot always be distinguished from crash failure in asynchronous systems.

- Purpose: model suspicion under uncertain timing.
- Existing production approaches: timeouts, heartbeats, suspicion scores, adaptive thresholds, gossip, quorum.
- Known patterns: suspicion level rather than immediate binary truth.
- Known failure patterns: false suspicion under high latency or packet loss.
- Known recovery patterns: suspicion clears when communication becomes stable.
- Known tradeoffs: faster reaction lowers downtime but increases false positives.
- Known limitations: academic models need operational safety gates before direct product use.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Binary healthy/unhealthy vs graded degradation | Some systems need simple routing eligibility; others need nuanced service quality. | Binary is operationally simple; graded quality improves decisions but needs more evidence. | Binary for basic LB/routing; graded for service/user quality and autonomy decisions. |
| Failover vs graceful degradation vs load shedding | Degradation may be solved by moving traffic or reducing demand. | Failover helps if alternatives are healthy; graceful degradation protects capacity; load shedding protects core service. | Failover for isolated target degradation; degradation/shedding for systemic overload. |
| Synthetic probes vs real user impact | Probes can be earlier than user harm but not representative. | Synthetic checks are controlled; real traffic is authoritative but delayed. | Use probes for early warning and real outcomes for confirmation. |
| Network-level quality vs application-level quality | Underlay path and service response can diverge. | Network metrics catch path brownouts; app metrics catch service failure. | Combine when action affects user routing. |

### Industry Disagreement Research

1. Latency/error degradation versus binary health.
   LBs and probes often reduce to healthy/unhealthy, while SRE and academic systems treat degradation as a gradient.

2. User traffic evidence versus synthetic probes.
   Synthetic probes are controlled and early; user traffic is real but may arrive after damage.

3. Service-level degradation versus network-level degradation.
   Routing protocols can miss service degradation; application proxies can miss underlay path trouble.

4. Automatic failover versus graceful degradation.
   Some systems move traffic; others shed load, reduce features, throttle, or wait.

5. Per-endpoint response versus global capacity safety.
   Local endpoint removal can be correct but globally unsafe if remaining capacity is insufficient.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: `tools/v7-users-autoswitch`, `tools/v7-egress-quality-compact`, `tools/v7-service-matrix-refresh-all`, `admin_core/operator_decision_surface.py`, `admin_core/autonomy_trust_acceleration.py`;
- evidence: quality/service/route/capacity gates exist, freshness/actionability reports currently stop when required domains are stale or unknown, runtime automation `NO`;
- no implementation or authority change performed.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: degradation is trend/threshold, not one binary event. | `FULLY_IMPLEMENTED` | Planner/autoswitch, quality compact, service matrix. | Candidate scores, service persistence thresholds, historical quality and blockers exist. | Reuse existing score/persistence logic. | `CONFIGURATION_ONLY`: align thresholds to canonical policy. |
| CS2: quality evidence includes latency/error/timeout/loss/jitter/saturation/service failure. | `PARTIALLY_IMPLEMENTED` | Quality compact, service matrix, route/service views. | V7 captures route/service/quality signals; not every industry signal is canonicalized. | Reuse signal owners. | `SMALL_EXTENSION`: normalize signal-to-policy mapping. |
| CS3: degradation reaction must be safety-bounded. | `FULLY_IMPLEMENTED` | Planner gates, restore barrier, action-class runtime eligibility. | Runtime eligibility blocks automation; blast/rollback/freshness gates are present. | Reuse OMP/action-class gates. | `CONFIGURATION_ONLY`: bind policy to classes. |
| CS4: active probes and passive observation are complementary. | `PARTIALLY_IMPLEMENTED` | Service matrix, quality compact, trust/outcome stores. | Both read/probe and observed-outcome paths exist, but source confidence remains incomplete. | Reuse evidence inventory and source confidence owners. | `MODERATE_EXTENSION`: complete observed degradation attribution. |
| CS5: circuit breakers/outlier ejection/load shedding are common responses. | `NOT_IMPLEMENTED` | Planner/autoswitch can be extended. | V7 currently moves users/channels; no circuit-breaker/load-shedding runtime behavior. | Extend planner policy if V7 fit requires it. | `MODERATE_EXTENSION`: choose V7-appropriate degradation response. |
| CS6: SLO/SLA thresholds when objectives are explicit. | `PARTIALLY_IMPLEMENTED` | Service-user SLA fit model, planner policy gates. | Read-only SLA/cohort fit exists; explicit service objectives are not fully policy-bound. | Reuse service-user SLA fit. | `SMALL_EXTENSION`: bind SLO/SLA thresholds to policy. |
| CS7: probabilistic suspicion is useful but architecture-specific. | `UNKNOWN` | Trust/confidence model, shadow autonomy. | V7 has confidence/trust models, but no canonical probabilistic degradation classifier. | Reuse trust/confidence only if fit analysis approves. | `DOCUMENTATION_ONLY`: decide applicability. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `61%` |
| Reuse potential | `90%` |
| Missing coverage | `39%` |
| Complexity of remaining work | `MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `ADAPT`.

Soft-degradation practice fits V7, but V7 must adapt proxy/cloud degradation responses to channel/user movement, read-only suitability, and action-class promotion. V7 should not introduce a separate degradation planner.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Degradation as trend/threshold, not binary event. | `YES` | `REUSE` | Existing score, persistence, history, and blockers already express gradual quality loss. | Planner/autoswitch, quality compact, service matrix. | Align thresholds to canonical policy vocabulary. | `NONE` | High: protects against noisy moves. | `B3` |
| Latency/error/timeout/loss/jitter/saturation/service evidence. | `YES` | `ADAPT` | V7 captures many signals but needs canonical signal-to-policy mapping. | Quality compact, service matrix, route/service views. | Normalize signal mapping by policy. | `SMALL_EXTENSION` | High: improves diagnosis and eligibility. | `B4` |
| Safety-bounded degradation reaction. | `YES` | `REUSE` | Existing runtime eligibility and planner gates already block unsafe action. | Planner gates, restore barrier, action-class runtime eligibility. | Bind policy to action classes. | `NONE` | High: preserves safety. | `A6` |
| Active probes plus passive observation. | `YES` | `ADAPT` | V7 has both paths but source confidence remains incomplete. | Service matrix, quality compact, trust/outcome stores. | Complete observed degradation attribution. | `MODERATE_EXTENSION` | High: distinguishes user impact from probe-only noise. | `B5` |
| Circuit breaker, outlier ejection, load shedding. | `PARTIAL` | `ADAPT` | V7 can map this to evacuation, quarantine, or no-action; it should not create unrelated proxy behavior. | Planner/autoswitch. | Choose V7-native degradation response per class. | `MODERATE_EXTENSION` | Medium high: better partial-failure handling. | `B6` |
| SLO/SLA thresholds. | `YES` | `REUSE` | Service-user SLA fit exists as read-only policy input. | Service-user SLA fit model, planner policy gates. | Bind service objectives to policy. | `SMALL_EXTENSION` | Medium high: service-aware routing. | `B7` |
| Probabilistic suspicion. | `PARTIAL` | `ADAPT` | Confidence/trust can support suspicion, but cannot replace safety gates. | Trust/confidence model, shadow autonomy. | Use only as advisory evidence. | `SMALL_EXTENSION` | Medium: better prioritization without unsafe autonomy. | `C2` |

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
- Google SRE, Handling Overload: https://sre.google/sre-book/handling-overload/
- Cloudflare Load Balancing health details: https://developers.cloudflare.com/load-balancing/understand-basics/health-details/
- AWS ELB target group health checks: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
- AWS ECS service unhealthy event messages: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-unhealthy-event-messages.html
- Azure Traffic Manager endpoint monitoring: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Google Cloud health checks: https://docs.cloud.google.com/load-balancing/docs/health-check-concepts
- Kubernetes Pod lifecycle and probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Envoy health checking: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking
- Envoy outlier detection: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier
- Istio DestinationRule OutlierDetection: https://istio.io/latest/docs/reference/config/networking/destination-rule/#OutlierDetection
- HAProxy health checks: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/
- NGINX HTTP health checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
- Netflix Eureka at a glance: https://github.com/Netflix/eureka/wiki/Eureka-at-a-glance
- Chandra and Toueg, Unreliable Failure Detectors: https://dl.acm.org/doi/10.1145/226643.226647
- Hayashibara et al., The Phi Accrual Failure Detector: https://ieeexplore.ieee.org/document/1353004

## Open Questions

- Which degradation signals survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which systems treat degradation as action-worthy versus observation-only?
- Which degradation evidence families must share freshness and anti-flap gates?
