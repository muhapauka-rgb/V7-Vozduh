# PROGRAM SMALL BATCH STABILITY WINDOW AND MEDIUM BATCH REVIEW REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence folder: `small_batch_stability_evidence/`

Scope: observation and certification only. No user movement, no apply, no authority promotion, no MEDIUM_BATCH execution, no autonomy.

## 1. Production Truth

Production truth checks were run in read-only mode.

Evidence:

- `small_batch_stability_evidence/truth_check_all.json`
- `small_batch_stability_evidence/convergence_status.json`

Result:

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS |
| Runtime convergence | FULLY_ALIGNED |
| Runtime access status | READY |
| Runtime truth status | KNOWN |
| State truth status | KNOWN |
| `tools/v7-convergence-status --json` | PASS |
| Convergence status | ALIGNED |
| Runtime action status | READY_FOR_RUNTIME_ACTION |

Verdict: production truth is aligned.

## 2. SMALL_BATCH User Review

Reviewed users:

- `10.0.0.3`
- `10.0.0.6`

Evidence:

- `small_batch_stability_evidence/production_users_registry.txt`
- `small_batch_stability_evidence/production_egress_registry.txt`
- `small_batch_stability_evidence/production_service_matrix.json`
- `small_batch_stability_evidence/production_v7_state.json`
- `small_batch_stability_evidence/small_batch_stability_summary.json`

Current user state:

| User | Current egress | Enabled | Health verdict |
| --- | --- | --- | --- |
| `10.0.0.3` | `vless` | `1` | healthy |
| `10.0.0.6` | `vless` | `1` | healthy |

Current target egress metrics for `vless`:

| Metric | Value |
| --- | --- |
| average Mbps | `29.8583` |
| minimum Mbps | `17.45` |
| stability | `0.584427` |
| HTTP code | `200` |
| diagnostic severity | `SUSPECT` |
| diagnostic reason | `handshake_unsupported_for_protocol_vless` |

The protocol diagnostic remains limited/suspect because the generic handshake probe is not semantically valid for `vless`, but the service-level evidence overrides the quality floor. This is expected after the service truth freshness/transient classification fix.

Service matrix for both users on `vless`:

| Service | Status | Evidence |
| --- | --- | --- |
| YouTube | OK | reachable |
| Instagram | OK | reachable |
| Telegram | OK / reachable | TCP endpoints reachable |
| Google | OK | reachable |
| Google Auth | OK | reachable |

Rollback state:

| User | Verification | Rollback required | Rollback attempted |
| --- | --- | --- | --- |
| `10.0.0.3` | PASS | false | false |
| `10.0.0.6` | PASS | false | false |

Verdict: the 2-user SMALL_BATCH cohort remains healthy and does not require rollback.

## 3. Feedback Review

Evidence:

- `small_batch_stability_evidence/production_runtime_trust_tail.jsonl`
- `small_batch_stability_evidence/production_execution_events_tail.jsonl`
- `small_batch_stability_evidence/production_closure_records_tail.jsonl`
- `small_batch_stability_evidence/production_operator_execution_audit_tail.jsonl`
- `small_batch_stability_evidence/production_trust_summaries.json`
- `small_batch_stability_evidence/production_prediction_summaries.json`
- `small_batch_stability_evidence/production_candidate_suitability_summary.json`
- `small_batch_stability_evidence/production_trust_evolution_summaries.json`

Trust feedback:

| User | Source | Target | Outcome | Trust delta |
| --- | --- | --- | --- | --- |
| `10.0.0.3` | `awg3` | `vless` | success | `+1.0` |
| `10.0.0.6` | `awg3` | `vless` | success | `+1.0` |

Prediction feedback:

| User | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| `10.0.0.3` | `0.75` | `1.0` | success |
| `10.0.0.6` | `0.75` | `1.0` | success |

Closure:

| User | Closure state |
| --- | --- |
| `10.0.0.3` | CLOSED |
| `10.0.0.6` | CLOSED |

Snapshot families:

| Family | Freshness | Confidence |
| --- | --- | --- |
| trust summaries | FRESH | `1.0` |
| prediction summaries | FRESH | `0.9572` |
| trust evolution summaries | FRESH | `0.9804` |
| candidate suitability summary | FRESH | `0.8466` |

Recommendation state:

For both target users, `vless`, `awg0`, and `awg3` remain recommended as `prefer`. `vless` is eligible and accepted by the planner, while current recommendation scoring still ranks `awg0`/`awg3` slightly above `vless`. This is not a rollback condition, but it is relevant for MEDIUM_BATCH planning because the planner must continue to compare the full pool rather than blindly expand `vless`.

Verdict: outcome, trust, prediction, recommendation, and closure feedback are materialized.

## 4. Service Truth Review

Evidence:

- `small_batch_stability_evidence/production_service_matrix.json`
- `small_batch_stability_evidence/production_planner_dry_run.json`
- `small_batch_stability_evidence/small_batch_stability_summary.json`

Service truth classifier state:

| Check | Result |
| --- | --- |
| service truth classifier evidence active | true |
| transient classification active | true |
| persistent classification active | true |
| unexpected hard blocks for target users | none |

Target user service truth classes:

| Service | Truth class |
| --- | --- |
| YouTube | HEALTHY |
| Instagram | HEALTHY |
| Telegram | HEALTHY |
| Google | HEALTHY |
| Google Auth | HEALTHY |

Planner candidate reasons for `vless` include:

- `severity_protocol_diagnostic_limited_suspect`
- `quality_floor_overridden_by_service_evidence`
- `quality_history_fail_rate_high_advisory`
- service health OK reasons for YouTube, Instagram, Telegram, Google, and Google Auth
- `route_class_VIDEO_OPTIMIZED_ok`
- `best_available_pool_rank_1`

Verdict: service truth classification is active and is preventing protocol-diagnostic noise from incorrectly blocking service-proven channels.

## 5. Planner Review

Planner was run in dry-run mode only.

Evidence:

- `small_batch_stability_evidence/production_planner_dry_run.json`

Planner summary:

| Metric | Value |
| --- | --- |
| users_total | `18` |
| egress_total | `7` |
| healthy_egress_total | `2` |
| candidate_moves_total | `15` |
| selected_moves | `0` |
| reconnect_rotation_candidates | `0` |
| rebalance_candidates | `6` |
| terminal_state | `DRY_RUN` |
| terminal_reason | `dry_run_intelligence_snapshot_stop_required` |

Eligible channels:

- `awg0`
- `vless`

Best available pool:

- `awg0`
- `vless`

Planner stop condition:

| Condition | Value |
| --- | --- |
| intelligence snapshot stop required | true |
| stop families | `channel-service-scores`, `service-scores` |
| source mismatch families | `channel-service-scores`, `service-scores` |

Interpretation:

Planner behavior is sane in candidate discovery and channel eligibility, but it correctly stops before producing selected moves because intelligence snapshot source mismatch is present. This is a fail-closed behavior and should not be bypassed.

Verdict: planner safety behavior is valid, but planner readiness for MEDIUM_BATCH execution is not valid until snapshot source mismatch is closed.

## 6. Snapshot Refresh Review

Dry-run only. No snapshot write was performed.

Evidence:

- `small_batch_stability_evidence/production_snapshot_refresh_dry_run.json`

Result:

| Check | Result |
| --- | --- |
| refresh CLI dry-run | PASS |
| source_stable | true |
| snapshot_count | `11` |
| warnings | none |

Interpretation:

The approved snapshot refresh mechanism appears capable of producing stable snapshots, but the current program did not permit a write refresh. Therefore the source mismatch remains a blocker for MEDIUM_BATCH execution until an approved snapshot refresh write and follow-up planner dry-run are completed.

## 7. SMALL_BATCH Stability Verdict

SMALL_BATCH_STABLE=true.

Reason:

The two governed users remain on `vless`, are service-healthy, have verified successful execution outcomes, do not require rollback, and have materialized trust, prediction, recommendation, and closure feedback after deployment of service truth classification.

Important limitation:

This certifies the stability of the completed 2-user cohort. It does not certify MEDIUM_BATCH execution, because planner dry-run currently stops on intelligence snapshot source mismatch.

## 8. MEDIUM_BATCH Review

Target:

- authority: MEDIUM_BATCH
- budget: 5 users

Readiness:

| Requirement | Status |
| --- | --- |
| production truth aligned | ready |
| SMALL_BATCH cohort healthy | ready |
| rollback not required | ready |
| service truth model active | ready |
| feedback materialized | ready |
| planner dry-run clean | blocked |
| snapshot source mismatch closed | blocked |
| 5-user approval packet reviewed | not started |
| 5-user rollback manifest reviewed | not started |
| governed apply for 5 users | not safe |

Risk level: MEDIUM until snapshot mismatch is closed and a clean planner dry-run proves a bounded 5-user candidate set.

Required evidence before MEDIUM_BATCH execution:

1. Approved write snapshot refresh, using the existing `v7-intelligence-snapshot-refresh` mechanism.
2. Follow-up `v7-truth-check --all --json` PASS / FULLY_ALIGNED.
3. Follow-up planner dry-run without `dry_run_intelligence_snapshot_stop_required`.
4. Candidate set review for exactly up to 5 users.
5. Restore barrier and rollback manifest review for budget 5.
6. Operator approval packet review for budget 5.
7. Explicit user confirmation before any governed apply.

## Final Verdicts

| Verdict | Value |
| --- | --- |
| small_batch_stable | true |
| users_remain_healthy | true |
| rollback_required | false |
| service_truth_model_active | true |
| planner_behavior_valid | false |
| ready_for_medium_batch_review | true |
| safe_for_medium_batch_execution | false |
| SAFE_NEXT_STEP | `APPROVED_INTELLIGENCE_SNAPSHOT_REFRESH_WRITE_THEN_TRUTH_CHECK_AND_PLANNER_DRY_RUN` |

## Safe Next Step

Run a separate, explicitly approved snapshot refresh convergence stage:

1. Perform approved write refresh of intelligence snapshots.
2. Re-run production truth check.
3. Re-run convergence status.
4. Re-run planner dry-run.
5. If snapshot source mismatch is gone and the candidate set is bounded, proceed to a MEDIUM_BATCH approval-packet review.

Do not execute MEDIUM_BATCH until this blocker is closed.
