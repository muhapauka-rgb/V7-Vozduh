# AUTONOMY.PREDICTION.EVIDENCE.1 Report

Status: discover-only prediction evidence forensics  
Timestamp: 2026-06-22T10:27:13Z  
Commit: `7695fc38e1dfd7fc577671bd8a27b16b06cf4321`  
Runtime apply: `false`  
Users moved: `0`  
Snapshot written: `false`

## 1. Evidence Paths

| Evidence | Path |
| --- | --- |
| Production prediction forensics | `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_1_EVIDENCE/production_prediction_forensics.json` |
| Analysis summary | `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_1_EVIDENCE/analysis_summary.json` |
| Final truth check | `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_1_EVIDENCE/final_truth_check.json` |
| Final convergence status | `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_1_EVIDENCE/final_convergence_status.json` |

The production probe was read-only. It imported existing production owners, rebuilt in-memory prediction rows, compared forecasts to existing actual rows, and did not write snapshots or move users.

Commands run:

```text
tools/v7-truth-check --all --json
tools/v7-convergence-status --json
production read-only prediction evidence probe
rg/sed/jq for local source and evidence inspection
```

## 2. Prediction Model Map

| Step | Owner | Existing source |
| --- | --- | --- |
| Prediction forecast generation | `admin_core/intelligence_workers.py::build_prediction_snapshot` | Service matrix, quality summary, risk summary, trust summary, blast-radius summary |
| Forecast row extraction | `admin_core/intelligence_workers.py::_prediction_forecast_rows` | `channel_forecasts` + `service_forecasts` |
| Actual row construction | `admin_core/intelligence_workers.py::build_prediction_actual_rows` | Existing service/channel score rows and bounded decision records |
| Accuracy/confidence calculation | `admin_core/intelligence_platform.py::prediction_accuracy_model` | Forecast rows matched to actual rows by `id/channel/service/target/user/index` |
| Autonomy gate consumption | `admin_core/operator_execution_pipeline.py::autonomy_engine_trace_model` and `autonomous_safety_gates` | Candidate prediction confidence merged with outcome prediction confidence |

Formula currently used by the existing model:

```text
prediction_confidence = mean(matched_forecast_accuracy) * mean(forecast_confidence)
matched_forecast_accuracy = 100 - abs(predicted_quality - observed_quality)
final_autonomy_prediction_confidence = max(candidate_prediction_confidence, outcome_prediction_confidence)
floor = 70.0
```

## 3. Production Findings

| Metric | Value |
| --- | ---: |
| Forecasts seen | 21 |
| Prediction actuals built | 21 |
| Service actuals built | 21 |
| Matched forecasts | 21 |
| Pending forecasts | 0 |
| Unmatched forecasts | 0 |
| Ignored service actuals | 0 |
| Mean forecast accuracy | 98.488 |
| Mean forecast confidence | 0.3792 |
| Outcome prediction confidence | 37.351 |
| Candidate prediction confidence currently gating autonomy | 39.6 |
| Floor | 70.0 |
| Estimated perfect additional actuals needed for floor | 23 |

The blocker is not row matching. All 21 forecasts matched actual rows, and no service actuals were ignored by this probe.

The blocker is low forecast/source confidence. Accuracy is high, but the model multiplies it by mean forecast confidence around `0.3792`, so the confidence result remains around `37.351`.

## 4. Missing Evidence Map

| Evidence type | Exists now | Gap |
| --- | --- | --- |
| Matched prediction actuals | Yes: 21/21 matched | Count is too small to overcome low source confidence |
| Forecast accuracy | Yes: 98.488 mean | Accuracy is not the limiting factor |
| Forecast confidence | Yes: 0.3792 mean | Main limiting factor |
| Time-separated outcome loop | Partial | Current actuals come from existing service/channel evidence; stronger proof needs repeated forecast -> later outcome comparisons |
| Operator comparison evidence | Missing for current decisions | Current comparison count remains too low for autonomy trust |
| Blast-radius visible evidence | Partial | REMATERIALIZATION.4 proved impact if visible, but recovery not executed |
| Candidate outcome quality | Partial | Existing candidate outcomes are consumed but suitability confidence remains low |

## 5. Industry Comparison

| System pattern | Evidence / trust concept | V7 status |
| --- | --- | --- |
| Google SRE automation | Automate after reliable signals, keep humans in the loop when confidence or blast risk is unclear, and use error-budget style gates for production risk | `PARTIALLY_EXISTS_IN_V7` |
| Kubernetes controllers | Continuous reconciliation compares desired state with observed state before acting | `PARTIALLY_EXISTS_IN_V7` |
| Automated canary analysis / Kayenta-style rollout | Compare candidate behavior against baseline metrics before promoting | `PARTIALLY_EXISTS_IN_V7` |
| LinkedIn-style recommendation systems | Offline/online outcome comparison, experimentation, and feedback loops build confidence before ranking/action changes | `PARTIALLY_EXISTS_IN_V7` |
| OpenAI eval loops | Keep explicit eval datasets/runs and compare outputs to expected behavior before deployment | `PARTIALLY_EXISTS_IN_V7` |
| Open-source progressive delivery | Use analysis templates/metrics to gate incremental rollout | `MISSING_IN_V7` for production autonomy; `PARTIALLY_EXISTS_IN_V7` for bounded BA/manual runs |

Sources used for philosophy only:

- Google SRE automation: `https://sre.google/sre-book/automation-at-google/`
- Kubernetes controller pattern: `https://kubernetes.io/docs/concepts/architecture/controller/`
- Kubernetes desired state/object model: `https://kubernetes.io/docs/concepts/overview/working-with-objects/`
- Spinnaker canary guide: `https://spinnaker.io/docs/guides/user/canary/`
- OpenAI evals: `https://platform.openai.com/docs/guides/evals`
- LinkedIn recommender evidence literature: `https://arxiv.org/abs/1809.06473`

## 6. V7 Comparison Matrix

| Evidence concept | V7 current state | Classification |
| --- | --- | --- |
| Existing planner before action | `tools/v7-users-autoswitch` exists and is reused | `ALREADY_EXISTS_IN_V7` |
| Restore barrier before apply | Existing restore settle gate and packet validation | `ALREADY_EXISTS_IN_V7` |
| Forecast -> actual comparison | `prediction_accuracy_model` validates matched actuals | `ALREADY_EXISTS_IN_V7` |
| Repeated future outcome evidence | No certified production loop for accumulating later actuals from forecasts | `PARTIALLY_EXISTS_IN_V7` |
| Operator shadow comparison | Existing endpoint/store exists, but current comparison evidence remains insufficient | `PARTIALLY_EXISTS_IN_V7` |
| Blast-radius visibility | Builder can classify evidence; final visible decision set still blocks recovery | `PARTIALLY_EXISTS_IN_V7` |
| Event-driven production daemon | Desired model documented; not enabled | `MISSING_IN_V7` |
| Progressive autonomous rollout gates | BA certifications exist up to 10 users, but production daemon gates still fail | `PARTIALLY_EXISTS_IN_V7` |

## 7. Readiness Recalculation

| Subsystem | Readiness | Blocker |
| --- | ---: | --- |
| Prediction model understanding | 90% | Model path and formula are now mapped |
| Prediction evidence quality | 45% | Actuals match, but forecast confidence is too low |
| Operator comparison | 20% | Existing comparison path has insufficient current records |
| Blast-radius recovery | 80% | Existing rows can help, but not yet visible in final consumed set |
| Autonomous trust | 55% | REMATERIALIZATION.4 visible-row preview reaches 54.684, still below floor |
| Production autonomy | 40% | Confidence, trust, and prediction floors still fail |

## 8. What Would Raise Prediction Confidence

Only existing systems may be used.

| Required evidence | Existing owner |
| --- | --- |
| More matched forecast -> later actual comparisons from real service/channel outcomes | `admin_core/intelligence_workers.py`, `tools/v7-intelligence-snapshot-refresh` |
| Higher source confidence for forecasts through fresher service, quality, trust, and blast inputs | Existing service matrix, quality compact, trust evolution refresh |
| Operator comparison records for current shadow decisions | `/api/actions/shadow-autonomy-compare`, `admin_core/shadow_autonomy.py` |
| Visible blast-radius evidence in final trust-evolution decision set | Existing blast builder + trust evolution snapshot refresh/materialization path |

Do not raise the number by changing floors, changing the formula, creating synthetic actuals, or adding a new prediction owner.

## 9. Next Phase

`AUTONOMY.PREDICTION.EVIDENCE.2_REAL_OUTCOME_CONFIDENCE_COLLECTION`

Purpose:

1. Reuse existing snapshot refresh and outcome stores.
2. Collect time-separated forecast -> later actual evidence.
3. Keep it read-only or evidence-write-only.
4. Recalculate prediction confidence without changing thresholds, formulas, planner, governance, execution, or truth source.

## 10. Verdict

`PREDICTION_EVIDENCE_GAP_MAPPED`

Prediction confidence remains low because forecasts are accurate but low-confidence. V7 has a real prediction comparison model; it does not yet have enough high-confidence production outcome evidence to certify operator-free autonomy.

Final alignment:

| Check | Status |
| --- | --- |
| Truth | `PASS` |
| Convergence | `ALIGNED` |
| Runtime | `RUNTIME_ALIGNED`; docs-only mismatch ignored; blocking `false` |
| Apply | `not executed` |
| Users moved | `0` |
