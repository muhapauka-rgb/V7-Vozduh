# OPERATOR.COMPARISON.COLLECTION.1 Report

Date: 2026-06-23
Branch: `Updatesystem`
Mode: implementation, test, verify, document
Implementation commit: `f86148dc70a3a4d039dc41b555060ae0d2d4f13e`
Deploy id: `deploy-z8-14-Updatesystem-f86148d-20260623T094821`

## 1. Lifecycle Trace

The existing operator comparison path is now explicit and durable:

```text
Decision
  -> Operator Review Packet
  -> /api/actions/shadow-autonomy-compare
  -> operator_comparison JSONL record
  -> agreement rate
  -> earned confidence
  -> autonomous trust evidence
  -> canary readiness gates
```

This remains review-only. No runtime apply, user movement, daemon enablement, planner change, governance change, execution change, threshold change, formula change, synthetic comparison, or new truth source occurred.

## 2. Owners Reused

| Owner | Reused | Change |
| --- | --- | --- |
| `admin_core/shadow_autonomy.py` | yes | Added explicit review packet, comparison eligibility, and growth projection using existing formulas. |
| `/api/actions/shadow-autonomy-compare` | yes | Existing endpoint remains the only valid writer for real operator comparisons. |
| `shadow-autonomy-decisions.jsonl` | yes | Existing JSONL family remains the evidence store. |
| `admin/v7-admin-api` | yes | Reads active and rotated shadow JSONL records so comparisons are not lost behind newer decision rows. |
| Operator UI | yes | Existing Shadow observation block now shows review packet and nearest confidence target. |

## 3. Durability Analysis

Before this phase, shadow history was read from a bounded active file tail. That made old comparison records vulnerable to practical disappearance when newer decision records filled the tail or when production logs rotated.

The fix keeps the same store but changes the read path:

- Read active `shadow-autonomy-decisions.jsonl`.
- Read rotated JSONL family records.
- Preserve decision and comparison tails separately.
- Rebuild the model from reread evidence.

No new storage was created.

## 4. Production Review Inventory

Evidence file:

- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_EVIDENCE/production_review_inventory_before.json`
- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_EVIDENCE/production_review_inventory_after_deploy.json`
- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_EVIDENCE/production_review_inventory_after_refresh.json`

Captured read-only by SSH from registry/state/snapshots/shadow JSONL, without calling `/api/operator/shadow-autonomy`.

| Metric | Value |
| --- | ---: |
| Users | 27 |
| `awg3` users | 8 |
| `wireguard-1779454504-c43409` users | 8 |
| `vless` users | 11 |
| Current decisions | 27 |
| Reviewable decisions | 27 |
| Move recommendations | 10 |
| Existing comparison records read | 0 |
| Agreement rate | 0.0 |
| Earned confidence | 45.802 |

Full per-decision fields in the evidence include `decision_id`, user, source channel, target, recommendation, confidence, trust, blockers, age, and eligibility.

After deploy, runtime exposes `operator_review_packet` with 27 reviewable decisions, 0 reviewed decisions, `synthetic_agreement_allowed=false`, `runtime_mutation_performed=false`, `apply_executed=false`, and `users_moved=0`.

## 5. Growth Model

The projection uses the existing formula only:

```text
earned = base_decision_confidence * (1 - min(comparisons/20, 1))
       + agreement_percent * min(comparisons/20, 1)
```

Production base decision confidence: `45.802`.

| Comparisons | 100% agreement | 90% agreement | 80% agreement | 75% agreement |
| ---: | ---: | ---: | ---: | ---: |
| 5 | 59.352 | 56.852 | 54.352 | 53.102 |
| 10 | 72.901 | 67.901 | 62.901 | 60.401 |
| 15 | 86.451 | 78.951 | 71.451 | 67.701 |
| 20 | 100.000 | 90.000 | 80.000 | 75.000 |

Practical floor estimate: at least 5 comparisons are required structurally, but `70` earned confidence requires about 10 comparisons at 100%, 11 at 90%, 15 at 80%, or 17 at 75%.

## 6. Lifecycle Verification

Evidence file:

- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_EVIDENCE/local_comparison_lifecycle.json`

| Check | Result |
| --- | --- |
| Comparison survives reread | PASS |
| Agreement rate survives reread | PASS |
| Earned confidence survives rebuild | PASS |
| Review packet survives rebuild | PASS |
| Synthetic agreement created | NO |
| Runtime apply executed | NO |
| Users moved | 0 |

Production before/after/after-refresh lifecycle:

| Stage | Decisions | Comparisons | Agreement | Earned Confidence | Reviewable | Reviewed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Before deploy | 27 | 0 | 0.0 | 45.802 | n/a | n/a |
| After deploy | 27 | 0 | 0.0 | 45.801 | 27 | 0 |
| After snapshot refresh | 27 | 0 | 0.0 | 45.801 | 27 | 0 |

Snapshot refresh evidence:

- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_EVIDENCE/production_snapshot_refresh_after_deploy.json`
- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`
- `users_moved=false`
- `source_stable=true`

## 7. Tests

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.unit.test_shadow_autonomy tests.unit.test_operator_execution_pipeline tests.unit.test_intelligence_platform` | PASS, 57 tests |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin_core/shadow_autonomy.py admin/v7-admin-api` | PASS |
| `tools/v7-truth-check --all --json` | PASS before implementation |
| `tools/v7-convergence-status --json` | ALIGNED before implementation |
| `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --restart-admin-if-changed --json` | PASS |

Final post-deploy truth/convergence evidence is recorded in the evidence directory.

## 8. Remaining Blockers

| Blocker | Meaning |
| --- | --- |
| `comparisons_total = 0` | No real operator comparison has been recorded yet in production. |
| `shadow_comparison_history_below_minimum` | Minimum comparison count is not met. |
| `shadow_confidence_below_operator_floor` | Earned confidence is still below `70`. |
| Prediction confidence below floor | Operator comparison does not directly fix prediction confidence. |
| Event consumer certification missing | Operator comparison does not certify live event-driven apply. |

## 9. Updated Readiness

| Area | Before | After | Reason |
| --- | ---: | ---: | --- |
| Operator comparison path | 25% | 55% | Existing path now has durable review packet, rotated history read, separate comparison retention, and lifecycle tests. |
| Operator comparison evidence | 25% | 25% | Production still has `0` real comparisons. |
| Autonomous trust | 55% | 55% | No real comparison evidence was added. |
| Production autonomy | 43% | 43% | No apply gate changed; autonomy remains blocked. |

## 10. Final Verdict

`COMPARISON_PATH_READY`

The path is ready for real operator review collection. It is not yet evidence-rich enough to raise autonomous trust to the production floor.
