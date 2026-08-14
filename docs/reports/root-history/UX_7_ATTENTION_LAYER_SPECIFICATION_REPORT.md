# UX.7 Attention Layer Specification Report

Project: V7 VOZDUH
Program: UX.7_ATTENTION_LAYER_SPECIFICATION
Date: 2026-06-14
Mode: specification only. No UI implementation. No UI changes. No new page, drawer, workflow, truth source, planner, governance path, execution path, storage, deploy, or runtime mutation.

## Truth Gate

Required gate was run before this specification.

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |

Truth gate verdict: PASS. UX.7 may proceed as read-only Attention Layer specification.

Inputs inspected:

| Input | Use |
|---|---|
| `UX_0_OPERATOR_TASK_DISCOVERY_AND_INFORMATION_ARCHITECTURE_REPORT.md` | Operator tasks, information hierarchy, noise removal, one-screen rule. |
| `UX_1_USER_DRAWER_REBUILD_SPECIFICATION_REPORT.md` | Three-screen User Drawer philosophy and Screen 1 answer model. |
| `UX_2_USER_DRAWER_WIREFRAME_AND_IMPLEMENTATION_PLAN_REPORT.md` | Exact future User Drawer structure and implementation readiness pattern. |
| `UX_3_REAL_WORLD_OPERATOR_SCENARIOS_AND_FINAL_VISUAL_MOCKUPS_REPORT.md` | Real operator scenarios and 5-second / 10-second validation model. |
| `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md` | Channel Drawer three-screen structure and User/Channel consistency. |
| `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md` | Commercial-ready User Drawer baseline: 2 buttons, human reasons, mobile pass. |
| `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md` | Final strategic verdict: `HYBRID_RECOMMENDED`. |
| `EXPLAINABILITY_2_CANONICAL_ADAPTER_AND_WHY_CARD_FOUNDATION_REPORT.md` | Existing read-only Why Card foundation and canonical explainability fields. |
| `admin/v7-admin-api` | Existing overview alerts, user drawer answer model, channel status, checks, route/security, recommendations, and operator decision surfaces. |

Commercial references used:

| Product | Source |
|---|---|
| Stripe Radar Reviews | `https://docs.stripe.com/radar/reviews` |
| Stripe Disputes | `https://docs.stripe.com/disputes` |
| Cloudflare One Insights | `https://developers.cloudflare.com/cloudflare-one/insights/` |
| Linear Triage | `https://linear.app/docs/triage` |
| Datadog Monitors | `https://docs.datadoghq.com/monitors/` |
| Datadog Incident Management | `https://docs.datadoghq.com/incident_response/incident_management/` |
| GitHub Security Overview | `https://docs.github.com/en/enterprise-cloud@latest/code-security/concepts/security-at-scale/about-security-overview` |

## 1. Existing Attention Sources

Attention Layer must be a thin operator layer above existing objects. It must not create a new problem database, ticket queue, planner, snapshot, governance model, execution path, or independent truth source.

Existing sources already contain attention signals:

| Existing Source | Problem Exists | Reuse | Gap |
|---|---|---|---|
| Overview Alerts | Yes | Reuse `buildAlerts`, `openOverviewAlertsCenter`, existing alert level/action/target shape. | Normalize alert cards into a smaller canonical attention item with one primary action and one details action. |
| Operator Center | Yes | Reuse existing operator decision surface, execution dashboard, approval preview, readiness/gate summaries. | Surface only "needs operator attention" states; do not expose execution internals in the attention list. |
| Recommendations | Yes | Reuse recommendation rows, `openUserRecommendationDrawer`, approval/ignore review flow. | Show "Recommendation waiting" as a review item without creating a second recommendation queue. |
| Why Cards | Yes | Reuse user/channel/planner `why_cards` from EXPLAINABILITY.2. | Use only the one-line reason in Attention Layer; full Why Card remains in Details. |
| User Status | Yes | Reuse `renderUserDrawerAnswer`, `userDrawerScreenOneReason`, `userPrimaryActionButton`, profile/connection/route/speed states. | Derive attention items from existing user state; no new user-state authority. |
| Channel Status | Yes | Reuse `channelOperatorStatus`, channel snapshots, service matrix summary, runtime readiness, assigned users. | Convert channel health/capacity/service warnings into problem-first items while opening existing Channel Drawer for detail. |
| Checks | Yes | Reuse checks/security workspaces, killswitch check, capacity check, routing checks, speed/service checks. | Failed/stale/actionable checks may create items; raw check rows must stay behind Details. |
| Warnings | Yes | Reuse user/channel warnings, phone confirmation warnings, route leak warnings, runtime blocking warnings. | Translate every warning into operator language; hide empty warnings. |
| Execution Readiness | Yes | Reuse execution dashboard/gates and existing blocked/readiness state. | Attention item can say "Execution blocked"; it must not execute or bypass governance. |
| Route Problems | Yes | Reuse route drawer, route reality, direct RU route checks, route mismatch and runtime drift records. | Link the item to User Drawer or Route detail; no separate route-problem workflow. |
| Leak Problems | Yes | Reuse killswitch/security checks, route leak detection, runtime drift `route-leak-risk` records. | Promote to highest severity and open existing checks/route/user detail. |
| Service Failures | Yes | Reuse channel service matrix, channel health, service compatibility, channel checklist. | Show one business-language failure summary; service rows remain Screen 2/3. |
| Capacity Problems | Yes | Reuse channel users/headroom, capacity status, execution capacity gates. | Show impact and action, not raw soft/hard/internal limits on first attention row. |
| Logs/Evidence | Indirect | Reuse only as proof inside existing details/evidence/history screens. | Logs/evidence must not create top-level attention noise unless another source already marks a problem. |

Source verdict: no new truth source is needed. V7 already has the source material; UX.7 only standardizes how active problems are projected to the operator.

## 2. Attention Item Model

Canonical Attention Item:

| Field | Required | Operator Meaning | Source Rule |
|---|---|---|---|
| Problem | Yes | What needs attention. Example: `Profile missing`. | Derived from existing alert/user/channel/check/recommendation/gate state. |
| Severity | Yes | How urgent this is. | Mapped from existing `bad`, `warn`, `info`, runtime blocking, check failure, and safety state. |
| Object Type | Yes | What kind of object is affected: user, channel, route, check, recommendation, execution. | Existing object family only. |
| Object Name | Yes | Human label: user name/IP, channel name, route name, check name, recommendation target. | Existing display fields. |
| Reason | Yes | One plain-language sentence explaining why it appears. | From existing humanized reason or compact Why Card reason. Raw values are forbidden. |
| Primary Action | Yes | One safe next action. | Existing action only: issue profile, check route, request speed, run check, open channel, review recommendation. |
| Details Action | Yes | Opens existing detail path. | Existing User Drawer, Channel Drawer, Route Drawer, Recommendation Drawer, Checks, Operator Center. |
| Source | Yes | Where the item came from. | Existing source id/family: overview alert, user status, channel status, check, route, recommendation, execution readiness. |
| Updated | Yes | When the signal was last refreshed. | Existing source timestamp when available; otherwise current overview/admin refresh time. |

Internal implementation may also keep object identifiers such as IP, channel id, route id, check id, or recommendation id, but those are not operator-visible fields.

Canonical item example:

```text
Problem: Profile missing
Severity: Needs Action
Object Type: User
Object Name: Ivan Petrov / 10.0.0.2
Reason: Profile not issued
Primary Action: Issue Profile
Details Action: Open User
Source: User Status
Updated: overview refresh time
```

Non-goals:

| Not Allowed | Reason |
|---|---|
| New persisted attention table | Creates a second truth source. |
| New ticket system | Violates "no new workflow" and adds operator overhead. |
| New problem page | Violates "no new page"; object drawers already exist. |
| New execution/apply path | Violates governance and safety constraints. |
| New planner | V7 already has planner/decision/execution surfaces. |
| Raw source payload on the attention item | Increases cognitive load and leaks technical language. |

## 3. Severity Model

Use existing severity language wherever possible. Do not invent a separate risk engine.

Recommended operator severity:

| Attention Severity | Existing Inputs | Meaning | Example |
|---|---|---|---|
| Critical | Runtime blocking, route leak risk, security/killswitch failure, service failure affecting users, execution unsafe | Safety or outage risk; operator should look first. | Leak risk, channel failure, execution blocked by safety gate. |
| Needs Action | Existing `bad`, blocking user state, phone confirmation, profile missing, capacity overflow, recommendation waiting for decision | Operator has a clear next action. | Profile missing, phone confirmation required, channel overload. |
| Needs Check | Existing `warn`, stale/no measurements, route requires verification, speed needs fresh check, low stability | Operator should verify before deciding. | Speed complaint, route needs check, no recent channel measurements. |
| Waiting | Existing `info`, user waiting for first connection, non-urgent pending state | Not urgent but should remain visible when relevant. | User has not connected yet. |

Healthy is not an attention severity. Healthy objects remain in Users, Channels, Routes, and normal object-first views.

Ordering rule:

```text
Critical
Needs Action
Needs Check
Waiting

Within same severity:
  most recent safety/user-impact item first
  then wider impact before single object
  then existing source order
```

Deduplication rule:

```text
problem + object_type + object_identifier + source_family
```

If the same problem appears from overview alert and object state, keep one item and prefer the source with the clearer primary action.

## 4. Example Attention Items

| Problem | Severity | Object | Reason | Primary Action | Details |
|---|---|---|---|---|---|
| Profile Missing | Needs Action | User: Ivan Petrov / 10.0.0.2 | Profile not issued | Issue Profile | Open User Drawer |
| No Connection | Waiting or Needs Check | User: Ivan Petrov / 10.0.0.2 | User has not connected | Check Connection | Open User Drawer |
| Speed Complaint | Needs Check | User: Olga Smirnova / 10.0.0.5 | Fresh speed check required | Request Speed Check | Open User Drawer |
| Route Issue | Needs Action | User or Route | Route verification required | Check Route | Open User Drawer or Route Drawer |
| Leak Risk | Critical | Route/User/Check | Route leak risk detected | Run Killswitch Check | Open Checks or Route detail |
| Channel Failure | Critical | Channel: awg3 | Channel service check failed | Run Service Check | Open Channel Drawer |
| Channel Overload | Needs Action | Channel: awg3 | Too many users on this channel | Open Users | Open Channel Drawer |
| Execution Blocked | Critical or Needs Action | Execution Readiness | Action is blocked by safety gate | Open Readiness | Open Operator Center |
| Recommendation Waiting | Needs Action | Recommendation/User | Review recommended route change | Review Recommendation | Open Recommendation Drawer |

Compact operator list target:

```text
--------------------------------------------------
NEEDS ATTENTION (4)
--------------------------------------------------

Critical
Leak risk
Route: RU direct
[Run Check]   [Details]

Needs Action
Profile missing
Ivan Petrov / 10.0.0.2
[Issue Profile]   [Details]

Needs Check
Speed complaint
Olga Smirnova / 10.0.0.5
[Request Check]   [Details]

Waiting
Recommendation waiting
Maria / awg3 -> awg4
[Review]   [Details]
--------------------------------------------------
```

List rule:

| Visible on Item | Hidden From Item |
|---|---|
| Problem title | Raw metrics |
| Affected object | Trust score |
| One reason sentence | Suitability score |
| One primary action | Execution chain |
| One details action | Evidence/logs/contracts |
| Severity | Service matrix rows |
| Updated age if useful | Raw reasons/internal buckets |

## 5. Healthy State Experience

Healthy state must remain calm and object-first. If there are no active attention items, do not show an empty queue or fake problem dashboard.

Healthy state target:

```text
--------------------------------------------------
NO ACTIVE ISSUES
--------------------------------------------------

Internet working normally
Users: X
Channels: Y

[Users]   [Channels]   [Routes]
--------------------------------------------------
```

Healthy rules:

| Rule | Reason |
|---|---|
| No attention cards when count is zero | Empty operational surfaces become noise. |
| Continue to Users / Channels / Routes | Healthy state is object-first by UX.6. |
| Show simple system confidence | Operator should know nothing is urgent. |
| Keep checks available | Operator can still investigate manually. |
| Do not show raw green metrics | Green tables do not help daily operators. |

This preserves the UX.6 hybrid decision:

```text
Healthy state:
  Object First

Problem state:
  Problem First
```

## 6. Object Integration

Attention item must always resolve into an existing object or existing workflow.

| Attention Item Type | Opens Existing Surface | Existing Action Principle |
|---|---|---|
| Profile Missing | User Drawer | Primary action uses existing profile issuance path. |
| No Connection | User Drawer | Primary action uses existing connection/profile/check action. |
| Speed Complaint | User Drawer Speed area | Primary action uses existing speed request/check. |
| Route Issue | User Drawer or Route Drawer | Primary action uses existing route check. |
| Leak Risk | Checks/Security, Route Drawer, or affected User Drawer | Primary action uses existing killswitch/security check. |
| Channel Failure | Channel Drawer | Primary action uses existing service check/channel investigation. |
| Channel Overload | Channel Drawer assigned users/capacity | Primary action opens existing users/capacity context. |
| Execution Blocked | Operator Center / execution dashboard | Primary action opens readiness; no execute action. |
| Recommendation Waiting | Existing Recommendation Drawer | Primary action opens review; approval still follows existing governance. |

Integration rule:

```text
Attention Layer does not own the problem.
It points operator to the existing owner.
```

No separate "problem detail" drawer is allowed. Details means existing object details.

## 7. Commercial Benchmark

| Product | Philosophy Observed | Attention Layer Lesson |
|---|---|---|
| Stripe Reviews/Disputes | Active risk/review work is presented as a queue, with object/payment details behind the decision. | V7 should show active operational work first, then open user/channel details. |
| Linear Triage | Incoming work is triaged from an inbox, but the canonical object remains the issue. | V7 can have an attention list without becoming a ticket system. |
| Cloudflare Alerts/Insights | Network visibility is hybrid: dashboards for healthy monitoring, diagnostics/alerts for active issues. | Healthy V7 stays object-first; problem state becomes attention-first. |
| Datadog Monitors/Incidents | Operators start from alert/incident when action is needed, then drill into services/logs. | V7 attention items should lead with problem and one action, with evidence deeper. |
| GitHub Security Overview | Risk/alert views aggregate across repositories, then open canonical object/remediation context. | V7 can aggregate user/channel/route risks without duplicating those objects. |

Commercial conclusion: the strongest fit is a thin triage/attention layer, not a new page. It should behave like an operational inbox only when problems exist, and disappear into calm system status when nothing needs action.

## 8. Noise Audit

These must never appear in the compact Attention Layer:

| Noise Item | Why It Is Noise | Allowed Place |
|---|---|---|
| Raw metrics | Operator needs decision first, not measurement table. | Existing drawer Screen 2/3. |
| Trust score | Technical confidence, not first action. | Channel/User details, Why Card full view. |
| Suitability score | Internal recommendation detail. | Recommendation Drawer / Why Card detail. |
| Execution details | Can imply action is executable and adds stress. | Operator Center / execution dashboard. |
| Evidence bundles | Proof is useful after problem selection. | Existing Evidence/detail sections. |
| Logs | Investigation/audit only. | Logs and Screen 3. |
| Contracts | Governance/technical proof, not operator triage. | Screen 3 / Operator Center. |
| Raw reasons | Internal labels confuse non-technical operators. | Technical details only. |
| Service matrix rows | Too dense for first attention list. | Channel Drawer Screen 2. |
| Config/export/delete/admin commands | Risky or rare actions. | Existing guarded technical paths. |
| Multiple primary buttons | Increases decision cost. | Attention item allows one primary plus Details only. |
| Empty warnings | Consume space and create false concern. | Hidden. |
| Full history/timeline | Useful only after diagnosis. | Existing history/audit views. |

Allowed first-layer copy examples:

| Internal/Raw Style | Operator Style |
|---|---|
| `best-available-pool_not_fresh` | Need fresh data |
| `sticky_keep_current` | Current route is best |
| `runtime_blocking` | Action is blocked by safety check |
| `route-leak-risk` | Route leak risk detected |
| `candidate-suitability-summary` | Recommendation needs review |

## 9. Cognitive Load Comparison

| Model | Clicks To First Problem | Time To Understand | Time To First Action | Operator Stress | Main Risk |
|---|---:|---|---|---|---|
| Current admin only | 1-4 | 20-60 seconds when object is unknown | 30-90 seconds | Medium | Operator must know which object to inspect. |
| Current admin + Attention Layer | 0-1 | 5-10 seconds | 10-20 seconds | Low/Medium | Attention list must stay small and deduplicated. |
| Full problem-first rewrite | 0-1 | 5-10 seconds | 10-20 seconds | Medium | Would hide healthy object model and violate no-new-workflow direction. |

Workflow comparison:

| Workflow | Current Admin | With Attention Layer |
|---|---|---|
| Daily "what is broken?" | Overview, tabs, alerts, checks, drawers | Needs Attention list first. |
| Known user complaint | Open user, read drawer | Open user as today; attention may confirm problem. |
| Leak risk | Checks/routing/alerts must be noticed | Critical item appears at top and opens existing check/route detail. |
| Channel failure | Operator must inspect channel/table/checks | Channel problem item opens Channel Drawer. |
| Healthy monitoring | Users/Channels/Routes | Same object-first flow; attention count is zero. |

UX.7 expected impact:

| Metric | Current | With Attention Layer |
|---|---|---|
| First screen question | "Which object should I inspect?" | "What needs attention?" |
| Visible action count | Varies by surface | One primary per item. |
| Cross-object problems | Fragmented | Aggregated by problem. |
| Raw technical exposure | Medium/high in older surfaces | Hidden until details. |
| Healthy day experience | Object-first | Object-first, unchanged. |

## 10. Final Attention Layer Architecture

Final architecture:

```text
Existing Sources
  Overview Alerts
  User Status
  Channel Status
  Why Cards
  Checks
  Route/Security Signals
  Recommendations
  Execution Readiness

        |
        v

Derived Attention Projection
  normalize
  humanize reason
  assign existing severity
  attach existing action
  attach existing details target
  deduplicate
  sort

        |
        v

Operator Attention Layer
  compact count
  compact item list
  one primary action
  one details action

        |
        v

Existing Object Surfaces
  User Drawer
  Channel Drawer
  Route Drawer
  Recommendation Drawer
  Checks
  Operator Center
```

Architecture rules:

| Rule | Decision |
|---|---|
| Storage | None. Derived only from existing admin/source payloads. |
| State ownership | Existing owners keep ownership: user, channel, route, checks, recommendation, execution readiness. |
| Rendering ownership | Future implementation may place a compact attention band/list in existing overview/admin flow, but UX.7 does not implement it. |
| Actions | Existing actions only. No new apply, no new execution, no new governance bypass. |
| Details | Existing drawers/workflows only. No new problem drawer. |
| Reason | Plain operator sentence only. Full Why Card remains deeper. |
| Severity | Mapped from existing levels and safety gates. |
| Deduplication | Required before display. |
| Empty state | Calm healthy state, no empty queue. |
| Mobile | Compact list; each item must fit with problem, object, primary action, details. |

Future implementation phases, when approved:

| Phase | Scope | Risk |
|---|---|---|
| Phase 1 | Build read-only attention projection from existing overview alerts and user/channel status helpers. | Low |
| Phase 2 | Add recommendation/check/execution readiness items using existing payloads. | Medium |
| Phase 3 | Add UI compact list/band in existing overview surface and route items to existing drawers. | Medium |
| Phase 4 | Visual validation desktop/mobile, button/noise/severity audit. | Low |

Implementation readiness constraints:

| Constraint | Required |
|---|---|
| No new endpoint | Prefer existing admin payloads unless a future existing endpoint extension is approved. |
| No new DB/state | Required. |
| No new page/drawer | Required. |
| No new workflow | Required. |
| No new execution path | Required. |
| Existing object integration | Required. |
| Truth/convergence gates | Required before and after implementation. |

## 11. Verdict

READY_FOR_ATTENTION_IMPLEMENTATION

Reason:

V7 should add a thin derived Attention Layer above existing Users, Channels, Routes, Checks, Recommendations, Why Cards, and Operator Center. This follows the UX.6 hybrid model:

```text
Healthy state:
  Object First

Problem state:
  Problem First
```

The layer is commercially justified and technically safe because it reuses existing truth, existing object owners, existing drawers, existing actions, and existing governance. It should not become a ticket system, page, drawer, planner, storage model, or execution path.

Alignment status at specification time:

| Check | Status |
|---|---|
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS; docs-only runtime mismatch acceptable for reports |
| Truth | PASS / FULLY_ALIGNED |
| Convergence | PASS / ALIGNED |
