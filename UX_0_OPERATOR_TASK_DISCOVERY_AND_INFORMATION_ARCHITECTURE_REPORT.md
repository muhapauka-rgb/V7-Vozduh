# UX.0 Operator Task Discovery And Information Architecture Report

Date: 2026-06-14

Mode: discovery only. No UI implementation. No page creation. No component removal. No runtime changes. No apply. No user movement beyond approved deploy alignment already completed before this audit.

Truth gate after alignment:

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |

Audited surfaces:

| Area | Current source |
| --- | --- |
| Users | `admin/v7-admin-api` Users tab, user table, user drawer, identity workspaces |
| User Drawer | `renderUserDrawerQuick`, `renderUserDrawerLive`, recommendation drawer |
| Channels | Channels tab, channel table, matrix/readiness/onboarding workspaces |
| Channel Drawer | `channelDrawerBody`, `renderChannelDrawerLive`, channel state drawer |
| Routes | Routing tab, route drawer, route readiness/reality views |
| Recommendations | Operator decision surface, user recommended channel cell, batch preview |
| Evidence | Evidence/proposal object panels, hardening search drawer, operator evidence |
| Execution | Operator tab, execution dashboard, approval preview, governed workflow |
| Diagnostics | Checks tab, routing checks, channel/user checks, service matrix, speed tests |
| Settings | Settings tab, policy, impact, autoswitch, modes, guardrails |
| Operator | Operator center, approval, execution history, targets, delayed movement |

## 1. Operator Tasks

| Task | Frequency | Value | Current Screens Used |
| --- | --- | --- | --- |
| Issue profile / add user | Daily | High | Users > Выдать профиль, Identity, User Drawer |
| Investigate user issue | Daily | High | Users table, User Drawer, Checks, Logs |
| Confirm phone / identity | Daily | High | Users table, User Drawer, Identity people/access |
| Check user route | Daily | High | User Drawer, Routing, Checks |
| Check user speed | Daily | Medium | User Drawer, client speed request, Checks |
| Understand why user is on channel | Daily | High | User Drawer, Recommendation Drawer, Operator decision surface |
| Review recommendation | Daily/Weekly | High | Users table recommended channel, Recommendation Drawer, Operator |
| Prepare movement approval | Weekly | High | Recommendation Drawer, Operator approval, Execution |
| Verify no user movement is currently allowed | Daily | High | Operator center, batch preview, execution dashboard |
| Check channel status | Daily | High | Channels table, Channel Drawer |
| Check channel service matrix | Daily/Weekly | High | Channels matrix, Channel Drawer, Checks |
| Check channel speed | Daily/Weekly | Medium | Channels table, Channel Drawer |
| Understand channel selection | Daily | High | Channel Drawer, User recommendation, Operator targets |
| Add channel | Weekly/Rare | High | Channels onboarding wizard |
| Pause/start/delete channel | Rare | High/Risky | Channel Drawer, Channels actions |
| Verify internet works | Daily | High | Checks, Channels, User Drawer |
| Verify no leak | Weekly/Incident | High | Routing, Checks, Security |
| Check route class / RU direct | Weekly/Incident | High | Routing overview, route drawer, route reality |
| Review execution readiness | Weekly | High | Operator, Execution drawers |
| Review evidence/proposals | Weekly/Incident | Medium | Object panels, hardening search, Operator evidence |
| Audit history/logs | Incident | High | Logs, Operator history, Evidence |
| Change policy/settings | Rare | High/Risky | Settings policy/impact/autoswitch/guardrails |
| Backup/rollback/maintenance | Rare/Incident | High/Risky | Security |

Primary daily operator jobs are not "manage every setting"; they are:

1. Find the affected user/channel.
2. See current status and problem.
3. Understand why V7 chose the current/recommended state.
4. Take one safe next action.
5. Escalate to route/evidence/execution only when the first screen is not enough.

## 2. Information Hierarchy

| Information | Level |
| --- | --- |
| Object identity: user name, phone/company/device, IP | Level 1 |
| User current status: OK, waiting, disabled, blocked, phone pending | Level 1 |
| Current channel / assigned route | Level 1 |
| Internet works / connected / route OK / leak risk | Level 1 |
| Required next action | Level 1 |
| Channel status: enabled, health, users, service readiness | Level 1 |
| Recommendation state: keep/move/hidden/review | Level 1 |
| Why summary from completed explainability cards | Level 2 |
| Route short explanation | Level 2 |
| Profile/onboarding state | Level 2 |
| Device identity state | Level 2 |
| Channel service score / matrix summary | Level 2 |
| Capacity/headroom/load summary | Level 2 |
| Client/server speed detail | Level 3 |
| Traffic by day/week/month/total | Level 3 |
| Profile artifacts and delivery history | Level 3 |
| Recent commands/events | Level 3 |
| Assigned users list inside channel | Level 3 |
| Service-by-service matrix rows | Level 3 |
| Evidence bundles | Level 4 |
| Proposal records | Level 4 |
| Execution contracts and validation previews | Level 4 |
| Approval packet, restore barrier, rollback packet | Level 4 |
| Raw snapshot reasons | Level 5 |
| Internal contract fields and schema names | Level 5 |
| Runtime fingerprints, release linkage, deploy manifests | Level 5 |
| Redacted configs and technical command output | Level 5 |

## 3. Noise Audit

| Item | Duplicate | Canonical Place |
| --- | --- | --- |
| Current channel appears in user table, quick drawer, live drawer, recommendation drawer | Yes | User Screen 1 summary |
| User status appears as status pill, issue text, readiness text, next action | Yes | One "Problem / Status / Next action" block |
| Route OK appears in table, user checklist, factual route section, route drawer | Yes | User Screen 1 short; full in Route one-click |
| Speed appears in user action card and speed section | Yes | One-click Speed section |
| Traffic appears in quick drawer and detailed drawer | Yes | One-click Usage section |
| Profile/onboarding appears in quick actions, path, VLESS, profiles/delivery | Yes | One Profile section behind click |
| Device identity appears in metadata, identification, device table | Yes | User Screen 1 device line; details behind click |
| Evidence/proposals/execution appear in many drawers as separate panels | Yes | Technical Details tab/panel |
| Channel health appears in channel table, snapshot, kv rows, checklist | Yes | Channel Screen 1 status line |
| Channel service matrix appears in table, snapshot, checklist, service section | Yes | Screen 1 summary; rows behind click |
| Channel speed appears in table, snapshot, speed section | Yes | Screen 1 if stale/bad; otherwise one-click |
| Channel users count and assigned users table both visible in drawer | Yes | Count first; list one-click |
| Route class purpose appears in overview, route snapshot, rule section | Yes | Route Screen 1 purpose sentence |
| Execution disabled text repeated across Operator, recommendation, approval | Yes | Single "Apply status" line with drilldown |
| Raw snapshot reasons duplicate why card | Yes | Technical Details only |
| Policy explanations inside Settings appear next to controls | Partial | Keep in Settings, not user/channel cards |

## 4. One Screen Rule Audit

Goal: User Drawer Screen 1 must fit without scrolling. Current quick drawer likely does not, and live drawer definitely does not.

| Section | Keep | Move | Hide |
| --- | --- | --- | --- |
| Phone confirmation | Keep only if pending; otherwise hide | Screen 1 conditional | Hidden when not needed |
| Why Card | Keep as compact "Why?" row or expandable inline | Screen 1 Level 2 | No separate explainability block |
| Основное metadata form | Keep only name/company/device/IP/current channel/status | Full edit form behind click | Notes/raw metadata hidden |
| Traffic | Move | One click | Not hidden |
| Что сделать | Keep | Screen 1 | Never hide |
| Object panels: proposals/evidence/execution | Move | Technical details | Hidden by default |
| Operator snapshot | Keep only status/next action | Details to Screen 2 | Raw fields hidden |
| Inspection checklist | Move | Screen 2 | Not hidden |
| Device identity | Move | Screen 2 | Not hidden |
| Onboarding path | Move | Screen 2 | Not hidden |
| VLESS profile | Move | Screen 2 | Not hidden |
| User actions | Keep only primary next action and one secondary | More actions in Screen 2 | Dangerous actions hidden behind confirmation |
| Factual route | Move | One click Route | Not hidden |
| Client speed | Move | One click Speed | Not hidden |
| Profiles and delivery | Move | Screen 2 Profile | Not hidden |
| Warnings | Keep only count/severity if non-empty | Screen 2 | Hide if empty |
| Switch history | Move | Technical details | Not hidden |
| Recent commands | Move | Technical details | Not hidden |
| Recent events | Move | Technical details | Not hidden |

Channel Drawer one-screen audit:

| Section | Keep | Move | Hide |
| --- | --- | --- | --- |
| Channel status summary | Keep | Screen 1 | Never hide |
| Why Card | Keep as inline "Why?" near status | Screen 1 Level 2 | No standalone section |
| Traffic | Move | One click | Not hidden |
| Action controls | Keep one primary next action | Screen 1 | Extra actions behind click |
| Object panels | Move | Technical details | Hidden by default |
| Channel snapshot cards | Keep compressed | Screen 1 | Duplicate detail hidden |
| Checklist | Move | Screen 2 | Not hidden |
| Lifecycle | Move | Screen 2 | Not hidden |
| Speed comparison | Move | Screen 2 | Not hidden |
| Assigned users | Move | Screen 2 | Not hidden |
| Client speed rows | Move | Screen 3 | Hidden until needed |
| Service matrix rows | Move | Screen 2 | Not hidden |
| Config | Move | Technical details | Hidden by default |
| Events | Move | Technical details | Hidden by default |

## 5. Progressive Disclosure Plan

| Information | Immediate | One Click | Technical Only |
| --- | --- | --- | --- |
| User identity/name/company/device/IP | Yes | Edit full metadata | No |
| Current problem/status | Yes | Checklist | No |
| Current channel and recommended channel | Yes | Recommendation details | No |
| Required action | Yes | Full action list | No |
| Why summary | Yes, inline | Why details | Raw reasons technical |
| Route OK/leak risk | Yes as status | Route detail | Raw route output |
| Connected/profile state | Yes as status | Profile detail | Profile artifact internals |
| Speed | Only if missing/bad | Speed detail/request | Raw command output |
| Traffic | No | Usage summary | Raw counters |
| Device identity | Device label only | Device detail | Identity events |
| Evidence/proposals/execution | No | Short object panels | Full records |
| Channel health/users/capacity | Yes | Channel checklist | Raw state |
| Service matrix | Summary only | Service rows | Raw HTTP samples |
| Runtime fingerprint/deploy | No | Operator trust drawer | Engineering only |
| Policy/settings | No on user/channel | Settings impact | Raw config |

Progressive disclosure target:

1. Screen 1 answers "what is wrong and what do I do?"
2. Screen 2 answers "why and what evidence supports it?"
3. Screen 3 answers "what did the system read/write historically?"

## 6. User Drawer Future Structure

SCREEN 1: Operator Summary

| Section | Contents |
| --- | --- |
| Header | Name, company, phone, device, IP |
| Problem | OK / waiting / blocked / disabled / phone pending |
| Current state | Current channel, connected yes/no, route OK/leak risk |
| Why? | One compact explainability row: keep/move reason, confidence, top metric |
| Required action | One primary action, one secondary action |
| Conditional warning | Phone confirmation, rejected phone, blocked profile, leak risk |

SCREEN 2: Work The Case

| Section | Contents |
| --- | --- |
| Checklist | Route, profile, connection, speed, device, logs |
| Profile | Onboarding path, VLESS/profile status, latest delivery |
| Route | Factual route, expected path, leak state |
| Speed | Client V7/direct, degradation, request speed |
| Device | Linked identity device, client type, quality |
| Actions | Reissue, check, delivery link, pause/enable |

SCREEN 3: Technical Details

| Section | Contents |
| --- | --- |
| Evidence | Evidence bundles by object |
| Proposals | Related proposals |
| Execution | Contracts, validation preview, approval packet |
| History | Switch history, commands, events |
| Raw reasons | Snapshot reason list |
| Artifacts | Profile files, redacted config metadata |

Remove from Screen 1 completely:

| Remove from first screen | New location |
| --- | --- |
| Traffic block | Screen 2 Usage |
| Object panels | Screen 3 Technical Details |
| Full metadata edit form | Edit action / Screen 2 |
| Profile artifact table | Screen 3 |
| Recent commands/events | Screen 3 |
| Raw snapshot reasons | Screen 3 |

## 7. Channel Drawer Future Structure

SCREEN 1: Channel Summary

| Section | Contents |
| --- | --- |
| Header | Human label, channel id, protocol/role |
| Status | Ready / working but incomplete / disabled / bad |
| Capacity | Users, soft/hard, headroom |
| Service health | Matrix summary, service score |
| Why? | Compact channel why row: state reason, source, top metric |
| Required action | One primary action: check services, speed, start, pause, open logs |

SCREEN 2: Operate Channel

| Section | Contents |
| --- | --- |
| Checklist | Health, service matrix, speed, users, runtime profile, logs |
| Services | Service-by-service matrix with actions |
| Speed | Server/client speed and degradation |
| Users | Assigned users list |
| Lifecycle | Draft/provision/enable history |
| Actions | Run speed, run matrix, pause/start, rename |

SCREEN 3: Technical Details

| Section | Contents |
| --- | --- |
| Evidence | Evidence bundles |
| Proposals | Proposal records |
| Execution | Contracts and validation |
| Config metadata | Path, size, redacted status |
| Events | Channel events |
| Raw state | Registry/runtime fields |

Remove from Screen 1 completely:

| Remove from first screen | New location |
| --- | --- |
| Full service rows | Screen 2 Services |
| Full assigned user table | Screen 2 Users |
| Config metadata | Screen 3 |
| Events | Screen 3 |
| Evidence/proposal/execution panels | Screen 3 |
| Raw trust/recovery fields | Screen 3 |

## 8. Explainability Placement Plan

Principle: no separate explainability page and no separate explainability section. Explainability appears exactly where the operator asks "why?"

| Explainability card | Placement | Behavior |
| --- | --- | --- |
| User Why Card | User Screen 1, next to status/current channel | One-line summary; click expands metrics |
| User Why Card | Recommendation drawer, below decision | Full compact details for keep/move/review |
| Channel Why Card | Channel Screen 1, next to channel status | One-line reason and top metric |
| Channel Why Card | Channel state drawer | Full compact details |
| Planner Why Card | Operator execution/planner block | Explains no-move or candidate count |
| Raw reasons | Technical Details only | Not visible on first screen |

Target wording:

| Operator question | Where answer appears |
| --- | --- |
| "Why is this user here?" | User summary current/recommended row |
| "Why move or not move this user?" | Recommendation drawer |
| "Why is this channel good/bad?" | Channel summary status row |
| "Why no movement now?" | Operator planner summary |
| "What raw evidence supports this?" | Technical Details |

## 9. Top 20 Simplifications

| Rank | Simplification | Value | Risk | Complexity |
| --- | --- | --- | --- | --- |
| 1 | Collapse User Screen 1 into identity/status/channel/why/action only | High | Medium | Medium |
| 2 | Move traffic out of User Screen 1 | High | Low | Low |
| 3 | Move object panels to Technical Details | High | Low | Low |
| 4 | Replace full metadata form on first screen with read summary + Edit | High | Medium | Medium |
| 5 | Merge status/readiness/issue into one Problem block | High | Medium | Medium |
| 6 | Make one primary next action per user | High | Medium | Medium |
| 7 | Keep phone confirmation only when pending | High | Low | Low |
| 8 | Move raw snapshot reasons under Technical Details | High | Low | Low |
| 9 | Compress User live drawer checklist into Screen 2 | Medium | Low | Medium |
| 10 | Collapse Channel Screen 1 into status/capacity/service/why/action | High | Medium | Medium |
| 11 | Move channel traffic to Screen 2 | Medium | Low | Low |
| 12 | Move channel object panels to Technical Details | High | Low | Low |
| 13 | Keep assigned users count first; list behind click | High | Low | Low |
| 14 | Keep service matrix summary first; rows behind click | High | Low | Low |
| 15 | Convert route drawer into status/path/fact/action first | Medium | Medium | Medium |
| 16 | Stop repeating "apply disabled" in every block; show one Apply status | Medium | Medium | Medium |
| 17 | Merge Evidence/Proposal/Execution tabs inside object technical details | Medium | Low | Medium |
| 18 | Keep Settings out of daily operator flow | Medium | Low | Low |
| 19 | Turn Logs into incident/history destination, not daily status source | Medium | Low | Low |
| 20 | Use completed Why Cards as inline answers, not new cards | High | Medium | Medium |

## 10. Final Recommended Architecture

Recommended admin-v2 information architecture:

| Layer | Purpose | Screens |
| --- | --- | --- |
| Daily Operations | Solve user/channel issues fast | Users, Channels, Checks |
| Decision Review | Understand recommendations and movement readiness | User Recommendation, Operator |
| Network Reality | Verify routes, internet, leaks | Routing, Checks |
| Evidence And History | Prove what happened | Logs, Evidence, Operator history |
| Controlled Change | Risky operations and policy | Security, Settings |
| Engineering Detail | Contracts, raw evidence, runtime truth | Technical Details drawers |

Recommended first-screen pattern for all object drawers:

| Slot | Meaning |
| --- | --- |
| Identity | What object am I looking at? |
| Status | Is it OK, blocked, waiting, or risky? |
| Current state | Where is it routed / assigned / running now? |
| Why | One explainability answer in context |
| Next action | One safe operator action |
| Drilldown buttons | Route, speed, evidence, logs, technical |

Commercial product benchmark:

| Principle | Current State | Gap |
| --- | --- | --- |
| Linear: task-first issue view | Some problem drawers exist, but object drawers still show many sections | Need one problem/action summary first |
| Stripe: concise object summary with tabs behind | Tables are useful; drawers mix summary and deep detail | Move details behind structured disclosure |
| Cloudflare: operational status before raw config | Channel status exists, but raw/lifecycle/config details compete | Make status/capacity/service the first screen |
| Tailscale: device/user/network clarity | User/device/profile data exists but scattered | Merge identity/device/profile into one coherent case flow |
| GitHub Enterprise: audit/evidence available but not primary | Logs/evidence are accessible from many places | Keep as drilldown, not first-screen content |
| Datadog: incident summary before telemetry | Checks and metrics exist | Show only bad/stale metric first, details on demand |
| Minimal cognitive load | Many buttons and repeated sections | One primary next action per context |
| Single next action | Partially present in readiness/next_action fields | Needs UI hierarchy enforcement |
| Progressive disclosure | Existing object panels are lazy-loaded | Needs stricter placement and naming |

Screens to preserve:

| Screen | Preserve because |
| --- | --- |
| Users | Primary operator workspace |
| Channels | Primary infrastructure workspace |
| Routing | Network/reality workspace |
| Operator | Decision/execution governance workspace |
| Checks | Safe diagnostics workspace |
| Security | Risky/admin safeguards |
| Settings | Rare policy work |
| Logs | Investigation/history |

Screens not to create:

| New screen idea | Decision |
| --- | --- |
| Separate Explainability page | Do not create |
| Separate Evidence dashboard for daily use | Do not create |
| New recommendation page | Do not create |
| Beautiful mock dashboard detached from admin-v2 | Do not create |

## 11. Final Verdict

READY_FOR_UX_REBUILD

Reason: current admin-v2 already exposes the necessary tasks, contracts, drawers, and read-only explainability payloads. The next phase can safely rebuild information hierarchy inside existing screens without new pages, without removing workflows blindly, and without changing runtime behavior.
