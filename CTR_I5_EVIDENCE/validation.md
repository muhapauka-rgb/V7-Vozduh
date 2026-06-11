# CTR.I5 Validation Evidence

## Targeted tests

Passed:

- `tests.unit.test_ctr_i5_observation_window`
- `tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_ctr_soft_score_simulation_can_detect_ranking_delta_without_runtime_change`

Result:

- 3 tests OK

## Static validation

Passed:

- `py_compile tools/v7-ctr-observation-window`
- `py_compile tools/v7-users-autoswitch`
- `py_compile admin_core/operator_decision_surface.py`
- `py_compile admin_core/operator_execution_feedback.py`
- `py_compile admin_core/operator_execution_pipeline.py`

## Full regression

Passed:

- `python3 -m unittest discover tests`
- 435 tests OK

## Diff validation

Passed:

- `git diff --check`

## Existing production dry-run aggregation

Command:

```bash
tools/v7-ctr-observation-window \
  --input-dir canary_expansion_small_batch_evidence \
  --input-dir medium_batch_readiness_evidence \
  --input-dir large_batch_stability_pool_readiness_evidence \
  --input-dir pool_stability_post_pool_evidence \
  --min-cycles 10 \
  --out CTR_I5_EVIDENCE/existing_production_dry_run_observation_window.json \
  --pretty
```

Result:

- total_cycles=0
- ctr_confidence_score=0.0
- final_verdict=INSUFFICIENT_DATA

Reason:

- existing production dry-run files do not contain CTR.I4 `ctr_shadow_comparison` payloads.
