# CHANNELS.OPERATOR_ENGINEER_SEPARATION Report

Date: 2026-06-19
Commit: `3fcae441`
Runtime deploy: `deploy-z8-14-Updatesystem-3fcae44-20260619T223600`

## 1. Reference First

Read before implementation:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-006-channel-operator-signal-model.md`
- `docs/decisions/ADR-007-channel-signal-semantics-correction.md`
- `docs/decisions/ADR-009-capacity-and-health-semantics.md`
- `docs/decisions/ADR-010-diagnostics-reality-first-model.md`
- `CHANNELS_FINAL_UX_CLOSE_ONE_PASS_REPORT.md`
- `CHANNELS_FINAL_ACTIONABILITY_AND_DENSITY_REPORT.md`

Stable conclusion reused: Channel Decision V7 is primary; Channel Score and Technical Health are diagnostics, not operator truth.

## 2. Current Drawer Audit

| Item | Previous Placement | Classification | Action |
| --- | --- | --- | --- |
| Channel name | First screen header | Operator | Kept |
| `score/100` | First screen header | Engineer | Removed from operator surface |
| Technical health/status pill | First screen header | Engineer | Removed from operator surface |
| V7 decision | First screen | Operator | Kept |
| One-sentence reason | First screen | Operator | Kept |
| S/L/R/T signals | First screen | Operator support | Kept compact |
| Problems accordion | First screen | Operator | Kept actionable |
| Works/confirmed block | First screen | Mixed/duplicate | Removed from first screen |
| Diagnostics entry | First screen | Boundary | Renamed to engineer boundary |
| Evidence/history/service matrix/details | Collapsed diagnostics | Engineer | Kept behind diagnostics |

## 3. Operator Surface

Final first-screen order:

1. Channel
2. Decision V7
3. Reason
4. Signals
5. Problems
6. Engineer diagnostics entry

Removed from first screen:

- `score/100`
- technical health/rating
- confidence labels
- raw technical state
- evidence/history/logs
- service matrix details
- duplicate confirmed/works block

## 4. Engineer Surface

Engineer diagnostics remain available through the existing drawer path:

- drawer header `Диагностика`
- first-screen `Открыть инженерную диагностику`
- collapsed `Инженерная диагностика`

Diagnostics still expose technical state, score inputs, service evidence, route/capacity/runtime/history details, settings, and existing safe actions. No planner, governance, formula, storage, endpoint, execution, or truth source changed.

## 5. Language Cleanup

| Previous Wording | New Wording |
| --- | --- |
| `route-handler` | `безопасное действие для маршрута` |
| `governed flow` | `штатное действие V7` |
| `runtime-снимок` | `подтверждение готовности` |
| `snapshot` on operator problem | `последние данные` |
| `нет безопасного обработчика` | `нет безопасного действия в этом окне` |

## 6. Screenshots

| Scenario | Channel | Screenshot |
| --- | --- | --- |
| Desktop Use / Operator | `awg0` | `docs/channels_operator_engineer_separation/screenshots/desktop_use_operator.jpg` |
| Desktop Evacuate / Operator | `vless` | `docs/channels_operator_engineer_separation/screenshots/desktop_evacuate_operator.jpg` |
| Desktop Emergency / Operator | `1` | `docs/channels_operator_engineer_separation/screenshots/desktop_emergency_operator.jpg` |
| Desktop Engineer Diagnostics | `vless` | `docs/channels_operator_engineer_separation/screenshots/desktop_engineer_diagnostics.jpg` |
| Mobile 390 / Operator | `vless` | `docs/channels_operator_engineer_separation/screenshots/mobile_operator_390.jpg` |
| Mobile 390 / Engineer Diagnostics | `vless` | `docs/channels_operator_engineer_separation/screenshots/mobile_engineer_diagnostics_390.jpg` |

Audit file: `docs/channels_operator_engineer_separation/screenshots/capture_audit.json`.

## 7. Operator Test

| Question | Result |
| --- | --- |
| What does V7 want? | Visible in `Решение V7` |
| Why? | Visible in `Почему` |
| What should operator do? | Visible in decision text / actionable problem |
| Can operator answer without diagnostics? | PASS |
| Is `score/100` visible on operator surface? | NO |
| Is technical state visible on operator surface? | NO |

## 8. Engineer Test

| Question | Result |
| --- | --- |
| Can engineer open diagnostics from drawer? | PASS |
| Can engineer see technical health/score inputs? | PASS |
| Can engineer inspect service/capacity/route/runtime/history details? | PASS |
| Is diagnostics separate from operator surface? | PASS |

## 9. Mobile Review

| Screen | Result |
| --- | --- |
| Operator 390px | PASS, no horizontal overflow observed in screenshot |
| Engineer diagnostics 390px | PASS, diagnostics opens in same drawer and remains scrollable |

## 10. Tests

| Check | Result |
| --- | --- |
| Python compile | PASS: `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` |
| Diff whitespace | PASS: `git diff --check` |
| Safe deploy | PASS: `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json` |
| Runtime screenshots | PASS: production CDP capture after deploy |
| Operator no-score audit | PASS: all operator screenshots `hasScoreOnOperatorSurface=false` |
| Operator no-technical-state audit | PASS: all operator screenshots `hasTechnicalStateOnOperatorSurface=false` |

## 11. Remaining Issues

- The existing engineer diagnostics still contains older technical/detail blocks such as service score evidence and channel settings. This is acceptable because it is behind the engineer boundary and was not in scope to redesign.
- Production currently has no separate `Blocked` channel in the captured set; captured real states were `Use`, `Evacuate`, `Keep`, and `Emergency`.

## 12. Final Verdict

CHANNELS_LOCKED
