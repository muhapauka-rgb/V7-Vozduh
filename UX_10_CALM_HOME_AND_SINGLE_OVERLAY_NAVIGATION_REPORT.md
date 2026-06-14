# UX.10 Calm Home And Single Overlay Navigation Report

## 1. Current Problems

Truth gate passed after UX.9 deployment:

| Check | Status |
|---|---|
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS |

Current overview is safer than UX.8 and calmer than pre-UX.9, but it is still not fully operator-story-first.

| Problem | Evidence | Impact |
|---|---|---|
| Home still starts from system objects | Metrics show `Состояние V7`, `Пользователи`, `Каналы`, `Маршруты`, `Защита трафика`, `Требует внимания` | Operator reads structure before problem |
| Trust/runtime/release are on Home | Home contains `Доверие`, `Runtime`, `Release`, `Execution` | Non-technical operator sees engineering governance too early |
| Topology still resembles architecture | Flow is Users -> V7 server -> channel groups -> Services | Better than channel chips, but still reads as a network diagram |
| Attention opens a drawer, then actions may jump tabs | Actions still use patterns like `showTab(...); closeDrawer()` | Operator can lose context |
| Drawer is single DOM overlay but not single journey | `openDrawer()` can push snapshots; object actions open new content or navigate away | Feels like popup/navigation stacking even when only one DOM drawer exists |

Current Home block audit:

| Block | Keep | Move | Remove |
|---|---|---|---|
| System state metric | Keep, rewrite as story headline | No | No |
| Users metric | Keep, rewrite as operator summary | No | No |
| Channels metric | Keep, rewrite as health summary | No | No |
| Routes metric | Keep only if problem-oriented | Move details to Route/Operator | No |
| Traffic protection metric | Keep when attention exists | Move technical proof to Operator/Security | No |
| Attention counters | Keep | No | No |
| Topology | Keep, convert to operational groups | No | No |
| Trust block | No | Operator | No |
| Runtime | No | Operator technical | No |
| Release | No | Operator technical | No |
| Execution | No | Operator technical | No |
| Active users table | Keep as small preview only | Full table in Users | No |
| Channels table | Keep as small preview only | Full table in Channels | No |

## 2. Single Overlay Architecture

Use the existing `#drawer` as the only overlay. Do not create a second modal, new drawer, new page, or new workflow.

Target architecture:

```text
Main Page
  -> open single overlay
    -> Level 1: Problem
    -> Level 2: Object
    -> Level 3: Technical
```

Single overlay rules:

| Rule | Decision |
|---|---|
| One overlay DOM | Reuse existing `#drawer` |
| One navigation context | Drawer content swaps, overlay remains open |
| No modal over modal | Any object/detail action renders into current drawer |
| No popup stacking | Disable implicit snapshot stack for attention journey |
| No tab jump from primary flow | Replace `showTab(...); closeDrawer()` in attention actions with drawer-level transitions |
| Existing object renderers reused | User, Channel, Route, Recommendation, Operator detail bodies remain canonical |

Proposed controller model:

| Concept | Meaning |
|---|---|
| `journey.items` | Current problem list, e.g. all Critical problems |
| `journey.index` | Current item position, e.g. `1 / 5` |
| `journey.level` | `problem`, `object`, or `technical` |
| `journey.objectRef` | Existing user/channel/route/check/reference |
| `journey.render()` | Swaps drawer body only |

This is not a new truth source. It is temporary UI state derived from existing attention items and existing object references.

## 3. Attention Navigation Flow

Current:

```text
Attention counter
  -> compact alert drawer
    -> Primary Action
      -> showTab(...) or open object
        -> operator may lose place
```

Target:

```text
Attention counter
  -> single overlay: Problem 1 / N
    -> Primary Action stays visible
    -> Details swaps to Object level
    -> Technical swaps to Evidence/History/Execution level
```

Multi-problem flow:

```text
--------------------------------------------------
Critical
1 / 5

Route Leak Risk
Ivan Petrov

Reason
Route verification required

[Check Route] [Details]

< Previous                 Next >
--------------------------------------------------
```

Level 1: Problem

| Row | Purpose |
|---|---|
| Severity + count | Operator knows scope |
| Problem name | What is wrong |
| Object label | Who/what is affected |
| One reason | Why it matters |
| Primary action | What to do now |
| Details | Move to Level 2 |

Level 2: Object

| Object Type | Reuse |
|---|---|
| User | `renderUserDrawerQuick`, then `renderUserDrawerLive` where needed |
| Channel | `channelDrawerBody`, `renderChannelDrawerLive` |
| Route | `routeDrawerBody` |
| Recommendation | `openUserRecommendationDrawer` content model |
| Operator/execution | Existing operator detail sections |

Level 3: Technical

| Technical Area | Reuse |
|---|---|
| Evidence | Existing evidence object buttons and drawers, rendered inside current overlay |
| History | Existing event/log summaries |
| Execution | Existing execution summary/detail sections |
| Contracts | Existing operator execution contract sections |

## 4. Home Page Story Model

Home should tell the operator story, not expose system structure.

Target first screen:

```text
--------------------------------------------------
System Requires Attention
2 issues
1 critical

Protection requires check
[Open]
--------------------------------------------------

Users
24 working
2 require attention

Channels
97 healthy
2 need check
1 problem

Services
44 healthy
3 need check
--------------------------------------------------
```

Story model:

| Story Block | Operator Question | Source |
|---|---|---|
| System state | Do I need to act? | Attention + overview summary |
| Problem summary | What is the biggest issue? | Existing attention items |
| Users | Are users okay? | Existing user status |
| Channels | Can users safely stay on channels? | Existing channel status |
| Services | Are services reachable? | Existing service matrix |

Do not show on first screen:

| Item | Destination |
|---|---|
| Runtime trust | Operator technical |
| Release trust | Operator technical |
| Execution readiness | Operator technical |
| Raw route classes | Route/Technical |
| Raw evidence/logs | Technical level |
| Full users table | Users page |
| Full channels table | Channels page |

## 5. Trust/Runtime Placement Audit

| Item | Home | Operator | Technical |
|---|---|---|---|
| Runtime Trust | No | Summary only | Full |
| Release Trust | No | Summary only | Full |
| Execution readiness | No | Summary/action | Full |
| Restore barrier | No | Summary | Full |
| Deployment/runtime mismatch | Only if critical | Yes | Full |
| Evidence freshness | Only as stale warning | Yes | Full |
| Governance contracts | No | Yes | Full |

Decision: Trust/runtime/release should leave Home. Home may show only a human warning if the operator must act.

## 6. Scalable Topology Model

Current UX.9 topology groups channels, but the visual still reads as architecture:

```text
Users -> V7 server -> Channels -> Services
```

Target operational topology:

```text
--------------------------------------------------
Users
24 working
2 need attention
--------------------------------------------------
        |
        v
--------------------------------------------------
V7
Protecting traffic
1 check required
--------------------------------------------------
        |
        v
--------------------------------------------------
Channels
Healthy 97
Check 2
Problem 1
--------------------------------------------------
        |
        v
--------------------------------------------------
Services
Healthy 44
Check 3
--------------------------------------------------
```

Channel group drilldown:

| Group | Click Result |
|---|---|
| Healthy 97 | Existing Channels workspace filtered to healthy |
| Check 2 | Existing Channels workspace filtered to check |
| Problem 1 | Existing Channels workspace filtered to problem |
| Disabled/Reserve | Existing Channels workspace filtered to disabled/reserve |

No new page. No new data owner. The filter remains derived from existing `channelTopologyState()`.

## 7. 10/30/100/300 Channel Validation

The overview must remain readable at every scale by never rendering individual channel objects on Home.

10 channels:

```text
Channels
Healthy 8
Check 1
Problem 1
```

30 channels:

```text
Channels
Healthy 25
Check 4
Problem 1
```

100 channels:

```text
Channels
Healthy 93
Check 5
Problem 2
```

300 channels:

```text
Channels
Healthy 281
Check 15
Problem 4
```

Validation matrix:

| Channel Count | Individual Channels Visible | Overview Readable | Drilldown Path |
|---:|---|---|---|
| 10 | No | YES | Group -> filtered Channels |
| 30 | No | YES | Group -> filtered Channels |
| 100 | No | YES | Group -> filtered Channels |
| 300 | No | YES | Group -> filtered Channels |

Recommended implementation: fixed story cards, not a horizontal topology diagram. A group count can grow from `10` to `300` without changing layout.

## 8. Mobile Validation

Mobile target:

```text
System Requires Attention
2 issues

[Open]

Users
24 working
2 need attention

Channels
97 healthy
2 need check
1 problem

Services
44 healthy
3 need check
```

Mobile overlay target:

```text
Critical
1 / 5

Route Leak Risk
Ivan Petrov

[Check Route]
[Details]

< Prev       Next >
```

Mobile rules:

| Area | Requirement |
|---|---|
| Overview | One column, no horizontal scroll |
| Attention | Counters become story rows |
| Overlay | Full-width modal, body swaps in place |
| Topology | Vertical operational groups |
| Actions | Primary + Details fit without clipping |
| Technical | Hidden behind one tap |

## 9. Commercial Benchmark

| Product | Philosophy | UX.10 Application |
|---|---|---|
| Stripe | Home starts from state and required action | Put problem/action before raw system objects |
| Cloudflare | Incidents and health before deep configuration | Show safe/unsafe groups, move config details deeper |
| Linear | One focused issue at a time | Problem 1 / N inside a single overlay |
| Tailscale | Device/network health without noisy internals | Human-readable channel/service health |
| Datadog | Triage starts at monitor/incident, then evidence | Attention -> problem -> object -> technical |

Conclusion: UX.10 should move V7 Home from object-first to problem-story-first, while preserving existing object drawers as deeper levels.

## 10. Recommended Implementation Plan

Phase 1: Single overlay journey

| Change | Risk | Complexity |
|---|---|---|
| Add derived drawer journey state | Low | Medium |
| Render attention item as Problem 1 / N | Low | Medium |
| Add Previous/Next inside current drawer | Low | Low |
| Convert Details to object-level body swap | Medium | Medium |

Phase 2: Stop attention context jumps

| Change | Risk | Complexity |
|---|---|---|
| Replace `showTab(...); closeDrawer()` in attention primary/detail flow | Medium | Medium |
| Reuse existing user/channel/route renderers inside current drawer | Medium | Medium |
| Keep tab navigation only as explicit escape action | Low | Low |

Phase 3: Calm Home story

| Change | Risk | Complexity |
|---|---|---|
| Rewrite top metrics into operator story blocks | Low | Medium |
| Move trust/runtime/release from Home to Operator | Medium | Medium |
| Keep Home previews tiny and problem-first | Low | Medium |

Phase 4: Operational topology

| Change | Risk | Complexity |
|---|---|---|
| Replace architecture diagram with vertical operational groups | Medium | Medium |
| Keep channel group drilldown via existing filters | Low | Low |
| Validate 10/30/100/300 count layouts | Low | Low |

Implementation guardrails:

| Rule | Required |
|---|---|
| No new page | YES |
| No new drawer | YES |
| No new endpoint | YES |
| No new truth source | YES |
| No storage | YES |
| No runtime mutation | YES |
| No user/channel mutation | YES |
| No deploy until implementation approved | YES |

## 11. Final Verdict

READY_FOR_IMPLEMENTATION

UX.10 should proceed after approval as a small UI-navigation implementation, not a new product surface. The core decision is approved: V7 Home should become problem-story-first, and Attention should become a single-overlay journey with object and technical details rendered inside the same overlay.
