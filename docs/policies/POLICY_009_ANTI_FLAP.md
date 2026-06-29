# POLICY_009_ANTI_FLAP

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: anti-flap
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for anti-flap.

Anti-flap means preventing repeated oscillation between states, channels, routes, targets, or policies when evidence changes rapidly or ambiguously.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Automation can make failures worse when it changes state repeatedly in response to unstable signals.

Mature systems use hysteresis, dampening, cooldown, hold-down, backoff, consecutive pass/fail thresholds, max ejection percentages, rollout pauses, rate limits, and staged recovery to avoid oscillation.

Anti-flap is shared by hard failure, soft degradation, recovery admission, rollback, freshness, authority, and blast-radius policies.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Automation must include anti-flap controls when signals can change rapidly or ambiguously. | `STRONG` | BGP damping, routing timers, BFD guidance, HAProxy/NGINX rise/fall, Envoy/Istio ejection, Kubernetes backoff, cloud health thresholds, Google SRE | `HIGH`: broad across routing, LBs, mesh, cloud, orchestrators, SRE | None for unstable signals. |
| Hysteresis or asymmetric thresholds are common: removal can differ from re-admission. | `STRONG` | HAProxy rise/fall, NGINX fails/passes, Cloudflare consecutive down/up, AWS/GCP health thresholds, Kubernetes readiness/backoff | `HIGH`: repeated production mechanisms | Some protocols use symmetric timers but still have state machines. |
| Cooldown, hold-down, dampening, backoff, or recovery windows protect against oscillation. | `STRONG` | BGP, Juniper/Cisco/Arista, Kubernetes, Google SRE, SD-WAN, load balancers | `HIGH`: repeated independent systems | None for repeated instability. |
| Anti-flap must be balanced against availability because too much suppression delays recovery. | `STRONG` | RIPE/BGP damping history, routing vendors, SRE, LBs, Kubernetes | `HIGH`: production evidence and known limitations | None; the tradeoff is universal. |
| Pool-wide bounds such as max ejection percentage or minimum health are common in proxy/mesh systems. | `MEDIUM` | Envoy, Istio, service mesh | `MEDIUM`: strong in mesh/proxy architectures | Routing/cloud systems use other blast-radius controls. |
| Operator freeze/manual review is useful during broad or ambiguous instability. | `MEDIUM` | SRE incident practice, SD-WAN/operator best practices, network operations | `MEDIUM`: common practice, less formally specified | Fully automated low-risk systems may unfreeze by timer. |
| Route flap damping is specialized and not universally recommended in its original aggressive form. | `WEAK` | RFC 2439, RIPE recommendations, routing operations | `MEDIUM`: strong history but context-specific | Many systems use softer hold-down/hysteresis instead. |

### Industry Consensus Research

#### BGP / Routing

BGP route flap damping, route timers, hold time, MRAI behavior, and routing policy are classic anti-flap mechanisms. OSPF/IS-IS SPF throttling and BFD damping/hold-down approaches serve similar purposes.

- Purpose: prevent unstable routes from causing repeated global reconvergence.
- Existing production approaches: route flap damping, hold timers, SPF throttling, BFD damping, route policy.
- Known patterns: suppress unstable state for a period after repeated change.
- Known failure patterns: route oscillation, link instability, route leak.
- Known recovery patterns: penalty decays or hold-down expires.
- Known tradeoffs: damping can suppress legitimately recovered routes.
- Known limitations: aggressive damping has historically harmed reachability if misused.

#### Juniper / Cisco / Arista

Network vendors support timer tuning, dampening, hold-down, BFD interval/multiplier tuning, route policy, and commit/rollback safeguards.

- Purpose: keep fast detection from creating unstable routing.
- Existing production approaches: BFD timer guidance, damping, hold-down, route policy.
- Known patterns: fast failure detection is paired with stability controls.
- Known failure patterns: congestion causes false BFD failure, intermittent link, unstable adjacency.
- Known recovery patterns: session must stay up long enough to be trusted.
- Known tradeoffs: anti-flap delays recovery.
- Known limitations: vendor/platform timer limits differ.

#### HAProxy / NGINX / Load Balancers

Load balancers use `fall` and `rise` counters, fail timeout, slow start, passive failure counters, and max failure windows.

- Purpose: avoid adding/removing backend on every transient response.
- Existing production approaches: consecutive fail and success thresholds, slow start, max fails, fail timeout.
- Known patterns: different thresholds for down and up create hysteresis.
- Known failure patterns: intermittent backend, overloaded server, bad health-check path.
- Known recovery patterns: rise threshold and slow start.
- Known tradeoffs: high thresholds delay reaction; low thresholds flap.
- Known limitations: probe choice can dominate behavior.

#### Envoy / Istio

Envoy and Istio use outlier ejection time, maximum ejection percent, interval, consecutive errors, enforcing percentages, and minimum health percentage.

- Purpose: avoid excessive endpoint ejection and repeated churn.
- Existing production approaches: base ejection time, max ejection percentage, min health percentage, panic/fail-open modes in load balancing.
- Known patterns: bound both individual endpoint churn and pool-wide impact.
- Known failure patterns: retry amplification, pool collapse, repeated ejection.
- Known recovery patterns: ejection expiry and successful health.
- Known tradeoffs: too conservative ejection leaves bad hosts active; too aggressive removes capacity.
- Known limitations: traffic shape can affect passive outlier accuracy.

#### Kubernetes

Kubernetes uses restart backoff, readiness gates, startup probes, rollout progress deadlines, max unavailable, and controller reconciliation to avoid rapid unsafe change.

- Purpose: avoid repeated restart or rollout churn.
- Existing production approaches: exponential backoff, readiness gating, rollout pause/rollback.
- Known patterns: backoff after repeated failure, readiness before traffic.
- Known failure patterns: CrashLoopBackOff, bad liveness probe, stuck rollout.
- Known recovery patterns: stable readiness and backoff reset.
- Known tradeoffs: backoff protects the system but delays recovery.
- Known limitations: misconfigured probes can create self-induced flapping.

#### Cloudflare / AWS / Azure / GCP

Cloud and edge health systems use consecutive up/down thresholds, health-check intervals, tolerated failures, DNS TTL, target deregistration delay, slow replacement, deployment alarms, and safe rollout rings.

- Purpose: prevent transient probe changes from immediately reshaping traffic.
- Existing production approaches: consecutive thresholds, TTL, deployment alarms, progressive rollout.
- Known patterns: repeated evidence before state transition.
- Known failure patterns: intermittent origin, probe location issue, deployment alarm flicker.
- Known recovery patterns: enough successful checks and stable alarm state.
- Known tradeoffs: stability versus response speed.
- Known limitations: DNS and caches can make anti-flap behavior hard to observe immediately.

#### Google SRE / Distributed Systems

SRE practice uses backoff, jitter, load shedding, rate limits, overload controls, and avoiding positive feedback loops. Distributed systems use suspicion thresholds, leases, exponential backoff, and quorum.

- Purpose: avoid synchronized retry/failover storms.
- Existing production approaches: exponential backoff, jitter, circuit breakers, load shedding, leases, rate limits.
- Known patterns: slow down repeated attempts after failure.
- Known failure patterns: thundering herd, retry storm, cascading failure.
- Known recovery patterns: controlled retry and gradual restoration.
- Known tradeoffs: slower retries reduce immediate success probability but protect the system.
- Known limitations: clients must actually honor backoff.

#### SD-WAN / Operator Best Practices

SD-WAN and operations teams use SLA hold-down, path preference, minimum stable windows, dampening, and manual freeze during incidents.

- Purpose: stop traffic from bouncing between unstable paths.
- Existing production approaches: SLA thresholds, hold-down, preferred path, recovery window, operator freeze.
- Known patterns: require stable path before re-entry.
- Known failure patterns: brownout oscillation, provider instability.
- Known recovery patterns: stable probe window and gradual re-admission.
- Known tradeoffs: conservative anti-flap may leave traffic on suboptimal path.
- Known limitations: vendor defaults differ.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Fixed cooldown vs adaptive dampening | Instability patterns differ by target and history. | Fixed is simple; adaptive is responsive but complex. | Fixed for initial safety; adaptive after outcome evidence. |
| Fast failover vs flap suppression | Immediate movement can protect users but may bounce traffic repeatedly. | Fast response reduces downtime; suppression preserves stability. | Fast for confirmed hard failure; suppression for noisy degradation/recovery. |
| Symmetric vs asymmetric thresholds | Removing a bad target and re-admitting a recovered target carry different risks. | Symmetric is simple; asymmetric reduces relapse. | Asymmetric for recovery-sensitive systems. |
| Automatic unfreeze vs operator review | Some instability is routine; some indicates unknown systemic failure. | Automatic unfreeze reduces toil; operator review prevents repeated incident loops. | Automatic for certified bounded classes; review for broad ambiguity. |

### Industry Disagreement Research

1. Fixed cooldown versus adaptive dampening.
   Fixed cooldown is simple; adaptive dampening responds to repeated instability.

2. Fail fast versus suppress flapping.
   Fast detection helps outages; suppression protects against false positives and oscillation.

3. Symmetric versus asymmetric thresholds.
   Many systems require fewer failures to remove than successes to restore; others use symmetric thresholds.

4. Automatic unfreeze versus operator review.
   Some systems automatically re-enable after timer; high-risk environments require human review.

5. Per-target anti-flap versus global anti-flap.
   Endpoint-level cooldown may not protect against system-wide oscillation.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: planner cooldown/freeze/quarantine logic, `build_anti_flapping`, safety policy, rollback/verification history;
- evidence: anti-flap read-only overlay exists with cooldown, hysteresis, minimum observation window, rapid oscillation threshold; runtime automation `NO`.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: automation needs anti-flap controls for rapidly changing/ambiguous signals. | `FULLY_IMPLEMENTED` | Planner safety policy, anti-flap overlay. | Cooldowns, freeze/quarantine, and read-only anti-flap model exist. | Reuse existing controls. | `CONFIGURATION_ONLY`: bind canonical policy. |
| CS2: hysteresis/asymmetric thresholds are common. | `PARTIALLY_IMPLEMENTED` | Service signal thresholds, recovery admission. | Failure persistence and recovery success thresholds exist in different owners; not unified as canonical hysteresis. | Reuse service/recovery owners. | `SMALL_EXTENSION`: centralize hysteresis mapping. |
| CS3: cooldown/hold-down/dampening/backoff/recovery windows protect stability. | `FULLY_IMPLEMENTED` | Planner cooldown, anti-flap overlay. | Cooldown windows and freeze/quarantine thresholds exist. | Reuse planner safety policy. | None. |
| CS4: anti-flap must balance availability. | `PARTIALLY_IMPLEMENTED` | OMP, planner, runtime eligibility. | Stops are safe, but availability tradeoff policy is not canonicalized. | Reuse OMP arbitration and policy priority. | `SMALL_EXTENSION`: encode when hard failure overrides anti-flap. |
| CS5: pool-wide max ejection/minimum health common in mesh/proxy systems. | `PARTIALLY_IMPLEMENTED` | Planner capacity/load, action-class ladder. | V7 has move limits and capacity gates, not proxy max-ejection semantics. | Reuse capacity/load gates. | `DOCUMENTATION_ONLY`: decide applicability. |
| CS6: operator freeze/manual review useful during broad ambiguity. | `FULLY_IMPLEMENTED` | OMP authority boundary, planner freeze, runtime stop. | Authority boundary/manual approval and user/egress freeze logic exist. | Reuse authority and safety owners. | None. |
| CS7: route flap damping specialized, not universal. | `NOT_IMPLEMENTED` | None required for current scope. | V7 does not implement BGP route flap damping. | Reuse route/planner only if future fit requires it. | `DOCUMENTATION_ONLY`: likely non-applicable. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `68%` |
| Reuse potential | `91%` |
| Missing coverage | `32%` |
| Complexity of remaining work | `SMALL_TO_MODERATE` |
| Expected implementation risk | `LOW_MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `REUSE`.

Anti-flap practice fits V7 directly. Existing cooldown, freeze, anti-flap, authority boundary, and recovery admission owners should be reused; V7 should not copy route-flap dampening wholesale unless future routing substrate requires it.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anti-flap controls for ambiguous/rapidly changing signals. | `YES` | `REUSE` | Cooldowns, freeze/quarantine, and read-only anti-flap model exist. | Planner safety policy, anti-flap overlay. | Bind canonical policy to existing controls. | `NONE` | Very high: prevents oscillation. | `A6` |
| Hysteresis/asymmetric thresholds. | `YES` | `ADAPT` | Failure and recovery thresholds exist in different owners. | Service signal thresholds, recovery admission. | Centralize hysteresis mapping. | `SMALL_EXTENSION` | High: improves stability. | `B19` |
| Cooldown/hold-down/dampening/backoff/recovery windows. | `YES` | `REUSE` | Cooldown windows and freeze/quarantine exist. | Planner cooldown, anti-flap overlay. | Preserve planner safety policy. | `NONE` | High: reduces repeated moves. | `A6` |
| Availability tradeoff. | `YES` | `ADAPT` | V7 needs explicit arbitration when hard failure should override anti-flap. | OMP, planner, runtime eligibility. | Encode hard-failure override rule. | `SMALL_EXTENSION` | High: avoids both stuck-dead and oscillating paths. | `B20` |
| Pool max ejection/minimum health. | `DONE_READ_ONLY` | `ADAPT_COMPLETE` | V7 maps proxy max-ejection to action-class/certified blast-radius bounds and minimum-health to capacity/load, service-fit, freshness, and STOP_SAFE bounds; it does not create runtime ejection semantics. | Planner capacity/load, action-class ladder, Runtime Model freshness/blast bounds, OMP. | Preserve V7-native capacity and blast bounds; future runtime consumption requires separate authority/certification. | `NONE` | Medium high: better pool protection. | `C7_COMPLETE` |
| Operator freeze/manual review. | `YES` | `REUSE` | Authority boundary and freeze logic exist. | OMP authority boundary, planner freeze, runtime stop. | Keep manual review during broad ambiguity. | `NONE` | High: safe escalation. | `A6` |
| Route flap damping. | `NO_FOR_CURRENT_SCOPE` | `REJECT` | BGP route-flap damping is not V7's current abstraction. | None required. | Defer to future route owner if needed. | `NONE` | Optional. | `D6` |

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

- RFC 2439 BGP Route Flap Damping: https://www.rfc-editor.org/rfc/rfc2439
- RIPE-378 Route Flap Damping recommendations: https://www.ripe.net/publications/docs/ripe-378/
- RFC 5880 BFD: https://www.rfc-editor.org/rfc/rfc5880
- Juniper BFD and damping documentation: https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/bfd.html
- HAProxy health checks: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/
- NGINX HTTP health checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
- Envoy outlier detection: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier
- Istio DestinationRule OutlierDetection: https://istio.io/latest/docs/reference/config/networking/destination-rule/#OutlierDetection
- Kubernetes Pod lifecycle and probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Google SRE, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/
- Google SRE, Handling Overload: https://sre.google/sre-book/handling-overload/

## Open Questions

- Which anti-flap mechanisms survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which controls belong to recovery admission versus anti-flap?
- Which cooldowns should be per-user, per-channel, per-service, or global?
