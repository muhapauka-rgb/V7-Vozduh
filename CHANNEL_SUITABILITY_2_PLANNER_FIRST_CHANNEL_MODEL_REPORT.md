# CHANNEL.SUITABILITY.2_PLANNER_FIRST_CHANNEL_MODEL REPORT

Date: 2026-06-15

Commit deployed for runtime validation: `94d6612cf5205fa99c6457bc4416284689c5b800`

## 1. Reuse Audit

| UI Element | Existing Source | Reused |
|---|---|---|
| V7 Decision | `channelAssignmentStatus(source)` derived from `operatorDecisionSurface.assignment_truth` | Yes |
| Use | Existing eligible/selected target status | Yes |
| Evacuate | Existing `selected_moves` current-egress evidence | Yes |
| Keep Current Users | Existing users-present/no-new-assignment branch | Yes |
| Emergency Only | Existing `manual_only`, `reserve_only`, `canary`, `production_assignment_allowed=false` gates | Yes |
| Blocked | Existing assignment blockers and routing unavailable state | Yes |
| Technical Health | Existing `channelSuitability(source)` | Yes, formula unchanged |
| Problems | Existing `channelCompressedListHtml(..., 'problem')` | Yes |
| Working | Existing `channelCompressedListHtml(..., 'working')` | Yes |

No new planner, governance, execution path, truth source, database, storage, snapshot, eligibility engine, or scoring engine was added.

## 2. Decision Model

The primary channel operator model is now:

1. V7 Decision
2. Reason inside the same decision block
3. Action text inside decision details

Visible operator statuses:

| Decision | Operator Meaning |
|---|---|
| Use | V7 can use this channel for new assignments |
| Evacuate | Current users should leave this channel |
| Keep Current Users | Existing users may stay, new users should not be assigned |
| Emergency Only | Manual or emergency use only |
| Blocked | Do not assign users |

The previous first-screen split between `Assignment`, `Reason`, `Blocker`, and conflict wording was removed from the primary card.

## 3. Health Model

Technical Health remains the existing 0-100 score from `channelSuitability(source)`.

The formula was not changed. The UI now presents it as secondary information after V7 Decision.

## 4. Table Before/After

| Before | After |
|---|---|
| Channel | Channel |
| Quality / Score | Decision |
| Assignment | Health |
| Blocker | Users |
| Users |  |
| Action | Hidden by default |

Production validation showed table headers:

`Канал | Решение | Здоровье | Пользователи`

Old primary headers `Оценка`, `Назначение`, and `Блокер` were not visible.

## 5. Drawer Before/After

| Before | After |
|---|---|
| Качество | Решение V7 |
| Назначение | Technical Health |
| Problems | Problems |
| Working | Working |
| Details | Details |

Validated drawer order:

1. `МОДЕЛЬ КАНАЛА`
2. `Решение V7`
3. `Technical Health`
4. `Проблемы`
5. `Работает`
6. Existing details below

## 6. Screenshots

| Evidence | Path |
|---|---|
| Desktop table, decision first | `docs/channel_suitability_2/screenshots/desktop_channels_table_decision_first.png` |
| Desktop Use, awg0 | `docs/channel_suitability_2/screenshots/desktop_drawer_use_awg0.png` |
| Desktop Evacuate, vless | `docs/channel_suitability_2/screenshots/desktop_drawer_evacuate_vless.png` |
| Desktop Emergency Only, OpenVPN | `docs/channel_suitability_2/screenshots/desktop_drawer_emergency_openvpn.png` |
| Desktop problem click | `docs/channel_suitability_2/screenshots/desktop_drawer_problem_click_openvpn.png` |
| Desktop working click | `docs/channel_suitability_2/screenshots/desktop_drawer_working_click_openvpn.png` |
| Mobile table, 390px | `docs/channel_suitability_2/screenshots/mobile_channels_table_decision_first.png` |
| Mobile Evacuate drawer, 390px | `docs/channel_suitability_2/screenshots/mobile_drawer_evacuate_vless.png` |

Production status coverage:

| Required State | Production Example | Screenshot |
|---|---|---|
| Use | `awg0` | Yes |
| Evacuate | `vless` | Yes |
| Keep Current Users | Not present in current production sample | Not available without synthetic state |
| Emergency Only | `OpenVPN-Kolosov` | Yes |
| Blocked | Not present in current production sample | Not available without synthetic state |

## 7. Mobile Validation

| Check | Result |
|---|---|
| Width | 390px |
| Table headers visible | PASS |
| Decision visible immediately | PASS |
| Health secondary | PASS |
| Horizontal overflow | PASS, none detected |
| Drawer readable | PASS |
| Old primary card words | PASS, not present in channel model |

## 8. Consistency Audit

| Question | Result |
|---|---|
| What did V7 decide? | Visible first |
| Why? | Visible in the same decision block |
| How healthy is channel? | Visible second as Technical Health |
| What is broken? | Visible in Problems |
| What works? | Visible in Working |
| Does operator need planner knowledge? | No |

## 9. Remaining Issues

No UI implementation issue remains for the final channel model.

Evidence limitation: current production data did not include live `Keep Current Users` or `Blocked` examples, so those screenshots could not be honestly captured from production.

## 10. Final Verdict

CHANNEL_MODEL_FINALIZED

Final alignment target:

| Check | Status |
|---|---|
| Local | PASS |
| GitHub | PASS after push; one later truth run hit transient remote read failure |
| Runtime | PASS, deployed `94d6612c` |
| Truth | PASS for local/runtime; GitHub read intermittently flapped |
| Convergence | Runtime aligned; GitHub read intermittently flapped |
