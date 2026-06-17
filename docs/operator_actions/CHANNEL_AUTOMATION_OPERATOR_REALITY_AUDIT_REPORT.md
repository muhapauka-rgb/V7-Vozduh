# CHANNEL.AUTOMATION.1 Operator Action Reality Audit

## 1. Saved State

| Check | Result |
|---|---|
| Branch | `Updatesystem` |
| Head before report | `34640a25 Refresh operator action automation audit` |
| Git status before audit | `?? V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` |
| Scope | Channel automation audit / report only |
| UI changes | None |
| Planner / governance / execution changes | None |
| Database / storage / snapshot changes | None |
| New automation | None |

This audit is intentionally read-only. It uses existing code, systemd definitions, runtime truth snapshots, and previous operator-action evidence. No channel UX, runtime behavior, planner rule, or automation was changed.

## 2. Truth Gate

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS / `FULLY_ALIGNED` |
| `tools/v7-convergence-status --json` | PASS / `ALIGNED` |
| Local | PASS, `34640a25ebe1fc701108f45ed123e3e2e5c550b4` |
| GitHub | PASS, `34640a25ebe1fc701108f45ed123e3e2e5c550b4` |
| Runtime | PASS, deployed code `ed64d94d8e00f2ba9f937cfe869daf781eeecf3c` |
| Runtime classification | Docs-only mismatch ignored; no deploy required |

Runtime evidence from truth-check:

| Runtime Fact | Evidence |
|---|---|
| Admin runtime | `v7-admin-api.service` active |
| Runtime tools | `v7-users-autoswitch`, `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-egress-quality-compact` present with known hashes |
| Autoswitch | Scheduler/service inactive by approved manual mode |
| State root | `/opt/v7/egress/state` known |
| Snapshot root | `/opt/v7/egress/state/intelligence` known |

## 3. Action Inventory

| Action | Location | Handler |
|---|---|---|
| Открыть канал | Channel table, drawer, health/problem details | `openChannelDrawer(id)` |
| Детали оценки | Channel score / health details | `openChannelSuitabilityBreakdown(id)` |
| Проверить сервисы | Problems, health details, service matrix, attention layer | `runV2ServiceMatrix(id)` -> `/api/actions/service-matrix-test` |
| Запустить service matrix row | Service Matrix workspace | `runV2ServiceMatrix(id)` |
| Проверить отдельный сервис | Service Matrix cell | `runV2ServiceMatrixForService(id, service)` |
| Замерить скорость | Readiness/speed detail surfaces | `runV2EgressSpeed(id)` -> `/api/actions/egress-speedtest` |
| Открыть пользователей | Capacity/load problem, users column | `toggleChannelUsers(id)` / `openChannelMetricDetail("users")` |
| Открыть нагрузку | Channel metric detail | `openLoadMetricDetail()` |
| Проверить маршрут | Route problem/health item | No real channel-local safe validation handler found; current behavior is status/details/disabled safe action |
| Проверить готовность | Runtime/readiness problem | Runtime readiness read model and logs/details; no standalone remediation handler |
| Логи канала | Channel details / health / controls | `openV2ChannelLogs(id)` -> `/api/events` |
| Показать план | Channel controls | `previewV2ChannelAutoswitch(id)` -> `/api/autoswitch-plan` |
| AUTOSWITCH | Channel controls | `runV2ChannelAutoswitch(id)` guarded plan/apply path |
| Запустить канал | Channel controls / problem action | `startV2ChannelFromList(id)` -> `/api/actions/egress-set-state-apply` |
| Приостановить канал | Channel controls | `pauseV2ChannelFromList(id)` -> `/api/actions/egress-pause-apply` |
| Save policy / autopick | Channel controls | `saveV2ChannelAutoswitchPolicy(id)` -> `/api/actions/org-egress-policy-update` |
| Переключить одного | Channel controls | `openV2ManualSwitchPanel(id)` |
| Evidence / Proposals / Execution | Channel details panels | `loadChannelObjectPanel(id, kind)` |
| Export / Copy config | Channel drawer controls | `/api/egress-config-export`, clipboard |
| Delete / migrate-delete | Channel lifecycle controls | `/api/actions/egress-delete-apply` |

## 4. Automation Inventory

| Function | Automatic? | Worker | Frequency | Evidence |
|---|---:|---|---|---|
| Service Matrix full refresh | Configured automatic | `v7-service-matrix-refresh-all` | `systemd/v7-service-matrix-refresh.timer`: `OnUnitActiveSec=15min` | Timer/service files, runtime tool hash |
| Service Matrix targeted refresh | No | `v7-service-matrix-test` | Operator-triggered | `/api/actions/service-matrix-test` |
| Route Validation | Partly automatic/read-only | `route_status`, direct route freshness, route summaries | On admin read / diagnostic refresh | `admin_core/route_reality_views.py`, route views |
| Runtime Readiness | Yes/read-only | runtime readiness views | On admin read / runtime truth | `admin_core/runtime_read_views.py`, truth snapshot |
| Health Evaluation | Yes | `channelHealth`, `channelSuitability*` | On channel render | `admin/v7-admin-api` |
| Trust | Yes | intelligence snapshots / planner | Snapshot and planner reads | `v7-intelligence-snapshot-refresh`, `admin_core/intelligence_workers.py`, `v7-users-autoswitch` |
| Recovery | Yes | channel trust recovery model | Snapshot-derived | `trust-evolution-summaries`, `build_channel_trust_recovery_model` |
| History | Yes | `v7-egress-quality-compact`, planner quality history | `systemd/v7-egress-quality-compact.timer`: `OnUnitActiveSec=5min` | Timer/tool, planner history readers |
| Stability | Yes | `v7-egress-stability`, quality compact | health loop draft every 30s; quality compact every 5m | `systemd/drafts/v7-health.service`, `tools/runtime-support/v7-egress-stability` |
| Capacity | Yes | `v7-egress-load`, channel load read model | health loop draft every 30s / admin read | `tools/runtime-support/v7-egress-load`, channel load UI |
| Planner Evaluation | Hybrid | `v7-users-autoswitch` | Planner/readiness generation automatic; apply manual in production | Runtime truth: autoswitch scheduler inactive approved manual mode |
| Eligibility Evaluation | Yes | `v7-users-autoswitch` candidate/blocker model | Planner evaluation | `stability_below_floor`, role, route, trust, capacity blockers |

## 5. Service Matrix Reality

SERVICE_MATRIX_REALITY_REPORT

| Question | Answer |
|---|---|
| Does Service Matrix already run automatically? | Yes, repo systemd defines `v7-service-matrix-refresh.timer` at 15 minute cadence. Runtime truth confirms `v7-service-matrix-refresh-all` exists with known hash. |
| Which timer? | `systemd/v7-service-matrix-refresh.timer` |
| Which worker? | `/usr/local/bin/v7-service-matrix-refresh-all` from `tools/v7-service-matrix-refresh-all` |
| Manual worker? | `/usr/local/bin/v7-service-matrix-test` from `tools/v7-service-matrix-test` |
| Which outputs? | Service matrix state consumed by overview, channel table, service matrix workspace, channel drawer, channel suitability/services score, and required-service gates. |
| What if operator never presses `Проверить сервисы`? | The configured background refresh will refresh the same diagnostic class. Operator loses immediate refresh/proof, not the existence of validation. |

Verdict: `Проверить сервисы` is not a first-line operator action. It is an optional manual acceleration and should live in details, while the first-line operator surface shows the human outcome: service failed, stale, or healthy.

## 6. Route Validation Reality

ROUTE_VALIDATION_REALITY_REPORT

| Question | Answer |
|---|---|
| What is route validation? | A read-model/diagnostic family: user route reality, direct route freshness, route summaries, and channel route suitability. |
| What generates it? | Admin read models such as `route_status`, direct routing freshness, route views, and suitability derivation. |
| What consumes it? | Overview route metrics, security/route surfaces, channel suitability route score, and operator route status language. |
| Should operator manually trigger it? | Not as a raw channel action. Operator should see route outcome and only get a button if a real safe handler exists. |
| Does a real channel-local safe action exist? | No concrete channel-local `Проверить маршрут` handler was found. Current safe behavior is details/status/disabled action. |

Verdict: `Проверить маршрут` should be `STATUS ONLY` until a real safe channel-local handler exists.

## 7. Validation Classification

| Validation | Classification | Evidence |
|---|---|---|
| Services | A. Background intelligence + B. Operator review | Background timer exists; manual refresh only accelerates proof. |
| Route | A. Background intelligence | Read-only route/readiness models exist; no channel-local action. |
| Runtime | A. Background intelligence | Runtime readiness is read from runtime state/truth and admin read models. |
| Health | A. Background intelligence | `channelHealth`/`channelSuitability*` compute on render. |
| Trust | A. Background intelligence | Planner/snapshot model consumes trust summaries. |
| Recovery | A. Background intelligence + B. Operator review | Recovery state is snapshot-derived; operator may review, not compute. |
| History | A. Background intelligence | Quality history is compacted and read by planner. |
| Stability | A. Background intelligence | `v7-egress-stability` and quality compact derive stability. |
| Capacity | A. Background intelligence + C. Operator action | Load is calculated automatically; resolving overload may require opening users/moving users. |
| Planner Evaluation | A. Background intelligence + B. Operator review | Plan can be generated; production apply remains manual/governed. |
| Eligibility Evaluation | A. Background intelligence | Candidate blockers are calculated by planner. |

## 8. Button Value Audit

| Button | Automatic Equivalent Exists? | Operator Value |
|---|---:|---|
| Проверить сервисы | Yes | Optional immediate refresh; not primary daily action |
| Запустить service matrix | Yes | Optional diagnostic refresh in details |
| Проверить отдельный сервис | Partial | Useful targeted check in details |
| Проверить маршрут | Partial read-only | No real channel-local action; should be status/details |
| Проверить стабильность | Yes | No direct operator value as button |
| Проверить историю | Yes | No direct operator value as button |
| Проверить готовность | Yes/read-only | Operator needs outcome/logs, not raw validator |
| Замерить скорость | Partial | Useful manual check for speed complaint |
| Открыть пользователей | No | Real operator action for overload/evacuation |
| Открыть канал | No | Real navigation/investigation |
| Логи канала | No | Real evidence review |
| Показать план | No | Real governed review |
| AUTOSWITCH | No in current production mode | Real governed/manual action |
| Запустить канал | No | Real lifecycle action |
| Приостановить канал | No | Real lifecycle action |
| Policy/autopick save | No | Real admin configuration |
| Переключить одного | No | Real manual intervention |
| Delete / migrate-delete | No | Real protected lifecycle action |

## 9. Problem Relevance Audit

| Problem | Raw Engine State | Human Outcome |
|---|---|---|
| Требуется проверка сервисов | Hide | Сервисы требуют свежей проверки |
| Telegram unavailable | Hide matrix reason | Telegram недоступен |
| Требуется проверка маршрута | Hide | Маршрут не подтвержден |
| History validation required | Hide | Недостаточно данных |
| Stability validation required | Hide | Стабильность ниже требуемого уровня |
| Runtime validation required | Hide | Готовность канала не подтверждена |
| Capacity / load limit | Show humanized | Канал перегружен |
| Assignment blocked | Hide raw blocker | Канал нельзя использовать: human blocker |
| Emergency only / manual only | Hide raw role code | Только вручную / аварийно |

## 10. Keep / Remove Matrix

| Action | Category | Recommendation |
|---|---|---|
| Открыть канал | A - Operator Required | KEEP |
| Открыть пользователей | A - Operator Required | KEEP |
| Логи канала | A - Operator Required | KEEP deeper |
| Показать план | A - Operator Required | KEEP governed/deeper |
| AUTOSWITCH | A - Operator Required | KEEP governed/deeper |
| Запустить канал | A - Operator Required | KEEP lifecycle/deeper |
| Приостановить канал | A - Operator Required | KEEP lifecycle/deeper |
| Save policy/autopick | A - Operator Required | KEEP settings/deeper |
| Переключить одного | A - Operator Required | KEEP deeper |
| Delete / migrate-delete | A - Operator Required | KEEP protected/deeper |
| Проверить сервисы | B - Operator Optional | BACKGROUND ONLY on first-line UX; keep manual refresh in details |
| Запустить service matrix | B - Operator Optional | KEEP in service matrix details |
| Проверить отдельный сервис | B - Operator Optional | KEEP in service details |
| Замерить скорость | B - Operator Optional | KEEP in speed/details |
| Проверить маршрут | C - Operator Irrelevant as raw action | REMOVE / STATUS ONLY |
| Проверить стабильность | C - Operator Irrelevant | BACKGROUND ONLY |
| Проверить историю | C - Operator Irrelevant | BACKGROUND ONLY |
| Проверить готовность | C - Operator Irrelevant as raw action | BACKGROUND ONLY, expose logs/details |
| Trust/recovery validation | C - Operator Irrelevant as raw action | BACKGROUND ONLY, expose decision/reason |

## 11. Ideal Operator Model

Evidence supports a mixed model:

Problem
↓
Meaning
↓
Resolution
↓
Safe action only if operator involvement is real

Operator should see:

| Visible | Hidden From First-Line UX |
|---|---|
| Human problem outcome | Internal validators |
| Business meaning | Background diagnostics |
| One real next action | Route mechanics |
| Details/evidence on demand | Planner internals |
| Governed lifecycle actions | Raw engine states |

## 12. Final Recommendation

| Current Channel Action Class | Decision |
|---|---|
| Navigation/investigation | KEEP |
| Users/load resolution | KEEP |
| Governed lifecycle and autoswitch | MANUAL ONLY |
| Policy changes and destructive actions | MANUAL ONLY, protected/deeper |
| Service Matrix | BACKGROUND ONLY on first-line UX; manual refresh in details |
| Speed check | BACKGROUND/STATUS first, manual details for complaints |
| Route validation | REMOVE as button / STATUS ONLY |
| Stability/history/runtime/trust/recovery validation | BACKGROUND ONLY |
| Planner eligibility/blockers | Human outcome only, not raw engine mechanics |

The next channel UX pass should not add more controls. It should remove first-line exposure to internal validators and keep only real operator work.

## 13. Final Verdict

MIXED_MODEL

V7 already performs or derives most channel validation automatically. Operator actions remain valid only where human/governed involvement is real: lifecycle, users, manual movement, policy, guarded execution, logs, and evidence review. First-line channel UX should stop presenting automated validators as if they are daily operator buttons.
