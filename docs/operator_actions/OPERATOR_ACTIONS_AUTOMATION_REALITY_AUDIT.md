# OPERATOR.ACTIONS.1 Automation Reality Audit

## 1. Saved State

| Check | Result |
|---|---|
| Branch | `Updatesystem` |
| Head | `2ffbde2c Add channel health action evidence` |
| Git status before audit | `?? V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` |
| Scope | Audit/report only |
| UI changes | None |
| Runtime / planner / governance changes | None |

Production access note: direct read-only SSH checks for timer state were attempted, but SSH authentication was not available non-interactively (`Permission denied (publickey,password)`). Production reality below uses the successful `tools/v7-truth-check --all --json` runtime snapshot plus local source evidence.

## 2. Truth Gate

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |
| GitHub | PASS, remote `Updatesystem` at `2ffbde2c` |
| Runtime | PASS, deployed code commit `ed64d94d`; local head differs only by docs/evidence |

Runtime snapshot facts:

| Runtime Fact | Evidence |
|---|---|
| Admin service active | `v7-admin-api.service active (running)` |
| Autoswitch service/timer | Intentionally inactive, approved manual mode |
| Runtime tools present | `v7-users-autoswitch`, `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-egress-quality-compact` executable hashes known |
| Intelligence refresh service/timer | Not installed as systemd units |
| Intelligence snapshot files | Present under `/opt/v7/egress/state/intelligence` |

## 3. Action Inventory

| Action | Location | Existing Handler |
|---|---|---|
| Открыть канал / Карточка канала | Channel table, problem drawer, health drawer | `openChannelDrawer(id)` -> `/api/egress-detail` |
| Детали / здоровье score breakdown | Drawer header, score cell | `openChannelSuitabilityBreakdown(id)` |
| Проверить сервисы / Сервисная матрица | Table services cell, health breakdown, drawer snapshot, matrix workspace | `runV2ServiceMatrix(id)` -> `/api/actions/service-matrix-test` |
| Проверить one service | Service matrix cells | `runV2ServiceMatrixForService(id, service)` -> `/api/actions/service-matrix-test` |
| Проверить скорость / Замерить скорость | Channel speed cell, readiness workspace, drawer checklist | `runV2EgressSpeed(id)` -> `/api/actions/egress-speedtest` |
| Открыть пользователей / Показать пользователей | Users column, capacity/load problem | `toggleChannelUsers(id)` |
| Открыть нагрузку | Channel stats, load problem | `openLoadMetricDetail()` |
| Проверить маршрут | Health model action for route deficit | Current safe action opens channel drawer; no route-specific channel handler |
| Проверить готовность / Runtime | Health model, drawer checklist | Mostly `openV2ChannelLogs(id)` and runtime readiness read model |
| Логи канала | Problem drawer, health breakdown, drawer controls | `openV2ChannelLogs(id)` -> `/api/events` filter |
| Показать план | Channel drawer controls | `previewV2ChannelAutoswitch(id)` -> `/api/autoswitch-plan` |
| AUTOSWITCH | Channel drawer controls | `runV2ChannelAutoswitch(id)` -> dry-run then guarded apply if selected moves exist |
| Запустить канал | Drawer controls / problem drawer | `startV2ChannelFromList(id)` -> `/api/actions/egress-set-state-apply` with `ENABLE` |
| Приостановить канал | Drawer controls | `pauseV2ChannelFromList(id)` -> `/api/actions/egress-pause-apply` with `PAUSE_EGRESS` |
| Сохранить policy/autopick settings | Drawer controls | `saveV2ChannelAutoswitchPolicy(id)` -> `/api/actions/org-egress-policy-update` |
| Переключить одного | Drawer controls/checklist | `openV2ManualSwitchPanel(id)` |
| Открыть service catalog/matrix | Channel stats, topology services | `openServiceCatalogDrawer()`, `showChannelWorkspace('matrix')` |
| Доказательства / Предложения / Execution | Channel object panels | `loadChannelObjectPanel(id, kind)` |
| Export config / Copy config | Channel drawer/export path | `/api/egress-config-export`, clipboard copy |
| Delete / migrate and delete channel | Channel drawer delete path | `/api/actions/egress-delete-apply` |

## 4. Automation Audit

| Function | Automatic? | Frequency / Trigger | Truth Source |
|---|---:|---|---|
| Service Matrix full refresh | Configured yes; production active state not directly verified by SSH | Repo systemd timer: every 15 min. Runtime has tool and state source. | `systemd/v7-service-matrix-refresh.timer`, `tools/v7-service-matrix-refresh-all`, runtime truth hashes |
| Manual Service Matrix test | No, operator-triggered refresh | Button POST; up to 120s | `/api/actions/service-matrix-test`, `v7-service-matrix-test` |
| Speed / benchmark state | Partly background via `v7-health`/`v7-benchmark`; manual button exists | Repo health loop every 30s includes history/stability/load/diagnose; direct speedtest is manual | `systemd/drafts/v7-health.service`, `/api/actions/egress-speedtest` |
| Stability validation | Background intelligence | Derived from `egress-history.jsonl` into `stability.state` | `tools/runtime-support/v7-egress-stability` |
| Capacity / load validation | Background intelligence | Derived from users registry into `egress-load.state`; repo health loop every 30s | `tools/runtime-support/v7-egress-load`, `systemd/drafts/v7-health.service` |
| Runtime readiness | Background/read-only model | Read from runtime files and readiness checks; not a user movement action | `egress_runtime_readiness`, `admin_core/runtime_read_views.py` |
| Route reality | Background/read-only checks in overview; route-specific channel action not present | `ip route get` read-only for users, direct routing freshness checks | `route_status`, `admin_core/route_reality_views.py` |
| Trust / history / recovery | Background intelligence | Derived from events, quality summaries, switch history, snapshots | `v7-intelligence-snapshot-refresh`, `v7-users-autoswitch` planner inputs |
| Telegram fast sentinel | Configured background advisory | Repo timer every 4s, `--no-autoswitch` | `systemd/v7-telegram-sentinel.timer`, `tools/v7-telegram-sentinel` |
| Planner evaluation | Automatic when dry-run is invoked; production scheduler inactive | `v7-users-autoswitch --pre-planner-refresh write ... --pretty` | `autoswitch_read_only_plan_command`, runtime truth |
| Autoswitch apply | Operator/governed only in current production | Runtime truth: intentionally inactive approved manual mode | Runtime truth snapshot, `/api/actions/autoswitch-apply-guarded` |

## 5. Operator Value Audit

| Action | Automatic Equivalent Exists? | Operator Value |
|---|---:|---|
| Проверить сервисы | Yes, if service matrix refresh timer is active/configured | Optional acceleration / immediate proof |
| Проверить one service | Partial | Optional targeted refresh; useful during support calls |
| Замерить скорость | Partial | Optional immediate live measurement; useful for complaints |
| Проверить маршрут | Partial read-only route checks exist, but no channel-specific handler | Should be outcome/status, not a button unless a real handler is attached |
| Проверить готовность | Yes as runtime readiness read model | Mostly informational; logs are investigation |
| Открыть пользователей | No equivalent | Operator investigation/action needed for load and evacuation |
| Логи канала | No equivalent | Operator investigation |
| Открыть канал | No equivalent | Navigation/investigation |
| Показать план | No automatic UI equivalent | Operator review of governed plan |
| AUTOSWITCH | No, production scheduler inactive | Operator/governed action |
| Запустить канал | No | Operator-required lifecycle action |
| Приостановить канал | No | Operator-required lifecycle action, may migrate users |
| Сохранить policy/autopick settings | No | Operator/admin configuration |
| Переключить одного | No | Operator/manual intervention |
| Delete / migrate and delete | No | Operator/destructive lifecycle action |
| Evidence/proposals/execution panels | No | Investigation/governance review |

## 6. Service Matrix Reality

The service matrix exists in two forms:

| Layer | Reality |
|---|---|
| Background refresh | `v7-service-matrix-refresh-all` refreshes all enabled egress channels and writes `service-matrix-refresh-summary.json`; repo timer is configured for every 15 minutes. |
| Manual refresh | `/api/actions/service-matrix-test` runs `v7-service-matrix-test egress service` and returns updated `service_matrix_state()`. |
| UI usage | Channel table, service matrix workspace, channel drawer, suitability score, required-services gates. |
| Mutability | Service matrix refresh writes diagnostic state; it does not move users. |
| Operator need | Operator should not need to understand "service matrix" as a daily task. They need the outcome: service unavailable / needs fresh check / service healthy. |

Audit result:

| Current Button | Reality | Recommendation |
|---|---|---|
| Проверить сервисы | Duplicates background refresh when timer is active; useful as manual immediate refresh | BACKGROUND ONLY on first screen; keep manual refresh in details |
| Проверить one service | Targeted refresh, not fully duplicated by all-channel batch | KEEP in service details |
| Сервисная матрица | Internal mechanism name | Rename later to outcome language; keep technical label only deeper |

## 7. Route Validation Reality

Route validation is not a single channel-local action today.

| Route Signal | Reality |
|---|---|
| User route reality | `route_status(users)` runs read-only `ip route get ... from user_ip iif wg0` and checks expected device. |
| Direct RU freshness | `direct_routing_freshness()` runs safe read-only direct domain tests and reports stale/mismatch. |
| Service-aware routing | `service_aware_route_dry_run()` is read-only and explicitly reports `routing_changed: False`, `users_moved: False`, `registry_changed: False`. |
| Channel health route score | `channelSuitabilityRoute()` maps topology groups to Route score; it does not run a route repair. |
| Current route action | `Проверить маршрут` currently opens the channel drawer or disabled no-handler action in health detail. |

Audit result: route validation should not appear as a raw operator command in channel health unless a concrete safe handler is connected. The operator should see the outcome:

| Current Raw Problem | Better Operator Outcome |
|---|---|
| Route validation required | Маршрут не подтвержден |
| Route needs check | Маршрут требует проверки |
| Route OK | Маршрут подтвержден |

## 8. Stability / History Reality

| Validation | Operator Needed? | Evidence |
|---|---:|---|
| Stability | No for calculation; yes only for incident review | `v7-egress-stability` computes avg/floor/stability from `egress-history.jsonl` |
| History | No for calculation; yes only for investigation | `channelSuitabilityHistory()` reads channel decision / why card / recent trust labels |
| Recovery | No direct channel button should be required | Recovery/trust are derived from events and snapshots |
| Runtime readiness | No for calculation; yes for remediation if readiness blocks enable/use | `egress_runtime_readiness`, runtime read models |
| Capacity | No for calculation; yes for resolving overloaded users | `v7-egress-load` derives load from `users.registry`; operator may need to open users |
| Trust evaluation | No | Planner and intelligence snapshots derive trust; operator reviews decisions |

## 9. Problem Relevance Audit

| Problem Currently Shown | Show Raw? | Show Outcome? | Recommendation |
|---|---:|---:|---|
| Telegram unavailable | No | Yes | Show "Telegram недоступен"; hide internal matrix mechanics |
| Service verification required | No | Yes | Show "Сервисы требуют свежей проверки" |
| Route validation required | No | Yes | Show "Маршрут не подтвержден" |
| Channel overloaded | Yes | Yes | Keep; action is users/evacuation, not metric tuning |
| Runtime not measured | No | Yes | Show "Готовность канала не подтверждена" |
| History insufficient | No | Yes | Show "Недостаточно истории для уверенного выбора" |
| Stability below floor | No | Yes | Show "Стабильность ниже требуемого уровня" |
| Assignment blocked | No | Yes | Show human blocker and decision |
| Manual only / reserve / canary | No raw codes | Yes | Show "Только вручную / аварийно" |

## 10. Ideal Operator Model

Operator should see:

1. Problem
2. Meaning
3. Resolution
4. Existing safe action only if operator participation is real

Operator should not see background engine mechanics on the first action surface:

| Hide From First Screen | Reason |
|---|---|
| Service Matrix as command language | It is a measurement system, not an operator goal |
| Route Validation as raw term | Operator needs "route confirmed / not confirmed" |
| Stability/history/recovery validation | Derived intelligence; not something an operator manually performs |
| Planner internals | Should become decision and blocker language |
| Raw score mechanics | Useful deeper, not primary action |

## 11. Keep / Remove Matrix

| Action | Classification | Recommendation |
|---|---|---|
| Открыть канал | Operator Required | KEEP |
| Открыть пользователей | Operator Required | KEEP |
| Логи канала | Operator Required for investigation | KEEP, deeper |
| Показать план | Operator Required for governed decision | KEEP |
| AUTOSWITCH | Operator Required in current production manual mode | KEEP, governed/deeper |
| Запустить канал | Operator Required | KEEP, lifecycle/deeper |
| Приостановить канал | Operator Required | KEEP, lifecycle/deeper |
| Сохранить policy/autopick settings | Operator Required/admin config | KEEP, settings/deeper |
| Переключить одного | Operator Required/manual intervention | KEEP, deeper |
| Delete / migrate and delete | Operator Required/destructive lifecycle | KEEP, protected/deeper |
| Проверить сервисы | Operator Optional | BACKGROUND ONLY on first screen; keep manual refresh in details |
| Проверить one service | Operator Optional | KEEP in service matrix details |
| Замерить скорость | Operator Optional | KEEP in details; first screen should show speed outcome |
| Проверить маршрут | Operator Irrelevant until safe handler exists | REMOVE as button / show status only |
| Проверить готовность | Operator Irrelevant as raw action | BACKGROUND ONLY; expose logs if remediation needed |
| Stability validation | Operator Irrelevant | BACKGROUND ONLY |
| History validation | Operator Irrelevant | BACKGROUND ONLY |
| Recovery validation | Operator Irrelevant | BACKGROUND ONLY |
| Trust evaluation | Operator Irrelevant | BACKGROUND ONLY |

## 12. Final Recommendation

V7 should treat channel actions as a mixed model:

| Category | What Belongs Here |
|---|---|
| KEEP | Navigation, investigation, governed lifecycle changes, user evacuation/manual switch, policy save, protected delete |
| BACKGROUND ONLY | Service matrix result, stability, history, runtime readiness, trust/recovery, capacity calculation |
| MANUAL ONLY | Start/pause channel, one-user switch, guarded autoswitch apply, delete/migrate-delete, policy changes |
| REMOVE / STATUS ONLY | Raw "route validation", "history validation", "stability validation", "runtime validation" as operator buttons |

The next UX step should compress first-screen channel actions to real operator work:

| Problem | Operator Should See |
|---|---|
| Services stale/failing | "Сервисы требуют проверки" + details/manual refresh |
| Overload | "Канал перегружен" + open users/prepare movement |
| Route not confirmed | "Маршрут не подтвержден" + status/details until real handler exists |
| Runtime not ready | "Канал не готов к запуску" + logs/details |
| History/stability weak | "Недостаточно уверенности" + details |

## 13. Final Verdict

MIXED_MODEL

