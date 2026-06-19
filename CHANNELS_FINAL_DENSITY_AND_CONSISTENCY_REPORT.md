# CHANNELS.TABLE_AND_LAYOUT_FINAL_POLISH Report

Date: 2026-06-19
Commit: `eca6b9a5`
Runtime deploy: `deploy-z8-14-Updatesystem-eca6b9a-20260619T231836`

## 1. Reference First

Read before implementation:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-006-channel-operator-signal-model.md`
- `docs/decisions/ADR-007-channel-signal-semantics-correction.md`
- `docs/decisions/ADR-009-capacity-and-health-semantics.md`
- `docs/decisions/ADR-010-diagnostics-reality-first-model.md`
- `CHANNELS_OPERATOR_ENGINEER_SEPARATION_REPORT.md`

Stable rule reused: Channel Decision V7, planner truth, assignment, signal semantics, capacity, routing, diagnostics, and execution paths are unchanged. This pass changed only visual density and presentation placement.

## 2. Reuse Audit

| Existing Source | Reused |
| --- | --- |
| `.metric` overview cards | Yes |
| `.stat-card` dashboard cards | Yes |
| `.cards-grid`, `.check-card`, `.route-card` | Yes |
| `.filterbar`, `.filter-chip` | Yes |
| `channelSignalsHeaderLabel()` | Yes |
| `sortableHeader()` | Yes |
| Channel table local sort config | Yes |
| Channel Drawer decision-first surface | Yes |

No new page, drawer, workflow, truth source, planner, governance path, storage, snapshot, endpoint, or score formula was added.

## 3. CARD_STANDARD_AUDIT

| Surface | Previous Issue | Final Standard |
| --- | --- | --- |
| Overview cards | Large 82px metric cards | Shared compact metric height 64px |
| Channels cards | 76px stat cards with excess vertical space | Shared compact stat-card height about 58-63px |
| Users / Routes / Checks cards | Used related `.stat-card` / `.check-card` classes | Same compact padding, radius, and gap |
| Drawer cards | Large section padding | Drawer section padding reduced while preserving hierarchy |

Result: Channels, Users, Routes, Operator, and Checks now share the same compact dashboard-card rhythm rather than visually jumping between tabs.

## 4. Filter Bar

The channel filter row no longer behaves like a content card.

| Item | Before | After |
| --- | --- | --- |
| Wrapper border/background | Visible container | Removed |
| Vertical padding | Large | Compact |
| Mobile filter height | 82px | 34px |
| Visual meaning | Card-like block | Lightweight navigation |

## 5. Signal Header

The standalone signal legend row was removed.

Before:

`Сигналы: S сервисы · L нагрузка · R runtime · T стабильность`

After:

The existing `Signals / S L R T` header is the only legend. Detailed signal meaning remains in the existing tooltip source.

## 6. SIGNAL_SORT_AUDIT

Required options were verified in the live production sort drawer:

| Required Sort | Status |
| --- | --- |
| Services | PASS: `По сервисам` |
| Load | PASS: `По нагрузке` |
| Runtime | PASS: `По runtime` |
| Stability | PASS: `По стабильности` |
| Users | PASS: `По пользователям` |
| Decision | PASS: `По решению V7` |

Signal-specific sorting continues to use severity rank: red first, yellow second, green third.

## 7. Table Density

| Metric | Before | After |
| --- | --- | --- |
| Standalone signal legend row | Yes | No |
| Desktop stat card height | 76px | 59px |
| Mobile filter strip height | 82px | 34px |
| Visible rows at 390px | 4 | 7 |
| Horizontal overflow at 390px | No | No |

## 8. Drawer Density

Channel Drawer spacing was tightened through existing shared drawer classes:

- Drawer header padding reduced.
- Drawer body gap reduced.
- Drawer section padding reduced.
- Channel decision surface gaps reduced.
- Signal cards inside the drawer reduced slightly.

The decision-first hierarchy remains unchanged: Channel -> Decision -> Reason -> Signals -> Problems -> Engineer Diagnostics.

## 9. VISUAL_STANDARD_REPORT

| Area | Standard |
| --- | --- |
| Card heights | Compact shared `.metric` / `.stat-card` rhythm |
| Font sizes | Existing hierarchy preserved; value text slightly tighter |
| Section spacing | Reduced where it created empty vertical space |
| Container padding | Reduced on cards, drawer sections, tables |
| Header spacing | Signal legend moved into header, zero extra row |

## 10. Screenshots

| Capture | File |
| --- | --- |
| Before desktop Channels | `docs/channels_final_density_and_consistency/screenshots/before_desktop_channels.png` |
| Before mobile Channels | `docs/channels_final_density_and_consistency/screenshots/before_mobile_channels.png` |
| After desktop light | `docs/channels_final_density_and_consistency/screenshots/after_desktop_channels.png` |
| After desktop dark | `docs/channels_final_density_and_consistency/screenshots/after_desktop_dark_channels.png` |
| After sorting drawer | `docs/channels_final_density_and_consistency/screenshots/after_desktop_sorting.png` |
| After channel drawer | `docs/channels_final_density_and_consistency/screenshots/after_desktop_drawer.png` |
| After mobile table | `docs/channels_final_density_and_consistency/screenshots/after_mobile_channels.png` |
| After mobile drawer | `docs/channels_final_density_and_consistency/screenshots/after_mobile_drawer.png` |

Audit file: `docs/channels_final_density_and_consistency/screenshots/capture_audit.json`.

## 11. Documentation

Updated:

- `docs/reference/V7_CANONICAL_REFERENCE.md`: added `UI Density Rules`; clarified S/L/R/T belongs in the signal header legend.
- `docs/reference/SYSTEM_MAP.md`: added `Admin UI Density Standard`.

## 12. Tests

| Check | Result |
| --- | --- |
| Pre-change truth gate | PASS |
| Pre-change convergence gate | PASS |
| Python compile | PASS: `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` |
| Diff whitespace | PASS: `git diff --check` |
| Production deploy | PASS |
| Desktop light screenshot | PASS |
| Desktop dark screenshot | PASS |
| Mobile 390 screenshot | PASS |
| Signal standalone legend removed | PASS |
| Signal header legend visible | PASS |
| Sort options verified | PASS |
| Mobile overflow | PASS |

## 13. Remaining Issues

- PNG screenshots are ignored by the project-wide `.gitignore`; they were intentionally force-added for this report evidence.
- The Channel Drawer still contains full engineer diagnostics deeper in the drawer. This is expected and outside this density-only pass.

## 14. Final Verdict

CHANNELS_UI_LOCKED
