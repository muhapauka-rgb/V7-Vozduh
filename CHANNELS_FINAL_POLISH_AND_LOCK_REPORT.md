# CHANNELS.FINAL.POLISH_AND_LOCK Report

Date: 2026-06-19
Branch: Updatesystem
Implementation commits: `fba3c993`, `c2ddc3d1`
Production deploy id: `deploy-z8-14-Updatesystem-c2ddc3d-20260619T185759`

## 1. Scope

Finished the Channel operator surface polish without changing planner, assignment truth, governance, execution, route formula, capacity formula, signal model, or score formula.

The work was limited to operator wording, final UI loading semantics, diagnostics language, and visual validation.

## 2. Problems Fixed

| Problem | Fixed | Evidence |
|---|---:|---|
| Vague `Требует проверки` / `Нужна проверка` on Channels operator surface | Yes | Final capture `badText: []` |
| Route looked like broken speed/quality/bandwidth | Yes | Diagnostics say route readiness/confidence and explicitly not speed/capacity |
| Capacity looked like internet overload | Yes | Diagnostics explain assigned users, hard limit, new assignment restriction, current users not disconnected |
| Mobile could show false `Запрещён` before assignment truth loaded | Yes | Added transient `Загрузка решения`; final capture `loadingDecisionVisible: false` |
| Minimal signal legend missing | Yes | Legend visible in desktop and mobile |
| Diagnostics used score/penalty language | Yes | Final diagnostics are reality-first component states |

## 3. Reuse Audit

| Area | Reused |
|---|---:|
| Existing Channels table | Yes |
| Existing Channel Drawer | Yes |
| Existing assignment truth adapter | Yes |
| Existing planner/read model | Yes |
| Existing channel signal dots | Yes |
| Existing technical diagnostics drawer | Yes |
| Existing safe deploy/truth tooling | Yes |

No new page, drawer, planner, execution path, storage, score formula, or signal model was created.

## 4. Terminology Lock

| Old / Confusing | Final Operator Wording |
|---|---|
| Требует проверки | Уверенность неполная / Уточнить / Нет свежего подтверждения |
| Нужна проверка | Нет свежих данных / Нет свежего подтверждения |
| Канал перегружен | Лимит назначений достигнут |
| Маршрут не подтвержден | Маршрутная готовность не подтверждена |
| Route broken by score | Готовность маршрута частичная; это не оценка скорости или пропускной способности |
| Score penalty / points lost | Reality-first component status |

`Загрузка решения` is allowed only as a transient loading state before assignment truth arrives. It is not a planner decision and is not counted as `Blocked`.

## 5. Decision Labels

| Decision | Final Table Label |
|---|---|
| Use | Использовать |
| Evacuate | Перевести |
| Emergency Only | Только аварийно |
| Blocked | Запрещён |
| Keep Current Users | Оставить текущих |

`Blocked` and `Keep Current Users` were not present as live production examples during final capture.

## 6. Screenshots

| Evidence | File |
|---|---|
| Desktop table | `docs/channels_final/screenshots/desktop_channels_table.png` |
| Desktop Use drawer | `docs/channels_final/screenshots/desktop_use_awg3_drawer.png` |
| Desktop Evacuate drawer | `docs/channels_final/screenshots/desktop_evacuate_vless_drawer.png` |
| Desktop Emergency drawer | `docs/channels_final/screenshots/desktop_emergency_wg_germashka_wireguard-1779454504-c43409_drawer.png` |
| Desktop Diagnostics expanded | `docs/channels_final/screenshots/desktop_diagnostics_expanded_vless.png` |
| Mobile table | `docs/channels_final/screenshots/mobile_channels_table.png` |
| Mobile Use drawer | `docs/channels_final/screenshots/mobile_use_vless_drawer.png` |
| Mobile Evacuate drawer | `docs/channels_final/screenshots/mobile_evacuate_awg3_drawer.png` |
| Mobile Emergency drawer | `docs/channels_final/screenshots/mobile_emergency_wg_germashka_wireguard-1779454504-c43409_drawer.png` |
| Mobile Diagnostics expanded | `docs/channels_final/screenshots/mobile_diagnostics_expanded_awg3.png` |
| Machine audit | `docs/channels_final/screenshots/capture_audit.json` |

## 7. Visual Validation

| Check | Desktop | Mobile |
|---|---:|---:|
| Use visible | Pass | Pass |
| Evacuate visible | Pass | Pass |
| Emergency visible | Pass | Pass |
| Blocked visible | Not available in live data | Not available in live data |
| Keep visible | Not available in live data | Not available in live data |
| Signal legend visible | Pass | Pass |
| Old confusing wording absent | Pass | Pass |
| Loading state absent after settled render | Pass | Pass |
| No horizontal overflow | Pass | Pass |
| Console errors | 0 | 0 |

## 8. Operator Walkthrough

| Question | Answered |
|---|---:|
| What does V7 want? | Yes: decision column is primary |
| Why? | Yes: signals and drawer reason explain cause |
| What should operator do? | Yes: drawer action text follows assignment truth |
| Is it speed/bandwidth? | Yes: diagnostics explicitly avoid that interpretation |
| Is capacity breaking current users? | Yes: current users are not automatically disconnected |

## 9. Canonical Lock

Updated:

| File | Update |
|---|---|
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Locked final channel wording, route/capacity semantics, transient loading state |
| `docs/reference/SYSTEM_MAP.md` | Linked Channels final polish report |
| `docs/decisions/ADR-010-diagnostics-reality-first-model.md` | Locked diagnostics language against score/penalty/check wording |

## 10. Tests Run

| Test | Result |
|---|---:|
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| Playwright desktop capture | PASS |
| Playwright mobile 390 capture | PASS |
| Mobile overflow audit | PASS |
| Console error audit | PASS |
| `tools/v7-truth-check --all --json` after deploy | PASS |
| `tools/v7-convergence-status --json` after deploy | PASS |

## 11. Remaining Issues

| Issue | Impact |
|---|---|
| No live `Blocked` channel during final capture | Cannot provide real production screenshot for that state without mutating data |
| No live `Keep Current Users` channel during final capture | Same evidence gap |
| `vless` / `awg3` assignment changed between sequential desktop and mobile page loads | UI reflects live assignment truth, but planner/read-model volatility should be audited separately if it continues |

## 12. Final Verdict

CONDITIONAL_PASS

Reason: Channel UI polish is implemented, deployed, and visually validated on desktop/mobile for available live states. Full `CHANNELS_COMPLETE` is withheld because live production did not provide `Blocked` / `Keep Current Users` examples, and assignment truth changed between sequential screenshot loads.
