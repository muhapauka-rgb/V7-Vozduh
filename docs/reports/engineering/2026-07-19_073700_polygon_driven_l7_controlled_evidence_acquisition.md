Mission ID: `V7_POLYGON_DRIVEN_L7_CONTROLLED_EVIDENCE_ACQUISITION_V1`
Run Nonce: `V7_POLYGON_L7_ACQ_20260719T073700Z`

# Polygon-driven L7 controlled evidence acquisition

Status: `COMPLETE_CONSUMED`

## Result

- Discovery/reuse: existing Polygon, Controlled Production, delegated-policy, Situation/Decision/Packet, Verification, outcome, Learning, replay, CPS and OMP owners reused; no second owner, store, watcher, queue or truth source created.
- L8 defect closed: consumers now discover real date-partitioned `telegram-sentinel-YYYYMMDD.jsonl` and `service-matrix-refresh-YYYYMMDD.jsonl` producers. Fresh production read consumed 1,290 event records; all five capture roles pass.
- Controlled opportunity: Polygon selected the exact `controlled_production_present` cell and a genuine policy-admitted production need. No ordinary customer was relabelled solely to manufacture evidence.
- Real transaction: `govdry_9120aeee5c81eb6b41d0542b` / `runtime_autoswitch_3fbda1bafa1cd40b251555b0`; Packet `pkt_preview_41ea92391de82055aff5da5b`; Decision `decision_commit_63e253d2145710961cd8c4ed`; user `10.0.0.3`; `awg3 -> vless`; terminal `SUCCESS`; verification PASS; rollback not required; final Admin Safe Mode OPEN.
- Learning: `learn_7fe115732d2495a0eec80673` consumed the real outcome through existing owners.
- Identity repair: transitive owner-ID union collapses 18 event/outcome/feedback/Learning/lease records into one material Passport instead of three duplicates.
- Controlled Passport: `outpass_57779380ae119a2932498de8`
- Replay: Decision Trace, bound snapshot `731ea11341f5db848d06f0e2ae5f479b61d23a8db65750b3b1d0576c6ad39668`, expected/actual `SUCCESS` and `NO_DRIFT` all PASS.
- Temporal terminal: `PASS`
- Eligibility set: `outset_a30d20db4837099f36706414`; one eligible controlled Passport; `complete_temporal_and_replay=true`; `controlled_production_present=true`.
- L8 capture readiness: `PASS`
- Controlled next boundary: `ENGINEERING_AUTHORITY`
- Authority impact: `NONE`
- Production Maturity: `NO_CHANGE`

## Mission terminals

| Stage | Terminal |
| --- | --- |
| `P0/P1` | exact gap and highest-value scenario `COMPLETE_CONSUMED` |
| `P2` | next deliberate condition/certification pool `ENGINEERING_AUTHORITY_REQUIRED_FOR_CERTIFICATION_POOL_OR_DELIBERATE_CONDITION` |
| `P3` | L8 owner chain `READY_FOR_NEXT_NATURAL_EVENT` |
| `P4` | one real bounded controlled transaction `COMPLETE_CONSUMED`; no fresh genuine Candidate remains |
| `P5` | natural evidence `EVENT_DRIVEN_CAPTURE_READY`; no natural event manufactured |
| `P6` | immutable set `INSUFFICIENT_EVIDENCE` |
| `P7` | `INSUFFICIENT_EVIDENCE`; current `GOVERNED_ONLY` scope retained |
| `M8` | `MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT` |

## Exact residual

Remaining cells are exactly `eligible_passports_at_least_5`, `material_variation_present`, `natural_production_present`, and `rollback_and_no_rollback_present`. The controlled lane stops at independent Engineering Authority because no fresh genuine Candidate exists and the available certification source is disabled; the natural lane separately stops at `REAL_WORLD_LIMIT` with complete capture readiness.

## Verification and deployment

- Focused regression: `201 tests`, PASS.
- Production code deploys: `20b0df5261ab768c3a25554e329e5deb1e832818` / `deploy-z8-14-Updatesystem-20b0df5-20260719T134934`; finalizer `6d708c79daaaddeb4eb0031716c01599e7d88c8e` / `deploy-z8-14-Updatesystem-6d708c7-20260719T140652`.
- Latest deploy delta: only `tools/v7_sync_lib.py` and `tools/v7-truth-check`; blockers none; systemd/routing/user/packet/restore-barrier/rollback/Authority/maturity effects none.
- The one user movement above was the separately admitted real controlled-production transaction, not a deploy effect. It remained inside the approved one-user/one-transaction delegated policy.
- Final truth, convergence and local/GitHub/production equality: `PENDING_FINAL_CPS_COMMIT`.
