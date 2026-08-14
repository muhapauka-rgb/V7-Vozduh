# UX.2 USER DRAWER WIREFRAME AND IMPLEMENTATION PLAN REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: wireframe and implementation-readiness planning only

No UI changes were made. No component movement was made. No implementation was made. No runtime code was changed. No deploy was performed.

## Truth Gate

Required gate was run before discovery.

| Gate | Result | Notes |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED | Local, GitHub, and runtime truth readable. Existing untracked handoff document classified documentation-only and ignored. |
| `tools/v7-convergence-status --json` | PASS / ALIGNED | Runtime action guard is ready; current production mismatch is docs-only for UX reports. |

Truth gate verdict: PASS. UX.2 may proceed as a read-only wireframe and implementation plan.

## Inputs Used

| Input | Status | Use |
| --- | --- | --- |
| `UX_0_OPERATOR_TASK_DISCOVERY_AND_INFORMATION_ARCHITECTURE_REPORT.md` | Used | Operator tasks, one-screen rule, progressive disclosure model. |
| `UX_1_USER_DRAWER_REBUILD_SPECIFICATION_REPORT.md` | Used | Future Screen 1/2/3 structure and migration risks. |
| `EXPLAINABILITY_2_CANONICAL_ADAPTER_AND_WHY_CARD_FOUNDATION_REPORT.md` | Used | `why_cards` payload and compact/full Why Card distinction. |
| `admin/v7-admin-api` | Inspected | Current `renderUserDrawerQuick`, `renderUserDrawerLive`, `openUserRecommendationDrawer`, `whyCardSection`, `userActionControls`. |

## 1. Current Drawer Map

Current User Drawer is not one drawer experience; it is three related surfaces:

- quick drawer from `renderUserDrawerQuick`
- live/detail drawer from `renderUserDrawerLive`
- recommendation drawer from `openUserRecommendationDrawer`

### Current Quick Drawer Compact Map

| Section | Height | Purpose | Keep? |
| --- | ---: | --- | --- |
| Header actions: Delete, Disable/Enable | 44 px | Destructive/user access controls | Keep, but move out of Screen 1 primary path. |
| Phone confirmation | 0-220 px | Confirm/reject identity when required | Keep conditional on Screen 1. |
| Why Card | 220-360 px | Explain why user is here | Keep, but compress to one-line Screen 1. |
| Основное metadata form | 360-520 px | Name, company, phone, device, note, connection mode, IP/channel/status, save/detail | Keep, but split summary Screen 1 and edit Screen 2. |
| Трафик | 120-240 px | Usage/traffic summary | Keep on Screen 2. |
| Что сделать | 180-280 px | Profile/route/speed cards, next action, buttons | Keep, but Screen 1 gets one primary plus one secondary action. |
| Материалы и контракты | 160-220 px | Proposal/evidence/execution tabs | Keep on Screen 3. |

Approx quick drawer height: 1,086-1,840 px. On a 760 px visible drawer, this is about 1.4-2.4 screens.

### Current Live Drawer Compact Map

| Section | Height | Purpose | Keep? |
| --- | ---: | --- | --- |
| Header actions: Delete, Disable/Enable | 44 px | Destructive/user access controls | Keep, not first-screen primary. |
| Состояние пользователя | 180-260 px | Status, profile, route, speed cards | Keep as Screen 2 expanded state; Screen 1 compact row. |
| Why Card | 220-360 px | Full explainability table | Keep full on Screen 2; compact on Screen 1. |
| Live identity/state rows | 240-360 px | User/device/IP/channel/table/status/readiness/next/connection | Keep as Screen 1 summary and Screen 2 detail. |
| Чеклист оператора | 320-460 px | Profile/connection/route/leak/speed/logs workflow | Keep Screen 2. |
| Трафик | 120-240 px | Usage diagnosis | Keep Screen 2. |
| Идентификация устройства | 180-320 px | Device identity facts | Keep Screen 2. |
| Путь подключения | 180-320 px | Onboarding/delivery path | Keep Screen 2. |
| VLESS-профиль | 180-300 px | Profile connection internals | Keep Screen 2, rename/copy later for operator language. |
| Следующее действие | 100-180 px | Next action and controls | Keep Screen 1/2. |
| Действия оператора | 120-220 px | Issue/check/repair/speed/logs/switch/access controls | Keep Screen 2; reduce Screen 1. |
| Материалы и контракты | 160-220 px | Proposal/evidence/execution tabs | Keep Screen 3. |
| Устройство | 120-260 px | Linked device table | Keep Screen 2. |
| Фактический маршрут | 120-220 px | Expected/status/leak/explanation | Keep Screen 2. |
| Скорость клиента | 120-200 px | V7/direct/degradation/client | Keep Screen 2. |
| Профили и выдача | 420-760 px | Artifacts, smart profiles, latest delivery, capabilities | Keep Screen 2. |
| Предупреждения | 80-220 px | Warnings list or empty state | Keep non-empty only; hide empty on Screen 1. |
| История переключений | 140-320 px | Historical movements | Keep Screen 3. |
| Последние команды пользователя | 160-320 px | Command audit | Keep Screen 3. |
| Последние события пользователя | 180-380 px | Event audit | Keep Screen 3. |

Approx live drawer height: 3,344-6,182 px. On a 760 px visible drawer, this is about 4.4-8.1 screens.

### Current Recommendation Drawer Compact Map

| Section | Height | Purpose | Keep? |
| --- | ---: | --- | --- |
| Решение | 300-460 px | Current/recommended channel, state, confidence, benefit, risk, trust, review, next action | Keep as Screen 2 detail; compact outcome on Screen 1. |
| Why Card | 220-360 px | Explain recommendation | Keep compact Screen 1, full Screen 2. |
| Прогноз | 100-180 px | Prediction availability/confidence/summary | Keep Screen 2. |
| Сырые причины snapshot | 160-320 px | Raw reasons | Keep Screen 3. |
| Как система дойдет до действия | 260-440 px | Governed chain | Keep Screen 3. |
| Действия | 120-200 px | Prepare approval, hide recommendation, check packet | Keep Screen 2; Screen 1 gets one safe primary only. |

Approx recommendation drawer height: 1,160-1,960 px. On a 760 px visible drawer, this is about 1.5-2.6 screens.

## 2. Future Screen 1 Wireframe

Purpose: one non-scrolling operator answer. No tables, no raw metrics, no technical terms, no empty states.

Exact future order:

```text
--------------------------------------------------
USER
--------------------------------------------------
Name / Company
Phone
Device
IP

--------------------------------------------------
STATUS
--------------------------------------------------
Needs Action
Short reason: Profile is missing

--------------------------------------------------
CURRENT
--------------------------------------------------
Channel: awg3
Connection: Waiting
Profile: Missing
Route: Not checked

--------------------------------------------------
WHY
--------------------------------------------------
Reason: Current route is best
[Details]

--------------------------------------------------
ACTION
--------------------------------------------------
[Issue Profile]
[Details]

--------------------------------------------------
WARNING
--------------------------------------------------
Phone Confirmation Required
--------------------------------------------------
```

Rules for this wireframe:

| Row | Required | Max Height | Source |
| --- | --- | ---: | --- |
| USER | Yes | 96 px | Existing identity/metadata fields from quick/live drawer. |
| STATUS | Yes | 72 px | Existing readiness/status/operator state. |
| CURRENT | Yes | 96 px | Existing current channel, connection, profile, route facts. |
| WHY | Yes | 64 px | Compact `why_cards.users_by_ip[ip].reason` or recommendation reason. |
| ACTION | Yes | 56 px | Existing `nextUserActionButtons` / recommendation action, reduced to one primary and one secondary. |
| WARNING | Conditional | 48-72 px | Existing phone/leak/profile/device/channel warnings. |

Screen 1 target height:

- normal: 384 px
- with one warning: 456 px
- with phone warning plus one operational warning: 528 px

Screen 1 button target:

- one primary action
- one secondary `Details`
- destructive Delete/Disable remains available in drawer header or deeper controls, but is not part of the first-screen action decision

## 3. Future Screen 2 Wireframe

Purpose: work the case. Screen 2 may scroll. It should contain operator detail and safe support controls, not raw execution/audit history.

Exact future order:

```text
--------------------------------------------------
SCREEN 2: INVESTIGATION
--------------------------------------------------

1. State Snapshot
   Profile | Connection | Route | Speed

2. Operator Checklist
   Profile
   Connection
   Route
   Leak
   Speed
   Logs

3. Full Why Card
   Status
   Reason
   Values / thresholds
   Required to move
   Updated

4. Identity and Metadata
   Name
   Company
   Phone
   Device
   Note
   Connection mode

5. Profile and Delivery
   Profile state
   Smart profiles
   Latest one-time link
   Client capabilities

6. Device Identity
   Linked device
   Client
   VPN IP
   Status

7. Connection Path
   Onboarding stage
   Last delivery
   Next step

8. Route Detail
   Expected route
   Actual route state
   Leak risk
   Plain explanation

9. Traffic
   User traffic summary

10. Speed
   V7 speed
   Direct speed
   Degradation
   Client state

11. Warnings
   Only non-empty warnings

12. Actions
   Issue profile
   Check user
   Request speed
   Logs
   Enable/disable
   Manual switch
--------------------------------------------------
```

Screen 2 visible behavior:

- first fold should show State Snapshot, Checklist start, and Why Card title
- all high-risk or multi-button controls are below diagnosis
- empty warnings do not render
- full Why Card may be table-like here because Screen 2 is investigation, not the first answer

## 4. Future Screen 3 Wireframe

Purpose: evidence, audit, and technical trace. Screen 3 is for advanced operator/engineering review.

Exact future order:

```text
--------------------------------------------------
SCREEN 3: EVIDENCE AND AUDIT
--------------------------------------------------

1. Evidence
   Evidence bundles
   Source
   Freshness
   Linked recommendation

2. Proposals
   Suggested next steps
   Benefit
   Confidence
   Rollback hint

3. Execution / Contracts
   Draft contracts
   Stored contracts
   Validation preview
   Readiness blockers

4. Raw Reasons
   Recommendation reasons
   Snapshot reasons

5. Decision Chain
   Recommendation
   Approval packet
   Freshness gate
   Restore barrier
   Rollback packet
   Governance
   Execution
   Audit
   Closure

6. Switch History
   Time
   From
   To
   Reason

7. Command History
   Time
   Action
   Status
   Reason

8. Event History
   Time
   Severity
   Action
   Result
   Message

9. Technical Metadata
   Source
   Updated
   Authority
   Read-only
   Schema
--------------------------------------------------
```

Screen 3 visible behavior:

- this screen may be long
- it must not be the default for daily support
- raw reasons and schema names are allowed only here
- execution details remain read-only unless existing governed workflows are explicitly invoked through existing controls

## 5. Scroll Reduction Analysis

### Current Drawer

| Section | Approx Height |
| --- | ---: |
| Header actions | 44 px |
| Phone confirmation | 0-220 px |
| Why Card | 220-360 px |
| Основное metadata form | 360-520 px |
| Трафик | 120-240 px |
| Что сделать | 180-280 px |
| Материалы и контракты | 160-220 px |
| Live-only state/checklist/device/profile/route/speed/history/logs | 2,260-4,342 px |

Current quick drawer screen count: 1.4-2.4 screens.

Current live drawer screen count: 4.4-8.1 screens.

Current recommendation drawer screen count: 1.5-2.6 screens.

### Future Drawer

| Section | Approx Height |
| --- | ---: |
| Screen 1 USER | 96 px |
| Screen 1 STATUS | 72 px |
| Screen 1 CURRENT | 96 px |
| Screen 1 WHY | 64 px |
| Screen 1 ACTION | 56 px |
| Screen 1 WARNING | 0-144 px |
| Screen 2 investigation blocks | 1,860-3,320 px |
| Screen 3 evidence/audit blocks | 1,540-3,060 px |

Future Screen 1 count: 0.5-0.7 screens on desktop drawer, about 0.8-1.1 screens on phone if both warning bands appear.

Future Screen 2 count: 2.4-4.4 screens.

Future Screen 3 count: 2.0-4.0 screens.

Scroll reduction verdict:

| Measure | Current | Future | Reduction |
| --- | ---: | ---: | ---: |
| First answer height | 1,086-1,840 px | 384-528 px | About 55-75% less. |
| First answer sections | 6-7 sections | 5-6 compact rows | About 15-30% fewer sections, much less dense. |
| First answer tables | 2-4 tables/forms | 0 tables/forms | 100% removed from Screen 1. |
| First answer raw/expert terms | Several possible | 0 target | 100% removed from Screen 1. |

Goal status: achieved in wireframe. Visible information is dramatically reduced.

## 6. Button Reduction Analysis

### Current Buttons Visible

| Surface | Buttons Visible | Count |
| --- | --- | ---: |
| Quick drawer header | Delete, Disable/Enable | 2 |
| Quick Основное | Save, Details | 2 |
| Quick Что сделать cards | Profile, Route, Speed | 3 |
| Quick Что сделать actions | Details, refresh/update, possible issue/check/download/link buttons, pending check/revoke | 2-6 |
| Quick Materials tabs | Proposals, Evidence, Execution | 3 |
| Live checklist | Six Open buttons | 6 |
| Live next/action controls | Issue, check, repair, speed, logs, switch, enable/disable | 7+ |
| Recommendation drawer | Prepare approval, hide, check packet | 3 |

Current practical first-drawer button count:

- normal quick drawer: 12-16 visible buttons
- pending/profile-heavy state: 14-18 visible buttons
- live drawer: 25+ visible buttons across the scroll

### Future Buttons Visible

| Screen | Buttons Visible | Count |
| --- | --- | ---: |
| Screen 1 | One primary action, Details | 2 |
| Screen 2 | Investigation/action controls, existing workflows reused | 6-10, below diagnostic content |
| Screen 3 | Object tabs/actions only inside evidence/proposal/execution context | 3-8, not first-screen |

Button reduction verdict:

| Measure | Current | Future | Result |
| --- | ---: | ---: | --- |
| First visible action choices | 12-16 | 2 | Meets goal. |
| Primary actions | Multiple competing | 1 | Meets goal. |
| Secondary actions | Many | 1 visible on Screen 1 | Meets goal. |
| Dangerous actions | Header/immediate | Not primary path | Needs careful implementation but architecture is sound. |

## 7. Warning Placement

| Warning | Screen 1 | Screen 2 | Hidden |
| --- | --- | --- | --- |
| Phone confirmation required | Yes, top warning | Full phone details if needed | No |
| Phone rejected | Yes, top warning | Full rejection metadata if needed | No |
| Phone confirmed | No, unless recently relevant | Optional identity details | Yes from Screen 1 |
| User disabled | Yes, status row | Action controls | No |
| Missing profile | Yes, if active blocker | Profile/delivery detail | No |
| Pending profile / first connection waiting | Yes, status/action | Profile/delivery detail | No |
| No connection | Yes, current row/status | Connection path | No |
| Leak risk | Yes, warning band | Route detail | No |
| Bad route / route not checked | Yes, current row | Route detail | No |
| No speed measurement | Only if speed issue active | Speed section | Hidden from Screen 1 otherwise |
| Channel unavailable | Yes, if current/recommended channel state blocks action | Why Card / channel detail | No |
| No recommendation / keep current | Yes as WHY, not warning | Full Why Card/raw reasons | No |
| Empty warnings list | No | No | Yes |
| Command/event empty states | No | No | Hidden until Screen 3 |

Warning rule: Screen 1 shows warnings only if they change the next operator action.

## 8. Why Card Placement

Current `whyCardSection` renders:

- status row
- reason row
- source row
- updated row
- next action row
- metric table
- optional required-to-move table

That is too large for Screen 1.

### Future Why Card Sizes

| Context | Size | Contents |
| --- | ---: | --- |
| Screen 1 compact Why | 64 px | `Reason: Current route is best` plus `[Details]`. |
| Screen 2 full Why | 220-420 px | Status, reason, values, thresholds, required-to-move, updated. |
| Screen 3 raw Why/evidence | 160-520 px | Raw reasons, source, schema, authority, trace. |

Exact Screen 1 Why wireframe:

```text
--------------------------------------------------
WHY
--------------------------------------------------
Reason: Current route is best                 [Details]
--------------------------------------------------
```

Why Card audit verdict:

| Requirement | Verdict |
| --- | --- |
| One-line answer on Screen 1 | PASS |
| Full Why Card stays deeper | PASS |
| Reuses existing `why_cards` | PASS |
| No new truth source | PASS |
| No raw metrics on Screen 1 | PASS |

## 9. Mobile Review

| Screen | Mobile Friendly | Issue |
| --- | --- | --- |
| Screen 1 | Yes | With both phone and leak warnings it may reach one full phone viewport; still acceptable because all first answers remain stacked and table-free. |
| Screen 2 | Partly | Tables from checklist/profile/route/speed need single-column responsive rows during implementation. |
| Screen 3 | Partly | Evidence/contracts/history tables are long; mobile should use stacked rows or horizontal scroll only inside technical sections. |

Mobile implementation constraints:

- Screen 1 must be one column only.
- Screen 1 cannot use multi-column tables.
- Screen 1 action row must wrap to two full-width buttons on narrow screens.
- Screen 2 check cards should become 2-column or 1-column depending width.
- Screen 3 tables may scroll horizontally only inside their own section, not the whole drawer.
- Long IP/channel/device names must wrap or truncate with tooltip/title; they must not push buttons off-screen.

## 10. Commercial Review

| Benchmark | Task First | Problem First | One Action | Minimal Cognitive Load |
| --- | --- | --- | --- | --- |
| Linear | PASS: Screen 1 starts with support answer | PASS | PASS | PASS |
| Stripe | PASS: decision before evidence | PASS | PASS | PASS: evidence is deeper |
| Cloudflare | PASS: status/current before diagnostics | PASS | PASS | PASS |
| Tailscale | PASS: person/device/channel first | PASS | PASS | PASS |
| GitHub Enterprise | PASS: audit trail exists but is not default | PASS | PASS | PASS |

Commercial verdict:

- Screen 1 behaves like a support cockpit, not an engineering log.
- Screen 2 behaves like an investigation workspace.
- Screen 3 behaves like audit/evidence.
- The future design is task-first and problem-first.
- Cognitive load is reduced by removing forms, tables, logs, raw reasons, and execution vocabulary from Screen 1.

## 11. Safe Implementation Phases

No implementation is performed in UX.2. The following phases are the proposed next-step plan after wireframe approval.

| Change | Risk | Complexity |
| --- | --- | --- |
| Add compact Screen 1 renderer using existing user/readiness/why data | Medium | Medium |
| Add compact Why Card rendering mode | Low | Low |
| Reorder current quick drawer blocks into Screen 1/2/3 grouping | Medium | Medium |
| Move full metadata form to Screen 2 position | Medium | Low |
| Move traffic/object panels/history out of first answer | Low | Low |
| Reduce visible Screen 1 actions to primary + Details | Medium | Medium |
| Preserve existing header Delete/Disable controls safely | Medium | Low |
| Make warnings conditional and hide empty warning block | Low | Low |
| Add mobile stacked layout rules for Screen 1 | Medium | Medium |
| Validate with Playwright desktop/mobile screenshots | Low | Medium |

### Phase 1: Screen 1 Shell

Small safe changes only:

1. Create a compact rendering path inside existing User Drawer functions.
2. Reuse existing identity, readiness, current channel, connection, route, speed, and `why_cards`.
3. Add compact Why Card mode for one-line Screen 1.
4. Keep existing full sections available below or behind Details.
5. No new drawer, no new route, no new endpoint.

Exit criteria:

- Screen 1 shows USER, STATUS, CURRENT, WHY, ACTION, conditional WARNING.
- Screen 1 has one primary action and one secondary Details action.
- Full Why Card remains available deeper.

### Phase 2: Investigation Screen Reorganization

Small safe changes only:

1. Place expanded state snapshot first.
2. Place checklist second.
3. Place full Why Card third.
4. Place editable metadata after diagnosis.
5. Keep profile, device, connection, route, traffic, speed, warnings, actions in existing workflows.

Exit criteria:

- Operator can still issue profile, check user, request speed, view logs, and manage access.
- No existing action endpoint changes.
- Empty warning block no longer consumes first-screen space.

### Phase 3: Evidence/Audit Screen Cleanup

Small safe changes only:

1. Group object panels, raw reasons, decision chain, switch history, commands, and events under technical/evidence area.
2. Keep existing proposal/evidence/execution object panel loaders.
3. Preserve read-only safety copy for recommendation approval.
4. Add screenshot/mobile validation.

Exit criteria:

- Screen 3 contains all technical traceability.
- Screen 1 remains clean.
- No runtime mutation path changes.

## 12. Final Wireframe

### Current -> Future

```text
CURRENT QUICK DRAWER
--------------------------------------------------
Header: Delete / Disable
Phone confirmation (conditional)
Why Card (large)
Основное metadata form
Traffic
Что сделать
  Profile / Route / Speed
  Details / profile / check / refresh / pending controls
Materials and contracts
  Proposals / Evidence / Execution
--------------------------------------------------

FUTURE SCREEN 1
--------------------------------------------------
USER
Name / Company
Phone
Device / IP

STATUS
Needs Action
Short reason

CURRENT
Channel / Connection / Profile / Route

WHY
Reason: Current route is best                 [Details]

ACTION
[Primary Action]                              [Details]

WARNING
Only actionable warning
--------------------------------------------------
```

```text
CURRENT LIVE DRAWER
--------------------------------------------------
State cards
Why Card
Identity rows
Checklist
Traffic
Device identity
Connection path
VLESS profile
Next action
Operator actions
Materials/contracts
Device table
Factual route
Client speed
Profiles/delivery
Warnings
Switch history
Commands
Events
--------------------------------------------------

FUTURE SCREEN 2
--------------------------------------------------
State Snapshot
Operator Checklist
Full Why Card
Identity and Metadata
Profile and Delivery
Device Identity
Connection Path
Route Detail
Traffic
Speed
Warnings
Actions
--------------------------------------------------
```

```text
CURRENT RECOMMENDATION / TECHNICAL DETAIL
--------------------------------------------------
Decision
Why Card
Forecast
Raw snapshot reasons
Decision chain
Actions
Object panels mixed into user drawer
History mixed into live drawer
Commands/events at bottom
--------------------------------------------------

FUTURE SCREEN 3
--------------------------------------------------
Evidence
Proposals
Execution / Contracts
Raw Reasons
Decision Chain
Switch History
Command History
Event History
Technical Metadata
--------------------------------------------------
```

Final approved target:

```text
--------------------------------------------------
SCREEN 1: OPERATOR ANSWER
--------------------------------------------------
USER
STATUS
CURRENT
WHY
ACTION
WARNING
--------------------------------------------------

--------------------------------------------------
SCREEN 2: INVESTIGATION
--------------------------------------------------
STATE SNAPSHOT
CHECKLIST
FULL WHY CARD
IDENTITY / METADATA
PROFILE / DELIVERY
DEVICE
CONNECTION PATH
ROUTE
TRAFFIC
SPEED
WARNINGS
ACTIONS
--------------------------------------------------

--------------------------------------------------
SCREEN 3: EVIDENCE AND AUDIT
--------------------------------------------------
EVIDENCE
PROPOSALS
EXECUTION / CONTRACTS
RAW REASONS
DECISION CHAIN
SWITCH HISTORY
COMMAND HISTORY
EVENT HISTORY
TECHNICAL METADATA
--------------------------------------------------
```

## 13. Verdict

Final verdict: READY_FOR_UI_IMPLEMENTATION.

Reason:

- Required truth gate passed.
- Current drawer map is documented with approximate heights.
- Future Screen 1/2/3 wireframes are exact and ordered.
- Screen 1 reduces first-answer height from roughly 1,086-1,840 px to 384-528 px.
- Screen 1 reduces visible action choices from roughly 12-16 to 2.
- Why Card is reduced to one line on Screen 1 and kept full on Screen 2.
- Warnings are actionable-only on Screen 1.
- Mobile constraints are defined.
- Implementation phases are small and reuse existing functions and workflows.

Final alignment status at report creation:

| Check | Status |
| --- | --- |
| Local | PASS / ALIGNED |
| GitHub | PASS / ALIGNED |
| Runtime | PASS / ALIGNED with docs-only mismatch ignored |
| Overall | PASS / FULLY_ALIGNED before this docs-only report |

Post-commit and post-push alignment must be verified by the required after-report commands.
