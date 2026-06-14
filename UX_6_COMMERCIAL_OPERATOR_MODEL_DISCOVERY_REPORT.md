# UX.6 Commercial Operator Model Discovery Report

Project: V7 VOZDUH  
Program: UX.6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY  
Date: 2026-06-14  
Mode: discovery only. No UI implementation. No UI changes. No drawer changes. No deploy.

## Truth Gate

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |

Inputs inspected:

| Input | Use |
|---|---|
| `UX_0_OPERATOR_TASK_DISCOVERY_AND_INFORMATION_ARCHITECTURE_REPORT.md` | Daily operator tasks, information hierarchy, noise audit. |
| `UX_3_REAL_WORLD_OPERATOR_SCENARIOS_AND_FINAL_VISUAL_MOCKUPS_REPORT.md` | Five-second / ten-second operator scenarios. |
| `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md` | Channel drawer philosophy and one-screen rule. |
| `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md` | Current User Drawer commercial-ready baseline. |
| `admin/v7-admin-api` | Current admin-v2 user, channel, overview alert, and operator surfaces. |

External commercial references reviewed:

| Product | Source |
|---|---|
| Stripe | `https://docs.stripe.com/radar/reviews`, `https://docs.stripe.com/disputes` |
| Cloudflare | `https://developers.cloudflare.com/cloudflare-one/insights/` |
| Tailscale | `https://tailscale.com/docs/reference/tailscale-cli`, `https://tailscale.com/docs/reference/troubleshooting` |
| Linear | `https://linear.app/docs/triage` |
| Datadog | `https://docs.datadoghq.com/monitors/`, `https://docs.datadoghq.com/incident_response/incident_management/` |
| GitHub Enterprise | `https://docs.github.com/en/enterprise-cloud@latest/code-security/concepts/security-at-scale/about-security-overview` |

## 1. Operator Work Analysis

Current UX.5B is commercially understandable, but it is still mostly object-entry:

```text
Operator -> User -> Status -> Problem -> Reason -> Action
Operator -> Channel -> Health -> Problem -> Reason -> Action
```

Actual operator work is more mixed. Some tasks start with a known person, some start with a known channel, and many start with a symptom.

| Operator Goal | Starts From User? | Starts From Channel? | Starts From Problem? |
|---|---|---|---|
| No profile | Yes, when operator knows the customer | No | Yes, from "profile missing" queue |
| No connection | Yes | No | Yes, from "never connected" / complaint |
| Speed complaint | Yes, if complaint names user | Sometimes, if many users on same channel | Yes |
| Route issue | Yes, if one user mismatches | Yes, if channel/runtime is cause | Yes |
| Leak risk | Sometimes | Sometimes | Yes |
| Bad channel | No | Yes | Yes |
| User complaint | Yes | Maybe | Yes |
| Channel overload | No | Yes | Yes |
| Service failure | No | Yes | Yes |
| Phone confirmation | Yes | No | Yes, from attention list |
| Profile reissue | Yes | No | Yes, if caused by access failure |
| Recommendation review | Yes | Yes | Yes, if framed as "move needed" |
| Execution readiness | No | No | Yes |
| Evidence/history review | Sometimes | Sometimes | Yes, after incident |
| Healthy inspection | Yes | Yes | No |

Operator intent clusters:

| Cluster | What operator is really trying to solve | Best starting point |
|---|---|---|
| Known customer support | "This user says internet does not work." | User, then problem |
| System health | "What needs attention now?" | Problem |
| Channel operations | "Can this channel carry users safely?" | Channel, then problem |
| Routing safety | "Is traffic going through the right path?" | Problem |
| Governance/execution | "Can V7 safely act?" | Problem / action readiness |
| Healthy audit | "Show me the state of this object." | Object |

## 2. Object vs Problem Audit

Current admin-v2 already contains three entry styles:

| Surface | Current Model | Evidence in admin-v2 |
|---|---|---|
| Users tab | Object-first | `renderUsers`, user table, `openUserDrawer`, `renderUserDrawerAnswer`. |
| Channels tab | Object-first | `renderChannels`, channel table, `openChannelDrawer`, `channelDrawerBody`. |
| Overview alerts | Problem-first | `buildAlerts`, `openOverviewAlertsCenter`, `alertActionPlan`. |
| Operator center | Problem/action-first | decision surface, approval preview, delayed movement, execution dashboard. |
| Checks | Problem/action-first | targeted diagnostic action cards. |
| Logs/evidence | Investigation-first | events and evidence after problem selection. |

Workflow comparison:

| Workflow | Current Model | Problem-First Better? |
|---|---|---|
| Healthy user check | Object -> status -> observe | No. Object-first is calmer. |
| Healthy channel check | Object -> health -> observe | No. Object-first is correct. |
| No profile | User -> profile missing -> issue profile | Yes, if operator did not start from a named user. |
| No connection | User -> connection state -> resend/check | Yes, if surfaced as "users waiting". |
| Speed complaint | User/channel -> speed data -> request check | Yes. Complaint is the starting object. |
| Route issue | User/channel -> route mismatch -> check route | Yes. Risk should lead. |
| Leak risk | Object -> evidence -> warning | Strong yes. This is a safety problem. |
| Bad channel | Channel -> health -> service matrix | Yes, if many users affected. |
| Channel overload | Channel -> users/load -> action | Yes. Capacity is the operator task. |
| Service failure | Channel -> service rows -> action | Yes. Service failure is the first question. |
| Phone confirmation | User -> phone warning -> approve/reject | Yes, when multiple users wait. |
| Recommendation review | User/channel -> recommendation -> approve/ignore | Yes. "Movement candidates" is the work queue. |
| Execution readiness | Operator center -> gates -> disabled actions | Already problem/action-first. |
| Audit history | Object/event -> history | No. Investigation can stay object/event-first. |

Discovery result: V7 already has the seeds of problem-first in Overview alerts and Operator center. The missing product model is not a new drawer; it is a clearer top-level operator mental model.

## 3. Commercial Product Audit

Commercial systems do not use one model everywhere.

| Product | Operator Starts From | Evidence / Philosophy | V7 Lesson |
|---|---|---|---|
| Stripe Radar | Problem queue first, object detail second | Radar review queue is a prioritized list of payments needing investigation; details and risk insights support the decision. | Suspicious V7 states should appear as a queue: problem, action, affected user/channel. |
| Stripe Disputes | Problem first | Dashboard guides response by dispute reason and evidence. | V7 should guide by problem type when action is required. |
| Cloudflare One | Hybrid | Insights include dashboards, device monitoring, diagnostics, notifications, logs, users, devices, and network objects. | Healthy network admin is object/visibility; incidents are problem-first. |
| Tailscale | Object-first for admin, problem-first for troubleshooting | Device/user/access management is object-first; troubleshooting and bug reports start from connectivity issue. | V7 healthy state should remain user/channel-first; complaints should start from symptom. |
| Linear | Problem/inbox first | Triage is a team inbox for incoming issues; actions are accept, duplicate, decline, snooze. | V7 needs an "attention inbox" behavior for active issues, not another object table. |
| Datadog | Problem/incident first for operations | Monitors alert on issues; incidents can be declared from alerts, signals, events, and cases. | Operational mode should start from alerts and time-to-resolution. |
| GitHub Enterprise | Problem/risk first for security; repo object second | Security overview provides focused views for detection, remediation, prevention, risk, coverage, and alert remediation. | V7 should aggregate risk/problem views across users/channels, with object drilldown. |

Conclusion: mature commercial products are hybrid. They preserve object inventories, but daily operator attention starts from queues, alerts, incidents, reviews, risks, or triage when there is active work.

## 4. V7 Reality Audit

Approximate distribution of daily V7 operator work by starting intent:

| Category | Approx % | Reason |
|---|---:|---|
| User-focused | 35% | Support often begins with a known user: issue profile, no connection, phone confirmation, speed complaint. |
| Channel-focused | 20% | Channel health, service matrix, overload, disabled/reserve/canary channel checks. |
| Problem-focused | 45% | Attention queue, leak risk, route mismatch, service failure, recommendations, execution readiness, stale checks. |

This is not a vote to delete objects. It means active work is more problem-shaped than the current drawer entry model implies.

Problem-first candidates in V7:

| Problem | Object(s) Behind It | Why Problem-First Helps |
|---|---|---|
| Profile not issued | User | The action is obvious before full user detail. |
| User never connected | User/profile/client | Operator needs the next step, not metadata. |
| Speed complaint | User + current channel | Symptom may be user-specific or channel-wide. |
| Route mismatch | User + route class + channel | Safety risk should lead. |
| Leak risk | User/route/runtime | Highest urgency; object is secondary. |
| Service failure | Channel + service matrix | Operator starts from broken service. |
| Channel overload | Channel + affected users | Needs impact view before channel internals. |
| Movement recommendation | User + current/recommended channel | Work item is approval/ignore, not browsing users. |
| Execution gate failure | Gate/evidence/contracts | Already action-readiness oriented. |

## 5. Option A Analysis

Option A: Object First

```text
User
Channel
Route
then problem
```

Strengths:

| Strength | Evidence |
|---|---|
| Good for known customer support | Operator can open a named user and act. |
| Good for healthy state | No false urgency when nothing is wrong. |
| Good for admin inventory | Users/channels/routes remain stable mental anchors. |
| Already implemented well | UX.5B User Drawer is `COMMERCIAL_READY`; UX.4 Channel Drawer spec follows same philosophy. |

Weaknesses:

| Weakness | Impact |
|---|---|
| Active incidents are hidden behind object selection | Operator must know where to look. |
| Cross-object problems are fragmented | Speed/route/service issues can involve both user and channel. |
| Attention queue feels secondary | Overview alerts already compensate for this. |
| Operator may inspect healthy objects before urgent problems | Cognitive load increases under pressure. |

Verdict for Option A: keep as foundation, but not enough for commercial daily operations.

## 6. Option B Analysis

Option B: Problem First

```text
Problems
Actions
Objects
```

Strengths:

| Strength | Evidence |
|---|---|
| Fastest path to urgent work | Mirrors Linear triage, Stripe review queues, Datadog incidents, GitHub alert remediation. |
| Best for non-technical operator | "What is wrong? What do I press?" comes first. |
| Best for safety issues | Leak risk, route mismatch, execution gates should not wait behind object browsing. |
| Better for cross-object diagnosis | User complaint can reveal a bad channel; bad channel can affect users. |

Risks:

| Risk | Impact |
|---|---|
| May create false alarm culture | Healthy days become noisy if every object is rephrased as a problem. |
| Can obscure ownership | Operator still needs to know which user/channel is affected. |
| Could duplicate existing drawers | Violates project rule if implemented as new workflow/page/drawer. |
| Requires careful severity model | Without severity, problem-first becomes another table. |

Verdict for Option B: useful for active work, too aggressive as the whole product model.

## 7. Option C Analysis

Option C: Hybrid

```text
Healthy state:
Object -> Status -> Details

Problem state:
Problem -> Action -> Object -> Details
```

This is the recommended model.

| Condition | Entry Model | Why |
|---|---|---|
| Everything healthy | Object-first | Calm overview, low stress, no fake urgency. |
| Known user complaint | User-first with problem-first drawer summary | Operator already has the user identity. |
| Unknown issue / daily queue | Problem-first | Operator needs what to solve now. |
| Safety risk | Problem-first | Risk should interrupt object browsing. |
| Channel-wide failure | Problem-first | Impact and action matter before channel internals. |
| Configuration/admin work | Object-first | Intent is to manage a specific object. |
| Execution governance | Problem/action-first | Readiness and gates are the work item. |

Hybrid rule:

```text
If V7 has no active problem:
  show objects calmly.

If V7 has active problems:
  show problems first, with one action and affected objects as drilldown.
```

This does not require new truth source. It can reuse existing overview alerts, operator decision surface, user drawer answer model, channel drawer answer model, why cards, evidence, and existing actions.

## 8. Example Workflows

### Healthy User

Current UX model:

```text
USER
Ivan Petrov

STATE
Works

PROBLEM
No action required

REASON
Current route is best

ACTION
[Observe] [Details]
```

Problem-first model:

```text
PROBLEMS
No active user problems

ACTION
[Open Users]

OBJECTS
Healthy users: 24
```

Discovery: current object-first is better. A healthy user should not be converted into a fake work item.

### No Profile

Current UX model:

```text
USER
Maria Smirnova

STATE
Needs Action

PROBLEM
Profile missing

REASON
Profile not issued

ACTION
[Issue Profile] [Details]
```

Problem-first model:

```text
PROBLEM
Profile not issued

ACTION
[Issue Profile]

AFFECTED
Maria Smirnova
North Trade
10.0.0.34

WHY
User cannot connect until profile is issued

DETAILS
[Open User]
```

Discovery: problem-first is better when this appears in a daily attention queue. Object drawer remains correct after click.

### Speed Complaint

Current UX model:

```text
USER
Ivan Petrov

STATE
Needs Check

PROBLEM
Speed complaint

REASON
Fresh speed check required

ACTION
[Request Speed] [Details]
```

Problem-first model:

```text
PROBLEM
Speed needs check

ACTION
[Request Speed Check]

AFFECTED
Ivan Petrov
Current channel: awg3

WHY
Latest speed data is stale or missing

DETAILS
[Open User] [Open Channel]
```

Discovery: problem-first is better because speed may be user-side or channel-side.

### Route Issue

Current UX model:

```text
USER
Ivan Petrov

STATE
Needs Action

PROBLEM
Route mismatch

REASON
Route verification required

ACTION
[Check Route] [Details]
```

Problem-first model:

```text
PROBLEM
Route requires verification

ACTION
[Check Route]

AFFECTED
Ivan Petrov
Route class: global traffic
Current channel: awg3

WARNING
Traffic may be using the wrong path

DETAILS
[Open User] [Open Route Evidence]
```

Discovery: problem-first is better. Safety risk should lead the operator model.

## 9. Cognitive Load Comparison

| Model | Clicks | Time To Understand | Operator Stress |
|---|---:|---|---|
| Object-first | 1-3 when object is known; 3-6 when problem is unknown | Fast for known user/channel; slower for system-wide issues | Low in healthy state, medium during incidents |
| Problem-first | 1-2 for active problems; 3+ for healthy browsing | Fast for incidents; awkward when nothing is wrong | Low during incidents, medium on healthy days if overused |
| Hybrid | 1-2 for active problems; 1-2 for known objects | Fast in both healthy and problem states | Lowest overall if severity is disciplined |

Specific V7 cognitive load:

| Question | Object-first | Problem-first | Hybrid |
|---|---|---|---|
| What needs attention now? | Medium | High | High |
| Is this user OK? | High | Medium | High |
| Can users stay on this channel? | High | Medium | High |
| What should I press? | High after UX.5B | High | High |
| Why is this happening? | High after why cards | High | High |
| Where is evidence/history? | High in details | Medium | High with drilldown |
| Will healthy state stay calm? | High | Low | High |

## 10. Recommended Future Model

Recommendation: `HYBRID_RECOMMENDED`.

V7 should not move to pure problem-first. V7 should make problem-first the operator's active-work mode while preserving User/Channel/Route object drawers as the stable detail model.

Future operator principle:

```text
Attention first when there is attention.
Objects first when there is no active problem.
Details only after the operator asks.
```

Recommended information model:

| Layer | Purpose | Reuses |
|---|---|---|
| Attention / Problems | Shows active work: problem, action, affected object, why | Existing overview alerts, operator decision surface, user/channel answer model |
| User/Channel drawers | Work one selected object | Existing `renderUserDrawerQuick`, `renderUserDrawerLive`, `openChannelDrawer`, channel drawer |
| Details | Investigation | Existing Details, Why Cards, Profile, Route, Speed, Service Matrix |
| Evidence/Execution | Technical proof and governance | Existing evidence, execution, operator center |

Do not create new truth source. If implemented later, derive problem cards from existing:

| Existing Source | Possible Problem Card |
|---|---|
| `buildAlerts` | Active overview attention |
| `operator_decision_surface_response` | Recommendation / movement candidates |
| User drawer answer model | Profile missing, no connection, speed check, route issue |
| Channel drawer answer model | Bad channel, service failure, no measurements, capacity |
| Why cards | One-line reason |
| Existing actions | One primary action |

Implementation should not start from UX.6. Next step should be UX.7: specification for a hybrid attention model, still no implementation.

## 11. Verdict

`HYBRID_RECOMMENDED`

Rationale:

| Decision Factor | Verdict |
|---|---|
| Current UX.5B quality | Keep. It is commercially ready for selected user objects. |
| Channel drawer philosophy | Keep. It should match User Drawer. |
| Daily operator work | More problem-shaped than object-shaped when action is required. |
| Commercial benchmark | Hybrid: queues/incidents/alerts for active work; objects for inventory/detail. |
| Cognitive load | Hybrid is lowest. |
| Risk of pure problem-first | Too high; it would create noise and hide stable object management. |
| Strategic recommendation | Add problem-first active-work model only as a derived layer over existing objects. |

Final alignment state before report creation:

| Check | Status |
|---|---|
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS |
| Truth | PASS / FULLY_ALIGNED |
| Convergence | PASS / ALIGNED |

