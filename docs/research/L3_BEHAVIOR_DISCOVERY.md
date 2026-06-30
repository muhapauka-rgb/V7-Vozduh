# L3 Behavior Discovery

Status: `DISCOVERY_COMPLETE`
Scope: production-grade emergency autonomous failover behavior
Implementation impact: `NONE`
Runtime impact: `NONE`
L3 specification modified: `NO`

## Executive Summary

This discovery studies how mature routing, orchestration, service mesh, load balancing, and SRE systems behave after a channel, endpoint, node, route, or service path suddenly fails.

The strongest production consensus is behavioral, not architectural:

1. Detect failure through owner-specific health evidence and thresholds.
2. Collapse duplicate or late events before action.
3. Open an incident or reconciliation context.
4. Identify affected subjects and viable replacement targets.
5. Revalidate target health and authority immediately before mutation.
6. Execute only inside a bounded budget.
7. Verify the new state after mutation.
8. Roll back, contain, or suspend on failed verification.
9. Apply retry/backoff/circuit-breaker rules to prevent repeated harm.
10. Record terminal outcome and feed learning/reconciliation.

V7 already describes the core L3 emergency failover path: wake, observe, classify, plan, authority, eligibility, execute, verify, rollback/contain, learn, report, sleep.

The main production behavior patterns that are not yet fully explicit in the L3 capability specification are:

- event collapse and duplicate-event suppression;
- incident merge/split rules;
- retry budget and backoff policy;
- partial-success handling;
- unknown-state quarantine;
- parallel incident arbitration;
- late/stale event handling;
- resume-after-suspend contract;
- target-lost-during-execution behavior;
- budget exhaustion terminal behavior.

These are not new architecture. They are behavior contracts that can reuse the existing Autonomous Runtime Model, L3 capability owner composition, incident/report lifecycle, runtime eligibility, rollback, verification, anti-flap, freshness, and OMP certification owners.

## Industry Survey

| System family | Observed production behavior |
| --- | --- |
| Cisco / Juniper / Arista routing | Failure detection is normally delegated to protocol or liveness mechanisms such as BFD, routing adjacency state, IP SLA/RPM-like probing, route withdrawal, route preference, or fast reroute. Behavior emphasizes fast local detection, bounded convergence, hold-down/dampening, and operator-visible control. |
| VMware NSX | HA and edge/service failover behavior is controller/cluster mediated: detect edge/service health, choose standby/alternate path, preserve state where possible, and expose failover state to operators. |
| Google SRE / Borg / Traffic Director / Service Mesh | Behavior emphasizes overload avoidance, backoff, draining, health-aware traffic steering, controller reconciliation, incident response, and avoiding cascading failure. Failover is bounded by capacity and SLO risk. |
| Kubernetes controllers | Controllers reconcile desired/current state, use readiness/liveness/startup probes, restart backoff, EndpointSlice readiness, rollout status, progress deadlines, and event/retry handling. Controllers do not treat one event as permanent truth; they keep reconciling until desired state or terminal failure. |
| Istio / Envoy / Linkerd | Mesh behavior uses endpoint health, retries, timeouts, outlier detection/ejection, circuit breakers, retry budgets, mTLS/service policy, and route/weight control. Verification is traffic/health based, and repeated bad targets are ejected or circuit-broken. |
| AWS / Azure / GCP | Managed control planes use health checks, target group state, endpoint monitoring, alarms, DNS/LB failover, deployment rollback, and automated replacement. They separate health evidence, routing decision, execution, and alarm/rollback. |
| Cloudflare | Load balancing behavior uses monitors, pool health, steering policy, fallback pools, session affinity controls, and global traffic steering. The behavior is failover inside configured pools, not arbitrary runtime invention. |
| Meta / Netflix | Public material emphasizes resilient control loops, failure isolation, circuit breakers, fallback, client/server health, regional or cell isolation, backoff, and learning from incidents. Netflix Hystrix-style behavior is especially relevant for circuit breaking, fallback, and isolation. |
| Consul | Service discovery and service-resolver behavior supports failover targets, locality, health-aware service selection, and policy-driven target choice. |
| Cilium | Kubernetes/eBPF service networking focuses on efficient datapath, service load balancing, identity/policy, and control-plane integration; failover behavior is normally consumed through Kubernetes/service state and health-aware routing. |
| HAProxy / NGINX | Load balancers use active/passive health checks, rise/fall or max_fails/fail_timeout style thresholds, backup servers, retries, timeouts, draining, and endpoint disable/reenable. |
| Linux HA clusters | HA clusters use resource agents, monitors, fencing/STONITH, quorum, failover policies, restart/failover thresholds, migration thresholds, and constraints. They strongly separate "unknown" from "safe to run elsewhere." |

## Behavior Catalog

| Behavior | Problem solved | Production pattern | V7 classification | Existing V7 owner mapping |
| --- | --- | --- | --- | --- |
| Failure thresholding | Avoid acting on one noisy sample. | Consecutive failures, BFD multiplier, probe thresholds, readiness conditions. | Already Exists | Policy 001, Policy 008, service evidence, freshness. |
| Incident open | Preserve visibility and state. | Controller event, deployment condition, load balancer health event, incident page. | Already Exists | L3 Incident Contract, report lifecycle, CPS. |
| Event collapse | Avoid duplicate execution from repeated signals. | Workqueue coalescing, idempotency key, debounce, health-state transition only. | Needs Extension | Autonomous Runtime Model event dispatch, L3 idempotency, incident owner. |
| Incident merge | Avoid parallel duplicate incidents for same failure scope. | Merge same source/scope/failure-family into one active incident. | Needs Extension | Incident/report owner, CPS, L3 incident contract. |
| Incident split | Avoid one broad incident hiding independent failures. | Split by affected source, target, service family, authority envelope, or blast radius. | Needs Extension | Incident/report owner, planner subject mapping. |
| Affected subject discovery | Find who is harmed. | Endpoint membership, pods on node, clients on failed pool, routes via failed path. | Already Exists | Planner/user assignment owners. |
| Safe target selection | Avoid moving to an unhealthy destination. | Health-aware LB, readiness, endpoint health, priority/fallback pools. | Already Exists | Planner/autoswitch, service suitability, load/quality/policy gates. |
| Immediate pre-commit revalidation | Avoid stale action. | Reconcile current health before applying traffic or config. | Already Exists | Runtime eligibility, freshness, restore barrier, decision identity. |
| Target lost before apply | Stop if destination becomes bad during cycle. | Revalidate target; ejection or STOP before mutation. | Needs Extension | Runtime eligibility, material state change, L3 readiness. |
| Partial success | Avoid binary success/failure lies. | Per-subject status, rollout partial progress, degraded terminal states. | Needs Extension | Terminal outcome classification, incident/report, learning. |
| Verification timeout | Avoid hanging runtime. | Bounded timeout, unknown state, rollback/contain/escalate. | Needs Extension | Verification owner, L3 verification contract. |
| Rollback success | Preserve safety and learn. | Rollback/revert/route restore succeeds after failed verification. | Already Exists | Policy 007, terminal classification, feedback/learning. |
| Rollback failure | Escalate and suspend. | Incident remains open, containment/fencing/manual review. | Already Exists | Policy 007, L3 rollback, incident/suspension. |
| Retry budget | Avoid infinite attempts. | Limited retries, retry budgets, rate limits, max attempts/window. | Needs Extension | Anti-flap, execution budget, runtime circuit breaker. |
| Backoff | Avoid retry storms/flapping. | Exponential backoff, hold-down, damping, cooldown, jitter. | Needs Extension | Policy 009, movement protection, circuit breaker. |
| Circuit breaker | Stop unsafe repeated execution. | Open breaker after failures, half-open probe, suspend automation. | Already Exists (partial) | L3 readiness, Autonomous Runtime Model SUSPENDED, Policy 009. |
| Kill switch / operator override | Stop automation immediately. | Manual disable, freeze, maintenance mode. | Already Exists | Authority, OMP, Runtime suspension, operator surface. |
| Duplicate event | Avoid duplicate apply. | Idempotency, event resource version, workqueue dedupe. | Already Exists (test-level) / Needs Extension (behavior detail) | L3 test contract, execution idempotency. |
| Late event | Avoid acting on outdated failure. | Resource version, timestamp, state generation, monotonic incident state. | Needs Extension | Freshness, owner-issued versions, incident owner. |
| Stale event | Stop or ignore safely. | TTL, generation mismatch, stale observation stop. | Already Exists | Freshness, runtime eligibility. |
| Multiple incidents | Preserve local safety under parallel failures. | Per-scope budgets, global breaker, incident merge/split, priority. | Needs Extension | Blast radius, execution budget, incident arbitration. |
| Race condition | Avoid apply after state changed. | Optimistic concurrency, generation match, final eligibility. | Already Exists | Decision commit, material state change, restore barrier. |
| Unknown state | Do not guess. | Quarantine, suspend, manual review, no mutation. | Needs Extension | Runtime STOP_SAFE/SUSPENDED, incident contract. |
| Recovery during execution | Decide whether to abort, continue verify, or close no-op. | Revalidate source/target; if source recovered before commit, abort; if after commit, verify terminal state. | Needs Extension | Runtime eligibility, verification, terminal outcome. |
| Recovery after suspend | Resume only after stable windows and authority. | Half-open/probe, slow start, stable readiness. | Needs Extension | Recovery admission, Policy 003, slow start, OMP certification. |
| Budget exhaustion | Stop when execution/retry/blast budget consumed. | Max unavailable, error budget, retry budget, ejection max, rate limit. | Needs Extension | Blast radius, execution budget, circuit breaker. |

## Scenario Library

### Happy Path

- Trigger: confirmed current-channel hard/service failure.
- Current State: affected user remains on failed source; one safe target exists.
- Expected Behavior: open incident, select target, pass authority/readiness, execute one failover, verify route/services, close success, learn.
- State Transitions: `IDLE -> WAKE -> OBSERVE -> CLASSIFY -> WORLD_READY -> PLAN_READY -> READY -> EXECUTING -> VERIFYING -> LEARNING -> REPORTING -> SLEEP`.
- Terminal State: `SUCCESS`.
- V7 Classification: Already Exists.

### Hard Failure

- Trigger: hard failure or service loss reaches certified threshold.
- Expected Behavior: remove/de-prefer failed source for affected subject, do not wait for optimization, use emergency authority only if certified, stop if no target.
- Failure Modes: false positive, stale signal, target overload.
- V7 Classification: Already Exists.

### Soft Failure

- Trigger: latency/error/degradation without complete service loss.
- Expected Behavior: do not execute L3 unless it is reclassified as current-channel service failure; route to L4/Later capability.
- Terminal State: `NO_ACTION` or `STOP_SAFE`.
- V7 Classification: Already Exists / Not Suitable for L3 execution.

### No Target

- Trigger: current channel failed, but no safe eligible target exists.
- Expected Behavior: open incident, expose no-target blocker, do not move, possibly suspend L3 for scope.
- Terminal State: `STOP_SAFE` or `INCIDENT_OPEN`.
- V7 Classification: Already Exists.

### Target Lost Before Apply

- Trigger: target was safe during planning but fails before apply.
- Expected Behavior: final live validation fails, no apply, incident records target-lost reason, optional replan only if certified; L3 current spec should make this explicit.
- Terminal State: `STOP_SAFE`.
- V7 Classification: Needs Extension.

### Verification Failed

- Trigger: apply completed but target route/service verification fails.
- Expected Behavior: rollback or contain, classify from terminal state, do not count success.
- Terminal State: `ROLLBACK_SUCCESS`, `ROLLBACK_FAILURE`, or containment incident.
- V7 Classification: Already Exists.

### Rollback Failed

- Trigger: verification failed and rollback cannot prove safe state.
- Expected Behavior: suspend, incident escalation, no further autonomy for scope, operator-visible unsafe state.
- Terminal State: `ROLLBACK_FAILURE` / `SUSPENDED`.
- V7 Classification: Already Exists.

### Duplicate Event

- Trigger: same failure event arrives multiple times or source emits repeated samples.
- Expected Behavior: collapse into existing incident/execution key; no duplicate execution; duplicate is observed, not acted upon.
- State Transitions: active incident remains active; no second `EXECUTING`.
- V7 Classification: Needs Extension.

### Repeated Failure

- Trigger: same source or same target fails repeatedly after attempts.
- Expected Behavior: open circuit breaker, increase backoff, suspend scope, require operator/OMP review after budget exhausted.
- Terminal State: `SUSPENDED`.
- V7 Classification: Needs Extension.

### Multiple Incidents

- Trigger: several channels fail or same provider/service family fails in parallel.
- Expected Behavior: merge shared root cause where appropriate; split independent blast scopes; enforce global and per-scope budgets.
- V7 Classification: Needs Extension.

### Event Collapse

- Trigger: many users on same failed current channel generate many wake events.
- Expected Behavior: one incident/context per source/failure family; select bounded subjects according to certified blast radius; do not start one runtime loop per user without dedupe.
- V7 Classification: Needs Extension.

### Race Condition

- Trigger: source, target, authority, rollback, or user assignment changes between plan and apply.
- Expected Behavior: material state change -> STOP_SAFE; non-material observation update -> continue if identity and gates remain valid.
- V7 Classification: Already Exists.

### Partial Success

- Trigger: some verification dimensions pass and others fail, or one user moves while service subset remains broken.
- Expected Behavior: do not collapse to SUCCESS; classify per terminal proof; keep incident partially open or rollback/contain.
- V7 Classification: Needs Extension.

### Slow Verification

- Trigger: verification takes longer than expected.
- Expected Behavior: bounded timeout, no infinite wait, rollback/contain/unknown-state incident depending on mutation status.
- V7 Classification: Needs Extension.

### Timeout

- Trigger: plan/apply/verify/rollback exceeds certified time bound.
- Expected Behavior: terminal timeout classification and circuit-breaker accounting; if mutation risk exists, rollback/contain.
- V7 Classification: Needs Extension.

### Unknown State

- Trigger: required truth source unavailable, contradictory, or owner cannot prove state.
- Expected Behavior: STOP_SAFE before mutation; if after mutation, incident remains open and autonomy suspends for scope until state proven.
- V7 Classification: Needs Extension.

### Authority Lost

- Trigger: authority generation changes or envelope revoked during cycle.
- Expected Behavior: stop before apply; if after apply, finish verification/rollback/incident closure but do not start new action.
- V7 Classification: Already Exists / Needs Extension for post-apply semantics.

### Target Degraded

- Trigger: target passes basic liveness but shows degradation.
- Expected Behavior: target ineligible for L3 unless degradation is explicitly acceptable under policy; choose alternate or STOP_SAFE.
- V7 Classification: Already Exists.

### Recovery During Execution

- Trigger: source recovers while L3 cycle is underway.
- Expected Behavior: before commit/apply, abort if emergency no longer exists; after apply, verify terminal result and learn; do not oscillate back automatically.
- V7 Classification: Needs Extension.

### Recovery After Suspend

- Trigger: failed source or target stabilizes after suspension.
- Expected Behavior: require recovery admission, stable window, half-open/probe, and OMP/certified authority before resuming.
- V7 Classification: Needs Extension.

### Operator Override / Kill Switch

- Trigger: operator freezes or disables L3.
- Expected Behavior: no new autonomous execution; in-flight operation finishes only as safety requires: verify, rollback, or contain.
- V7 Classification: Already Exists.

### Idempotent Replay

- Trigger: runtime replay after process restart or duplicate delivery.
- Expected Behavior: same semantic execution key maps to same incident/decision/attempt; no duplicate apply.
- V7 Classification: Already Exists / Needs Extension for explicit incident replay.

### Late / Stale Event

- Trigger: event arrives after source recovered or after incident closed.
- Expected Behavior: compare generation/time/current state; ignore or record as stale; no mutation.
- V7 Classification: Needs Extension.

## State Transition Library

Canonical reusable transitions for L3 behavior:

| Transition | Required meaning | Missing detail to consider for L3 |
| --- | --- | --- |
| `IDLE -> WAKE` | approved failure event starts observation. | Wake dedupe key. |
| `WAKE -> OBSERVE` | read current reality without mutation. | Event generation and stale-event handling. |
| `OBSERVE -> CLASSIFY` | map observed failure to L3 or no-action. | Event collapse for same source/failure. |
| `CLASSIFY -> INCIDENT_OPEN` | create/merge incident context. | Merge/split rules. |
| `INCIDENT_OPEN -> PLAN_READY` | affected subject and target selected. | Parallel incident arbitration. |
| `PLAN_READY -> READY` | authority and live gates pass. | Target-lost and budget checks. |
| `READY -> EXECUTING` | one bounded mutation begins. | Retry budget must already permit attempt. |
| `EXECUTING -> VERIFYING` | mutation attempted; prove terminal state. | Timeout and partial-success handling. |
| `VERIFYING -> ROLLBACK` | verification failed. | Rollback timeouts and rollback failure. |
| `ROLLBACK -> INCIDENT_OPEN` | rollback failed or unknown. | Suspension and operator escalation. |
| `LEARNING -> REPORTING` | terminal result becomes evidence. | Partial/unknown states must not become success. |
| `REPORTING -> SLEEP` | no active work remains. | Active incident must be closed or suspended. |
| `ANY -> SUSPENDED` | breaker/kill switch/unknown unsafe state. | Resume contract. |

## Failure Library

| Failure mode | Production-grade response | V7 status |
| --- | --- | --- |
| False positive source failure | Thresholds, freshness, owner evidence, rollback/contain. | Already Exists. |
| No safe target | Incident + STOP_SAFE. | Already Exists. |
| Target becomes unhealthy before apply | Final validation blocks. | Needs Extension in L3 behavior wording. |
| Target becomes unhealthy after apply | Verification fails -> rollback/contain. | Already Exists. |
| Duplicate wake event | Idempotent event collapse. | Needs Extension. |
| Late event | Generation/TTL check; ignore if stale. | Needs Extension. |
| Parallel source failures | Merge/split incidents and enforce global budgets. | Needs Extension. |
| Verification timeout | Treat as non-success; rollback/contain/incident. | Needs Extension. |
| Rollback timeout | Escalate and suspend. | Needs Extension. |
| Rollback failure | Incident + suspension + no success credit. | Already Exists. |
| Unknown state | Quarantine or suspend, never guess. | Needs Extension. |
| Repeated failover loop | Backoff, breaker, hold-down. | Needs Extension. |
| Authority revoked | Stop before mutation; after mutation finish safety closure only. | Needs Extension. |
| Operator kill switch | Stop new actions immediately. | Already Exists. |

## Recovery Library

Reusable recovery behaviors:

1. Pre-apply abort: if source recovers or target fails before mutation, L3 stops without movement.
2. Post-apply verification: after mutation, the system verifies the actual new state instead of undoing based on old assumptions.
3. Rollback success: failed verification is recovered and classified separately.
4. Rollback failure: autonomy suspends and incident stays visible.
5. Recovery admission: recovered source/target cannot immediately receive users without stable evidence.
6. Half-open probe: after breaker/suspension, only a certified small probe may resume automation.
7. No automatic return: L3 failover does not automatically move users back to recovered source; that belongs to recovery/rebalance policy.

## Retry Library

Production systems rarely allow unbounded retry. Relevant patterns:

| Retry behavior | Meaning | V7 fit |
| --- | --- | --- |
| Max attempts per incident | Only N attempts before suspend. | Needs Extension. |
| Max attempts per source/target/window | Prevents repeated bad target selection. | Needs Extension. |
| Exponential backoff | Delay grows after repeated failure. | Needs Extension. |
| Jitter | Prevents synchronized waves. | Reusable later, not critical for one-user L3. |
| Retry budget | Binds retries to error/safety budget. | Needs Extension. |
| No retry after mutation unless certified | Avoids hidden second movement. | Already Exists. |
| Idempotent replay is not retry | Replay may finish the same attempt; it must not create a new attempt. | Needs Extension. |

## Rollback Library

| Rollback behavior | Required production meaning | V7 status |
| --- | --- | --- |
| Rollback plan before apply | Mutating action has restore/containment plan first. | Already Exists. |
| Rollback verification | Rollback result must be verified. | Already Exists / partial by class. |
| Rollback timeout | Timeout becomes incident/suspension. | Needs Extension. |
| Rollback failure | Do not mark success; escalate. | Already Exists. |
| No-rollback certification | Some actions are compensating/containment rather than exact undo. | Already Exists. |
| Rollback budget | Repeated rollback indicates unsafe action class or target. | Needs Extension. |

## Incident Library

Production-grade incident behavior for L3 should include:

- incident key: source channel, failure family, service family, authority envelope, active generation;
- affected subject set: users/cohorts currently harmed;
- merge rule: same key joins existing incident;
- split rule: different source/failure/service/authority/blast scope creates separate incident;
- terminal states: success, no target, stop safe, rollback success, rollback failure, unknown, suspended;
- visibility: operator can see why action happened or did not happen;
- closure rule: incident closes only after terminal outcome, learning, and report;
- resume rule: suspended incident resumes only through certified recovery/admission path;
- stale-event rule: events older than incident generation cannot trigger mutation.

## Operator Interaction

Production systems vary on how much human approval remains, but they converge on a few operator-visible behaviors:

- operators define policy, SLO/risk, authority, and kill switches;
- runtime handles certified low-level failover inside bounds;
- broad, ambiguous, repeated, or unknown failures escalate to operator review;
- operator sees incident reason, impact, target, gates, rollback state, and terminal result;
- human approval is not normally required for every low-risk certified failover in mature systems, but certification and policy authority must exist first.

## Common Patterns

1. Health evidence is owner-specific and thresholded.
2. Runtime is idempotent and event-driven.
3. Controllers reconcile current state rather than trusting old events.
4. Failover is bounded by blast radius and capacity.
5. Retry/backoff/breakers prevent self-inflicted incidents.
6. Verification defines success; apply alone never defines success.
7. Rollback/containment is prepared before risky mutation.
8. Unknown state is unsafe, not neutral.
9. Incidents are mergeable/splittable stateful objects.
10. Learning consumes terminal outcomes only.

## Behavior Comparison Matrix

| Behavior | Kubernetes | Envoy/Istio/Linkerd | AWS/Azure/GCP | Cloudflare | Network routing | HAProxy/NGINX | V7 L3 today |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Thresholded failure | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Event reconciliation | Yes | Controller dependent | Yes | Yes | Protocol dependent | Health-check loop | Partial |
| Duplicate suppression | Yes | Config/control-plane dependent | Yes | Yes | Protocol state | Health state | Partial |
| Incident merge/split | Condition/event dependent | Mostly external | Alarm/incident systems | Pool/monitor state | NOC/telemetry | External | Missing explicit |
| Target selection | Scheduler/service/controller | LB/mesh route | LB/DNS/managed service | Pool steering | Routing preference | Upstream selection | Yes |
| Final revalidation | Yes | Yes | Yes | Yes | Convergence/adjacency | Health state | Yes |
| Verification | Readiness/status | Metrics/health | Health/alarm | Monitor/traffic | Protocol state | Health check | Yes |
| Rollback/contain | Rollout undo/reconcile | Route/config revert | Rollback/replacement | fallback/revert | route/config rollback | disable/backup | Yes |
| Retry budget/backoff | Yes | Yes | Yes | Partial | dampening/hold-down | retry/timeouts | Missing explicit |
| Circuit breaker | Backoff/conditions | Yes | Alarms/breakers | Pool fallback | dampening | passive/active health | Partial |
| Unknown-state suspend | Yes | External/control plane | Yes | Yes | operator/protocol | fail closed/external | Missing explicit |

## V7 Coverage

Already covered by existing V7 L3 / Runtime / Policy owners:

- emergency-only L3 boundary;
- current-channel failure entry;
- affected-user discovery;
- safe target requirement;
- freshness requirement;
- authority envelope;
- rollback/restore readiness;
- live readiness gates;
- final verification;
- rollback classification;
- incident visibility;
- learning from terminal outcomes;
- duplicate execution test family;
- STOP_SAFE on missing mandatory gates.

## Missing Behaviors

| Missing behavior | Why production systems need it | Does V7 need it? | Owner mapping | Architecture impact | Implementation impact |
| --- | --- | --- | --- | --- | --- |
| Event collapse | Prevent one failure from spawning many execution loops. | Yes | Autonomous Runtime event dispatch, L3 incident owner, CPS. | None | Add event/incident keying and dedupe behavior. |
| Incident merge/split | Avoid duplicate incidents while preserving independent blast scopes. | Yes | Incident/report lifecycle, planner subject mapping. | None | Define merge/split keys and state transitions. |
| Retry budget | Prevent repeated unsafe attempts. | Yes | Execution budget, Policy 009, circuit breaker. | None | Add attempt/window counters and STOP/SUSPEND terminal states. |
| Backoff | Avoid retry storms and oscillation. | Yes | Anti-flap, movement protection. | None | Add bounded backoff after failed attempts. |
| Target lost during execution | Avoid stale safe target assumption. | Yes | Runtime eligibility, material state, L3 readiness. | None | Make explicit STOP_SAFE before apply / rollback after apply behavior. |
| Partial success | Prevent misleading success records. | Yes | Terminal classification, verification, learning. | None | Add partial terminal state or incident-open rule. |
| Unknown state quarantine | Never guess when truth source is missing. | Yes | Runtime STOP_SAFE/SUSPENDED, incident owner. | None | Add quarantine/suspension behavior for post-mutation unknown state. |
| Recovery during execution | Avoid unnecessary movement or oscillation. | Yes | Runtime eligibility, verification, Recovery Admission. | None | Define pre-apply abort vs post-apply terminal verification. |
| Resume after suspend | Avoid immediate repeat after breaker. | Yes | Policy 003, Policy 009, OMP certification. | None | Add half-open/stable-window resume contract. |
| Late/stale event rule | Avoid acting on old failures. | Yes | Freshness, owner-issued version, incident generation. | None | Compare event generation to current incident/world generation. |
| Parallel incident arbitration | Avoid exceeding global blast/risk budgets. | Yes later | Blast radius, execution budget, OMP. | None | Start serial-only; add per-scope/global budget as L3 matures. |
| Budget exhaustion terminal state | Make "too many failures" explicit. | Yes | Circuit breaker, report lifecycle, CPS. | None | Add `BUDGET_EXHAUSTED` / `SUSPENDED` reason. |

## Recommendations

Do not modify Runtime or L3 specification during this discovery stage.

Recommended next step:

1. Extend the existing L3 capability specification, not architecture, with a Behavior Library section.
2. Add explicit behavior contracts for event collapse, incident merge/split, retry/backoff, partial success, unknown-state quarantine, target-lost, stale/late event, recovery during execution, and budget exhaustion.
3. Keep all implementation mapped to existing owners.
4. Do not enable automation until L3 implementation and certification satisfy those behavior contracts.

## References

- RFC 5880, Bidirectional Forwarding Detection: https://www.rfc-editor.org/rfc/rfc5880
- Kubernetes Pod lifecycle, probes, readiness and backoff behavior: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Kubernetes deployments, rollout status, progress and rollback: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes controller concepts: https://kubernetes.io/docs/concepts/architecture/controller/
- Envoy outlier detection: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier
- Envoy circuit breaking: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/circuit_breaking
- Envoy active health checking: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking
- Istio traffic management, retries, timeouts, outlier detection: https://istio.io/latest/docs/concepts/traffic-management/
- Linkerd retries and timeouts: https://linkerd.io/2.15/features/retries-and-timeouts/
- AWS Route 53 DNS failover: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
- AWS Elastic Load Balancing target health checks: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
- AWS CodeDeploy rollback and redeploy: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
- Azure Traffic Manager endpoint monitoring and failover: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Cloudflare Load Balancing traffic steering: https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/
- Google SRE, Handling Overload: https://sre.google/sre-book/handling-overload/
- Google SRE, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/
- Google Borg paper: https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/
- Netflix Hystrix behavior model: https://github.com/Netflix/Hystrix/wiki/How-it-Works
- Consul service resolver failover behavior: https://developer.hashicorp.com/consul/docs/connect/config-entries/service-resolver
- HAProxy configuration, health checks and server state options: https://docs.haproxy.org/3.0/configuration.html
- NGINX upstream health/failover options: https://nginx.org/en/docs/http/ngx_http_upstream_module.html
- Cilium Kubernetes service load-balancing integration: https://docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/

## Validation

Behavior Audit: `PASS`.

Industry Audit: `PASS`.

Runtime Audit: `PASS` - no Runtime behavior changed.

Owner Audit: `PASS` - missing behaviors map to existing owners.

Duplicate Behavior Audit: `PASS` - this document records discovery only and does not duplicate L3 specification.

Conflict Audit: `PASS` - no discovered behavior requires architecture replacement.

Final verdict:

```text
L3_BEHAVIOR_DISCOVERY_COMPLETE
```
