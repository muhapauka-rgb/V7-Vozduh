# CHANNEL.TRUTH.4 Channel Role Model Report

Date: 2026-06-15

Program: CHANNEL.TRUTH.4_CHANNEL_ROLE_MODEL

Verdict: CONDITIONAL_PASS

Reason for conditional verdict: the role model is implemented and production-validated for every assignment role currently present in live data, but current production data exposes only Use, Evacuate, and Emergency Only. Keep Only and Blocked are implemented in the shared role mapping, but no real production channel currently renders those statuses without changing truth/data.

## 1. Reuse Audit

| Area | Reused | Notes |
| --- | --- | --- |
| Assignment truth | Yes | Continued deriving from `operatorDecisionSurface.assignment_truth`, selected moves, candidates, blockers, registry role flags, safety gates. |
| Eligibility logic | Yes | No eligibility rules changed. |
| Planner/routing decision | Yes | Existing selected move evidence is only translated into operator language. |
| Channel score | Yes | Existing suitability score remains unchanged. |
| Channel table | Yes | Existing `assignment` and `assignment_blocker` columns now show role reason language. |
| Channel drawer | Yes | Existing Channel Analysis card now shows role reason/action under Assignment. |
| Storage/snapshots | No new storage | No database, snapshot, or new truth source added. |

## 2. Existing Truth Reused

| Status | Existing Truth | Source |
| --- | --- | --- |
| Use | Eligible candidates or selected target moves, or no assignment blocker | `channelAssignmentEvidence()` from existing assignment truth and channel state |
| Keep Only | Current users exist while new assignment is restricted/not selected | Existing user count and blockers from assignment evidence |
| Evacuate | Selected moves away from this channel | `selected_moves.current_egress` / batch preview moves |
| Emergency Only | Manual/reserve/canary/production assignment disabled flags | Existing registry role flags and blockers |
| Blocked | Hard blocker without current-user keep/emergency classification | Existing candidate/decision/blocker evidence |

## 3. Role Definitions

| Status | Operator Definition |
| --- | --- |
| Use | Channel is approved for receiving users. |
| Keep Only | Current users may stay. New users should not be assigned. |
| Evacuate | Current users should leave. |
| Emergency Only | Reserved for manual or emergency use. Automatic assignment is disabled. |
| Blocked | Cannot be used. Assignment is blocked by a hard gate. |

## 4. Role Reason Mapping

| Status | Reason Shown | Action Shown |
| --- | --- | --- |
| Use | Channel is approved for receiving users. Reason: Best available target. | Use this channel for new assignments. |
| Keep Only | Current users may stay. New users should not be assigned. | Keep current users here and avoid new assignments. |
| Evacuate | Current users should leave. Reason: Routing decision recommends moving users away. | Move users away from this channel. |
| Emergency Only | Reserved for manual or emergency use. Automatic assignment is disabled. | Use only for manual or emergency operations. |
| Blocked | Cannot be used. Reason: Assignment blocked by a hard gate. | Do not assign users to this channel. |

## 5. Table Before/After

| Area | Before | After |
| --- | --- | --- |
| Assignment cell subtext | Raw/technical snippets could leak assignment internals | Role reason sentence is visible directly in the assignment cell |
| Blocker cell subtext | `planner truth`, `planner blocker`, quality/planner conflict wording | `Routing decision` or `Channel quality is high, but assignment is restricted.` |
| Movement language | `Recommended movement` | `Users should be moved` |
| Manual channel language | `Manual only` | `Manual use only` |

Production table examples:

| Channel | Quality | Assignment | Blocker | Operator Meaning |
| --- | ---: | --- | --- | --- |
| awg0 | 92/100 | Use | No assignment blocker | Approved for receiving users |
| vless | 69/100 | Evacuate | Users should be moved | Current users should leave |
| OpenVPN-Kolosov | 37/100 | Emergency Only | Manual use only | Manual/emergency use only |

## 6. Drawer Before/After

| Area | Before | After |
| --- | --- | --- |
| Assignment | Status plus short reason only | Status, short reason, role reason, role action |
| Operator explanation | Operator still had to infer WHY | `Почему назначение` appears directly under Assignment |
| Action consistency | Quality action and assignment reason could feel disconnected | Assignment action now states what the role means before deeper quality action |
| Internal language | Planner/technical words could appear | Operator language replaces planner vocabulary |

Production drawer examples verified:

| Channel | Assignment | Reason Visible | Action Visible |
| --- | --- | --- | --- |
| awg0 | Use | Yes | Yes |
| vless | Evacuate | Yes | Yes |
| OpenVPN-Kolosov | Emergency Only | Yes | Yes |

## 7. Screenshots

Desktop:

- `docs/channel_truth_4/screenshots/desktop_channels_table.png`
- `docs/channel_truth_4/screenshots/desktop_drawer_use_awg0.png`
- `docs/channel_truth_4/screenshots/desktop_drawer_evacuate_vless.png`
- `docs/channel_truth_4/screenshots/desktop_drawer_emergency_openvpn.png`

Mobile:

- `docs/channel_truth_4/screenshots/mobile_channels_table.png`
- `docs/channel_truth_4/screenshots/mobile_drawer_use_awg0.png`
- `docs/channel_truth_4/screenshots/mobile_drawer_evacuate_vless.png`
- `docs/channel_truth_4/screenshots/mobile_drawer_emergency_openvpn.png`

Screenshot availability:

| Role | Desktop Screenshot | Mobile Screenshot | Note |
| --- | --- | --- | --- |
| Use | Yes | Yes | awg0 |
| Keep Only | Not available | Not available | No current production channel has Keep Only after live truth refresh |
| Evacuate | Yes | Yes | vless |
| Emergency Only | Yes | Yes | OpenVPN-Kolosov |
| Blocked | Not available | Not available | No current production channel has a hard-gate Blocked state without data mutation |

## 8. Mobile Validation

| Check | Status |
| --- | --- |
| 390px table renders | PASS |
| Quality visible | PASS |
| Assignment visible | PASS |
| Blocker visible | PASS |
| Role reason visible in drawer | PASS |
| Assignment action visible in drawer | PASS |
| Horizontal overflow observed | PASS: none observed in captured viewport |
| Clipped role reason | PASS |

## 9. Consistency Audit

| Channel | Table Story | Drawer Story | Consistent |
| --- | --- | --- | --- |
| awg0 | Use, no assignment blocker | Use, approved for receiving users, use for new assignments | Yes |
| vless | Evacuate, users should be moved | Evacuate, routing decision recommends moving users away | Yes |
| OpenVPN-Kolosov | Emergency Only, manual use only | Emergency Only, automatic assignment disabled | Yes |

Internal language audit:

| Phrase | Result |
| --- | --- |
| Recommended movement | Removed from operator UI |
| Planner truth | Removed from operator UI |
| quality score conflicts with planner truth | Removed from operator UI |
| Manual only | Replaced with Manual use only |

## 10. Remaining Issues

| Issue | Impact | Next Step |
| --- | --- | --- |
| No live Keep Only example | Cannot provide real production screenshot for this role today | Revalidate when production truth emits Keep Only again |
| No live Blocked example | Cannot provide real production screenshot for this role today | Revalidate when production truth emits a hard-gate Blocked channel |

No code issue was found for the missing screenshots. The absence is caused by current production truth/data, not by missing UI mapping.

## 11. Final Verdict

CONDITIONAL_PASS

The implementation satisfies the role model requirement for the live roles currently present in production. A non-technical operator can now answer within 5 seconds:

- How good is this channel?
- Can V7 use it?
- Why does it have this assignment status?
- What should I do?

Final closure to `CHANNEL_TRUTH_CLOSED` requires real production screenshots for Keep Only and Blocked when those statuses exist in live data.

## Validation Status

| Check | Status |
| --- | --- |
| Compile | PASS |
| Unit tests | PASS: 447 tests |
| Truth | PASS: FULLY_ALIGNED |
| Convergence | PASS: ALIGNED |
| Table renders | PASS |
| Drawer renders | PASS |
| Role reason renders | PASS |
| Mobile works | PASS |
| No overflow | PASS |
| No console errors | PASS |

