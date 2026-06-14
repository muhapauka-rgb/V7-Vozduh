# CHANNEL.TRUTH.2 Assignment Eligibility Truth Discovery

Date: 2026-06-15

Program: CHANNEL.TRUTH.2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY

Final Verdict: EXISTING_TRUTH_SUFFICIENT

## 1. Saved State

| Check | Result |
| --- | --- |
| Workspace | `/Users/ponch/Documents/New project` |
| Branch | `Updatesystem` |
| HEAD before audit | `bcca20e6 Audit channel decision pipeline alignment` |
| Git status before audit | Only `V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` untracked |
| Approved UX/channel work committed | Yes |
| Runtime mutation | None |
| UI change | None |
| Planner change | None |
| Governance change | None |
| Autoswitch apply | Not run |
| User movement | None |

The untracked handoff document is outside this program and was not touched.

## 2. Truth Gate

| Gate | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS after escalated rerun |
| `tools/v7-convergence-status --json` | PASS after escalated rerun |

The first sandboxed gate attempt could not read GitHub and returned `github_remote_unreadable`. The required escalated rerun returned `FULLY_ALIGNED` / `ALIGNED`: local and GitHub at `bcca20e67c2d82fc1b8fb12a635de5284b955736`, runtime at `566ee5122c70f731e536bec84e75d4db90f994c4`, with docs-only runtime mismatch ignored by the truth model.

## 3. Owner Map

| Decision Area | Owner | File | Function | Runtime Source |
| --- | --- | --- | --- | --- |
| Assignment eligibility | Runtime planner | `tools/v7-users-autoswitch` | `AutoswitchPlanner._candidate`, `_block`, `_gate_*` | `decisions[].candidates[].eligible`, `blocked` |
| Retention eligibility | Runtime planner | `tools/v7-users-autoswitch` | `_decision_for_user` current candidate path | current candidate with `purpose="current"` plus decision reason |
| Evacuation decision | Runtime planner | `tools/v7-users-autoswitch` | `_decision_for_user`, `_select_moves` | `selected_moves`, `reason=current_egress_not_eligible` |
| Planner eligibility | Runtime planner | `tools/v7-users-autoswitch` | `_candidate`, `_candidate_json` | candidate JSON fields: `eligible`, `blocked`, `score`, `score_parts` |
| Channel ranking | Runtime planner | `tools/v7-users-autoswitch` | candidate sort in `_decision_for_user`, `_mark_best_available_pool` | sorted eligible candidates and `best_available_pool` |
| Candidate generation | Runtime planner | `tools/v7-users-autoswitch` | `_decision_for_user` | all egress rows converted into user-specific candidates |
| Hard gates | Runtime planner | `tools/v7-users-autoswitch` | `_gate_basic`, `_gate_reservation`, `_gate_org`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety` | `blocked` reasons |
| Governance gates | Existing authority policy | `tools/v7-users-autoswitch` | `_authority_budget_gate` | `safety.authority_budget_gate` |
| Restore barrier | Existing restore gate | `tools/v7-users-autoswitch`, `tools/v7-restore-settle-gate` | `_restore_barrier_status`, restore settle checker | `safety.restore_barrier` |
| Service suitability | Runtime planner | `tools/v7-users-autoswitch` | `_service_suitability`, `_gate_service`, `_gate_service_failures` | `service_suitability`, service matrix, Telegram sentinel |
| Capacity suitability | Runtime planner | `tools/v7-users-autoswitch` | `_capacity_decision`, `_gate_load`, `_pick_projected_moves` | `capacity_decision`, projected load |
| Route suitability | Runtime planner | `tools/v7-users-autoswitch` | `_route_class_for_services`, `_gate_service` route fitness branch | route class fitness, service truth |
| Trust/recovery influence | Advisory only | `admin_core/routing_brain.py`, `admin_core/operator_decision_surface.py`, `admin_core/intelligence_snapshots.py` | candidate advisory and trust/recovery readers | CTR/advisory fields; no selected-move authority |
| Current UI channel score | Admin UI | `admin/v7-admin-api` | `channelSuitability` | browser-side derived score, not planner truth |

## 4. Assignment Trace

Question: what exact path must succeed before V7 assigns a user to a channel?

| Step | PASS Condition | FAIL Condition | Blocks Assignment? |
| --- | --- | --- | --- |
| User considered | active enabled user selected by planner | user disabled or outside requested user filter | Yes |
| Egress candidate created | `_candidate(... purpose="planned")` starts with `eligible=True` | candidate cannot be constructed from known egress | Yes |
| Basic gate | enabled, not maintenance/disabled/quarantine, not manual-only, health code acceptable, severity not hard-blocked | `egress_disabled`, `egress_state_*`, `manual_only`, `health_code_*`, `severity_*`, static `hard_full`, `reserve_only` | Yes |
| Reservation gate | not canary-reserved for production assignment | `canary_reserved_production_assignment_blocked` | Yes |
| Org gate | group policy allows target and isolation is safe | `not_in_group_allowed_pool`, `excluded_by_group_policy`, `exclusive_to_*`, `not_in_egress_group_acl`, `egress_in_use_by_other_group` | Yes |
| Quality gate | speed and stability meet planner floors or permitted evidence exception | `avg_mbps_below_floor`, `min_mbps_below_floor`, `stability_below_floor` | Yes |
| Service gate | required services and route class pass | `telegram_required_*`, `service_*_evidence_unknown`, `service_*_persistent_failed`, `route_class_*_failed` | Yes |
| Load gate | target is not over planned/failover hard limit | `planned_hard_full`, `failover_full` | Yes |
| Safety gate | no quarantine, failed verification limit, target block, or pair reversal window | `egress_safety_quarantine`, `egress_failed_verifications_limit`, `target_blocked_for_user`, `pair_reversal_stability_window` | Yes |
| Score/rank | only after all gates remain eligible; `score_parts` are summed | no eligible candidate | Yes |
| Selection | best eligible target beats current or failover/rebalance/reconnect condition exists | `sticky_keep_current`, `current_is_best`, cooldown/freeze, or no eligible alternative | Yes |
| Policy selection caps | `_select_moves` fits per-run failover/reconnect/rebalance/planned limits and projected capacity | over selected limit or projected target capacity | Yes |
| Authority budget | `_authority_budget_gate` allows selected moves within certified/current budget | budget zero, frozen/revoked, cap removes moves | Yes |
| Restore / snapshot gates | restore clearance and snapshot gate do not suppress selected moves | restore generation/budget mismatch, active STOP snapshot gate | Yes |
| Execution envelope | selected moves have operation id, selected hash, atomic envelope | invalid envelope during apply | Yes for execution |

Assignment truth already exists as: candidate `eligible=true`, no `blocked` reasons, selected/ranked inside the planner, then not suppressed by authority/restore/snapshot gates.

## 5. Retention Trace

Question: what exact path allows current users to remain?

| Step | PASS | FAIL | Consequence |
| --- | --- | --- | --- |
| Current candidate built | `_candidate(... purpose="current")` remains eligible | current candidate missing or ineligible | failover branch starts |
| Canary current exception | current canary-reserved channel can be held with separate drain approval note | current channel not eligible for non-canary reasons | failover search |
| Restore barrier check | no failover quarantine/post-TTL generation clearance requirement | restore barrier suppresses failover or requires clearance | users stay temporarily; move not selected |
| Service restore stage | service-only block is not under unapproved restore stage | restore stage requires approval | users stay temporarily; move not selected |
| Eligible failover exists | failover candidate exists, differs from current, cooldown ok | no target or cooldown/freeze | no selected move |
| Selection cap survives | move remains after policy/capacity/authority/snapshot gates | selected move removed | no movement |

Current production evidence:

| Channel | Current Users | Retention Result | Source |
| --- | ---: | --- | --- |
| `vless` | 10 | Cannot keep; 10 users selected to leave | `selected_moves_by_source.vless=10`, reason `current_egress_not_eligible` |
| `awg3` | 8 | Cannot keep; 8 users selected to leave | `selected_moves_by_source.awg3=8`, reason `current_egress_not_eligible` |
| `wireguard-1779454504-c43409` | 8 | Can keep and can receive | candidate eligible count 26, selected target for 18 moves |

Retention is therefore not a separate model. It is the current-candidate branch of the same planner plus selected move evidence.

## 6. Evacuation Trace

Question: what causes V7 to decide users should leave?

| Channel | Reason Users Leave | Source |
| --- | --- | --- |
| `vless` | Current egress candidate is not eligible because planner blocks `min_mbps_below_floor` and `stability_below_floor`; failover target exists | `docs/channel_truth_1/evidence/autoswitch_planner_preview.json`, `docs/channel_truth_1/evidence/channel_pipeline_audit_summary.json` |
| `awg3` | Current egress candidate is not eligible because planner blocks `stability_below_floor`; failover target exists | same |

Selected movement evidence:

| From | To | Count | Reason |
| --- | --- | ---: | --- |
| `vless` | `wireguard-1779454504-c43409` | 10 | `current_egress_not_eligible` |
| `awg3` | `wireguard-1779454504-c43409` | 8 | `current_egress_not_eligible` |

Evacuation truth already exists as selected moves where `current_egress` equals the channel and move reason includes `current_egress_not_eligible`.

## 7. Hard Gate Inventory

Complete inventory observed in the real planner path and current evidence:

| Gate | Source | Blocks Assign | Blocks Keep | Blocks Execute |
| --- | --- | --- | --- | --- |
| `egress_disabled` | `_gate_basic`, registry enabled/state | Yes | Conditional | Yes |
| `egress_state_maintenance` / `disabled` / `quarantine` | `_gate_basic` | Yes | Conditional | Yes |
| `manual_only` | `_gate_basic`, registry | Yes | No for current hold | Yes |
| `reserve_only` | `_gate_basic`, registry | Yes | Conditional | Yes |
| `health_code_*` | `_gate_basic`, health code | Yes | Yes if current candidate fails | Yes |
| `severity_*` | `_gate_basic`, severity classification | Yes | Yes if current candidate fails | Yes |
| `hard_full` | `_gate_basic` in static load mode | Yes | No for current | Yes |
| `canary_reserved_production_assignment_blocked` | `_gate_reservation` | Yes | No for same current channel; separate drain approval note | Yes |
| `planned_hard_full` | `_gate_load` | Yes | No for current | Yes |
| `failover_full` | `_gate_load` for failover target | Yes | N/A | Yes |
| `egress_safety_quarantine` | `_gate_safety` | Yes | No for current | Yes |
| `egress_failed_verifications_limit` | `_gate_safety` | Yes | No for current | Yes |
| `target_blocked_for_user` | `_gate_safety` | Yes | No for current | Yes |
| `pair_reversal_stability_window` | `_gate_safety` | Yes | No for current | Yes |
| `not_in_group_allowed_pool` | `_gate_org` | Yes | Conditional | Yes |
| `excluded_by_group_policy` | `_gate_org` | Yes | Conditional | Yes |
| `exclusive_to_*` | `_gate_org` | Yes | Conditional | Yes |
| `not_in_egress_group_acl` | `_gate_org` | Yes | Conditional | Yes |
| `egress_in_use_by_other_group` | `_gate_org` | Yes | Conditional | Yes |
| `avg_mbps_below_floor` | `_gate_quality` | Yes | Yes if current candidate fails | Yes |
| `min_mbps_below_floor` | `_gate_quality` | Yes | Yes if current candidate fails | Yes |
| `stability_below_floor` | `_gate_quality` | Yes | Yes if current candidate fails | Yes |
| `trusted_ru_required` | `_gate_service` | Yes | Conditional by route class | Yes |
| `telegram_required_*` | `_gate_service` | Yes | Yes if current candidate fails | Yes |
| `service_*_evidence_unknown` | `_gate_service` | Yes for explicit required services | Conditional | Yes |
| `service_multiple_critical_failed` | `_gate_service_failures` | Yes | Conditional | Yes |
| `service_*_persistent_failed` | `_gate_service_failures` | Yes | Conditional | Yes |
| `route_class_*_failed` | `_gate_service` route fitness | Yes | Conditional | Yes |
| `cooldown` / user freeze | `_decision_for_user` | Blocks selection, not eligibility | Keeps user in place | Yes |
| authority budget zero/cap | `_authority_budget_gate` | Blocks/caps selected moves | Keeps user in place | Yes |
| restore barrier clearance/generation mismatch | `plan()` restore checks | Blocks selected moves | Keeps user in place | Yes |
| intelligence snapshot STOP | `_intelligence_snapshot_gate` | Blocks selected moves | Keeps user in place | Yes |
| invalid atomic execution envelope | `apply()` | No | No | Yes |

Current evidence hard gates by channel:

| Channel | Current Hard Gate(s) |
| --- | --- |
| `vless` | `min_mbps_below_floor`, `stability_below_floor` |
| `awg0` | `min_mbps_below_floor`, `stability_below_floor` |
| `awg3` | `stability_below_floor` |
| `1` | `health_code_000`, `severity_FAIL`, `avg_mbps_below_floor`, `min_mbps_below_floor`, `telegram_required_telegram_down_14s` |
| `openvpn-1779388847-d2ad7c` | same as `1` |
| `wireguard-1779454504-c43409` | none observed |
| `amneziawg-exec-20260528-10-8-1-14` | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor` |

## 8. Eligibility Model Discovery

Can the current system already answer these statuses without new code?

| Status | Already Exists? | Source |
| --- | --- | --- |
| Eligible | Yes | Any planner candidate for channel has `eligible=true`, no `blocked`, survives policy/authority/snapshot gates |
| Keep Only | Yes, derived | current candidate eligible but planned assignment candidate blocked or not selected; current channel has users and no selected moves away |
| Evacuate | Yes | `selected_moves` from channel with reason `current_egress_not_eligible` or equivalent failover reason |
| Blocked | Yes | candidate `eligible=false` with `blocked` reasons |
| Emergency Only | Yes, derived from existing flags | `manual_only`, `reserve_only`, `canary_reserved`, execution-only role, and no production assignment eligibility |

No new eligibility model is required. The missing piece is presentation: current admin score does not expose these existing planner/governance truths directly.

## 9. Planner Alignment

Using the current production snapshot captured in `CHANNEL.TRUTH.1`:

| Channel | Planner Eligible | Planner Rank | Candidate? | Selected? | Reason |
| --- | --- | --- | --- | --- | --- |
| `vless` | No | None | Yes, blocked | Selected as source for 10 moves | `min_mbps_below_floor`, `stability_below_floor`, `current_egress_not_eligible` |
| `awg0` | No | None | Yes, blocked | No | `min_mbps_below_floor`, `stability_below_floor` |
| `awg3` | No | None | Yes, blocked | Selected as source for 8 moves | `stability_below_floor`, `current_egress_not_eligible` |
| `1` | No | None | Yes, blocked | No | `health_code_000`, `severity_FAIL`, Telegram hard block, speed floor |
| `openvpn-1779388847-d2ad7c` | No | None | Yes, blocked | No | same hard blockers as `1` |
| `wireguard-1779454504-c43409` | Yes | Best available pool rank 1 | Yes | Selected as target for 18 moves | eligible target; no blockers |
| `amneziawg-exec-20260528-10-8-1-14` | No | None | Yes, blocked | No | `manual_only`, `reserve_only`, canary reserved, stability floor |

Planner summary: 26 active users, 7 egress rows, 18 candidate moves, 18 selected moves, all selected moves target `wireguard-1779454504-c43409`.

## 10. Governance Alignment

| Channel | Planner Allows | Governance Allows | Final Result |
| --- | --- | --- | --- |
| `vless` | No as target; yes as source evacuation | Authority budget allows selected moves | Evacuate users to eligible target |
| `awg0` | No | N/A because no selected move targets it | Block assignment |
| `awg3` | No as target; yes as source evacuation | Authority budget allows selected moves | Evacuate users to eligible target |
| `1` | No | N/A because no selected move targets it | Block assignment |
| `openvpn-1779388847-d2ad7c` | No | N/A because no selected move targets it | Block assignment |
| `wireguard-1779454504-c43409` | Yes | Authority budget gate allows 18 of 18 selected moves; restore barrier inactive in planner preview | Eligible target, selected |
| `amneziawg-exec-20260528-10-8-1-14` | No for production assignment | N/A because no selected move targets it | Emergency/reserve only, do not auto-assign |

Governance evidence:

| Gate | Current Evidence |
| --- | --- |
| Authority budget | `safety.authority_budget_gate`: `enabled=true`, `authority_class=POOL`, `current_allowed_user_budget=25`, `selected_moves_before_gate=18`, `selected_moves_after_gate=18`, `blocked_actions=[]` |
| Restore barrier in planner preview | `enabled=false`, `active=false`, `post_ttl_blocking=false`, `failover_quarantine=false` |
| Restore settle checker | `gate_status=NO-GO` for restore-settle evidence readiness; read-only, execution_allowed_now=false |
| Control-plane governance | Governance model exists; direct apply/restore requires separate approval; no runtime commands executed |

Governance is not a replacement for eligibility. It is the execution and blast-radius gate after planner-selected moves exist.

## 11. Duplication Audit

| Future Idea | Existing Equivalent | Reuse? |
| --- | --- | --- |
| New Assignment Status | `decisions[].candidates[].eligible`, `blocked`, `safety.authority_budget_gate`, `selected_moves` | Yes, derive from planner output |
| New Candidate Status | Candidate JSON from `_candidate_json` | Yes |
| New Governance Status | `safety.authority_budget_gate`, operator execution pipeline, control-plane governance checker | Yes |
| New Execution Status | `apply_result`, terminal verdict, atomic execution envelope, restore barrier | Yes |
| New Channel Status | Admin `channelSuitability` | Reuse only as technical/display quality, not assignment truth |
| New Evacuation Model | `selected_moves` grouped by `current_egress` | Yes |
| New Keep Model | current candidate branch plus absence of selected moves away | Yes |
| New Emergency Only Model | registry flags: `manual_only`, `reserve_only`, `canary_reserved`, execution-only role | Yes |

Creating a new status engine would duplicate the planner and increase risk. The safe path is an adapter/read-model over existing planner evidence.

## 12. Existing Truth Reuse Map

| Operator Question | Existing Field / Path | Meaning |
| --- | --- | --- |
| Can this channel receive users? | grouped planner candidates where `egress=<channel>` and `eligible=true`; selected target evidence | Yes if eligible candidate exists and not suppressed by selected-move gates |
| Can current users stay here? | current candidate from `_decision_for_user`; absence of selected moves from channel | Yes if current candidate is eligible and no failover/rebalance selected away |
| Should users leave? | `selected_moves[]` where `current_egress=<channel>` | Yes if selected moves exist from channel |
| Why is it blocked? | `candidate.blocked[]` plus `quality_decision`, `service_suitability`, `telegram`, `capacity_decision` | Operator reason can be mapped from real blockers |
| Why is it selected? | `reason[]`, `recommended_score`, `candidates[]`, `best_available_pool` | Planner reason and target choice |
| Is execution allowed now? | `safety.authority_budget_gate`, `safety.restore_barrier`, `safety.intelligence_snapshots`, `apply_result` | Execution readiness, not assignment quality |
| Is it emergency/reserve only? | registry flags surfaced in candidate: `manual_only`, `reserve_only`, `canary_reserved`, role | Production assignment blocked unless explicit governed path |

Recommended presentation terms can be derived without a new model:

| UI Term | Existing Derivation |
| --- | --- |
| `Eligible` | eligible candidate exists and no execution-level suppression relevant to planned selected moves |
| `Keep Only` | current users exist; no selected moves away; planned assignment candidate blocked or not selected |
| `Evacuate` | selected moves from this channel > 0 |
| `Blocked` | no eligible candidate and hard blockers exist |
| `Emergency Only` | `manual_only` / `reserve_only` / `canary_reserved` production assignment block |

## 13. Gap Analysis

| Gap | Real? | Detail |
| --- | --- | --- |
| Need a new eligibility engine | No | Planner already owns eligibility and writes candidate truth. |
| Need a new score formula | No | Score is secondary; eligibility must come from hard gates first. |
| Need a new database/snapshot | No | Planner output and existing evidence files contain enough truth. |
| Need a new governance layer | No | Authority budget, restore barrier, approval packet model, and control-plane governance already exist. |
| Need UI-readable aggregation | Yes | Current admin table score is not the assignment truth and needs a read-model/adapter in a later implementation program. |
| Need human blocker labels | Yes | Existing blockers are machine reasons; operator labels should map from those reasons without changing the decision source. |
| Need per-channel summarized planner truth in admin payload | Partial | Existing planner JSON has the data, but admin UI does not currently present it as first-class channel truth. This is a presentation/API aggregation gap, not a truth-model gap. |

## 14. Recommendation

Recommendation: A. Existing truth sufficient.

Exact reuse path:

1. Treat `tools/v7-users-autoswitch` as the assignment, retention, evacuation, ranking, and selected-move authority.
2. Treat candidate `eligible=false` and `blocked[]` as the hard assignment truth.
3. Treat `selected_moves` grouped by source channel as evacuation truth.
4. Treat `selected_moves` grouped by target channel plus eligible candidates as receive-users truth.
5. Treat registry reservation flags as emergency/reserve-only truth.
6. Treat `safety.authority_budget_gate`, `safety.restore_barrier`, and `safety.intelligence_snapshots` as execution/readiness gates after planner selection.
7. Keep current `channelSuitability` only as a technical quality display until it is explicitly renamed or subordinated to planner truth.
8. In a later implementation program, build an adapter that reads existing planner output and exposes channel-level statuses; do not create a parallel decision system.

Do not implement in this program.

## 15. Final Verdict

EXISTING_TRUTH_SUFFICIENT

The real V7 eligibility model already exists. It lives in `tools/v7-users-autoswitch`, not in the current admin score. Assignment, retention, evacuation, hard blockers, ranking, selected moves, authority budget, restore barrier, and execution readiness are all already available from existing runtime/planner/governance outputs.

The gap is not truth. The gap is presentation and aggregation: the admin needs to reuse this existing truth so operators see assignment eligibility before technical score.
