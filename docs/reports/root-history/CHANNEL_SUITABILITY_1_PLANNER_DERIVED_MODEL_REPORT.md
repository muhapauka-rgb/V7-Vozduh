# CHANNEL.SUITABILITY.1 Planner-Derived Suitability Model Report

Project: V7 VOZDUH
Program: CHANNEL.SUITABILITY.1_PLANNER_DERIVED_SUITABILITY_MODEL
Date: 2026-06-15

Final Verdict: MODEL_DERIVABLE

This report is discovery and model only. No code, UI, planner, governance, storage, snapshot, database, execution, or runtime changes were made.

## 1. Saved State

| Check | Result |
| --- | --- |
| Branch | Updatesystem |
| Local HEAD | e6e854e3 Add channel accordion validation report |
| Git status before report | Untracked docs handoff only: `V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` |
| New runtime state created | No |
| New planner run created | No |
| UI changed | No |
| Score implemented | No |

Reason for not creating new production planner evidence: the prompt forbids new storage/snapshots and implementation. This report uses existing production evidence from CHANNEL_TRUTH_1/2/3/4, planner preview evidence, selected moves evidence, candidate evidence, governance reports, service matrix analysis, and current production UI observations already captured in the project history.

## 2. Truth Gate

Pre-report verification:

| Gate | Status | Evidence |
| --- | --- | --- |
| Local | PASS | `tools/v7-truth-check --all --json` |
| GitHub | PASS | Remote branch `Updatesystem` read successfully after network-enabled gate |
| Runtime | PASS | Runtime access ready; docs-only local/runtime mismatch accepted |
| Truth | PASS | `final_verdict=PASS` |
| Convergence | PASS | `tools/v7-convergence-status --json`, `status=ALIGNED` |

Initial sandbox-only gate returned `github_remote_unreadable`; rerun with network access passed. This was treated as environment access noise, not a V7 blocker.

## 3. Real Planner Behavior

Actual planner behavior is not the same as the current channel table score. The planner pipeline is:

1. Build a candidate for every channel per user.
2. Apply hard gates.
3. If a candidate is not eligible, return it with score `0` and no `score_parts`.
4. Only eligible candidates receive `score_parts`.
5. Sort candidates by `(eligible, score)`.
6. Select the best eligible target for failover, planned switch, reconnect rotation, or rebalance.
7. Convert decisions into selected moves, then apply governance, restore, and authority gates.

Evidence from `tools/v7-users-autoswitch`:

| Planner Step | Code Owner | Behavior |
| --- | --- | --- |
| Candidate construction | `_candidate` | Runs basic, reservation, org, quality, service, load, and safety gates before score |
| Ranking | `_decision_for_user` | Sorts by `(eligible, score)`; ineligible candidates cannot outrank eligible candidates |
| Selected target | `_decision_for_user` | Uses failover when current egress is not eligible |
| Evacuation source | `_select_moves` plus selected move evidence | Sources are current egresses with selected moves away |
| Score parts | `_score_parts` | Applied only after hard gates pass |

Production planner preview evidence:

| Metric | Value |
| --- | --- |
| Active users | 26 |
| Egress rows | 7 |
| Healthy egress total | 1 |
| Candidate moves | 18 |
| Selected moves | 18 |
| Selected target | `wireguard-1779454504-c43409` for 18 moves |
| Selected sources | `vless` 10, `awg3` 8 |

Per-channel reality:

| Channel | Selected Target? | Selected Source? | Eligible? | Blocked? |
| --- | --- | --- | --- | --- |
| `wireguard-1779454504-c43409` | Yes, 18 moves | No; current users kept | Yes | No observed blockers |
| `vless` | No | Yes, 10 moves | No | Yes: `min_mbps_below_floor`, `stability_below_floor` |
| `awg3` | No | Yes, 8 moves | No | Yes: `stability_below_floor` |
| `awg0` | No | No | No | Yes: `min_mbps_below_floor`, `stability_below_floor` |
| `1` | No | No | No | Yes: `health_code_000`, `severity_FAIL`, speed floors, Telegram down |
| `openvpn-1779388847-d2ad7c` | No | No | No | Yes: `health_code_000`, `severity_FAIL`, speed floors, Telegram down |
| `amneziawg-exec-20260528-10-8-1-14` | No | No | No for normal assignment | Yes: `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor` |

Key conclusion: current UI quality score can say `92/100`, but planner truth can still say `eligible=false`. Planner-derived suitability must therefore be gate-first, not weighted-score-first.

## 4. Planner Factor Inventory

| Factor | Used By Planner? | Source | Importance Evidence |
| --- | --- | --- | --- |
| Enabled/state/manual/quarantine | Yes | `_gate_basic` | Hard blocks before score |
| Health code | Yes | `_gate_basic` | `health_code_000` blocks `1` and OpenVPN |
| Severity classification | Yes | `_gate_basic` | `severity_FAIL` blocks `1` and OpenVPN |
| Reserve only | Yes | `_gate_basic` | Blocks planned assignment |
| Canary reserved | Yes | `_gate_reservation` | Blocks production assignment unless current hold exception applies |
| Group constraints | Yes | `_gate_org` | Can block incompatible user/channel combinations |
| Speed average floor | Yes | `_gate_quality` | `avg_mbps_below_floor` hard blocks unusable channels |
| Speed minimum floor | Yes | `_gate_quality` | `min_mbps_below_floor` blocks `vless`, `awg0`, `1`, OpenVPN |
| Stability floor | Yes | `_gate_quality` | `stability_below_floor` blocks `vless`, `awg0`, `awg3`, emergency channels |
| Quality history | Yes | `_gate_quality`, `_score_parts` | Can block or add score through fail rate and stability trend |
| Required services | Yes | `_gate_service` | Missing required evidence or hard service failure blocks |
| Telegram sentinel | Yes | `_telegram_candidate_state`, `_gate_service` | `telegram_required_telegram_down_14s` blocks `1` and OpenVPN |
| Route class fitness | Yes | `_gate_service` | Persistent route-class failure blocks; nonpersistent failure is advisory |
| Capacity/load | Yes | `_gate_load`, `_score_parts` | Hard-full blocks; load/capacity influence eligible ranking |
| Safety/freeze/reversal | Yes | `_gate_safety`, `_cooldown_ok`, `_user_frozen` | Can block or suppress moves after candidate quality |
| Service suitability | Yes | `_service_scores` | High weight in eligible score; also required-service gate |
| Latency | Yes | `_service_scores` | Eligible ranking factor |
| Runtime readiness | Yes | Basic health, severity, runtime/gov gates | Runtime failures can block assignment or execution |
| Trust/recovery advisory | Limited | CTR advisory simulation | Dry-run/advisory; score not currently applied to selected moves |
| Routing intelligence | Conditional | `_routing_intelligence_candidate_advice` | Applied only if `planner_influence_active` is true |
| Sticky current route | Yes | `_score_parts`, `_decision_for_user` | Current channel gets sticky score; move still occurs if current is ineligible |
| Priority/weight | Yes | `_score_parts` | Ranking among eligible candidates |
| Best available pool | Yes | `_mark_best_available_pool` | Marks eligible top candidates; does not rescue blocked channels |
| Governance/restore/authority | Yes | plan gates | Can suppress selected moves even after planner chooses them |

## 5. Target Channel Analysis

Question: why did planner choose `wireguard-1779454504-c43409` instead of `awg0`, `awg3`, or `vless`?

| Candidate | Reason Selected | Reason Rejected |
| --- | --- | --- |
| `wireguard-1779454504-c43409` | Only eligible production target in the preview; no hard blockers; best available pool rank 1; score around `2209-2259` depending sticky/current context | Not rejected |
| `awg0` | Not selected | Ineligible before score: `min_mbps_below_floor`, `stability_below_floor`; service checks are OK but speed floor collapses |
| `awg3` | Not selected | Ineligible before score: `stability_below_floor`; selected as source for 8 moves |
| `vless` | Not selected | Ineligible before score: `min_mbps_below_floor`, `stability_below_floor`; selected as source for 10 moves |

Important correction to the current UI intuition:

| Channel | UI-looking Quality | Planner Candidate Score | Planner Truth |
| --- | --- | --- | --- |
| `awg0` | High, shown historically around `92/100` | `0` in planner preview because hard-gated | Do not assign |
| `wireguard-1779454504-c43409` | Medium, shown historically around `72/100` | `2209+` when eligible | Use / selected target |

The planner rewards operational eligibility first. A high service/trust-looking score without stable speed floor is not enough.

## 6. Source Channel Analysis

| Channel | Evacuation Cause | Evidence |
| --- | --- | --- |
| `vless` | Current egress is not eligible; planner failover found eligible target | 10 selected moves from `vless` to `wireguard-1779454504-c43409`, reason `current_egress_not_eligible`; blockers `min_mbps_below_floor`, `stability_below_floor` |
| `awg3` | Current egress is not eligible; planner failover found eligible target | 8 selected moves from `awg3` to `wireguard-1779454504-c43409`, reason `current_egress_not_eligible`; blocker `stability_below_floor` |

Evacuation is not a visual label invented by admin. It is a planner decision: current channel cannot keep users safely under current evidence and a valid target exists.

## 7. Hard Gate Model

Hard gates are not score. They override score.

| Gate | Effect |
| --- | --- |
| Disabled / maintenance / quarantine | Candidate cannot receive users |
| Manual only | Candidate cannot be normal production target; classify as Emergency Only |
| Reserve only | Candidate cannot be planned assignment target; classify as Emergency Only |
| Canary reserved | Candidate cannot be normal production target except current-hold handling |
| Bad health code | Candidate blocked |
| Hard severity failure | Candidate blocked |
| Org/group/exclusive constraints | Candidate blocked for incompatible users |
| Average Mbps below floor | Candidate blocked for assignment/retention |
| Minimum Mbps below floor | Candidate blocked for assignment/retention |
| Stability below floor | Candidate blocked for assignment/retention |
| Required service evidence unknown | Candidate blocked when service is explicit/required |
| Required Telegram down | Candidate blocked for Telegram-required routes |
| Persistent service failure | Candidate blocked |
| Route class persistent failure | Candidate blocked |
| Planned/failover hard full | Candidate blocked for target purpose |
| Safety quarantine / target blocked for user | Candidate blocked |
| Cooldown/frozen user | Move suppressed even when a better target exists |
| Restore barrier / authority budget / governance | Selected moves can be suppressed after planner selection |

Model implication:

```
if hard_gate_failed:
    target_suitability = 0
    expose status = Blocked / Evacuate / Emergency Only
else:
    target_suitability = normalized planner preference among eligible candidates
```

## 8. Suitability Model Draft

The model is derivable only if it remains purpose-specific:

| Suitability Purpose | Meaning |
| --- | --- |
| Receive users now | Probability that planner would choose this channel as a target now |
| Keep current users | Probability that planner would let existing users safely remain |
| Evacuate source | Probability that planner wants users moved away from this channel |
| Emergency use | Channel is operationally restricted to manual/reserve/canary scenarios |

This cannot be a single static "channel goodness" number. It must be a planner-derived, current-state, purpose-scoped suitability.

Draft scoring after hard gates:

| Component | Weight | Evidence |
| --- | --- | --- |
| Services and required service suitability | 20 | `_service_scores`; service aggregate multiplied heavily in planner score; required service failures can hard-block |
| Stability and speed floor strength | 25 | `min_mbps_below_floor` and `stability_below_floor` are dominant blockers for `vless`, `awg0`, `awg3`; speed and stability are large score parts after gates |
| Capacity/load | 10 | `_gate_load`, `load`, `capacity`; affects hard-full and tie/ranking after eligibility |
| Route class fitness | 10 | `_route_class_fitness`; persistent failures block, OK route adds confidence |
| Runtime health/severity readiness | 10 | health and severity hard-block before score |
| Priority/weight/sticky/org preference | 10 | planner score includes priority, weight, sticky, org preference; explains keep vs move among eligible choices |
| Quality history | 5 | fail rate, trend, and 1h stability affect score and warnings |
| Trust/recovery/routing intelligence | 5 | advisory or conditional planner influence; currently not enough to override hard gates |
| Planner preference evidence | 5 | selected target, best available pool rank, selected-source evidence calibrate the displayed score to real planner behavior |

Total: 100.

Hard gates remain outside the 100 points. A gated channel must not display a high assignment suitability score just because its service component is high.

Recommended formula shape:

```
gate_state = derive_gate_state(candidate, purpose)

if gate_state in ["blocked", "emergency_only"]:
    suitability_score = 0
    suitability_label = gate_state
else:
    raw = weighted_sum(score_components)
    rank_boost = selected_target_or_best_pool_adjustment
    suitability_score = normalize_against_eligible_pool(raw + rank_boost)
```

For evacuation:

```
evacuation_score = 100 when selected_moves source channel exists
evacuation_score = high when current candidate is not eligible and eligible failover exists
evacuation_score = 0 when current channel is eligible and kept
```

## 9. Replay Validation

Replay against production planner preview:

| Channel | Draft Receive-Users Score | Planner Rank | Match |
| --- | --- | --- | --- |
| `wireguard-1779454504-c43409` | 100 after normalization among eligible targets | Rank 1, selected target for 18 moves | Yes |
| `vless` | 0 for target suitability | Ineligible; selected source for 10 moves | Yes |
| `awg3` | 0 for target suitability | Ineligible; selected source for 8 moves | Yes |
| `awg0` | 0 for target suitability | Ineligible; no selected target | Yes |
| `1` | 0 for target suitability | Ineligible; health/severity/service blockers | Yes |
| `openvpn-1779388847-d2ad7c` | 0 for target suitability | Ineligible; health/severity/service blockers | Yes |
| `amneziawg-exec-20260528-10-8-1-14` | 0 for normal target suitability; Emergency Only role | Ineligible for normal assignment | Yes |

Replay against source/evacuation purpose:

| Channel | Draft Evacuation Score | Planner Source Role | Match |
| --- | --- | --- | --- |
| `vless` | 100 | Selected source for 10 moves | Yes |
| `awg3` | 100 | Selected source for 8 moves | Yes |
| `wireguard-1779454504-c43409` | 0 | Current users kept; selected target | Yes |
| `awg0` | 0 current evacuation because no current users, but target blocked | No source moves | Yes |

## 10. Mismatch Analysis

| Channel | Draft | Planner | Cause |
| --- | --- | --- | --- |
| `awg0` | Receive-users suitability 0 despite high technical-looking UI score | Planner blocks | Speed floor and stability floor are hard gates; services alone are not enough |
| `wireguard-1779454504-c43409` | Receive-users suitability 100 in current pool | Planner selects | Only eligible target; strong stability, no hard blockers |
| `vless` | Target suitability 0, evacuation 100 | Planner evacuates | Current egress not eligible; speed/stability floors fail |
| `awg3` | Target suitability 0, evacuation 100 | Planner evacuates | Stability floor fails |
| `amneziawg-exec-20260528-10-8-1-14` | Normal suitability 0; Emergency Only | Planner blocks normal assignment | Manual/reserve/canary gates override high service/technical appearance |

Core mismatch: previous UI score behaved like a technical quality/suitability blend. Planner truth behaves like:

```
Can this channel be used for this purpose now?
If yes, how strongly does planner prefer it?
If no, why is it blocked or why must users leave?
```

This explains the user-facing contradiction where `awg0` can look highly rated while historically and currently unsafe for automatic assignment.

## 11. Final Formula Recommendation

Can suitability become "Probability that planner wants this channel"?

Answer: Yes, with constraints.

The correct name is not generic "Channel Score". The correct model is:

`Planner Suitability = probability that V7 planner would choose or keep this channel for a specific purpose in the current evidence window.`

Required model contract:

| Requirement | Decision |
| --- | --- |
| Derived from existing planner truth | Required |
| Hard gates outside numeric score | Required |
| Purpose-specific score | Required |
| Current-state/time-window specific | Required |
| Normalized among eligible candidates | Required |
| Selected moves used as validation/calibration | Required |
| Existing UI technical score reused as input only | Allowed |
| New planner | Forbidden |
| New truth source | Forbidden |

Recommended output fields for future implementation:

| Field | Meaning |
| --- | --- |
| `planner_suitability_score` | 0-100 normalized planner preference for a purpose |
| `planner_suitability_purpose` | receive_users / keep_current_users / evacuate_source / emergency_use |
| `gate_state` | eligible / blocked / emergency_only / evacuate / keep_only |
| `hard_blockers` | Human-readable hard blockers |
| `planner_rank` | Rank among eligible candidates |
| `selected_target_count` | Number of selected moves targeting channel |
| `selected_source_count` | Number of selected moves leaving channel |
| `source_evidence` | Existing candidate/selected-move evidence pointers |

Recommended display principle:

| Bad | Good |
| --- | --- |
| `92/100` with hidden planner blocker | `Blocked for assignment: stability below required level` |
| `Excellent` when planner will not assign | `Cannot receive users now` |
| One universal quality number | Purpose-scoped planner suitability |
| Services first | Assignment truth first, details second |

## 12. Future UI Recommendation

Future channel UI should separate three ideas:

| Layer | Operator Meaning | Example |
| --- | --- | --- |
| Planner suitability | Can V7 use this channel now? | Use, Keep Only, Evacuate, Blocked, Emergency Only |
| Technical quality | How good are services/speed/capacity technically? | Services OK, speed unstable |
| Evidence | Why did planner decide this? | Stability below required level |

Screen/table recommendation:

| Column | Purpose |
| --- | --- |
| Channel | Object identity |
| Planner Suitability | Primary truth: Use / Evacuate / Blocked / Emergency Only |
| Score | Planner-derived 0-100 for current purpose, not generic quality |
| Main Blocker | Human-readable hard gate if score is 0 |
| Users | Current exposure |
| Action | One operator action |

Critical UI rule:

If a hard gate is active, numeric score must visually submit to the gate. Example:

```
awg0
Cannot receive users
Reason: Stability below required level
Technical quality: Services OK
```

This prevents the exact confusion seen in production: high-looking `awg0` rating while planner truth rejects assignment.

## 13. Final Verdict

MODEL_DERIVABLE

The final channel suitability model is derivable from actual V7 planner behavior if it is built as a gate-first, purpose-specific, planner-derived model.

It must not be a generic technical score. The planner already tells us what it rewards and punishes:

| Planner Rewards | Planner Punishes |
| --- | --- |
| Eligibility after all hard gates | Failed speed floors |
| Strong stability and minimum speed | Stability below floor |
| Required services and route class OK | Required service failures |
| Available capacity | Hard/full capacity |
| Runtime health and safe severity | Bad health/severity |
| Best available eligible pool rank | Manual/reserve/canary production restrictions |
| Current route only when still safe | Current route becoming ineligible |

The next implementation should reuse `v7-users-autoswitch` candidate truth, selected moves, blockers, best available pool rank, and governance output. It should not invent weights independently of planner behavior.

Alignment state at report creation:

| Check | Status |
| --- | --- |
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS |
| Truth | PASS |
| Convergence | PASS |
