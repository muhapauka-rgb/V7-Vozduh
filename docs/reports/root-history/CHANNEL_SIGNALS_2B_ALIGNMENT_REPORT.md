# CHANNEL.SIGNALS.2B Decision Signal Alignment Report

## 1. Current Contradiction

Production previously allowed an operator-facing contradiction:

| Decision | First-Level Signal | Problem |
| --- | --- | --- |
| `Использовать` | red diagnostic badge | Operator could read the channel as both usable and broken. |

The contradiction came from display severity, not planner truth. Channel Decision V7 remained the assignment source; Channel Score / Technical Health remained diagnostic.

## 2. Reference-First Review

Read before implementation:

| Source | Result |
| --- | --- |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Channel Decision V7 is assignment truth; score/health are diagnostics. |
| `docs/decisions/ADR-002-channel-score-is-mixed-score.md` | Score is mixed and must not become the planner. |
| `docs/decisions/ADR-007-channel-signal-semantics-correction.md` | First-level signals must explain the decision. |
| `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md` | Remaining issue: possible `Use` + red signal mismatch. |

## 3. Decision Signal Rule

Implemented operator-display rule:

| Decision | First-Level Red Allowed? | Meaning |
| --- | --- | --- |
| `Использовать` | No | Diagnostics may show warning, but not red contradiction. |
| `Оставить` | No | Current users can stay; warning may explain limitation. |
| `Перевести` | Yes | Red matches required movement/action. |
| `Аварийно` | No for role/capacity diagnostics | Emergency role is already the decision; warning is enough unless planner exposes a critical blocker. |
| `Запрещён` | Yes | Red matches block. |

## 4. Implementation

Changed only `admin/v7-admin-api` display helpers:

| Function | Change |
| --- | --- |
| `channelDecisionAlignedSignalTone` | Downgrades raw `bad` to `warn` for `use`, `keep`, and `emergency` first-level display. |
| `channelSignalDecisionNote` | Adds tooltip text explaining that the diagnostic signal does not block the visible planner decision. |
| `channelSignalSummary` | Keeps `rawTone`, uses aligned `tone`, and sorts/filters by visible operator severity. |

No planner, governance, execution, score formula, capacity model, storage, or truth source changed.

## 5. Live Production Validation

Production capture after deploy `deploy-z8-14-Updatesystem-2859c0e-20260618T233217`.

| Case | Live Example | Result |
| --- | --- | --- |
| Use | `awg3`, `awg0` | PASS: no red first-level signals. |
| Keep Current Users | Not present in live data | Not captured; no synthetic state created. |
| Evacuate | `vless` | PASS: red `Нагрузка` remains because decision is `Перевести`. |
| Emergency | `wg гермашка`, `1`, `OpenVPN-Kolosov`, `amneziawg-exec...` | PASS: role/capacity diagnostics are warning/ok, not contradictory red. |

Validation summary:

| Check | Result |
| --- | --- |
| `Use + redSignals` | `[]` |
| Desktop states found | `evacuate=1`, `use=2`, `emergency=4` |
| Mobile horizontal overflow | `false` (`scrollWidth=390`, `innerWidth=390`) |

## 6. Screenshots

| Screenshot | Path |
| --- | --- |
| Desktop table | `docs/channel_signals_2b/screenshots/desktop_channels_table.png` |
| Desktop Use tooltip | `docs/channel_signals_2b/screenshots/desktop_use_tooltip.png` |
| Desktop Evacuate tooltip | `docs/channel_signals_2b/screenshots/desktop_evacuate_tooltip.png` |
| Desktop Emergency tooltip | `docs/channel_signals_2b/screenshots/desktop_emergency_tooltip.png` |
| Mobile table 390px | `docs/channel_signals_2b/screenshots/mobile_channels_table_390.png` |
| Mobile Use tooltip 390px | `docs/channel_signals_2b/screenshots/mobile_use_tooltip_390.png` |
| Mobile Emergency tooltip 390px | `docs/channel_signals_2b/screenshots/mobile_emergency_tooltip_390.png` |
| Machine summary | `docs/channel_signals_2b/screenshots/validation_summary.json` |

## 7. Tests

| Test | Status |
| --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| `tools/v7-run-tests` | PASS, 447 tests |
| `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json` | PASS |
| Production screenshot capture | PASS |

## 8. Remaining Issues

| Issue | Status |
| --- | --- |
| Keep Current Users screenshot | Not available in current production data. |
| Raw diagnostics vs assignment | Preserved: raw diagnostic reason remains in tooltip/details. |

## 9. Final Verdict

DECISION_SIGNAL_ALIGNED
