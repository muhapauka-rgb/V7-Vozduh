# CTR.I4 Shadow Comparison Window Report

## 1. Executive Summary

CTR.I4 is complete.

Final verdict: CTR_POSITIVE_VALUE.

CTR shadow comparison now measures whether CTR-simulated ranking would improve planner decisions. It does this using real planner candidate output from each dry-run plan, without changing production score, planner ranking, selected moves, routing, governance, packets, restore barriers, or runtime behavior.

No users were moved. No autoswitch apply was run. No deploy was run.

## 2. Reality Audit

CTR.I3 was still present:

- candidate-level CTR advisory
- dry-run score simulation
- ranking delta fields

CTR was still not applied to:

- production score
- `_score_parts`
- planner ranking
- selected moves
- runtime routing

No existing production CTR influence was found.

## 3. Shadow Comparison Results

Implemented:

- `ctr_shadow_comparison`

For every planner cycle it captures:

- `current_ranking`
- `ctr_simulated_ranking`
- `winner_without_ctr`
- `winner_with_ctr`
- `same_winner`
- `different_top3`
- `different_pool_order`
- `quality_delta`
- `service_aware_validation`

## 4. Ranking Delta Analysis

The comparison reads existing CTR.I3 fields:

- rank before
- rank after
- ranking delta
- existing score
- simulated score
- CTR soft adjustment

It does not feed the simulated ranking back into the planner.

## 5. Service-Aware Analysis

CTR.I4 tracks service-aware impact for:

- Telegram
- YouTube
- Instagram
- ChatGPT
- Google

Current implementation uses the candidate aggregate service suitability available in the planner output. If a future per-service planner output becomes available, this can be extended without changing the runtime path.

## 6. Pool Analysis

CTR.I4 measures:

- top candidate changes
- top 3 changes
- best available pool order changes
- pool membership changes

Pool membership is not recomputed by CTR.I4 because that would create a second pool owner. The program only compares current pool order against simulated CTR order.

## 7. Decision Quality Analysis

CTR.I4 separates:

- service suitability improvement/regression
- overall decision quality improvement/regression

This matters because CTR may improve a decision through trust/recovery evidence while service suitability remains unchanged.

The validation fixture proved a useful case:

- current winner: current channel
- CTR simulated winner: trusted channel
- service suitability: neutral
- decision quality: improved through trust/recovery
- selected moves: unchanged

## 8. CTR State Analysis

The shadow comparison tracks candidate movement by CTR state:

- TRUSTED promoted/demoted/unchanged
- WATCH promoted/demoted/unchanged
- NEW promoted/demoted/unchanged
- RECOVERING promoted/demoted/unchanged
- DEGRADED promoted/demoted/unchanged
- QUARANTINED promoted/demoted/unchanged
- UNKNOWN promoted/demoted/unchanged

This allows later evidence-based review of which CTR states are useful, neutral, or harmful.

## 9. Readiness Review

Current readiness:

- shadow scoring: READY
- governance influence: READY
- soft score application: NEEDS_MORE_DATA
- pool influence: NEEDS_MORE_DATA
- planner influence: NOT_READY

Reason:

CTR shadow comparison can now show value, but one implementation-stage proof is not enough to enable production ranking influence.

## 10. No-Bypass Certification

CTR.I4 cannot:

- change selected moves
- change planner ranking
- change routing
- change governance authority
- change packet authority
- change restore barrier
- mutate runtime

No-bypass flags are emitted directly in `ctr_shadow_comparison.no_bypass`.

Validation passed:

- targeted CTR/autoswitch tests: 10 OK
- full unit suite: 433 OK
- py_compile on changed runtime/admin modules
- git diff --check

Known warning:

- Existing `admin/v7-admin-api` HTML string emits a Python `DeprecationWarning` for an invalid escape sequence. This is pre-existing and did not fail validation.

## 11. Recommendation

Next safe step:

Run a real production dry-run observation window and collect CTR shadow comparison results over multiple planner cycles.

Do not enable CTR production score influence yet.

## 12. Final Verdict

FINAL_VERDICT=CTR_POSITIVE_VALUE

ctr_shadow_comparison_created=true
decision_quality_measured=true
service_aware_validation_created=true
pool_analysis_created=true
state_analysis_created=true
selected_moves_changed=false
planner_ranking_changed=false
runtime_behavior_changed=false
routing_changed=false
governance_authority_changed=false
packet_authority_changed=false
shadow_scoring_ready=true
soft_score_application_ready=false
planner_influence_ready=false
safe_next_step=CTR.I5_production_dry_run_observation_window
