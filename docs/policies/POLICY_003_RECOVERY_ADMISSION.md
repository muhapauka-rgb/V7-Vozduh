# POLICY_003_RECOVERY_ADMISSION

Status: `READ_ONLY_RUNTIME_INTEGRATION_CERTIFIED`
Policy class: recovery admission
Current lifecycle: `READ_ONLY_RUNTIME_INTEGRATION_CERTIFIED`
Next lifecycle: `PRODUCTION_AUTHORITY_AND_OUTCOME_CERTIFICATION`
Certification state: `B8_B9_B10_A6_READ_ONLY_CERTIFIED`
Implementation state: `DONE_READ_ONLY`
Runtime automation enabled: `NO`

## Purpose

This policy records the world research, V7 adaptation, and current read-only integration state for recovery admission.

Recovery admission means deciding when a previously failed or degraded channel, server, endpoint, route, service, or provider may safely receive traffic again.

V7 implements recovery admission as a read-only staged chain: B8 certification, B9 post-admission observation, B10 one-user staged progression, and A6 Runtime Eligibility consumption. The chain does not grant Authority, enable Runtime apply, move users, or certify production autonomy.

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

- owners: `admin_core/autonomy_trust_acceleration.py` B8/B9/B10 and A6 read models, freshness/actionability, restore/rollback, service/quality, authority, and autoswitch owners;
- evidence: recovery admission remains read-only, requires actionable current evidence, and now reaches A6 as a fail-closed one-user recovery-review candidate; production admission and runtime automation remain `NO`.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: recovery admission requires repeated success/readiness. | `DONE_READ_ONLY` | B8 recovery certification. | B8 requires repeated successful checks plus service, quality, freshness, and objective evidence. | Reuse B8. | Production outcome certification remains. |
| CS2: liveness and readiness/admission are separate. | `FULLY_IMPLEMENTED` | Recovery admission, service/route/readiness models. | V7 separates current evidence, admission overlay, and runtime eligibility. | Reuse existing separation. | `CONFIGURATION_ONLY`: bind to canonical policy. |
| CS3: recovered targets must continue to be observed. | `DONE_READ_ONLY` | B9, service matrix, quality compact. | B9 verifies existing post-admission observation windows after B8 certification. | Reuse B9 and existing observation owners. | Real post-action production outcomes remain. |
| CS4: slow start / gradual reintroduction is common when overload risk exists. | `DONE_READ_ONLY` | B10, A6, blast-radius/action-class ladder. | B10 maps recovery to one-user governed progression; A6 consumes it without apply. | Reuse B10, A6, and existing autoswitch owner. | Production authority and outcome certification remain. |
| CS5: replacement instead of re-admission is common in replaceable infrastructure. | `UNKNOWN` | Planner/autoswitch. | V7 routes users/channels; provider replacement is outside current runtime scope. | Reuse planner if replacement concept maps to alternate target. | `DOCUMENTATION_ONLY`: V7 fit decision needed. |
| CS6: time-based expiry alone is insufficient. | `DONE_READ_ONLY` | Freshness/actionability, B8, A6. | Recovery requires actionable evidence and explicit certification; timer expiry alone cannot pass A6. | Reuse existing freshness and recovery gates. | No read-only gap. |
| CS7: DNS-level recovery is limited to new connections. | `NOT_IMPLEMENTED` | None required for current scope. | V7 does not currently use DNS failover as primary recovery mechanism. | Reuse only if future DNS owner appears. | `DOCUMENTATION_ONLY`: likely non-applicable. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Read-only implementation coverage | `COMPLETE_FOR_B8_B9_B10_A6_PATH` |
| Existing-owner reuse | `COMPLETE` |
| Production authority coverage | `NOT_GRANTED` |
| Real production outcome coverage | `NOT_CERTIFIED` |
| Complexity of remaining work | `PRODUCTION_CERTIFICATION_ONLY` |
| Expected implementation risk | `HIGH_IF_AUTHORITY_IS_LATER_GRANTED` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `ADAPT`.

Recovery-admission practice fits V7. The read-only implementation adapts cloud/load-balancer recovery into channel re-admission, one-user staged progression, anti-flap, and existing outcome/learning owners; production authority and outcome evidence remain separate later certifications.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repeated success/readiness before recovery. | `DONE_READ_ONLY` | `REUSE_COMPLETE` | B8 certifies repeated checks and readiness evidence without admitting traffic. | B8 recovery certification. | Collect and close real recovery outcomes before production authority. | `PRODUCTION_CERTIFICATION` | High: prevents premature return. | `B8_COMPLETE` |
| Separate liveness from readiness/admission. | `YES` | `REUSE` | V7 already separates current evidence, admission, and runtime eligibility. | Recovery admission, service/route/readiness models. | Bind separation to canonical policy. | `NONE` | High: avoids binary health errors. | `B8` |
| Continue observation after recovery. | `DONE_READ_ONLY` | `ADAPT_COMPLETE` | B9 verifies existing service and quality observation windows after B8. | B9, service matrix, quality compact. | Reuse existing observations; require real post-action outcomes later. | `PRODUCTION_CERTIFICATION` | High: catches rebound failure. | `B9_COMPLETE` |
| Slow start / gradual reintroduction. | `DONE_READ_ONLY` | `ADAPT_COMPLETE` | B10 maps slow start to one-user action-class progression and A6 consumes it without apply. | B10, A6, blast-radius/action-class ladder. | Reuse existing autoswitch and authority owners for any later authorized action. | `PRODUCTION_CERTIFICATION` | High: improves safe scale-up. | `B10_COMPLETE` |
| Replacement instead of re-admission. | `PARTIAL` | `REJECT_FOR_NOW` | Provider replacement is outside current runtime scope; alternate target selection already exists. | Planner/autoswitch. | Treat as future platform/provider operation. | `NONE` | Optional. | `D2` |
| Time expiry alone insufficient. | `DONE_READ_ONLY` | `REUSE_COMPLETE` | Freshness actionability and B8/A6 require current actionable evidence. | Freshness/actionability, B8, A6. | Preserve fail-closed freshness consumption. | `NONE` | Medium high: blocks stale recovery. | `A2_COMPLETE` |
| DNS-level recovery limits. | `NO_FOR_CURRENT_SCOPE` | `REJECT` | V7 does not use DNS failover as the primary recovery model. | None required. | Keep as future DNS-platform option only. | `NONE` | Optional. | `D3` |

Need New Owner: `FALSE`.

## V7 Adaptation

`IMPLEMENTED_READ_ONLY`.

V7 adapts slow start to governed user/action-class progression instead of introducing a traffic-weight ramp. The existing B8/B9/B10 owners prepare a recovery candidate for the existing A6 Runtime Eligibility and autoswitch authority path.

## Why V7 Differs

V7 routes users across channels and already bounds mutation through action classes, blast radius, packet/lease identity, rollback, and governed autoswitch execution. Recovery therefore progresses through `ONE_USER_GOVERNED_RECOVERY_REVIEW`; it does not create a separate recovery executor or immediately restore full traffic.

## Runtime Behavior

When B8 identifies a recovery candidate through recovered-watch context, A6 consumes B8 certification, B9 observation windows, and B10 staged progression as one fail-closed read-only gate. Missing, stale, blocked, contradictory, or unverified recovery evidence produces `STOP_SAFE`. A complete chain identifies the existing `tools/v7-users-autoswitch` execution owner and a maximum one-user candidate, but keeps `runtime_apply_allowed = false` and `direct_execution_allowed = false`.

When no recovery candidate exists, including ordinary `ELIGIBLE` channel rows, the recovery gate is not applicable and non-recovery routing eligibility remains unchanged.

## Authority Behavior

Recovery evidence never creates Authority. Any future apply requires the existing action-class, blast-radius, operator authority, packet/lease identity, and live recheck contracts. This policy does not expand authority or blast radius.

## Safety

The chain remains `STOP_SAFE` for incomplete B8/B9/B10 contracts, stale or insufficient evidence, active cooldown, quarantine or target block, anti-flap denial, failed observation verification, missing rollback/verification readiness, identity mismatch, authority denial, or runtime-apply denial. The read-only recovery candidate is bounded to one user.

## Verification

Unit and regression verification cover valid read-only B8/B9/B10 consumption, missing stages, failed observation windows, upstream freshness/cooldown/quarantine blockers, and non-recovery compatibility. Real production movement and production outcome evidence remain outside this certification.

## Rollback

Future authorized execution must reuse the existing packet, lease, restore-barrier, verification, and autoswitch rollback owners. The recovery read model does not write restore barriers or invoke apply/rollback.

## Learning

Observed terminal outcomes must continue through existing Verification, Closure, Learning, Production Maturity, CPS, and OMP paths. Recovery preparation does not create synthetic evidence or promote read-only candidates into learned truth.

## Implementation Owner

Existing owners are reused:

- recovery preparation and A6 integration: `admin_core.autonomy_trust_acceleration`;
- governed execution: `tools/v7-users-autoswitch`;
- authority, packet/lease identity, restore barrier, verification, closure, learning, and production maturity: their existing canonical owners.

## Certification State

`READ_ONLY_RUNTIME_INTEGRATION_CERTIFIED`.

World research, V7 fit, B8/B9/B10 preparation, and A6 read-only consumption are complete. Production execution authority, production movement, and real recovery outcome certification are not granted.

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

- Which existing authority mode may first permit a governed one-user recovery action?
- What real production outcome evidence is required before recovery authority can mature?
- Which capacity evidence must accompany health evidence for wider recovery stages?
