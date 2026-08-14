# CHANNEL.SIGNALS.2 Table Implementation Report

Project: V7 VOZDUH
Program: CHANNEL.SIGNALS.2_TABLE_IMPLEMENTATION
Date: 2026-06-18
Runtime code commit verified: e5ea631f

## 1. Reuse Audit

| Source | Reused | Notes |
| --- | --- | --- |
| Canonical Reference | Yes | Reference-first completed before implementation. |
| ADR-002 Channel score is mixed score | Yes | Score remains available deeper; it is not the first-line operator signal. |
| ADR-003 Health screen diagnostics only | Yes | Health is renamed to Diagnostics and removed from default table. |
| ADR-004 Channel drawer is primary operator surface | Yes | Row actions still open existing channel surfaces. |
| ADR-006 Channel operator signal model | Yes | Table now uses Decision, Signals, Users as the operator-facing model. |
| Planner decision / assignment status | Yes | Existing assignment status is displayed; no decision logic changed. |
| Channel suitability / breakdown | Yes | Existing breakdown feeds read-only signal badges. |
| Service matrix | Yes | Services signal is derived from existing service status data. |
| Capacity / load | Yes | Load signal is derived from existing user count and limits. |
| Route / topology | Yes | Route signal is derived from existing topology/readiness state. |
| Runtime readiness | Yes | Runtime signal is derived from existing runtime readiness state. |

No new storage, snapshots, background jobs, APIs, planner paths, truth sources, or score formulas were added.

## 2. Table Before/After

| State | First-line columns |
| --- | --- |
| Before | Channel / Decision / Health / Users |
| After | Channel / Decision / Signals / Users |

Health was not deleted. It remains available as the optional Diagnostics column and in deeper diagnostics surfaces.

## 3. Signal Rendering

The new Signals column renders compact badges:

| Signal | Meaning | Source |
| --- | --- | --- |
| Services | Service availability and service checks | Existing service matrix / suitability breakdown |
| Load | Capacity pressure and assigned users | Existing capacity/load data |
| Route | Route/topology readiness | Existing topology state |
| Runtime | Runtime readiness | Existing runtime readiness data |
| Stability | Shown only when existing stability data indicates a problem | Existing stability signals |

The table does not show channel score or technical health as the primary answer. The operator sees the decision first, then the concrete operational signals that explain what is wrong.

## 4. Tooltip Rendering

Every signal badge exposes a read-only tooltip through existing table UI. Tooltips are hover/focus based and contain human-readable operator text.

Examples:

| Badge | Tooltip style |
| --- | --- |
| Services | Services: available / total and whether service checks require attention |
| Load | Load: user count and soft/hard capacity limits |
| Route | Route: whether route/topology is ready |
| Runtime | Runtime: whether runtime is ready |

Tooltips do not create actions, navigation, execution, or a second source of truth.

## 5. Sorting Implementation

Default sort now follows the approved operator order when the operator has not chosen a custom column sort:

| Rank | Decision state |
| --- | --- |
| 1 | Evacuate |
| 2 | Blocked with users |
| 3 | Overloaded with users |
| 4 | Emergency Only |
| 5 | Keep Current Users |
| 6 | Blocked |
| 7 | Use |

Tie-breakers:

1. Affected users, descending.
2. Worst signal severity.
3. Channel name.

Manual sorting still works through the existing table sort mechanism.

## 6. Filtering Implementation

The existing channel topology filter surface was extended with operator filters:

| Filter | Meaning |
| --- | --- |
| All | Show all channels |
| Problematic | Show channels with a non-use decision or problem signal |
| Healthy | Show channels with usable decision and no problem signals |
| Evacuate | Show channels requiring user evacuation |
| Use | Show channels that can receive users |

Legacy topology filtering is preserved.

## 7. Screenshots

Screenshot artifacts:

| Capture | File |
| --- | --- |
| Desktop table | [desktop_channels_table.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/desktop_channels_table.png) |
| Desktop problematic filter | [desktop_filter_problematic.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/desktop_filter_problematic.png) |
| Desktop use filter | [desktop_filter_use.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/desktop_filter_use.png) |
| Desktop signal tooltip | [desktop_signal_tooltip.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/desktop_signal_tooltip.png) |
| Mobile table 390px | [mobile_channels_table_390.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/mobile_channels_table_390.png) |
| Mobile signal tooltip 390px | [mobile_signal_tooltip_390.png](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/mobile_signal_tooltip_390.png) |
| Validation summary | [validation_summary.json](/Users/ponch/Documents/New project/docs/channel_signals_2/screenshots/validation_summary.json) |

Captured against runtime code commit e5ea631f.

## 8. Mobile Validation

| Check | Result |
| --- | --- |
| 390px page width | PASS |
| Horizontal page overflow | PASS: document width 390 / scrollWidth 390 |
| Active table shell overflow | PASS: active shell clientWidth 364 / scrollWidth 364 |
| Signal badges readable | PASS |
| Tooltips visible | PASS |
| Tooltip clipping | PASS |
| Console errors | PASS: none captured |

## 9. Tests

| Test | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` before implementation | PASS |
| `tools/v7-convergence-status --json` before implementation | PASS |
| `tools/v7-run-tests` | PASS: 447 tests |
| `py_compile` | PASS |
| `git diff --check` | PASS |
| Table renders | PASS |
| Signals render | PASS |
| Tooltips render | PASS |
| Default sort renders | PASS |
| Filters render | PASS |
| Mobile no overflow | PASS |
| Safe deploy | PASS: deployed runtime code commit e5ea631f |

Final truth and convergence checks are recorded after commit/push in the task handoff.

## 10. Remaining Issues

| Issue | Status |
| --- | --- |
| Production data is live and filter counts can change between captures | Expected runtime behavior |
| Healthy filter may be empty when every channel has at least one active problem signal | Expected strict signal model behavior |
| Full channel score still exists in diagnostics/deeper surfaces | Intentional per ADR-002 and ADR-003 |

No blocking UI issues remain for this table implementation.

## 11. Final Verdict

TABLE_SIGNAL_MODEL_IMPLEMENTED

