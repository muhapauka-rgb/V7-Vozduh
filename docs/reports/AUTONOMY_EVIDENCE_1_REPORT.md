# AUTONOMY.EVIDENCE.1_OPERATOR_COMPARISON_AND_PREDICTION_EVIDENCE

Date: 2026-06-21T21:21:50+0700
Branch: `Updatesystem`
Commit: `51fd8c6263b1f45f4ac85b195dbd53537c19074d`
Mode: discovery and evidence-path exercise only

Final verdict: `EVIDENCE_PATHS_EXIST_COLLECTION_REQUIRED_NO_APPLY`

## 1. Scope

This phase audited whether V7 can earn missing autonomy evidence through existing mechanisms only.

No planner, governance, execution path, truth source, confidence model, trust model, prediction model, floors, thresholds, runtime apply, user movement, daemon, autoswitch enablement, or operator-free apply was changed.

## 2. Reference First

Read first:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`

Reference already answered the high-level model. This report adds the evidence collection feasibility and exact mechanics.

## 3. Evidence Paths

Saved evidence:

- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/truth_check.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/convergence_status.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/shadow_forensics.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/shadow_comparison_model_exercise.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/autonomy_dry_run_forensics.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/trust_evolution_advice.json`
- `docs/reports/AUTONOMY_EVIDENCE_1_EVIDENCE/evidence_math.json`

Commands included:

- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`
- `jq ... EVENT1_EVIDENCE/api_operator_autonomous_dry_run.json`
- `jq ... EVENT1_EVIDENCE/api_operator_decision_surface.json`
- `jq ... EVENT1_EVIDENCE/api_operator_overview.json`
- `sed -n ... admin_core/shadow_autonomy.py`
- `sed -n ... admin_core/intelligence_platform.py`
- `sed -n ... admin_core/intelligence_workers.py`
- `sed -n ... admin/v7-admin-api`
- local pure-model exercise of `admin_core.shadow_autonomy.operator_comparison_record`

## 4. Current Gate

| Gate | Current | Floor | Status |
|---|---:|---:|---|
| confidence | `45.8` | `70.0` | FAIL |
| trust | `39.584` | `70.0` | FAIL |
| prediction confidence | `39.6` | `70.0` | FAIL |
| rollback confidence | `100.0` | observed only | OK |
| comparisons total | `0` | `5+` plus quality | FAIL |
| earned confidence | `45.825` | `70.0` | FAIL |

No apply is allowed.

## 5. Shadow Comparison Findings

Owner:

- pure model: `admin_core/shadow_autonomy.py`
- GET model endpoint: `/api/operator/shadow-autonomy`
- write endpoint: `/api/actions/shadow-autonomy-compare`
- storage: `/opt/v7/egress/state/shadow-autonomy-decisions.jsonl`

Invocation flow:

1. Operator opens current shadow autonomy / operator surface.
2. Existing model exposes current `decision_id` values.
3. Authenticated admin POSTs `/api/actions/shadow-autonomy-compare` with CSRF.
4. Payload fields:
   - `decision_id`
   - `operator_decision`: `agree`, `disagree`, or `override`
   - `category`: `trust`, `service`, `capacity`, `risk`, `manual_preference`, or `other`
   - `reason`
5. API finds the current/history decision.
6. `operator_comparison_record(...)` builds a record.
7. API appends it to `SHADOW_AUTONOMY_LOG_FILE`.
8. API writes an admin audit record.
9. API refreshes the shadow autonomy model.

Exact record fields:

- `record_type=operator_comparison`
- `decision_id`
- `user`
- `recommended_action`
- `recommended_target`
- `operator_decision`
- `operator_agreed`
- `override`
- `category`
- `reason`
- `actor`
- `runtime_mutation_performed=false`
- `execution_allowed_now=false`
- `users_moved=0`
- `apply_executed=false`
- `autonomy_enabled=false`
- `comparison_id`

Important safety note:

I did not POST synthetic comparisons to production. Comparisons are evidence and must represent a real operator judgement. Fake `agree` records would increase confidence numerically while poisoning the model.

## 6. Why Comparisons Total Is 0

Current shadow state:

| Field | Value |
|---|---:|
| current decisions | `27` |
| decision history | `27` |
| comparison history | `0` |
| comparisons total | `0` |

Root cause:

- shadow decisions are created/read;
- operator comparison model exists;
- comparison POST endpoint exists;
- no existing `operator_comparison` records are present for the current decision ids.

BA execution feedback is not automatically counted as operator comparison. That is correct: execution outcomes and operator agreement are different evidence classes.

## 7. Comparison Model Exercise

A local pure-model exercise was run from EVENT1 decisions. It did not write to production.

| Scenario | comparisons_total | agreement_rate | earned_confidence | Certified |
|---|---:|---:|---:|---|
| 1 agree | 1 | 1.0 | 48.534 | false |
| 5 agree | 5 | 1.0 | 59.369 | false |
| 9 agree | 9 | 1.0 | 70.204 | true |
| 17 agree | 17 | 1.0 | 91.874 | true |
| 17 disagree | 17 | 0.0 | 6.874 | false |

Formula:

```text
earned = base_decision_confidence * (1 - evidence_weight)
       + operator_agreement_rate * 100 * evidence_weight

evidence_weight = min(1.0, comparisons_total / 20.0)
```

With current base `45.825`, theoretical minimums are:

| Agreement Rate | Comparisons Needed To Reach Earned Confidence 70 |
|---:|---:|
| 100% | 9 |
| 90% | 11 |
| 80% | 15 |
| 75% | 17 |

This only affects shadow comparison/earned confidence. It does not directly raise candidate trust or prediction confidence.

## 8. Prediction Evidence Findings

Owner:

- `admin_core/intelligence_platform.py::prediction_accuracy_model`
- `admin_core/intelligence_workers.py::build_prediction_actual_rows`
- snapshot family: `trust-evolution-summaries`

Current:

| Field | Value |
|---|---:|
| prediction actuals | `21` |
| outcome prediction confidence | `37.355` |
| candidate prediction confidence | `39.6` |
| final prediction confidence | `39.6` |
| floor | `70.0` |
| gap | `30.4` |

What constitutes a prediction actual:

- an existing service/channel actual derived from service/channel score rows;
- matched to a forecast by `id`, `channel`, `service`, `target`, or index;
- emitted by `build_prediction_actual_rows`.

Current exact rejected/unmatched counts are not exposed by the flattened admin API evidence. The model itself tracks rows as `MATCHED` or `PENDING_OUTCOME`, but EVENT1 captured only the summarized count. From summarized current evidence:

- matched/current actual count: `21`
- additional perfect prediction actuals estimated to reach floor: `23`

Basis for `23`:

```text
(37.355 * 21 + 100 * 23) / (21 + 23) = 70.101
```

Realistic path:

- run existing governed actions or observation cycles that produce accurate service/channel actuals;
- refresh intelligence snapshots through the existing snapshot owner;
- do not change prediction formula or floor.

## 9. Service Evidence Findings

Owner:

- `admin_core/intelligence_platform.py::service_intelligence_trust_model`
- `admin_core/intelligence_workers.py::build_service_actual_rows`

Current:

| Field | Value |
|---|---:|
| service actuals | `21` |
| service confidence | `39.225` |

Inputs:

- `service-scores`
- `channel-service-scores`
- service/channel actuals derived from those rows
- decision evidence confidence can raise evidence confidence, but does not create new service truth.

Service matrix history contributes indirectly through service/channel score snapshots. Telegram sentinel is an event/regression source, but it is not direct service-confidence evidence unless its output is materialized into existing service/quality evidence consumed by the snapshot worker.

Missing evidence:

- more high-quality service observations with stable confidence;
- stronger match between predicted service/channel score and observed actual score;
- fresh service matrix/quality summaries where scores are not low-confidence or contradictory.

## 10. Candidate Evidence Findings

Owner:

- `admin_core/intelligence_platform.py::suitability_trust_model`
- `admin_core/intelligence_workers.py::build_candidate_outcome_rows`
- candidate floor merge in `admin_core/operator_execution_pipeline.py`

Current:

| Field | Value |
|---|---:|
| candidate outcomes | `83` |
| suitability confidence | `29.528` |
| outcome confidence score | `39.584` |
| direct candidate confidence | `45.8` |
| final confidence | `45.8` |

Candidate outcomes already exist, but they are not strong enough to lift the outcome score above direct candidate confidence or the `70` floor.

Why confidence remains below floor:

- direct candidate score is only `45.8`;
- outcome confidence score is lower (`39.584`);
- merge rule keeps the max, so final stays `45.8`.

Existing evidence can increase confidence only if either:

- direct candidate confidence rises from the existing candidate/suitability/planner evidence; or
- trust-evolution confidence score rises above `45.8` and eventually above `70`.

## 11. Blast-Radius Findings

Owner:

- `admin_core/intelligence_platform.py::blast_radius_confidence_model`
- `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows`

Current:

| Field | Value |
|---|---:|
| blast radius confidence | `0.0` |
| inherited execution trust | `87.048` |
| governed evidence score | `100.0` |
| governed feedback evidence score | `96.97` |

Formula:

- each success/no-rollback record contributes `100`;
- each unsuccessful/rollback-required record contributes `20`;
- a recommended budget can add `100 - max(0, recommended_budget - 25)`;
- confidence is the mean of those values.

Does BA1/BA3/BA4 contribute?

Partially, but not to this field in current evidence. BA evidence contributes to governed execution trust and feedback evidence. Current `blast_radius_confidence=0.0` means the records currently consumed by the trust-evolution snapshot did not classify into explicit blast-radius evidence rows for this model.

Likely blocker:

- existing BA outcomes are visible as governed execution/feedback evidence;
- they are not currently represented in the snapshot's `blast_radius_records` as explicit success/no-rollback rows with usable movement radius.

This does not require a new model. It requires either:

- future governed operations whose records include explicit `blast_radius`, `affected_users`, `users_moved`, `selected_move_count`, or selected move lists in the consumed decision records; or
- a future audit to confirm whether historical BA evidence can be re-materialized through the existing feedback/snapshot owner without creating a new truth source.

## 12. Feasibility Matrix

| Evidence Class | Can Increase Without Code Changes? | How | Blocker |
|---|---|---|---|
| Operator comparisons | Yes | Existing `/api/actions/shadow-autonomy-compare` | Requires real operator judgement; should not be auto-generated |
| Prediction actuals | Yes | Existing service/channel actuals + snapshot refresh | Needs high-quality matched actuals; current confidence low |
| Service evidence | Yes | Existing service matrix/quality snapshot path | Needs better/stabler observations |
| Candidate evidence | Yes | Existing governed outcomes + snapshot refresh | Current outcomes do not lift suitability/confidence enough |
| Blast-radius evidence | Possibly | Existing `build_blast_radius_evidence_rows` | Current consumed records classify to `0.0`; may need new governed records or re-materialization audit |
| Confidence floor | Yes, indirectly | better direct candidate evidence or better trust-evolution confidence | current final `45.8` |
| Trust floor | Yes, indirectly | service/suitability/blast evidence | current final `39.584` |
| Prediction floor | Yes, indirectly | high-quality matched prediction actuals | current final `39.6`; about 23 perfect additional actuals estimated |

## 13. Exact Next Safe Phase

Recommended next phase: `AUTONOMY.EVIDENCE.2_OPERATOR_COMPARISON_COLLECTION_DRY_RUN`.

Scope:

1. Build an operator UI/procedure list of current decision ids.
2. Have the operator review each decision and explicitly mark `agree`, `disagree`, or `override`.
3. Submit comparisons through existing `/api/actions/shadow-autonomy-compare`.
4. Re-read `/api/operator/shadow-autonomy`.
5. Verify comparisons total, agreement rate, earned confidence, and missing targets.
6. Do not run apply.
7. Do not change thresholds.
8. Do not enable daemon/autoswitch.

Parallel safe evidence work:

- run existing service/prediction observation refreshes;
- keep all movement governed/manual;
- capture whether new prediction/service/candidate actuals change trust-evolution scores.

## 14. Final Verdict

`EVIDENCE_PATHS_EXIST_COLLECTION_REQUIRED_NO_APPLY`

V7 can realistically move toward autonomy readiness without changing autonomy logic, but only by collecting real evidence through existing paths. It cannot honestly reach readiness by synthetic comparisons, threshold changes, or timer/apply enablement.
