# PR.1 Planner Reality, Eligibility, Snapshot Reliability, CTR Root Cause Report

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: READ ONLY  
Generated: 2026-06-11

## 1. Executive Summary

Final root cause verdict: **MIXED_ROOT_CAUSE**.

This is not a CTR implementation failure. CTR is implemented, integrated and visible, but current planner decisions are controlled by a higher-priority chain:

1. hard eligibility gates;
2. service / quality / capacity / safety gates;
3. planner score parts;
4. move selection;
5. intelligence snapshot runtime stop gate.

CTR currently remains **advisory and shadow-only**. It explains, simulates and contributes governance evidence, but it does not create candidates, make ineligible candidates eligible, approve packets, write selected moves or mutate runtime.

Production evidence shows:

- `vless` won 26/26 decisions in the detailed production dry-run sample.
- `vless` was CTR `DEGRADED`, but it was the only eligible candidate in that sample.
- TRUSTED alternatives were excluded by hard planner blockers such as `stability_below_floor`, `min_mbps_below_floor`, `canary_reserved_production_assignment_blocked`, `manual_only` and `reserve_only`.
- CTR observation window had `234` cycles, `234` ranking/top-3 changes, but `0` winner changes.
- The snapshot gate is currently not clean: `service-scores` and `channel-service-scores` have `source_hash_mismatch:*:service_matrix` and runtime behavior `STOP`.
- Selected moves are suppressed at runtime: terminal reason `dry_run_intelligence_snapshot_stop_required`, selected moves `0`.

So the answer is:

CTR did not change winners because the planner never gave CTR decision authority, and because real winners are dominated by eligibility and score before CTR simulation. Snapshot mismatch separately prevents selected moves from materializing and must be closed before any future production decision-quality certification.

## 2. Planner Reality Map

| Stage | Owner | Inputs | Outputs | Authority |
| --- | --- | --- | --- | --- |
| Candidate Creation | `tools/v7-users-autoswitch` | users registry, egress registry, current routes | candidates per user/egress | creates candidate list |
| Eligibility | `tools/v7-users-autoswitch` candidate gates | health, role, manual/reserve/canary flags, quality, service, org, load, safety | `eligible=true/false`, blockers | hard decision gate |
| Quality Gates | `_gate_quality` | speed, min speed, stability, severity, quality history | blockers/reasons | hard or advisory depending condition |
| Service Gates | `_gate_service`, `_gate_service_failures` | required services, service matrix, route class | required service pass/fail, service score | can hard-block required service failures |
| Capacity Gates | `_gate_load`, projected load | current users, soft/hard/failover limits | load status, load penalty/block | hard block at hard limits |
| Safety Gates | `_gate_safety`, cooldown/freeze/restore state | recent switches, verification failures, restore barriers | suppressions, reasons | hard movement safety |
| Score Parts | `_score_parts` | eligible candidate data, health, service, capacity, speed, stability, RI score | numeric planner score | ranks eligible candidates |
| Pool | `_mark_best_available_pool`, best-available snapshots | ranked candidate pool | pool rank/advice | advisory/selection support |
| Winner | `_decision_for_user` | sorted candidates | recommended egress/action | planner decision owner |
| Move Selection | `_select_moves`, `_pick_projected_moves` | decisions, budget, authority, projected load | selected moves | selected move owner |
| Snapshot Gates | intelligence snapshot gate / atomic envelope | snapshot families and source hashes | stop/warn/allow | runtime stop authority |

Code evidence:

- `PR1_EVIDENCE/planner_decision_chain_code_excerpt.txt`
- `PR1_EVIDENCE/planner_candidate_gates_score_code_excerpt.txt`
- `PR1_EVIDENCE/planner_move_selection_snapshot_code_excerpt.txt`
- `PR1_EVIDENCE/ctr_shadow_comparison_code_excerpt.txt`

Key code fact:

`_decision_for_user` creates candidates, sorts by `(eligible, score)`, then attaches CTR score simulation. CTR simulation comes after real candidate ordering and does not alter planner score or selected moves.

## 3. Winner Forensics

Detailed production sample:

- Source: `CTR_FINAL_EVIDENCE/dry_runs/production_dry_run_01.json`
- Decisions: `26`
- Winner: `vless` in `26/26`
- Selected moves: `0`
- Terminal reason: `dry_run_intelligence_snapshot_stop_required`

Winner explanation:

| Winner | CTR state | Eligible | Why it won |
| --- | --- | --- | --- |
| `vless` | `DEGRADED` | `26/26` | Only eligible production target in the sample; service evidence overrode quality floor; score remained dominant. |

Why second / third places lost:

- TRUSTED candidates were not eligible in the detailed sample.
- Ineligible candidates had score `0` and could not outrank the eligible winner.
- CTR `TRUSTED +20` simulation could move top-3 ordering but could not cross eligibility gates.

Evidence:

- `PR1_EVIDENCE/winner_forensics_ctr_final_sample.json`
- `PR1_EVIDENCE/channel_eligibility_audit_ctr_final_sample.json`

## 4. Eligibility Root Cause

Production channel audit from detailed sample:

| Channel | CTR state | Eligible | Ineligible | Main blockers |
| --- | --- | ---: | ---: | --- |
| `vless` | `DEGRADED` | 26 | 0 | none |
| `awg0` | `TRUSTED` | 0 | 26 | `stability_below_floor` |
| `awg3` | `TRUSTED` | 0 | 26 | `min_mbps_below_floor`, `stability_below_floor` |
| `amneziawg-exec-20260528-10-8-1-14` | `TRUSTED` | 0 | 26 | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor` |
| `wireguard-1779454504-c43409` | `TRUSTED` | 0 | 26 | `canary_reserved_production_assignment_blocked` |
| `1` | `QUARANTINED` | 0 | 26 | health/speed/service failures |
| `openvpn-1779388847-d2ad7c` | `QUARANTINED` | 0 | 26 | health/speed/service failures |

Top blockers:

| Blocker | Count |
| --- | ---: |
| `min_mbps_below_floor` | 104 |
| `stability_below_floor` | 78 |
| `avg_mbps_below_floor` | 52 |
| `canary_reserved_production_assignment_blocked` | 52 |
| `health_code_000` | 52 |
| `severity_FAIL` | 52 |
| `telegram_required_telegram_down_14s` | 52 |
| `manual_only` | 26 |
| `reserve_only` | 26 |

Why TRUSTED channels are excluded:

CTR `TRUSTED` means the channel has favorable trust/recovery evidence. It does not mean the channel passes live planner eligibility. Current planner correctly treats operational eligibility as stronger than advisory trust.

Whether exclusion is correct:

Yes under current rules. A `TRUSTED` channel can still be manual-only, reserved, canary-reserved, too slow, unstable, or failing required services. CTR should not override those gates without a separate planner policy change.

## 5. DEGRADED Winner Analysis

`DEGRADED` remained winner because:

1. CTR state is not a hard gate.
2. CTR soft adjustment is not applied to real planner score.
3. In the detailed production sample, all TRUSTED alternatives were ineligible.
4. `vless` had service evidence sufficient for the planner to keep it usable despite degradation warnings.
5. Snapshot stop prevented selected moves from materializing, so even planned movement was blocked at runtime.

Was planner correct?

Mostly yes under current policy. The planner did not prefer a degraded channel over healthy eligible alternatives in the detailed sample. It chose the only eligible target.

What remains questionable:

The system currently allows a CTR `DEGRADED` candidate to remain winner if it passes service/quality eligibility. That is acceptable only if CTR is advisory. If the product expects CTR to affect routing, then CTR must be moved into a normalized planner influence model with explicit authority and tests.

## 6. Snapshot Reliability Audit

Current snapshot gate result:

| Family | Validation | Runtime behavior | Error |
| --- | --- | --- | --- |
| `service-scores` | false | STOP | `source_hash_mismatch:service-scores:service_matrix` |
| `channel-service-scores` | false | STOP | `source_hash_mismatch:channel-service-scores:service_matrix` |

Impact classification: **Critical**.

Impact:

- Planner visibility still exists.
- Advisory explanations still exist.
- Candidate rankings can still be inspected.
- Selected moves are blocked: selected move count `0`.
- Production decision-quality certification is distorted because no selected moves materialize while snapshot stop is active.
- CTR value cannot be fairly certified for runtime outcomes until snapshot gate is clean.

This is not a CTR bug. It is a snapshot/source reliability blocker.

Evidence:

- `PR1_EVIDENCE/snapshot_reliability_ctr_final_sample.json`
- `PR1_EVIDENCE/production_plan_summary.json`
- `PR1_EVIDENCE/truth_check_all.json`
- `PR1_EVIDENCE/convergence_status.json`

Runtime truth note:

`tools/v7-truth-check --all --json` and `tools/v7-convergence-status --json` currently return `NO-GO` because the workspace contains uncommitted report/evidence files and GitHub remote read was unavailable from this environment. Runtime deployable file hashes are reported as matching, but local/GitHub/production convergence is not clean.

## 7. Planner Dominance Analysis

Real dominance order:

1. Hard eligibility gates.
2. Required service gates.
3. Capacity and safety gates.
4. Planner score parts.
5. Current route / sticky keep logic.
6. Snapshot stop gate for selected moves.
7. CTR advisory/shadow.

CTR influence measured:

- Observation cycles: `234`
- Ranking changes: `234`
- Top-3 changes: `234`
- Winner changes: `0`
- Pool changes: `0`
- Positive service changes: `0`
- Negative service changes: `0`

Quantified conclusion:

CTR currently changes explainability/ranking simulation, not real winner selection.

## 8. Counterfactual Analysis

| Counterfactual | Expected effect | Evidence-backed conclusion |
| --- | --- | --- |
| Remove CTR | Winner remains the same in observed samples | CTR did not control winner. |
| Remove Eligibility | Winner selection could change radically | Eligibility is a primary decision driver. |
| Remove Capacity | Limited effect in current sample | Capacity was not the primary blocker for TRUSTED channels. |
| Remove Service Gates | Some failed/quarantined channels could re-enter | Unsafe; service gates are essential. |
| Remove Snapshot Stop | Selected moves could materialize if move candidates exist | Snapshot stop is runtime-critical, but not the reason CTR failed to change winner. |

True decision drivers:

- Eligibility first.
- Score second.
- Snapshot stop decides whether selected moves can proceed.
- CTR is currently non-authoritative.

## 9. CTR Reassessment

CTR is advisory because:

**D. Eligibility model dominates everything**, and also **A. CTR is inherently advisory by design**.

CTR is not useless. It has value in:

- operator explanation;
- governance evidence;
- channel trust/recovery visibility;
- review-required semantics;
- shadow comparison;
- showing when a technically winning channel is trust-degraded.

CTR should not become planner authority until:

1. snapshot gate is clean;
2. multiple healthy eligible alternatives exist in the same decision window;
3. CTR score is normalized against planner score scale;
4. CTR influence is explicitly applied only to eligible candidates;
5. shadow evidence proves winner/service quality improvement;
6. no-bypass tests remain green.

Current recommendation: **keep CTR advisory**.

## 10. Commercial System Comparison

The current dominance of hard eligibility gates is normal for commercial routing, SD-WAN and traffic-engineering systems.

Commercial systems usually separate:

- hard eligibility / health / policy exclusion;
- SLA and service-quality gates;
- capacity and safety constraints;
- scoring / ranking;
- trust / reputation / recovery confidence.

What is normal:

- A trusted path can be excluded if it is reserved, overloaded, unstable, too slow, manually locked or failing required services.
- A degraded path can remain in service if all alternatives are worse or unavailable and the path still satisfies minimum SLA.
- advisory trust should not override health and safety gates.

What is not ideal:

- CTR coefficients are not normalized to planner score scale.
- Snapshot mismatch blocks runtime selection and clouds certification.
- Operator language can make `TRUSTED` sound like `eligible`, which is not true.

Commercial-style conclusion:

V7's gate-first model is directionally correct. The missing maturity is cleaner state vocabulary and clean snapshot reliability, not forcing CTR into planner authority.

## 11. Final Root Cause

Final verdict: **MIXED_ROOT_CAUSE**.

Root cause components:

1. **Planner correct under current rules**: hard eligibility and score dominate, and CTR is not authorized to override them.
2. **Eligibility is strict but mostly justified**: TRUSTED channels were excluded for operational reasons, not because CTR failed.
3. **Snapshot layer is blocking runtime materialization**: `service-scores` and `channel-service-scores` source mismatches produce STOP.
4. **CTR valuable but suppressed by design**: CTR contributes evidence and simulation, but not real score or eligibility.

Rejected verdicts:

- `CTR_NOT_VALUABLE`: rejected. CTR has explainability/governance value.
- `PLANNER_CORRECT` alone: incomplete because snapshot stop is a real critical blocker.
- `SNAPSHOT_LAYER_BLOCKING` alone: incomplete because snapshot stop does not explain CTR zero winner changes.
- `ELIGIBILITY_TOO_STRICT` alone: not proven. Some eligibility rules may need calibration, but current exclusions have valid blockers.

## 12. Recommended Next Program

Exact next direction:

**PROGRAM SNAP.1 - Service Matrix Snapshot Source Reliability and Pre-Planner Refresh Closure**

Goal:

Close `service-scores` and `channel-service-scores` source hash mismatch so planner dry-runs and runtime selected-move gates can become clean again.

Scope:

- read current service matrix writer;
- trace source hashes for service matrix, service scores and channel service scores;
- verify refresh order;
- prove whether mismatch is stale snapshot, volatile writer timing, schema/hash contract mismatch or missing pre-planner refresh;
- apply only safe snapshot refresh / hash contract fix if proven;
- retest with production dry-run;
- require `snapshot_stop_required=false` and empty `source_mismatch_families`.

After SNAP.1:

Run **PROGRAM ELIG.1 - Planner Eligibility Language and Policy Calibration** only if needed.

ELIG.1 should not weaken gates blindly. It should clarify operator semantics:

- `TRUSTED` means trust/recovery state;
- `eligible` means currently routeable;
- `DEGRADED but eligible` means routeable with warning;
- `TRUSTED but ineligible` means trusted historically but blocked now.

No further CTR discovery program is required.

## 13. Final Verdict

- planner_decisions_fully_explained: true
- eligibility_behavior_fully_explained: true
- snapshot_issues_fully_explained: true
- ctr_role_fully_explained: true
- final_root_cause: MIXED_ROOT_CAUSE
- planner_correct_under_current_rules: true
- eligibility_too_strict: not_proven
- snapshot_layer_blocking: true
- ctr_not_valuable: false
- ctr_valuable_but_suppressed: true
- ctr_final_role: KEEP_ADVISORY
- no_more_planner_ctr_discovery_required: true
- recommended_next_program: PROGRAM SNAP.1 - Service Matrix Snapshot Source Reliability and Pre-Planner Refresh Closure
- users_moved: 0
- apply_executed: false
- routing_changed: false
- score_changed: false
- eligibility_changed: false
- deploy_executed: false
