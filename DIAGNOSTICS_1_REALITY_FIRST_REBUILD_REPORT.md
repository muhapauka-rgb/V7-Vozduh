# DIAGNOSTICS.1 Reality-First Rebuild Report

Project: V7 VOZDUH  
Program: DIAGNOSTICS.1_REALITY_FIRST_REBUILD  
Date: 2026-06-19  
Implementation commit: 46f747eefc83cf0febaf7a48a607e01e421c8deb

## 1. Diagnostics Source Map

| Diagnostic Area | Existing Source Reused | Display Surface | Changed? |
|---|---|---|---|
| Services | service matrix evidence, `channelScoreServiceEvidence`, `channelSuitabilityServices` | Channel diagnostics / health details | Display language only |
| Stability | channel lifecycle / health state, `channelSuitabilityStability` | Channel diagnostics / health details | Display language only |
| Capacity / Load | `egressUserCount`, `channelLoadLimit`, `channelSuitabilityCapacity` | Channel diagnostics / health details | Display language only |
| Route | topology readiness, route evidence, `channelSuitabilityRoute` | Channel diagnostics / health details | Display language only |
| Runtime | runtime readiness snapshot, `channelSuitabilityRuntime` | Channel diagnostics / health details | Display language only |
| History | channel decision history / trust evidence, `channelSuitabilityHistory` | Channel diagnostics / health details | Display language only |

No planner, assignment, governance, execution, capacity, route, or score formula changes were made.

## 2. Legacy Score-First Surface Report

The diagnostics layer previously explained technical condition through point math:

| Legacy Pattern | Status |
|---|---|
| Component score / max inside diagnostics | Removed from diagnostics |
| Lost points / penalty wording | Removed from diagnostics |
| "Снизили балл" / "частичный балл" wording | Removed from diagnostics |
| Total diagnostic score as the diagnostic conclusion | Removed from diagnostics |
| Explanation focused on why a score happened | Replaced with what is happening in reality |

Remaining score surface:

| Surface | Status | Reason |
|---|---|---|
| Channel table score pill such as `92/100` | Kept outside diagnostics | This is a secondary channel score surface, not the diagnostic explanation. The prompt prohibited formula and score changes. |

## 3. Reality-First Conversion

Diagnostics now explain observed reality first:

| Area | New Operator Explanation |
|---|---|
| Services | Which services are working, unavailable, or require a fresh check |
| Stability | Whether the channel/interface appears stable enough to trust |
| Capacity | How many users are assigned, what the preferred level is, and whether new assignments are restricted |
| Route | Whether route readiness/topology confidence is confirmed; explicitly not speed or bandwidth |
| Runtime | Whether the current runtime snapshot is fresh and usable |
| History | Whether recent history supports confidence in the channel |

## 4. Health Rebuild

Technical health remains diagnostics-only. The visible diagnostics section now starts from:

`Техническая диагностика` -> `Реальность канала`

It no longer leads with score contribution, point loss, or component math. The operator sees practical state labels such as `OK`, `Проблема`, and `Проверить`, followed by reason and operator meaning.

## 5. Capacity Rebuild

Capacity follows ADR-009 semantics:

| Required Meaning | Implemented |
|---|---|
| Capacity is assigned-user load | Yes |
| Capacity is not bandwidth | Yes |
| Preferred level and hard limit are visible | Yes |
| Current users are not implied to be disconnected | Yes |
| New assignments may be restricted | Yes |

Observed production text in diagnostics:

`11 пользователей назначено; жёсткий предел 2. Новые назначения ограничены, текущие пользователи не отключаются.`

## 6. Route Rebuild

Route diagnostics now describe readiness confidence and topology state. They do not describe traffic quality, speed, or bandwidth.

Observed production text in diagnostics:

`Готовность маршрута частичная: лимит ёмкости. Это не оценка скорости или пропускной способности.`

## 7. Services Rebuild

Services diagnostics now explain real service condition:

| Signal | Operator Meaning |
|---|---|
| Working services | Services currently confirmed available |
| Unavailable services | Services that block normal confidence |
| No fresh data | Operator must refresh the service matrix |
| Partial services | Channel needs service verification before trust |

## 8. Diagnostics Test

Reality-first validation was run against the live production admin.

| Check | Result |
|---|---|
| Diagnostics contains score fraction | PASS: false |
| Diagnostics contains Russian score-first language | PASS: false |
| Diagnostics contains reality header | PASS: true |
| Console errors during capture | PASS: none |
| Mobile horizontal overflow at 390px | PASS: false |

Evidence file:

`docs/diagnostics_1/screenshots/capture_audit.json`

## 9. Screenshots

Captured real production screenshots:

| Screenshot | File |
|---|---|
| Desktop diagnostics opened | `docs/diagnostics_1/screenshots/desktop_diagnostics_vless.png` |
| Desktop diagnostics expanded | `docs/diagnostics_1/screenshots/desktop_diagnostics_expanded_vless.png` |
| Mobile 390 diagnostics expanded | `docs/diagnostics_1/screenshots/mobile_diagnostics_vless_390.png` |

Required live examples not available at capture time:

| Required Example | Capture Status | Reason |
|---|---|---|
| Use channel | Not captured | Live production table had no `Use` rows |
| Evacuate channel | Not captured | Live production table had no `Evacuate` rows |
| Emergency channel | Not captured | Live production table had no `Emergency Only` rows |
| Diagnostics expanded | Captured | `vless` blocked channel was available |

No synthetic screenshots were created.

## 10. Canonical Update

| File | Update |
|---|---|
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Added reality-first diagnostics rule for Channel Score, Technical Health, and Channel Operator Signal Model |
| `docs/reference/SYSTEM_MAP.md` | Updated Channel Score / Technical Health and Channel Operator Signal Model entries |
| `docs/decisions/ADR-010-diagnostics-reality-first-model.md` | Created accepted ADR for reality-first diagnostics |

## 11. Tests

| Test | Result |
|---|---|
| Mandatory truth gate before implementation | PASS |
| Mandatory convergence gate before implementation | PASS |
| `python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| Safe deploy | PASS |
| Production screenshot capture | PASS, with live-data limitation |
| Diagnostics score-language audit | PASS |
| Mobile 390 overflow audit | PASS |

## 12. Remaining Issues

| Issue | Impact |
|---|---|
| Production dataset had only blocked channels during screenshot capture | Required Use/Evacuate/Emergency examples could not be visually proven without fabricating state |
| Channel score pill remains in table outside diagnostics | Intentional: score formula and score surface outside diagnostics were not changed |

## 13. Final Verdict

CONDITIONAL_PASS

Reality-first diagnostics are implemented, deployed, and validated on live production UI. The remaining condition is visual evidence coverage: Use, Evacuate, and Emergency channel examples were not present in the live dataset at capture time, so only the available blocked-channel diagnostics could be captured honestly.
