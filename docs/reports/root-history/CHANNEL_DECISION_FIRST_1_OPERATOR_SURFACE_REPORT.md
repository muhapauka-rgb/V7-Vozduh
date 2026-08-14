# CHANNEL.DECISION_FIRST.1_OPERATOR_SURFACE_REBUILD

Date: 2026-06-19
Branch: Updatesystem
Code commit: 6d913101078c552881855f0b7b6147056a5998b3
Runtime deploy: deploy-z8-14-Updatesystem-6d91310-20260619T145313

## 1. Current Surface Inventory

| Area | Previous Operator Surface | Problem |
| --- | --- | --- |
| Top cards | Здоровые каналы, Сервисы OK, Активные пользователи, Нагрузка | Started from health/metrics, not V7 decision. |
| Table | Channel / Decision / Signals / Users default, with optional Diagnostics score column | Default was close, but score-first Diagnostics was still available in operator columns. |
| Filters | Все, Проблемные, Здоровые, Перевести, Использовать | Mixed topology and health wording; not aligned to assignment decisions. |
| Overview channel metric | Healthy channel count | Still used health-first language outside technical diagnostics. |
| Signals | Services / Load / Route / Runtime wording | Included route in signal language, while approved compact signal model is Services / Load / Runtime / Stability. |

## 2. Reuse Audit

| Existing Source | Reused |
| --- | --- |
| `channelAssignmentStatus` | Yes |
| `channelAssignmentEvidence` | Yes |
| `channelAssignmentTableLabel` | Yes |
| `channelAssignmentTone` | Yes |
| `channelDecisionReason` | Yes |
| `channelDecisionActionText` | Yes |
| `channelDecisionCell` | Yes |
| `channelSignalSummary` | Yes |
| `channelSignalsCell` | Yes |
| Existing channel table renderer | Yes |
| Existing channel drawer/open actions | Yes |
| Existing safe deploy path | Yes |

No new planner, governance, execution path, truth source, storage, score formula, capacity formula, or route formula was added.

## 3. Score-First Language Removal

| Item | Result |
| --- | --- |
| Healthy Channels card | Replaced by decision cards. |
| Healthy filter | Replaced by Use decision filter. Legacy key remains mapped internally for compatibility only. |
| Diagnostics/score table column | Removed from operator column definitions. Technical health remains available deeper, not as the table answer. |
| Overview channel metric | Reworded to Use by V7 decision. |
| Generic health-first channel answer | Removed from primary channels surface. |

## 4. Decision-First Top Cards

New top cards:

| Card | Operator Meaning |
| --- | --- |
| Use | Channels V7 can use. |
| Evacuate | Channels where users should move away. |
| Emergency Only | Channels reserved for manual/emergency use. |
| Users | Users currently assigned to channels. |

Production counts captured after deploy:

| Card | Count |
| --- | --- |
| Use | 2 |
| Evacuate | 1 |
| Emergency Only | 4 |
| Users | 27 |

## 5. Decision-First Table

Final primary table:

| Column | Purpose |
| --- | --- |
| Channel | Object identity. |
| Decision | What V7 wants. |
| Signals | Why V7 wants it, compactly. |
| Users | Impact. |

Production validation:

| Check | Result |
| --- | --- |
| Headers are Channel / Decision / Signals / Users | PASS |
| Score/Health header absent | PASS |
| Decision column primary | PASS |
| Signals explain decision | PASS |

## 6. Compact Signals

Operator signal model remains derived from existing helpers:

| Signal | Status |
| --- | --- |
| Services | Reused |
| Load | Reused |
| Runtime | Reused |
| Stability | Reused |

Route remains available deeper where appropriate, but is not presented as one of the four compact table signals.

## 7. Decision Filters

Final filters:

| Filter | Production Count |
| --- | --- |
| All | 7 |
| Use | 2 |
| Evacuate | 1 |
| Emergency | 4 |
| Attention | 6 |

## 8. Operator Test

| Question | Result |
| --- | --- |
| In 3 seconds, can operator see what V7 wants? | PASS: top cards and Decision column are first. |
| In 5 seconds, can operator see why? | PASS: Signals column is adjacent to Decision. |
| Can operator see affected users? | PASS: Users column remains visible. |
| Does operator need score interpretation? | NO. Score/health no longer drives first screen. |

## 9. Screenshots

Production screenshots were captured after safe deploy.

| Screenshot | File |
| --- | --- |
| Desktop All | `docs/channel_decision_first_1/screenshots/desktop_all.png` |
| Desktop Use | `docs/channel_decision_first_1/screenshots/desktop_use.png` |
| Desktop Evacuate | `docs/channel_decision_first_1/screenshots/desktop_evacuate.png` |
| Desktop Emergency | `docs/channel_decision_first_1/screenshots/desktop_emergency.png` |
| Mobile 390 All | `docs/channel_decision_first_1/screenshots/mobile_all_390.png` |
| Mobile 390 Use | `docs/channel_decision_first_1/screenshots/mobile_use_390.png` |
| Mobile 390 Attention | `docs/channel_decision_first_1/screenshots/mobile_attention_390.png` |
| Screenshot audit | `docs/channel_decision_first_1/screenshots/capture_audit.json` |

## 10. Visual Validation

From `capture_audit.json`:

| Check | Result |
| --- | --- |
| Desktop cards | Use 2 / Evacuate 1 / Emergency Only 4 / Users 27 |
| Desktop filters | All 7 / Use 2 / Evacuate 1 / Emergency 4 / Attention 6 |
| Desktop headers | КАНАЛ / РЕШЕНИЕ / СИГНАЛЫ / ПОЛЬЗОВАТЕЛИ |
| Score header visible | No |
| Healthy card visible | No |
| Desktop overflow | No |
| Mobile 390 overflow | No |
| Console errors | None |

## 11. Tests

| Test | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` before implementation | PASS |
| `tools/v7-convergence-status --json` before implementation | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api` | PASS |
| Production safe deploy | PASS |
| Desktop screenshot capture | PASS |
| Mobile screenshot capture | PASS |
| Table renders | PASS |
| Cards render | PASS |
| Filters render | PASS |
| Mobile no overflow | PASS |
| Console errors | PASS |

## 12. Reference / ADR Decision

No canonical semantic change was made.

The implementation applies the already-approved decision-first operator model using existing assignment truth and existing signal helpers. Therefore:

| Document | Update |
| --- | --- |
| Canonical Reference | Not required |
| SYSTEM_MAP | Not required |
| New ADR | Not required |

## 13. Remaining Issues

| Issue | Status |
| --- | --- |
| Legacy internal filter keys `healthy` / `problematic` | Kept only for compatibility with existing calls. They now map to decision-first behavior. |
| Technical health score | Still available deeper as diagnostics, per ADR-003. Not removed from system. |

## 14. Final Verdict

DECISION_FIRST_SURFACE_IMPLEMENTED
