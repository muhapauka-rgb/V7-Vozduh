# POLICY_007_ROLLBACK

Status: `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`
Policy class: rollback
Current lifecycle: `V7_FIT_ANALYSIS_COMPLETE`
Next lifecycle: `IMPLEMENTATION_BACKLOG`
Certification state: `RESEARCH_PENDING`
Implementation state: `NOT_IMPLEMENTED`
Runtime automation enabled: `NO`

## Purpose

This policy records world research for rollback.

Rollback means returning traffic, configuration, deployment, route state, assignment, or authority state to a known safer previous state after verification fails or risk increases.

This document currently contains only the `FULL WORLD RESEARCH` stage. It does not yet define V7 consensus, V7 adaptation, runtime behavior, authority behavior, implementation, certification, or autonomous enablement.

## Problem

Rollback is not just undo.

Some actions are reversible, some are only compensatable, and some should not be rolled back if the old state is worse than the new one.

Mature systems prepare rollback before mutation, verify rollback feasibility, keep enough state to reverse safely, and sometimes choose no-rollback with containment.

## Industry Consensus

`RESEARCH_STAGE_ONLY`.

This section records observations found during `FULL WORLD RESEARCH`. It does not yet assert final V7 consensus.

### Consensus Classification

| Consensus Statement | Consensus Strength | Supporting Systems | Evidence Quality | Conflicting Systems |
| --- | --- | --- | --- | --- |
| Risky production actions should have rollback, abort, revert, or compensation planned before mutation. | `STRONG` | Google SRE, Kubernetes, AWS CodeDeploy/CloudFormation, Azure/GCP deployment practice, network commit confirmed/config archives, service mesh route revert | `HIGH`: broad production evidence | None for risky actions. |
| Rollback must be verified; reverting configuration is not the same as proving user/service recovery. | `STRONG` | Google SRE, Kubernetes rollout status, AWS alarms, Cloudflare/LB health, network route verification, V7 normalized evidence | `HIGH`: cross-system operational evidence | None. |
| Some actions are not safely reversible and require containment or forward fix. | `STRONG` | Databases/distributed systems, SRE, cloud deployments, network operations | `HIGH`: common operations principle | None; disagreement is about when this applies. |
| Keeping a stable previous version or fallback target is common. | `MEDIUM` | Kubernetes, AWS CodeDeploy, Azure/GCP revisions, Istio/Envoy traffic shift, Cloudflare fallback, HAProxy/NGINX pools | `MEDIUM_HIGH`: widespread in deploy/LB/proxy systems | External routes/providers may lack a known-good target. |
| Automatic rollback is common when failure signals are reliable and authority is pre-approved. | `MEDIUM` | AWS CodeDeploy, Kubernetes controllers, progressive delivery controllers | `MEDIUM`: strong deployment evidence, less universal in network/authority contexts | Human approval remains common for high-risk network/authority rollback. |
| Transaction rollback models are specialized to data/state systems and do not generalize to all operational actions. | `WEAK` | Databases, consensus logs, distributed systems | `MEDIUM`: strong domain evidence | Traffic/routing rollbacks are often compensating operations. |

### Industry Consensus Research

#### Kubernetes

Kubernetes Deployments keep rollout history and support rollout undo. Desired-state reconciliation enables reverting manifests or ReplicaSets when rollout fails.

- Purpose: restore a previous working workload state.
- Existing production approaches: rollout history, rollout status, undo, pause/resume, readiness.
- Known patterns: rollback is tied to declared desired state and revision history.
- Known failure patterns: bad Deployment, bad image, failed readiness, stuck rollout.
- Known recovery patterns: undo to previous ReplicaSet or apply fixed manifest.
- Known tradeoffs: rollback restores infrastructure state, not necessarily data state.
- Known limitations: rollbacks cannot undo external side effects.

#### AWS

AWS CodeDeploy supports automatic rollback when deployment fails or alarms activate. CloudFormation can roll back stacks. ELB/Auto Scaling can replace unhealthy instances.

- Purpose: restore service after bad deployment or resource state.
- Existing production approaches: deployment alarms, lifecycle hooks, blue/green, rollback configuration, stack rollback.
- Known patterns: rollback is preconfigured before deployment.
- Known failure patterns: alarm triggers, hook failure, unhealthy replacement.
- Known recovery patterns: stop deployment and redeploy previous version.
- Known tradeoffs: rollback can be automatic but depends on alarm quality.
- Known limitations: rollback may fail if dependencies or resources changed externally.

#### Azure / GCP

Azure and GCP deployment tooling supports staged deployment, rollback/redeploy, managed instance replacement, versioned services, traffic splitting, and restoration of prior revisions in service platforms.

- Purpose: reduce time to safe state after bad change.
- Existing production approaches: deployment slots, revisions, traffic splitting, managed rollback, safe deployment rings.
- Known patterns: keep previous version alive until new one is proven.
- Known failure patterns: bad revision, bad config, regional rollout issue.
- Known recovery patterns: shift traffic back, redeploy prior version, stop rollout.
- Known tradeoffs: dual-running versions increase cost and complexity.
- Known limitations: data migrations can make rollback unsafe.

#### Google SRE

Google SRE release engineering treats rollback as a required production capability. Rollbacks must be fast, tested, and available when canary or SLO signals fail.

- Purpose: shorten incident duration.
- Existing production approaches: canary, monitoring, rollback, emergency response.
- Known patterns: rollback plan before rollout.
- Known failure patterns: rollback too slow, irreversible change, missing monitoring.
- Known recovery patterns: revert, stop rollout, mitigate.
- Known tradeoffs: systems designed for rollback may avoid certain risky changes.
- Known limitations: not every operational action is safely reversible.

#### Envoy / Istio / Service Mesh

Service mesh rollback often means changing route weights back, disabling a route policy, restoring circuit breaker settings, or returning traffic to a stable subset.

- Purpose: reverse unsafe traffic policy quickly.
- Existing production approaches: weighted routing, DestinationRule rollback, config revert.
- Known patterns: keep stable route available.
- Known failure patterns: bad subset, bad retries, wrong outlier policy.
- Known recovery patterns: route weight to stable, remove policy, restart/config reload.
- Known tradeoffs: config rollback can be fast but not all in-flight requests are recoverable.
- Known limitations: mesh policy rollback cannot fix broken service state.

#### Cloudflare / Global Edge

Cloudflare operational rollback often uses configuration revert, feature flag disablement, fallback pool, or edge deployment rollback.

- Purpose: restore global edge behavior after bad config or origin choice.
- Existing production approaches: product config versioning, fallback pools, staged edge rollout, API changes.
- Known patterns: isolate and revert at account/zone/product scope.
- Known failure patterns: bad monitor, wrong pool, global edge behavior regression.
- Known recovery patterns: revert config or steer to fallback.
- Known tradeoffs: rollback at edge can be fast but must consider cache and DNS propagation.
- Known limitations: external provider failures may leave no good rollback target.

#### Network Operations / Cisco / Juniper / Arista / OpenBSD / Linux

Network rollback uses candidate configuration, commit confirmed, route withdrawal, metric restoration, route table replacement, PF rule restoration, and configuration archives.

- Purpose: undo unsafe routing or firewall state.
- Existing production approaches: commit confirmed, config rollback, route replace/delete, PF reload, routing policy revert.
- Known patterns: keep previous config and require confirmation.
- Known failure patterns: route leak, bad ACL, wrong next hop, bad failover route.
- Known recovery patterns: auto-revert unconfirmed commit, apply saved config, withdraw route.
- Known tradeoffs: rollback can disconnect the operator if not protected.
- Known limitations: data-plane convergence may lag config rollback.

#### Databases / Distributed Systems

Distributed systems distinguish rollback from compensation. Consensus systems use logs and terms; databases use transactions, snapshots, backups, point-in-time recovery, and sometimes forward fix.

- Purpose: preserve correctness when state changes.
- Existing production approaches: transaction rollback, log replay, snapshot restore, compensation.
- Known patterns: rollback requires durable pre-change state or reversible operation.
- Known failure patterns: partial side effects, schema/data incompatibility, dual writes.
- Known recovery patterns: restore snapshot, apply compensating operation, fence writer.
- Known tradeoffs: full rollback can be expensive or impossible.
- Known limitations: not every failure has a safe automatic rollback.

## Industry Disagreements

`RESEARCH_STAGE_ONLY`.

This section records disagreements found during `FULL WORLD RESEARCH`. It does not yet assert final V7 disagreements.

### Disagreement Classification

| Alternatives | Why disagreement exists | Tradeoffs | Appropriate when |
| --- | --- | --- | --- |
| Rollback vs forward fix vs containment | Previous state may be unsafe or irreversible. | Rollback is fast when safe; forward fix handles irreversible change; containment limits damage. | Rollback for reversible movement/config; forward fix for data/schema/irreversible actions; containment when both are unsafe. |
| Automatic rollback vs human-approved rollback | Failure signals and authority differ by action class. | Automatic rollback lowers MTTR; human review avoids wrong reversal. | Automatic for certified bounded actions; human approval for authority/broad-scope changes. |
| Restore exact prior state vs alternate safe state | Old state may now be degraded. | Exact restore is simple; alternate safe state can be safer but requires fresh decision. | Exact restore only if old target remains fresh and safe. |
| Precomputed rollback vs runtime-computed rollback | Runtime may have fresher state but less certainty. | Precomputed is auditable; computed is adaptive. | Precompute for governed action; compute only inside certified policy with fresh evidence. |

### Industry Disagreement Research

1. Rollback versus forward fix.
   Rollback is preferred when safe; forward fix may be required when state cannot go backward.

2. Automatic rollback versus human-approved rollback.
   Deployment systems can auto-rollback; network and authority changes often need stricter approval.

3. Restore old state versus route to alternate safe state.
   Traffic systems may not restore the exact old path if it is also degraded.

4. Precomputed rollback versus runtime-computed rollback.
   Precomputed rollback is safer; runtime computation may adapt better but needs more trust.

5. Configuration rollback versus outcome rollback.
   Reverting config does not guarantee user impact is restored.

## Reality Audit

Status: `REALITY_AUDIT_COMPLETE`.

Reality source:

- owners: `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `tools/v7-restore-settle-gate`, feedback/learning stores;
- evidence: rollback manifests, rollback packet generation/execution, verify-fail rollback path, operation-scoped rollback records, restore-settle gate; runtime automation disabled.

### Consensus Reality Mapping

| Consensus item | Reality status | Existing owner(s) | Existing implementation / evidence | Reuse opportunity | Gap |
| --- | --- | --- | --- | --- | --- |
| CS1: rollback/abort/compensation planned before risky mutation. | `FULLY_IMPLEMENTED` | Packet owner, restore barrier, rollback manifest. | Governed packets include rollback manifests and restore clearance preview. | Reuse packet/restore owners. | None. |
| CS2: rollback must be verified. | `PARTIALLY_IMPLEMENTED` | Autoswitch verification, rollback execution, truth/convergence. | Verify-fail rollback exists; class-level rollback verification is not certified for all action classes. | Reuse verification and rollback owners. | `SMALL_EXTENSION`: certify per class. |
| CS3: some actions need containment/forward fix. | `PARTIALLY_IMPLEMENTED` | Runtime Model, execution packet partial-failure policy. | `stop_and_contain` exists; forward-fix semantics are not canonicalized. | Reuse execution lifecycle owner. | `SMALL_EXTENSION`: document/apply containment classification. |
| CS4: stable previous version/fallback target is common. | `FULLY_IMPLEMENTED` | Rollback manifest, planner current target. | Rollback target/user/current egress are captured in manifests. | Reuse rollback manifest. | None. |
| CS5: automatic rollback common when signals reliable and authority pre-approved. | `PARTIALLY_IMPLEMENTED` | Autoswitch rollback-on-verify-fail. | Tool can rollback on verification failure; autonomous authority is not approved. | Reuse existing dry-run/apply guarded owner. | `MODERATE_EXTENSION`: certify automatic rollback authority. |
| CS6: transaction rollback does not generalize everywhere. | `FULLY_IMPLEMENTED` | Runtime Model, rollback policy. | V7 treats rollback as operational compensation, not database transaction. | Reuse model. | None. |

### Policy Coverage

| Metric | Value |
| --- | --- |
| Implementation coverage | `74%` |
| Reuse potential | `96%` |
| Missing coverage | `26%` |
| Complexity of remaining work | `SMALL_TO_MODERATE` |
| Expected implementation risk | `MEDIUM` |
| Fundamental architecture gap | `NO` |

## V7 Fit Analysis

Status: `COMPLETE`.

Policy decision: `REUSE`.

Rollback practice already fits V7's restore-barrier and operation-scoped rollback model. Remaining work is class-level certification and clearer containment semantics, not a new rollback owner.

| Industry practice | Applicable to V7? | Decision | Why | Existing owner | Reuse path | Complexity | Expected production value | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rollback/abort/compensation before risky mutation. | `YES` | `REUSE` | Governed packets already include rollback manifests and restore clearance preview. | Packet owner, restore barrier, rollback manifest. | Keep rollback manifest mandatory. | `NONE` | Very high: bounded mutation. | `A3` |
| Rollback must be verified. | `YES` | `ADAPT` | Verification exists, but class-level rollback verification is not certified. | Autoswitch verification, rollback execution, truth/convergence. | Certify per action class. | `SMALL_EXTENSION` | Very high: trustworthy recovery. | `A3` |
| Containment/forward-fix for non-reversible actions. | `YES` | `ADAPT` | V7 has `stop_and_contain`; needs canonical classification. | Runtime Model, execution packet partial-failure policy. | Document and expose containment classification. | `SMALL_EXTENSION` | High: avoids unsafe rollback. | `B15` |
| Stable previous version/fallback target. | `YES` | `REUSE` | Current target and rollback manifest already capture fallback. | Rollback manifest, planner current target. | Keep target freshness gate. | `NONE` | High: preserves reversibility. | `A3` |
| Automatic rollback when signals reliable and authority pre-approved. | `YES_LATER` | `ADAPT` | Tool support exists but autonomous rollback authority is not approved. | Autoswitch rollback-on-verify-fail. | Certify automatic rollback authority after class evidence. | `MODERATE_EXTENSION` | High: reduces incident duration. | `B16` |
| Transaction rollback does not generalize. | `YES` | `REUSE` | V7 already treats rollback as operational compensation. | Runtime Model, rollback policy. | Preserve operational compensation semantics. | `NONE` | Medium: avoids false abstraction. | `C5` |

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

- Kubernetes Deployments rollback: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- AWS CodeDeploy rollback: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
- AWS CloudFormation stack rollback: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-rollback-triggers.html
- Google SRE, Release Engineering: https://sre.google/sre-book/release-engineering/
- Azure safe deployment practices: https://learn.microsoft.com/en-us/devops/operate/safe-deployment-practices
- Istio traffic management: https://istio.io/latest/docs/concepts/traffic-management/
- Envoy HTTP routing: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/http/http_routing
- OpenBSD ifstated: https://man.openbsd.org/ifstated
- Linux ip-route: https://man7.org/linux/man-pages/man8/ip-route.8.html

## Open Questions

- Which rollback forms survive the next `INDUSTRY_CONSENSUS_DETECTION` stage?
- When is no-rollback safer than rollback?
- Which rollback evidence must be prepared before an action is eligible?
