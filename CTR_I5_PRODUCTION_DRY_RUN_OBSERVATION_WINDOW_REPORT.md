# CTR.I5 Production Dry-Run Observation Window Report

## 1. Executive Summary

CTR.I5 is implemented, but production value certification is not yet complete.

Final verdict: INSUFFICIENT_DATA.

Reason:

The passive observation-window collector is now available, but the existing production dry-run evidence was generated before CTR.I4 added `ctr_shadow_comparison` to planner output. Therefore the historical production JSON plans cannot prove whether CTR consistently improves decisions.

No users were moved. No apply was run. No deploy was run. No runtime behavior was changed.

## 2. Reality Audit

Existing before CTR.I5:

- CTR advisory evidence
- CTR review semantics
- CTR governance evidence
- CTR.I3 dry-run score simulation
- CTR.I4 single-plan shadow comparison

Missing before CTR.I5:

- multi-cycle observation window aggregator
- statistical CTR value certification
- usefulness/confidence scores across real dry-run cycles

Implemented:

- `tools/v7-ctr-observation-window`

## 3. Observation Window Results

Existing production dry-run evidence was aggregated from:

- `canary_expansion_small_batch_evidence/`
- `medium_batch_readiness_evidence/`
- `large_batch_stability_pool_readiness_evidence/`
- `pool_stability_post_pool_evidence/`

Result:

- total_cycles=0
- ranking_changes=0
- winner_changes=0
- top3_changes=0
- pool_changes=0
- positive_changes=0
- negative_changes=0
- neutral_changes=0
- CTR usefulness score=50.0
- CTR confidence score=0.0

Interpretation:

The tool worked, but the historical files do not contain CTR shadow comparison cycles.

## 4. CTR State Analysis

No state-level production observation could be certified yet.

All states currently have zero observed CTR.I4 cycles:

- TRUSTED
- WATCH
- NEW
- RECOVERING
- DEGRADED
- QUARANTINED

## 5. Ranking Analysis

No production ranking-change statistics are available yet because historical plans lack `ctr_shadow_comparison`.

## 6. Service-Aware Analysis

No production service-aware CTR impact is available yet for:

- Telegram
- YouTube
- Instagram
- ChatGPT
- Google

## 7. Pool Analysis

No production pool ordering or pool membership impact can be certified yet.

Reason:

The older dry-run outputs do not contain CTR.I4 pool comparison payloads.

## 8. Statistical Certification

Current statistical result:

- minimum required cycles: 10
- observed CTR.I4 cycles: 0
- confidence score: 0.0
- final verdict: INSUFFICIENT_DATA

CTR value is not rejected.

CTR value is not certified.

The correct state is: observation mechanism ready, production evidence missing.

## 9. Readiness Review

Current readiness:

- soft score influence: NEEDS_MORE_DATA
- planner influence: NOT_READY
- pool influence: NOT_READY
- more observation required: true

CTR must not be enabled for score/ranking influence yet.

## 10. No-BYPASS Certification

CTR.I5 cannot:

- change selected moves
- change planner ranking
- change routing
- change runtime
- change governance authority
- change packet authority

The collector only reads JSON dry-run plans and writes an analysis report.

Validation passed:

- targeted CTR.I5 tests: 3 OK
- full unit suite: 435 OK
- py_compile on changed runtime/admin modules
- git diff --check

Known warning:

- Existing `admin/v7-admin-api` HTML string emits a Python `DeprecationWarning` for an invalid escape sequence. This is pre-existing and did not fail validation.

## 11. Recommendation

Next safe step:

Run a production dry-run observation window after CTR.I4/I5 code is deployed through the approved safe deployment process.

Required command shape after deployment:

```bash
tools/v7-users-autoswitch --pretty
```

Capture at least 10 dry-run JSON outputs, then aggregate:

```bash
tools/v7-ctr-observation-window --input-dir <dry-run-json-folder> --min-cycles 10 --pretty
```

Do not run `--apply`.

Do not move users.

## 12. Final Verdict

FINAL_VERDICT=INSUFFICIENT_DATA

observation_window_collector_created=true
real_production_dry_run_files_found=true
real_ctr_shadow_cycles_found=false
total_cycles=0
ranking_changes=0
winner_changes=0
top3_changes=0
pool_changes=0
positive_changes=0
negative_changes=0
neutral_changes=0
ctr_usefulness_score=50.0
ctr_confidence_score=0.0
soft_score_influence_ready=false
planner_influence_ready=false
pool_influence_ready=false
selected_moves_changed=false
planner_ranking_changed=false
routing_changed=false
runtime_changed=false
governance_authority_changed=false
packet_authority_changed=false
safe_next_step=deploy_CTR_shadow_output_then_collect_10_production_dry_run_cycles
