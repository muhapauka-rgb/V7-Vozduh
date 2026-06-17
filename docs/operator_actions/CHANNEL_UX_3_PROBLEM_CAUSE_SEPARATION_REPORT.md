# CHANNEL.UX.3 Problem / Cause Separation

## 1. Cause Inventory

| First-Layer Candidate | Classification | Final Placement |
|---|---|---|
| Route not confirmed / `Маршрут не подтвержден` | Cause | Expanded problem detail / technical breakdown only |
| Services require fresh verification | Cause | Expanded detail / services workspace only |
| Runtime readiness not confirmed | Cause | Technical health detail only |
| History validation / insufficient history | Cause | Technical health detail only |
| Trust / recovery validation states | Cause | Technical / evidence detail only |
| Stability below required level | Cause | Technical health detail only |
| Validator/measured/refresh-required language | Cause | Hidden from first-layer problem list |

## 2. Outcome Inventory

| Operator Outcome | First Layer |
|---|---:|
| YouTube unavailable | Yes |
| ChatGPT unavailable | Yes |
| Instagram unavailable | Yes |
| Telegram unavailable | Yes |
| WhatsApp unavailable | Yes |
| Google unavailable | Yes |
| Channel overloaded | Yes |
| Channel disabled | Yes |
| Channel not started | Yes |

## 3. Removed First-Layer Causes

The channel model now builds first-layer `Problems` from operator-visible outcomes only. Internal causes are filtered out before the drawer and main issue surfaces are rendered.

| Removed From First Layer | Still Available |
|---|---|
| `Маршрут не подтвержден` | Cause inside expanded outcome and technical breakdown |
| `Готовность канала не подтверждена` | Technical health detail |
| `Недостаточно данных` | Technical health detail |
| `Стабильность ниже требуемого уровня` | Technical health detail |
| `Сервисы требуют свежей проверки` | Services detail / technical breakdown |

If a channel has a low score but no user-visible outcome, the first layer does not invent a problem. It shows technical health and keeps causes behind details.

## 4. Service Matrix Cleanup

Service failures are shown as affected services:

| Service State | First Layer | Cause After Expansion |
|---|---|---|
| YouTube failed | `YouTube недоступен` | Route/service/runtime cause, depending on current signals |
| ChatGPT failed | `ChatGPT недоступен` | Route/service/runtime cause |
| Services not measured | Hidden from first-layer problems | Technical detail only |
| Services require refresh | Hidden from first-layer problems | Services workspace only |

The service matrix still runs and remains reachable. No validator or automation behavior changed.

## 5. Route Cleanup

Route is no longer rendered as a first-layer problem. In the validated service-failure scenario:

| Layer | Text |
|---|---|
| First-layer problem | `YouTube недоступен` |
| Expanded cause | `Маршрут не подтвержден` |
| Resolution | Open service/details path |

This matches the required `Problem -> Cause -> Resolution` model.

## 6. Screenshots

Screenshots were captured from local `127.0.0.1:13011` using current code and a synthetic non-private fixture.

| Scenario | File |
|---|---|
| Desktop service failure expanded | `docs/operator_actions/channel_ux_3_screenshots/desktop-01-service-failure-expanded.png` |
| Desktop good channel | `docs/operator_actions/channel_ux_3_screenshots/desktop-02-good-channel-awg0.png` |
| Desktop overloaded channel | `docs/operator_actions/channel_ux_3_screenshots/desktop-03-overloaded-channel-awg3.png` |
| Desktop service failure collapsed | `docs/operator_actions/channel_ux_3_screenshots/desktop-04-service-failure-vless.png` |
| Mobile drawer 390px | `docs/operator_actions/channel_ux_3_screenshots/mobile-01-drawer-vless-390.png` |
| Mobile expanded problem 390px | `docs/operator_actions/channel_ux_3_screenshots/mobile-02-expanded-problem-390.png` |

## 7. Mobile Validation

| Check | Result |
|---|---|
| 390px drawer readable | PASS |
| Expanded problem readable | PASS |
| Horizontal overflow | PASS, `overflowX=false`, `scrollWidth=390`, `clientWidth=390` |
| Cause hidden from first-layer list | PASS |
| Cause visible after expansion | PASS |

## 8. Tests

| Test | Result |
|---|---|
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| Desktop good channel | PASS, no first-layer Problems block |
| Desktop overloaded channel | PASS, shows `YouTube недоступен` and `Канал перегружен` only |
| Desktop service failure channel | PASS, shows service outcomes only |
| Expanded service problem | PASS, cause appears inside expansion |
| No route problem in first layer | PASS |
| No validator problem in first layer | PASS |
| Browser console errors | PASS, none captured |
| Mobile no overflow | PASS |

## 9. Remaining Issues

| Issue | Status |
|---|---|
| Technical breakdown still contains causes | Expected; this is the correct deeper layer |
| Good fixture channel scores 88/100 because technical causes may remain | Expected; no user-visible problem is invented |
| Production Browser capture | Not used; local screenshots use current code with non-private fixture |

## 10. Final Verdict

`CHANNEL_OPERATOR_MODEL_COMPLETE`

The channel drawer now separates:

Problem: user-visible outcome  
Cause: internal diagnosis  
Resolution: operator path

First-layer Problems contain only outcomes. Route, runtime, history, stability, trust/recovery, and validator states are not shown as peer problems.

