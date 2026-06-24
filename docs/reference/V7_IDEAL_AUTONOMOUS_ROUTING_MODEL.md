# V7 Ideal Autonomous Routing Model

Status: canonical target model  
Phase: `V7.IDEAL.AUTONOMOUS.ROUTING.SYSTEM.MODEL`  
Date: 2026-06-24  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Base commit: `61088d7a9fa48cc593a5cf2b681f520e8734b59d`

This document defines what V7 should be when it is fully successful: an autonomous routing/control-plane system for `10,000+` users and `100+` channels.

It is not a runtime authorization. It does not enable user movement, daemon apply, autoswitch apply, planner redesign, governance redesign, execution redesign, formula changes, floor changes, synthetic evidence, or a new truth source.

## 1. Target Identity

Ideal V7 is an event-driven autonomous routing control plane.

It continuously turns observed network reality into bounded routing decisions:

```text
observe
  -> classify
  -> decide
  -> plan
  -> limit blast radius
  -> execute if authorized
  -> verify
  -> rollback if needed
  -> learn
  -> update knowledge
```

The ideal system behaves like a reconciliation controller, not a blind timer:

```text
desired state
  -> observed state
  -> delta
  -> bounded action
  -> verified convergence
```

The desired state is not "move users every N minutes". The desired state is:

1. users receive service through channels that satisfy their policy/SLA needs;
2. unhealthy or unsuitable channels stop receiving new users;
3. users leave channels only when evidence, policy, authority, and blast limits allow it;
4. recovered channels re-enter service gradually;
5. every action leaves evidence that improves or reduces future confidence.

## 2. What Ideal V7 Knows

V7 must know:

| Knowledge | Meaning |
| --- | --- |
| Channels | What egress paths exist, their roles, limits, policy flags, and current users. |
| Services | Which user-facing services matter and how each channel performs for each service. |
| Users | User identity, policy, current channel, connection state, complaints, profile state, and SLA class. |
| Assignments | Why a user is on a channel, whether that assignment is still valid, and what target is safer. |
| Routes | Whether traffic reaches the intended route without mismatch or leak risk. |
| Capacity | Assignment pressure and safe headroom by channel, pool, and SLA class. |
| Quality | Latency, loss, throughput, stability, failure rate, and service-specific behavior. |
| Failures | What failed, where, who is affected, how severe it is, and whether it is still current. |
| Recovery | Whether a channel has recovered enough to accept traffic again. |
| Outcomes | What happened after V7 or an operator moved, retained, probed, or rejected a move. |
| Trust | Which components are mature enough for a tier and which remain below floor. |
| Freshness | Which evidence is current, stale, decayed, or retained only for history. |
| Policy | Who may be moved, where they may go, and which actions require human authority. |

## 3. What Ideal V7 Observes

V7 observes both active probes and passive reality.

| Observation Type | Examples | Ideal Use |
| --- | --- | --- |
| Active service probes | Telegram, YouTube, service matrix checks | Detect service-specific channel regression and recovery. |
| Active connectivity probes | ICMP/TCP/HTTP checks, route readiness | Establish basic reachability and route safety. |
| Passive user outcomes | post-switch quality, complaints, connection success, no-rollback | Prove whether decisions worked for real users. |
| Passive channel behavior | stability trend, fail rate, latency/throughput over user load | Learn practical suitability and capacity. |
| Planner outcomes | candidate accepted/rejected, blockers, selected moves | Learn where decision logic succeeds or fails. |
| Execution outcomes | apply success, verification success, rollback/no-rollback | Improve blast, rollback, and execution trust. |
| Operator outcomes | approved/rejected/overrode with context | Secondary supervised confirmation only. |

Active probes answer "can this path work now?" Passive outcomes answer "did this path work for users after a real decision?"

Ideal V7 needs both. Probe-only systems become overconfident. Passive-only systems react too slowly.

## 4. What Ideal V7 Decides

Ideal V7 produces explicit action decisions:

| Action | Meaning |
| --- | --- |
| `KEEP` | Current assignment is acceptable; no movement. |
| `MOVE` | Move one or more users to a better eligible channel under governance. |
| `FAILOVER` | Move affected users away from a failing channel. |
| `DRAIN` | Stop new assignments and gradually move users away if safe. |
| `QUARANTINE` | Remove channel from assignment/retention until recovery admission passes. |
| `RECOVER` | Re-admit a channel gradually after sufficient recovery evidence. |
| `PROBE_ONLY` | Collect fresh evidence; no movement. |
| `ASK_OPERATOR` | Human decision required because authority, confidence, policy, or ambiguity blocks autonomy. |
| `NO_ACTION` | No useful or safe action exists now. |

Decision flow:

```text
observed state
  -> policy constraints
  -> channel eligibility
  -> service suitability
  -> user/channel fit
  -> risk tier
  -> action type
  -> execution authority
```

## 5. What Ideal V7 Executes

Execution is always bounded.

Ideal execution requires:

1. a concrete planner packet;
2. target user/channel list;
3. policy clearance;
4. restore barrier;
5. rollback target;
6. blast-radius budget;
7. authority tier;
8. verification plan;
9. feedback/learning closure.

V7 must be able to execute:

- one-user governed canary;
- one-user autonomous canary after floors and authority pass;
- small bounded batch;
- drain by slices;
- quarantine without moving users;
- recover by staged admission;
- rollback to a prior known-good channel.

## 6. What Ideal V7 Verifies

Every mutation must be verified.

| Verification | Required Answer |
| --- | --- |
| Apply verification | Did the user actually move? |
| Connectivity verification | Is the user connected after move? |
| Service verification | Do required services work after move? |
| Route verification | Is there no mismatch/leak risk? |
| Quality verification | Did speed/latency/stability stay acceptable? |
| Rollback verification | If rollback was needed, did it restore service? |
| Learning verification | Was the outcome recorded and consumed? |

No verified outcome means no trust growth.

## 7. What Ideal V7 Learns

V7 learns from outcomes, not from labels alone.

It learns:

- channel/service suitability;
- user/channel fit;
- practical capacity under assigned load;
- prediction accuracy and source confidence;
- failure recurrence;
- recovery duration;
- rollback reliability;
- blast-radius safety;
- operator disagreement patterns where the operator had enough context.

Learning must update existing owners only. It must not create a second planner or a second truth source.

## 8. What Ideal V7 Forgets Or Decays

Ideal V7 retains evidence but decays its influence.

| Evidence Type | Freshness Expectation |
| --- | --- |
| Service probe | Minutes to hours; fast decay. |
| Route readiness | Minutes to hours; fast decay when topology changes. |
| Runtime readiness | Immediate; stale data should block action. |
| Channel behavior | Hours to weeks depending on stability. |
| Candidate outcome | Long-lived, but context-sensitive. |
| Blast/rollback safety | Long-lived, but tier/blast-size specific. |
| Operator comparison | Long-lived only if contextual and attributable. |

Forgetting means:

1. do not delete important history;
2. reduce stale evidence impact;
3. never let old success override current regression;
4. never let old failure permanently quarantine a recovered channel without new evidence.

## 9. When V7 Asks The Operator

V7 asks the operator when:

- confidence/trust/prediction floors for the target tier fail;
- target is surprising or contradicts recent operator expectation;
- policy or group constraints are ambiguous;
- rollback target is unknown;
- restore barrier is absent or expired;
- blast radius exceeds certified authority;
- data quality is insufficient or contradictory;
- the action is destructive, irreversible, or affects too many users;
- V7 detects a novel failure mode.

The operator should see:

```text
Problem
  -> affected users/channels
  -> V7 recommendation
  -> why
  -> risk
  -> approve/reject
```

## 10. When V7 Acts Autonomously

V7 acts autonomously only when all are true:

1. event is real and current;
2. planner packet is valid;
3. policy gates pass;
4. tier floors pass;
5. restore barrier and rollback target are valid;
6. blast budget allows the action;
7. verification can run;
8. feedback/learning will be recorded;
9. truth/convergence are aligned;
10. explicit authority for that tier exists.

Autonomy is tiered:

| Tier | Authority |
| --- | --- |
| `TIER_0` | Read-only preview. |
| `TIER_1` | Governed one-user operator review. |
| `TIER_2` | Governed canary after `70/70/70`. |
| `TIER_3` | Autonomous one-user after `70/70/70` plus explicit autonomous authority. |
| `TIER_4` | Small bounded batch after `85/85/85`. |
| `TIER_5` | Batch autonomy after `90/90/90`. |
| `TIER_6` | Production autonomy after `95/95/95` and explicit production approval. |

## 11. When V7 Stops Itself

V7 must stop before action when:

- evidence is stale;
- source confidence is low;
- planner and runtime disagree;
- channel is outside allowed role/policy;
- target is hard-full or blocked;
- restore barrier is invalid;
- rollback target is missing;
- truth/convergence fail;
- action would exceed blast budget;
- verification cannot run;
- an action loop would flap users.

V7 must stop after action when:

- verification fails;
- observed quality degrades;
- rollback is required;
- repeated moves happen without improvement;
- recovery admission did not hold;
- evidence no longer supports the decision.

## 12. Knowledge Objects

| Object | Source | Freshness | Confidence | Owner | Consumer | Decision Impact |
| --- | --- | --- | --- | --- | --- | --- |
| Channel Knowledge | registry, runtime, planner | current | high for identity, variable for quality | registry/planner/read models | planner, UI, autonomy | eligibility, retention, quarantine |
| Service Knowledge | service matrix and service actuals | fast | high only after repeated current checks | service matrix/intelligence | planner, diagnostics, trust | service suitability |
| User Assignment Knowledge | user registry and planner outcomes | current | high when runtime/user state matches | planner/user registry | planner, execution | keep/move/failover |
| Route Knowledge | route reality/readiness | fast | medium until verified by traffic | route read models | planner, diagnostics | route safety/blockers |
| Capacity Knowledge | limits + assigned users + observed behavior | current plus trend | high for configured limits, partial for observed capacity | planner/capacity/intelligence | planner, recovery, UI | assignment/load gates |
| Quality Knowledge | quality compact, speed, latency, failure rate | fast/medium | depends on sample and diversity | quality/intelligence | planner, trust | channel ranking and suitability |
| Failure Knowledge | events, probes, passive outcomes | fast | high when user-visible and attributable | events/intelligence | planner, attention | failover/quarantine |
| Recovery Knowledge | successful checks and retained outcomes | staged | requires hysteresis | service/quality/intelligence | planner/autonomy | recovery admission |
| Decision Outcome Knowledge | post-action verification and closure | long-lived | high when verified | execution/feedback/learning | trust, planner | confidence growth |
| Trust Knowledge | trust evolution summaries | medium | tier-specific | intelligence/trust inventory | autonomy gates | authority tier |
| Freshness Knowledge | evidence age/type/source | per evidence type | explicit | future evidence index/current owners | trust/planner | stale block/decay |
| Policy Knowledge | policy/group settings | current | high when configured | policy/planner/governance | planner/execution | allowed targets/actions |

## 13. Data Quality Model

High-quality data is decision-grade knowledge, not row count.

| Quality Dimension | Meaning |
| --- | --- |
| Freshness | Evidence is recent enough for its type. |
| Coverage | Evidence covers enough channels, services, users, and states for the decision. |
| Correctness | The observed outcome matches reality and later verification. |
| Consistency | Multiple sources do not contradict each other without explanation. |
| Diversity | Evidence covers normal, degraded, failed, recovered, loaded, and low-load states. |
| Source confidence | The source is reliable for this decision class. |
| User impact relevance | Evidence describes real user experience, not only internal health. |
| Service relevance | Evidence maps to the services users actually need. |
| Actionability | Evidence can lead to keep/move/probe/quarantine/recover/rollback. |

Rows without freshness, correctness, attribution, or actionability are not enough.

## 14. Evidence Maturity Model

| Stage | Requirements | V7 May Do | V7 Must Not Do |
| --- | --- | --- | --- |
| `RAW_OBSERVATION` | One raw reading/event/probe. | Display in diagnostics; trigger probe-only review. | Move users or increase trust materially. |
| `STABLE_SIGNAL` | Repeated or corroborated readings, current and attributable. | Affect attention, diagnostics, and planner ranking. | Grant autonomy by itself. |
| `CONFIRMED_KNOWLEDGE` | Signal verified against outcome or independent source. | Influence planner eligibility and confidence. | Override policy/restore/rollback gates. |
| `ACTIONABLE_KNOWLEDGE` | Known problem, target, risk, and safe action. | Prepare governed packet and ask operator. | Apply without tier authority. |
| `AUTONOMY_GRADE_KNOWLEDGE` | Tier floor passed, current evidence, rollback/restore/verification ready, explicit authority. | Act within blast budget. | Exceed tier, skip verification, or ignore fresh regression. |

## 15. Routing And Path Selection Model

Ideal V7 supports:

- `100+` channels;
- `10,000+` users;
- service-specific path needs;
- channel pools;
- capacity classes;
- SLA classes;
- channel quarantine;
- recovery admission;
- user migration;
- anti-flapping;
- progressive movement;
- rollback.

Core concepts:

| Concept | Ideal Meaning |
| --- | --- |
| Channel score | Diagnostic condition explanation, not assignment truth. |
| Channel decision | Planner/governance answer: use, keep, evacuate, emergency, blocked. |
| Service SLA | The service-specific quality/freshness requirement for user class. |
| Channel suitability | Whether this channel fits this user/service/policy now. |
| User assignment | Current binding plus reason and expiration/revalidation context. |
| Evacuation logic | Move users only when retention is unsafe and a safer target exists. |
| Recovery admission | Re-enter with probe-only, then canary, then gradual admission. |
| Load/capacity balancing | Respect configured limits and learned practical headroom. |

Anti-flapping requires:

1. hysteresis between fail and recover;
2. cooldown after move;
3. minimum observation window;
4. no repeated oscillation between two channels without new evidence;
5. operator stop when loop risk appears.

## 16. Target Architecture Layers

| Layer | Current Owner | Target Role | Missing Pieces | Implementation Path |
| --- | --- | --- | --- | --- |
| Observation | service matrix, quality compact, sentinel, route/runtime/capacity readers | Produce current active/passive evidence. | More passive user outcome telemetry and service-specific closure. | Extend existing owners; no new source until scale proves need. |
| Evidence Index / Knowledge Store | intelligence snapshots, trust inventory | Make evidence queryable by type/freshness/owner. | Unified knowledge quality/freshness model for 10k scale. | Shadow-first after production autonomy certification. |
| Decision Engine | `tools/v7-users-autoswitch`, decision surface | Decide keep/move/failover/drain/quarantine/recover/probe/ask/no-action. | Service/user/SLA class fit and recovery admission semantics. | Extend planner adapters and read models only after contract. |
| Risk / Authority | operator execution pipeline, floors, restore barrier | Gate action by tier, blast, policy, evidence maturity. | Autonomous boundary for TIER_3+. | Certify after TIER_2 evidence passes. |
| Execution | governed execution/autoswitch apply | Perform bounded moves. | Disabled production controller by design. | Enable only event-driven bounded authority after floors pass. |
| Verification / Rollback | restore barrier, rollback, feedback | Prove action worked or rollback. | Autonomous rollback certification. | One-user then batch certification. |
| Learning | intelligence platform, workers, snapshots | Convert outcomes to confidence/trust. | Higher-quality real outcomes and source confidence. | Governed/manual outcome closure. |
| Operator Surface | admin UI, attention, drawers | Show problem/action/why, not internals. | 10k triage scaling and SLA/cohort views. | Derived read models; no new workflow unless scale proves it. |

## 17. Current Mapping To Ideal

| Ideal Component | Current Classification | Evidence |
| --- | --- | --- |
| Observation | `EXISTS` | service matrix, quality compact, sentinel, route/runtime/capacity readers. |
| Active probes | `EXISTS` | service matrix and quality tools. |
| Passive real-user observations | `PARTIAL` | post-action/feedback exists; broad passive telemetry is incomplete. |
| Service-specific routing needs | `PARTIAL` | service matrix exists; SLA classes are not fully modeled. |
| User/channel fit | `PARTIAL` | planner/candidate outcomes exist but suitability quality is low. |
| Channel pools | `PARTIAL` | production pool exists; 100+ channel pool classes not modeled. |
| Capacity classes | `PARTIAL` | configured capacity exists; observed capacity shadow is concept-only. |
| SLA classes | `MISSING` | policy/group exists, but no canonical SLA class model for routing. |
| Quarantine | `PARTIAL` | assignment blockers/roles exist; staged recovery admission is not complete. |
| Recovery admission | `PARTIAL` | restore/recovery concepts exist; gradual admission model is missing. |
| Anti-flapping | `PARTIAL` | cooldowns/gates exist; explicit anti-flap state is not canonical. |
| Progressive movement | `PARTIAL` | BA/guided canaries exist; autonomous ladder is not certified. |
| Rollback | `EXISTS` | rollback model and restore barrier exist; autonomous rollback not certified. |
| Evidence maturity | `PARTIAL` | saturation/tier floors exist; explicit maturity stages added here. |
| Event-driven controller | `PARTIAL` | read-only event consumer certified; live apply disabled. |
| 10k-scale read models | `DEFERRED` | future evidence index/freshness is documented but not active. |
| Operator burden minimization | `PARTIAL` | attention/drawers improved; 10k triage requires cohort/SLA views. |

## 18. Why Existing Data Is Not Enough

The issue is not "V7 has collected nothing".

Current evidence shows:

1. prediction rows are matched (`21/21`) but source confidence is low;
2. service rows exist but are low-confidence;
3. candidate outcomes exist (`84/156`) but coverage and correctness are not enough;
4. visibility/capture/aggregation loss is now `0`;
5. blast and rollback are strong (`100`) but cannot substitute for suitability, service, or prediction;
6. passive real user/channel outcome closure is still sparse;
7. there is no full service/user/SLA outcome model;
8. freshness/decay is documented as future scale work, not active planner logic;
9. the ideal knowledge model was not explicit before this phase.

Therefore current data is insufficient because it is not yet autonomy-grade knowledge.

## 19. 10,000 User Scale Model

### NOW

- Keep one canonical planner.
- Keep one governance/execution path.
- Keep evidence collection through existing owners.
- Generate real governed/manual outcomes.
- Preserve truth/convergence.
- Define the ideal knowledge contract.

### NEXT

- Keep knowledge quality/readiness views and routing foundation overlays wired through the existing trust/evidence owner.
- Close service/user/channel outcome loops with real outcome records.
- Extend SLA/user cohort concepts from read-only fit into certified planner inputs only after contract proof.
- Certify recovery admission and anti-flapping semantics with real recovery/outcome evidence.
- Certify TIER_2 governed canary after floors pass.

### POST-PRODUCTION SCALE

- Evidence index and freshness model.
- Aggregated channel/service/user-cohort summaries.
- Cardinality control for per-user/per-service evidence.
- Decision latency budgets.
- 100+ channel pool grouping.
- 10k admin UI triage.
- Progressive autonomous rollout ladder.

## 20. Roadmap From Current To Ideal

| Phase | Goal | Code Change | Unchanged | Tests | Risk | Success Criteria |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Ideal Model + Knowledge Contract | Lock target model. | Docs/reference/ADR only. | Runtime/planner/execution. | Truth/convergence. | Low | Ideal model created. |
| 2. Knowledge Quality Model | Expose quality by freshness/coverage/correctness/actionability. | Existing read-model owners only. | Floors/formulas initially. | Unit + snapshot + truth. | Medium | Operator can see why evidence is not enough. |
| 3. Passive + Active Evidence Upgrade | Collect better real outcomes. | Existing service/quality/feedback owners. | No synthetic evidence. | Lifecycle tests. | Medium | Source confidence rises through real cycles. |
| 4. Service/User/Channel Outcome Closure | Tie decisions to verified outcomes. | Existing execution/feedback/intelligence; read-only closure contract active in routing foundation. | Planner authority. | End-to-end dry-run + closure tests. | Medium | Candidate outcomes become actionable knowledge. |
| 5. Autonomous Routing Decision Upgrade | Add service/user/SLA fit. | Read-only fit model active through existing trust/evidence inventory; future planner impact requires certification. | One planner/truth source. | Fit contract + planner regression tests. | High | Decisions explain user/service fit without bypassing governance. |
| 6. Event-Driven Bounded Autonomy | Enable event -> bounded action after floors. | Existing event/planner/packet/execution owners. | No timer-only movement. | Canary + rollback tests. | High | TIER_3 one-user autonomous canary passes. |
| 7. Scale Foundation For 10,000 Users | Build aggregated evidence/read models. | Existing-owner evidence index/freshness. | No direct planner impact until shadow passes. | Load/query/shadow tests. | Medium | 100+ channel, 10k user reads stay fast. |
| 8. Production Autonomy | Controlled production event-driven routing. | Enable certified controller authority. | Truth/convergence/rollback. | Production canary ladder. | Critical | TIER_6 approved and monitored. |

## 21. Stable Principles

1. Do not create another planner.
2. Do not create another execution path.
3. Do not create another truth source.
4. Distinguish channel score from channel decision.
5. Distinguish active probes from passive outcomes.
6. Distinguish raw evidence from autonomy-grade knowledge.
7. Movement requires authority, not just recommendation.
8. Recovery requires admission, not immediate trust.
9. Scale requires aggregation and decay, not more raw tables.
10. Operator burden falls only when V7 can explain and verify its own decisions.

## 22. Industry Principles Applied

Applicable patterns:

- Kubernetes controllers: desired state, current state, bounded reconciliation.
- Cloudflare load balancing: health first, then steering policy, with pool/endpoint removal on unhealthy state.
- Envoy health/outlier detection: active checks plus passive outlier ejection and backoff.
- Google SRE canarying: small time-limited exposure, evaluation, rollback, representative traffic.
- Argo Rollouts: analysis runs, failure limits, dry-run analysis, measurement retention.
- Google SRE automation: automation is useful only when scoped, reliable, and not amplifying bad decisions.

Industry sources:

- `https://kubernetes.io/docs/concepts/architecture/controller/`
- `https://developers.cloudflare.com/load-balancing/understand-basics/traffic-steering/`
- `https://developers.cloudflare.com/load-balancing/monitors/`
- `https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking`
- `https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier`
- `https://sre.google/workbook/canarying-releases/`
- `https://sre.google/sre-book/automation-at-google/`
- `https://sre.google/sre-book/monitoring-distributed-systems/`
- `https://argo-rollouts.readthedocs.io/en/stable/features/analysis/`

## 23. Verdict

`IDEAL_MODEL_CREATED`

V7's ideal is reachable in architecture shape, but not yet in runtime readiness. The current system already has most owners. The gap is knowledge maturity, service/user/SLA fit, passive outcome closure, recovery admission, anti-flapping, and certified event-driven authority at scale.
