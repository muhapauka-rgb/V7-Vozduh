# AUTONOMY.EVIDENCE.2 Blast Radius And Operator Comparison Collection

Date: 2026-06-21T14:55:56Z
Branch: `Updatesystem`
Commit at audit start: `1cfad5a1c5c2a98b4793fb4cb3bdc360262d5c7a`
Mode: discovery / evidence collection dry-run only

Final verdict: `AUTONOMY_EVIDENCE_BLOCKED_BY_MISSING_OPERATOR_JUDGEMENT`

## 1. Scope

This phase ran two parts:

1. `AUTONOMY.BLAST.1`: explain why current production `blast_radius_confidence=0.0`.
2. `AUTONOMY.EVIDENCE.2`: prepare real operator comparison collection through the existing mechanism only.

No apply was executed. No users were moved. No daemon, autoswitch timer, planner, governance, execution path, truth source, confidence model, trust model, prediction model, floor, or threshold was changed.

## 2. Reference First

Read first:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`
- `docs/reports/AUTONOMY_EVIDENCE_1_REPORT.md`

The high-level state was already known: autonomy remains blocked by confidence, trust, prediction confidence, operator comparisons, and evidence boundaries. This phase adds the exact blast-radius materialization finding and the operator review packet.

## 3. Commands And Evidence

Discovery:

- `rg -n "blast|blast_radius|affected_users|users_moved|selected_move_count|selected_moves|rollback_required|rollback_executed|verification_passed|feedback_closed|learning_closed" tools admin_core admin docs --glob '!node_modules' --glob '!venv'`
- `find docs -iname '*BA*' -o -iname '*AUTONOMY*' -o -iname '*BLAST*'`
- `rg -n "BA1|BA3|BA4|blast|users_moved|selected_move|rollback|verification|feedback|learning" docs --glob '!node_modules' --glob '!venv'`
- `sed -n ... admin_core/intelligence_platform.py`
- `sed -n ... admin_core/intelligence_workers.py`
- `sed -n ... admin_core/operator_execution_feedback.py`
- `sed -n ... admin_core/operator_execution.py`
- `sed -n ... tools/v7-users-autoswitch`
- `sed -n ... tools/v7-operator-execution-packet`

Verification and API capture:

- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`
- `POST /login`
- `GET /api/session`
- `GET /api/operator/autonomous-dry-run`
- `GET /api/operator/overview`
- `GET /api/operator/decision-surface`

Evidence paths:

- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/truth_check.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/convergence_status.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/api_operator_autonomous_dry_run.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/api_operator_decision_surface.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/api_operator_overview.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/blast_radius_forensics.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/operator_review_packet.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/OPERATOR_REVIEW_PACKET.md`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/readiness_before_after.json`

`GET /api/operator/shadow-autonomy` was not used. The endpoint currently calls `shadow_autonomy_response(record=True)`, which appends decision records to the production shadow JSONL store. That write is safe in normal product use, but it is not a strict read-only audit action. The review packet instead derives deterministic decision ids from the read-only decision surface via the existing pure `admin_core.shadow_autonomy.shadow_decision_record` logic.

## 4. Part A Blast-Radius Findings

Verdict:

`BLAST_RADIUS_HISTORICAL_EVIDENCE_EXISTS_NOT_MATERIALIZED`

Calculation owner:

- `admin_core/intelligence_platform.py::blast_radius_confidence_model`

Row builder owner:

- `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows`

Snapshot family:

- `trust-evolution-summaries`

The blast-radius model expects explicit movement-radius outcome rows. Radius can come from:

- `blast_radius`
- `affected_users`
- `movement_count`
- `users_moved`
- `selected_move_count`
- `target_users`
- `users`
- `moved_users`
- `selected_moves`
- `moves`

The row must also have a known outcome. Successful rows without rollback-required count as high-confidence blast-radius evidence.

Current production consumed evidence still reports:

| Field | Value |
|---|---:|
| `blast_radius_confidence` | `0.0` |
| `candidate_outcomes_count` | `83` |
| `prediction_actuals_count` | `21` |
| `service_actuals_count` | `21` |

Historical governed feedback contains usable evidence. Using the existing builder against saved governed feedback records from `small_batch_stability_evidence` produced:

| Field | Value |
|---|---:|
| `records_seen` | `2` |
| `successful_small_operations` | `2` |
| `unsafe_large_operations` | `0` |
| `blast_radius_confidence` | `100.0` |

A previous local rebuilt snapshot also showed:

| Field | Value |
|---|---:|
| `blast_radius_confidence` | `100.0` |
| `blast_radius_evidence_count` | `2` |
| `records_seen` | `2` |
| `successful_small_operations` | `2` |

Evidence:

- `PROGRAM_BLAST_RADIUS_AND_SUITABILITY_EVIDENCE_BINDING_CLOSURE_REPORT.md`
- `docs/reports/evidence/blast_radius_suitability_evidence_binding_evidence/local_rebuilt_snapshots/trust-evolution-summaries.json`
- `docs/reports/evidence/small_batch_stability_evidence/production_execution_events_tail.jsonl`
- `docs/reports/evidence/small_batch_stability_evidence/production_closure_records_tail.jsonl`
- `docs/reports/evidence/small_batch_stability_evidence/production_runtime_trust_tail.jsonl`

## 5. Part A Root Cause

Root cause:

Historical BA/governed feedback evidence exists and is usable by the current code, but the current production autonomy dry-run is still consuming a `trust-evolution-summaries` view where blast-radius records are not materialized. This is a materialization/refresh gap between existing feedback stores and the production consumed snapshot, not a need for a new blast-radius model.

The historical BA evidence can be reused through existing owners if it is refreshed/materialized through the correct production feedback stores and then verified by a new autonomous dry-run.

| Question | Answer |
|---|---|
| Code change required? | Not proven. Existing code can classify the saved governed feedback into blast-radius evidence. |
| Snapshot refresh enough? | Likely, if run through existing `v7-intelligence-snapshot-refresh` against correct production feedback stores and then verified. |
| New truth source required? | No. |
| Historical BA reusable? | Yes, through existing feedback/snapshot owners. |
| New governed evidence required? | Not before trying production rematerialization. It may be needed only if production feedback stores lack the historical records. |

## 6. Part B Operator Comparison Findings

Current operator review packet:

| Field | Value |
|---|---:|
| Decisions total | `27` |
| MOVE_USER decisions | `10` |
| KEEP_USER decisions | `17` |
| Comparisons submitted | `0` |

No operator comparisons were submitted because no explicit real operator judgement was provided for the generated `decision_id` rows. Synthetic `agree` records are forbidden.

Prepared review packet:

- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/operator_review_packet.json`
- `docs/reports/AUTONOMY_EVIDENCE_2_EVIDENCE/OPERATOR_REVIEW_PACKET.md`

Each row contains:

- `decision_id`
- `user`
- `current_channel`
- `recommended_action`
- `recommended_target`
- `reason`
- `confidence`
- `risk`
- `trust`
- `prediction_confidence`
- `blockers`
- required operator decision: `agree / disagree / override`

Valid collection path remains:

- existing endpoint: `/api/actions/shadow-autonomy-compare`
- requires auth and CSRF
- writes existing `operator_comparison` record only
- reports `runtime_mutation_performed=false`, `users_moved=0`, `apply_executed=false`, `autonomy_enabled=false`

## 7. Before / After Readiness

| Metric | Before | After |
|---|---:|---:|
| `comparisons_total` | `0` | `0` |
| `earned_confidence` | `45.825` | `45.813` |
| `confidence` | `45.8` | `45.8` |
| `trust` | `39.584` | `39.308` |
| `prediction_confidence` | `39.6` | `39.6` |
| `blast_radius_confidence` | `0.0` | `0.0` |
| `rollback_confidence` | `100.0` | `100.0` |
| `candidate_count` | `1` | `1` |
| `execution_allowed_now` | `false` | `false` |
| `apply_executed` | `false` | `false` |
| `users_moved` | `0` | `0` |

Hard stop blockers remain:

- `confidence_too_low`
- `trust_too_low`
- `prediction_confidence_too_low`

Current autonomous dry-run candidate:

| User | From | To | Allowed |
|---|---|---|---|
| `10.0.0.3` | `wireguard-1779454504-c43409` | `awg0` | No |

## 8. Blockers

| Blocker | Meaning | Current Status |
|---|---|---|
| Blast-radius materialization gap | Historical evidence exists but is not reflected in current production consumed autonomy snapshot | Still open |
| Missing operator judgement | No real `agree/disagree/override` decisions supplied | Still open |
| `confidence_too_low` | Candidate confidence below floor | Still open |
| `trust_too_low` | Trust below floor; blast-radius remains 0 in consumed snapshot | Still open |
| `prediction_confidence_too_low` | Prediction confidence below floor | Still open |

## 9. Apply Decision

NO APPLY.

Reasons:

- This phase is evidence-only.
- Operator comparison evidence was not collected because real operator judgement was unavailable.
- Current production dry-run still fails safety floors.
- Blast-radius historical evidence is not yet materialized into current production consumed autonomy evidence.

## 10. Documentation Updates

Updated:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

ADR:

- No ADR created. The event-driven autonomy architecture did not change.

## 11. Next Phase

Exact next safe phase:

`AUTONOMY.EVIDENCE.3_PRODUCTION_SNAPSHOT_REMATERIALIZATION_AND_OPERATOR_REVIEW`

Scope:

1. Run existing production snapshot refresh/materialization against real production feedback stores.
2. Re-read `trust-evolution-summaries` and autonomous dry-run.
3. Confirm whether `blast_radius_confidence` moves from `0.0` to the historical expected value.
4. Present `OPERATOR_REVIEW_PACKET.md` to the operator.
5. Submit comparisons only for rows where the operator explicitly chooses `agree`, `disagree`, or `override`.
6. Re-read shadow/autonomy readiness.
7. Stop before apply.

## 12. Final Verdict

`AUTONOMY_EVIDENCE_BLOCKED_BY_MISSING_OPERATOR_JUDGEMENT`

Secondary status:

`BLAST_RADIUS_HISTORICAL_EVIDENCE_EXISTS_NOT_MATERIALIZED`

The evidence paths exist. Historical blast-radius evidence is reusable through existing owners, but current production consumed autonomy evidence still shows `blast_radius_confidence=0.0`. Operator comparisons were not collected because doing so without real operator judgement would be fake confidence inflation.
