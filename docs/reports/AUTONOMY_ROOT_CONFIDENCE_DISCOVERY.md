# AUTONOMY.ROOT_CONFIDENCE_TRUST_DISCOVERY

Date: 2026-06-21T21:01:16+0700
Branch: `Updatesystem`
Commit: `68b4153e95712b1ac432ccfac785561025ea4aed`
Mode: discovery only

Final verdict: `ROOT_CAUSE_MAPPED_NO_RUNTIME_APPLY`

## 1. Scope

This audit maps why V7 does not yet trust itself enough for operator-free production autonomy.

No code, planner, governance, execution path, truth source, daemon, timer, threshold, runtime apply, or user movement was changed.

## 2. Reference First

Read first:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`

Reference already contained the high-level state: EVENT.1 is read-only and blocked by low confidence/trust/prediction confidence, operator comparison evidence below floor, blocked restore barrier readiness, and no certified live event consumer binding.

This audit was still required because the reference did not yet fully map the root confidence/trust model, formula owners, BA evidence consumption boundary, and missing evidence classes.

## 3. Commands Run

Discovery:

- `git status --short`
- `git branch --show-current`
- `sed -n ... docs/reference/V7_CANONICAL_REFERENCE.md`
- `sed -n ... docs/reference/SYSTEM_MAP.md`
- `sed -n ... docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `sed -n ... docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `sed -n ... docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `rg -n "confidence|trust|prediction|operator_comparison|shadow-autonomy|autonomy" ...`
- `sed -n ... admin_core/shadow_autonomy.py`
- `sed -n ... admin_core/operator_execution_pipeline.py`
- `sed -n ... admin_core/operator_decision_surface.py`
- `sed -n ... admin_core/operator_execution_feedback.py`
- `sed -n ... admin_core/intelligence_platform.py`
- `sed -n ... admin_core/intelligence_workers.py`
- `sed -n ... admin_core/intelligence_snapshots.py`
- `sed -n ... admin/v7-admin-api`
- `jq ... docs/reports/EVENT1_EVIDENCE/api_operator_autonomous_dry_run.json`
- `jq ... docs/reports/EVENT1_EVIDENCE/api_operator_overview.json`
- `rg ... BA* AUTONOMY reports`

Verification:

- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`

Saved evidence:

- `docs/reports/AUTONOMY_ROOT_EVIDENCE/truth_check.json`
- `docs/reports/AUTONOMY_ROOT_EVIDENCE/convergence_status.json`
- `docs/reports/AUTONOMY_ROOT_EVIDENCE/event1_autonomy_root_summary.json`

## 4. Current Runtime State

Fresh truth/convergence:

| Check | Result |
|---|---|
| truth-check | `PASS` |
| convergence | `PASS` / `ALIGNED` |
| local/GitHub | aligned at `68b4153e95712b1ac432ccfac785561025ea4aed` |
| runtime access | `READY` |
| runtime truth | `KNOWN` |
| state truth | `KNOWN` |
| autoswitch scheduler | inactive, approved manual mode |
| autoswitch service | inactive, explained |

Runtime still allows safe read-only discovery, but no event-driven production autonomy is active.

## 5. Current Autonomy Gate

EVENT.1 autonomous dry-run remains blocked:

| Field | Value |
|---|---:|
| candidate count | `1` |
| user | `10.7.0.5` |
| simulated from | `vless` |
| simulated to | `awg3` |
| confidence | `45.8` |
| trust | `39.584` |
| prediction confidence | `39.6` |
| rollback confidence | `100.0` |
| floor | `70.0` for confidence/trust/prediction |
| hard stop blockers | `confidence_too_low`, `trust_too_low`, `prediction_confidence_too_low` |
| apply executed | `false` |
| users moved | `0` |
| autonomy enabled | `false` |

## 6. Model Map

### Candidate Floor Model

Owner:

- `admin_core/operator_execution_pipeline.py`
- endpoint: `/api/operator/autonomous-dry-run`

Current hard floors:

- confidence floor: `70.0`
- trust floor: `70.0`
- prediction confidence floor: `70.0`
- rollback confidence is observed, not a hard floor in the current gate.

Final candidate values are produced from direct candidate evidence plus outcome-driven evidence:

```text
final_confidence = max(candidate_confidence, outcome_confidence_score)
final_trust = max(candidate_trust, outcome_trust_score)
final_prediction_confidence = max(candidate_prediction_confidence, outcome_prediction_confidence)
final_rollback_confidence = max(candidate_rollback_confidence, outcome_rollback_confidence)
```

Current outcome evidence is consumed and weighted. There is no missing wiring link in EVENT.1.

### Outcome-Driven Evidence Model

Owner:

- `admin_core/intelligence_platform.py`
- `admin_core/intelligence_workers.py`
- snapshot family: `trust-evolution-summaries`

Current components:

| Component | Current |
|---|---:|
| decision confidence | `50.0` |
| service confidence | `39.225` |
| suitability confidence | `29.528` |
| blast radius confidence | `0.0` |
| prediction confidence | `37.355` |
| rollback confidence | `100.0` |
| candidate outcomes | `83` |
| prediction actuals | `21` |
| service actuals | `21` |

Formulas:

- confidence outcome score = mean of decision, service, suitability confidence.
- trust outcome score = mean of decision, service, suitability, blast-radius confidence.
- prediction confidence = matched forecast accuracy multiplied by forecast confidence.
- rollback confidence = actual rollback success rate, or validated rollback readiness when rollback was not required.

Current result:

- outcome confidence score: `39.584`
- outcome trust score: `39.584`
- outcome prediction confidence: `37.355`
- outcome rollback confidence: `100.0`

Because direct candidate confidence is `45.8`, confidence remains `45.8`; because outcome trust is higher than direct candidate trust `3.15`, trust becomes `39.584`; because direct prediction confidence `39.6` is higher than outcome prediction `37.355`, prediction remains `39.6`.

## 7. Shadow Comparison Model

Owner:

- `admin_core/shadow_autonomy.py`
- endpoint: `/api/operator/shadow-autonomy`
- comparison endpoint: `/api/actions/shadow-autonomy-compare`
- storage: `/opt/v7/egress/state/shadow-autonomy-decisions.jsonl`

Current shadow state:

| Field | Value |
|---|---:|
| current decisions | `27` |
| decision history | `27` |
| comparisons total | `0` |
| average decision confidence | `45.825` |
| earned confidence | `45.825` |
| evidence targets met | `false` |

The earned confidence formula is:

```text
earned = base_decision_confidence * (1 - evidence_weight)
       + operator_agreement_rate * 100 * evidence_weight

evidence_weight = min(1.0, comparisons_total / 20.0)
```

With `comparisons_total=0`, evidence weight is `0`, so earned confidence stays equal to base decision confidence: `45.825`.

Shadow comparison blockers:

- `minimum_comparisons`
- `agreement_rate_floor`
- `earned_confidence_floor`

## 8. Why BA1-BA4 Evidence Does Not Close Operator-Free Autonomy

BA evidence exists and is partially consumed.

| Program | Result | Consumed By Current Model? | Boundary |
|---|---|---|---|
| BA1.FINAL | one-user execution/feedback certified | Yes, via feedback stores and trust-evolution summaries | Outcome classifier was conservative for BA1 feedback |
| BA2 | two-user attempt blocked before apply | Safety evidence, but no successful outcome lift | Atomic/source drift blocked apply |
| BA3.RETRY | five users moved, verified, feedback materialized | Yes | Governed execution evidence only |
| BA4 | ten users moved, verified, feedback materialized | Yes | Governed execution evidence only |

EVENT.1 proves this consumption path is active:

- `evidence_produced=true`
- `evidence_stored=true`
- `evidence_visible=true`
- `evidence_consumed=true`
- `evidence_weighted=true`
- missing links: `[]`

However BA evidence raises governed execution trust, not autonomous operator-free trust.

The governed-to-autonomy bridge currently reports:

| Field | Value |
|---|---:|
| governed execution evidence score | `100.0` |
| governed feedback evidence score | `96.97` |
| inherited execution trust | `87.048` |
| autonomy specific trust | `0.0` |
| autonomy specific gap | `100.0` |
| corrected autonomy trust | `52.229` |
| boundary cap | `OPERATOR_APPROVAL_READY` |
| bounded autonomy ready | `false` |
| production autonomy ready | `false` |

Meaning: V7 has strong evidence that the governed path can execute approved batches, but it does not yet have evidence that it may decide, trigger, compare, apply, and recover without an operator.

## 9. Root Cause Matrix

| Blocker | Root Cause | Evidence Owner | Missing Evidence |
|---|---|---|---|
| `confidence_too_low` | Direct candidate confidence is `45.8`; outcome confidence is only `39.584` | `operator_execution_pipeline.py`, `trust-evolution-summaries` | Higher quality matched candidate/service/suitability outcomes, or a direct candidate score above floor |
| `trust_too_low` | Direct trust is `3.15`; outcome trust raises it only to `39.584`; blast-radius confidence is `0.0` | `intelligence_platform.py`, `intelligence_workers.py` | Better service/suitability evidence and explicit blast-radius evidence |
| `prediction_confidence_too_low` | Prediction final is `39.6`; matched actuals exist but quality/confidence do not reach floor | `prediction_accuracy_model` | More high-quality matched prediction actuals; current model estimates 23 perfect additional prediction actuals would be needed |
| `operator_comparison_evidence_below_floor` | `comparisons_total=0` for current shadow decisions | `shadow_autonomy.py` | At least 5 current operator comparisons plus agreement/override quality |
| `operator_free_apply_not_certified` | Current program deliberately forbids operator-free apply | ADR-EVENT-DRIVEN-AUTONOMY, EVENT.1 | Future explicit canary program after floors pass |
| restore barrier blocked | Dry-run preview does not create a live approved plan lock or restore barrier | `operator_execution.py`, packet tool | Fresh approved packet/restore barrier only in a future governed apply phase |
| live event consumer missing | `v7-telegram-sentinel` runs as `--no-autoswitch`; autoswitch service/timer inactive | systemd/runtime truth | Read-only event consumer binding certification before any apply authority |

## 10. Prediction Confidence

Prediction confidence is not low because the endpoint is unwired. It is low because matched forecast evidence is not yet strong enough.

Current prediction trace:

- candidate prediction confidence: `39.6`
- outcome prediction confidence: `37.355`
- final prediction confidence: `39.6`
- floor: `70.0`
- gap: `30.4`
- prediction actuals count: `21`
- additional perfect prediction actuals estimated by current trace: `23`

Counts alone are insufficient. Evidence must be matched to the forecast/candidate keys and high quality.

## 11. What Is Proven

- Existing planner remains the owner.
- Existing packet/restore barrier/apply/rollback/feedback owners remain the owners.
- BA3/BA4 certified governed movement at 5 and 10 users.
- Feedback and learning stores are visible and consumed by `trust-evolution-summaries`.
- EVENT.1 read-only trigger path reuses the existing owners and correctly stops before apply.
- The current low confidence/trust/prediction block is evidence-based, not a missing UI label.
- The confidence engine, prediction engine, and rollback engine report healthy.
- The current floors are not marked unrealistically strict by the model.

## 12. What Is Not Proven

- Operator-free autonomous apply is not certified.
- Operator-free trigger from regression event to live apply is not certified.
- Autonomous rollback decision authority is not certified.
- Current shadow operator comparison evidence is not present.
- Blast-radius confidence is not present in the current trust floor formula.
- Production daemon/timer apply mode is not active.

## 13. Safe Next Phase

Next phase should be discovery/collection, not apply:

1. Keep production movement manual/governed.
2. Certify a read-only event consumer binding that converts regression evidence into planner preview only.
3. Add an operator comparison collection pass using the existing `/api/actions/shadow-autonomy-compare` endpoint; do not create a new comparison system.
4. Collect high-quality matched prediction/service/candidate actuals through existing feedback and snapshot refresh owners.
5. Add explicit blast-radius evidence through existing governed execution records; do not lower floors.
6. Re-run EVENT.1 style dry-run only after evidence improves.
7. Only consider a one-user operator-approved canary apply when confidence, trust, prediction, comparison, restore barrier, rollback, feedback, truth, and convergence gates pass together.

## 14. Documentation Updates

Updated:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

ADR creation:

- No new ADR was created. The stable architectural decision remains ADR-EVENT-DRIVEN-AUTONOMY. This audit clarifies model ownership and evidence boundaries without changing the decision.

## 15. Final Summary

V7 is working as designed for safety. The system has a certified governed execution path and consumes BA evidence, but production autonomy is intentionally blocked because the current model does not yet have enough operator-free evidence.

Root cause:

```text
governed execution trust is strong
but autonomous trigger/apply trust is not earned yet
```

Final verdict: `ROOT_CAUSE_MAPPED_NO_RUNTIME_APPLY`
