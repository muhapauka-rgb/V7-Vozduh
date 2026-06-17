# OPERATOR.ACTIONS.1 Automation Reality Audit

## 1. Saved State

| Check | Result |
|---|---|
| Branch | `Updatesystem` |
| Head before this report refresh | `07f16850 Move operator action audit into docs` |
| Git status before audit | `?? V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` |
| Scope | Audit/report only |
| UI changes | None |
| Runtime / planner / governance changes | None |
| Storage / snapshots / automation changes | None |
| Report path | `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md` |

Production access note: direct ad-hoc SSH timer checks were not available non-interactively in the previous pass (`Permission denied (publickey,password)`). This report therefore uses evidence from the successful `tools/v7-truth-check --all --json` runtime snapshot, repository systemd definitions, runtime tool hashes reported by truth-check, and source-level UI/action handlers. No production mutation was performed.

## 2. Truth Gate

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS / `FULLY_ALIGNED` |
| `tools/v7-convergence-status --json` | PASS / `ALIGNED` |
| Local | PASS, branch `Updatesystem`, commit `07f16850ff2c785f715a3a039ed702b8ab3b825c` |
| GitHub | PASS, remote `Updatesystem` at `07f16850ff2c785f715a3a039ed702b8ab3b825c` |
| Runtime | PASS, deployed code commit `ed64d94d8e00f2ba9f937cfe869daf781eeecf3c` |
| Runtime mismatch classification | Docs-only mismatch ignored; no deployment required |

Runtime snapshot facts used as evidence:

| Runtime Fact | Evidence |
|---|---|
| Admin service active | `v7-admin-api.service active (running)` from truth-check runtime snapshot |
| Autoswitch service/timer | Intentionally inactive, approved manual mode |
| Runtime tools present | `v7-users-autoswitch`, `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-egress-quality-compact` executable hashes known |
| Snapshot root known | `/opt/v7/egress/state` |
| Intelligence snapshot files | Present under `/opt/v7/egress/state/intelligence` |
| Runtime action status | `READY_FOR_RUNTIME_ACTION`, but this audit performed no runtime action |

## 3. Action Inventory

| Action | Location | Handler |
|---|---|---|
| Открыть канал / Карточка канала | Channel table, problem drawer, health drawer | `openChannelDrawer(id)` -> `/api/egress-detail` |
| Детали оценки / breakdown | Drawer header, score cell | `openChannelSuitabilityBreakdown(id)` |
| Проверить сервисы / Сервисная матрица | Table services cell, health breakdown, drawer snapshot, matrix workspace, Attention Layer | `runV2ServiceMatrix(id)` -> `/api/actions/service-matrix-test` |
| Проверить one service | Service matrix cells | `runV2ServiceMatrixForService(id, service)` -> `/api/actions/service-matrix-test` |
| Проверить скорость / Замерить скорость | Channel speed cell, readiness workspace, drawer checklist | `runV2EgressSpeed(id)` -> `/api/actions/egress-speedtest` |
| Открыть пользователей / Показать пользователей | Users column, capacity/load problem, Attention Layer | `toggleChannelUsers(id)` or `openChannelMetricDetail("users")` |
| Открыть нагрузку | Channel stats, load problem | `openLoadMetricDetail()` |
| Проверить маршрут | Health model action for route deficit | Current safe action opens channel drawer or shows disabled/info action; no channel-local route validation handler found |
| Проверить готовность / Runtime | Health model, drawer checklist | Runtime readiness read model plus logs/details; no standalone safe remediation handler |
| Логи канала | Problem drawer, health breakdown, drawer controls | `openV2ChannelLogs(id)` -> `/api/events` filter |
| Показать план | Channel drawer controls | `previewV2ChannelAutoswitch(id)` -> `/api/autoswitch-plan` |
| AUTOSWITCH | Channel drawer controls | `runV2ChannelAutoswitch(id)` -> dry-run then guarded apply only if selected moves exist |
| Запустить канал | Drawer controls / problem drawer | `startV2ChannelFromList(id)` -> `/api/actions/egress-set-state-apply` with `ENABLE` |
| Приостановить канал | Drawer controls | `pauseV2ChannelFromList(id)` -> `/api/actions/egress-pause-apply` with `PAUSE_EGRESS` |
| Сохранить policy/autopick settings | Drawer controls | `saveV2ChannelAutoswitchPolicy(id)` -> `/api/actions/org-egress-policy-update` |
| Переключить одного | Drawer controls/checklist | `openV2ManualSwitchPanel(id)` |
| Открыть service catalog/matrix | Channel stats, topology services | `openServiceCatalogDrawer()`, `showChannelWorkspace("matrix")` |
| Доказательства / Предложения / Execution | Channel object panels | `loadChannelObjectPanel(id, kind)` |
| Export config / Copy config | Channel drawer/export path | `/api/egress-config-export`, clipboard copy |
| Delete / migrate and delete channel | Channel drawer delete path | `/api/actions/egress-delete-apply` |

## 4. Automation Inventory

| Function | Automatic? | Worker | Frequency | Evidence |
|---|---:|---|---|---|
| Service Matrix full refresh | Configured automatic | `v7-service-matrix-refresh-all` | Repo timer `OnCalendar=*:0/15` | `systemd/v7-service-matrix-refresh.timer`, `tools/v7-service-matrix-refresh-all`, runtime truth hashes |
| Manual Service Matrix test | No | `v7-service-matrix-test` | Operator button only | `/api/actions/service-matrix-test` |
| Route Validation | Partly automatic/read-only | `route_status`, direct freshness, service-aware dry-run | On read/API refresh, not channel button | `admin_core/route_reality_views.py`, route summary models |
| Stability Validation | Yes | `v7-egress-stability` | Health loop draft every 30s; quality compaction every 5m | `systemd/drafts/v7-health.service`, `systemd/v7-egress-quality-compact.timer`, `tools/runtime-support/v7-egress-stability` |
| History Validation | Yes | `v7-egress-quality-compact`, planner history readers | Quality compact timer every 5m; planner reads history | `tools/v7-egress-quality-compact`, `tools/v7-users-autoswitch` |
| Recovery Validation | Yes | Intelligence snapshot / planner read models | Snapshot/plan refresh, event-derived | `tools/v7-intelligence-snapshot-refresh`, `admin_core/intelligence_snapshots.py` |
| Runtime Validation | Yes/read-only | Runtime readiness views | On admin API read and snapshot truth | `admin_core/runtime_read_views.py`, truth-check runtime snapshot |
| Trust Evaluation | Yes | Planner / intelligence platform | Planner run and snapshots | `tools/v7-users-autoswitch`, `admin_core/intelligence_platform.py` |
| Channel Health Evaluation | Yes | Admin read model | On overview/detail render | `channelHealth`, `channelSuitability*` in `admin/v7-admin-api` |
| Planner Evaluation | Hybrid | `v7-users-autoswitch` | Automatic dry-run/plan generation; apply is manual in production | Runtime truth: scheduler intentionally inactive approved manual mode |
| Capacity Evaluation | Yes | `v7-egress-load` | Health loop draft every 30s; admin read model | `tools/runtime-support/v7-egress-load`, `channelLoad` |
| Eligibility Evaluation | Yes | `v7-users-autoswitch` candidate rules | Planner evaluation | `tools/v7-users-autoswitch` assignment/blocker model |

## 5. Service Matrix Reality

`Service Matrix` is a measurement/diagnostic system, not a business action by itself.

| Question | Evidence-Based Answer |
|---|---|
| Does it already run automatically? | Yes in repo configuration: `v7-service-matrix-refresh.timer` runs every 15 minutes and calls `v7-service-matrix-refresh-all`. Runtime truth confirms the tool exists and hash is known. Direct timer active state was not rechecked via SSH in this audit. |
| Which worker? | `tools/v7-service-matrix-refresh-all` for all-channel refresh; `tools/v7-service-matrix-test` for operator/manual targeted check. |
| Which outputs? | Service matrix state used by overview, channel table, service matrix workspace, channel drawer, suitability score, and required-service gates. |
| What if operator never presses `Проверить сервисы`? | The configured background refresh should eventually refresh all enabled channels. Operator loses immediate proof/acceleration, not the underlying diagnostic path. |
| Is it safe to keep the manual button? | Yes, but only deeper/details. On first screen it duplicates automation and increases action noise. |

SERVICE_MATRIX_REALITY_REPORT:

| Current Surface | Reality | Recommendation |
|---|---|---|
| `Проверить сервисы` on first action layer | Duplicates background refresh when timer is active/configured | BACKGROUND ONLY on first screen; keep manual refresh in details |
| `Запустить` in matrix workspace | Explicit manual refresh of diagnostic state | KEEP in service details |
| One-service cell click | Targeted manual refresh, not fully equivalent to all-channel batch | KEEP in service details |
| Label `Сервисная матрица` | Internal system name | Keep only in technical/details, translate first-screen outcome to human problem language |

## 6. Route Validation Reality

Route validation is not a single channel-local safe action today.

ROUTE_VALIDATION_REALITY_REPORT:

| Route Signal | Reality |
|---|---|
| User route reality | `route_status(users)` performs read-only route checks such as `ip route get ...` and compares expected route/device. |
| Direct RU freshness | Direct routing freshness checks report stale/mismatch status. |
| Service-aware routing | Dry-run models are read-only and explicitly avoid routing/user/registry mutation. |
| Channel route score | Channel suitability route score is derived from topology/group/readiness, not from pressing a channel route button. |
| Current `Проверить маршрут` action | No concrete channel-local route validation handler was found; it opens details or shows no safe handler. |

Conclusion: `Проверить маршрут` should not appear as a raw primary operator command unless a real safe handler exists. Operator should see route outcome:

| Raw Engine State | Human Outcome |
|---|---|
| Route validation required | Маршрут не подтвержден |
| Route needs check | Маршрут требует проверки |
| Route OK | Маршрут подтвержден |

## 7. Stability / History Reality

| Validation | Automatic? | Operator Required? | Evidence |
|---|---:|---:|---|
| Stability | Yes | No for calculation; yes only for incident review | `v7-egress-stability` derives avg/floor/stability from `egress-history.jsonl` |
| History | Yes | No for calculation; yes only for investigation | `v7-egress-quality-compact`, planner quality history readers |
| Recovery | Yes | No direct operator button should be required | Recovery/trust are derived from events and snapshots |
| Runtime readiness | Yes/read-only | No for calculation; yes only if remediation is available | `egress_runtime_readiness`, runtime read models |
| Capacity | Yes | No for calculation; yes to resolve overload | `v7-egress-load` derives load; operator may need `Открыть пользователей` |
| Trust evaluation | Yes | No for calculation; yes to review decisions | Planner and intelligence snapshots derive trust/eligibility |

## 8. Button Value Audit

| Action | If operator never presses it, will V7 eventually do same check automatically? | Automatic Equivalent Exists? | Value |
|---|---:|---:|---|
| Проверить сервисы | Yes, if configured refresh timer is active | Yes | Optional acceleration / immediate proof |
| Проверить one service | Not exactly; all-refresh covers service state but not targeted operator timing | Partial | Optional targeted refresh |
| Замерить скорость | Partly; history/quality exists, immediate speedtest is manual | Partial | Useful for live complaint |
| Проверить маршрут | No channel-local handler; read-only route models already exist elsewhere | Partial/read-only | Should be status/outcome, not button |
| Проверить готовность | Yes as runtime readiness read model | Yes | Mostly informational |
| Открыть пользователей | No | No | Real investigation/action |
| Логи канала | No | No | Real investigation |
| Открыть канал | No | No | Navigation/investigation |
| Показать план | No UI equivalent | No | Real governed review |
| AUTOSWITCH | No, production scheduler is intentionally inactive | No | Real governed action |
| Запустить канал | No | No | Real lifecycle action |
| Приостановить канал | No | No | Real lifecycle action |
| Сохранить policy/autopick settings | No | No | Real admin configuration |
| Переключить одного | No | No | Real manual intervention |
| Delete / migrate and delete | No | No | Real protected lifecycle action |
| Evidence/proposals/execution panels | No | No | Real governance/investigation |

## 9. Problem Relevance Audit

| Problem | Show Raw Engine State? | Show Human Outcome? | Reason |
|---|---:|---:|---|
| Требуется проверка сервисов | No | Yes: `Сервисы требуют свежей проверки` | Service matrix is a background diagnostic mechanism. |
| Telegram unavailable | No | Yes: `Telegram недоступен` | Operator needs the failing service, not matrix internals. |
| Требуется проверка маршрута | No | Yes: `Маршрут не подтвержден` | No channel-local route action exists. |
| Channel overloaded / Канал перегружен | Yes, humanized | Yes: `Канал перегружен` | Real operator action is moving/opening users. |
| Runtime not measured | No | Yes: `Готовность канала не подтверждена` | Runtime validation is read-model work. |
| History validation required | No | Yes: `Недостаточно данных` | History is background intelligence. |
| Stability below floor | No raw code | Yes: `Стабильность ниже требуемого уровня` | Planner/internal threshold should not leak as code. |
| Assignment blocked | No raw blocker | Yes: human blocker and decision | Operator needs `can use / cannot use / why`. |
| Manual only / reserve / canary | No raw role code | Yes: `Только вручную / аварийно` | Role is valid, but must be human language. |

## 10. Keep / Remove Matrix

| Action | Category | Reason | Final Recommendation |
|---|---|---|---|
| Открыть канал | A - Operator Required | Navigation/investigation cannot happen automatically | KEEP |
| Открыть пользователей | A - Operator Required | Needed for overload/evacuation/user review | KEEP |
| Логи канала | A - Operator Required | Evidence review is operator investigation | KEEP deeper |
| Показать план | A - Operator Required | Governed decision review | KEEP |
| AUTOSWITCH | A - Operator Required | Production autoswitch scheduler is intentionally inactive | KEEP governed/deeper |
| Запустить канал | A - Operator Required | Lifecycle mutation requires operator/governance | KEEP |
| Приостановить канал | A - Operator Required | Lifecycle mutation requires operator/governance | KEEP |
| Сохранить policy/autopick settings | A - Operator Required | Admin configuration | KEEP settings/deeper |
| Переключить одного | A - Operator Required | Manual intervention | KEEP deeper |
| Delete / migrate and delete | A - Operator Required | Protected destructive lifecycle operation | KEEP protected/deeper |
| Проверить сервисы | B - Operator Optional | Background refresh exists/configured; manual accelerates proof | BACKGROUND ONLY on first screen; keep in details |
| Проверить one service | B - Operator Optional | Useful targeted refresh | KEEP in service details |
| Замерить скорость | B - Operator Optional | Manual live check accelerates complaint handling | KEEP in details |
| Проверить маршрут | C - Operator Irrelevant as button | No concrete safe channel-local handler; route is a status/read model | REMOVE as button / STATUS ONLY |
| Проверить готовность | C - Operator Irrelevant as raw button | Runtime readiness is calculated/read; remediation is separate | BACKGROUND ONLY |
| Stability validation | C - Operator Irrelevant | Continuous/background intelligence | BACKGROUND ONLY |
| History validation | C - Operator Irrelevant | Continuous/background intelligence | BACKGROUND ONLY |
| Recovery validation | C - Operator Irrelevant | Derived from events/snapshots | BACKGROUND ONLY |
| Trust evaluation | C - Operator Irrelevant | Planner/intelligence calculation | BACKGROUND ONLY |

## 11. Ideal Operator Model

Based on evidence, V7 should not expose validation mechanics as daily actions. The operator model should be:

Problem
↓
Meaning
↓
Resolution
↓
Existing safe action only when operator participation is real

| Visible To Operator | Hidden / Background |
|---|---|
| Human problem outcome | Service Matrix mechanics |
| Meaning in business language | Route validation internals |
| One real next action | Stability/history/recovery validators |
| Details/evidence on demand | Planner internals and raw blocker codes |
| Manual lifecycle/governed actions | Raw score calculation mechanics |

## 12. Final Recommendation

| Action / Class | Decision |
|---|---|
| Navigation and investigation | KEEP |
| Governed lifecycle changes | KEEP |
| User evacuation/manual switch | KEEP |
| Policy save / protected delete | KEEP protected/deeper |
| Service Matrix result | BACKGROUND ONLY on primary surfaces; manual refresh in details |
| Speed result | BACKGROUND/STATUS on primary surfaces; manual live measurement in details |
| Stability / history / recovery / trust | BACKGROUND ONLY |
| Runtime readiness | BACKGROUND ONLY unless a real remediation action exists |
| Route validation | REMOVE AS BUTTON / STATUS ONLY until safe channel-local handler exists |

Specific next UX guidance, not implementation:

| Current UI Language | Recommended Operator Language |
|---|---|
| Проверить сервисы | Сервисы требуют свежей проверки |
| Проверить маршрут | Маршрут не подтвержден |
| Stability validation required | Стабильность ниже требуемого уровня |
| History validation required | Недостаточно данных |
| Runtime validation required | Готовность канала не подтверждена |

## 13. Final Verdict

MIXED_MODEL

Reason: V7 already automates many validations and continuously derives channel truth, but it still needs operator/governed actions for lifecycle, user movement, policy changes, plan review, and protected execution. The first operator surface should keep real actions and demote duplicated/background validators to status or details.
