# AUTONOMY.SUITABILITY.KNOWLEDGE_AND_CONFIDENCE.FORENSICS REPORT

Timestamp: `2026-06-23T16:35:27Z`
Branch: `Updatesystem`
Local commit at start: `cfa06d1ec18f74c9bb2d203bf8a312fbe37c25e9`
Mission type: deep systems forensics plus existing-owner visibility fix.

## 1. Knowledge Flow Map

V7 experience is not a single score. It is a chain:

```text
Reality
  -> Observation
  -> Evidence
  -> Outcome
  -> Suitability
  -> Confidence
  -> Trust
  -> Planner
  -> Action
```

| Stage | Owner | Store / Snapshot | Consumer |
| --- | --- | --- | --- |
| Reality | Runtime channels, users, services | `/opt/v7/egress/state`, registries, service matrix outputs | probe and planner owners |
| Observation | Existing probes and read models | service/channel score snapshots, quality compact outputs | intelligence workers |
| Evidence | Intelligence and feedback owners | `trust-evolution-summaries`, service/channel rows, execution/feedback JSONL | trust acceleration inventory |
| Outcome | Existing outcome mappers | prediction actuals, service actuals, candidate outcomes, blast/rollback rows | `trust_evolution_summary` |
| Suitability | Candidate suitability + outcome mapper | `candidate-suitability-summary`, candidate outcome rows | suitability trust model |
| Confidence | Trust platform models | confidence summary, floor forensics, source confidence inventory | canary proximity |
| Trust | Trust evolution | confidence/trust floor values | autonomy gate |
| Planner | Existing autoswitch planner | dry-run/preview candidates | execution packet / operator |
| Action | Existing governed execution | restore barrier, bounded apply, feedback, rollback | future event-driven autonomy |

No new planner, governance, execution path, truth source, storage, or synthetic evidence was created.

## 2. Experience Inventory

Production evidence captured in:

`docs/reports/AUTONOMY_SUITABILITY_KNOWLEDGE_AND_CONFIDENCE_FORENSICS_EVIDENCE/production_trust_inventory.json`

Post-deploy production verification captured in:

`docs/reports/AUTONOMY_SUITABILITY_KNOWLEDGE_AND_CONFIDENCE_FORENSICS_EVIDENCE/production_trust_inventory_after_deploy.json`

| Source | Count | Freshness | Confidence impact | Trust impact | Classification |
| --- | ---: | --- | ---: | --- | --- |
| Prediction matches | `21/21` | FRESH | `35.346` | limited by low forecast source confidence | sufficient evidence, low attribution |
| Service outcomes | `21` | FRESH | `39.046` | contributes but remains low-confidence | insufficient high-confidence evidence |
| Candidate outcomes | `83/156` | FRESH | `27.715` | main confidence/trust blocker | incomplete and low-confidence |
| Blast evidence | `11` | FRESH | `100.0` | not blocker | sufficient |
| Rollback evidence | `20` | FRESH | `100.0` | not blocker | sufficient |
| Operator comparisons | `0` | event-log dependent | `45.817` secondary | cannot replace observed outcomes | underfed secondary path |

Current floors:

| Floor | Current | Target | Pass |
| --- | ---: | ---: | --- |
| Confidence | `38.920` | `70.000` | false |
| Trust | `54.190` | `70.000` | false |
| Prediction confidence | `35.346` | `70.000` | false |
| Operator earned confidence | `45.817` | `70.000` | false |

## 3. Aggregation Analysis

`83/156` does not mean 83 unique high-diversity real-world situations. It means 83 candidate outcomes matched against 156 current candidate keys in the suitability model.

The exposed raw suitability rows are bounded to 50 rows in `suitability_trust_model` for report size. In the captured production inventory those 50 rows contain:

| Dimension | Count |
| --- | ---: |
| Exposed rows | `50` |
| Exposed rows with outcomes | `42` |
| Exposed rows without outcomes | `8` |
| Unique exposed keys | `50` |
| Unique exposed users | `9` |
| Unique exposed channels | `6` |

The full counter remains `156` candidates, `83` outcomes, and `73` missing outcomes. Therefore diversity exists, but it is not yet strong enough for canary autonomy because the model lacks complete and high-confidence outcomes across the candidate space.

## 4. Experience Loss Analysis

| Loss point | Intentional? | Finding |
| --- | --- | --- |
| Bounded decision history | Yes | Protects stale/unbounded history from dominating current trust. |
| `suitability_trust_model` raw rows capped to 50 | Yes for payload size, but created visibility loss | Counters knew `156/83/73`, but projection displayed only the bounded exposed rows. |
| Candidate outcome matching by `user:channel` | Yes | Prevents unrelated outcomes from validating current candidates. |
| Missing outcomes treated as uncertain observed quality | Yes | Avoids pretending missing evidence is success. |
| Low source confidence weighting | Yes | Prevents high score from becoming autonomy confidence without strong source confidence. |
| Projection missing counter showed `0` after 8 visible missing rows | Accidental visibility loss | Fixed in this phase by adding full coverage counters to read-only projection output. |

## 5. Suitability Forensics

Suitability is truly low in the current model.

Evidence:

- `current_candidates = 156`
- `current_outcomes = 83`
- `missing_outcomes_to_full_coverage = 73`
- `mean_candidate_confidence = 0.407`
- `mean_correctness = 63.217`
- `suitability_confidence = 27.715`
- `current_correctness_can_reach_70_even_with_perfect_confidence = false`

Conclusion:

Suitability is not merely undervalued. It is incomplete and weakly validated. There was one visibility bug in the growth projection, but fixing that visibility does not make the suitability floor pass.

## 6. Industry Comparison

| System | Mature pattern | V7 status |
| --- | --- | --- |
| Google SRE | Error-budget style real outcome gates, freshness windows, bounded history | PARTIAL |
| Netflix | Real production canary evidence before automation expansion | PARTIAL |
| Kayenta | Canary analysis from measured baseline/canary outcomes | PARTIAL |
| Kubernetes Controllers | Event-driven reconcile loops with observed state and idempotent actions | PARTIAL |
| Argo Rollouts | Progressive delivery, analysis, abort/rollback gates | PARTIAL |
| Recommendation systems | Diversity-aware feedback, delayed attribution, stale-evidence handling | MISSING for long-term evidence index; PARTIAL for current bounded outcomes |

V7 has the right shape: observed outcome primary, bounded history, restore barrier, rollback, prediction, feedback, and trust owners. It still lacks enough real candidate/suitability outcomes and future-scale evidence indexing.

## 7. Undervaluation Analysis

| Area | Would an experienced engineer assign higher confidence? | Reason |
| --- | --- | --- |
| Prediction | Yes, as raw accuracy evidence | `21/21` matches and high accuracy are strong, but V7 intentionally limits autonomy confidence because source confidence is low. |
| Service | No | Correctness is high but row confidence is around `0.39`; V7 is appropriately cautious. |
| Suitability | No | Coverage and correctness are both insufficient for autonomy. |
| Trust | No | Blast and rollback are strong, but confidence/trust are constrained by service and suitability. |

## 8. Implementation

Implemented one existing-owner visibility fix in `admin_core/autonomy_trust_acceleration.py`.

Problem:

`real_outcome_growth_projection` used bounded raw suitability rows for missing-candidate projection. Production had full counters `156 candidates`, `83 outcomes`, `73 missing`, but projection rows showed only `8` visible missing rows and then `0` remaining. That was misleading.

Fix:

- Keep current formulas and floors unchanged.
- Keep projected suitability confidence unchanged.
- Add full candidate coverage counters to projection rows.
- Make `converted_missing_candidate_outcomes` and `missing_candidate_outcomes_remaining` use the known full coverage counter from `confidence_reality_audit`.
- Preserve visible-row counters separately:
  - `visible_suitability_rows`
  - `visible_converted_missing_candidate_outcomes`
  - `visible_missing_candidate_outcomes_remaining`
  - `projected_suitability_scope`

This is visibility/attribution only. It does not create evidence and does not change runtime behavior.

## 9. Tests

| Check | Result |
| --- | --- |
| `python3 -m unittest tests.unit.test_autonomy_trust_acceleration -v` | PASS, 6 tests |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin_core/autonomy_trust_acceleration.py tests/unit/test_autonomy_trust_acceleration.py` | PASS |
| Production inventory capture | PASS, read-only |
| `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json` | PASS, runtime commit `5cfe26d9808cdfe5f0ab18f6cdea2cb5ed981e89`, no apply/user movement |
| Production inventory after deploy | PASS: projection row now reports `known_missing_candidate_outcomes=73`, `converted_missing_candidate_outcomes=10`, `missing_candidate_outcomes_remaining=63`, and `visible_missing_candidate_outcomes_remaining=0` separately |
| `tools/v7-truth-check --all --json` | PASS, `FULLY_ALIGNED` |
| `tools/v7-convergence-status --json` | PASS, `ALIGNED` |

Initial `python3 -m pytest ...` did not run because the system Python has no `pytest`; the suite is unittest-compatible and passed through `unittest`.

## 10. Canary Impact

Current exact canary blockers:

| Blocker | Current gap |
| --- | --- |
| Confidence | `31.080` below floor |
| Trust | `15.810` below floor |
| Prediction confidence | `34.654` below floor |
| Suitability confidence | `27.715`, with `73` known missing candidate outcomes |
| Operator comparison | `0` comparisons; secondary path only |

Real vs aggregation vs confidence:

| Type | Impact |
| --- | --- |
| Real evidence gap | Candidate/suitability outcomes are incomplete; service rows need higher-confidence probe cycles. |
| Aggregation/visibility gap | Projection visibility previously hid the full missing-candidate counter after bounded rows; fixed. |
| Confidence gap | Prediction and service are consumed but under-confident; suitability is low due coverage and correctness. |

Canary remains blocked. This phase did not authorize apply or user movement.

## 11. Future Scale Review

For 100 channels, 1000 users, and years of evidence, current bounded snapshots will not be enough by themselves. V7 will need the already documented post-production evidence index and freshness model:

- typed evidence classes;
- per-source freshness windows;
- diversity-aware outcome summaries;
- deduplication by user/channel/action/context;
- bounded current read models plus long-term evidence catalog;
- shadow validation before any planner/trust impact.

This remains deferred until Production Autonomy is certified.

## 12. Final Verdict

`EXPERIENCE_MIXED`

V7 is not missing the whole experience pipeline. The pipeline exists and consumes real evidence. The current blocker is mixed:

- prediction is undervalued as accuracy evidence;
- suitability is genuinely incomplete and low;
- service evidence exists but is low-confidence;
- blast and rollback are strong;
- projection had a visibility/attribution bug, now fixed.
