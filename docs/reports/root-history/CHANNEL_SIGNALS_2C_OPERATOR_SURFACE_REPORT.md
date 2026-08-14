# CHANNEL.SIGNALS.2C Operator Surface Polish Report

Date: 2026-06-18
Program: `CHANNEL.SIGNALS.2C_OPERATOR_SURFACE_POLISH`
Code commit deployed: `b68eacc22fc868295f2bf3659f3975a9d4ac60d3`
Deploy id: `deploy-z8-14-Updatesystem-b68eacc-20260618T235958`

## 1. Reuse Audit

| Source | Reused | Notes |
|---|---:|---|
| V7 Canonical Reference | YES | Read before implementation; section 18 updated after validation. |
| ADR-006 Channel Operator Signal Model | YES | Kept `Channel / Decision / Signals / Users`. |
| ADR-007 Signal Semantics Correction | YES | No signal semantics changed. |
| Channel Decision V7 | YES | Decision remains source of operator answer. |
| Existing table rendering | YES | Reused `channelTableHtml`, `channelRows`, `channelSignalsCell`. |
| Existing filters | YES | Reused `Все`, `Проблемные`, `Здоровые`, `Перевести`, `Использовать`. |
| Existing screenshots workflow | YES | Production screenshots captured from `/admin-v2#channels`. |

## 2. Christmas Tree Effect Removal

| Requirement | Result |
|---|---|
| Remove text labels inside first-level signal cells | PASS |
| Keep color as compact indicator | PASS |
| Reveal meaning by hover/focus/tap | PASS |
| Do not add new signals | PASS |

Implementation result:

- Signal labels are rendered as compact dot indicators.
- The visible signal text count in production validation is `0`.
- Tooltip and aria labels preserve meaning without adding table noise.

Evidence: `docs/channel_signals_2c/screenshots/validation_summary.json`.

## 3. Tooltip Improvements

| Tooltip Rule | Result |
|---|---|
| No `policy` | PASS |
| No `planner` | PASS |
| No `soft limit` / `hard limit` | PASS |
| No `assignment restriction` | PASS |
| Operator language | PASS |

Validated tooltip example:

`Нагрузка: 11 пользователей назначено. Новые назначения ограничены. Текущие пользователи не затронуты.`

Machine audit:

| Metric | Value |
|---|---:|
| Tooltip bad-word count | 0 |
| Console errors | 0 |

## 4. Table Density Audit

| Surface | Result |
|---|---|
| Desktop all channels | PASS |
| Desktop problematic filter | PASS |
| Desktop use filter | PASS |
| Mobile all channels | PASS |
| Mobile problematic filter | PASS |
| Mobile use filter | PASS |

The table now scans as:

`Channel -> Decision -> compact signal dots -> Users`

It no longer repeats `Сервисы / Нагрузка / Runtime / Стабильность` on every row.

## 5. Filter Consistency Audit

Production filter counts after deploy:

| Filter | Rows |
|---|---:|
| Все | 7 |
| Проблемные | 5 |
| Использовать | 2 |

The screenshots and JSON validation agree on active filter state and visible row count.

## 6. Top Cards Audit

| Card | Status | Notes |
|---|---|---|
| Здоровые каналы | KEEP | Summary card remains useful. |
| Сервисы OK | KEEP | Explains service matrix coverage. |
| Активные пользователи | KEEP | Useful capacity context. |
| Нагрузка | KEEP | Still relevant as capacity warning. |

No top-card logic or semantics changed.

## 7. Visual Hierarchy Validation

| Question | Answer |
|---|---|
| Does operator see decision before diagnostics? | YES |
| Are signals secondary to decision? | YES |
| Are diagnostics hidden from first-level table? | YES |
| Does red signal mean action/removal/block is required? | YES |
| Can operator scan 20 channels quickly? | YES |

The table is now calmer: decision words carry the primary meaning, dots carry compact support, and details remain one interaction away.

## 8. Mobile Validation

| Check | Result |
|---|---|
| 390px viewport captured | PASS |
| No document horizontal overflow | PASS |
| Signal dots visible | PASS |
| Tooltip opens on focus/tap path | PASS |
| Users header no longer visually clipped | PASS |
| Buttons usable | PASS |

Machine audit:

| Surface | Horizontal Overflow |
|---|---|
| Mobile all | false |
| Mobile problematic | false |
| Mobile use | false |

## 9. Screenshots

| Screenshot | Path |
|---|---|
| Desktop all channels | `docs/channel_signals_2c/screenshots/desktop_all_channels.png` |
| Desktop problematic | `docs/channel_signals_2c/screenshots/desktop_problematic_channels.png` |
| Desktop use | `docs/channel_signals_2c/screenshots/desktop_use_channels.png` |
| Desktop load tooltip | `docs/channel_signals_2c/screenshots/desktop_tooltip_load.png` |
| Mobile all 390px | `docs/channel_signals_2c/screenshots/mobile_all_channels_390.png` |
| Mobile problematic 390px | `docs/channel_signals_2c/screenshots/mobile_problematic_channels_390.png` |
| Mobile use 390px | `docs/channel_signals_2c/screenshots/mobile_use_channels_390.png` |
| Mobile load tooltip 390px | `docs/channel_signals_2c/screenshots/mobile_tooltip_load_390.png` |
| Validation JSON | `docs/channel_signals_2c/screenshots/validation_summary.json` |

## 10. Tests

| Check | Result |
|---|---|
| `tools/v7-truth-check --all --json` before code work | PASS |
| `tools/v7-convergence-status --json` before code work | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| `tools/v7-run-tests` | PASS, 447 tests |
| Safe deploy | PASS |
| Production screenshot capture | PASS |
| Max first-level signals | PASS, `4` |
| Visible signal text count | PASS, `0` |
| Tooltip bad-word count | PASS, `0` |
| Console errors | PASS, `0` |

## 11. Final Verdict

`OPERATOR_SURFACE_READY`

The operator-facing Channels table is now calm, compact, decision-first, and production-verified on desktop and mobile. No planner, assignment, governance, execution, score, or signal semantics were changed.
