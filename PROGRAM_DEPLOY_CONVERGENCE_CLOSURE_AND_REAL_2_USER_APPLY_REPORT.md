# PROGRAM DEPLOY CONVERGENCE CLOSURE AND REAL 2 USER APPLY REPORT

Date: 2026-06-06

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence folder: `deploy_convergence_closure_evidence/`

## Executive Verdict

The original blocker `mixed_runtime_critical_dirty_workspace` was closed.

Local, GitHub, and production were synchronized and deployed through the approved safe-deploy path. Production reached `FULLY_ALIGNED` and `READY_FOR_RUNTIME_ACTION`.

The real 2-user apply was not executed because the current live planner no longer selects the approved target `vless`. The current single blocker is:

`target_vless_currently_not_eligible_no_selected_moves`

No users were moved.

## DIRTY_WORKSPACE_CLASSIFICATION

The dirty workspace root cause was a mixed runtime-critical workspace:

| Package | Files | Closure |
|---|---|---|
| Source stability fix | `tools/v7-users-autoswitch`, `tests/unit/test_v7_users_autoswitch_policy.py`, source-stability report/evidence | committed as `6f4ef07 Fix autoswitch source stability lease` |
| Admin UI/performance package | `admin/v7-admin-api`, admin report | committed in separate admin commits before this run |
| Restore-barrier source-bundle lease fix | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `tests/unit/test_v7_users_autoswitch_policy.py` | committed as `1bd7579 Fix restore barrier source bundle lease` |

The workspace was clean before the new evidence folder was created for this program.

## WORKSPACE_CLOSURE_REPORT

Initial state for this run:

- branch: `Updatesystem`
- local HEAD: `77dd4c4ef61cb23b6bcce582657d3ea9edded6a0`
- workspace: clean
- source-stability fix present in code
- admin UI/performance package already committed

Additional proven blocker after first deploy:

- fresh restore barrier was written, but next planner rejected it with `restore_barrier_clearance_atomic_envelope_id_mismatch`;
- cause: restore-barrier validation did not yet understand `service_matrix`-only source drift, even though apply validation did.

Closure:

- added approved per-source hashes to operator packet/barrier metadata;
- added restore-barrier source-bundle lease validation in `tools/v7-users-autoswitch`;
- allowed only `service_matrix` drift;
- kept users registry, egress registry, selected move hash/count, generation, and barrier TTL fail-closed.

## GITHUB_SYNC_REPORT

GitHub sync passed.

| Step | Result |
|---|---|
| GitHub HEAD check | `77dd4c4...` matched local before first deploy |
| Push restore-barrier lease fix | `1bd7579` pushed to `origin/Updatesystem` |

## SAFE_DEPLOY_REPORT

Approved safe deploy was run twice through `tools/v7-safe-deploy`:

1. First deploy closed the original mixed workspace convergence blocker and deployed source-stability/admin changes.
2. Second deploy deployed `1bd7579 Fix restore barrier source bundle lease`.

No manual file copy path was used.

No user movement was performed by deploy.

## FINAL_CONVERGENCE_REPORT

After the first deploy:

- `tools/v7-truth-check --all --json`: PASS
- convergence status: `FULLY_ALIGNED`
- runtime truth status: `KNOWN`
- state truth status: `KNOWN`
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

After the second deploy:

- `tools/v7-truth-check --all --json`: PASS
- `tools/v7-convergence-status --json`: PASS

Evidence:

- `phase5_truth_check_all.json`
- `phase5_convergence_status.json`
- `phase5b_truth_check_all_after_barrier_lease.json`
- `phase5b_convergence_status_after_barrier_lease.json`

## FRESH_PLANNER_REPORT

Fresh planner after convergence:

- snapshot refresh: `REFRESH_SUCCESS`
- `snapshot_stop_required=false`
- `source_mismatch_families=[]`
- authority lifecycle: `CANARY_EXPANSION`
- allowed user budget: `2`
- authority bridge: active

Before the restore-barrier lease fix, fresh packet/barrier could be written but the next planner rejected it with atomic-envelope mismatch. That blocker was fixed and deployed as `1bd7579`.

## BRIDGE_STATE_REPORT

Bridge state after deploy:

| Field | Value |
|---|---|
| authority_lifecycle_state | `CANARY_EXPANSION` |
| current_allowed_user_budget | `2` |
| authority_bridge_active | `true` |
| gate decision | `allow_transitional_authority_bridge_budget` |

## COHORT_REPORT

Earlier planner snapshot before the final live condition change identified the intended cohort:

| User | From | To |
|---|---|---|
| `10.0.0.3` | `awg3` | `vless` |
| `10.0.0.6` | `awg3` | `vless` |

Fresh approval packet generated from that snapshot:

- selected_move_budget: `2`
- selected_move_count: `2`
- allowed_users: `10.0.0.3`, `10.0.0.6`
- allowed_targets: `vless`
- rollback targets: `awg3`

## APPROVAL_PACKET_REPORT

Approval packet was generated:

- packet id: `pkt_0284de595c2a2276fb47eff1`
- budget: `2`
- target: `vless`
- rollback manifest items: `2`

Evidence:

- `phase9_fresh_approval_packet.json`
- `phase9_packet_generation_local.json`

## RESTORE_BARRIER_REPORT

Fresh restore barrier write path was exercised through the canonical owner:

- tool: `v7-operator-execution-packet`
- owner: `admin_core/operator_execution.py`
- runtime action scope: restore-barrier clearance only
- user movement: false
- routing mutation: false
- autoswitch apply: false

The first fresh barrier was valid as a write operation, but the next planner exposed a restore-barrier source-bundle drift gap. That gap was fixed in `1bd7579`.

## FINAL_READINESS_REPORT

Final readiness after the second deploy did not reach `selected_moves=2`.

Current live planner result:

- candidate_moves_total: `0`
- selected_moves: `0`
- target users still on `awg3`
- target `vless` is currently not eligible

Current target user assignments:

```text
ip=10.0.0.3 current=awg3 table=101 enabled=1
ip=10.0.0.6 current=awg3 table=104 enabled=1
```

For both target users, planner action is `keep`, reason:

```text
no_eligible_failover_target
```

For target `vless`, the blocking reason is:

```text
service_multiple_critical_failed
```

Observed failing service signals for `vless` included:

- `instagram`: FAIL / timeout
- `google_auth`: FAIL / timeout

Because planner selected zero moves, real apply was correctly not executed.

## REAL_APPLY_REPORT

Real apply was not executed.

Reason:

`target_vless_currently_not_eligible_no_selected_moves`

This is the correct safety behavior. Moving the users anyway would bypass planner selection and governance.

## VERIFICATION_REPORT

Verification of user movement was not applicable because users_moved=`0`.

Verified instead:

- local/GitHub/production convergence: PASS before live execution attempt
- target users remain on `awg3`
- no unapproved movement occurred
- no rollback required

## OUTCOME_REPORT

No movement outcome was materialized because no movement occurred.

No trust/prediction/recommendation feedback was updated for a movement outcome.

## SMALL_BATCH_CERTIFICATION

SMALL_BATCH was not certified.

Reason:

The required condition `users_moved=2` was not met.

## Tests

| Command | Result |
|---|---|
| `py_compile admin_core/operator_execution.py tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py` | PASS |
| `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` | PASS, 43 tests |
| `python3 -m unittest discover tests` | PASS, 334 tests |

Evidence:

- `phase_fix2_py_compile.txt`
- `phase_fix2_targeted_tests.txt`
- `phase_fix2_full_tests.txt`

## Final Verdicts

| Verdict | Value |
|---|---|
| workspace_clean | false, only this report/evidence are uncommitted after execution |
| github_synced | true |
| safe_deploy_pass | true |
| fully_aligned | true before final evidence/report dirtiness |
| bridge_active | true |
| users_selected | 0 current live planner |
| users_moved | 0 |
| verification_passed | false |
| outcomes_materialized | false |
| trust_feedback_updated | false |
| prediction_feedback_updated | false |
| recommendation_feedback_updated | false |
| small_batch_certified | false |
| current_certified_authority | CANARY |
| current_runtime_authority | CANARY |
| current_allowed_user_budget | 2 |
| SAFE_NEXT_STEP | wait for or restore planner eligibility for target vless, rerun fresh planner; proceed to packet/barrier/apply only when selected_moves=2 for 10.0.0.3 and 10.0.0.6 |

## Conclusion

The deploy/convergence blocker was closed.

The system is now blocked by live service suitability, not by deployment, source stability, bridge, packet generation, or restore-barrier ownership.

The next safe action is not to force movement. The next safe action is to re-run service checks / planner readiness when `vless` is again eligible, or let the planner choose a currently eligible target through the governed path.
