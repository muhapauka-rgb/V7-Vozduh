# UX.4 CHANNEL DRAWER REBUILD SPECIFICATION REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: discovery and specification only

No implementation was performed. No UI was changed. No component was moved. No new page, drawer, workflow, truth source, planner, governance path, execution path, or deploy was created.

## Truth Gate

| Gate | Result | Notes |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED | Existing untracked handoff document is documentation-only and ignored by the gate. |
| `tools/v7-convergence-status --json` | PASS / ALIGNED | Runtime mismatch is docs-only for existing UX reports; no deployment required. |

Truth gate verdict: PASS. UX.4 may proceed as read-only Channel Drawer specification.

## Inputs Used

| Input | Status | Relevant Use |
| --- | --- | --- |
| `UX_0_OPERATOR_TASK_DISCOVERY_AND_INFORMATION_ARCHITECTURE_REPORT.md` | Used | Channel one-screen audit and progressive disclosure model. |
| `UX_1_USER_DRAWER_REBUILD_SPECIFICATION_REPORT.md` | Used | Three-screen User Drawer philosophy and one-screen answer rule. |
| `UX_2_USER_DRAWER_WIREFRAME_AND_IMPLEMENTATION_PLAN_REPORT.md` | Used | Screen 1/2/3 structure, action reduction, mobile constraints. |
| `UX_3_REAL_WORLD_OPERATOR_SCENARIOS_AND_FINAL_VISUAL_MOCKUPS_REPORT.md` | Used | 5-second/10-second operator rule and visual simplicity target. |
| `EXPLAINABILITY_2_CANONICAL_ADAPTER_AND_WHY_CARD_FOUNDATION_REPORT.md` | Used | Existing channel `why_cards` and compact/full Why Card distinction. |
| `admin/v7-admin-api` | Inspected | `channelDrawerBody`, `renderChannelDrawerLive`, `openChannelStateDrawer`, `channelObjectPanelsSection`, `channelActionControls`. |

## 1. Current Channel Drawer Inventory

Current Channel Drawer has three related surfaces:

- fallback/quick channel drawer: `channelDrawerBody`
- live/detail channel drawer: `renderChannelDrawerLive`
- channel state explanation drawer: `openChannelStateDrawer`

| Block | Daily Use | Value | Keep | Move | Hide |
| --- | --- | --- | --- | --- | --- |
| Drawer header title / inline rename | Medium | Helps identify and rename channel | Yes | Screen 1 header identity | No |
| Header action: Export config | Rare | Needed for maintenance, contains sensitive material | Yes | Screen 3 technical area | Hide from Screen 1 |
| Header action: Delete channel | Rare/high risk | Destructive operation | Yes | Screen 2/3 guarded action path | Hide from Screen 1 primary decision |
| Quick state rows: state, role, users, speed, matrix, readiness | Daily | Core channel summary | Yes | Screen 1 compact answer; Screen 2 detail | No |
| Channel Why Card | Daily | Explains why channel is in its current state | Yes | Screen 1 one-line why; Screen 2 full card; Screen 3 trace | No |
| Traffic | Occasional | Supports capacity/usage investigation | Yes | Screen 2 | Hide from Screen 1 |
| Autoswitch / policy controls | Rare/high risk | Controls routing participation, reserve, groups, weight | Yes | Screen 2 actions/settings block | Hide from Screen 1 |
| Materials and contracts | Weekly/incident | Evidence/proposal/execution lookup | Yes | Screen 3 | Hide from Screen 1 |
| Proposal tab | Weekly/incident | Suggested next steps | Yes | Screen 3 | Hide from Screen 1 |
| Evidence tab | Weekly/incident | Proof/source records | Yes | Screen 3 | Hide from Screen 1 |
| Execution tab | Weekly/incident | Contracts/validation/execution records | Yes | Screen 3 | Hide from Screen 1 |
| State snapshot cards | Daily | Health, services, speed/traffic, runtime profile summary | Yes | Screen 1 compressed; Screen 2 expanded | No |
| Snapshot health card | Daily | "Is channel healthy?" | Yes | Screen 1 status row; Screen 2 detail | No |
| Snapshot services card | Daily/weekly | Service readiness | Yes | Screen 2 service health; Screen 1 only problem summary | Hide raw from Screen 1 |
| Snapshot speed/traffic card | Daily/weekly | Speed/traffic status | Yes | Screen 2 route/speed/traffic | Hide raw from Screen 1 unless problem |
| Snapshot events/profile card | Daily/incident | Runtime profile readiness | Yes | Screen 2 profile/runtime readiness; Screen 3 logs | Hide raw from Screen 1 |
| Live key-values: channel, pool state, type, profile readiness, users | Daily | Core facts | Yes | Screen 1 compact; Screen 2 detail | No |
| Operator checklist | Daily/incident | Work-the-problem flow | Yes | Screen 2 | Hide from Screen 1 |
| Checklist health row | Daily | Health check action | Yes | Screen 2 | Screen 1 only status |
| Checklist service matrix row | Daily/weekly | Service check action | Yes | Screen 2 | Screen 1 only service problem |
| Checklist speed row | Weekly/incident | Speed check action | Yes | Screen 2 | Screen 1 only if no measurement/speed issue |
| Checklist users row | Daily | Assigned users and manual switch path | Yes | Screen 2 | Screen 1 only user count/safety |
| Checklist runtime profile row | Daily/incident | Profile readiness | Yes | Screen 2 | Screen 1 only if blocking |
| Checklist logs row | Incident | Audit lookup | Yes | Screen 3 | Hide from Screen 1 |
| Жизненный цикл | Weekly/rare | Draft/import/lifecycle state | Yes | Screen 3 technical/history | Hide from Screen 1 |
| Сравнение скорости | Daily/weekly when diagnosing | Server/client speed details | Yes | Screen 2 | Hide from Screen 1 unless no measurement/speed problem |
| Назначенные пользователи | Daily/incident | Users on channel | Yes | Screen 2 | Screen 1 only count/safety |
| Замеры скорости клиентов | Incident | Per-user client speed detail | Yes | Screen 3 or Screen 2 when speed problem | Hide from Screen 1 |
| Сервисная матрица | Daily/weekly | Service health detail | Yes | Screen 2 | Hide raw rows from Screen 1 |
| Конфигурация | Rare/technical | Config file existence and redaction note | Yes | Screen 3 | Hide from Screen 1 |
| Последние события канала | Incident/audit | Event history | Yes | Screen 3 | Hide from Screen 1 |
| Channel state drawer Why Card | Daily | Explanation of channel trust/state | Yes | Screen 1 compact; Screen 2 full | No |
| Channel state summary | Daily | Trust/use safety/users | Yes | Screen 1/2 | No |
| Trust and recovery | Weekly/incident | Trust score/trend/recovery path | Yes | Screen 2/3 | Hide raw trust from Screen 1 |
| Why so / what happened / what to do | Daily | Operator explanation | Yes | Screen 1 compact and Screen 2 detail | No |
| State drawer services | Weekly/incident | Service status list | Yes | Screen 2 | Hide raw rows from Screen 1 |
| Channel logs drawer | Incident | Event audit and technical records | Yes | Screen 3 | Hide from Screen 1 |
| Config export drawer | Rare/technical | Full config text and copy action | Yes | Screen 3 technical | Hide from Screen 1 |
| Delete migration drawer | Rare/high risk | Migration/delete plan | Yes | Screen 3 or guarded destructive path | Hide from Screen 1 |

Inventory verdict: Channel Drawer already contains the right data, but first-screen information is mixed with investigation, policy, evidence, config, lifecycle, and audit content. The future drawer must separate "operator answer" from "diagnosis" and "technical proof".

## 2. Screen 1 Final Structure

Purpose: one no-scroll operator answer. It must answer only:

1. Channel?
2. Healthy?
3. Users safe?
4. Problem?
5. Action?
6. Why?

Screen 1 must use plain operator language. It must not show engineering vocabulary, raw metrics, evidence, contracts, execution, logs, config, policy internals, raw trust, raw suitability, or service matrix rows.

Exact order top to bottom:

| Row | Purpose |
| --- | --- |
| CHANNEL | Identify channel by display name/id, role/type, enabled/disabled state. |
| HEALTH | Answer healthy/not healthy/check needed in one line. |
| USERS SAFE | Show whether current assigned users can safely stay, with count. |
| PROBLEM | Show the one current problem if any: service, stability, capacity, route, disabled, reserve/canary, no measurements. |
| WHY | One-line channel Why Card reason before any detailed metrics. |
| ACTION | One primary safe next action plus one secondary Details action. |
| WARNING | Conditional only: unsafe users, disabled channel, capacity overflow, service failure, leak/route risk. |

Screen 1 wireframe:

```text
--------------------------------------------------
CHANNEL
--------------------------------------------------
awg3
Role: public traffic
State: enabled

--------------------------------------------------
HEALTH
--------------------------------------------------
Healthy
Channel responds

--------------------------------------------------
USERS SAFE
--------------------------------------------------
8 users assigned
Users can stay here

--------------------------------------------------
PROBLEM
--------------------------------------------------
No action required

--------------------------------------------------
WHY
--------------------------------------------------
Reason: service score and trust are strong       [Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Observe]                                       [Details]

--------------------------------------------------
```

Screen 1 state variants:

| Channel State | Health Row | Users Safe Row | Problem Row | Primary Action |
| --- | --- | --- | --- | --- |
| Healthy | Healthy | Users can stay | No action required | Observe |
| Service failure | Needs Action | Users may be affected | Service check failed | Run Service Check |
| Low stability | Needs Check | Users can stay for now / review | Stability is low | Review Channel |
| Capacity issue | Needs Action | Too many users / no headroom | Capacity issue | Open Users |
| Route issue | Blocked | Users may be unsafe | Route problem | Check Route |
| Disabled | Disabled | Users should not be assigned | Channel is off | Start Channel |
| Reserve | Reserved | Only reserve/canary users | Reserve-only | Details |
| Canary | Limited | Only test users | Canary channel | Details |
| No measurements | Needs Check | Unknown until checked | No recent checks | Run Check |

## 3. Screen 2 Final Structure

Purpose: investigation. Operator works the problem here. Screen 2 may scroll and may include service health, capacity, users, route quality, speed, warnings, and actions.

Exact order:

1. Expanded channel state snapshot.
2. Full Channel Why Card.
3. Operator checklist.
4. Service health summary and service matrix rows.
5. Capacity and assigned users.
6. Route quality and runtime readiness.
7. Speed and traffic.
8. Warnings and blockers, only if non-empty.
9. Safe action controls.
10. Policy/routing participation controls.

| Section | Contents | Purpose |
| --- | --- | --- |
| Expanded state snapshot | Health, services, speed/traffic, runtime profile cards | Gives fast diagnosis after Screen 1. |
| Full Channel Why Card | Status, reason, values, thresholds, source, updated_at, next action | Explains "why" with metrics, but not on first screen. |
| Operator checklist | Health, service matrix, speed, users, runtime profile, logs | Repeatable investigation workflow. |
| Service health | Service summary and per-service result rows | Solves service failure and no-measurement cases. |
| Capacity/users | Assigned user count, soft/hard/headroom if available, assigned users table | Shows whether users can safely stay. |
| Route/runtime readiness | Pool state, runtime profile readiness, route/working profile status | Solves route/runtime readiness issues. |
| Speed/traffic | Server speed, client average, direct average, degradation, traffic | Solves speed and capacity complaints. |
| Warnings/blockers | Only non-empty warnings | Keeps active risk visible without empty noise. |
| Safe actions | Run service matrix, measure speed, open logs, manual switch, start/pause as existing guarded actions | Lets operator act after diagnosis. |
| Policy controls | Existing autoswitch/group/reserve/weight controls | Keeps routing settings available, but below diagnosis. |

## 4. Screen 3 Final Structure

Purpose: technical proof, history, contracts, execution, and audit. This screen is for advanced review, not daily first action.

Exact order:

1. Evidence.
2. Proposals.
3. Execution/contracts.
4. Lifecycle/import history.
5. Raw trust/recovery/source facts.
6. Config existence/export path.
7. Event history/logs.
8. Delete/migration audit if relevant.
9. Technical metadata: source, updated, authority, read-only, schema.

| Section | Contents | Purpose |
| --- | --- | --- |
| Evidence | Evidence bundles, source, freshness, linked object | Proves channel state. |
| Proposals | Suggested next steps, confidence, benefit, rollback hint | Shows suggested operational plan. |
| Execution/contracts | Draft/stored contracts, validation previews | Keeps execution trace away from first screen. |
| Lifecycle | Draft, validation, pool action, profile status, next step | Explains how channel got here. |
| Raw trust/recovery | Trust score, trend, recovery path, blocked action summary, source | Advanced explainability only. |
| Config | File presence, size, redaction status, export action | Technical maintenance only. |
| Events/logs | Recent channel events and context logs | Audit trail. |
| Delete/migration audit | Assigned users, migration plan, blockers, delete result | High-risk path audit. |
| Technical metadata | Source, updated_at, authority, read_only, schema | Traceability. |

## 5. Problem -> Action Matrix

| Channel Problem | Operator Sees | Action |
| --- | --- | --- |
| Healthy | Healthy; users can stay; no action required | Observe |
| Service failure | Needs Action; service check failed; users may be affected | Run Service Check |
| Low stability | Needs Check; stability is low; users can stay only if no active impact | Review Channel |
| Capacity issue | Needs Action; too many users or no headroom | Open Users / review assigned users |
| Route issue | Blocked; route/runtime readiness problem; users may be unsafe | Check Route / open route detail |
| Disabled | Disabled; users should not be assigned here | Start Channel if expected |
| Reserve | Reserved; only reserve users should be here | Details / verify policy |
| Canary | Limited; only test/canary users should be here | Details / verify policy |
| No measurements | Needs Check; no recent service/speed measurements | Run Check |
| Runtime profile not ready | Needs Action; working profile not ready | Open Logs / Details |
| Speed issue | Needs Check; speed stale or bad | Measure Speed |
| Assigned users on deletion | Destructive action blocked; users must migrate first | Open migration plan |

## 6. Why Card Placement

Rule: Why answer first, metrics later.

| Why Card | Screen | Placement | Size |
| --- | --- | --- | --- |
| Channel Why Card compact | Screen 1 | After Problem row, before Action row | One line: `Reason: ... [Details]` |
| Channel Why Card full | Screen 2 | After expanded state snapshot, before checklist | Full metric/threshold/source table |
| Channel Why evidence/raw detail | Screen 3 | After Evidence/Proposals or in raw trust/source facts | Technical trace only |

Screen 1 Why wireframe:

```text
--------------------------------------------------
WHY
--------------------------------------------------
Reason: service score and trust are strong       [Details]
--------------------------------------------------
```

What stays out of Screen 1:

- metric table
- thresholds
- source family
- updated_at unless stale and actionable
- trust score
- recovery path
- blocked action summary
- schema/authority

## 7. Noise Removal Plan

| Current Block | Remove From Screen 1? | New Location | Reason |
| --- | --- | --- | --- |
| Service matrix rows | Yes | Screen 2 | Raw service rows are investigation detail. |
| Assigned users table | Yes | Screen 2 | Screen 1 needs count and safety only. |
| Raw speeds | Yes | Screen 2 | Screen 1 only shows speed if it is the problem. |
| Raw trust score | Yes | Screen 3 | Trust score is technical unless summarized. |
| Raw suitability/recovery facts | Yes | Screen 3 | Advanced explainability. |
| Execution details | Yes | Screen 3 | Technical/governed path only. |
| Evidence | Yes | Screen 3 | Proof is behind details. |
| History/events/logs | Yes | Screen 3 | Audit trail, not first action. |
| Config export | Yes | Screen 3 | Sensitive maintenance action. |
| Delete action | Yes | Screen 2/3 guarded path | Destructive, not first decision. |
| Lifecycle table | Yes | Screen 3 | Import/draft detail. |
| Autoswitch policy controls | Yes | Screen 2 | Settings are useful but too heavy for first screen. |
| Traffic | Yes | Screen 2 | Diagnosis/detail. |
| Client speed rows | Yes | Screen 3 or Screen 2 when speed problem | Per-user detail is noisy first screen. |
| Empty service matrix | Yes | Screen 1 only shows "No recent checks" problem | Empty tables should not consume space. |
| Empty events | Yes | Screen 3 only | Empty logs do not help first answer. |

## 8. Empty State Strategy

Rule: empty information must not consume screen space.

| Empty Block | Hide | Collapse | Keep |
| --- | --- | --- | --- |
| No service matrix measurement | No | No | Keep as Screen 1 problem only if checks are needed; Screen 2 short empty line. |
| No speed measurement | No | Yes | Keep on Screen 2; Screen 1 only if speed/no-measurement is current problem. |
| No assigned users | No | Yes | Keep Screen 1 as `0 users assigned`; Screen 2 table may show empty message. |
| No warnings | Yes | No | No |
| No events | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty audit message only. |
| No evidence | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty evidence message only. |
| No proposals | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty proposal message only. |
| No execution contracts | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty technical message only. |
| No lifecycle history | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty lifecycle message only. |
| No config file | Yes on Screen 1 | No | Keep Screen 3 config status if maintenance opened. |
| No logs | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty log message only. |

## 9. One Screen Rule Validation

Can operator understand channel in 5 seconds?

Verdict: YES.

Reason:

- Screen 1 has one object: channel.
- Health is visible as the second row.
- User safety is visible before details.
- Problem is one sentence.
- Why appears before action.
- Only one primary action and one Details action are visible.
- Raw metrics, tables, logs, evidence, contracts, config, and history are removed.

| Question | Visible On Screen 1 | Required? |
| --- | --- | --- |
| Channel? | Yes | Yes |
| Healthy? | Yes | Yes |
| Users safe? | Yes | Yes |
| Problem? | Yes | Yes |
| Action? | Yes | Yes |
| Why? | Yes | Yes |
| Service matrix rows | No | No |
| Assigned users table | No | No |
| Raw speeds | No | No |
| Evidence/contracts/execution | No | No |
| Logs/history/config | No | No |

## 10. Mobile Review

| Block | Mobile Friendly | Issue |
| --- | --- | --- |
| CHANNEL row | Yes | Long display names must wrap or truncate cleanly. |
| HEALTH row | Yes | Status and short reason should be single-column. |
| USERS SAFE row | Yes | Count plus safety sentence fits. |
| PROBLEM row | Yes | Must stay one short sentence. |
| WHY row | Yes | One-line reason may wrap to two lines; acceptable. |
| ACTION row | Yes | Primary and Details should stack full-width on narrow screens. |
| WARNING row | Yes | Only one actionable warning should render. |
| Expanded snapshot | Partly | Cards must become 1-column on phones. |
| Full Why Card | Partly | Metric table should stack or scroll within section. |
| Service matrix | Partly | Per-service rows should stack; avoid full-page horizontal scroll. |
| Assigned users | Partly | IP/table/status rows should stack on mobile. |
| Speed/traffic | Yes | Key-values work if labels wrap. |
| Policy controls | Partly | Group/weight/reserve controls need vertical layout. |
| Evidence/contracts/logs | Partly | Technical tables can scroll inside Screen 3 sections only. |
| Config export | Partly | Textarea is technical; keep Screen 3 only. |

Mobile verdict: Screen 1 is mobile-friendly. Screens 2/3 require responsive row treatment during implementation, but the information architecture is sound.

## 11. User/Channel Consistency Audit

| Principle | User | Channel | Consistent? |
| --- | --- | --- | --- |
| Problem First | User Screen 1 shows status/problem before detail | Channel Screen 1 shows health/problem before detail | Yes |
| One Action | User Screen 1 has one primary action plus Details | Channel Screen 1 has one primary action plus Details | Yes |
| Why Before Details | User Screen 1 shows compact Why before action | Channel Screen 1 shows compact Why before action | Yes |
| Three Screens | User: Answer / Investigation / Evidence | Channel: Answer / Investigation / Evidence | Yes |
| Technical Last | User logs/contracts/raw reasons are Screen 3 | Channel logs/config/contracts/raw trust are Screen 3 | Yes |
| Empty States Hidden | User hides empty warnings/logs on Screen 1 | Channel hides empty warnings/logs on Screen 1 | Yes |
| No New Workflow | User reuses existing drawer/workflows | Channel reuses existing drawer/workflows | Yes |
| Safety Language | User does not imply direct runtime mutation | Channel avoids destructive/start/delete as first-screen default | Yes |
| Mobile First Screen | User Screen 1 stacks cleanly | Channel Screen 1 stacks cleanly | Yes |
| Operator Mental Model | User asks "who/problem/why/action" | Channel asks "channel/health/safety/problem/why/action" | Yes |

Consistency verdict: the future Channel Drawer follows the same philosophy as the future User Drawer. Operator does not need to learn a second interaction model.

## 12. Final Channel Drawer Specification

Future Channel Drawer is a three-screen information architecture.

| Screen | Name | Operator Question | Contents |
| --- | --- | --- | --- |
| Screen 1 | Operator Answer | "Is this channel healthy, are users safe, and what do I do?" | Channel, health, users safe, problem, why, action, conditional warning. |
| Screen 2 | Investigation | "What exactly is wrong and how do I work it?" | Snapshot, full Why Card, checklist, services, capacity/users, route/runtime, speed/traffic, warnings, actions/policy. |
| Screen 3 | Evidence and Audit | "What proves this and what happened before?" | Evidence, proposals, execution/contracts, lifecycle, raw trust/source facts, config, logs/events, migration/delete audit, metadata. |

Final Screen 1 order:

| Order | Row |
| ---: | --- |
| 1 | CHANNEL |
| 2 | HEALTH |
| 3 | USERS SAFE |
| 4 | PROBLEM |
| 5 | WHY |
| 6 | ACTION |
| 7 | WARNING, conditional only |

Final Screen 2 order:

| Order | Section |
| ---: | --- |
| 1 | Expanded channel state snapshot |
| 2 | Full Channel Why Card |
| 3 | Operator checklist |
| 4 | Service health / service matrix |
| 5 | Capacity and assigned users |
| 6 | Route quality and runtime readiness |
| 7 | Speed and traffic |
| 8 | Warnings and blockers |
| 9 | Safe action controls |
| 10 | Policy/routing participation controls |

Final Screen 3 order:

| Order | Section |
| ---: | --- |
| 1 | Evidence |
| 2 | Proposals |
| 3 | Execution/contracts |
| 4 | Lifecycle/import history |
| 5 | Raw trust/recovery/source facts |
| 6 | Config status/export |
| 7 | Event history/logs |
| 8 | Delete/migration audit |
| 9 | Technical metadata |

Implementation boundary for the future implementation stage:

- Reuse existing `channelDrawerBody`, `renderChannelDrawerLive`, `openChannelStateDrawer`, `channelWhyCard`, and existing channel action workflows.
- Reuse `why_cards.channels_by_id`.
- Do not add a new page, drawer, endpoint, planner, truth source, governance model, or execution path.
- Do not put config export, delete, logs, raw trust, raw service rows, execution, or contracts on Screen 1.
- Keep destructive actions guarded and away from the first operator answer.

## 13. Final Verdict

Final verdict: READY_FOR_CHANNEL_IMPLEMENTATION.

Reason:

- Required truth gate passed.
- Current Channel Drawer blocks are inventoried.
- Screen 1 answers channel health, action requirement, user safety, operator action, and why.
- Screen 2 gives investigation tools without becoming technical audit.
- Screen 3 preserves evidence, contracts, config, events, lifecycle, and audit trail.
- User Drawer and Channel Drawer now share one mental model.
- Mobile and empty-state rules are defined.
- No implementation, UI movement, runtime mutation, or deploy was performed.

Final alignment status at report creation:

| Check | Status |
| --- | --- |
| Local | PASS / ALIGNED |
| GitHub | PASS / ALIGNED |
| Runtime | PASS / ALIGNED with docs-only mismatch ignored |
| Overall | PASS / FULLY_ALIGNED before this docs-only report |

Post-commit and post-push alignment must be verified by the required after-report commands.
