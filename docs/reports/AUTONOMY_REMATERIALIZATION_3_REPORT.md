# AUTONOMY.REMATERIALIZATION.3 Production Feedback Store Forensics

Timestamp: 2026-06-22T04:53:28Z  
Branch: `Updatesystem`  
Commit at audit start: `acd0b7bfa52d75d1768a0eb45f1ea29a14cd9fc1`  
Mode: production feedback store forensics only

Final verdict: `BLAST_RADIUS_ROOT_CAUSE_FOUND`

## 1. Scope

This phase located the break between production feedback stores, the blast-radius builder, and the consumed trust-evolution snapshot.

No apply was executed. No users were moved. No daemon or autoswitch was enabled. No planner, governance, execution path, truth source, confidence model, trust model, prediction model, threshold, floor, or snapshot model was changed. No trust snapshot was manually edited and no synthetic evidence was created.

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

Known starting truth: existing code can classify saved governed evidence into blast-radius rows, and production snapshot refresh executes safely, but the default production refresh still produces `blast_radius_records=[]`.

## 3. Commands And Evidence

Discovery and verification:

- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`
- `sed -n ... docs/reference/V7_CANONICAL_REFERENCE.md`
- `sed -n ... docs/reference/SYSTEM_MAP.md`
- `sed -n ... docs/reference/V7_PROJECT_MAP.md`
- `sed -n ... docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `sed -n ... docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `sed -n ... docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `sed -n ... docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`
- `sed -n ... docs/reports/AUTONOMY_EVIDENCE_1_REPORT.md`
- `sed -n ... docs/reports/AUTONOMY_EVIDENCE_2_BLAST_AND_COMPARISON_REPORT.md`
- `sed -n ... docs/reports/AUTONOMY_REMATERIALIZATION_1_REPORT.md`
- `sed -n ... docs/reports/AUTONOMY_REMATERIALIZATION_2_REPORT.md`
- `rg -n "build_blast_radius_evidence_rows|blast_radius_confidence_model|execution-events|runtime-trust|closure-records|proposal-records|proposals|feedback"`
- Read-only production SSH forensic probes for store inventory, archive search, and existing-builder execution.
- `/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run --pretty ...` against rotated `.jsonl.1` inputs, with no snapshot writes.

Evidence paths:

- `docs/reports/AUTONOMY_REMATERIALIZATION_3_EVIDENCE/production_store_forensics.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_3_EVIDENCE/production_archive_search.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_3_EVIDENCE/production_rotated_store_builder.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_3_EVIDENCE/production_rotated_refresh_dry_run.json`
- `docs/reports/AUTONOMY_REMATERIALIZATION_3_EVIDENCE/analysis_summary.json`

## 4. Store Inventory

Default refresh inputs from `tools/v7-intelligence-snapshot-refresh`:

| Store | Path | Active Records | Newest | Refresh Participation |
| --- | --- | ---: | --- | --- |
| execution-events | `/opt/v7/egress/state/execution-events.jsonl` | 0 | - | yes |
| runtime-trust | `/opt/v7/egress/state/runtime-trust.jsonl` | 0 | - | yes |
| proposal-records | `/opt/v7/egress/state/proposal-records.jsonl` | 0 | - | yes |
| proposals | `/opt/v7/egress/state/proposals.jsonl` | 0 | - | yes |
| closure-records | `/opt/v7/egress/state/closure-records.jsonl` | 0 | - | yes |
| audit | `/opt/v7/audit/audit.jsonl` | 894 | 2026-06-22T04:46:24.258257+00:00 | yes |
| operator-execution-audit | `/opt/v7/audit/operator-execution-audit.jsonl` | 0 | - | yes |
| operator-runtime-governance-actions | `/opt/v7/audit/operator-runtime-governance-actions.jsonl` | 0 | - | yes |
| switch-history | `/opt/v7/events/switch-history.jsonl` | 2851 | 2026-06-13T19:16:49.231796+00:00 | yes |
| rollback-history | `/opt/v7/events/rollback-history.jsonl` | missing | - | yes |

The active default feedback stores contain no BA operation ids and no movement-radius fields. The combined active bounded input had 1000 records, but existing `build_blast_radius_evidence_rows` returned 0 rows.

## 5. Builder Trace

Owner:

- `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows`

Qualification logic:

1. Normalize the record with `normalize_outcome_evidence`.
2. Reject when normalized outcome is `unknown`.
3. Read movement radius from `blast_radius`, `affected_users`, `movement_count`, `users_moved`, `selected_move_count`, `target_users`, `users`, `moved_users`, `selected_moves`, or `moves`.
4. Group records by `audit_reference`, `operation_id`, nested `execution_outcome.operation_id`, or `packet_id`.
5. If grouped radius is missing but grouped user identities exist, infer radius from unique users.
6. Emit rows only when a nonzero radius exists.

Production active input result:

| Metric | Value |
| --- | ---: |
| bounded decisions | 1000 |
| blast rows | 0 |
| qualification tail `status_unknown` | 65 / 80 |
| qualification tail `radius_missing` | 80 / 80 |
| qualification tail `operation_id_missing_for_grouping` | 80 / 80 |
| trust snapshot `blast_radius_evidence_count` | 0 |

## 6. Production Vs Saved Evidence

Saved evidence from `small_batch_stability_evidence` still produces valid rows:

| Operation | Radius | Result | Rollback |
| --- | ---: | --- | --- |
| `runtime_autoswitch_e33f678dabd7ad432b38f2a7` | 1 | success | false |
| `runtime_autoswitch_b5063a475a06312ff23c90a7` | 2 | success | false |

Current production active stores:

- do not contain those rows in the current default feedback files;
- have 0 records in active `execution-events`, `runtime-trust`, and `closure-records`;
- have no `ba_operation_mentions` in current default stores.

Production rotated stores:

| Rotated Store | Records | Existing Builder Rows |
| --- | ---: | ---: |
| `/opt/v7/egress/state/execution-events.jsonl.1` | 148 | 10 |
| `/opt/v7/egress/state/runtime-trust.jsonl.1` | 74 | 5 |
| `/opt/v7/egress/state/closure-records.jsonl.1` | 74 | 5 |
| `/opt/v7/egress/state/proposal-records.jsonl.1` | 74 | 5 |
| `/opt/v7/egress/state/proposals.jsonl.1` | 2 | 1 |
| Combined rotated `.1` inputs | 372 | 11 |

The current builder classified rotated production records without code changes. Therefore the records are not rejected because of schema mismatch or builder logic.

## 7. Retention Analysis

The exact retention/rotation mechanism was observed as file placement:

- current default files are present but empty;
- historical governed evidence is present in rotated sibling files ending in `.jsonl.1`;
- standard production refresh does not include those rotated paths unless passed explicitly.

This is retention/path selection, not model failure. The certified root cause is still store/path placement because the rows exist in production but outside the default refresh input set.

## 8. Lineage Map

| Stage | Status | Evidence |
| --- | --- | --- |
| BA1 saved evidence | present in saved local evidence | `small_batch_stability_evidence`, `AUTONOMY_REMATERIALIZATION_1_EVIDENCE/local_blast_rematerialization.json` |
| BA3/BA4 production evidence | present in production rotated/review paths | `production_archive_search.json`, `production_rotated_store_builder.json` |
| Active execution-events | absent from active default store | 0 records |
| Active runtime-trust | absent from active default store | 0 records |
| Active closure-records | absent from active default store | 0 records |
| Blast Radius Builder on active inputs | filtered by missing radius/outcome/grouping | 0 rows |
| Blast Radius Builder on rotated inputs | present | 11 rows |
| Trust Evolution Snapshot | still empty blast evidence | `blast_radius_evidence_count=0` |
| Autonomous Dry Run | still blocked | no metric recovery from REMATERIALIZATION.2 |

## 9. Certified Root Cause

`BLAST_RECORDS_IN_DIFFERENT_STORE`

Exact reason:

The default production refresh reads active paths such as `/opt/v7/egress/state/execution-events.jsonl`, `/opt/v7/egress/state/runtime-trust.jsonl`, and `/opt/v7/egress/state/closure-records.jsonl`. Those active files are empty. Historical governed blast-radius evidence exists in production rotated `.jsonl.1` files and review JSON outside the default refresh input set. When the existing builder is pointed at rotated `.jsonl.1` files, it produces 11 valid blast-radius rows. Therefore production `blast_radius_records` disappear before the builder receives the right records in the standard refresh path.

Rejected causes:

| Cause | Result |
| --- | --- |
| `BLAST_RECORDS_FILTERED_BY_BUILDER` | rejected: builder accepts rotated records |
| `BLAST_RECORDS_SCHEMA_MISMATCH` | rejected: rotated production schemas classify |
| `BLAST_RECORDS_MISSING_FROM_PRODUCTION_STORE` | rejected as absolute statement: records exist in production, but not active default stores |
| `BLAST_RECORDS_OUTSIDE_RETENTION_WINDOW` | secondary mechanism only: rotation places evidence outside default input paths |

## 10. Recovery Path

Shortest safe path:

Use the existing snapshot rebuild/refresh capability with explicit existing feedback inputs that include rotated `.jsonl.1` files, or use an existing archive restore/materialization owner to repopulate active feedback stores before refresh.

Safe options:

| Option | Fit | Notes |
| --- | --- | --- |
| Existing refresh only | insufficient | default inputs stay empty |
| Existing execution-feedback-materialize owner | possible later | must not synthesize evidence; only if rebuilding from real execution contracts |
| Existing archive restore path | likely safe candidate | restore/copy real existing JSONL evidence into active owner paths only with explicit approval |
| Existing snapshot rebuild path | likely shortest | run refresh with explicit rotated feedback file inputs; no manual snapshot editing |
| Code change required | not required for proof | may be needed later so supported production refresh includes rotated/archive inputs automatically |

No recovery was executed in this phase.

## 11. Safety

| Check | Result |
| --- | --- |
| Runtime apply | not executed |
| Users moved | 0 |
| Daemon enabled | no |
| Autoswitch enabled | no |
| Synthetic evidence | no |
| Manual trust snapshot edit | no |
| Production write | no snapshot write; only read-only probes and dry-run |

## 12. Remaining Problems

1. Production consumed `trust-evolution-summaries` still has `blast_radius_evidence_count=0`.
2. Default refresh does not include rotated `.jsonl.1` stores.
3. Recovery has not yet been executed.
4. Even after blast-radius recovery, autonomy still remains blocked by confidence/trust/prediction floors and missing operator comparisons.

## 13. Next Phase

Exact next phase:

`AUTONOMY.REMATERIALIZATION.4_ROTATED_STORE_RECOVERY_DRY_RUN_AND_APPROVAL`

Allowed shape:

1. Read-only preview refresh with explicit rotated feedback inputs.
2. Confirm `trust-evolution-summaries` would include blast-radius rows.
3. Decide whether to use existing archive restore/materialization or snapshot rebuild owner.
4. Require explicit approval before any write to active stores or intelligence snapshots.
5. Still no user movement, daemon enablement, autoswitch apply, synthetic evidence, or manual trust editing.

Final verdict: `BLAST_RADIUS_ROOT_CAUSE_FOUND`
