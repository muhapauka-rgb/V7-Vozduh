# V7 Knowledge Quality Model

Status: canonical knowledge quality model
Phase: `V7.KNOWLEDGE.QUALITY.MODEL`
Date: 2026-06-24
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Base commit: `f46a28639e839cb585e29289a9f5e044eecb963b`

This document defines how V7 evaluates routing knowledge quality.

It is not a trust audit, confidence audit, canary audit, outcome count audit, runtime authorization, planner redesign, governance redesign, execution redesign, formula change, floor change, new truth source, synthetic evidence action, daemon enablement, autoswitch enablement, or user movement.

## 1. Purpose

V7 must separate four different things:

```text
data
  -> signal
  -> knowledge
  -> action authority
```

Rows, reports, probes, screenshots, or audits are not automatically knowledge.

High-quality routing knowledge is current, covered, correct, consistent, diverse, attributable to a reliable source, relevant to users and services, and actionable through existing V7 owners.

## 2. Scoring Scale

Every knowledge object is scored from `0` to `5` on each quality dimension.

| Score | Meaning |
| ---: | --- |
| `0` | Missing or unknown. |
| `1` | Exists as raw or isolated data; not reliable for decisions. |
| `2` | Repeated or visible, but incomplete, stale, weakly attributed, or weakly actionable. |
| `3` | Usable supporting signal; may affect attention, diagnostics, ranking, or preview. |
| `4` | Actionable knowledge; can prepare governed packets or block unsafe actions. |
| `5` | Autonomy-grade for its tier; current, verified, attributable, safe, and authority-ready. |

Quality dimensions:

| Dimension | Meaning |
| --- | --- |
| Freshness | Evidence is recent enough for its type. |
| Coverage | Evidence covers relevant channels, services, users, policies, and states. |
| Correctness | Evidence matches reality or later verification. |
| Consistency | Sources agree or contradictions are explained. |
| Diversity | Evidence covers normal, degraded, failed, recovered, loaded, and low-load states. |
| Source Confidence | The source is reliable for the decision class. |
| User Impact Relevance | Evidence maps to real user experience. |
| Service Relevance | Evidence maps to services users actually need. |
| Actionability | Evidence can safely drive keep, move, failover, drain, recover, probe, rollback, or ask-operator decisions. |

## 3. Knowledge Inventory

| Knowledge Object | Owner | Source | Consumer | Purpose |
| --- | --- | --- | --- | --- |
| Channel Knowledge | registry, planner, read models | egress registry, runtime state, planner output | planner, UI, autonomy | Know what channels exist, roles, limits, users, and assignment posture. |
| Service Knowledge | service matrix, intelligence | service probes, service actual rows | planner, diagnostics, trust | Know whether each channel supports required services. |
| User Assignment Knowledge | planner, user registry | user registry, current channel, candidate outcomes | planner, execution, UI | Know who is where, whether that assignment still makes sense, and where a safer target may be. |
| Route Knowledge | route read models | route reality, route readiness, leak/mismatch evidence | diagnostics, planner support | Know whether route path is safe and not leaking/mismatched. |
| Capacity Knowledge | planner, capacity/read models | configured limits, assigned users, dynamic load summaries | planner, recovery, UI | Know assignment pressure and safe headroom. |
| Quality Knowledge | quality compact, intelligence | speed, latency, stability, failure rate | planner, trust, diagnostics | Know current and historical channel behavior. |
| Failure Knowledge | events, probes, intelligence | sentinel, service matrix, quality regressions, planner blockers | attention, planner, operator | Know what failed, who is affected, and whether action is required. |
| Recovery Knowledge | service/quality/intelligence | successful checks, retained outcomes, post-recovery behavior | planner, autonomy | Know when a failed channel can safely re-enter service. |
| Decision Outcome Knowledge | execution, feedback, learning | post-action verification, closure, rollback/no-rollback | trust, planner, learning | Know whether previous keep/move/failover decisions worked. |
| Prediction Knowledge | intelligence workers/platform | forecasts, later actuals, governed prediction feedback | trust, autonomy gates | Know whether V7's forecasts predict reality. |
| Suitability Knowledge | trust inventory, intelligence, planner outcomes | candidate outcomes, selected/rejected moves, correctness | planner, trust, autonomy | Know whether channel recommendations fit real users and services. |
| Trust Knowledge | trust evolution, trust inventory | confidence components, source inventory, floors | governance, autonomy gates | Know which tier V7 may enter. |
| Policy Knowledge | planner, policy/governance | policy/group settings, access rules, channel roles | planner, execution | Know what moves and targets are allowed. |
| Freshness Knowledge | snapshots, future freshness/index owner, current evidence owners | evidence timestamps, source families, refresh state | planner, trust, UI | Know whether evidence is current, stale, or history-only. |
| Safety Knowledge | restore, rollback, packet, blast owners | packet validation, restore preview, rollback manifest, blast evidence | governance, execution, autonomy | Know whether bounded action can be applied and recovered. |
| Event Knowledge | event sources and read-only consumer | sentinel, service matrix, quality/capacity/route/runtime events | attention, planner preview, autonomy preview | Know whether a real regression should trigger the decision chain. |
| Operator Context Knowledge | shadow autonomy, operator comparison | contextual approve/reject/override evidence | secondary trust, UI | Know where human context agrees or disagrees with V7. |

## 4. Quality Scores

These scores summarize current certified project truth. They do not change runtime behavior.

| Knowledge Object | Fresh | Cover | Correct | Consist | Diverse | Source | User Impact | Service | Action | Average | Maturity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Channel Knowledge | 4 | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | 3.7 | `ACTIONABLE_KNOWLEDGE` |
| Service Knowledge | 3 | 3 | 3 | 3 | 2 | 2 | 2 | 4 | 3 | 2.8 | `STABLE_SIGNAL` |
| User Assignment Knowledge | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 2 | 4 | 3.7 | `ACTIONABLE_KNOWLEDGE` |
| Route Knowledge | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 2 | 3 | 2.7 | `STABLE_SIGNAL` |
| Capacity Knowledge | 4 | 4 | 4 | 4 | 2 | 4 | 3 | 2 | 4 | 3.4 | `CONFIRMED_KNOWLEDGE` |
| Quality Knowledge | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 2.9 | `STABLE_SIGNAL` |
| Failure Knowledge | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 3.2 | `CONFIRMED_KNOWLEDGE` |
| Recovery Knowledge | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | 2.1 | `STABLE_SIGNAL` |
| Decision Outcome Knowledge | 3 | 3 | 4 | 4 | 3 | 4 | 4 | 2 | 4 | 3.4 | `CONFIRMED_KNOWLEDGE` |
| Prediction Knowledge | 4 | 3 | 4 | 4 | 2 | 2 | 3 | 3 | 3 | 3.1 | `CONFIRMED_KNOWLEDGE` |
| Suitability Knowledge | 3 | 2 | 2 | 3 | 2 | 2 | 4 | 3 | 3 | 2.7 | `STABLE_SIGNAL` |
| Trust Knowledge | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 2 | 4 | 3.1 | `ACTIONABLE_KNOWLEDGE` |
| Policy Knowledge | 4 | 3 | 4 | 4 | 2 | 4 | 3 | 2 | 5 | 3.4 | `ACTIONABLE_KNOWLEDGE` |
| Freshness Knowledge | 2 | 2 | 3 | 3 | 2 | 3 | 2 | 2 | 2 | 2.3 | `STABLE_SIGNAL` |
| Safety Knowledge | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 2 | 5 | 4.1 | `AUTONOMY_GRADE_KNOWLEDGE` |
| Event Knowledge | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3.1 | `CONFIRMED_KNOWLEDGE` |
| Operator Context Knowledge | 2 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 1.9 | `RAW_OBSERVATION` |

## 5. Current Maturity Distribution

This is a knowledge-object estimate, not row counting.

| Maturity Stage | Approx Share | Objects |
| --- | ---: | --- |
| `RAW_OBSERVATION` | 6% | Operator Context Knowledge |
| `STABLE_SIGNAL` | 35% | Service, Route, Quality, Recovery, Suitability, Freshness |
| `CONFIRMED_KNOWLEDGE` | 29% | Capacity, Failure, Decision Outcome, Prediction, Event |
| `ACTIONABLE_KNOWLEDGE` | 24% | Channel, User Assignment, Trust, Policy |
| `AUTONOMY_GRADE_KNOWLEDGE` | 6% | Safety |

Current V7 has broad knowledge, but most of it is not autonomy-grade.

## 6. Tier Knowledge Requirements

| Tier | Required | Optional | Supporting | Diagnostic Only |
| --- | --- | --- | --- | --- |
| `TIER_0` Read-only preview | Channel, User Assignment, Planner, Policy, Event, Service, Quality | Prediction, Trust | Route, Capacity, Freshness | Raw logs, technical health details |
| `TIER_1` Governed one-user operator review | Channel, User Assignment, Policy, Safety, Planner packet, Restore preview, Rollback target | Prediction, Trust, Suitability | Service, Quality, Capacity, Route | Operator comparison, raw diagnostics |
| `TIER_2` Governed canary after floors | Channel, Assignment, Policy, Safety, Trust, Prediction, Decision Outcome, Suitability, Freshness | Operator Context | Service, Quality, Capacity, Route, Event | Technical health internals |
| `TIER_3` Autonomous one-user | All TIER_2 plus Event, Recovery, post-action verification, anti-flap/cooldown knowledge | Operator Context | Route, Capacity, Quality | Raw logs |
| `TIER_4` Small bounded batch | All TIER_3 plus cohort/service impact, batch rollback, capacity headroom, blast evidence by batch size | Operator Context | Observed capacity shadow | Technical health internals |
| `TIER_5` Batch autonomy | All TIER_4 plus recovery admission, stale-evidence decay, passive outcome closure, service/user fit | Operator Context | SLA/cohort read models | Raw probes alone |
| `TIER_6` Production autonomy | All TIER_5 plus autonomy-grade event controller, verified rollback, learning closure, 10k read-model scale | Operator Context | Long horizon trends | Raw unverified evidence |

## 7. Autonomy Readiness By Knowledge Object

| Knowledge Object | TIER_1 | TIER_2 | TIER_3 | TIER_4-6 | Current Readiness |
| --- | --- | --- | --- | --- | --- |
| Channel | Required | Required | Required | Required | Ready for governed review. |
| Service | Supporting | Required | Required | Required | Not autonomy-grade; low source confidence. |
| User Assignment | Required | Required | Required | Required | Ready for governed review. |
| Route | Supporting | Supporting | Required when route risk exists | Required | Supporting, not complete path-selection truth. |
| Capacity | Supporting | Required | Required | Required | Configured capacity strong; observed capacity partial. |
| Quality | Supporting | Required | Required | Required | Stable signal, not enough alone. |
| Failure | Supporting | Required | Required | Required | Confirmed for attention/read-only; live apply not authorized. |
| Recovery | Optional | Supporting | Required | Required | Major gap. |
| Decision Outcome | Optional | Required | Required | Required | Partial coverage; candidate outcomes incomplete. |
| Prediction | Optional | Required | Required | Required | Correctness high, source confidence low. |
| Suitability | Supporting | Required | Required | Required | Major blocker. |
| Trust | Supporting | Required | Required | Required | Correctly blocks higher tiers. |
| Policy | Required | Required | Required | Required | Strong for current governed paths. |
| Freshness | Supporting | Required | Required | Required | Not explicit enough for 10k autonomy. |
| Safety | Required | Required | Required | Required | Strongest knowledge class. |
| Event | Optional | Supporting | Required | Required | Read-only certified, not apply authority. |
| Operator Context | Optional | Optional | Optional | Optional | Secondary and underfed. |

## 8. Knowledge Gaps

These are missing knowledge, not missing code owners.

| Gap | Type | Why It Blocks |
| --- | --- | --- |
| Service/user/SLA fit | Service relevance, user impact, policy context | V7 cannot know the best target for a user if it does not know what services and SLA class that user needs. |
| Passive real-user outcome closure | Correctness, user impact | Active probes cannot prove a route worked for real users after a real decision. |
| Recovery admission knowledge | Correctness, consistency, anti-flap | A channel that looks better once is not necessarily safe to re-admit. |
| Suitability correctness | Correctness, coverage | Candidate outcomes are incomplete and mean correctness remains too weak. |
| Source confidence for predictions/services | Source confidence | Accurate matches still do not raise confidence enough when source confidence is low. |
| Freshness/decay semantics | Freshness, actionability | Old evidence must not outweigh current regression at 10k scale. |
| Cohort/SLA knowledge | Coverage, user impact | 10k users require cohort reasoning, not per-row operator scanning. |
| Autonomous rollback certification | Actionability, safety | Operator-free apply cannot be trusted without verified rollback closure. |
| Anti-flap knowledge | Consistency, actionability | Repeated movement without improvement must be blocked explicitly. |
| Contextual operator comparison | Secondary source confidence | Useful supervised signal is still underfed and must stay contextual. |

## 9. Quality Bottlenecks

| Area | Current Limiter | Bottleneck Class |
| --- | --- | --- |
| Prediction Quality | Matches are complete, but forecast/source confidence is low. | SOURCE_CONFIDENCE |
| Service Knowledge Quality | Service rows exist but are low-confidence and not fully tied to service/user/SLA outcomes. | SOURCE_CONFIDENCE + SERVICE_RELEVANCE |
| Suitability Quality | Candidate outcomes exist but coverage/correctness are insufficient. | COVERAGE + CORRECTNESS |
| Trust Quality | Trust correctly inherits weak prediction/service/suitability inputs. | QUALITY + ATTRIBUTION |
| Autonomy Readiness | Safety is strong, but service/user/suitability/recovery/freshness knowledge is not autonomy-grade. | ACTIONABILITY + COVERAGE |

## 10. Routing System Comparison

| System Pattern | Knowledge They Usually Possess | V7 Status |
| --- | --- | --- |
| SD-WAN path routing | SLA class, application path quality, path health, policy, brownout/blackout state | Partial: V7 has health/policy, lacks full SLA/application fit. |
| Traffic engineering control plane | Desired/current state, capacity, utilization, route safety, convergence state | Partial: desired/current structure exists, scale/cohort read models missing. |
| Load balancers | Pool/endpoint health, active/passive checks, ejection/recovery, traffic steering policy | Partial: service health and planner decisions exist; staged recovery admission incomplete. |
| Active/passive health systems | Probe health plus passive outlier/outcome detection | Partial: active probes strong, passive user outcome closure underfed. |
| Progressive delivery/canary | Blast budget, verification, rollback, promotion/abort criteria | Strong in safety; not yet strong in service/user/suitability evidence. |
| Kubernetes-style controllers | Desired state, current state, diff, bounded reconciliation, status feedback | Architecture matches; live event-driven controller remains disabled by design. |

## 11. 10,000 User / 100+ Channel Readiness

| Knowledge Object | Scale Readiness | Reason |
| --- | --- | --- |
| Channel | PARTIAL | Registry/planner can scale conceptually, but pool classes for 100+ channels need explicit read models. |
| Service | PARTIAL | Service matrix exists; service families/SLA fit and aggregation need work. |
| User Assignment | PARTIAL | Current assignment truth exists; 10k needs cohort summaries and action batching views. |
| Route | PARTIAL | Supporting route evidence exists; route aggregation and per-cohort route risk need work. |
| Capacity | PARTIAL | Configured limits scale; observed practical capacity is not implemented. |
| Quality | PARTIAL | Quality compact exists; 10k needs indexed summaries and freshness/decay. |
| Failure | PARTIAL | Events exist; attention prioritization needs cohort impact and source maturity. |
| Recovery | NOT_READY | Staged recovery admission is not canonical enough. |
| Decision Outcome | PARTIAL | Outcome closure exists but coverage is incomplete. |
| Prediction | PARTIAL | Lifecycle works; source confidence and future cycles are the issue. |
| Suitability | NOT_READY | Current suitability is too low/incomplete for broad autonomy. |
| Trust | PARTIAL | Gates are structurally correct; inputs are not enough. |
| Policy | PARTIAL | Current policy works; SLA/cohort policy needs richer modeling. |
| Freshness | NOT_READY | Future freshness/index model is documented but not active. |
| Safety | READY | Restore/rollback/blast knowledge is the strongest area. |
| Event | PARTIAL | Read-only chain certified; apply authority missing by design. |
| Operator Context | NOT_READY | Secondary path exists but evidence is sparse and contextual only. |

## 12. Knowledge Roadmap

| Priority | Current Knowledge State | Required Knowledge State | Gap | Implementation Path |
| --- | --- | --- | --- | --- |
| P0 | Suitability is `STABLE_SIGNAL`. | Suitability becomes `ACTIONABLE_KNOWLEDGE`. | Coverage/correctness. | Use existing candidate outcome, feedback, and intelligence owners; no synthetic evidence. |
| P0 | Recovery is `STABLE_SIGNAL`. | Recovery becomes `ACTIONABLE_KNOWLEDGE`. | Admission/hysteresis. | Define recovery admission contract in planner/read models before any autonomous recovery. |
| P0 | Freshness is implicit/supporting. | Freshness blocks stale action and labels stale knowledge. | Explicit decay/actionability. | Add read-only freshness/maturity labels through existing snapshot/trust inventory owners. |
| P0 | Service knowledge is probe-heavy. | Service knowledge is service/user/SLA outcome-aware. | Service relevance and user impact. | Extend existing service/intelligence summaries; keep planner unchanged until contract is proven. |
| P0 | Safety is strong but autonomous rollback not certified. | Rollback is certified for autonomous tier. | Operator-free verification. | Certify one-user rollback before TIER_3. |
| P1 | Prediction matches are accurate but under-confident. | Prediction source confidence grows through future real cycles. | Source confidence. | Continue forecast-to-later-actual evidence through existing owners. |
| P1 | Event consumer is read-only. | Event can trigger bounded apply after floors. | Authority. | Keep read-only until confidence/trust/prediction and restore/rollback pass. |
| P1 | Policy knows current constraints. | Policy includes SLA/cohort routing context. | SLA model. | Add read-only SLA/cohort model before planner impact. |
| P2 | Operator context evidence is sparse. | Contextual operator comparison supports supervised confidence. | Evidence. | Use existing compare endpoint only where operator has context. |
| P2 | 10k read models are deferred. | Aggregated channel/service/cohort summaries exist. | Scale. | Start after production autonomy or when read pressure proves need; shadow-first. |

## 13. Final Verdict

`KNOWLEDGE_MODEL_COMPLETE`

V7 now has a canonical knowledge quality model. Current V7 knowledge is broad and structurally well-owned, but only Safety Knowledge is autonomy-grade today. Most routing knowledge is stable, confirmed, or actionable for governed review, not sufficient for operator-free autonomy.

