# AUTONOMY.REMATERIALIZATION.4 Rotated Store Recovery Preview

Timestamp: 2026-06-22T10:10:42Z  
Branch: `Updatesystem`  
Commit at preview start: `ede2c1290add8b563b0d7a28538f9a9e5232c4ea`  
Mode: preview only, no production mutation

Final verdict: `BLAST_RECOVERY_HAS_MODERATE_READINESS_IMPACT`

## 1. Scope

This phase estimated what autonomy metrics would become if rotated blast-radius evidence became visible to the existing trust-evolution pipeline.

No runtime apply was executed. No users were moved. No daemon or autoswitch was enabled. No production snapshot was written. No feedback store, archive, active store, threshold, floor, confidence model, trust model, prediction model, planner, governance path, execution path, or truth source was changed.

## 2. Reference First

Read first:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_PROJECT_MAP.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`
- `docs/reports/AUTONOMY_EVIDENCE_1_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_2_BLAST_AND_COMPARISON_REPORT.md`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_REPORT.md`
- `docs/reports/AUTONOMY_REMATERIALIZATION_2_REPORT.md`
- `docs/reports/AUTONOMY_REMATERIALIZATION_3_REPORT.md`

Starting truth from REMATERIALIZATION.3: active feedback stores are empty, while rotated `.jsonl.1` production stores contain real governed evidence that the existing builder can classify into 11 blast-radius rows.

## 3. Commands And Evidence

Commands:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`
- `rg -n "AUTONOMY_BLAST_RADIUS|REMATERIALIZATION|blast_radius_confidence|trust-evolution|prediction_confidence|operator comparison|confidence gate|trust gate|prediction gate" ...`
- `rg -n "def .*trust|blast_radius_confidence|prediction_confidence|confidence_gate|trust_gate|prediction_gate|trust_evolution|comparison|autonomy" admin_core tools admin ...`
- Read-only production preview probe using existing `admin_core.intelligence_workers` and `admin_core.intelligence_platform` functions.

Evidence:

- `docs/reports/AUTONOMY_REMATERIALIZATION_4_EVIDENCE/production_rotated_recovery_preview.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_4_EVIDENCE/analysis_summary.json`

The production probe wrote no V7 state. A temporary probe file was copied only to `/tmp` on production because interactive SSH stdin truncated the script; it was removed immediately after execution. The probe read production stores, built snapshots in memory, and returned JSON evidence.

## 4. Preview Inputs

Active default feedback stores:

| Store | Records |
| --- | ---: |
| `/opt/v7/egress/state/execution-events.jsonl` | 0 |
| `/opt/v7/egress/state/runtime-trust.jsonl` | 0 |
| `/opt/v7/egress/state/proposal-records.jsonl` | 0 |
| `/opt/v7/egress/state/proposals.jsonl` | 0 |
| `/opt/v7/egress/state/closure-records.jsonl` | 0 |

Rotated feedback stores:

| Store | Records |
| --- | ---: |
| `/opt/v7/egress/state/execution-events.jsonl.1` | 148 |
| `/opt/v7/egress/state/runtime-trust.jsonl.1` | 74 |
| `/opt/v7/egress/state/proposal-records.jsonl.1` | 74 |
| `/opt/v7/egress/state/proposals.jsonl.1` | 2 |
| `/opt/v7/egress/state/closure-records.jsonl.1` | 74 |

## 5. Preview Outputs

Two preview modes were separated because they answer different questions.

### Strict Rotated Refresh Equivalent

This uses the same full refresh-equivalent flow with rotated files as feedback inputs.

Result:

| Metric | Current | Strict Rotated Refresh Equivalent |
| --- | ---: | ---: |
| `blast_radius_confidence` | 0.0 | 0.0 |
| `blast_evidence_count` | 0 | 0 |
| `overall_confidence` | 42.678 | 42.678 |
| operator `confidence` | 45.8 | 45.8 |
| operator `trust` | 39.602 | 39.579 |
| operator `prediction_confidence` | 39.6 | 39.6 |

Important finding: simply pointing the full refresh-equivalent pipeline at rotated feedback files is still not sufficient. The trust-evolution snapshot bounds the combined decision stream to the latest 1000 decisions, and the useful rotated blast rows are not visible in that final bounded set.

### Visible Blast Rows Counterfactual

This uses the existing builder-classified rotated blast rows as visible `blast_radius_records` for the existing `trust_evolution_summary` model. No snapshot was written.

Result:

| Metric | Current | Preview |
| --- | ---: | ---: |
| `blast_radius_confidence` | 0.0 | 100.0 |
| `blast_evidence_count` | 0 | 11 |
| `overall_confidence` | 42.678 | 59.345 |
| operator `confidence` | 45.8 | 45.8 |
| operator `trust` | 39.602 | 54.684 |
| operator `prediction_confidence` | 39.6 | 39.6 |

The 11 visible rows materially improve blast-radius and trust, but not confidence or prediction confidence.

## 6. Autonomy Gate Preview

Floors:

| Gate | Floor |
| --- | ---: |
| confidence | 70.0 |
| trust | 70.0 |
| prediction confidence | 70.0 |

Strict rotated refresh equivalent:

| Gate | Preview | Gap | Pass |
| --- | ---: | ---: | --- |
| confidence | 45.8 | 24.2 | no |
| trust | 39.579 | 30.421 | no |
| prediction confidence | 39.6 | 30.4 | no |

Visible blast rows counterfactual:

| Gate | Preview | Gap | Pass |
| --- | ---: | ---: | --- |
| confidence | 45.8 | 24.2 | no |
| trust | 54.684 | 15.316 | no |
| prediction confidence | 39.6 | 30.4 | no |

Autonomy remains blocked after blast recovery. The dominant remaining blocker becomes `prediction_confidence`, with `confidence` still a close second blocker.

## 7. Delta Analysis

| Area | Current | Preview | Delta |
| --- | ---: | ---: | ---: |
| blast-radius evidence count | 0 | 11 | +11 |
| blast-radius confidence | 0.0 | 100.0 | +100.0 |
| overall trust-evolution confidence | 42.678 | 59.345 | +16.667 |
| operator trust gate value | 39.602 | 54.684 | +15.082 |
| operator confidence gate value | 45.8 | 45.8 | 0.0 |
| operator prediction gate value | 39.6 | 39.6 | 0.0 |

## 8. Readiness Impact

| Question | Answer |
| --- | --- |
| Does blast recovery materially improve readiness? | Yes. It moves blast confidence to 100.0 and trust to 54.684 in the visible-row preview. |
| Does it remove the trust blocker? | No. Trust remains below 70.0. |
| Does it remove the confidence blocker? | No. Confidence remains 45.8. |
| Does it remove the prediction blocker? | No. Prediction confidence remains 39.6. |
| Which blocker becomes dominant afterwards? | `prediction_confidence_too_low` by gap size. |
| Is recovery worth executing? | Yes, but only as a bounded materialization/recovery step; it is not enough to enable autonomy. |

## 9. Next Phase Recommendation

Chosen next phase: `AUTONOMY.PREDICTION.EVIDENCE.1`

Reason: once blast rows are visible, the largest remaining gap is prediction confidence: `39.6 -> 70.0`, gap `30.4`. Confidence also remains below floor, so the prediction phase should collect only real matched prediction actuals through existing owners and should not lower floors or synthesize evidence.

Recovery itself still needs an approved execution phase because strict rotated refresh-equivalent input does not make rows visible to the consumed snapshot. The recovery phase must therefore materialize real builder-classified blast rows into the existing consumed path, not merely pass rotated files to the default refresh.

## 10. Safety

| Check | Result |
| --- | --- |
| Runtime apply | not executed |
| Users moved | 0 |
| Daemon enabled | no |
| Autoswitch enabled | no |
| Production snapshot write | no |
| Production feedback write | no |
| Archive restore | no |
| Active store modification | no |
| Synthetic evidence | no |
| Manual trust manipulation | no |

## 11. Remaining Problems

1. Current consumed production snapshot still has `blast_radius_confidence=0.0`.
2. Strict rotated refresh-equivalent inputs still produce `blast_radius_confidence=0.0` because the rows do not survive into the bounded decision set.
3. A recovery phase must make real blast rows visible as `blast_radius_records` through an existing owner.
4. Even after visible blast recovery, autonomy remains blocked by confidence, trust, and prediction confidence floors.
5. Prediction confidence becomes the dominant remaining blocker.

## 12. Final Verdict

`BLAST_RECOVERY_HAS_MODERATE_READINESS_IMPACT`

Blast recovery is worth doing because it materially raises trust and proves the blast-radius model path, but it is not a direct route to autonomy. The exact next evidence phase is `AUTONOMY.PREDICTION.EVIDENCE.1`.
