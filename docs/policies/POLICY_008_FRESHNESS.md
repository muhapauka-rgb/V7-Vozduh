# POLICY_008_FRESHNESS

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: freshness
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for freshness.

Freshness means whether evidence, health, state, policy, route, assignment, or approval is recent enough to support an operational decision.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Stale evidence can make a correct historical decision unsafe now.

Production systems deal with freshness through TTLs, leases, resource versions, observed generations, timestamps, health-check intervals, cache invalidation, monotonic versions, eventual consistency rules, and explicit stale/unknown states.

Freshness must be checked before action, not only when evidence is collected.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Mutation or routing action must not rely on stale evidence when current state can materially change. | `STRONG` | Kubernetes, cloud health checks, DNS/HTTP caching, BGP/BFD, Prometheus, Eureka, distributed systems | `HIGH`: broad across APIs, health systems, protocols, caches, and distributed systems | None for mutation safety. |
| Freshness must be represented explicitly through age, TTL, lease, version, generation, timer, timestamp, or status transition. | `STRONG` | Kubernetes resourceVersion/observedGeneration, DNS TTL, HTTP caching, BGP hold timer, BFD detect time, Prometheus scrape time, Eureka lease | `HIGH`: multiple independent technical families | None. |
| Unknown or stale evidence must be distinguishable from healthy/current evidence. | `STRONG` | Kubernetes conditions, Prometheus staleness, cloud health status, DNS/cache semantics, failure detector theory | `HIGH`: cross-system evidence | None. |
| Freshness requirements should vary by action risk and evidence type. | `MEDIUM` | Cloud health intervals, routing timers, SRE practice, Kubernetes controllers, distributed systems | `MEDIUM_HIGH`: broad but values are context-specific | Some systems use fixed defaults. |
| Caching/stale-read tolerance is acceptable for observation but not automatically acceptable for mutation. | `MEDIUM` | DNS/HTTP caching, Eureka client cache, distributed systems | `MEDIUM`: strong in caching/discovery, must be bounded for action | Availability-first systems may tolerate stale data under explicit policy. |
| Perfect freshness is impossible in distributed systems; bounded staleness or explicit stop is required. | `MEDIUM` | Academic distributed systems, leases/quorums, SRE practice | `MEDIUM`: strong theory and production relevance | Simple local systems may not expose this complexity. |
| Local timestamps alone are weaker than owner-issued versions or leases. | `WEAK` | Kubernetes versions, distributed systems, cache validators | `MEDIUM`: strong concept but implementation-dependent | Some systems accept local timestamps for low-risk observability. |

### Industry Consensus Research

#### Kubernetes

Kubernetes APIs use resource versions, observed generation, status conditions, controller reconciliation, leases, and readiness state. Controllers compare desired state and observed state continuously.

- Purpose: prevent controllers and operators from acting on stale object state.
- Existing production approaches: resourceVersion, generation/observedGeneration, status conditions, Lease objects, watch streams.
- Known patterns: controller observes state, reconciles, and updates status.
- Known failure patterns: stale watch, delayed status, controller lag.
- Known recovery patterns: relist/watch restart, reconciliation loop.
- Known tradeoffs: strict freshness can reduce actionability during API delay.
- Known limitations: observedGeneration proves controller observation, not real-world success.

#### Cloudflare / AWS / Azure / GCP Health Systems

Cloud and edge health systems define freshness through probe interval, timeout, consecutive thresholds, last transition, DNS TTL, target state, and monitor status.

- Purpose: ensure health decisions are based on recent observation.
- Existing production approaches: health-check interval, timeout, TTL, consecutive pass/fail count, status timestamp.
- Known patterns: fresh enough is tied to action class and risk.
- Known failure patterns: stale DNS, delayed monitor update, missing probe, unknown health.
- Known recovery patterns: repeat probes and recompute status.
- Known tradeoffs: shorter intervals improve freshness but increase load and false positives.
- Known limitations: probe freshness is not always user-impact freshness.

#### DNS / HTTP / Caching

DNS TTL, HTTP Cache-Control, ETags, Last-Modified, stale-if-error, and cache validation provide broad production models for freshness.

- Purpose: avoid using old data as current truth without validation.
- Existing production approaches: TTL, revalidation, validators, stale allowance, cache purge.
- Known patterns: data can be fresh, stale-but-allowed, stale-forbidden, or unknown.
- Known failure patterns: stale cache after state change, overlong TTL, clock skew.
- Known recovery patterns: expire, revalidate, purge, update version.
- Known tradeoffs: caching improves performance but creates staleness.
- Known limitations: freshness semantics differ by layer.

#### Service Discovery / Netflix Eureka

Eureka uses leases and heartbeats. Client caches intentionally tolerate registry outages, trading exact freshness for resilience.

- Purpose: maintain membership freshness while surviving discovery service failure.
- Existing production approaches: heartbeat renewal, lease expiry, registry cache, peer replication.
- Known patterns: lease freshness and cache staleness are explicit design choices.
- Known failure patterns: stale registry entry, partition, missed heartbeat.
- Known recovery patterns: renewal, re-registration, cache refresh.
- Known tradeoffs: resilience can require tolerating stale membership.
- Known limitations: membership freshness is not service-quality freshness.

#### Prometheus / Monitoring Systems

Prometheus models stale time series and timestamps; monitoring queries depend on scrape interval, evaluation interval, and staleness behavior.

- Purpose: avoid treating old metrics as current.
- Existing production approaches: scrape timestamps, staleness markers, range vectors, evaluation intervals.
- Known patterns: metrics have collection time and query-time interpretation.
- Known failure patterns: missing scrape, stale target, delayed ingestion.
- Known recovery patterns: new samples restore series usefulness.
- Known tradeoffs: high scrape frequency improves freshness but costs resources.
- Known limitations: metric freshness does not prove end-to-end correctness.

#### Routing Protocols

BGP, OSPF, IS-IS, and BFD define freshness through timers, keepalives, hello/dead intervals, hold time, sequence numbers, and adjacency state.

- Purpose: decide whether routing information and neighbor liveness are current.
- Existing production approaches: hold timers, hello intervals, LSA/LSP sequence and age, BFD intervals.
- Known patterns: expire information if not refreshed.
- Known failure patterns: stale route, dead adjacency, delayed withdrawal.
- Known recovery patterns: fresh update, adjacency re-form, route reconvergence.
- Known tradeoffs: short timers improve freshness but risk instability.
- Known limitations: routing freshness does not equal application freshness.

#### Distributed Systems / Academic Work

Distributed systems research treats freshness through leases, clocks, logical clocks, vector clocks, quorum reads, bounded staleness, and session guarantees.

- Purpose: bound how old a decision's input may be.
- Existing production approaches: lease validity, quorum, version vectors, timestamp bounds.
- Known patterns: stale reads can be acceptable only under explicit bounds.
- Known failure patterns: clock skew, stale leader, partition, delayed message.
- Known recovery patterns: lease expiry, quorum refresh, fencing.
- Known tradeoffs: stronger freshness usually costs latency or availability.
- Known limitations: perfect freshness is impossible in distributed systems under partitions.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Strict freshness vs availability | Fresh reads may be unavailable during incidents. | Strict freshness prevents stale mutation; relaxed freshness preserves observation/actionability. | Strict for mutation; relaxed only for read-only display or explicitly bounded degraded mode. |
| TTL-based freshness vs event/version-based freshness | Systems differ in whether state changes are evented or polled. | TTL is simple; versions/events are precise but need owner support. | TTL for external probes; versions/generations for owned state. |
| Stale-but-allowed vs stale-forbidden | Some data can be useful while stale; action evidence usually cannot. | Stale allowance improves resilience; stale-forbidden improves safety. | Allow stale for context; forbid stale for execution eligibility. |
| Probe freshness vs user-impact freshness | Recent probes may not represent all users/services. | Probes are available and cheap; user impact is authoritative but harder to collect. | Combine before higher authority actions. |

### Industry Disagreement Research

1. Strict freshness versus availability.
   Strict freshness prevents stale action but can stop action during telemetry gaps.

2. TTL freshness versus event freshness.
   TTLs are simple; events can be more precise but require reliable delivery.

3. Stale-but-allowed versus stale-forbidden.
   Caches may allow stale data for reads, but mutation decisions usually need stricter freshness.

4. Local timestamp versus globally ordered version.
   Local timestamps are easy but vulnerable to clock issues; versions are stronger but require owner coordination.

5. Probe freshness versus user-impact freshness.
   A recent probe may not represent every user, service, or geography.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: `admin_core/intelligence_snapshots.py`, `admin_core/autonomy_trust_acceleration.py::build_freshness_actionability`, snapshot refresh, planner snapshot gate, runtime eligibility;
- evidence: runtime eligibility requires fresh packet immediately before execution; current read-only inventory blocks on stale/unknown domains; truth/convergence reports runtime aligned.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: mutation/routing action must not rely on stale evidence. | `FULLY_IMPLEMENTED` | Freshness actionability, runtime eligibility, planner snapshot gate. | Stale evidence produces STOP/blockers; runtime automation remains disabled. | Reuse freshness gate. | None. |
| CS2: freshness represented through age/TTL/lease/version/generation/timestamp/status. | `PARTIALLY_IMPLEMENTED` | Intelligence snapshots, packet/lease owner, truth snapshot. | Timestamps, generations, packet leases, runtime fingerprints exist; not every evidence family has owner-issued versions. | Reuse snapshot and lease owners. | `SMALL_EXTENSION`: normalize freshness fields across evidence families. |
| CS3: unknown/stale evidence distinct from healthy/current evidence. | `FULLY_IMPLEMENTED` | Freshness actionability. | Inventory returns `UNKNOWN`, `STALE_RECHECK_REQUIRED`, `ACTIONABLE_NOW`, and STOP behavior. | Reuse classifications. | None. |
| CS4: freshness requirements vary by action risk/evidence type. | `PARTIALLY_IMPLEMENTED` | Delegated policy preview, action-class runtime eligibility. | Required freshness domains exist; per-policy risk windows are not canonicalized. | Reuse delegated policy preview. | `SMALL_EXTENSION`: define policy-specific windows. |
| CS5: stale reads may be acceptable for observation, not automatically mutation. | `FULLY_IMPLEMENTED` | Runtime eligibility, truth/convergence, read-only inventory. | Read-only views can report stale/unknown; mutation remains blocked. | Reuse read-only/action split. | None. |
| CS6: perfect freshness impossible; bounded staleness or explicit stop required. | `FULLY_IMPLEMENTED_READ_ONLY` | Freshness actionability, OMP stop rules, `bounded_stale_allowance_by_action_class`. | Explicit stop exists; C6 decides stale/unknown evidence may be observed, diagnosed, and reported, but stale mutation allowance is `0` and fresh evidence inside existing action-class windows is required before mutation review. | Reuse stop conditions and action-class windows. | None. |
| CS7: local timestamps weaker than owner-issued versions/leases. | `PARTIALLY_IMPLEMENTED` | Execution lease, runtime snapshot, intelligence snapshots. | Leases exist for execution packets; broader evidence uses mixed timestamp/snapshot status. | Reuse lease/version patterns. | `SMALL_EXTENSION`: prefer owner-issued versions where available. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `72%` |
| Reuse potential | `95%` |
| Missing coverage | `28%` |
| Complexity of remaining work | `SMALL_TO_MODERATE` |
| Expected implementation risk | `LOW_MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `REUSE`.

Freshness practice fits V7 directly. V7 already stops mutation on stale evidence; implementation work should normalize windows, owner-issued versions, and per-action-class freshness requirements.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mutation must not rely on stale evidence. | `YES` | `REUSE` | Freshness gates already block stale mutation. | Freshness actionability, runtime eligibility, planner snapshot gate. | Keep as first policy gate. | `NONE` | Very high: prevents wrong moves. | `A2` |
| Age/TTL/lease/version/generation/timestamp/status. | `YES` | `ADAPT` | V7 has mixed freshness forms; not all are normalized. | Intelligence snapshots, packet/lease owner, truth snapshot. | Normalize fields across evidence families. | `SMALL_EXTENSION` | Very high: enables reliable Runtime decisions. | `A2` |
| Unknown/stale distinct from healthy/current. | `YES` | `REUSE` | Existing classifications already distinguish unknown, stale, and actionable. | Freshness actionability. | Preserve stop behavior. | `NONE` | High: avoids false health. | `A2` |
| Freshness varies by action risk/evidence type. | `YES` | `ADAPT` | Required domains exist; policy-specific windows are not canonicalized. | Delegated policy preview, action-class runtime eligibility. | Define per-policy risk windows. | `SMALL_EXTENSION` | Very high: gates autonomy safely. | `A2` |
| Stale reads may be acceptable for observation, not mutation. | `YES` | `REUSE` | V7 already separates read-only stale reporting from mutation. | Runtime eligibility, truth/convergence, read-only inventory. | Preserve read-only/action split. | `NONE` | High: useful diagnostics without risk. | `B17` |
| Perfect freshness impossible; bounded stop required. | `YES` | `REUSE_DONE_READ_ONLY` | Explicit stops exist; bounded stale allowance is decided by class with `0` stale mutation allowance. | Freshness actionability, OMP stop rules, `bounded_stale_allowance_by_action_class`. | Preserve stale read visibility while requiring fresh evidence before mutation review. | `NONE` | Medium high: practical reliability. | `C6` complete |
| Owner-issued versions stronger than local timestamps. | `YES` | `ADAPT` | Packet lease exists; broader evidence should prefer owner-issued versions. | Execution lease, runtime snapshot, intelligence snapshots. | Extend version/lease pattern where available. | `SMALL_EXTENSION` | High: improves idempotency. | `B18` |

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

- Kubernetes API concepts: https://kubernetes.io/docs/reference/using-api/api-concepts/
- Kubernetes Leases: https://kubernetes.io/docs/concepts/architecture/leases/
- Kubernetes Pod lifecycle and probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Cloudflare health details: https://developers.cloudflare.com/load-balancing/understand-basics/health-details/
- AWS Route 53 DNS failover: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
- Azure Traffic Manager endpoint monitoring: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Google Cloud health checks: https://docs.cloud.google.com/load-balancing/docs/health-check-concepts
- Prometheus querying basics and staleness: https://prometheus.io/docs/prometheus/latest/querying/basics/
- RFC 9111 HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111
- RFC 1035 Domain Names implementation: https://www.rfc-editor.org/rfc/rfc1035
- RFC 4271 BGP-4: https://www.rfc-editor.org/rfc/rfc4271
- RFC 5880 BFD: https://www.rfc-editor.org/rfc/rfc5880
- Netflix Eureka at a glance: https://github.com/Netflix/eureka/wiki/Eureka-at-a-glance

## Open Questions

- Which freshness classes survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which evidence may be stale-but-observable and which must be fresh-before-action?
- Which policy owns freshness for authority versus runtime evidence?
