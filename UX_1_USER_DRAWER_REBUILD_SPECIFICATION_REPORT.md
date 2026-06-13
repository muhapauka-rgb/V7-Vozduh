# UX.1 USER DRAWER REBUILD SPECIFICATION REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: discovery and specification only

No implementation was performed. No component was moved. No UI was changed. No runtime code was changed. No deploy was performed.

## Truth Gate

Required gate was run before this specification.

| Gate | Result | Notes |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED | One transient GitHub read failure was retried; direct repeat passed. |
| `tools/v7-convergence-status --json` | PASS / ALIGNED | Local and GitHub are aligned at `c715a573c0923fe60368b45f6beb6563485c261c`; production is runtime-aligned at `2a4f7fbc43243efbcd9eac3e218ccd034bac5595` with docs-only mismatch ignored. |

Truth gate verdict: PASS. UX.1 may proceed as read-only specification.

## Inputs Used

| Input | Status | Relevant Finding |
| --- | --- | --- |
| `EXPLAINABILITY_0_DISCOVERY_AND_GAP_AUDIT_REPORT.md` | Used | Existing explainability data is strong but fragmented; User Drawer needs one default why-card before expert detail. |
| `EXPLAINABILITY_1_CONTRACT_DISCOVERY_AND_STANDARDIZATION_AUDIT_REPORT.md` | Used | Canonical explainability shape should expose status, reason, value, threshold, source, updated_at, confidence, next_action, read_only, and authority. |
| `EXPLAINABILITY_2_CANONICAL_ADAPTER_AND_WHY_CARD_FOUNDATION_REPORT.md` | Used | Read-only user/channel/planner Why Cards now exist over existing operator decision surface data. |
| `UX_0_OPERATOR_TASK_DISCOVERY_AND_INFORMATION_ARCHITECTURE_REPORT.md` | Used | Future User Drawer should split into Screen 1 operator answer, Screen 2 investigation, Screen 3 evidence/contracts/history. |
| `admin/v7-admin-api` | Inspected | Current drawer blocks are rendered by `renderUserDrawerQuick`, `renderUserDrawerLive`, and `openUserRecommendationDrawer`. |

## 1. Current Drawer Inventory

### Full Current Inventory

| Block | Current Position | Daily Operator Use | Value | Keep | Move | Hide |
| --- | --- | --- | --- | --- | --- | --- |
| Phone confirmation | Quick drawer top | Only when phone requires admin decision | High when present | Yes | Screen 1 conditional warning | No |
| User Why Card | Quick drawer near top, live drawer near top, recommendation drawer after decision | Daily answer to "why" | High | Yes | Screen 1 why row and Screen 2 detail | No |
| Основное / user metadata form | Quick drawer main block | Identify user, company, phone, device, channel | High | Yes | Screen 1 compact identity; editable form to Screen 2 | No |
| Traffic summary | Quick drawer after Основное; live drawer after checklist | Occasional diagnostic | Medium | Yes | Screen 2 | Hide from Screen 1 |
| Что сделать / quick actions | Quick drawer after traffic | Daily next action | High | Yes | Screen 1 required action; expanded controls Screen 2 | No |
| Материалы и контракты tabs | Quick and live drawers near middle | Advanced evidence/proposal/execution lookup | High for audit, low for first decision | Yes | Screen 3 | Hide from Screen 1 |
| Состояние пользователя snapshot | Live drawer top | Daily problem scan | High | Yes | Screen 1 compact state; expanded Screen 2 | No |
| Live identity/state key-values | Live drawer after Why Card | Daily identity/status/channel facts | High | Yes | Screen 1 compact identity/current state; Screen 2 full rows | No |
| Чеклист оператора | Live drawer after live key-values | Daily investigation | High | Yes | Screen 2 | Hide from Screen 1 |
| Идентификация устройства | Live drawer after traffic | Investigation and support | Medium | Yes | Screen 2 | Hide from Screen 1 |
| Путь подключения | Live drawer after device identity | Investigation and onboarding support | Medium | Yes | Screen 2 | Hide from Screen 1 |
| VLESS-профиль | Live drawer after onboarding path | Technical support | Medium | Yes | Screen 2 | Hide from Screen 1 |
| Следующее действие | Live drawer after VLESS profile | Daily action | High | Yes | Screen 1 action; Screen 2 controls | No |
| Действия оператора | Live drawer after next action | Manual operator operations | High but risky/noisy | Yes | Screen 2 | Hide from Screen 1 except one primary action |
| Устройство table | Live drawer after object panels | Investigation | Medium | Yes | Screen 2 | Hide from Screen 1 |
| Фактический маршрут | Live drawer after device table | Route diagnosis | High when route issue exists | Yes | Screen 2; Screen 1 only problem summary | Hide raw table from Screen 1 |
| Скорость клиента | Live drawer after route | Speed investigation | Medium | Yes | Screen 2 | Hide from Screen 1 unless speed is the problem |
| Профили и выдача | Live drawer after speed | Profile support | Medium | Yes | Screen 2 | Hide from Screen 1 unless profile is the problem |
| Предупреждения | Live drawer after profiles | Daily exception awareness | High when non-empty | Yes | Screen 1 conditional warning; Screen 2 list | Hide empty state |
| История переключений | Live drawer after warnings | Audit/history | Medium | Yes | Screen 3 | Hide from Screen 1 |
| Последние команды пользователя | Live drawer near bottom | Technical/audit support | Low for first decision | Yes | Screen 3 | Hide from Screen 1 |
| Последние события пользователя | Live drawer bottom | Technical/audit support | Low for first decision | Yes | Screen 3 | Hide from Screen 1 |
| Recommendation Решение | Recommendation drawer top | Daily route decision review | High | Yes | Screen 1 compact recommendation state; Screen 2 detail | No |
| Recommendation Why Card | Recommendation drawer after decision | Daily explainability | High | Yes | Screen 1 why row; Screen 2 full why card | No |
| Recommendation Прогноз | Recommendation drawer after Why Card | Advanced confidence check | Medium | Yes | Screen 2 | Hide from Screen 1 |
| Сырые причины snapshot | Recommendation drawer after forecast | Debug/detail | Medium | Yes | Screen 3 | Hide from Screen 1 |
| Как система дойдет до действия | Recommendation drawer after raw reasons | Governance path | Medium | Yes | Screen 3 | Hide from Screen 1 |
| Recommendation Действия | Recommendation drawer bottom | Operator approval workflow | High but must be safe | Yes | Screen 2 action area; Screen 1 only safe primary next action | No |

### Required Prompt Inventory

| Block | Keep | Move | Hide |
| --- | --- | --- | --- |
| Phone confirmation | Yes | Screen 1 conditional warning | No |
| User Why Card | Yes | Screen 1 top-half why row | No |
| Основное / metadata | Yes | Screen 1 compact; Screen 2 editable | No |
| Traffic | Yes | Screen 2 | Screen 1 |
| Quick actions | Yes | Screen 1 action; Screen 2 controls | No |
| Materials/contracts | Yes | Screen 3 | Screen 1 |
| Live snapshot | Yes | Screen 1 compact; Screen 2 expanded | No |
| Checklist | Yes | Screen 2 | Screen 1 |
| Device identity | Yes | Screen 2 | Screen 1 |
| Onboarding path | Yes | Screen 2 | Screen 1 |
| VLESS profile | Yes | Screen 2 | Screen 1 |
| Route table | Yes | Screen 2 | Screen 1 raw table |
| Speed | Yes | Screen 2 | Screen 1 unless speed issue |
| Profiles/delivery | Yes | Screen 2 | Screen 1 unless profile issue |
| Warnings | Yes | Screen 1 if non-empty; Screen 2 list | Empty Screen 1 block |
| Switch history | Yes | Screen 3 | Screen 1 |
| Commands/events | Yes | Screen 3 | Screen 1 |
| Raw reasons | Yes | Screen 3 | Screen 1 |
| Execution/evidence/proposals | Yes | Screen 3 | Screen 1 |

## 2. Screen 1 Final Structure

Purpose: one non-scrolling operator answer. It must use plain Russian business language and avoid technical vocabulary such as snapshot, contract, execution, VLESS, governance, adapter, source hash, route reality, and schema.

Ordered exactly top to bottom:

1. Conditional phone/identity warning, only if action is required.
2. Header identity row: name/company, phone, device, IP as secondary text.
3. Problem status row: Works / Needs action / Waiting / Blocked.
4. Current state row: current channel, connection, profile, route, speed summarized as compact chips.
5. Why row: compact User Why Card in one or two plain sentences.
6. Required action row: one primary safe action plus one secondary "details" action.
7. Conditional warning row: leak risk, no profile, no device link, no connection, or channel unavailable. Hidden when empty.

| Block | Contents | Purpose | Why It Stays |
| --- | --- | --- | --- |
| Conditional phone warning | Phone verification/rejection/confirmation status and required decision | Blocks support until identity is resolved | It is urgent and user-specific; hiding it causes wrong operator action. |
| Identity header | Name, company, phone, device, IP | Answers "Who is this?" | Operators start from the person, not from technical facts. |
| Problem status | Works, needs action, waiting, blocked; one short reason | Answers "Is there a problem?" | This is the first operational decision. |
| Current state | Current channel, connection yes/no, profile ready/missing, route OK/leak/check, speed measured/not measured | Answers "Internet works?" and "Current channel?" | These are the minimum daily support facts. |
| Compact Why Card | Kept/move reason, current/recommended channel, source freshness only as plain "updated" text | Answers "Why?" | EXPLAINABILITY.2 already provides the read-only why object; Screen 1 must surface it. |
| Required action | One next safe action from readiness/recommendation state | Answers "What should I do?" | Prevents the drawer from becoming a passive diagnostic page. |
| Conditional warning | Leak risk, missing profile, missing device, unavailable channel, no recommendation | Prevents hidden danger | Warnings must appear only when actionable so they do not consume screen space. |

Screen 1 copy rules:

- Use "пользователь", "канал", "подключение", "профиль", "маршрут", "скорость", "проверить", "выдать", "подождать".
- Do not show "Execution", "snapshot", "contract", "schema", "source_hash", "VLESS", "governance", "adapter" on Screen 1.
- Show at most one primary action.
- Never show empty tables.
- Never show raw logs, raw reasons, contracts, command history, event history, or execution chain.

## 3. Screen 2 Final Structure

Purpose: operator investigation. Screen 2 may scroll and may contain detail, tables, and multiple action controls, but still must stay operator-friendly.

Ordered exactly top to bottom:

1. Expanded user state snapshot.
2. Full operator checklist.
3. Full Why Card with metrics and required-to-move conditions.
4. Editable identity/basic metadata.
5. Profile and delivery detail.
6. Device identity.
7. Connection/onboarding path.
8. Route detail.
9. Traffic summary.
10. Speed detail.
11. Warning list, only if non-empty.
12. Operator action controls.

| Block | Contents | Purpose |
| --- | --- | --- |
| Expanded state snapshot | Profile, route, speed, connection cards with clear status | Fast diagnosis after Screen 1. |
| Operator checklist | Profile, connection, route, leak, speed, logs with status and action | Gives repeatable support workflow. |
| Full User Why Card | Status, reason, value, threshold, source, updated_at, confidence, next action | Makes explainability actionable without raw debug blocks. |
| Basic metadata form | Name, company, phone, device, note, connection mode, IP, channel, status | Allows support data correction. |
| Profile/delivery | Generated profiles, smart profiles, latest link, client capabilities | Solves profile issuance problems. |
| Device identity | Linked device, client, VPN IP, status, revoke action | Solves missing/wrong device cases. |
| Connection path | Onboarding step, last delivery, next step | Explains why user is waiting or not connected. |
| Route detail | Expected route, route status, leak risk, plain explanation | Solves bad route and leak cases. |
| Traffic | Recent/summary traffic for this user | Supports usage/connection investigation. |
| Speed | V7/direct speed, degradation, client status | Solves speed complaints without cluttering Screen 1. |
| Warnings | Service/severity/reason rows | Keeps non-empty risk visible during investigation. |
| Operator actions | Reissue profile, check user, download/link profile, prepare approval, hide recommendation, refresh | Executes safe support actions after diagnosis. |

## 4. Screen 3 Final Structure

Purpose: technical evidence, history, execution readiness, and audit trail. Screen 3 is for advanced operators and engineering-grade review.

Ordered exactly top to bottom:

1. Evidence bundles.
2. Proposals.
3. Execution/contracts.
4. Recommendation raw reasons.
5. Decision chain.
6. Switch history.
7. Command history.
8. Event history.
9. Runtime/source/freshness contract metadata.

| Block | Contents | Purpose |
| --- | --- | --- |
| Evidence | Evidence items, linked source, freshness, recommendation refs | Proves why the operator-facing answer is credible. |
| Proposals | Suggested next steps, benefit, confidence, rollback hint | Shows planned or possible action without implying direct mutation. |
| Execution/contracts | Draft/stored contracts, validation preview, readiness blockers | Keeps safety/governance details away from the first screen. |
| Raw reasons | Snapshot/recommendation reason list | Debugs recommendation construction. |
| Decision chain | Recommendation to approval packet to gates to rollback to execution/audit/closure | Explains full governed path for advanced review. |
| Switch history | Previous user channel moves and reason | Answers historical "what happened before". |
| Command history | Recent user commands and command status | Audits support/runtime actions. |
| Event history | Recent user events and messages | Audits system/user timeline. |
| Contract metadata | source, updated_at, authority, read_only flags, schema names if needed | Technical traceability only. |

## 5. Problem -> Action Matrix

| Problem | What Operator Sees | Action |
| --- | --- | --- |
| No profile | "Профиль не готов" and reason from readiness | Primary: issue/reissue profile. Details: Screen 2 profile block. |
| Device not linked | "Устройство не связано" or empty device identity warning | Primary: open device/access detail. Details: Screen 2 device identity. |
| No connection | "Ждем подключения" with last activity absent/old | Primary: ask user to connect or open link again. Details: Screen 2 connection path. |
| Leak risk | "Есть риск утечки" warning | Primary: run/check actual route before any routing change. Details: Screen 2 route block. |
| Bad route | "Маршрут проверить" with plain route detail | Primary: check user route. Details: Screen 2 route detail. |
| Speed issue | "Нет замера" or degradation shown | Primary: request client speed measurement. Details: Screen 2 speed block. |
| Channel unavailable | Current/recommended channel shown as blocked/unavailable | Primary: inspect recommendation/channel state. Details: Screen 2 Why Card and Screen 3 evidence. |
| No recommendation | "Оставить текущий канал" or "нет безопасного переноса" | Primary: observe / no move. Details: Screen 2 full Why Card and Screen 3 raw reasons. |
| Phone confirmation required | Phone warning at top | Primary: confirm or reject phone. Details stay in warning block. |
| User disabled | "Пользователь приостановлен" | Primary: enable only if expected. Details: Screen 2 actions. |
| Profile delivery pending | "Ждем первое подключение по быстрому коду" | Primary: check pending profile or revoke code if needed. Details: Screen 2 profile/delivery. |
| Warning exists | Non-empty warning row on Screen 1 | Primary: open details. Details: Screen 2 warning list. |

## 6. Why Card Placement

| Why Card | Screen | Position |
| --- | --- | --- |
| User Why Card | Screen 1 | After current state row, before required action. Compact plain-language version. |
| User Why Card | Screen 2 | After checklist, before editable metadata. Full metrics and required-to-move conditions. |
| Recommendation Why Card | Screen 1 | Merged into compact why row when recommendation context is the active problem. |
| Recommendation Why Card | Screen 2 | In recommendation/detail area after decision summary. |
| Recommendation Why Card | Screen 3 | Raw reasons and decision chain only; not the primary card. |
| Route Why Card | Screen 1 | Only as one route chip/warning: OK, check, or leak risk. |
| Route Why Card | Screen 2 | In route detail after profile/connection context. |
| Route Why Card | Screen 3 | Evidence/source route facts and trace metadata. |

Placement rule: Screen 1 has one visible why answer. Screen 2 may show the full canonical metric table. Screen 3 may show raw evidence and contracts.

## 7. Noise Removal Plan

| Current Block | Remove From Screen 1? | New Location | Reason |
| --- | --- | --- | --- |
| Traffic | Yes | Screen 2 | Useful for diagnosis, not first decision. |
| Materials/contracts | Yes | Screen 3 | Advanced objects clutter first screen. |
| Full metadata form | Partly | Screen 2 | Screen 1 needs identity summary, not editing controls. |
| Checklist | Yes | Screen 2 | It is investigation workflow, not first answer. |
| Device identity table | Yes | Screen 2 | Only relevant after missing/wrong device problem. |
| Onboarding path | Yes | Screen 2 | Diagnostic flow; Screen 1 only shows waiting/ready state. |
| VLESS profile | Yes | Screen 2 | Technical term and detail should not appear on first screen. |
| Full route table | Yes | Screen 2 | Screen 1 needs route verdict only. |
| Speed details | Yes unless speed problem | Screen 2 | Measurements are detail except when complaint is speed. |
| Profile artifacts and smart profiles | Yes unless profile problem | Screen 2 | Too large for first screen. |
| Empty warnings | Yes | Hidden | Empty information must not consume space. |
| Switch history | Yes | Screen 3 | Audit history is not daily first action. |
| Commands/events | Yes | Screen 3 | Technical log detail. |
| Raw reasons | Yes | Screen 3 | Debug detail, not operator-first language. |
| Decision chain | Yes | Screen 3 | Governance path belongs to advanced review. |
| Source/schema/authority metadata | Yes | Screen 3 | Technical traceability only. |

## 8. Empty State Strategy

Commercial rule: empty information should not consume screen space.

| Empty Block | Hide? | Collapse? | Keep? |
| --- | --- | --- | --- |
| No warnings | Yes | No | No |
| No traffic | No | Yes | Keep only on Screen 2 as collapsed/short empty line. |
| No measurement | No | Yes | Keep on Screen 2; Screen 1 shows "нет замера" only when speed is relevant. |
| No events | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty message only. |
| No history | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty message only. |
| No commands | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty message only. |
| No generated profiles | Yes on Screen 1 | Yes on Screen 2 | Keep only if profile issue is active. |
| No linked evidence | Yes on Screen 1/2 | Yes on Screen 3 | Keep Screen 3 empty evidence message. |
| No recommendation | No | No | Keep compact "нет безопасного переноса / оставить текущий канал" on Screen 1. |
| No Why Card schema | No | No | Keep fallback plain reason if available; otherwise show "причина пока не рассчитана" only on Screen 2. |

## 9. One Screen Rule Validation

Screen 1 target: visible without scrolling on ordinary admin laptop viewport. It must fit by hiding empty states and removing tables/logs/forms.

| Item | Visible On Screen 1 | Required? |
| --- | --- | --- |
| Identity | Yes | Yes |
| Problem status | Yes | Yes |
| Internet works / connection state | Yes | Yes |
| Current channel | Yes | Yes |
| Why | Yes | Yes |
| Required action | Yes | Yes |
| Phone warning | Conditional | Required only when present |
| Leak/profile/device/channel warning | Conditional | Required only when present |
| Traffic | No | No |
| Full checklist | No | No |
| Editable metadata form | No | No |
| Device table | No | No |
| Profile artifacts | No | No |
| Route table | No | No |
| Speed table | No | No |
| Evidence/proposals/execution | No | No |
| History/logs/raw reasons | No | No |

Fit verdict: YES, the future Screen 1 can fit without scrolling if it is limited to identity, problem, current state, one why answer, one action, and conditional warnings.

## 10. Commercial Benchmark Validation

| Principle | Future Drawer Compliance |
| --- | --- |
| Linear: one customer support answer first | Compliant. Screen 1 starts with person, problem, why, action. |
| Stripe: decision and evidence separated | Compliant. Screen 1 shows answer; Screens 2/3 hold detail/evidence. |
| Cloudflare: status before diagnostics | Compliant. Health/problem/channel appear before route/speed tables. |
| Tailscale: device/user identity is human-readable | Compliant. Screen 1 uses name/company/phone/device; technical IDs are secondary. |
| GitHub Enterprise: audit trail exists but is not first-screen noise | Compliant. History, commands, events, contracts move to Screen 3. |
| Commercial control-panel rule: empty states do not take space | Compliant. Empty warnings/events/history/contracts are hidden or collapsed. |
| Operator safety: action is explicit and safe | Compliant. Screen 1 has one safe next action; governed execution details stay separate. |
| Explainability: why is visible before action | Compliant. Compact Why Card is before required action. |

## 11. Migration Risk Assessment

| Current Feature | Risk If Moved | Mitigation |
| --- | --- | --- |
| Phone confirmation | Operator may miss identity approval/rejection | Keep as Screen 1 conditional top warning. |
| User Why Card | Operator may lose reason for current channel | Keep compact Screen 1 version and full Screen 2 version. |
| Metadata form | Editing could become harder to find | Keep identity summary on Screen 1; put edit form early on Screen 2. |
| Quick actions | Operator may lose support controls | Keep one primary action on Screen 1 and full controls on Screen 2. |
| Traffic | Support may need usage data | Move to Screen 2, not Screen 3. |
| Checklist | Operators may lose repeatable workflow | Make it the first major Screen 2 block. |
| Profile issue | Profile issuance could be buried | If profile is active problem, show it in Screen 1 problem/action; details Screen 2. |
| Route issue | Leak/bad route could be underplayed | Show route verdict and leak warning on Screen 1; details Screen 2. |
| Speed issue | Speed complaints could require extra click | If active problem is speed, show measurement state on Screen 1; details Screen 2. |
| Evidence | Advanced users may distrust simplified answer | Keep evidence one click away on Screen 3 and show source/update in full Why Card. |
| Execution/contracts | Safety chain could be hidden | Screen 3 keeps full chain; Screen 1 action copy must not imply direct runtime mutation. |
| Raw reasons | Debugging could slow down | Keep raw reasons on Screen 3. |
| History/events | Audit trail could become less discoverable | Group all history in Screen 3 with clear order. |
| Empty warnings | Empty "no warnings" may reassure some operators | Use absence of warning as quiet state; keep explicit OK in status row. |

## 12. Final User Drawer Specification

Future User Drawer is a three-screen information architecture:

| Screen | Name | User Question | Contents |
| --- | --- | --- | --- |
| Screen 1 | Operator Answer | "Who is this, is there a problem, why, and what do I do?" | Identity, status, current channel/connection, compact Why Card, one action, conditional warnings. |
| Screen 2 | Investigation | "What exactly is wrong and how do I fix/check it?" | Snapshot, checklist, full Why Card, metadata edit, profile, device, onboarding, route, traffic, speed, warnings, action controls. |
| Screen 3 | Evidence and Audit | "What proves this and what happened before?" | Evidence, proposals, execution/contracts, raw reasons, decision chain, switch history, commands, events, technical metadata. |

Screen 1 must answer these six questions in order:

1. Who is this?
2. Is there a problem?
3. Internet works?
4. Current channel?
5. Why?
6. What should I do?

Final Screen 1 order:

| Order | Block | Max Visible Weight |
| ---: | --- | --- |
| 1 | Conditional identity/phone warning | 1 compact warning band |
| 2 | Identity header | 1 compact row |
| 3 | Problem status | 1 compact row |
| 4 | Current state | 1 compact row of chips |
| 5 | Why | 1 compact card |
| 6 | Required action | 1 compact action row |
| 7 | Conditional operational warning | 1 compact warning band |

Final Screen 2 order:

| Order | Block |
| ---: | --- |
| 1 | Expanded state snapshot |
| 2 | Operator checklist |
| 3 | Full User/Recommendation Why Card |
| 4 | Editable metadata |
| 5 | Profile and delivery |
| 6 | Device identity |
| 7 | Connection/onboarding path |
| 8 | Route detail |
| 9 | Traffic |
| 10 | Speed |
| 11 | Warnings |
| 12 | Operator action controls |

Final Screen 3 order:

| Order | Block |
| ---: | --- |
| 1 | Evidence |
| 2 | Proposals |
| 3 | Execution/contracts |
| 4 | Raw reasons |
| 5 | Decision chain |
| 6 | Switch history |
| 7 | Command history |
| 8 | Event history |
| 9 | Technical source/authority metadata |

Implementation boundary for the next stage:

- Reuse the existing `why_cards` payload from the operator decision surface.
- Reuse existing `renderUserDrawerQuick`, `renderUserDrawerLive`, `openUserRecommendationDrawer`, and object panel sources.
- Do not create a new truth source, planner, routing engine, governance flow, evidence store, or execution path.
- Do not make Screen 1 a dashboard of all facts. It is an operator answer.
- Preserve existing safety copy that approval/preparation does not directly move a user.

## 13. Final Verdict

Final verdict: READY_FOR_IMPLEMENTATION.

Reason:

- Required truth gate passed.
- Current drawer blocks are inventoried.
- Future Screen 1/2/3 structure is defined without changing UI.
- One-screen rule is achievable.
- Why Card placement is defined for user, recommendation, and route contexts.
- Noise and empty-state strategy is defined.
- Migration risks are identified with mitigations.

Final alignment status at report creation:

| Check | Status |
| --- | --- |
| Local | PASS / ALIGNED |
| GitHub | PASS / ALIGNED |
| Runtime | PASS / ALIGNED with docs-only mismatch ignored |
| Overall | PASS / FULLY_ALIGNED before this docs-only report |

Post-commit and post-push alignment must be verified by the required after-report commands.
