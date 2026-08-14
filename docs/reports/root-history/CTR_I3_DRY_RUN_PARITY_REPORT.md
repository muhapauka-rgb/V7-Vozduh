# CTR.I3 Dry-Run Parity Report

## 1. Executive Summary

CTR.I3 is complete.

Final verdict: PASS_VALUE_DETECTED.

CTR soft adjustments are now visible as a dry-run score simulation. The simulation shows how CTR would affect candidate scores and ranking if later approved, but it does not change production score, planner ranking, selected moves, packets, restore barriers, governance authority, or runtime behavior.

No users were moved. No apply was run. No deploy was run.

## 2. Reality Audit

CTR advisory evidence already existed before this program.

Existing pieces:

- channel trust/recovery snapshot reader
- CTR lifecycle state reader
- state-based soft adjustment values
- candidate-level CTR advisory output
- operator-facing review/governance evidence from CTR.I1 and CTR.I2

Missing piece before CTR.I3:

- dry-run score simulation showing existing score, CTR adjustment, simulated score, and ranking delta.

Existing CTR values:

- TRUSTED: +20
- WATCH: 0
- NEW: -8
- RECOVERING: -12
- DEGRADED: -18
- QUARANTINED: -24

CTR was not applied to the production score path.

## 3. Duplication Audit

No duplicate planner was created.

No duplicate ranking engine was created.

No duplicate selected-move path was created.

No duplicate pool owner was created.

CTR.I3 reuses:

- planner owner: `tools/v7-users-autoswitch`
- score owner: `_score_parts`
- candidate owner: `_decision_for_user`
- selected move owner: `_select_moves`
- advisory output owner: routing brain summary

## 4. Existing Planner Ownership

Production score remains owned by `_score_parts`.

Candidate score remains:

```python
c.score = sum(c.score_parts.values())
```

Candidate sorting remains based on production score, not CTR simulation.

Selected moves remain owned by `_select_moves`.

## 5. Dry-Run Score Simulation

Added:

- `Candidate.ctr_score_simulation`
- `_ctr_simulated_score(candidate)`
- `_attach_ctr_score_simulation(candidates)`

For every candidate the simulation calculates:

- existing score
- CTR soft adjustment
- simulated score
- score delta
- old ranking position
- simulated ranking position
- ranking delta
- CTR state and reason
- service, capacity, trust, and recovery impact summaries

The simulation is output-only.

## 6. Ranking Comparison

CTR.I3 compares current production ranking with simulated CTR ranking.

The summary reports:

- simulated score candidate count
- simulated ranking change count
- whether simulated value was detected

The test fixture proved that CTR simulation can detect a ranking delta without changing selected moves.

## 7. Candidate Impact Analysis

Each candidate now exposes:

- `ctr_score_simulation.service_impact`
- `ctr_score_simulation.capacity_impact`
- `ctr_score_simulation.trust_impact`
- `ctr_score_simulation.recovery_impact`

This gives the operator a direct explanation of why the simulated score changed.

## 8. Explainability Review

The output explains:

- CTR state
- soft adjustment
- why it changed
- service impact
- capacity impact
- trust impact
- recovery impact

The existing explanation still says CTR score is not applied.

## 9. No-Bypass Certification

CTR.I3 cannot:

- change selected moves
- change production planner ranking
- change routing
- change packet generation
- change restore barrier
- change governance authority
- change runtime authority

Every simulation row explicitly marks:

- `planner_score_applied=false`
- `planner_ranking_changed=false`
- `selected_moves_changed=false`
- `runtime_behavior_changed=false`
- `simulation_authority=none`

## 10. Validation Results

Passed:

- targeted CTR/autoswitch tests: 10 OK
- full unit suite: 433 OK
- py_compile on changed runtime/admin modules
- git diff --check

Known warning:

- Existing admin HTML string emits a Python `DeprecationWarning` for an invalid escape sequence. This is not introduced by CTR.I3 and did not fail tests.

## 11. Risk Review

Risk level: LOW.

Reason:

- CTR is still not in `_score_parts`.
- CTR simulation is not used by `_beats_current`.
- CTR simulation is not used by `_projected_target_for_move`.
- CTR simulation is not used by `_select_moves`.
- No runtime action path consumes the simulated score.

## 12. Recommendation

Next safe step:

Review production dry-run output and decide whether CTR soft score should remain advisory-only or move to a separately approved shadow comparison window.

Do not apply CTR to production scoring until a later program explicitly authorizes that change with parity evidence.

## 13. Final Verdict

FINAL_VERDICT=PASS_VALUE_DETECTED

ctr_score_influence_already_existed=false
dry_run_score_simulation_created=true
ranking_comparison_created=true
candidate_impact_analysis_created=true
selected_moves_changed=false
production_score_changed=false
planner_ranking_changed=false
packet_changed=false
restore_barrier_changed=false
governance_authority_changed=false
runtime_authority_changed=false
tests_pass=true
safe_next_step=CTR.I4_shadow_comparison_window_or_operator_review_of_CTR_simulated_ranking

