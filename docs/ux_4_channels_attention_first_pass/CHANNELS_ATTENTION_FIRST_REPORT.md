# CHANNELS ATTENTION FIRST REPORT

Project: V7 VOZDUH  
Program: UX.4_CHANNELS_ATTENTION_FIRST_PASS  
Date: 2026-06-20  
Branch: Updatesystem  
Runtime commit verified for UI capture: 7886c249a7e09089282c13b459bdb4afceae57d4

## 1. Reference First

Read before implementation:

| Source | Used |
| --- | --- |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Yes |
| `docs/reference/SYSTEM_MAP.md` | Yes |
| `docs/decisions/ADR-006-channel-operator-signal-model.md` | Yes |
| `docs/decisions/ADR-007-channel-signal-semantics-correction.md` | Yes |
| `docs/decisions/ADR-009-capacity-and-health-semantics.md` | Yes |
| `docs/decisions/ADR-010-diagnostics-reality-first-model.md` | Yes |
| `docs/ux_2_channels_operator_clarity_pass/CHANNELS_OPERATOR_CLARITY_REPORT.md` | Yes |
| `docs/ux_3_channels_action_flow_pass/CHANNELS_ACTION_FLOW_REPORT.md` | Yes |

No planner, assignment, execution, governance, signal calculation, decision logic, capacity formula, or routing formula was changed.

## 2. Reuse Audit

| Source | Reused |
| --- | --- |
| Existing Attention layer | Yes. Channel items are derived from existing attention-producing states. |
| Overview layer | Yes. Reused as a derived source, suppressed when the channel is already healthy by table rules. |
| Channel table | Yes. No new page, drawer, or workflow. |
| Existing problem severity | Yes. Mapped to Critical, Action Required, Review, Information, Healthy. |
| Existing signal severity | Yes. First-level signal tones drive attention only through display/order. |
| Existing decision model | Yes. `Use`, `Evacuate`, `Emergency Only`, `Blocked`, `Keep Current` remain the source of assignment meaning. |

## 3. Attention Inventory

Created: `docs/ux_4_channels_attention_first_pass/CHANNEL_ATTENTION_MATRIX.md`.

| State | Severity | Action Required | Urgent |
| --- | --- | --- | --- |
| Evacuate | Critical | Yes | Yes |
| Blocked with users | Critical | Yes | Yes |
| Disabled with users | Action Required | Yes | Yes |
| Not started with users | Action Required | Yes | Yes |
| Load hard/full | Action Required | Yes | Yes |
| Service degradation | Review / Action Required | Sometimes | Sometimes |
| Runtime issue | Review | No direct execution | No |
| Stability issue | Review | No direct execution | No |
| Missing data | Review | Check | No |
| Emergency Only | Information | No | No |
| Use / Keep with OK signals | Healthy | No | No |

## 4. Attention Priority

Strict priority implemented:

1. Critical
2. Action Required
3. Review
4. Information
5. Healthy

Tie-breakers:

| Tie-breaker | Rule |
| --- | --- |
| Users | More assigned users first. |
| First-level signals | Worse first-level signal first. |
| Existing order | Existing operator/default ordering remains fallback. |
| Name | Stable final fallback. |

## 5. Table Attention Mode

Added an existing-table switch:

| Mode | Behavior |
| --- | --- |
| `Обычный` | Keeps existing table/manual/default ordering. |
| `Внимание сначала` | Sorts derived attention states first, healthy channels last. |

The aggregate `Сигналы` column was not made sortable. This follows the canonical rule that individual first-level signals can guide order, but the aggregate signal group is not a new truth source.

## 6. Visual Attention

| Requirement | Result |
| --- | --- |
| Urgent items visible | Pass. Critical card and red row marker appear first. |
| Healthy items calm | Pass. Healthy `awg0` is visually calm and not promoted to review. |
| No screaming interface | Pass. Uses small cards and narrow row markers, not full-table alarm styling. |
| No duplicate attention system | Pass. It is a derived table view inside Channels. |

## 7. Channel Badge Audit

| Badge | Hierarchy |
| --- | --- |
| Evacuate | Highest operator urgency. Appears as Critical. |
| Blocked | Critical when users are assigned, Information when empty. |
| Use | Healthy if first-level signals are OK. |
| Emergency Only | Information unless existing users/signal severity require review. |
| Keep Current | Healthy only when first-level signals are OK. |

## 8. Problem Priority

When multiple problems exist, the attention card and row order use the highest-priority item first. Example from production:

| Channel | Visible Priority |
| --- | --- |
| `vless` | Critical: `Перевести пользователей` / `Лимит назначений достигнут` |
| `awg3` | Action Required: `Лимит назначений достигнут` |
| `wg гермашка, работает` | Action Required: `Лимит назначений достигнут` |
| `awg0` | Healthy/calm |

## 9. Operator Test

Question: what should a new operator look at first within 2 seconds?

Answer visible: `vless` / `Перевести пользователей` / `Лимит назначений достигнут`.

| Check | Result |
| --- | --- |
| What requires attention | Pass |
| What is healthy | Pass |
| What can be ignored | Pass |
| No need to open every channel | Pass |

## 10. Desktop Test

| Viewport | Theme | Result |
| --- | --- | --- |
| 1440x900 | Light/current | Pass |
| 1440x900 | Dark | Pass |

Screenshots:

- `docs/ux_4_channels_attention_first_pass/screenshots/desktop_light_default.png`
- `docs/ux_4_channels_attention_first_pass/screenshots/desktop_light_attention_first.png`
- `docs/ux_4_channels_attention_first_pass/screenshots/desktop_dark_attention_first.png`
- `docs/ux_4_channels_attention_first_pass/screenshots/critical_channel_vless.png`
- `docs/ux_4_channels_attention_first_pass/screenshots/healthy_channel_awg0.png`

## 11. Mobile Test

Viewport: 390x900.

| Check | Result |
| --- | --- |
| Attention panel visible | Pass |
| Critical card visible | Pass |
| Buttons usable | Pass |
| Horizontal overflow | Pass: none detected |
| Text clipping | Pass for visible attention content |

Screenshot:

- `docs/ux_4_channels_attention_first_pass/screenshots/mobile_390_attention_first.png`

## 12. Documentation Update

Updated `docs/reference/V7_CANONICAL_REFERENCE.md` with `CHANNEL_ATTENTION_RULES`.

Canonical rule added:

Attention First is a derived operator ordering over existing channel truth. It must not become a second attention system, a new planner, a new workflow, or a new truth source.

## 13. Tests

| Test | Result |
| --- | --- |
| `python3 -m py_compile admin/v7-admin-api` | Pass |
| Inline admin JS parse with Node VM | Pass |
| `git diff --check` | Pass |
| Production deploy | Pass: `deploy-z8-14-Updatesystem-7886c24-20260620T013352` |
| Production admin restart | Pass |
| Desktop screenshot capture | Pass |
| Mobile screenshot capture | Pass |
| Horizontal overflow audit | Pass |

## 14. Remaining Issues

None blocking.

The attention layer intentionally does not execute actions and does not decide assignment. It only makes existing channel decisions and first-level signal severity visible sooner.

## 15. Final Verdict

ATTENTION_MODEL_LOCK
