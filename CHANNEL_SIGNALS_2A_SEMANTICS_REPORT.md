# CHANNEL.SIGNALS.2A_SIGNAL_SEMANTICS_CORRECTION REPORT

Date: 2026-06-18
Branch: `Updatesystem`
Code commit verified: `021e7312`

## 1. Signal Contradiction Report

| Contradiction | Evidence | Decision |
| --- | --- | --- |
| `Route` appeared as a first-level red channel problem even when the underlying cause was capacity or services | `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md` shows current Route is readiness/topology confidence, not route quality. Live rows showed Route degrading with `HARD_FULL` or partial services. | Remove `Route` from first-level table signals. Keep route deeper as supporting/diagnostic evidence. |
| Hidden/supporting endpoints made operator-facing `Services` look degraded | Live service matrix: otherwise usable channels failed `Anthropic API`; primary user services were available. | First-level `Services` uses primary user-facing services only. Hidden/supporting endpoint failures stay in tooltip/details. |
| `Load` could be read as bad speed or bad internet | Current load values come from policy/assignment capacity limits and users assigned. | Keep `Load`, but label/tooltip it as capacity/assignment pressure, not speed quality. |
| Score/assignment/signal were visually conflated | Prior table made a high score, assignment decision, and red Route look like one truth source. | Signals are diagnostics. Assignment remains planner-derived. Score remains secondary. |

## 2. Route Signal Audit

Route is not a first-level operator signal today.

Current route component means:

- topology/readiness confidence;
- route/runtime alignment support;
- affected by service and capacity state;
- not direct latency, speed, packet loss, country route quality, or user traffic quality.

Final placement:

| Location | Route Status |
| --- | --- |
| Channel table first layer | Hidden |
| Channel drawer screen 1 | Only if a real route blocker exists |
| Details / diagnostics | Keep |
| Evidence / technical | Keep |

## 3. Capacity Operator Trust Report

Capacity/Load remains visible because it is directly actionable for assignment trust.

Operator meaning:

- `OK`: channel is within current assignment policy.
- `Warn/Bad`: channel is at or above policy limit.
- It does not mean slow speed by itself.

Observed production tooltip:

`Нагрузка: 11 пользователей. По текущей policy канал выше жёсткого лимита 2; это ограничивает новые назначения, но не означает плохую скорость.`

Known caveat: current policy limits are strict for several channels. That is a policy/planner question, not a table signal semantics question.

## 4. Service Importance Report

First-level Services now tracks primary user-facing services.

Primary services:

| Service |
| --- |
| Telegram |
| YouTube |
| Instagram |
| Google |
| WhatsApp |
| ChatGPT |
| Claude |

Supporting/hidden diagnostics:

| Endpoint | First-Level Effect |
| --- | --- |
| `anthropic` / Anthropic API | Does not downgrade first-level Services by itself |
| `openai_auth` | Does not downgrade first-level Services by itself |
| `google_auth` | Does not downgrade first-level Services by itself |

Observed production tooltip:

`Сервисы: основные пользовательские сервисы доступны 7/7. Дополнительные endpoint-проверки не влияют на первый слой: Anthropic API.`

## 5. Operator Mental Model Test

| Operator Question | Answer After 2A |
| --- | --- |
| Can users use the main internet services? | `Services` |
| Is the channel overloaded for assignment policy? | `Load` |
| Is runtime ready now? | `Runtime` |
| Is there a stability/interface problem? | `Stability`, shown only when not OK |
| Is route quality bad? | Not claimed by table; route details stay deeper |
| Can planner assign here? | Assignment/decision column, not score/signal |

## 6. Commercial Validation Report

Commercial operator systems do not show a derived supporting signal as a first-level red incident when the real cause is another first-level problem.

| Product Philosophy | 2A Alignment |
| --- | --- |
| Cloudflare / Datadog | Incident first, derived diagnostics later |
| Stripe / GitHub Enterprise | Operator-facing cause before raw internals |
| Tailscale | Connectivity/readiness separated from policy and diagnostics |
| Linear | One visible meaning per label |

Result: the corrected signal model is commercially clearer than the previous mixed `Services/Load/Route` first layer.

## 7. Final Signal Set

| Signal | First-Level? | Meaning |
| --- | --- | --- |
| Services | Yes | Primary user-facing service availability |
| Load | Yes | Assignment/capacity pressure under current policy |
| Runtime | Yes | Runtime readiness in current snapshot |
| Stability | Conditional | Shown only when not OK |
| Route | No | Supporting route/readiness diagnostics unless real route blocker exists |
| Score | No | Secondary mixed diagnostic score |
| History | No | Evidence/details |

## 8. Implementation

Changed only `admin/v7-admin-api` signal presentation helpers:

- added primary-service evidence extraction;
- changed Services badge to use primary user-facing services;
- changed Services tooltip to mention optional/hidden endpoint failures separately;
- changed Load tooltip to say assignment policy/capacity, not speed;
- removed Route from first-level table signal summary;
- kept planner, assignment, governance, execution, score formulas, storage, and APIs unchanged.

Canonical docs updated:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-007-channel-signal-semantics-correction.md`

## 9. Screenshots

| Screenshot | File |
| --- | --- |
| Desktop table | `docs/channel_signals_2a/screenshots/desktop_channels_table.png` |
| Desktop table, Playwright capture | `docs/channel_signals_2a/screenshots/desktop_channels_table_pw.png` |
| Desktop problematic filter | `docs/channel_signals_2a/screenshots/desktop_filter_problematic.png` |
| Desktop use filter | `docs/channel_signals_2a/screenshots/desktop_filter_use.png` |
| Desktop signal tooltip | `docs/channel_signals_2a/screenshots/desktop_signal_tooltip_pw.png` |
| Mobile table, 390px | `docs/channel_signals_2a/screenshots/mobile_channels_table_390.png` |
| Mobile signal tooltip, 390px | `docs/channel_signals_2a/screenshots/mobile_signal_tooltip_390.png` |
| Validation JSON | `docs/channel_signals_2a/screenshots/validation_summary.json` |

Visual validation:

| Check | Result |
| --- | --- |
| `Route` absent from first-level channel table signals | PASS |
| `Services` green when only hidden Anthropic endpoint fails | PASS |
| `Load` remains visible for overloaded channels | PASS |
| `Load` tooltip says assignment/capacity, not speed | PASS |
| Mobile 390px horizontal overflow | PASS: `false` |

## 10. Tests

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` before implementation | PASS |
| `tools/v7-convergence-status --json` before implementation | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| `tools/v7-run-tests` | PASS: 447 tests |
| Safe deploy | PASS: `deploy-z8-14-Updatesystem-021e731-20260618T180858` |
| Production screenshot capture | PASS |

## 11. Remaining Issues

| Issue | Scope |
| --- | --- |
| One headless Playwright capture showed conservative `Запрещён` decision labels while the read-only `decision-surface` API still reported trusted channel states for `vless`, `awg0`, and `awg3`. | Out of scope for SIGNALS. Needs a separate assignment display/runtime rendering audit only if reproduced in the operator browser. |
| Current capacity policy limits are strict for several channels. | Planner/policy decision, not signal semantics. |

## 12. Final Verdict

`SIGNALS_READY_FOR_DRAWER`

The channel table signal semantics are now aligned:

- no fake first-level Route problem;
- primary Services mean user-facing services;
- hidden endpoint failures stay diagnostic;
- Load means assignment/capacity pressure;
- score, assignment, and diagnostics no longer pretend to be the same truth.
