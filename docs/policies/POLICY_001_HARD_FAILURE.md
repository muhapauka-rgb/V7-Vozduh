# POLICY_001_HARD_FAILURE

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: hard failure
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy defines the research basis for complete channel or server hard failure.

Hard failure means the system has evidence that a channel, server, endpoint, peer, node, route, or service target is not able to carry the expected traffic at all.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

Stage 1 all-policy research pass preserved and extended the earlier hard-failure research. No accumulated hard-failure findings were removed.

## Problem

Production systems must distinguish hard failure from ordinary slowness, overload, maintenance, partial degradation, recovery, and policy-denied traffic.

If hard failure is detected too slowly, users remain on a dead path and availability falls.

If hard failure is detected too aggressively, false positives remove usable capacity, shift load to remaining capacity, and can create cascading failure.

If reaction is not bounded, a local failure can become a global incident by moving too much traffic too quickly.

If recovery is admitted too quickly, a repaired target can fail again under full load.

Therefore mature systems treat hard failure as a closed loop:

```text
probe or observe
  -> classify unavailable
  -> remove or reduce traffic
  -> continue checking
  -> verify alternate path
  -> admit recovery gradually or with thresholds
  -> log outcome
```

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Hard failure must be based on explicit liveness evidence such as missed heartbeats, failed probes, failed health checks, dead sessions, down adjacencies, or unavailable targets. | `STRONG` | Cisco, Juniper, Arista, Cloudflare, AWS, Azure, GCP, Kubernetes, Envoy, HAProxy, NGINX, BGP, OSPF, IS-IS, BFD RFCs | `HIGH`: network vendors, hyperscalers, cloud LBs, Kubernetes, proxies, RFCs | None for the need for liveness evidence. |
| A single noisy observation should not normally trigger hard-failure action; mature systems use timers, multipliers, consecutive failures, hold times, or state machines. | `STRONG` | BFD, BGP, OSPF, IS-IS, Cloudflare, AWS ELB, Azure Traffic Manager, GCP health checks, HAProxy, NGINX, Kubernetes | `HIGH`: repeated across RFCs, cloud platforms, proxies, and orchestrators | Some local link signals can be immediate, but still enter a protocol/state-machine reaction. |
| Once hard failure is classified, traffic or route eligibility is automatically removed or de-preferred inside preconfigured policy. | `STRONG` | Routing protocols, BFD clients, Cloudflare, AWS, Azure, GCP, Kubernetes EndpointSlices, Envoy, Istio, HAProxy, NGINX | `HIGH`: all major production families converge on automatic reaction inside policy | Human intervention remains for broad incidents or authority expansion. |
| Hard-failure reaction must continue verification and recovery checks after removal. | `STRONG` | Cloudflare, AWS, Azure, GCP, Kubernetes, HAProxy, NGINX, Envoy, routing protocols | `HIGH`: common in health-check loops and routing reconvergence | None for continued checking. |
| Failover must be bounded by fallback availability, capacity, routing policy, or blast-radius controls. | `MEDIUM` | Google SRE, Cloudflare fallback pools, AWS/Azure/GCP LBs, MPLS FRR, SD-WAN, service mesh, HAProxy/NGINX pools | `MEDIUM_HIGH`: strong production evidence, but exact guard differs by architecture | Some protocols perform local repair before global capacity context is available. |
| Multi-vantage health improves global hard-failure decisions. | `MEDIUM` | Cloudflare, Azure Traffic Manager, Route 53, global LB practice | `MEDIUM`: strong in global/DNS/edge systems | Local routing protocols and node-local proxies rely on local evidence. |
| Fast sub-second or near-real-time detection is appropriate only when the system can tolerate false-positive risk and control-plane load. | `MEDIUM` | BFD vendors, Juniper timer guidance, Arista/Cisco, Google SRE warnings | `MEDIUM`: strong network evidence plus SRE cautions | DNS/global health systems often prefer slower thresholds. |
| Fail-open behavior when all targets are unhealthy is architecture-specific, not universal. | `WEAK` | AWS ALB, some load-balancer/fallback designs | `MEDIUM`: documented in specific systems | Security/correctness-sensitive systems may fail closed. |
| Local repair before global recomputation is useful for MPLS/routing but not a universal hard-failure policy. | `WEAK` | MPLS RSVP-TE FRR, routing operations | `MEDIUM`: strong RFC/vendor basis for routing only | Application/LB/cloud systems use different recovery models. |

### Industry Consensus Research

#### Cisco

Cisco production routing practice uses BFD and protocol/object tracking to detect hard failures faster than routing-protocol hello timers alone. Cisco IOS XE has a dedicated BFD configuration guide, and BFD is used with static routes, OSPFv3, IS-IS, and other routing clients.

- Definition of hard failure: BFD session down, tracked object down, route reachability lost, or first-hop/link redundancy state lost.
- Detection rules: control packets or tracked probes fail for configured intervals/multipliers.
- Failure thresholds: BFD interval and multiplier; IP SLA/object tracking thresholds depend on configured probes.
- Reaction strategy: notify routing clients, withdraw or de-prefer routes, trigger first-hop redundancy or static route failover.
- Safety gates: protocol adjacency state, object tracking state, dampening where configured, backup route availability.
- Rollback strategy: restoration follows routing reconvergence or tracked-object recovery, not manual per-packet approval.
- Verification: route/client state and BFD/session state.
- Recovery interaction: recovered sessions/routes can be reintroduced through routing policy and timers.
- Operator role: configure policies, timers, tracking, and backup paths; runtime reaction is automatic.
- Automation level: high inside configured routing policy.
- Tradeoffs: faster detection increases control traffic and false-positive risk.
- Why this design exists: routing protocols alone can be too slow for modern traffic loss tolerance.
- Known limitations: aggressive timers can flap; failure detection is only as good as the monitored path.

#### Juniper

Junos documents BFD as a simple hello mechanism that detects neighbor failure when replies stop arriving after a specified interval. Juniper also distinguishes centralized, distributed, inline, and hardware-assisted BFD, with timer guidance and damping.

- Definition of hard failure: neighbor/path liveness down or BFD session down.
- Detection rules: periodic BFD packet exchange; no reply after configured interval/multiplier.
- Failure thresholds: Juniper recommends different minimum intervals by mode, for example centralized versus distributed BFD; hold-down and damping can suppress brief flaps.
- Reaction strategy: notify routing clients/protocols; remove affected adjacency or route from usable forwarding decisions.
- Safety gates: platform support, centralized versus distributed mode, NSR/GRES constraints, damping, hold-down intervals.
- Rollback strategy: session up and routing client reconvergence restore eligibility.
- Verification: BFD session state, routing table, protocol adjacency.
- Recovery interaction: damping and hold-down avoid immediate oscillation after short failures.
- Operator role: set timer aggressiveness and platform mode; runtime detection and notification are automatic.
- Automation level: high for detection and route-client notification.
- Tradeoffs: hardware/inline BFD improves latency but has platform limitations; very fast timers can produce flapping under congestion.
- Why this design exists: forwarding-plane liveness can fail independently of control-plane protocol health.
- Known limitations: tunnel, VXLAN, LAG, chassis, authentication, and platform constraints vary.

#### Arista

Arista EOS uses RFC 5880 BFD behavior. EOS exchanges BFD control packets and informs the requesting protocol when a configured number of successive packets are missed. EOS supports asynchronous mode and echo function.

- Definition of hard failure: BFD session down due to missing successive control packets or echo interruption.
- Detection rules: per-interface transmit interval, receive interval, and multiplier.
- Failure thresholds: missed-packet multiplier and detect time.
- Reaction strategy: requesting routing protocol responds to loss of connectivity.
- Safety gates: BFD per-link mode for port channels, RFC-compliant micro sessions where configured, routing client behavior.
- Rollback strategy: session up and protocol reconvergence.
- Verification: BFD session state, detect time, client protocol state.
- Recovery interaction: returning BFD session re-enables protocol eligibility.
- Operator role: configure intervals/multipliers and protocol attachment.
- Automation level: high after configuration.
- Tradeoffs: BFD detects quickly but the routing protocol is responsible for final reaction.
- Why this design exists: separates fast failure detection from protocol-specific policy.
- Known limitations: unsupported demand mode in EOS and port-channel behavior differences.

#### Cloudflare

Cloudflare Load Balancing determines endpoint and pool health through monitors, health checks, regional majority rules, consecutive up/down parameters, pool thresholds, and fallback pools.

- Definition of hard failure: endpoint cannot answer monitor request at all, cannot answer within timeout, returns unexpected status/body, or pool falls below health threshold.
- Detection rules: health monitor requests from multiple data centers and regions.
- Failure thresholds: majority of data centers/regions, `consecutive_down`, `consecutive_up`, pool health threshold.
- Reaction strategy: remove unhealthy endpoints or critical pools from steering; use fallback pool when all default pools fail.
- Safety gates: regional majority, consecutive transition counts, fallback pool, global health events.
- Rollback strategy: health checks continue and recovered endpoints/pools return when enough checks pass.
- Verification: monitor event logs, endpoint/pool/load balancer health status.
- Recovery interaction: continuing health checks, consecutive up counts, and pool status restore eligibility.
- Operator role: configure monitors, thresholds, steering, fallback pools, and regions.
- Automation level: high inside configured load-balancing policy.
- Tradeoffs: global accuracy improves with multiple vantage points but detection is bounded by probe interval and thresholds.
- Why this design exists: single-probe failure is not reliable enough for global traffic steering.
- Known limitations: fallback can still serve traffic when all normal pools are unhealthy; monitoring gaps make health unknown.

#### Google SRE

Google SRE material treats hard failures as dangerous because failover can overload the remaining system. The Cascading Failures chapter shows that when one cluster fails and load shifts to another, capacity can collapse if failover is not constrained. Maglev describes Google production load balancing with ECMP, consistent hashing, and connection tracking to reduce fault impact.

- Definition of hard failure: cluster, task, server, or endpoint cannot serve useful work; may crash, fail health checks, miss deadlines, or disappear from serving capacity.
- Detection rules: health checks, load balancer signals, task state, error/latency/deadline symptoms.
- Failure thresholds: system-specific SLOs, health checks, task schedulers, load-balancing controllers.
- Reaction strategy: remove failed capacity, shift traffic, protect remaining capacity with overload controls and graceful degradation.
- Safety gates: capacity testing, load shedding, backoff, jitter, client throttling, avoiding positive feedback loops.
- Rollback strategy: restore traffic only after capacity can safely handle it.
- Verification: served traffic, error rates, capacity, health check state, postmortems.
- Recovery interaction: recovery must consider overload and warm-up, not just binary health.
- Operator role: define SLOs, capacity, automation, and incident response.
- Automation level: high in load-balancing/control systems, with human incident response for broad outages.
- Tradeoffs: fast failover can increase blast radius if remaining capacity is insufficient.
- Why this design exists: distributed systems fail by feedback loops, not only by isolated component loss.
- Known limitations: health checks can fail because of overload rather than root-cause failure.

#### Google Traffic Engineering

Google Maglev uses software load balancers deployed as distributed systems, with ECMP distributing traffic to Maglev machines and Maglev distributing to service endpoints. Consistent hashing and connection tracking reduce the effect of machine faults and failures on connection-oriented protocols.

- Definition of hard failure: load balancer or endpoint machine fault affecting packet handling or endpoint serviceability.
- Detection rules: fleet membership, endpoint health, connection tracking, routing distribution.
- Failure thresholds: production-specific health and membership state.
- Reaction strategy: redistribute traffic across remaining Maglev machines and service endpoints.
- Safety gates: consistent hashing, ECMP, connection tracking, distributed capacity.
- Rollback strategy: reintroduce capacity when healthy.
- Verification: packet processing, connection continuity, endpoint distribution.
- Recovery interaction: recovered load balancer or endpoint re-enters distribution.
- Operator role: design capacity and fleet-level policy.
- Automation level: high.
- Tradeoffs: distributed LB improves scale but requires careful consistency and connection handling.
- Why this design exists: hardware load balancers do not scale or fail as flexibly as large software fleets.
- Known limitations: public paper focuses on LB architecture rather than full operational policy.

#### Netflix

Netflix Eureka is used for service discovery, middle-tier load balancing, failover, and instance registration in AWS. Services renew leases with heartbeats; instances that fail renewal are removed from the registry after a configured window. Clients cache registry data to survive Eureka server outages.

- Definition of hard failure: service instance no longer renews lease or is removed from registry; registry server unavailable; instance disappears in cloud.
- Detection rules: service heartbeat and lease renewal.
- Failure thresholds: default renewal every 30 seconds and removal after missed renewals around 90 seconds in the documented architecture.
- Reaction strategy: deregister failed instances from discovery; clients avoid them through updated/cached registry.
- Safety gates: client-side cache, zone/region isolation, peer replication, self-preservation against partitions.
- Rollback strategy: renewed registration/heartbeat restores visibility.
- Verification: registry state, client lookup, monitoring/alerting.
- Recovery interaction: re-registration and lease renewal.
- Operator role: define discovery, registration, and regional topology.
- Automation level: high inside configured discovery model.
- Tradeoffs: cached registry increases resilience but can serve stale membership.
- Why this design exists: cloud instances appear and disappear dynamically, making static load balancer membership insufficient.
- Known limitations: lease-based detection is slower than BFD or local LB probes; partition behavior requires safety bias.

#### AWS

AWS Route 53, Elastic Load Balancing, ECS, and Auto Scaling represent several hard-failure models. Route 53 uses health checks and DNS failover. Application Load Balancer performs target health checks, removes unhealthy targets, and restores them after enough successes. Auto Scaling can replace unhealthy instances and treats non-running instance states as immediate failures.

- Definition of hard failure: resource unavailable, target timeout, response-code mismatch, failed health checks, stopped/terminated instance, impaired status checks, or task unhealthy in target group.
- Detection rules: HTTP/HTTPS/TCP/gRPC health checks, EC2 status checks, target health, service events.
- Failure thresholds: ALB unhealthy and healthy threshold counts; Route 53 health-check status; Auto Scaling health status.
- Reaction strategy: remove target from service, route DNS to healthy resource, replace instance, or report service unhealthy.
- Safety gates: consecutive failure thresholds, enabled AZs, target state, deregistration delay/connection draining.
- Rollback strategy: healthy thresholds restore target; replacement instance enters service after health passes.
- Verification: target health status, reason codes, health check logs, Auto Scaling lifecycle state.
- Recovery interaction: ALB and Route 53 continue checking unhealthy resources; Auto Scaling replacement provides fresh capacity.
- Operator role: configure checks, thresholds, target groups, DNS failover, and replacement policy.
- Automation level: high after configuration.
- Tradeoffs: ALB fails open if all targets are unhealthy; DNS failover depends on TTL/cache behavior.
- Why this design exists: managed services must preserve availability without per-target human approval.
- Known limitations: fail-open and DNS cache mean some traffic may still hit failed targets.

#### Azure

Azure Traffic Manager includes endpoint monitoring and automatic endpoint failover. It probes endpoints via HTTP, HTTPS, or TCP, with configurable protocol, port, path, expected status codes, probe interval, tolerated failures, and timeout.

- Definition of hard failure: endpoint returns unexpected status, no response before timeout, wrong TCP response, timeout, or any connection issue making the endpoint unreachable.
- Detection rules: probes from multiple locations with configured protocol/path/port.
- Failure thresholds: tolerated consecutive failures, probe interval, timeout, and status code ranges.
- Reaction strategy: mark endpoint `Degraded` and stop returning it in DNS responses; choose alternate endpoint according to routing method.
- Safety gates: multiple probe locations, DNS TTL, endpoint/profile state, routing method, nested profiles.
- Rollback strategy: continuous probes detect endpoint recovery and restore DNS eligibility.
- Verification: endpoint monitor status and profile monitor status.
- Recovery interaction: Traffic Manager continues checking degraded endpoints and returns them after successful checks.
- Operator role: configure monitor and routing policy.
- Automation level: high after configuration.
- Tradeoffs: DNS-level systems cannot affect existing connections and are constrained by TTL/cache.
- Why this design exists: region and endpoint failures need automated new-connection steering.
- Known limitations: if all endpoints are degraded, best-effort behavior can return degraded endpoints.

#### GCP

Google Cloud Load Balancing uses health check resources implemented by dedicated software tasks. Backends become healthy or unhealthy based on configurable sequential successes or failures, and health state determines eligibility to receive new requests or connections.

- Definition of hard failure: backend fails health probes enough consecutive times or does not satisfy success criteria.
- Detection rules: dedicated health-check probes over configured protocols and ports.
- Failure thresholds: configurable successful and failed probe counts.
- Reaction strategy: unhealthy backends are removed from receiving new requests/connections.
- Safety gates: health check compatibility with LB/backend type, protocol selection, special health-check paths.
- Rollback strategy: sequential successful probes restore backend health.
- Verification: backend health state, health check logging, LB status.
- Recovery interaction: recovered backend re-enters serving eligibility after passing checks.
- Operator role: configure compatible health checks and LB policy.
- Automation level: high after configuration.
- Tradeoffs: health checks are explicit resources that must match backend behavior.
- Why this design exists: request eligibility must follow observed backend availability.
- Known limitations: misconfigured probes can falsely remove healthy capacity.

#### Meta

Public Meta material found during this stage did not expose a directly comparable production hard-failure routing policy for channel/server failover. Meta engineering artifacts do show mature production emphasis on catching failures before they affect large backend systems, but this is not enough to populate operational failover policy content.

- Definition of hard failure: `SOURCE_GAP`.
- Detection rules: `SOURCE_GAP`.
- Failure thresholds: `SOURCE_GAP`.
- Reaction strategy: `SOURCE_GAP`.
- Safety gates: `SOURCE_GAP`.
- Rollback strategy: `SOURCE_GAP`.
- Verification: `SOURCE_GAP`.
- Recovery interaction: `SOURCE_GAP`.
- Operator role: `SOURCE_GAP`.
- Automation level: `SOURCE_GAP`.
- Tradeoffs: `SOURCE_GAP`.
- Why this design exists: `SOURCE_GAP`.
- Known limitations: no authoritative public hard-failure policy found in this stage.

#### Microsoft

Microsoft public operational evidence for this policy is represented by Azure Traffic Manager and Azure platform load-balancing documentation. No separate public Microsoft internal traffic-engineering hard-failure policy was found in this stage.

- Definition of hard failure: endpoint/probe failure in Azure Traffic Manager.
- Detection rules: HTTP/HTTPS/TCP probes, expected status, timeouts, consecutive tolerated failures.
- Failure thresholds: Traffic Manager probe interval, timeout, tolerated failures.
- Reaction strategy: DNS steering away from degraded endpoint.
- Safety gates: endpoint/profile state, multi-location probes, DNS TTL, routing policy.
- Rollback strategy: restored endpoint health returns to DNS responses.
- Verification: endpoint monitor status.
- Recovery interaction: continuous probe and status recomputation.
- Operator role: configure profile and monitoring.
- Automation level: high after configuration.
- Tradeoffs: DNS cache and existing connections remain outside immediate control.
- Why this design exists: DNS-based global failover is simple and broad but not instantaneous.
- Known limitations: same as Azure Traffic Manager.

#### Apple

No authoritative Apple production hard-failure routing or server-failover policy comparable to Cisco, Cloudflare, Google, AWS, Azure, Kubernetes, Envoy, HAProxy, or NGINX was found in this stage.

- Definition of hard failure: `SOURCE_GAP`.
- Detection rules: `SOURCE_GAP`.
- Failure thresholds: `SOURCE_GAP`.
- Reaction strategy: `SOURCE_GAP`.
- Safety gates: `SOURCE_GAP`.
- Rollback strategy: `SOURCE_GAP`.
- Verification: `SOURCE_GAP`.
- Recovery interaction: `SOURCE_GAP`.
- Operator role: `SOURCE_GAP`.
- Automation level: `SOURCE_GAP`.
- Tradeoffs: `SOURCE_GAP`.
- Why this design exists: `SOURCE_GAP`.
- Known limitations: no public comparable source found; do not infer Apple-specific policy.

#### Kubernetes

Kubernetes uses probes, Pod conditions, controllers, desired-state reconciliation, readiness gates, EndpointSlices, and restart policies. It separates liveness from readiness: liveness restarts a stuck container; readiness controls whether traffic should be sent.

- Definition of hard failure: container failed liveness, pod not ready, node dies, runtime sandbox unavailable, or container exits according to restart policy.
- Detection rules: kubelet probes, container state, node/pod lifecycle, readiness gates.
- Failure thresholds: probe failure thresholds, periods, timeouts, restart backoff.
- Reaction strategy: restart unhealthy containers; remove not-ready Pods from Service EndpointSlices; controllers replace failed Pods.
- Safety gates: startup probes, readiness gates, restart backoff, graceful termination, desired-state reconciliation.
- Rollback strategy: controller reconciles back to desired state; readiness gates restore service eligibility.
- Verification: Pod phase, Pod conditions, EndpointSlice membership, container status.
- Recovery interaction: recovered Pod must become Ready before receiving Service traffic.
- Operator role: define probes, readiness gates, PDBs, controller policy.
- Automation level: high after declared desired state.
- Tradeoffs: bad probes can cause restart loops or remove healthy capacity.
- Why this design exists: application runtime health and traffic eligibility are different decisions.
- Known limitations: node/network partitions and bad probes can produce ambiguous status.

#### Envoy

Envoy supports active health checking per upstream cluster and passive health checking through outlier detection. It supports HTTP, gRPC, L3/L4, Redis, and Thrift checks, configurable intervals, failure/success counts, event logging, health-check identity, and fast failure via an immediate-fail signal.

- Definition of hard failure: upstream host fails active check, passive outlier criteria, connection, protocol, or service identity check.
- Detection rules: active probes or observed traffic failures.
- Failure thresholds: check interval, failures required, successes required, passive outlier thresholds.
- Reaction strategy: exclude failed host from load balancing.
- Safety gates: event logs, service identity matching, active/passive combination, health-check filter behavior.
- Rollback strategy: successful checks or outlier ejection expiry restore eligibility.
- Verification: health-check events, cluster host state, load-balancing membership.
- Recovery interaction: successes required before healthy; passive ejection durations.
- Operator role: configure clusters, checks, thresholds, outlier detection.
- Automation level: high after configuration.
- Tradeoffs: active checks create probe load; passive checks can react quickly but may misread transient errors.
- Why this design exists: proxies need local, protocol-aware failure handling.
- Known limitations: eventual consistency and service identity complexity.

#### Istio

Istio exposes Envoy outlier detection through DestinationRule. It can eject upstream hosts after consecutive 5xx, gateway errors, local-origin failures, connection timeouts, or connection failures, with interval, base ejection time, max ejection percentage, and minimum health percentage.

- Definition of hard failure: host continually returns qualifying errors or has TCP connection timeouts/failures.
- Detection rules: proxy-observed outlier detection.
- Failure thresholds: consecutive errors/failures, ejection interval, ejection time, max ejection percent.
- Reaction strategy: eject host from connection pool for a period.
- Safety gates: max ejection percentage and minimum health percent.
- Rollback strategy: ejection period expires and host can be retried.
- Verification: proxy metrics, ejection state, traffic success.
- Recovery interaction: base ejection time can grow with repeated ejections.
- Operator role: configure traffic policy.
- Automation level: high after configuration.
- Tradeoffs: ejection protects clients but may reduce pool capacity too far if bounded incorrectly.
- Why this design exists: mesh-level clients need uniform failure handling.
- Known limitations: not all failures are visible as application-level errors; defaults may not fit small pools.

#### Linkerd

Linkerd service profiles and proxy behavior are oriented around service-aware routing, retries, timeouts, and route-level metrics. Public material found in this stage was less directly explicit for hard-failure ejection than Envoy/Istio.

- Definition of hard failure: route/backend unavailable or failing requests according to proxy/service profile signals.
- Detection rules: proxy-observed failures, route metrics, retries/timeouts.
- Failure thresholds: service-profile and proxy settings.
- Reaction strategy: retries, failfast behavior, and avoiding unavailable endpoints where control-plane data marks them unavailable.
- Safety gates: timeout/retry boundaries and service-aware metrics.
- Rollback strategy: endpoint/control-plane recovery restores availability.
- Verification: route metrics and proxy status.
- Recovery interaction: service discovery and route health update.
- Operator role: configure profiles and policy.
- Automation level: high for proxy behavior after configuration.
- Tradeoffs: less explicit active health-check model than Envoy.
- Why this design exists: service mesh should protect callers without application rewrites.
- Known limitations: public source did not provide enough hard-failure-specific detail for final policy.

#### HAProxy

HAProxy health checks keep only healthy servers in rotation. It supports active TCP and HTTP checks, custom send/expect sequences, configurable intervals, failure thresholds, success thresholds, passive checks, and agent checks.

- Definition of hard failure: server cannot accept TCP connection, fails expected HTTP/protocol response, or observed transactions fail.
- Detection rules: active connect/request checks and passive traffic observation.
- Failure thresholds: `fall`, `rise`, `inter`, and protocol-specific response criteria.
- Reaction strategy: remove server from rotation; continue checking while down.
- Safety gates: consecutive failure threshold, consecutive success threshold, initial state, agent checks.
- Rollback strategy: restore server after enough successful checks.
- Verification: HAProxy server state and health-check result.
- Recovery interaction: rise threshold and optional slow start.
- Operator role: configure checks and thresholds.
- Automation level: high after configuration.
- Tradeoffs: active probes add traffic; passive detection depends on live traffic.
- Why this design exists: load balancers must avoid failed backends without human intervention.
- Known limitations: a wrong health check path can produce false failure.

#### NGINX

NGINX and NGINX Plus can avoid failed upstream servers, perform passive health checks, active health checks in Plus, slow start recovered servers, and require mandatory checks before new servers receive traffic.

- Definition of hard failure: communication error, timeout, status outside accepted range, or custom match failure.
- Detection rules: passive transaction failures and active health-check requests.
- Failure thresholds: `max_fails`, `fail_timeout`, active check interval, `fails`, `passes`.
- Reaction strategy: mark server unavailable and stop sending traffic until it passes checks.
- Safety gates: custom match conditions, mandatory checks, persistent state, slow start.
- Rollback strategy: pass health checks and gradual reintroduction.
- Verification: upstream health state and response conditions.
- Recovery interaction: slow start reduces immediate overload on recovered server.
- Operator role: configure upstream parameters and health-check conditions.
- Automation level: high after configuration.
- Tradeoffs: NGINX Open Source passive checks differ from NGINX Plus active checks.
- Why this design exists: application load balancers need protocol-aware health.
- Known limitations: single-server groups and open-source feature boundaries affect behavior.

#### Linux Routing

Linux routing exposes route types, metrics, multiple tables, policy routing, unreachable/blackhole/prohibit routes, and route replacement. Linux itself is a routing substrate; hard-failure policy normally comes from routing daemons, netlink users, BFD daemons, keepalived, or operators above the kernel.

- Definition of hard failure: route or nexthop is absent/unusable according to routing table state or external daemon.
- Detection rules: not inherently defined by `ip route`; detection normally lives in protocol daemons or monitoring.
- Failure thresholds: external to kernel route primitives.
- Reaction strategy: add/change/replace/delete routes; use metrics, nexthops, policy tables, unreachable/blackhole/prohibit routes.
- Safety gates: route metrics, table separation, policy routing, daemon logic.
- Rollback strategy: replace route state when health returns.
- Verification: route lookup, table state, packet reachability.
- Recovery interaction: external owner restores route.
- Operator role: configure route daemons and rules.
- Automation level: depends on external owner.
- Tradeoffs: kernel route operations are powerful but not a complete policy.
- Why this design exists: Linux separates forwarding substrate from failure-detection control plane.
- Known limitations: no canonical hard-failure detection policy in `ip route` alone.

#### OpenBSD PF / ifstated

OpenBSD `ifstated` runs commands in response to network state changes by monitoring interface link state or external tests. It can work with CARP and PF to test server or link availability and modify translation or routing rules.

- Definition of hard failure: interface/link state change or failed external test.
- Detection rules: link-state monitoring and external tests.
- Failure thresholds: configured in tests and state machine.
- Reaction strategy: run configured commands to adjust services, CARP, PF, translation, or routing rules.
- Safety gates: explicit state-machine configuration and config test mode.
- Rollback strategy: state transition commands can reverse prior routing/PF changes.
- Verification: daemon logs, interface state, PF/routing state.
- Recovery interaction: state machine transitions when tests pass.
- Operator role: write ifstated rules and PF/CARP behavior.
- Automation level: high after explicit local configuration.
- Tradeoffs: simple and flexible, but policy correctness depends on operator-authored commands.
- Why this design exists: small systems need deterministic local failover hooks.
- Known limitations: no universal policy; it is a mechanism for local policy execution.

#### BGP

BGP detects peer hard failure through TCP session state and Hold Timer expiration. If keepalive, update, or notification messages are not received within Hold Time, the BGP connection is closed and a NOTIFICATION may be sent.

- Definition of hard failure: BGP peer session failure, hold timer expiration, TCP session loss, or administrative/session error.
- Detection rules: negotiated Hold Timer, KEEPALIVE messages, UPDATE/NOTIFICATION receipt, TCP state.
- Failure thresholds: Hold Time must be zero or at least three seconds; keepalives are typically sent often enough not to let hold expire.
- Reaction strategy: close BGP connection, withdraw learned paths, select alternate routes.
- Safety gates: route policy, local preference, route dampening, graceful restart where used, maximum prefix limits.
- Rollback strategy: session re-establishment and route re-advertisement.
- Verification: BGP session state and route table convergence.
- Recovery interaction: peer must re-establish session and pass policy.
- Operator role: configure timers, policy, prefix limits, graceful restart.
- Automation level: high after routing policy.
- Tradeoffs: conservative timers avoid false positives but slow failure detection; BFD can accelerate.
- Why this design exists: interdomain routing needs stable failure detection over TCP sessions.
- Known limitations: BGP sees peer/session liveness, not necessarily every data-plane failure.

#### OSPF

OSPF uses Hello packets and RouterDeadInterval to detect neighbor loss. BFD is commonly paired with OSPF when faster liveness detection is needed.

- Definition of hard failure: neighbor dead or adjacency down.
- Detection rules: no valid Hello within RouterDeadInterval or BFD down when integrated.
- Failure thresholds: Hello interval and RouterDeadInterval.
- Reaction strategy: adjacency removal, LSA updates, SPF recalculation, alternate route installation.
- Safety gates: area design, adjacency state machine, SPF throttling, BFD/timer tuning.
- Rollback strategy: neighbor adjacency re-forms and routing reconverges.
- Verification: adjacency state and route table.
- Recovery interaction: neighbor must pass OSPF state transitions.
- Operator role: configure area/timers/authentication/BFD.
- Automation level: high inside routing protocol.
- Tradeoffs: faster timers can increase instability; slower timers prolong outage.
- Why this design exists: link-state routing needs shared topology truth.
- Known limitations: control-plane adjacency can differ from application reachability.

#### IS-IS

IS-IS detects hard failure through adjacency hello loss and can integrate with BFD for faster detection.

- Definition of hard failure: adjacency down or BFD session down.
- Detection rules: IS-IS hellos, holding time, BFD notifications.
- Failure thresholds: hello/hold timer or BFD multiplier.
- Reaction strategy: LSP update, SPF recalculation, alternate route selection.
- Safety gates: level design, SPF throttling, BFD timer tuning.
- Rollback strategy: adjacency restoration and reconvergence.
- Verification: adjacency and route table state.
- Recovery interaction: re-formed adjacency participates in topology.
- Operator role: configure timers, levels, BFD, metrics.
- Automation level: high.
- Tradeoffs: same fast-detect versus false-positive balance as OSPF/BFD.
- Why this design exists: link-state routing requires topology consistency.
- Known limitations: not an application-level health check.

#### MPLS / RSVP-TE Fast Reroute

RFC 4090 describes RSVP-TE Fast Reroute for local repair of LSP tunnels when a node or link along the LSP path fails. It rationalizes one-to-one and facility backup methods and includes local repair notification.

- Definition of hard failure: link or node failure along an LSP path.
- Detection rules: local failure detection by PLR and supporting mechanisms such as link signals/BFD.
- Failure thresholds: depends on detection mechanism and preconfigured protection.
- Reaction strategy: local repair via detour or facility backup without waiting for global recomputation.
- Safety gates: pre-signaled backup capability, bandwidth/node protection flags, clear error if unsupported.
- Rollback strategy: head-end/global reoptimization can replace local repair after topology reconverges.
- Verification: local protection flags, RSVP state, path record, traffic continuity.
- Recovery interaction: repaired primary or optimized path may be restored later.
- Operator role: configure protection type and constraints.
- Automation level: high after preconfiguration.
- Tradeoffs: precomputed protection consumes resources but dramatically shortens outage.
- Why this design exists: waiting for end-to-end reconvergence is too slow for carrier traffic.
- Known limitations: protection method compatibility and resource availability.

#### SD-WAN

Public SD-WAN practice across major vendors generally treats hard failure as transport/path unavailability detected by probes, tunnel/BFD state, SLA classes, and controller/edge policy. During this research stage, authoritative vendor-specific detail was strongest for BFD/routing and general SD-WAN health concepts, not enough for final V7 policy.

- Definition of hard failure: WAN path, tunnel, transport, or edge peer unavailable.
- Detection rules: path probes, BFD/session state, controller telemetry, SLA state.
- Failure thresholds: vendor policy timers and loss-of-keepalive thresholds.
- Reaction strategy: steer traffic to remaining transports or backup path.
- Safety gates: SLA policy, application policy, path preference, tunnel health.
- Rollback strategy: path is restored after health returns and policy permits.
- Verification: tunnel state, path health, application reachability.
- Recovery interaction: recovered path may be admitted by SLA and anti-flap rules.
- Operator role: define application/path policies and SLA classes.
- Automation level: high inside approved policy.
- Tradeoffs: internet path variability makes false positives and oscillation important.
- Why this design exists: WAN underlays fail independently and need application-aware steering.
- Known limitations: vendor-specific behavior differs; consensus stage must separate common pattern from implementation detail.

#### IETF RFCs

The most relevant RFCs for hard failure are RFC 5880 for BFD, RFC 4271 for BGP hold timers, RFC 2328 for OSPF dead intervals, RFC 4090 for MPLS RSVP-TE Fast Reroute, and related BFD updates. They show that standards prefer explicit timers, missed message thresholds, state machines, protocol notifications, and precomputed or policy-bound reactions.

- Definition of hard failure: missed liveness messages, expired detection timers, session down, neighbor dead, or protected path failure.
- Detection rules: periodic packets, negotiated timers, missed-message multipliers, state machine transitions.
- Failure thresholds: protocol-defined or negotiated timers.
- Reaction strategy: signal client protocol, close session, remove routes, reroute, or locally repair.
- Safety gates: state machines, negotiated timers, authentication where available, protection flags.
- Rollback strategy: session/adjacency/path re-establishment.
- Verification: protocol state and forwarding continuity.
- Recovery interaction: controlled re-entry through the protocol state machine.
- Operator role: configure timers and policy.
- Automation level: high within protocol.
- Tradeoffs: standards avoid application-specific assumptions.
- Why this design exists: interoperable routing needs deterministic failure semantics.
- Known limitations: protocol liveness is not the same as application success.

#### Academic Failure Detector Literature

Academic distributed-systems literature treats failure detection as inherently unreliable under asynchrony. Chandra-Toueg failure detectors separate completeness from accuracy: a detector can eventually suspect crashed processes, but false suspicion is a central risk. Phi-accrual and adaptive detectors model suspicion as a level rather than a binary fact. Large-scale detector work studies scaling, decentralization, gossip, hierarchy, and QoS.

- Definition of hard failure: crashed, unreachable, or disconnected process, often indistinguishable from slow communication in asynchronous systems.
- Detection rules: timeouts, heartbeats, suspicion levels, gossip, tests, or diagnosis models.
- Failure thresholds: timeout, suspicion threshold, expected delay/drop assumptions.
- Reaction strategy: exclude suspected process, elect new leader, reconfigure membership, or trigger recovery.
- Safety gates: quorum/majority, eventual accuracy, backoff, adaptive thresholds.
- Rollback strategy: clear suspicion when communication resumes, or rejoin through membership.
- Verification: consensus progress, membership convergence, detector quality metrics.
- Recovery interaction: crash-recovery models require re-admission and state synchronization.
- Operator role: set assumptions, thresholds, topology, and risk tolerance.
- Automation level: algorithmic.
- Tradeoffs: faster detection reduces downtime but increases false suspicion.
- Why this design exists: perfect failure detection is impossible in fully asynchronous systems.
- Known limitations: academic models abstract away operational concerns such as user impact and rollback.

#### Production Postmortems And Operator Best Practices

Production postmortems and SRE practice repeatedly show that hard-failure response must account for cascading effects, DNS/connection persistence, stale membership, probe quality, and overload after failover. The strongest public examples found in this stage are Google SRE cascading-failure material, Google Maglev, Netflix Eureka, Cloudflare Load Balancing, AWS ELB/Auto Scaling, Azure Traffic Manager, and Kubernetes reconciliation.

- Definition of hard failure: component unable to serve, route traffic, or participate in expected production role.
- Detection rules: health checks, liveness signals, traffic errors, registry leases, route/session state.
- Failure thresholds: consecutive failures and timeouts rather than single events.
- Reaction strategy: remove from rotation, reroute, replace, or locally repair.
- Safety gates: capacity, fallback, blast radius, health check identity, anti-flap, staged recovery.
- Rollback strategy: continuous verification and controlled re-entry.
- Verification: external user impact, internal health, routing/LB state, outcome logs.
- Recovery interaction: gradual or gated return is common where overload risk exists.
- Operator role: define boundaries; runtime handles routine reaction.
- Automation level: high for bounded failure classes, human for broad incidents.
- Tradeoffs: single fast automatic action may be correct locally and unsafe globally.
- Why this design exists: availability is a system property, not a single endpoint property.
- Known limitations: public postmortems often describe consequences more than exact control policy.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Active probes vs passive traffic observation vs protocol liveness | Different layers can observe different truths: synthetic health, real user traffic, or protocol state. | Active probes detect early but can be unrepresentative; passive evidence is real but late; protocol liveness is fast but not application-specific. | Active probes for LB/service health; passive observation for real impact; protocol liveness for routing/control-plane failure. |
| Fast timers vs conservative thresholds vs damped suspicion | Lower latency response increases false-positive and flap risk. | Fast timers reduce outage time; conservative thresholds reduce churn; suspicion scoring handles uncertainty but adds complexity. | Fast timers for stable links/critical paths; conservative thresholds for noisy networks; suspicion for distributed systems. |
| DNS failover vs proxy failover vs routing failover | Each layer controls different traffic and has different propagation behavior. | DNS is broad but slow for existing connections; proxies are service-aware; routing is topology-aware. | DNS for global endpoint steering; proxy for service routing; routing for network reachability. |
| Fail-open vs fail-closed | When every target looks unhealthy, serving degraded traffic may be better or worse than stopping. | Fail-open preserves partial availability but may send users to broken targets; fail-closed protects correctness but can create total outage. | Fail-open for availability-first traffic; fail-closed for safety/security/correctness-sensitive action. |

### Industry Disagreement Research

1. Fast detection versus false positives.
   BFD, Envoy, HAProxy, and LBs can detect quickly, but Google SRE, Juniper damping, and cloud thresholds show that fast detection can produce flapping and cascades.

2. Active probes versus passive observation.
   Cloudflare, Azure, GCP, AWS, HAProxy, Envoy, and NGINX use active probes. Envoy/Istio/HAProxy/NGINX also support passive or observed-failure approaches. Active probes can detect before user traffic fails; passive signals reflect real traffic but can react after users are affected.

3. DNS failover versus proxy/routing failover.
   Route 53 and Azure Traffic Manager operate at DNS level and cannot affect existing connections immediately. Proxies and routing protocols can react closer to live traffic but have different scaling and state risks.

4. Binary health versus graded suspicion.
   Routing protocols and many load balancers make binary healthy/unhealthy decisions. Academic and large-scale SRE practice warn that suspicion may be probabilistic under latency, overload, or partitions.

5. Fail-closed versus fail-open.
   Cloudflare fallback pools and AWS ALB fail-open behavior show that when every endpoint is unhealthy, systems may still route somewhere rather than refuse all traffic. Security and correctness-oriented systems may prefer fail-closed.

6. Immediate removal versus capacity-aware removal.
   Load balancers usually remove failed endpoints quickly; Google SRE warns that shifting traffic to remaining capacity can create cascading failure.

7. Automatic re-entry versus staged recovery.
   Some protocols restore eligibility once adjacency or health checks pass. NGINX slow start, Kubernetes readiness, Cloudflare consecutive up, and Juniper damping show staged recovery is often safer.

8. Control-plane detection versus data-plane detection.
   BGP/OSPF/IS-IS detect protocol adjacency. BFD and Maglev emphasize forwarding-path behavior. Application LBs detect service-level responses. These can disagree.

9. Vendor-managed policy versus operator-authored local policy.
   AWS/Azure/GCP/Cloudflare provide managed health behavior; OpenBSD ifstated and Linux routing are mechanisms where operators author policy.

10. Single-vantage versus multi-vantage detection.
    Local routing protocols observe local neighbor state. Cloudflare and Azure use multiple probing locations. Multi-vantage improves global decision quality but adds latency and aggregation logic.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- code owners: `tools/v7-users-autoswitch`, `tools/v7-telegram-sentinel`, `tools/v7-egress-quality-compact`, `tools/v7-service-matrix-refresh-all`, `admin_core/events.py`, `admin_core/operator_execution_pipeline.py`, `admin_core/operator_execution.py`, `admin_core/autonomy_trust_acceleration.py`;
- production truth: `tools/v7-truth-check --all --json` PASS, runtime aligned, autoswitch service/timer inactive in approved manual mode;
- read-only inventory: action-class runtime path `PARTIAL`, first class `single-user governed candidate failover`, runtime automation `NO`;
- no runtime mutation, no authority expansion, no policy implementation performed by this audit.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: explicit liveness evidence. | `PARTIALLY_IMPLEMENTED` | Event sources, service matrix, quality compact, planner/autoswitch. | Read/probe/event inputs and planner blockers exist; canonical hard-failure classifier is not implemented. | Reuse event consumer, service matrix, quality compact, route/runtime read models. | `SMALL_EXTENSION`: bind liveness evidence to hard-failure classification. |
| CS2: avoid single noisy observation. | `PARTIALLY_IMPLEMENTED` | Planner gates, service-signal persistence, anti-flap overlay. | Thresholds/cooldowns and read-only anti-flap model exist; hard-failure thresholds are not certified. | Reuse service persistence and `build_anti_flapping`. | `SMALL_EXTENSION`: encode per-class thresholds. |
| CS3: remove/de-prefer confirmed failed target inside policy. | `PARTIALLY_IMPLEMENTED` | Planner/autoswitch, Runtime Model, action-class enablement. | Planner can propose moves and guarded apply path exists; autonomous execution is disabled and class authority is not approved. | Reuse autoswitch planner and guarded execution owners. | `MODERATE_EXTENSION`: certify class authority and runtime eligibility. |
| CS4: continue verification and recovery checks. | `PARTIALLY_IMPLEMENTED` | Restore/rollback, verification, recovery admission, feedback/learning. | Verification and recovery overlays exist; hard-failure outcome closure is not complete. | Reuse restore/rollback, feedback, learning, recovery admission. | `MODERATE_EXTENSION`: close real hard-failure outcomes. |
| CS5: bound failover by fallback/capacity/policy/blast radius. | `PARTIALLY_IMPLEMENTED` | Planner capacity/policy gates, restore barrier, action-class ladder. | One-user governed blast boundary exists; class-level blast certification is missing. | Reuse planner budgets, restore barrier, action-class ladder. | `SMALL_EXTENSION`: certify class blast-radius evidence. |
| CS6: multi-vantage health improves global decisions. | `PARTIALLY_IMPLEMENTED` | Service matrix, Telegram sentinel, quality compact, route reality. | Multiple read models exist; canonical multi-vantage aggregation is not implemented. | Reuse service/route/quality/event owners. | `MODERATE_EXTENSION`: aggregate liveness evidence by source family. |
| CS7: fast detection only when false-positive risk is tolerable. | `PARTIALLY_IMPLEMENTED` | OMP floors, safety policy, anti-flap overlay. | Safety gates exist; timer/tolerance policy is not canonicalized for hard failure. | Reuse risk-tiered floors and anti-flap model. | `SMALL_EXTENSION`: add hard-failure timer/risk class. |
| CS8: fail-open is architecture-specific. | `UNKNOWN` | Runtime Model, OMP, planner gates. | Current implementation stops or requires authority; explicit fail-open/fail-closed behavior is not audited. | Reuse stop-condition and policy gate owners. | `CONFIGURATION_ONLY`: decide in V7 fit analysis. |
| CS9: local repair is specialized. | `NOT_IMPLEMENTED` | No required owner for current scope. | V7 uses planner/route/user movement, not MPLS-style local repair. | Reuse planner if future fit requires local repair semantics. | `DOCUMENTATION_ONLY`: likely non-applicable unless substrate changes. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `56%` |
| Reuse potential | `92%` |
| Missing coverage | `44%` |
| Complexity of remaining work | `MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `ADAPT`.

Hard-failure practice fits V7, but V7 must adapt network/load-balancer hard-failure methods to a user/channel routing product. V7 should reuse existing liveness, service, quality, planner, rollback, freshness, blast-radius, and learning owners instead of creating a new hard-failure owner.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Explicit liveness evidence. | `YES` | `ADAPT` | V7 needs a canonical unavailable-channel classifier over existing probes/events. | Event sources, service matrix, quality compact, planner/autoswitch. | Bind existing liveness evidence to hard-failure classification. | `SMALL_EXTENSION` | Very high: removes dead-path ambiguity. | `A1` |
| Timers, multipliers, consecutive failures, or state machines. | `YES` | `ADAPT` | V7 must avoid one noisy event becoming movement. | Planner gates, service persistence, anti-flap overlay. | Encode per-action-class hard-failure thresholds. | `SMALL_EXTENSION` | High: reduces false-positive movement. | `A2` |
| Remove/de-prefer confirmed failed target inside policy. | `YES` | `ADAPT` | V7 should fail over only inside approved action-class/policy bounds. | Planner/autoswitch, Runtime Model, action-class enablement. | Reuse planner and guarded execution owners after certification. | `MODERATE_EXTENSION` | Very high: creates production failover path. | `A6` |
| Continue verification and recovery checks. | `YES` | `REUSE` | V7 already has verification, recovery admission, feedback, and learning owners. | Restore/rollback, verification, recovery admission, feedback/learning. | Require outcome closure for hard-failure actions. | `MODERATE_EXTENSION` | High: makes outcomes certifiable. | `A3` |
| Bound failover by fallback/capacity/policy/blast radius. | `YES` | `REUSE` | V7 action classes already require bounded scope. | Planner capacity/policy gates, restore barrier, action-class ladder. | Certify class-level blast-radius evidence. | `SMALL_EXTENSION` | Very high: prevents local failure from becoming global failure. | `A5` |
| Multi-vantage health. | `YES` | `ADAPT` | V7 has multiple evidence families but not canonical liveness aggregation. | Service matrix, Telegram sentinel, quality compact, route reality. | Aggregate liveness by source family and confidence. | `MODERATE_EXTENSION` | High: improves confidence under partial evidence. | `B1` |
| Fast detection only when false-positive risk is tolerable. | `YES` | `REUSE` | V7 already separates confidence from authority and safety. | OMP floors, safety policy, anti-flap overlay. | Add hard-failure timer/risk class to policy windows. | `SMALL_EXTENSION` | Medium high: safer speed. | `B2` |
| Fail-open behavior. | `PARTIAL` | `ADAPT` | V7 should default to safe stop unless a class policy explicitly permits fail-open. | Runtime Model, OMP, planner gates. | Record fail-open/fail-closed per action class. | `NONE` | Medium: removes ambiguity. | `C1` |
| Local repair before global recomputation. | `NO_FOR_CURRENT_SCOPE` | `REJECT` | MPLS/router-local repair is not V7's current product abstraction. | None required. | Keep as future substrate option only. | `NONE` | Optional only. | `D1` |

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

### Vendor And Platform Sources

- Cisco, IP Routing: BFD Configuration Guide: https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bfd/configuration/xe-16/irb-xe-16-book.html
- Juniper, Understanding How BFD Detects Network Failures: https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/bfd.html
- Arista, EOS Bidirectional Forwarding Detection: https://www.arista.com/en/um-eos/eos-bidirectional-forwarding-detection
- Cloudflare, How endpoints and pools become unhealthy: https://developers.cloudflare.com/load-balancing/understand-basics/health-details/
- Cloudflare, Monitors: https://developers.cloudflare.com/load-balancing/monitors/
- Google SRE, Addressing Cascading Failures: https://sre.google/sre-book/addressing-cascading-failures/
- Google SRE, Handling Overload: https://sre.google/sre-book/handling-overload/
- Google Research, Maglev: A Fast and Reliable Software Network Load Balancer: https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/
- Netflix Eureka, Eureka at a glance: https://github.com/Netflix/eureka/wiki/Eureka-at-a-glance
- AWS Route 53, Creating health checks: https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html
- AWS ELB, Application Load Balancer target health checks: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html
- AWS EC2 Auto Scaling, health checks: https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html
- AWS ECS, service unhealthy event messages: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-unhealthy-event-messages.html
- Azure Traffic Manager endpoint monitoring: https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-monitoring
- Google Cloud Load Balancing health checks: https://docs.cloud.google.com/load-balancing/docs/health-check-concepts
- Kubernetes Pod lifecycle and probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Envoy health checking: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking
- Istio DestinationRule OutlierDetection: https://istio.io/latest/docs/reference/config/networking/destination-rule/#OutlierDetection
- Linkerd service profiles: https://linkerd.io/docs/reference/service-profiles/
- HAProxy health checks: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/
- NGINX HTTP health checks: https://docs.nginx.com/nginx/admin-guide/load-balancer/http-health-check/
- Linux `ip-route(8)`: https://man7.org/linux/man-pages/man8/ip-route.8.html
- OpenBSD `ifstated(8)`: https://man.openbsd.org/ifstated
- OpenBSD `pf.conf(5)`: https://man.openbsd.org/pf.conf

### RFC And Standards Sources

- RFC 5880, Bidirectional Forwarding Detection: https://www.rfc-editor.org/rfc/rfc5880
- RFC 4271, BGP-4: https://www.rfc-editor.org/rfc/rfc4271
- RFC 2328, OSPF Version 2: https://www.rfc-editor.org/rfc/rfc2328
- RFC 4090, RSVP-TE Fast Reroute: https://www.rfc-editor.org/rfc/rfc4090
- RFC 7130, BFD on Link Aggregation Group Interfaces: https://www.rfc-editor.org/rfc/rfc7130
- RFC 5881, BFD for IPv4 and IPv6 single hop: https://www.rfc-editor.org/rfc/rfc5881

### Academic And Large-Scale Distributed Systems Sources

- Chandra and Toueg, Unreliable Failure Detectors for Reliable Distributed Systems: https://dl.acm.org/doi/10.1145/226643.226647
- Hayashibara et al., The Phi Accrual Failure Detector: https://ieeexplore.ieee.org/document/1353004
- Chen, Toueg, and Aguilera, On the Quality of Service of Failure Detectors: https://ieeexplore.ieee.org/document/980025
- Kumar and Welch, Implementing Eventually Perfect Failure Detection with bounded messages: https://arxiv.org/abs/1708.02906
- Duarte et al., Distributed diagnosis model for unreliable failure detectors: https://arxiv.org/abs/2210.02847
- Dobre et al., Robust Failure Detection Architecture for Large Scale Distributed Systems: https://arxiv.org/abs/0910.0708

### Research Coverage Notes

- Systems or families researched: 30.
- RFC or academic sources researched: 12.
- Production case-study sources researched: 7.
- Source gaps recorded: Meta and Apple did not expose enough authoritative public hard-failure routing policy detail for canonical policy content in this stage.
- Stage 1 all-policy pass reused this hard-failure research as the base for shared mechanisms across soft degradation, recovery admission, blast radius, freshness, rollback, action-class promotion, authority, and anti-flap.

## Open Questions

- Which observed patterns survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- Which disagreements are relevant to V7's channel/server model?
- Which existing V7 owners map to detection, reaction, verification, rollback, and learning?
- Which public source gaps require non-public operator evidence or exclusion?
