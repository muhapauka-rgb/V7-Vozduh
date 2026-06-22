# V7 Project Map

Status: project readiness map
Last updated: 2026-06-22
Last changed by: `AUTONOMY.FINAL.BRANCH_1A`

This map tracks current roadmap/readiness position. Percent values are operational readiness estimates for the named area, not product marketing scores.

## Current Position

V7 remains runtime/truth aligned, but the pool stability position changed after POOL.2.

POOL.1 classified the pool as stable with zero planner candidates. POOL.2 rechecked production and found the assignment distribution unchanged, but planner pressure returned:

- `awg3 = 8`
- `wireguard-1779454504-c43409 = 8`
- `vless = 10`
- `candidate_moves_total = 8`
- `healthy_egress_total = 2`
- all current move candidates are `awg3 -> wireguard-1779454504-c43409`

Current roadmap position:

`CHANNEL_RECOVERY_AWG3_AWG0_STABILITY_REVIEW`

## Changed Areas

| Area | Previous % | Current % | Delta | Last changed by | Reason |
| --- | ---: | ---: | ---: | --- | --- |
| Pool equilibrium readiness | 100% | 65% | -35% | `PROGRAM POOL.2` | POOL.1 had `candidate_moves_total=0`; POOL.2 found `candidate_moves_total=8` because `awg3` is no longer planner-eligible. |
| Channel pool health readiness | 85% | 60% | -25% | `PROGRAM POOL.2` | Planner healthy pool fell from 3 to 2. `awg3` is blocked by `min_mbps_below_floor` and `stability_below_floor`; `awg0` improved but remains below the `0.45` stability floor. |
| Autonomy execution readiness | 100% | 80% | -20% | `PROGRAM POOL.2` | Previous 1/2/5/10-user autonomy certifications remain valid, but new autonomous execution should not proceed until current pool recovery/failover pressure is reviewed. |
| Roadmap clarity | 90% | 95% | +5% | `PROGRAM POOL.2` | Next step became explicit: channel recovery review for `awg3` and `awg0`, not another broad autonomy or architecture phase. |
| Blast Materialization | 20% | 75% | +55% | `AUTONOMY.REMATERIALIZATION.3` | Root cause found: active refresh stores are empty, while real governed blast evidence exists in rotated `.jsonl.1` stores and current builder produces 11 rows from them. Recovery is not executed yet. |
| Autonomous Trust | 40% | 45% | +5% | `AUTONOMY.REMATERIALIZATION.3` | Trust did not numerically recover, but the evidence gap is now localized to rotated-store inclusion rather than model uncertainty. |
| Production Autonomy | 30% | 35% | +5% | `AUTONOMY.REMATERIALIZATION.3` | Production autonomy remains disabled and below floors, but the blast-radius blocker now has an exact safe recovery path. |
| Blast Materialization | 75% | 80% | +5% | `AUTONOMY.REMATERIALIZATION.4` | Preview proved that strict rotated refresh-equivalent inputs still do not surface blast rows, but supplying the 11 builder-classified rows as visible `blast_radius_records` moves blast confidence to `100.0`. Recovery is still not executed. |
| Autonomous Trust | 45% | 55% | +10% | `AUTONOMY.REMATERIALIZATION.4` | Visible blast-row preview raises operator trust from `39.602` to `54.684`, but trust remains below the `70.0` floor. |
| Production Autonomy | 35% | 38% | +3% | `AUTONOMY.REMATERIALIZATION.4` | Blast recovery has moderate readiness impact but does not remove confidence, trust, or prediction blockers; prediction confidence becomes the dominant remaining blocker. |
| Prediction Evidence Understanding | 35% | 90% | +55% | `AUTONOMY.PREDICTION.EVIDENCE.1` | Production forensics mapped the existing forecast -> actual -> confidence path and proved the blocker is low forecast/source confidence, not missing row matches. |
| Prediction Evidence Quality | 35% | 45% | +10% | `AUTONOMY.PREDICTION.EVIDENCE.1` | All 21 forecasts matched actuals with mean accuracy `98.488`, but mean forecast confidence is only `0.3792`, so outcome prediction confidence remains `37.351`. |
| Production Autonomy | 38% | 40% | +2% | `AUTONOMY.PREDICTION.EVIDENCE.1` | Autonomy is not safer yet, but the dominant prediction blocker is now quantified and the next evidence-collection phase is exact. |
| Blast Recovery | 80% | 90% | +10% | `AUTONOMY.FINAL.BRANCH_1` | Blast branch execution planning is closed with a concrete NO-GO reason for immediate recovery and an exact existing-owner visibility step. |
| Autonomous Trust | 55% | 55% | 0% | `AUTONOMY.FINAL.BRANCH_1` | No production snapshot was written; expected visible recovery still raises trust to `54.684`, below floor. |
| Production Autonomy | 40% | 40% | 0% | `AUTONOMY.FINAL.BRANCH_1` | No autonomy gate passes after blast recovery; confidence, trust, and prediction confidence remain below `70.0`. |
| Blast Branch | 90% | 100% | +10% | `AUTONOMY.FINAL.BRANCH_1A` | Existing-owner visibility fix dry-run passed with 11 real production blast rows and blast confidence `100.0`; branch is closed. |
| Blast Recovery | 90% | 95% | +5% | `AUTONOMY.FINAL.BRANCH_1A` | The evidence path is fixed and proven in dry-run; deploy plus approved snapshot-only recovery write remain. |
| Autonomous Trust | 55% | 59% | +4% | `AUTONOMY.FINAL.BRANCH_1A` | Trust-evolution dry-run overall confidence is `59.358`; trust still remains below the autonomy floor. |
| Production Autonomy | 40% | 42% | +2% | `AUTONOMY.FINAL.BRANCH_1A` | Blast branch no longer blocks conceptually, but confidence, trust, prediction confidence, and operator comparison evidence still block production autonomy. |

## Stable Areas

| Area | Current % | State | Evidence |
| --- | ---: | --- | --- |
| Runtime truth / convergence | 100% | PASS / FULLY_ALIGNED | `POOL2_EVIDENCE/truth_check.json`, `POOL2_EVIDENCE/convergence_status.json` |
| Snapshot gate | 100% | PASS | `stop_required=false`, `source_mismatch_families=[]` |
| Atomic envelope | 100% | valid | `condition=ENVELOPE_VALID`, `mismatches=[]` |
| Current distribution evidence | 100% | known | `POOL2_EVIDENCE/current_distribution.json` |

## Open Roadmap Items

| Priority | Item | Why |
| --- | --- | --- |
| P1 | `CHANNEL_RECOVERY_AWG3_AWG0_STABILITY_REVIEW` | `awg3` has 8 assigned users but is currently not eligible; `awg0` is close to recovery but still below stability floor. |
| P2 | Decide whether `awg3` recovers naturally or needs a governed failover review | POOL.2 found 8 failover candidates but did not execute movement by design. |
| P3 | Continue pool observation only after recovery/failover pressure is resolved | Current state is not clean equilibrium because planner disagrees with keeping `awg3` users there. |

## Changelog

### 2026-06-22 — AUTONOMY.FINAL.BRANCH_1A Blast Visibility Owner Fix

- Implemented the existing-owner visibility fix in `admin_core.intelligence_workers.build_trust_evolution_snapshot`.
- Changed blast row construction to use full existing `decision_records` before shared `[-1000]` bounding can hide older governed feedback; other outcome mappers remain bounded.
- Production-data dry-run with real rotated `.jsonl.1` inputs produced `blast_radius_evidence_count=11`, `blast_radius_confidence=100.0`, `trust_evolution_overall_confidence=59.358`, `users_moved=0`, and `snapshot_written=false`.
- Updated changed-area percentages:
  - Blast Branch: `90% -> 100%`
  - Blast Recovery: `90% -> 95%`
  - Autonomous Trust: `55% -> 59%`
  - Production Autonomy: `40% -> 42%`
- Recorded next phase: `AUTONOMY.FINAL.BRANCH_1B_DEPLOY_VISIBILITY_FIX_AND_SNAPSHOT_RECOVERY_APPROVAL`.

### 2026-06-22 — AUTONOMY.FINAL.BRANCH_1 Blast Branch Execution Planning

- Closed blast recovery planning with immediate execution `NO-GO`.
- Confirmed as-is recovery paths can still produce no metric change because `build_trust_evolution_snapshot` bounds `decision_records[-1000:]` after appending large `switch-history`, which can push restored feedback rows out of the consumed set.
- Confirmed expected visible-row impact remains useful but insufficient: blast confidence `0.0 -> 100.0`, trust `39.602 -> 54.684`, prediction `39.6 -> 39.6`, confidence `45.8 -> 45.8`.
- Updated changed-area percentages:
  - Blast Recovery: `80% -> 90%`
  - Autonomous Trust: `55% -> 55%`
  - Production Autonomy: `40% -> 40%`
- Recorded next phase: `AUTONOMY.FINAL.BRANCH_1A_BLAST_VISIBILITY_OWNER_FIX_AND_DRY_RUN`.

### 2026-06-22 — AUTONOMY.PREDICTION.EVIDENCE.1 Prediction Evidence Forensics

- Ran read-only production prediction forensics with no apply, no snapshot write, and `users_moved=0`.
- Confirmed prediction matching is not the current gap: `forecasts_seen=21`, `matched_count=21`, `unmatched_forecasts=0`, `ignored_service_actuals=0`.
- Confirmed forecast accuracy is high: mean accuracy `98.488`.
- Confirmed forecast/source confidence is low: mean forecast confidence `0.3792`, outcome prediction confidence `37.351`, current candidate prediction confidence still `39.6`, floor `70.0`.
- Updated changed-area percentages:
  - Prediction Evidence Understanding: `35% -> 90%`
  - Prediction Evidence Quality: `35% -> 45%`
  - Production Autonomy: `38% -> 40%`
- Recorded next evidence phase: `AUTONOMY.PREDICTION.EVIDENCE.2_REAL_OUTCOME_CONFIDENCE_COLLECTION`.

### 2026-06-22 — AUTONOMY.REMATERIALIZATION.4 Recovery Preview

- Previewed strict rotated refresh-equivalent inputs: `blast_radius_confidence` remained `0.0` because rotated rows still did not become visible in the final bounded trust-evolution set.
- Previewed visible-row materialization with the 11 existing builder-classified blast rows: `blast_radius_confidence 0.0 -> 100.0`, `overall_confidence 42.678 -> 59.345`, operator trust `39.602 -> 54.684`.
- Confirmed autonomy remains blocked after blast recovery: confidence `45.8`, trust `54.684`, prediction confidence `39.6`, all below the `70.0` autonomy floor.
- Updated changed-area percentages:
  - Blast Materialization: `75% -> 80%`
  - Autonomous Trust: `45% -> 55%`
  - Production Autonomy: `35% -> 38%`
- Recorded next evidence phase: `AUTONOMY.PREDICTION.EVIDENCE.1`.

### 2026-06-22 — AUTONOMY.REMATERIALIZATION.3 Store Forensics

- Certified root cause: `BLAST_RECORDS_IN_DIFFERENT_STORE`.
- Found active default feedback stores are empty: `execution-events.jsonl`, `runtime-trust.jsonl`, `proposal-records.jsonl`, `proposals.jsonl`, and `closure-records.jsonl` have 0 records.
- Found real governed evidence in production rotated stores: `.jsonl.1` inputs produce 11 valid blast-radius rows with the existing builder.
- Updated changed-area percentages:
  - Blast Materialization: `20% -> 75%`
  - Autonomous Trust: `40% -> 45%`
  - Production Autonomy: `30% -> 35%`
- Recorded safe next stage: `AUTONOMY.REMATERIALIZATION.4_ROTATED_STORE_RECOVERY_DRY_RUN_AND_APPROVAL`.

### 2026-06-22 — PROGRAM POOL.2 Project Map Update

- Added canonical project map file because `docs/reference/V7_PROJECT_MAP.md` did not previously exist.
- Recorded POOL.2 roadmap change from `POOL_STABLE` to `POOL_NEEDS_RECOVERY`.
- Added changed-area percentages:
  - Pool equilibrium readiness: `100% -> 65%`
  - Channel pool health readiness: `85% -> 60%`
  - Autonomy execution readiness: `100% -> 80%`
  - Roadmap clarity: `90% -> 95%`
- Recorded safe next stage: `CHANNEL_RECOVERY_AWG3_AWG0_STABILITY_REVIEW`.
