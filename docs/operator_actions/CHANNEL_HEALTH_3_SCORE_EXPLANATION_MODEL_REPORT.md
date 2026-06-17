# CHANNEL.HEALTH.3_SCORE_EXPLANATION_MODEL_REPORT

Date: 2026-06-18  
Branch: Updatesystem  
Production deploy: deploy-z8-14-Updatesystem-7cfac26-20260618T014614  
Final code commit: 7cfac268

## 1. Reuse Audit

| Source | Reused | Notes |
|---|---:|---|
| Existing channel suitability breakdown | Yes | Services, Stability, Capacity, Route, Runtime/Readiness, History reused. |
| Existing service matrix data | Yes | Services explanation uses current service matrix evidence. |
| Existing channel health state | Yes | Stability explanation uses existing `channelHealth(row)` diagnostics. |
| Existing capacity/load model | Yes | Capacity explanation uses current assigned user count and load limits. |
| Existing topology / route state | Yes | Route explanation uses current topology state, not a new route check. |
| Existing runtime readiness snapshot | Yes | Readiness explanation uses current runtime readiness snapshot. |
| Existing history / decision rows | Yes | History explanation uses existing channel decision/why-card state. |
| New storage / database / snapshot | No | None added. |
| New planner / governance / execution path | No | None added. |
| Score formula changes | No | No score weights or formula changed. |

## 2. Removed Action Language

Health Diagnostics now explains score only. The diagnostic section does not show resolution flow, action buttons, validator commands, or operator execution prompts.

| Removed From Health Diagnostics | Status |
|---|---:|
| `Проблема` / `Решение` / `Что делать` model | Removed |
| Refresh / Check / Open action buttons | Removed |
| Detached resolution panels | Removed |
| Raw action-oriented validator wording | Removed from verified score components |
| Score-changing logic | Not touched |

## 3. Services Explanation

Services component now answers why the services score is what it is:

| Evidence | Operator Text |
|---|---|
| Service matrix count | `13/14 сервисов доступны, остальные снизили балл.` |
| Expanded evidence | Available/unavailable service names are shown as evidence only. |
| Action model | None in diagnostics. |

Screenshot: `docs/operator_actions/channel_health_3_screenshots/desktop_services_expanded_openvpn.png`

## 4. Stability Explanation

Stability component now explains channel state without exposing raw internal codes.

| Raw Signal | Operator Text |
|---|---|
| `interface_down_or_missing` | `Интерфейс канала не поднят или не найден.` |
| Healthy channel | `Канал отвечает нормально, состояние выше минимального уровня.` |

No stability action is exposed inside Health Diagnostics.

## 5. Capacity Explanation

Capacity component explains load score using existing assigned users and limits:

| Channel | Evidence |
|---|---|
| awg3 | `8 пользователей; предпочтительный уровень 1. Нагрузка снизила балл.` |
| awg0 | `0 пользователей; предпочтительный уровень 1. Нагрузка внутри нормы.` |

Expanded view shows users, preferred limit, hard limit, and status. No move-user action appears in Health Diagnostics.

Screenshot: `docs/operator_actions/channel_health_3_screenshots/desktop_capacity_expanded_awg3.png`

## 6. Route Explanation

Route component now explains route score from the same topology signal used by the score.

| Channel | Evidence |
|---|---|
| awg3 | `Топология канала: лимит ёмкости. Этот сигнал снизил маршрутный компонент.` |
| OpenVPN-Kolosov | `Топология канала: сервисы не проходят. Этот сигнал снизил маршрутный компонент.` |

The previous confusing route explanation based only on confirmed route rows was removed from the score explanation path.

Screenshot: `docs/operator_actions/channel_health_3_screenshots/desktop_route_expanded_awg3.png`

## 7. History Explanation

History component remains diagnostic only:

| State | Explanation |
|---|---|
| Full score | `Недавняя история не содержит негативных сигналов.` |
| Partial score | Existing channel decision state is translated through operator text. |

No recovery, trust, or execution action is exposed in Health Diagnostics.

## 8. Screenshots

| Required Screenshot | File |
|---|---|
| Desktop table | `docs/operator_actions/channel_health_3_screenshots/desktop_channels_table.png` |
| Desktop 72 score | `docs/operator_actions/channel_health_3_screenshots/desktop_score_72_awg3.png` |
| Desktop 37 score | `docs/operator_actions/channel_health_3_screenshots/desktop_score_37_openvpn.png` |
| Desktop 92 score | `docs/operator_actions/channel_health_3_screenshots/desktop_score_92_awg0.png` |
| Services expanded | `docs/operator_actions/channel_health_3_screenshots/desktop_services_expanded_openvpn.png` |
| Route expanded | `docs/operator_actions/channel_health_3_screenshots/desktop_route_expanded_awg3.png` |
| Capacity expanded | `docs/operator_actions/channel_health_3_screenshots/desktop_capacity_expanded_awg3.png` |
| Mobile table | `docs/operator_actions/channel_health_3_screenshots/mobile_channels_table.png` |
| Mobile Health Diagnostics | `docs/operator_actions/channel_health_3_screenshots/mobile_health_diagnostics_awg3.png` |
| Mobile expanded component | `docs/operator_actions/channel_health_3_screenshots/mobile_component_expanded_awg3.png` |

## 9. Mobile Validation

| Check | Result |
|---|---:|
| 390px viewport used | PASS |
| Health Diagnostics readable | PASS |
| Expanded score component readable | PASS |
| Diagnostics horizontal overflow | PASS, none detected |
| Clipped diagnostics buttons | PASS, none detected |
| Action buttons inside diagnostics | PASS, none detected |
| Raw `interface_down_or_missing` visible | PASS, not visible |

## 10. Tests

| Test | Result |
|---|---:|
| `python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| `tools/v7-run-tests` | PASS, 447 tests OK |
| Production desktop diagnostics render | PASS |
| Production mobile diagnostics render | PASS |
| No action buttons in diagnostics | PASS |
| No `Что делать` / `Решение` / `Проблема:` inside diagnostics | PASS |
| Score explanation visible | PASS |
| No diagnostics overflow at 390px | PASS |
| Console/runtime blockers observed | PASS, none observed in validation path |

Known pre-existing warning during tests: Python emits `DeprecationWarning: invalid escape sequence \d` from the existing HTML string. This was not introduced by this task.

## 11. Remaining Issues

No remaining blockers in Health Diagnostics.

Out of scope: the broader channel drawer still contains operator checklist and detail sections outside Health Diagnostics. CHANNEL.HEALTH.3 only demotes Health Diagnostics into score explanation and does not redesign the whole drawer.

## 12. Final Verdict

HEALTH_DIAGNOSTICS_COMPLETE

Health Diagnostics now answers only: why this score. It reuses existing signals, exposes component score evidence, removes action/resolution language, keeps planner/governance/execution untouched, and has production screenshots for desktop and mobile validation.
