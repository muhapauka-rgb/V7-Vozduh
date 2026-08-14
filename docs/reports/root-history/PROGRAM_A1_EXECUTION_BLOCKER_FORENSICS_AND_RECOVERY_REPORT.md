# PROGRAM A.1 - EXECUTION BLOCKER FORENSICS, RECOVERY AND PASS ATTEMPT REPORT

Date: 2026-06-02
Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Executive Verdict

Program A.1 completed as a fail-closed recovery attempt.

Safe runtime evidence refresh was performed. The canonical planner was rerun before and after refresh. The result did not change:

- `selected_moves=0`
- `healthy_egress_total=0`
- `candidate_moves=0`
- `execution_allowed_now=false`

Primary root cause: no production-eligible egress candidate exists under the current live health, quality, trust/reservation, service, and policy gates.

Restore barrier is expired and still blocks execution readiness, but it is not hiding a valid move. The planner reports `clearance_selected_moves_before_guard=0`, proving that no selected move exists behind the restore-barrier guard.

## Evidence

- `docs/reports/evidence/program_a1_evidence/phase1_remote_pipeline_refresh.txt`
- `docs/reports/evidence/program_a1_evidence/planner_before_after_summary.json`
- `docs/reports/evidence/program_a1_evidence/phase2_post_refresh_no_movement_check.txt`
- `docs/reports/evidence/program_a1_evidence/a1_remote_pipeline_refresh.sh`
- `docs/reports/evidence/program_a1_evidence/a1_post_refresh_no_movement_check.sh`

## Safety Statement

No direct user movement was executed.

No direct `v7-user-switch` was executed.

No route mutation, policy mutation, capacity override, planner override, service restart, systemd change, or manual execution bypass was performed.

Important note: `v7-telegram-sentinel` internally invoked the canonical autoswitch owner with `--apply --service telegram --route-class GLOBAL_STABLE`. That invocation produced `selected_move_count=0`, terminal state `NOOP`, and `terminal_reason=no_selected_moves`. It emitted a canonical runtime audit event, but no user movement occurred. Post-refresh evidence shows empty recent switch log and no hidden mover process.

## Fresh Runtime Read

Runtime host:

- `v3119922.hosted-by-vdsina.ru`

Runtime time:

- `2026-06-02T21:51:53+03:00`

Services:

- `v7-admin-api.service`: active
- `v7-users-autoswitch.service`: inactive
- `v7-users-autoswitch.timer`: inactive
- `v7-service-matrix-refresh.timer`: active
- `v7-telegram-sentinel.timer`: active
- `v7-egress-quality-compact.timer`: active

Runtime deploy lineage:

- deploy id: `deploy-z8-14-Updatesystem-ddc7d1c-20260602T154925`

`/opt/v7` is not a Git checkout, so branch/HEAD are not available via `git -C /opt/v7`. Runtime identity is therefore deployment-linkage based, not repository-worktree based.

## Duplication Audit

No running alternate mover was observed in the process scan.

Rejected or bypass-capable paths remain:

| Component | Classification | Program A.1 handling |
| --- | --- | --- |
| `v7-user-switch` | Low-level direct movement primitive | Reject direct use. Canonical owner may call it only if selected moves exist. |
| Admin user-switch endpoint | Alternate execution path | Reject for this program. |
| Admin rollback endpoint | Alternate rollback path | Reject without a fresh canonical rollback scope. |
| Runtime support rollback tools | Support/legacy material | Reject for A.1 recovery attempt. |
| `v7-telegram-sentinel` | Diagnostic refresh tool that can invoke canonical autoswitch `--apply` for Telegram service context | Reuse with caution; A.1 observed NOOP only, with `selected_move_count=0` and no user movement. |
| `tools/v7-users-autoswitch` | Canonical runtime owner | Reuse only. |
| Restore barrier state | Governance-owned execution clearance | Reuse; no bypass or override. |

## Full Pipeline Trace

Health:

- Fresh `v7-state-stale-check`: `V7_STALE_RESULT=OK`.
- `v7-state.json`, `summary.state`, and `egress-status.state` were fresh before refresh.

Service Matrix:

- Refreshed by `v7-service-matrix-refresh-all`.
- After refresh:
  - `1`: `FAIL 0/14`
  - `openvpn-1779388847-d2ad7c`: `FAIL 0/14`
  - `amneziawg-exec-20260528-10-8-1-14`: `WARN 13/14`
  - `awg0`: `WARN 13/14`
  - `awg3`: `WARN 13/14`
  - `vless`: `WARN 13/14`
  - `wireguard-1779454504-c43409`: `WARN 13/14`

Telegram:

- Refreshed by `v7-telegram-sentinel`.
- After refresh:
  - Telegram DOWN: `1`, `openvpn-1779388847-d2ad7c`
  - Telegram OK: `amneziawg-exec-20260528-10-8-1-14`, `awg0`, `awg3`, `vless`
  - WireGuard canary: degraded in detailed sample but not hard-blocked by planner; still blocked by reservation.

Quality:

- Refreshed by `v7-egress-quality-compact`.
- Planner still rejects available non-reserved candidates by quality/health/severity gates.

Capacity:

- `v7-egress-load` was refreshed.
- Capacity does not appear to be the primary blocker; planner candidate rows show load status OK for targets, but target `capacity_users=0` once eligibility gates fail.

Trust / Reservation:

- `wireguard-1779454504-c43409` is blocked by `canary_reserved_production_assignment_blocked`.
- `amneziawg-exec-20260528-10-8-1-14` is blocked by `manual_only`, `reserve_only`, and `canary_reserved_production_assignment_blocked`.

Policy / Group:

- No group isolation conflict was observed.
- Planner explanations report `group default allowed`.

Eligibility:

- All potential candidates are ineligible.

Planner:

- Before refresh: `selected_moves=0`, `healthy_egress_total=0`, `candidate_moves=0`.
- After refresh: `selected_moves=0`, `healthy_egress_total=0`, `candidate_moves=0`.

Selected Moves:

- Before refresh selected move hash: empty selected-move hash `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
- After refresh selected move hash: same empty selected-move hash.

Restore Barrier:

- Enabled: `true`
- Clearance expired at `2026-06-01T18:02:59.305408+00:00`
- Approved generation id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- Current generation id after refresh: `2f23e3acb00b8fe29837449096d8b4d5bc9eee6e3bc80058b7037be76c6adee8`
- Approved selected move hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- Current selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- `clearance_selected_moves_before_guard=0`
- `clearance_generation_reason=restore_barrier_clearance_generation_expired`

Runtime Recheck:

- Post-refresh planner still returns dry-run terminal reason `dry_run_restore_barrier_clearance_generation_expired`.
- No selected move was produced before the barrier guard.

Execution Gate:

- Restore-settle gate after refresh: `CONDITIONAL`
- `execution_allowed_now=false`
- Reasons:
  - `sample_count_below_required:1<3`
  - `apply_timer_intervals_below_required:0.00<2`

## Candidate-by-Candidate Eligibility

The following candidate evidence is from the after-refresh planner summary. Each candidate appeared across 18 user decisions and was never eligible.

| Candidate | Eligible | Exact blockers |
| --- | --- | --- |
| `1` | false | `avg_mbps_below_floor`, `health_code_000`, `min_mbps_below_floor`, `route_class_VIDEO_OPTIMIZED_failed`, `service_multiple_critical_failed`, `severity_FAIL`, `telegram_required_telegram_down_14s` |
| `amneziawg-exec-20260528-10-8-1-14` | false | `avg_mbps_below_floor`, `canary_reserved_production_assignment_blocked`, `manual_only`, `min_mbps_below_floor`, `reserve_only`, `stability_below_floor` |
| `awg0` | false | `avg_mbps_below_floor`, `min_mbps_below_floor` |
| `awg3` | false | `avg_mbps_below_floor`, `min_mbps_below_floor`, `stability_below_floor` |
| `openvpn-1779388847-d2ad7c` | false | `avg_mbps_below_floor`, `health_code_000`, `min_mbps_below_floor`, `route_class_VIDEO_OPTIMIZED_failed`, `service_multiple_critical_failed`, `severity_FAIL`, `telegram_required_telegram_down_14s` |
| `vless` | false | `severity_SUSPECT` |
| `wireguard-1779454504-c43409` | false | `canary_reserved_production_assignment_blocked` |

## Theory Matrix

| Theory | Result | Evidence-backed decision |
| --- | --- | --- |
| 1. No healthy candidates actually exist | CONFIRMED | Planner after refresh: `healthy_egress_total=0`, all candidates ineligible. |
| 2. Healthy egress calculation is wrong | NOT PROVEN | Service matrix/telegram refresh improved some service signals, but quality/severity/reservation gates still block all candidates. |
| 3. Service Matrix blocks candidates | PARTIAL | `1` and `openvpn` are service/Telegram hard blocked; others pass or warn service checks but fail other gates. |
| 4. Capacity blocks candidates | NOT PRIMARY | No evidence of hard capacity overload as primary blocker; eligibility gates fail first. |
| 5. Trust blocks candidates | CONFIRMED PARTIAL | Execution target and WireGuard canary are blocked by manual/reserve/canary reservation. |
| 6. Group constraints block candidates | FALSE | Planner reports `group default allowed`. |
| 7. Restore Barrier blocks otherwise valid moves | FALSE FOR SELECTED MOVES | `clearance_selected_moves_before_guard=0`; no move exists behind barrier. |
| 8. Planner generation drift exists | CONFIRMED SECONDARY | Approved generation differs from fresh generation. |
| 9. Runtime state is stale | REMEDIATED / NOT PRIMARY | Stale check was OK and safe refresh was performed; planner still selected zero moves. |
| 10. Scheduler inactivity causes stale evidence | FALSE AFTER REFRESH | Refresh timers were active; manual safe refresh also ran. Planner still selected zero. |
| 11. Candidate exists but is filtered late | FALSE | Candidate rows show exact early eligibility blockers for every candidate. |
| 12. Operation wiring affects planner path | NOT PROVEN | Operation/audit/closure objects are produced correctly; planner fails at eligibility. |
| 13. Governance packet mismatch | CONFIRMED SECONDARY | Restore clearance generation/hash do not match current generation/hash. |
| 14. Selected move hash mismatch | CONFIRMED SECONDARY | Approved hash expects prior one-move packet; current hash is empty selected-move hash. |
| 15. Restore clearance expiry only | FALSE | Expiry exists, but selected moves before guard are zero. |

Additional theory:

| Theory | Result | Evidence-backed decision |
| --- | --- | --- |
| 16. Diagnostic refresh can close the blocker | FALSE | Safe service/telegram/quality/load refresh completed; selected moves remained zero. |

## Root Cause Decision

Primary root cause:

`no_production_eligible_egress_candidate_under_current_runtime_health_quality_and_governance_constraints`

Secondary root causes:

- `restore_barrier_clearance_generation_expired`
- `restore_barrier_generation_and_selected_move_hash_mismatch`
- `restore_settle_window_insufficient`
- `reserved_or_manual_only_targets_are_not_available_for_production_assignment`

Why this is not merely restore barrier:

- The planner computes selected moves before the restore-barrier generation guard.
- After safe refresh, that pre-guard count is still `0`.
- Therefore removing or refreshing the barrier alone would not produce a valid movement candidate.

## Safe Remediation Performed

Performed:

- service matrix refresh
- Telegram sentinel refresh
- quality summary compaction
- egress load refresh
- stale-state recheck
- planner rerun
- restore-settle rerun
- post-refresh no-movement verification

Not performed:

- direct movement
- direct user-switch
- route mutation
- policy mutation
- capacity override
- planner override
- restore-barrier override
- service restart

## Pass Attempt Result

After remediation:

- `selected_moves_present=false`
- `execution_allowed_now=false`
- `safe_to_retry_PROGRAM_A=false`

No PASS was achieved.

## Single Remaining External Blocker

The remaining blocker is:

`no_production_eligible_egress_candidate_exists_under_current_runtime_health_quality_reservation_gates`

This cannot be fixed safely inside A.1 because making a candidate eligible would require at least one forbidden action:

- policy or planner override;
- canary/reservation override;
- manual/reserve-only target override;
- route or runtime repair beyond diagnostic state refresh;
- direct movement bypass.

## Final Verdicts

root_cause_found=true
all_theories_tested=true
healthy_candidates_exist=false
planner_candidate_exists=false
restore_barrier_blocking=true
planner_generation_valid=false
runtime_state_fresh=true
safe_remediation_performed=true
selected_moves_present=false
execution_allowed_now=false
safe_to_retry_PROGRAM_A=false

## Conclusion

Program A.1 proves that Program A failed for a real runtime eligibility reason, not just because of stale evidence or an expired barrier. Safe refresh did not produce a candidate. The system remains fail-closed, and Program A must not be retried until at least one production-eligible, non-reserved, policy-allowed candidate exists and a fresh governance clearance is generated for that exact selected move hash.
