# CHANNEL.DECISION_FIRST.2_DRAWER_REBUILD Report

Date: 2026-06-19  
Branch: Updatesystem  
Implementation commit: bc088803  
Program verdict: DRAWER_DECISION_FIRST_IMPLEMENTED

## 1. Reuse Audit

| Source | Reused | Notes |
|---|---:|---|
| V7 Canonical Reference | Yes | Reference-first rule followed before implementation. |
| ADR-002 Channel Score | Yes | No score or formula changes. |
| ADR-003 Health Diagnostics | Yes | Diagnostics are last, not first-screen operator truth. |
| ADR-004 Channel Drawer | Yes | Drawer remains the primary operator surface. |
| ADR-006 Channel Decision V7 | Yes | Drawer now starts from V7 decision. |
| ADR-007 Decision-First Channel Surface | Yes | Decision, reason, signals, problems, works, diagnostics order implemented. |
| ADR-009 Channel Operator Signal Model | Yes | First-screen signals limited to Services, Load, Runtime, Stability when available. |
| Existing channel drawer | Yes | No new page, drawer, workflow, storage, planner, or truth source. |
| Existing problem accordion | Yes | Active problems use the existing inline Problem -> Cause -> Resolution behavior. |
| Existing diagnostics content | Yes | Technical health, score breakdown, route, history, evidence, logs, execution context, and service matrix remain under Diagnostics. |

## 2. Implemented Drawer Structure

Final top-to-bottom Channel Drawer structure:

1. Решение V7
2. Почему
3. Сигналы
4. Проблемы
5. Работает
6. Диагностика

Nothing is rendered above the Decision block except the drawer object header. The first screen is now decision-first instead of health/score-first.

## 3. Decision Block

| Decision | Operator Meaning |
|---|---|
| Использовать | Назначать новых пользователей на этот канал. |
| Перевести пользователей | Подготовить перевод пользователей с канала. |
| Аварийно | Использовать только как ручной резерв. |
| Запрещён | Не назначать пользователей на этот канал. |

No planner, assignment, governance, execution, score, route, or capacity semantics were changed. The drawer only exposes the existing decision truth earlier and more clearly.

## 4. Reason Block

The Reason block is one operator sentence. It uses the existing assignment blocker / recommendation explanation and keeps technical details out of Screen 1.

Examples captured:

| Channel | Reason |
|---|---|
| awg0 | Канал можно использовать |
| vless | Назначение заблокировано |
| wg гермашка, работает | Ручной резерв |

## 5. Signal Model

First-screen Signals are compact operator support only:

| Signal | First Screen Meaning | Diagnostics Kept? |
|---|---|---:|
| Сервисы | Service availability is OK or needs check | Yes |
| Нагрузка | Load/capacity is OK or needs check | Yes |
| Runtime | Runtime readiness is OK or needs check | Yes |
| Стабильность | Stability is OK or needs check when evidence exists | Yes |

No score breakdown, raw health details, route evidence, service matrix rows, logs, or execution context are shown inside Signals.

## 6. Problem Flow

Active problems remain clickable inline:

Problem  
↓  
Cause  
↓  
Resolution

Captured example:

| Channel | Problem | Inline Flow |
|---|---|---|
| vless | Канал перегружен | Problem, Cause, Resolution shown directly under the row. |

No detached panel, new page, or separate solution area was added.

## 7. Diagnostics Placement

Diagnostics are last and collapsed by default. They contain the existing technical material:

- Technical Health
- score breakdown
- Route
- History
- Evidence
- Logs
- Execution context
- Service matrix details

This preserves engineering visibility while keeping the operator first screen focused on what V7 wants.

## 8. Screenshot Gallery

| Scenario | Screenshot |
|---|---|
| Desktop table | `docs/channel_decision_first_2/screenshots/desktop_table.png` |
| Desktop Use | `docs/channel_decision_first_2/screenshots/desktop_use_awg0.png` |
| Desktop Evacuate | `docs/channel_decision_first_2/screenshots/desktop_evacuate_vless.png` |
| Desktop Emergency | `docs/channel_decision_first_2/screenshots/desktop_emergency_wg.png` |
| Desktop Blocked | `docs/channel_decision_first_2/screenshots/desktop_blocked_vless.png` |
| Desktop problem expanded | `docs/channel_decision_first_2/screenshots/desktop_problem_expanded_vless.png` |
| Desktop diagnostics expanded | `docs/channel_decision_first_2/screenshots/desktop_diagnostics_expanded_wg.png` |
| Mobile table 390 | `docs/channel_decision_first_2/screenshots/mobile_table_390.png` |
| Mobile Evacuate 390 | `docs/channel_decision_first_2/screenshots/mobile_evacuate_vless_390.png` |
| Mobile Diagnostics 390 | `docs/channel_decision_first_2/screenshots/mobile_diagnostics_vless_390.png` |
| Capture audit | `docs/channel_decision_first_2/screenshots/capture_audit.json` |

Screenshot caveat: a fresh Mobile Use drawer screenshot was not available at final capture time because the live production dataset had no `Использовать` row; all rows were `Запрещён`. The existing Desktop Use screenshot was captured earlier from real production when `awg0` was usable. No synthetic data was used.

## 9. Mobile Validation

| Screen | Width | Overflow | Result |
|---|---:|---:|---|
| Table | 390 | No | PASS |
| Evacuate drawer | 390 | No | PASS |
| Diagnostics drawer | 390 | No | PASS |
| Use drawer | 390 | Not recaptured | Live Use scenario unavailable at final capture |

The responsive drawer layout uses one-column signal cards on mobile. Captured mobile evidence shows no horizontal overflow and no clipped action controls.

## 10. Tests

| Check | Result |
|---|---|
| Pre-implementation truth-check | PASS |
| Pre-implementation convergence-status | PASS |
| Python compile | PASS |
| Diff whitespace check | PASS |
| Drawer renders | PASS via production screenshots |
| Problem inline expansion | PASS via `desktop_problem_expanded_vless.png` |
| Diagnostics last and expandable | PASS via `desktop_diagnostics_expanded_wg.png` and `mobile_diagnostics_vless_390.png` |
| Duplicate first-screen diagnostics blocks | PASS |
| Mobile overflow | PASS for captured mobile states |
| Console errors | PASS, no console errors recorded in capture audit |
| Post-deploy truth-check | PASS, FULLY_ALIGNED at implementation commit |
| Post-deploy convergence-status | PASS, ALIGNED at implementation commit |

## 11. Remaining Issues

| Issue | Impact | Follow-up |
|---|---|---|
| Mobile Use screenshot unavailable at final capture | Evidence gap only; production had no live Use row during final capture | Recapture when planner exposes a live Use channel again. |
| Live channel states changed during capture window | Screenshot names must be read with capture audit | Capture audit records actual live conditions. |

## 12. Final Verification State

| Area | Status |
|---|---|
| Logic changes | None |
| UI changes | Channel Drawer only |
| Planner changes | None |
| Assignment changes | None |
| Governance changes | None |
| Execution changes | None |
| New storage | None |
| New truth source | None |
| Runtime deployment | Completed for implementation commit bc088803 |

## 13. Final Verdict

DRAWER_DECISION_FIRST_IMPLEMENTED

Channel Drawer now uses the approved Decision-First order and keeps diagnostics behind the operator decision surface. The only remaining gap is a screenshot availability gap for Mobile Use caused by current live production state, not by missing UI implementation.
