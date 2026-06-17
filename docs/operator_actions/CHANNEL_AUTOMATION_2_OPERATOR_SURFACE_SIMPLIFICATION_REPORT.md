# CHANNEL.AUTOMATION.2 Operator Surface Simplification

## 1. Reuse Audit

| Source | Reused | Result |
|---|---:|---|
| Existing channel table | Yes | First-line channel status now shows operator outcomes, not validation mechanics. |
| Existing channel drawer | Yes | Health problems remain in the same drawer and expand inline. |
| Existing service workspace | Yes | Service data remains available under the existing channel workspace. |
| Existing service matrix action | Yes | Manual refresh is retained in deeper service context only. |
| Existing problem accordion | Yes | Red problem rows remain the action entry point. |
| Existing why/reason copy paths | Yes | Reasons are human-readable on the operator surface. |
| Existing channel assignment/planner truth | Yes | No planner, score, eligibility, or assignment formula was changed. |
| Existing screenshots/Browser validation flow | Yes | Local visual validation used current code with a synthetic non-private fixture. |

No new page, drawer, workflow, endpoint, planner, governance path, execution path, database, storage, snapshot, validator, or automation was added.

## 2. Removed Validation Actions

| Old First-Line Exposure | New Operator Surface | Status |
|---|---|---|
| `Проверить сервисы` | `Сервисы` / `Открыть канал` / inline service outcome | Removed from first-line channel actions |
| `Проверить маршрут` | `Маршрут не подтвержден` | Converted to status/outcome |
| `Проверить готовность` | `Готовность канала не подтверждена` | Converted to status/outcome |
| `Запустить` in service workspace | `Обновить` | Reworded as manual refresh in details |
| Service failure as duplicated breakdown group | Per-service problem rows | Deduplicated |

Manual refresh still exists where it is honest: deeper service workspace or specific service detail. The first screen no longer asks the operator to run validators that already have background/read-model equivalents.

## 3. Service Matrix Changes

| Area | Change |
|---|---|
| Workspace tab | `Сервисная матрица` became `Сервисы` |
| Channel problem label | Service problems now describe service outcome/freshness |
| Attention layer action | Service problem opens the channel instead of presenting a raw service check |
| Service detail action | Manual service refresh is labeled `Обновить` |
| Empty/service stale states | Copy now says service data is unavailable or not confirmed |

The operator now sees service health as a business problem first. The validation mechanism is available only after opening service details.

## 4. Route Status Changes

| Old Surface | New Surface |
|---|---|
| `Проверить маршрут` | `Маршрут не подтвержден` |
| Route raw blocker language | Human route status |
| Detached route validation action | Details/status only unless a real safe handler exists |

No route formula or runtime route readiness logic was changed.

## 5. Stability Status Changes

| Old Surface | New Surface |
|---|---|
| Raw stability/check language | `Стабильность ниже требуемого уровня` |
| Validation-as-action | Status plus inline reason/resolution |

Stability remains background intelligence. The operator gets a problem statement, not an instruction to validate the validator.

## 6. History Status Changes

| Old Surface | New Surface |
|---|---|
| History/check mechanics | `Недостаточно данных` |
| Technical validation prompt | Details/evidence path |

History remains available in technical details and evidence.

## 7. Runtime Status Changes

| Old Surface | New Surface |
|---|---|
| `Проверить готовность` | `Готовность канала не подтверждена` |
| Runtime validation as button | Runtime status with logs/details |

Runtime readiness remains read-model driven. No new runtime action was created.

## 8. Deduplication Results

| Duplicate / Noise | Result |
|---|---|
| Failed service group plus individual failed services | Removed duplicate failed-service group |
| Multiple service-check entry points on first-line UX | Reduced to details/service workspace |
| Raw validator labels in problem rows | Replaced with operator outcomes |
| Ambiguous `Запустить` in service workspace | Replaced with `Обновить` |

## 9. Screenshots

Screenshots were captured from local `127.0.0.1:13011` using the current deployed code and a synthetic non-private channel fixture. Production Browser capture for `https://v7-admin.195-2-79-116.sslip.io` was blocked by Browser security policy, and broad production state copying was not used because it could transfer private runtime/user data.

| Screenshot | File |
|---|---|
| Desktop channels overview | `docs/operator_actions/channel_automation_2_screenshots/desktop-01-channels-overview.png` |
| Desktop channel drawer | `docs/operator_actions/channel_automation_2_screenshots/desktop-02-channel-drawer-vless.png` |
| Desktop service problem expanded | `docs/operator_actions/channel_automation_2_screenshots/desktop-03-service-problem-expanded.png` |
| Desktop services workspace | `docs/operator_actions/channel_automation_2_screenshots/desktop-04-services-workspace.png` |
| Mobile channels overview, 390px | `docs/operator_actions/channel_automation_2_screenshots/mobile-01-channels-overview-390.png` |
| Mobile channel drawer, 390px | `docs/operator_actions/channel_automation_2_screenshots/mobile-02-channel-drawer-390.png` |

## 10. Mobile Validation

| Check | Result |
|---|---|
| 390px viewport | PASS |
| Horizontal overflow | PASS, none detected |
| Drawer problem readability | PASS |
| Buttons clipped | PASS, none detected |
| Raw validation copy visible | PASS, none detected in inspected drawer/workspace |

Browser measurement: `scrollWidth=390`, `clientWidth=390`, `overflowX=false`.

## 11. Tests

| Test | Result |
|---|---|
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| Raw label search for first-line validation actions | PASS scoped; only legacy/i18n or unrelated execution-rehearsal strings remain |
| Desktop drawer opens | PASS |
| Red service problem expands inline | PASS |
| Services workspace renders | PASS |
| Service workspace row action says `Обновить` | PASS |
| Mobile 390px no overflow | PASS |
| Safe deploy | PASS, runtime fingerprint updated to `7f21806567b22fad8ece83fb7f7478e0f9c5c588` |

## 12. Remaining Issues

| Issue | Status |
|---|---|
| Production Browser screenshots | Blocked by Browser security policy for the authenticated production URL |
| Production state copy for screenshots | Not used; rejected as unsafe/private-data transfer risk |
| Legacy `Проверить сервисы` translation map entry | Remains as i18n/legacy phrase support, not as first-line operator action |
| Operator execution rehearsal wording | Out of scope; not channel health validation surface |

## 13. Final Verdict

`CHANNEL_OPERATOR_SURFACE_FINAL`

The channel operator surface now presents outcomes first: service problem, route status, runtime readiness, stability, history, and load. Validation mechanics are moved behind details or retained only as deeper manual refresh actions where a safe existing handler already exists.

