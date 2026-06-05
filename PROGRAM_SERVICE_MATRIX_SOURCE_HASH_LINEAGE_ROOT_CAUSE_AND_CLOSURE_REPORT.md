# PROGRAM SERVICE MATRIX SOURCE HASH LINEAGE ROOT CAUSE AND CLOSURE REPORT

Project: V7 Vozduh
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem
Date: 2026-06-06
Evidence folder: service_matrix_lineage_evidence/

## Executive Verdict

The `source_hash_mismatch:service_matrix` blocker is identified, proven, and closed for the governed planner path.

No new hash authority, truth source, snapshot root, planner, governance path, execution path, or authority model was created. Snapshot validation was not weakened. Fail-closed behavior remains intact.

The fix is to use the existing deployed `--pre-planner-refresh=write` path for runtime planning validation instead of doing an external snapshot refresh followed by a separate planner run while `service-matrix.json` is volatile.

## SERVICE_MATRIX_LINEAGE_MAP

| Stage | Owner | File / Function | Behavior |
| --- | --- | --- | --- |
| Source writer | service matrix refresh tooling | `/opt/v7/egress/state/service-matrix.json` | Live service signal source; can update independently |
| Snapshot refresh CLI | `tools/v7-intelligence-snapshot-refresh` | `load_inputs()` | Reads `service-matrix.json`, `egress-quality-summary.json`, `service-preferences.json` |
| Snapshot builder | `admin_core/intelligence_workers.py` | `build_service_score_snapshots()` | Computes `source_hashes(service_matrix=sha256_json(...))` |
| Snapshot writer | `admin_core/intelligence_workers.py` | `write_snapshots()` | Writes `service-scores.json` and `channel-service-scores.json` |
| Planner source reader | `tools/v7-users-autoswitch` | `self.matrix = read_json(service-matrix.json)` | Reads current planner source |
| Snapshot validator | `tools/v7-users-autoswitch` | `_intelligence_snapshot_source_mismatches()` | Compares snapshot `source_hashes.service_matrix` with `sha256_json(self.matrix)` |
| Race closure path | `tools/v7-users-autoswitch` | `--pre-planner-refresh=write` + `_reload_intelligence_sources_after_pre_planner_refresh()` | Refreshes snapshots inside planner run, reloads sources, then validates |

## HASH_GENERATION_TRACE

Production before closure:

| Value | Hash |
| --- | --- |
| Snapshot `service-scores.source_hashes.service_matrix` | `7cc6d45924e501989b00219e5f3ed313e0944c3d0e4823b3d7486e7f6b372412` |
| Snapshot `channel-service-scores.source_hashes.service_matrix` | `7cc6d45924e501989b00219e5f3ed313e0944c3d0e4823b3d7486e7f6b372412` |
| Validator current `sha256_json(service-matrix.json)` | `e6f1714c905d17acff1c80cbac7691092f78f56b139ea39b642a6e38dba3564a` |
| Raw file `sha256sum(service-matrix.json)` | `e504a6d00433a0cf899697ad4d189e76dc83fb6d220251f9f122aa5175b7236a` |

The raw file hash is intentionally not the validator contract. The contract is canonical JSON hash via `sha256_json`.

Production timestamps:

| File | Timestamp |
| --- | --- |
| `service-scores.json` | 2026-06-06 00:47:16 MSK |
| `channel-service-scores.json` | 2026-06-06 00:47:16 MSK |
| `service-matrix.json` | 2026-06-06 00:47:19 MSK |

This proves the service matrix source changed after snapshots were written.

## HASH_DIFF_ANALYSIS

The mismatch is not caused by:

- field ordering
- JSON serialization differences
- raw file hash vs canonical JSON hash confusion
- missing `quality_summary`
- missing `service_preferences`
- weakened validation

The exact mismatch is temporal lineage drift:

```text
external snapshot refresh reads service_matrix at T1
snapshot writer stores HASH_A in service-scores/channel-service-scores
service-matrix.json updates at T2
separate planner run reads service_matrix at T3
validator computes HASH_B
HASH_A != HASH_B
snapshot gate stops
```

The standalone snapshot refresh can be internally source-stable and still become stale seconds later because `service-matrix.json` is an active live signal.

## ROOT_CAUSE_PROOF

Writer computed:

`HASH_A=7cc6d45924e501989b00219e5f3ed313e0944c3d0e4823b3d7486e7f6b372412`

Validator computed:

`HASH_B=e6f1714c905d17acff1c80cbac7691092f78f56b139ea39b642a6e38dba3564a`

Because:

- `service-scores.json` and `channel-service-scores.json` were generated at 00:47:16 MSK.
- `service-matrix.json` was modified at 00:47:19 MSK.
- The planner validator read the newer `service-matrix.json`.

Existing proof files:

- `production_hash_generation_trace_before_fix.json`
- `production_source_file_stat_before_fix.txt`
- `phase2_snapshot_root_cause.json` from the previous CANARY_EXPANSION attempt

## FIX_IMPLEMENTATION_REPORT

No code change was required.

The already deployed fix path is:

```text
/usr/local/bin/v7-users-autoswitch
  --pre-planner-refresh write
  --pre-planner-refresh-command /usr/local/bin/v7-intelligence-snapshot-refresh
```

This reuses:

- existing snapshot refresh owner
- existing snapshot root
- existing snapshot source hashes
- existing planner
- existing snapshot validation
- existing fail-closed behavior

It does not:

- run `--apply`
- move users
- create a new truth source
- weaken validation
- create a new planner
- bypass governance

The key closure behavior already exists in `tools/v7-users-autoswitch`:

- after `REFRESH_SUCCESS`
- reload `service_matrix`, `quality_summary`, and `service_preferences`
- then load and validate snapshots
- write evidence under `plan.safety.intelligence_snapshots.pre_planner_refresh.source_reload`

## LOCAL_HASH_RETEST

Existing local regression already covers this race:

`tests/unit/test_runtime_snapshot_fast_path.py::test_pre_planner_refresh_reloads_sources_before_gate_validation`

This test simulates the source changing during pre-planner refresh. The planner reloads source inputs and the gate passes with:

- `source_reload` present
- `service_matrix` in changed keys
- `stop_required=false`
- `source_mismatch_families=[]`

Local tests:

| Check | Result |
| --- | --- |
| py_compile | PASS |
| snapshot/planner/authority targeted tests | PASS, 54 tests |
| full unittest discover | PASS, 319 tests |

## PRODUCTION_DEPLOY_REPORT

No code change was needed for lineage closure, but production was safely redeployed to align runtime fingerprint with current `Updatesystem` after the previous report commit.

Safe deploy:

- tool: `tools/v7-safe-deploy`
- final_verdict: PASS
- deployed commit: `4215f243e23997e46fe45ed39f085b8e8c077bea`
- autoswitch_apply_executed=false
- routing_mutation_executed=false
- user_movement_executed=false

Final truth:

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |
| production commit | `4215f243e23997e46fe45ed39f085b8e8c077bea` |
| runtime truth | KNOWN |
| runtime access | READY |

## PRODUCTION_REFRESH_REPORT

Production validation command:

```text
/usr/local/bin/v7-users-autoswitch \
  --pre-planner-refresh write \
  --pre-planner-refresh-command /usr/local/bin/v7-intelligence-snapshot-refresh \
  --target-egress vless \
  --max-selected-moves 2 \
  --pretty
```

Refresh result inside planner:

| Field | Value |
| --- | --- |
| pre_planner_refresh_state | REFRESH_SUCCESS |
| pre_planner_refresh_decision | freshness_refreshed |
| pre_planner_refresh_snapshot_count | 11 |
| source_reload_present | true |
| source_reload_changed_keys | [] |
| users_moved | false |

## PRODUCTION_VALIDATION_REPORT

Final production snapshot gate:

| Field | Value |
| --- | --- |
| terminal_state | DRY_RUN |
| terminal_reason | dry_run_restore_barrier_clearance_generation_expired |
| snapshot_stop_required | false |
| source_mismatch_families | [] |
| stop_families | [] |
| service-scores validation_ok | true |
| channel-service-scores validation_ok | true |

Final service family validation:

| Family | freshness_state | validation_ok | validation_errors |
| --- | --- | --- | --- |
| service-scores | FRESH | true | [] |
| channel-service-scores | FRESH | true | [] |

The service matrix source hash lineage blocker is closed.

## CANARY_EXPANSION_READINESS

Snapshot blocker is closed, but CANARY_EXPANSION is not executable yet because later gates are still pending:

| Field | Value |
| --- | --- |
| candidate_moves_total | 9 |
| selected_moves | 0 |
| prepared_authority_class | SMALL_BATCH |
| certified_authority_class | CANARY |
| authority_lifecycle_state | PREPARED |
| current_allowed_user_budget | 1 |
| authority_bridge_active | false |
| authority_decision | cap_prepared_authority_to_certified_evidence |
| restore barrier | expired |

This is expected. This program was scoped to lineage closure only and did not change authority or governance state.

## Final Verdicts

root_cause_identified=true

root_cause_proven=true

fix_implemented=true

local_hash_match=true

production_deployed=true

snapshot_refresh_pass=true

snapshot_stop_required=false

source_mismatch_families=[]

validation_ok=true

canary_expansion_ready=false

new_truth_sources_created=false

duplicate_systems_created=false

SAFE_NEXT_STEP=ENTER_CANARY_EXPANSION_AUTHORITY_STATE_AND_REGENERATE_FRESH_RESTORE_BARRIER_CLEARANCE_THEN_RETRY_CANARY_EXPANSION_FROM_ELIGIBILITY_GATE_USING_PRE_PLANNER_REFRESH_WRITE

## Conclusion

The final blocker was not a broken hash algorithm. It was a volatile-source timing window.

External snapshot refresh plus a later planner run can lose the race against `service-matrix.json` updates. The existing governed pre-planner refresh path closes that race by refreshing snapshots and reloading planner inputs in one runtime cycle before validation.

The snapshot gate now passes in production:

```text
snapshot_stop_required=false
source_mismatch_families=[]
validation_ok=true
```

Do not retry live apply with external refresh plus separate dry-run. Retry CANARY_EXPANSION with the existing pre-planner refresh write path, after explicit authority bridge activation and fresh restore barrier clearance.
