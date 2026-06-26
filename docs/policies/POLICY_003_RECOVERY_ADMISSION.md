# POLICY_003_RECOVERY_ADMISSION

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: recovery admission
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for recovery admission.

Recovery admission means deciding when a previously failed or degraded channel, server, endpoint, route, service, or provider may safely receive traffic again.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Recovery is not the same as a single passing health check.

Many incidents recur because a target briefly looks healthy, receives full traffic immediately, overloads, fails again, and causes oscillation.

Mature systems therefore use recovery admission windows, consecutive success thresholds, slow start, dampening, readiness gates, route reconvergence, staged rollouts, and capacity checks before treating a recovered target as fully safe.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Recovery admission requires more than one successful observation; mature systems use repeated success, readiness, healthy thresholds, or state-machine recovery. | `STRONG` | Cloudflare, AWS, Azure, GCP, Kubernetes, HAProxy, NGINX, routing protocols, BFD, Eureka | `HIGH`: repeated across clouds, orchestrators, proxies, routing, and service discovery | None for high-risk recovery. |
| Liveness and readiness/admission are separate concepts. | `STRONG` | Kubernetes, GCP/AWS health checks, Envoy, HAProxy, NGINX, service discovery | `HIGH`: common in orchestrators/LBs/proxies | Some routing protocols expose only adjacency/liveness. |
| Recovered targets must continue to be observed after admission. | `STRONG` | Cloud health checks, Kubernetes, LBs, Envoy, routing protocols | `HIGH`: common control loop | None. |
| Slow start or gradual reintroduction is common when recovered capacity can overload. | `MEDIUM` | NGINX, HAProxy, Google SRE, service mesh, rollout systems | `MEDIUM_HIGH`: strong in LB/SRE/rollout systems | Some systems return fully after thresholds pass. |
| Replacement instead of re-admission is common in cloud instance/service models. | `MEDIUM` | AWS Auto Scaling, ECS, managed instance groups, Kubernetes controllers | `MEDIUM`: strong in replaceable infrastructure | Routing paths and external providers are often re-admitted rather than replaced. |
| Time-based ejection expiry alone is insufficient as a universal recovery proof. | `MEDIUM` | Envoy/Istio plus SRE caution | `MEDIUM`: documented pattern with known limits | Some low-risk outlier systems rely on expiry as pragmatic re-test. |
| DNS-level recovery is useful for new connections but not a complete session recovery model. | `WEAK` | Azure Traffic Manager, Route 53 | `MEDIUM`: strong for DNS systems only | Proxy/routing systems can influence active traffic differently. |

### Industry Consensus Research

#### Cloudflare

Cloudflare health checks use consecutive successful checks and pool health status before restoring endpoint or pool eligibility.

- Purpose: avoid immediately returning traffic to an endpoint after a transient good response.
- Existing production approaches: continuous monitors, `consecutive_up`, regional aggregation, pool thresholds.
- Known patterns: recovery requires repeated success and aggregation, not one check.
- Known failure patterns: intermittent endpoint, region-specific failure, partial pool recovery.
- Known recovery patterns: endpoint/pool returns after enough successful monitor results.
- Known tradeoffs: waiting improves stability but delays use of recovered capacity.
- Known limitations: health-check success may not equal full user-service recovery.

#### AWS

AWS ALB target health uses healthy thresholds before a target becomes healthy again. CodeDeploy, Auto Scaling, and ECS use health checks, alarms, replacement, and deployment rollback.

- Purpose: ensure recovered resources pass enough checks before service re-entry.
- Existing production approaches: healthy threshold count, deregistration delay, replacement instances, deployment alarms.
- Known patterns: repeated successes, lifecycle state, draining and re-registration.
- Known failure patterns: replacement instance unhealthy, deployment alarm, partial service recovery.
- Known recovery patterns: target group health returns after successful checks; replacement enters service after health passes.
- Known tradeoffs: replacement can be safer than reusing a suspect instance.
- Known limitations: ALB fail-open and health check mismatch can affect recovery meaning.

#### Azure

Azure Traffic Manager keeps probing degraded endpoints and returns them to DNS eligibility after monitor checks pass according to configured profile rules.

- Purpose: restore endpoint routing after evidence of stable reachability.
- Existing production approaches: endpoint monitor status, interval, tolerated failures, timeout, expected status.
- Known patterns: continuous probe loop, DNS TTL, endpoint status.
- Known failure patterns: endpoint intermittently passing, DNS cache retaining old choices.
- Known recovery patterns: endpoint moves from degraded to online once checks pass.
- Known tradeoffs: DNS propagation means recovery is not instantaneous.
- Known limitations: existing sessions are not controlled by DNS recovery.

#### GCP

Google Cloud Load Balancing uses successful probe thresholds to restore backend health and eligibility.

- Purpose: ensure backend can serve before routing traffic.
- Existing production approaches: configurable healthy/unhealthy thresholds and health-check resources.
- Known patterns: success count before healthy, backend health visibility.
- Known failure patterns: wrong health path, resource saturation, backend dependency failure.
- Known recovery patterns: repeated passing probes restore new request/connection eligibility.
- Known tradeoffs: explicit checks must be matched to real service readiness.
- Known limitations: backend health may be too coarse for user-specific service recovery.

#### Kubernetes

Kubernetes readiness is a recovery admission mechanism. A Pod can exist and run but remain out of Service traffic until readiness succeeds. Startup probes prevent liveness from killing slow-starting services, and controllers reconcile desired state.

- Purpose: avoid sending traffic to a container before it is ready.
- Existing production approaches: readiness probes, readiness gates, startup probes, EndpointSlice membership.
- Known patterns: traffic admission is separate from process liveness.
- Known failure patterns: restart loop, dependency not ready, bad readiness probe.
- Known recovery patterns: Pod becomes Ready, then Service endpoints include it.
- Known tradeoffs: too strict readiness keeps capacity idle; too loose readiness causes failed traffic.
- Known limitations: readiness may not prove all downstream dependencies are healthy.

#### Envoy / Istio

Envoy active health checking and Istio outlier detection provide re-admission after successful health checks or ejection-duration expiry, with configurable success thresholds and ejection bounds.

- Purpose: return upstream hosts to traffic after enough evidence.
- Existing production approaches: successful active checks, ejection expiry, base ejection time, max ejection percent.
- Known patterns: separate ejection and re-entry controls.
- Known failure patterns: repeated ejection, pool collapse, local-origin errors.
- Known recovery patterns: ejected endpoint re-enters after time/success criteria.
- Known tradeoffs: short ejection tests recovery sooner but may flap.
- Known limitations: ejection expiry alone may not prove full recovery.

#### HAProxy / NGINX

HAProxy uses `rise` counters, and NGINX Plus supports slow start and mandatory health checks before a server receives traffic.

- Purpose: avoid full immediate load on recently recovered backends.
- Existing production approaches: rise/fall counters, active health checks, slow start, mandatory checks.
- Known patterns: consecutive success, gradual weight restoration.
- Known failure patterns: transient pass followed by overload.
- Known recovery patterns: pass enough checks and gradually receive traffic.
- Known tradeoffs: slow start protects the backend but reduces immediate available capacity.
- Known limitations: open-source and commercial feature sets differ.

#### Cisco / Juniper / Arista / Routing

Routing systems recover through session/adjacency restoration, route reconvergence, BFD up state, object tracking recovery, dampening, hold-down, and route policy.

- Purpose: avoid unstable route reintroduction.
- Existing production approaches: protocol state machines, BFD session up, damping, hold-down, route reconvergence.
- Known patterns: state-machine recovery, not ad hoc traffic restoration.
- Known failure patterns: route flapping, link intermittency, control-plane/data-plane mismatch.
- Known recovery patterns: adjacency/session re-establishes and route becomes eligible.
- Known tradeoffs: dampening delays recovery but protects stability.
- Known limitations: protocol recovery may not prove application quality.

#### Netflix / Service Discovery

Eureka re-admits service instances through registration and heartbeat renewal. Clients consume registry changes while caches provide resilience.

- Purpose: return instances to discovery after they renew membership.
- Existing production approaches: registration, lease renewal, registry replication, client cache.
- Known patterns: membership recovery through lease state.
- Known failure patterns: stale registry, partition, delayed propagation.
- Known recovery patterns: instance re-registers and renews lease.
- Known tradeoffs: client caches reduce dependency on registry but delay exact freshness.
- Known limitations: discovery presence is not full service quality.

#### Google SRE And Production Postmortems

Google SRE emphasizes that recovery can trigger overload if traffic returns too quickly. Recovery should consider capacity, backoff, overload controls, and the risk of cascading failure.

- Purpose: restore service without re-triggering the incident.
- Existing production approaches: gradual restoration, load shedding, overload controls, capacity validation.
- Known patterns: recovery is a capacity and stability decision, not only a health bit.
- Known failure patterns: thundering herd, retry storm, traffic shift overload.
- Known recovery patterns: controlled traffic reintroduction with monitoring.
- Known tradeoffs: safer recovery can be slower.
- Known limitations: every service has different safe warm-up behavior.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Immediate re-entry after threshold vs slow start | Passing checks may not prove full capacity. | Immediate re-entry restores capacity; slow start avoids relapse. | Immediate for low-risk targets; slow start for overloaded/recently failed targets. |
| Health proof vs capacity proof | A target can answer checks but fail under load. | Health proof is cheap; capacity proof is safer but harder. | Health proof for simple endpoints; capacity proof for high blast-radius admission. |
| Re-admit same target vs replace target | Some resources are cattle; routes/providers may not be replaceable. | Replacement avoids suspect state; re-admission preserves scarce resources. | Replace ephemeral compute; re-admit external channels/routes after stability. |
| Timer expiry vs successful probes | Time can cool down instability, but success proves current liveness. | Timer expiry is simple; probes are evidence-backed. | Timer for cooldown; probes for admission. |

### Industry Disagreement Research

1. Immediate re-entry versus slow start.
   Some systems restore after health thresholds; others ramp traffic gradually.

2. Health success versus capacity proof.
   Probe success can show reachability; SRE practice demands capacity safety too.

3. Session/state recovery versus service recovery.
   Routing adjacency recovery may happen before application-level service quality returns.

4. Time-based expiry versus success-based recovery.
   Ejection timers can expire even when quality is uncertain; active checks require explicit pass.

5. Replacement versus re-admission.
   Cloud systems may replace bad instances instead of trusting recovered ones.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: `admin_core/autonomy_trust_acceleration.py::build_recovery_admission`, freshness/actionability, restore/rollback, service/quality owners;
- evidence: recovery admission is read-only, requires `ACTIONABLE_NOW`, currently sees no eligible production rows in local inventory; runtime automation `NO`.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: recovery admission requires repeated success/readiness. | `PARTIALLY_IMPLEMENTED` | `build_recovery_admission`. | Policy includes minimum successful checks and watch checks; not certified with real recovery outcomes. | Reuse recovery admission overlay. | `MODERATE_EXTENSION`: collect real recovery outcomes. |
| CS2: liveness and readiness/admission are separate. | `FULLY_IMPLEMENTED` | Recovery admission, service/route/readiness models. | V7 separates current evidence, admission overlay, and runtime eligibility. | Reuse existing separation. | `CONFIGURATION_ONLY`: bind to canonical policy. |
| CS3: recovered targets must continue to be observed. | `PARTIALLY_IMPLEMENTED` | Service matrix, quality compact, recovery admission. | Continued observation owners exist; closed recovery outcome evidence is incomplete. | Reuse service/quality refresh. | `SMALL_EXTENSION`: require post-admission observation window. |
| CS4: slow start / gradual reintroduction is common when overload risk exists. | `PARTIALLY_IMPLEMENTED` | Blast-radius/action-class ladder. | One-user bounds exist; explicit slow-start recovery progression is not implemented. | Reuse action-class ladder and blast-radius gates. | `MODERATE_EXTENSION`: define recovery slow-start path. |
| CS5: replacement instead of re-admission is common in replaceable infrastructure. | `UNKNOWN` | Planner/autoswitch. | V7 routes users/channels; provider replacement is outside current runtime scope. | Reuse planner if replacement concept maps to alternate target. | `DOCUMENTATION_ONLY`: V7 fit decision needed. |
| CS6: time-based expiry alone is insufficient. | `PARTIALLY_IMPLEMENTED` | Freshness/actionability and recovery admission. | Freshness requires actionable evidence, not only time expiry; certification still pending. | Reuse freshness gate. | `SMALL_EXTENSION`: enforce in canonical recovery policy. |
| CS7: DNS-level recovery is limited to new connections. | `NOT_IMPLEMENTED` | None required for current scope. | V7 does not currently use DNS failover as primary recovery mechanism. | Reuse only if future DNS owner appears. | `DOCUMENTATION_ONLY`: likely non-applicable. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `48%` |
| Reuse potential | `86%` |
| Missing coverage | `52%` |
| Complexity of remaining work | `MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `ADAPT`.

Recovery-admission practice fits V7, but V7 must adapt cloud/load-balancer recovery into channel re-admission, slow-start movement, anti-flap, and outcome-certified learning.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repeated success/readiness before recovery. | `YES` | `REUSE` | Recovery admission overlay exists and needs real outcome certification. | `build_recovery_admission`. | Collect and close real recovery outcomes. | `MODERATE_EXTENSION` | High: prevents premature return. | `B8` |
| Separate liveness from readiness/admission. | `YES` | `REUSE` | V7 already separates current evidence, admission, and runtime eligibility. | Recovery admission, service/route/readiness models. | Bind separation to canonical policy. | `NONE` | High: avoids binary health errors. | `B8` |
| Continue observation after recovery. | `YES` | `ADAPT` | Existing observation owners need post-admission windows. | Service matrix, quality compact, recovery admission. | Require post-admission observation windows. | `SMALL_EXTENSION` | High: catches rebound failure. | `B9` |
| Slow start / gradual reintroduction. | `YES` | `ADAPT` | V7 should map slow start to users/action classes, not traffic weights by default. | Blast-radius/action-class ladder. | Define recovery slow-start path. | `MODERATE_EXTENSION` | High: improves safe scale-up. | `B10` |
| Replacement instead of re-admission. | `PARTIAL` | `REJECT_FOR_NOW` | Provider replacement is outside current runtime scope; alternate target selection already exists. | Planner/autoswitch. | Treat as future platform/provider operation. | `NONE` | Optional. | `D2` |
| Time expiry alone insufficient. | `YES` | `REUSE` | Freshness actionability already requires actionable evidence. | Freshness/actionability and recovery admission. | Enforce in canonical recovery policy. | `SMALL_EXTENSION` | Medium high: blocks stale recovery. | `A2` |
| DNS-level recovery limits. | `NO_FOR_CURRENT_SCOPE` | `REJECT` | V7 does not use DNS failover as the primary recovery model. | None required. | Keep as future DNS-platform option only. | `NONE` | Optional. | `D3` |

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

- Cloudflare health details: https://developers.cloudflare.com/load-balancing/understand-basics/health-details/
- AWS ALB target group health checks: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
- AWS CodeDeploy rollback and redeploy: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
- Azure Traffic Manager endpoint monitoring: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Google Cloud health checks: https://docs.cloud.google.com/load-balancing/docs/health-check-concepts
- Kubernetes Pod lifecycle and probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Envoy health checking: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking
- Istio DestinationRule OutlierDetection: https://istio.io/latest/docs/reference/config/networking/destination-rule/#OutlierDetection
- HAProxy health checks: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/
- NGINX HTTP health checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
- Netflix Eureka at a glance: https://github.com/Netflix/eureka/wiki/Eureka-at-a-glance
- Google SRE, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/

## Open Questions

- Which recovery windows survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which recovery controls must be shared with anti-flap and freshness policies?
- Which systems require capacity proof in addition to health proof?
