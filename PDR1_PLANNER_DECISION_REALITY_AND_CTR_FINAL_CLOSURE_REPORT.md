# PROGRAM PDR.1 - Planner Decision Reality And CTR Final Closure

Дата: 2026-06-11  
Проект: V7 Vozduh  
Ветка: Updatesystem  
Режим: READ ONLY  
Финальный вердикт: **CTR_KEEP_ADVISORY**

## Executive Summary

CTR track is closed.

Root cause is proven:

1. Planner winner selection is controlled first by hard eligibility gates, then by large planner score parts.
2. CTR does not participate in real winner selection. It is attached as advisory and shadow simulation only.
3. In production samples, `vless` remained winner because it was the only eligible production candidate for the affected users.
4. `vless` was marked `DEGRADED`, but its real planner score was around `1721-1857`; CTR's simulated `DEGRADED` penalty was only `-18`.
5. TRUSTED alternatives were promoted in CTR shadow ranking, but they were already `eligible=false`; therefore they could not become winners.
6. Production planner also had snapshot stop active for `service-scores` and `channel-service-scores`, so selected moves were suppressed.

CTR should remain advisory/governance/explainability only. It should not influence planner ranking now.

Final recommendation: **CTR_KEEP_ADVISORY**

No additional CTR discovery program is required.

## Phase 1 - Planner Ownership Audit

Canonical planner owner:

- `tools/v7-users-autoswitch`

Decision chain:

```text
registry/state inputs
-> service suitability
-> routing intelligence advisory
-> CTR advisory
-> basic/reservation/org/quality/service/load/safety gates
-> score parts for eligible candidates only
-> candidate sort
-> current-vs-best decision
-> selected move picking
-> snapshot/atomic/authority/restore-barrier gates
```

Ownership map:

| Stage | Owner | Evidence |
|---|---|---|
| Candidate creation | `tools/v7-users-autoswitch` | `_candidate()` |
| Basic eligibility | `tools/v7-users-autoswitch` | `_gate_basic()` |
| Reservation/canary hold | `tools/v7-users-autoswitch` | `_gate_reservation()` |
| Org policy | `tools/v7-users-autoswitch` | `_gate_org()` |
| Quality floor | `tools/v7-users-autoswitch` | `_gate_quality()` |
| Service failures | `tools/v7-users-autoswitch` | `_gate_service()` and `_gate_service_failures()` |
| Load/capacity gate | `tools/v7-users-autoswitch` | `_gate_load()` and `_capacity_decision()` |
| Safety quarantine/reversal | `tools/v7-users-autoswitch` | `_gate_safety()` |
| Score parts | `tools/v7-users-autoswitch` | `_score_parts()` |
| Winner selection | `tools/v7-users-autoswitch` | `_decision_for_user()` |
| CTR advisory | `tools/v7-users-autoswitch` consuming CTR state | `_ctr_advisory_for_egress()` and `_attach_ctr_score_simulation()` |
| CTR shadow comparison | `tools/v7-users-autoswitch` | `_ctr_shadow_comparison()` |
| Move selection | `tools/v7-users-autoswitch` | `_select_moves()` and `_pick_projected_moves()` |
| Runtime suppression | `tools/v7-users-autoswitch` | intelligence snapshot gate / atomic envelope |

Important code facts:

- Candidates are sorted by `(eligible, score)` before CTR simulation is attached.
- CTR simulation is attached after `_mark_best_available_pool()`.
- CTR simulation sets `planner_score_applied=false`, `selected_moves_changed=false`, and `runtime_behavior_changed=false`.

## Phase 2 - Winner Selection Forensics

Real production sample:

- Source: `CTR_FINAL_EVIDENCE/dry_runs/production_dry_run_01.json`
- Users total: `26`
- Candidate rows: `182`
- Eligible candidates: `26`
- Ineligible candidates: `156`
- Recommended target for every decision: `vless`
- Candidate moves: `16`
- Selected moves: `0`

Per-channel eligibility in the sample:

| Channel | CTR State | Candidate Rows | Eligible Rows | Avg Score |
|---|---:|---:|---:|---:|
| `vless` | `DEGRADED` | 26 | 26 | ~1746 |
| `awg0` | `TRUSTED` | 26 | 0 | 0 |
| `awg3` | `TRUSTED` | 26 | 0 | 0 |
| `amneziawg-exec-20260528-10-8-1-14` | `TRUSTED` | 26 | 0 | 0 |
| `wireguard-1779454504-c43409` | `TRUSTED` | 26 | 0 | 0 |
| `1` | `QUARANTINED` | 26 | 0 | 0 |
| `openvpn-1779388847-d2ad7c` | `QUARANTINED` | 26 | 0 | 0 |

Why winner won:

- `vless` was eligible.
- It passed quality through `quality_floor_overridden_by_service_evidence`.
- Required/profile-relevant services were mostly healthy or only transient/degraded.
- Capacity was available.
- It was marked `best_available_pool_rank_1`.

Why second/third places lost:

- They were not eligible.
- Examples from production sample:
  - `awg0`: `stability_below_floor`
  - `awg3`: `stability_below_floor`
  - `amneziawg-exec-20260528-10-8-1-14`: `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `min_mbps_below_floor`, `stability_below_floor`
  - `1`: `health_code_000`, `severity_FAIL`, speed floors, Telegram hard failure

The planner did not choose between one DEGRADED eligible candidate and several healthy eligible candidates. It chose the only eligible production target.

## Phase 3 - DEGRADED Winner Analysis

`DEGRADED` remained winner because CTR state is advisory, not a hard gate.

For `vless` in production sample:

- CTR state: `DEGRADED`
- CTR reason: `current_service_signal_below_floor`
- real planner score: around `1721.65`
- CTR soft adjustment: `-18`
- simulated score: around `1703.65`
- old position: `1`
- new position: `1`

This was not an arithmetic anomaly. The penalty was far too small to overcome the planner's eligibility and score dominance.

This was also not a CTR bypass. CTR explicitly reports:

- `planner_score_applied=false`
- `hard_gate_applied=false`
- `target_suppression_applied=false`
- `selected_moves_write_authority=none`

Was the DEGRADED winner correct?

Yes, under current planner rules. The candidate was service-degraded but still eligible because the planner treats transient/service-signal degradation as warning/penalty unless it becomes persistent or required-service hard failure.

## Phase 4 - CTR Impact Forensics

CTR changed:

- shadow top-3 order;
- advisory state labels;
- operator/governance explanations;
- simulated ranking positions for ineligible TRUSTED/QUARANTINED alternatives.

CTR did not change:

- candidate eligibility;
- real candidate score;
- winner;
- selected moves;
- runtime behavior;
- governance authority;
- packet authority;
- restore barrier behavior.

Production CTR.FINAL observation:

- comparison cycles: `234`
- ranking changes: `234`
- top-3 changes: `234`
- winner changes: `0`
- pool changes: `0`
- positive changes: `0`
- negative changes: `0`
- neutral changes: `234`
- usefulness score: `50.0`
- confidence score: `100.0`

CTR impact is visible but not decision-effective.

## Phase 5 - Planner Dominance Analysis

Actual dominance order proven by code and production sample:

1. Hard eligibility gates
2. Current egress eligibility/failover path
3. Service suitability and service failure classification
4. Quality floor and evidence-backed exception
5. Load/capacity hard limits
6. Safety quarantine / pair reversal / target block
7. Score parts
8. Best available pool
9. Current-vs-best policy thresholds
10. Selected move picker and projected capacity
11. Snapshot/atomic/authority/restore-barrier gates
12. CTR shadow simulation

CTR is currently below all decision-making layers because it is not applied to the actual planner score and cannot affect eligibility.

Score dominance:

- `health`: `1000`
- service score: aggregate service suitability multiplied by `3`
- speed/stability/capacity/load/quality/priority/weight/sticky also contribute large values
- CTR current coefficient range: `+20` to `-24`

Therefore CTR is numerically too small to change winners even if it were applied, unless candidates are already very close.

## Phase 6 - Counterfactual Analysis

CTR removed entirely:

- Real planner winner: unchanged
- Selected moves: unchanged
- Runtime behavior: unchanged
- Service quality: unchanged
- User movement: unchanged
- Operator visibility: degraded
- Governance evidence: degraded

CTR applied with current coefficients:

- Winner still unchanged in observed window.
- Top-3 changes only.
- No service improvement or regression.

CTR applied with conservative/aggressive coefficients from CTR.FINAL:

- MODEL_A_CURRENT: neutral
- MODEL_B_CONSERVATIVE: neutral
- MODEL_C_AGGRESSIVE: neutral

Even aggressive coefficients did not produce winner changes in the observed window.

## Phase 7 - CTR Value Analysis

CTR has meaningful value in:

- Explainability: yes
- Governance evidence: yes
- Operator review: yes
- Channel state visibility: yes
- Recovery narrative: yes

CTR does not currently have proven value in:

- Planner winner selection
- Pool membership
- Runtime movement
- Selected move creation
- Autonomous authority

CTR should not be retired entirely because it improves operator understanding and governance evidence. But it should be retired from planner-influence ambitions until a separate future need is proven.

## Phase 8 - Final Certification

Final recommendation: **CTR_KEEP_ADVISORY**

Rejected:

- `CTR_ENABLE_SOFT_INFLUENCE`: rejected because winner changes and service improvements are zero.
- `CTR_ENABLE_SOFT_INFLUENCE_WITH_TUNING`: rejected because even aggressive coefficients were neutral.
- `CTR_RETIRE_TO_EXPLAINABILITY`: rejected because CTR still has governance/advisory value beyond simple UI text.

Certified role:

```text
CTR = advisory + explainability + governance evidence
CTR != planner influence
CTR != pool influence
CTR != runtime authority
CTR != hard gate
```

## Phase 9 - Track Closure

CTR track is closed.

Why CTR remains advisory:

- It is safe.
- It is deployed.
- It produces useful operator evidence.
- It does not bypass planner/governance.
- It did not prove measurable planner value.

Why CTR should not influence planner:

- Planner winner is dominated by eligibility and score parts.
- CTR is not applied to real score.
- CTR cannot make ineligible TRUSTED channels eligible.
- CTR current weights are too small relative to score scale.
- Production evidence showed zero winner changes and zero service improvements.
- Snapshot gate was not clean during production observation.

If planner influence is ever reconsidered, it should not be a CTR continuation program. It should be a new planner scoring calibration program with explicit scope:

- normalize score scale;
- separate eligibility from ranking;
- define service degradation semantics;
- prove clean snapshot gate first;
- run controlled shadow comparison with measurable winner/service deltas.

No additional CTR discovery programs are required.

## Final Verdicts

- planner_decision_chain_mapped: true
- winner_selection_explained: true
- degraded_winner_root_cause_known: true
- ctr_impact_quantified: true
- planner_dominance_order_known: true
- ctr_future_value_known: true
- ctr_should_influence_planner: false
- ctr_should_remain_advisory: true
- ctr_should_retire_to_explainability_only: false
- final_recommendation: CTR_KEEP_ADVISORY
- ctr_track_closed: true
- additional_ctr_discovery_required: false
- users_moved: 0
- autoswitch_apply_run: false
- routing_changed: false
- deploy_run: false
- SAFE_NEXT_STEP: close production snapshot mismatch outside CTR track; continue with planner/snapshot reliability work, not CTR discovery

