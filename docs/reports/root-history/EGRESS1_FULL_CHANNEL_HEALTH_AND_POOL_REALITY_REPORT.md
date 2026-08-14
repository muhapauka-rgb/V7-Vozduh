# EGRESS.1 - Full Channel Health, Eligibility, And Planner Pool Reality Audit

Дата: 2026-06-13  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: READ ONLY. No apply, no routing changes, no policy changes, no eligibility changes, no autonomy changes, no deploy.

## 1. Channel Inventory

Evidence:

- `docs/reports/evidence/EGRESS1_EVIDENCE/channel_inventory_health_eligibility.json`
- `docs/reports/evidence/EGRESS1_EVIDENCE/channel_inventory_health_eligibility.csv`
- `docs/reports/evidence/EGRESS1_EVIDENCE/source_stability1_close_phase6_fresh_planner.json`

Planner-visible pool contains 7 channels.

| Channel | Protocol | Role | Users | Eligible | State |
|---|---|---|---:|---|---|
| `vless` | vless | `GLOBAL_FAST` | 23 | true | only healthy planner channel |
| `awg0` | amneziawg | `GLOBAL_STABLE` | 2 | false | service OK, stability below floor |
| `awg3` | amneziawg | `GLOBAL_STABLE` | 1 | false | service almost OK, stability below floor |
| `wireguard-1779454504-c43409` | wireguard | `GLOBAL_FAST` | 0 | false | healthy but canary-reserved |
| `amneziawg-exec-20260528-10-8-1-14` | amneziawg | `EXECUTION_ONLY` | 0 | false | manual/reserve/canary blocked + unstable |
| `1` | unknown | `GLOBAL_FAST` | 0 | false | hard health/service failure |
| `openvpn-1779388847-d2ad7c` | openvpn | `GLOBAL_FAST` | 0 | false | hard health/service failure |

Truth note:

- `tools/v7-truth-check --all --json` returned overall `NO-GO` because this sandbox could not read GitHub remote branch.
- Local truth was `PASS`.
- Runtime truth section was `PASS`, `runtime_access_status=READY`, `runtime_truth_status=KNOWN`.
- Channel diagnosis uses the latest production BA.3 blocker planner evidence from `docs/reports/evidence/STABILITY1_CLOSE_EVIDENCE/phase6_fresh_planner.json`.

## 2. Health Audit

| Channel | Health severity | Service score | Telegram | 1h avg Mbps | 1h min Mbps | 1h stability | Health interpretation |
|---|---|---:|---|---:|---:|---:|---|
| `vless` | `SUSPECT` | 100.0 | OK | 41.596 | 27.47 | 0.4814 | usable; protocol diagnostic suspect is not hard-blocking |
| `awg0` | `OK` | 100.0 | OK | 35.875 | 14.199 | 0.2162 | service OK but unstable |
| `awg3` | `OK` | 99.767 | OK | 37.137 | 13.068 | 0.1836 | service OK but unstable |
| `wireguard-1779454504-c43409` | `OK` | 100.0 | OK | 59.982 | 56.562 | 0.8216 | healthy but reserved |
| `amneziawg-exec-20260528-10-8-1-14` | `OK` | 100.0 | OK | 40.49 | 13.732 | 0.1567 | role-blocked and unstable |
| `1` | `FAIL` | 2.834 | down | 8.398 | 8.398 | 0.0002 | real failure |
| `openvpn-1779388847-d2ad7c` | `FAIL` | 2.838 | down | 0.002 | 0.002 | 0.0002 | real failure |

The important part: `awg0` and `awg3` are not failing service suitability. Their services are OK. They are blocked by stability.

## 3. Eligibility Audit

| Channel | Eligible | Exact blockers |
|---|---|---|
| `vless` | true | none |
| `awg0` | false | `stability_below_floor` |
| `awg3` | false | `stability_below_floor` |
| `wireguard-1779454504-c43409` | false | `canary_reserved_production_assignment_blocked` |
| `amneziawg-exec-20260528-10-8-1-14` | false | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor` |
| `1` | false | `health_code_000`, `severity_FAIL`, `avg_mbps_below_floor`, `min_mbps_below_floor`, `telegram_required_telegram_down_14s` |
| `openvpn-1779388847-d2ad7c` | false | `health_code_000`, `severity_FAIL`, `avg_mbps_below_floor`, `min_mbps_below_floor`, `telegram_required_telegram_down_14s` |

## 4. Why Only One Healthy Channel

Direct answer: V7 currently has only one healthy planner channel because only `vless` passes eligibility for production routing.

Excluded channels:

| Channel | Why excluded? | Real problem? | Policy/threshold? | Temporary? |
|---|---|---|---|---|
| `awg0` | `stability_below_floor` | yes, observed stability is low | threshold is doing its job | likely temporary/recoverable |
| `awg3` | `stability_below_floor` | yes, observed stability is low | threshold is doing its job | likely temporary/recoverable |
| `wireguard-1779454504-c43409` | canary-reserved | no health problem proven | governance reservation | recoverable by approval/certification |
| `amneziawg-exec-20260528-10-8-1-14` | manual/reserve/canary + stability | mixed | role and stability block | not production-pool ready |
| `1` | hard fail + Telegram down + speed floors | yes | not a threshold-only issue | unknown until repaired |
| `openvpn-1779388847-d2ad7c` | hard fail + Telegram down + speed floors | yes | not a threshold-only issue | unknown until repaired |

## 5. Channel History

Evidence available in planner quality windows:

- 1h quality metrics are present for every channel.
- 7d window details are present inside `source_stability1_close_phase6_fresh_planner.json`.
- CTR/trust state is present per candidate where available.

Classification from current evidence:

| Channel | Current history signal | Recovery state |
|---|---|---|
| `vless` | enough stability to pass floor with service evidence exception | healthy |
| `awg0` | good services, low 1h stability | temporarily degraded |
| `awg3` | good services, low 1h stability | temporarily degraded |
| `wireguard-1779454504-c43409` | strong health/stability but canary-reserved | healthy but blocked |
| `amneziawg-exec-20260528-10-8-1-14` | services OK but low stability and execution-only role | blocked/review required |
| `1` | hard fail and Telegram down | bad |
| `openvpn-1779388847-d2ad7c` | hard fail and Telegram down | bad |

## 6. Counterfactual Analysis

Evidence:

- `docs/reports/evidence/EGRESS1_EVIDENCE/counterfactual_analysis.json`

Diagnostic only; no runtime changes were made.

| Scenario | Channels that would be available | Meaning |
|---|---|---|
| Current eligibility | `vless` only | BA.3 remains blocked: only 3 real candidates |
| Ignore stability floor only | likely `vless`, `awg0`, `awg3` | would likely restore BA.3-style rebalance pool, but this would be unsafe without proof |
| Ignore trust only | no change | no channel was blocked by trust/CTR in current evidence |
| Ignore canary reservation only | adds `wireguard-1779454504-c43409` | health is good, but governance reservation is intentional |

Conclusion: the main practical limiter is stability floor on `awg0`/`awg3`, not trust and not planner candidate accounting.

## 7. Planner Impact

Evidence:

- `docs/reports/evidence/EGRESS1_EVIDENCE/planner_impact.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase3_fresh_planner.json`
- `docs/reports/evidence/STABILITY1_CLOSE_EVIDENCE/phase6_fresh_planner.json`

Current:

- healthy pool: `vless`
- candidate moves: 3
- BA.3 readiness: false
- reason: BA.3 needs 5 real planner candidates; only 3 failovers exist.

Recovered `awg0`/`awg3` scenario:

- healthy pool would become approximately `vless`, `awg0`, `awg3`;
- original BA.3 reference had `candidate_moves_total=23`;
- BA.3 would likely become possible again if fresh planner confirms `candidate_moves_total >= 5`.

Reserved WireGuard scenario:

- `wireguard-1779454504-c43409` is healthy but canary-reserved;
- it should not be silently added to production routing without governance review.

## 8. Root Cause Classification

| Channel | Classification | Reason |
|---|---|---|
| `vless` | `HEALTHY` | eligible, best available pool, service score 100 |
| `awg0` | `TEMPORARY_FAILURE` | service OK, but stability `0.2162 < 0.45` |
| `awg3` | `TEMPORARY_FAILURE` | service OK, but stability `0.1836 < 0.45` |
| `wireguard-1779454504-c43409` | `CANARY_BLOCKED` | healthy, but production assignment blocked by canary reservation |
| `amneziawg-exec-20260528-10-8-1-14` | `MANUAL_BLOCKED` | execution-only/manual/reserve/canary plus low stability |
| `1` | `REAL_FAILURE` | hard health fail, Telegram down, speed floors fail |
| `openvpn-1779388847-d2ad7c` | `REAL_FAILURE` | hard health fail, Telegram down, speed floors fail |

No `MISCLASSIFIED` channel was proven.

## 9. Recovery Plan

Do not implement inside EGRESS.1.

Recommended recovery path:

| Channel | Recovery path |
|---|---|
| `awg0` | observe/retest quality window; run service/health audit; if stability recovers above `0.45`, rerun planner; do not lower floor blindly |
| `awg3` | observe/retest quality window; run service/health audit; if stability recovers above `0.45`, rerun planner; do not lower floor blindly |
| `wireguard-1779454504-c43409` | separate governance review for canary reservation; if approved, certify as production pool member |
| `amneziawg-exec-20260528-10-8-1-14` | role/purpose review first; then stability certification; not a normal pool channel today |
| `1` | repair interface/connectivity/Telegram reachability; rerun service matrix; only then planner |
| `openvpn-1779388847-d2ad7c` | repair interface/connectivity/Telegram reachability; rerun service matrix; only then planner |

## 10. Final Verdict

Final answer: the channel pool is genuinely degraded for planner purposes.

It is not proven that Planner/Eligibility is classifying too aggressively. The eligibility model is doing what it is supposed to do:

- hard-failed channels are excluded;
- reserved/canary channels are excluded;
- channels with good services but unstable recent quality are excluded until stability recovers.

The immediate BA.3 blocker is not a planner bug. It is insufficient healthy eligible pool:

- `healthy_egress_total=1`
- `candidate_moves_total=3`
- `BA3_READY=false`

Final verdicts:

| Verdict | Value |
|---|---|
| channel_pool_genuinely_degraded | true |
| planner_overaggressive_classification_proven | false |
| eligibility_misclassification_found | false |
| only_healthy_planner_channel | `vless` |
| awg0_recoverable | true |
| awg3_recoverable | true |
| hard_failed_channels | `1`, `openvpn-1779388847-d2ad7c` |
| healthy_but_governance_blocked_channel | `wireguard-1779454504-c43409` |
| ba3_safe_to_rerun_now | false |
| users_moved | 0 |
| apply_executed | false |
| routing_changed | false |
| policy_changed | false |
| deploy_executed | false |
| SAFE_NEXT_STEP | `CHANNEL_STABILITY_RECOVERY_WINDOW_FOR_AWG0_AWG3_THEN_RERUN_BA3_PLANNER` |

