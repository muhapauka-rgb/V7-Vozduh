# SNAP.1 Service Matrix Snapshot Reliability Report

Project: V7 Vozduh  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: read-only first, bounded safe fix applied locally  
Generated: 2026-06-11

## 1. Executive Summary

Final verdict: **ROOT_CAUSE_FOUND_BUT_NOT_FIXED**

Important nuance: the root cause is fixed in the local workspace and fully tested, but it is not production-fixed yet because the changed admin runtime file is not deployed. Production must not be considered clean until commit, push, approved safe deploy, admin restart if changed, and fresh truth/convergence checks pass.

Root cause:

The production admin read-only planner endpoint used the stale snapshot path:

`v7-users-autoswitch --pretty`

That path does not run the existing canonical pre-planner refresh. If `service-matrix.json` changes after the last snapshot write, the planner compares live service matrix truth against old `service-scores` and `channel-service-scores` source hashes and fails closed:

- `source_hash_mismatch:service-scores:service_matrix`
- `source_hash_mismatch:channel-service-scores:service_matrix`
- terminal reason: `dry_run_intelligence_snapshot_stop_required`
- selected moves: `0`

The codebase already had the correct owner and fix path:

`v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --pretty`

This is already used by the systemd planner service and by the admin planner refresh dry-run action. SNAP.1 extends the same existing path to the normal admin read-only plan endpoints.

No users were moved. No autoswitch apply was run. No routing, packet or restore-barrier mutation was performed.

## 2. Snapshot Architecture Map

| Stage | Owner | Inputs | Outputs | Authority |
| --- | --- | --- | --- | --- |
| Service matrix source | service probe / service matrix writers | `/opt/v7/egress/state/service-matrix.json` | live service truth | canonical source truth |
| Service scores worker | `admin_core/intelligence_workers.py` | service matrix, quality summary, preferences | `service-scores.json` | snapshot producer |
| Channel service scores worker | `admin_core/intelligence_workers.py` | same source bundle | `channel-service-scores.json` | snapshot producer |
| Snapshot refresh CLI | `tools/v7-intelligence-snapshot-refresh` | runtime state, events, audit, registries | intelligence snapshot root | snapshot write owner |
| Planner reader | `tools/v7-users-autoswitch` | snapshots and live source files | gate result, candidate advice | runtime planner owner |
| Snapshot gate | `tools/v7-users-autoswitch` | embedded snapshot source hashes vs live source hashes | ALLOW/STOP | selected move suppression authority |
| Admin read-only plan | `admin/v7-admin-api` | command wrapper | `/api/autoswitch-plan`, dry-run output | operator surface, no apply |

## 3. Source Hash Forensics

Baseline production evidence:

- `service-scores` validation: false
- `channel-service-scores` validation: false
- source mismatch family: `service_matrix`
- runtime behavior: `STOP`
- snapshot freshness: `FRESH`

This means the snapshots were not stale by TTL. They were stale by source lineage: their embedded `service_matrix` hash did not match the current planner-read service matrix hash.

Prior source consistency evidence already proved the valid fix pattern:

- after pre-planner refresh succeeds, planner reloads source inputs;
- if sources changed during refresh, planner retries refresh;
- if sources remain unstable after retry, planner fails closed.

Current SNAP.1 evidence shows the admin plan endpoint did not use that fix pattern. It invoked only:

`v7-users-autoswitch --pretty`

Therefore the first point of divergence is the admin read-only planner command path, not the snapshot worker hash algorithm.

Evidence:

- `docs/reports/evidence/PR1_EVIDENCE/snapshot_reliability_ctr_final_sample.json`
- `docs/reports/evidence/SNAP1_EVIDENCE/baseline_existing_production_snapshot_gate.json`
- `docs/reports/evidence/source1_consistency_evidence/hash_mismatch_root_cause_report.md`
- `docs/reports/evidence/SNAP1_EVIDENCE/fix_diff.patch`

## 4. Refresh Order Audit

Existing correct order:

1. acquire service matrix lock when pre-planner refresh is enabled;
2. run `v7-intelligence-snapshot-refresh`;
3. refresh tool builds snapshots;
4. refresh tool rereads sources and retries if sources changed during build;
5. planner reloads service matrix / quality summary / preferences after successful refresh;
6. planner retries refresh if reload observed changes;
7. planner loads intelligence snapshots;
8. snapshot gate compares snapshot hashes to current source inputs.

Incorrect admin read-only order before SNAP.1:

1. admin API called `v7-users-autoswitch --pretty`;
2. pre-planner refresh remained `off`;
3. planner loaded existing snapshots;
4. planner compared existing snapshot hashes to current service matrix;
5. mismatch caused STOP.

Fix:

`autoswitch_plan_state()` and `autoswitch_dry_run_state()` now use the same existing pre-planner refresh command as the canonical planner refresh path.

Changed files:

- `admin/v7-admin-api`
- `tests/unit/test_api3_read_only_views.py`

## 5. Planner Consumption Audit

Planner source consumption:

- `tools/v7-users-autoswitch` reads `service-matrix.json` into `self.matrix`.
- Runtime-required snapshots include `service-scores` and `channel-service-scores`.
- `_intelligence_snapshot_source_mismatches()` compares each snapshot's embedded source hashes against current planner inputs.
- If a runtime-required family mismatches, the gate sets STOP and selected moves are suppressed.

Admin surface before fix:

- `/api/autoswitch-plan` returned plan data from a no-refresh planner run.
- `/api/actions/autoswitch-dry-run` also used the no-refresh planner run.
- `/api/actions/planner-refresh-dry-run` already used the correct refresh path.

Admin surface after local fix:

- `/api/autoswitch-plan` uses pre-planner refresh write.
- `/api/actions/autoswitch-dry-run` uses pre-planner refresh write.
- `/api/actions/autoswitch-apply-guarded` is unchanged.

## 6. Counterfactual Analysis

If mismatch disappears:

- snapshot gate can become clean;
- `source_mismatch_families` can become empty;
- selected moves are no longer blocked by snapshot stop;
- planner certification can continue;
- CTR value can be reassessed only after selected moves are no longer suppressed.

If no fix is applied:

- admin planner view can keep reporting `dry_run_intelligence_snapshot_stop_required`;
- selected moves remain zero in broad admin dry-runs;
- operator may see stale blocking state even though canonical pre-planner refresh can close it;
- CTR/planner certification remains polluted by a stale snapshot read path.

Blast radius of fix:

- read-only admin plan surfaces now run existing snapshot refresh write;
- no apply path changed;
- no user movement path changed;
- no routing mutation changed;
- no packet or restore barrier path changed.

## 7. Root Cause

Root cause classification: **REFRESH_ORDER + STALE_SNAPSHOT**

More exact root cause:

`admin/v7-admin-api` had two read-only planner entrypoints that bypassed the existing pre-planner refresh owner and consumed existing snapshots directly.

Not root cause:

- not duplicate truth source;
- not duplicate snapshot root;
- not broken hash algorithm;
- not CTR;
- not planner winner logic;
- not a reason to weaken fail-closed behavior.

The STOP was real and correct for the no-refresh path. The process bug was that the operator-facing read-only plan endpoint did not first refresh snapshots through the canonical owner.

## 8. Fix Applied

Local code fix:

Added `autoswitch_read_only_plan_command()` in `admin/v7-admin-api`.

The helper builds:

`v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --pretty`

It is reused by:

- `autoswitch_plan_state()`
- `autoswitch_dry_run_state()`

Unchanged:

- `autoswitch_apply_guarded()`
- governance approval
- restore barrier
- routing mutation
- selected move writer
- runtime execution

Tests added:

- read-only plan command includes `--pre-planner-refresh write`;
- autoswitch plan state reuses the refresh command.

## 9. Retest Results

Local verification:

| Check | Result |
| --- | --- |
| `py_compile` | PASS |
| targeted tests | PASS, 52 tests |
| full test suite | PASS, 437 tests |
| `git diff --check` | PASS |

Evidence:

- `docs/reports/evidence/SNAP1_EVIDENCE/py_compile.txt`
- `docs/reports/evidence/SNAP1_EVIDENCE/targeted_tests.txt`
- `docs/reports/evidence/SNAP1_EVIDENCE/full_unittest.txt`
- `docs/reports/evidence/SNAP1_EVIDENCE/git_diff_check.txt`

Truth/convergence after local fix:

| Gate | Result | Reason |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | NO-GO | dirty workspace, runtime critical dirty, GitHub unreadable, runtime/local commit mismatch |
| `tools/v7-convergence-status --json` | NO-GO | admin API deploy delta not deployed |

Evidence:

- `docs/reports/evidence/SNAP1_EVIDENCE/truth_check_all_after_fix.json`
- `docs/reports/evidence/SNAP1_EVIDENCE/convergence_status_after_fix.json`
- `docs/reports/evidence/SNAP1_EVIDENCE/git_status_after_fix.txt`

Production retest was not completed because the fix is not deployed. Convergence correctly reports `admin/v7-admin-api` hash mismatch between local and production.

## 10. Certification

- snapshot_gate_clean: unknown_on_production
- root_cause_proven: true
- selected_moves_blocked_by_snapshot: true_on_current_production_sample
- planner_can_be_certified: false_until_deploy_and_recheck
- CTR_reassessment_needed: false_now

CTR reassessment should wait until:

1. SNAP.1 fix is committed;
2. code is pushed;
3. approved safe deploy updates admin API;
4. admin service is restarted if changed;
5. `/api/autoswitch-plan` or equivalent read-only planner sample shows `snapshot_stop_required=false`;
6. truth/convergence pass.

## 11. Final Verdict

Final verdict option: **ROOT_CAUSE_FOUND_BUT_NOT_FIXED**

Why not `ROOT_CAUSE_FIXED`:

The repository fix is implemented and tested, but production still runs the old admin API hash. The live blocker is not certified closed until deployment and production read-only recheck.

Final verdicts:

- root_cause_proven=true
- root_cause_classification=REFRESH_ORDER+STALE_SNAPSHOT
- local_fix_applied=true
- production_fix_deployed=false
- py_compile_pass=true
- targeted_tests_pass=true
- full_tests_pass=true
- truth_check_pass=false
- convergence_pass=false
- users_moved=0
- autoswitch_apply_run=false
- routing_changed=false
- packet_changed=false
- restore_barrier_changed=false
- planner_certification_can_continue=false
- SAFE_NEXT_STEP=commit CTR_VERIFY + PDR1 + PR1 + SNAP1 artifacts and SNAP1 code fix separately if desired, push Updatesystem, run approved safe deploy with admin restart if changed, then rerun truth/convergence and `/api/autoswitch-plan` production read-only sample
