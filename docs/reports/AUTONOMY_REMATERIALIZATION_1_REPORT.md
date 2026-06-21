# AUTONOMY.REMATERIALIZATION.1 Blast-Radius Recovery And Trust Recalculation

Timestamp: 2026-06-21T15:18:45Z  
Branch: `Updatesystem`  
Commit at audit start: `d519bcbf736653538ea9975386213babd5438007`  
Mode: discover / verify only

Final verdict: `AUTONOMY_REMATERIALIZATION_POSSIBLE_REQUIRES_REFRESH`

## 1. Scope

This phase verified whether blast-radius confidence can be recovered through existing production materialization paths.

No apply was executed. No users were moved. No daemon or autoswitch was enabled. No planner, governance, execution path, truth source, trust model, confidence model, prediction model, floors, or thresholds were changed.

## 2. Reference First

Read first:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`
- `docs/reports/AUTONOMY_EVIDENCE_1_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_2_BLAST_AND_COMPARISON_REPORT.md`

Known starting truth: historical governed blast-radius evidence exists, but the production autonomy snapshot consumed by the current dry-run still reports `blast_radius_confidence=0.0`.

## 3. Commands And Evidence

Discovery and verification commands:

- `rg -n "v7-intelligence-snapshot-refresh|trust-evolution|snapshot refresh|materialize|rematerialize|build_blast_radius_evidence_rows|blast_radius_confidence|execution-events|runtime-trust|closure-records|feedback-log" tools admin_core admin docs ...`
- `sed -n ... tools/v7-intelligence-snapshot-refresh`
- `sed -n ... admin_core/intelligence_workers.py`
- `sed -n ... admin_core/intelligence_platform.py`
- `tools/v7-intelligence-snapshot-refresh --help`
- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`
- `POST /login`
- `GET /api/session`
- `GET /api/operator/autonomous-dry-run`
- `GET /api/operator/decision-surface`
- `GET /api/operator/overview`
- Local existing-builder exercise against saved production feedback files from `small_batch_stability_evidence`

Evidence paths:

- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/truth_check.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/convergence_status.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/api_operator_autonomous_dry_run.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/api_operator_decision_surface.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/api_operator_overview.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/api_session.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/snapshot_refresh_help.txt`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/local_blast_rematerialization.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_1_EVIDENCE/analysis_summary.json`

Direct SSH file probing was attempted in strict `BatchMode` and failed with publickey/password denial. No production files were modified or read directly over SSH in this phase. Production API read-only capture succeeded, and truth/convergence retained runtime access.

## 4. Dependency Chain

| Stage | Owner | Input | Output | Current Finding |
| --- | --- | --- | --- | --- |
| Historical governed execution | Existing BA/governed runs | Verified one-user and two-user applied operations | Execution feedback, runtime trust, closure records | Reusable evidence exists |
| Feedback materialization | `admin_core/operator_execution_feedback.py` | Execution contracts/outcomes | `execution-events.jsonl`, `runtime-trust.jsonl`, `closure-records.jsonl` | Saved production evidence contains success/no-rollback rows |
| Row builder | `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows` | Existing feedback/audit records | Blast-radius evidence rows | Current code builds 2 rows |
| Model | `admin_core/intelligence_platform.py::blast_radius_confidence_model` | Blast-radius rows | `blast_radius_confidence` | Current code returns `100.0` on those rows |
| Snapshot refresh | `tools/v7-intelligence-snapshot-refresh` | State, audit, feedback stores | `trust-evolution-summaries.json` | Existing CLI supports required inputs |
| Runtime consumer | `/api/operator/autonomous-dry-run` | `trust-evolution-summaries` | autonomy gates | Current production capture still consumes `blast_radius_confidence=0.0` |

## 5. Blast-Radius Forensics

Required movement-radius fields are already supported by the existing builder:

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

The local existing-builder exercise consumed saved production feedback sources:

| Source | Records |
| --- | ---: |
| `small_batch_stability_evidence/production_operator_execution_audit_tail.jsonl` | 28 |
| `small_batch_stability_evidence/production_execution_events_tail.jsonl` | 6 |
| `small_batch_stability_evidence/production_runtime_trust_tail.jsonl` | 3 |
| `small_batch_stability_evidence/production_closure_records_tail.jsonl` | 3 |

Rows produced:

| Operation | Blast Radius | Result | Rollback Required |
| --- | ---: | --- | --- |
| `runtime_autoswitch_e33f678dabd7ad432b38f2a7` | 1 | success | false |
| `runtime_autoswitch_b5063a475a06312ff23c90a7` | 2 | success | false |

Model result:

| Field | Value |
| --- | ---: |
| `records_seen` | 2 |
| `successful_small_operations` | 2 |
| `unsafe_large_operations` | 0 |
| `blast_radius_confidence` | 100.0 |

## 6. Materialization Capability

`tools/v7-intelligence-snapshot-refresh` already supports:

- `--feedback-log`
- `--execution-events-file`
- `--runtime-trust-file`
- `--proposal-records-file`
- `--closure-records-file`
- `--dry-run`
- `--out-dir`

The tool explicitly states it writes only intelligence snapshot files and does not move users, write selected moves, approve governance, execute runtime actions, restart services, or integrate snapshots into planner decisions.

Therefore the existing materialization capability exists. The missing step is a production refresh against the correct production feedback stores, followed by re-reading `trust-evolution-summaries` and `/api/operator/autonomous-dry-run`.

## 7. Current Production Capture

Fresh read-only API capture:

| Field | Value |
| --- | ---: |
| `confidence` | 39.597 |
| `trust` | 39.597 |
| `prediction_confidence` | 39.6 |
| `blast_radius_confidence` | 0.0 |
| `execution_allowed_now` | false |
| `apply_executed` | false |
| `users_moved` | 0 |

Hard-stop blockers:

- `confidence_too_low`
- `trust_too_low`
- `prediction_confidence_too_low`

Truth/convergence:

| Check | Status |
| --- | --- |
| Truth | `PASS`, `FULLY_ALIGNED`, runtime access `READY` |
| Convergence | `PASS`, `ALIGNED`, runtime action status `READY_FOR_RUNTIME_ACTION` |

## 8. Trust Impact Analysis

Current components from the fresh autonomy dry-run:

| Component | Value |
| --- | ---: |
| `decision_confidence` | 50.0 |
| `service_confidence` | 39.225 |
| `suitability_confidence` | 29.567 |
| `prediction_confidence` | 37.313 |
| `blast_radius_confidence` | 0.0 |
| `rollback_confidence` | 100.0 |

Estimated after blast-radius materialization only:

| Metric | Before | Estimated After |
| --- | ---: | ---: |
| `blast_radius_confidence` | 0.0 | 100.0 |
| `trust` | 39.597 | 54.698 |
| `confidence` | 39.597 | 39.597 |
| `prediction_confidence` | 39.6 | 39.6 |
| `autonomy_readiness` | NOT_READY | NOT_READY |

The trust floor would still not pass. Estimated trust rises materially, but remains below the `70` floor.

## 9. Readiness Recalculation

Autonomy remains blocked after blast-radius recovery alone.

Remaining blockers:

- `confidence_too_low`
- `trust_too_low`
- `prediction_confidence_too_low`
- operator comparison evidence still absent for current decisions
- suitability remains the lowest confidence component after blast-radius recovery
- production consumed snapshot has not yet been refreshed to expose blast-radius recovery

## 10. Feasibility Verdict

| Question | Answer |
| --- | --- |
| Did blast-radius evidence disappear because the model is wrong? | No. Existing model classifies historical evidence correctly. |
| Is historical BA/governed evidence reusable? | Yes. Existing builder produced 2 usable rows. |
| Does existing refresh/materialization tooling exist? | Yes. `v7-intelligence-snapshot-refresh` supports feedback inputs and snapshot refresh. |
| Is rematerialization safe in principle? | Yes, if limited to existing snapshot refresh, no apply, and verified after. |
| Is production currently consuming recovered blast-radius evidence? | No. Fresh API still reports `blast_radius_confidence=0.0`. |
| Is code change required? | Not proven. Existing code path can classify the evidence. |

## 11. Remaining Problems

1. Production snapshot has not been refreshed in this phase because this phase was discover/verify only.
2. Direct SSH read-only probe was unavailable in this environment, so live file contents were verified through production API and truth/convergence plus saved production evidence, not direct shell file reads.
3. Even if blast-radius becomes `100.0`, autonomy remains blocked by confidence/trust/prediction floors.
4. Operator comparison evidence remains missing and must not be faked.

## 12. Next Phase

Exact next safe phase:

`AUTONOMY.REMATERIALIZATION.2_PRODUCTION_SNAPSHOT_REFRESH_AND_RECHECK`

Allowed shape:

1. Run existing `v7-intelligence-snapshot-refresh` against production feedback stores.
2. Do not apply movements.
3. Do not enable daemon/autoswitch.
4. Re-read `trust-evolution-summaries`.
5. Re-read `/api/operator/autonomous-dry-run`.
6. Accept only if `blast_radius_confidence` becomes visible in the production consumed snapshot.
7. Continue evidence collection for confidence, trust, prediction, and real operator comparisons.

Final verdict: `AUTONOMY_REMATERIALIZATION_POSSIBLE_REQUIRES_REFRESH`
