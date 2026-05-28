# BLOCK E11.14 Delayed Apply-Restore Movement Root-Cause and Apply Timer Governance Fix Report

block=E11.14
mode=LARGE_MULTI_THEORY_ROOT_CAUSE_AND_GOVERNANCE_FIX
canary_performed=false

## Executive Verdict

E11.13 mini-cohort movement and rollback were clean, but apply timer restore exposed a governance gap: restore-settle GO only proved the sampled window, not future apply-timer generations. At 2026-05-27T13:18:24+03:00 a fresh apply-timer run recomputed target `1` as service-signal ineligible due to `telegram_required_telegram_down_14s`, selected three non-cohort failovers, and moved 10.7.0.9, 10.7.0.10, and 10.7.0.13 from `1` to `awg0`.

This was not stale selected_moves and not a hidden mover. It was timer-driven fresh apply logic operating without a post-restore service-signal barrier.

## Root Cause

root_cause_classification=H_MIXED
primary_root_cause=GOVERNANCE_GAP
secondary_root_cause=DELAYED_RECOMPUTE_SERVICE_SIGNAL
confidence=HIGH

Evidence:

- Restore-settle before apply restore: `gate_status=GO`, `selected_moves_by_sample=[0,0,0]`.
- Apply runs at 13:16:38, 13:17:00, 13:17:23, 13:17:43, and 13:18:04 had `selected_moves=0`.
- Apply run at 13:18:24 had `candidate_moves_total=5`, `selected_moves=3`, `applied=true`.
- Selected moves: 10.7.0.9, 10.7.0.10, 10.7.0.13 from `1` to `awg0`.
- Move reason: `current_egress_not_eligible`; selected move detail shows target `1` blocked by `telegram_required_telegram_down_14s`.
- WireGuard reservation held: WireGuard stayed blocked by `canary_reserved_production_assignment_blocked`.

## Fix

fix_path_selected=RESTORE_BARRIER_FAILOVER_QUARANTINE
runtime_fix_executed=true
rollback_performed=false

Bounded runtime fix:

- Deployed updated `/usr/local/bin/v7-users-autoswitch`.
- Backup: `/usr/local/bin/v7-users-autoswitch.e11_14_backup_20260527T105151Z`.
- Installed SHA: `10e87444c6f522bdeca0a3d21f02e8819e6d4f5797653546deeb89f92bed0e60`.
- Added restore barrier support through `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
- Active barrier TTL: `2026-05-28T10:52:27.369480+00:00`.
- Extended service-signal-only classification to include `telegram_required_*`.
- v2 correction suppresses all failover selection while restore barrier is active.
- Reason: final dry-run after v1 showed non-service failover pressure (`awg0` stability below floor), so service-signal-only suppression was insufficient for post-restore lifecycle containment.

No user movement was performed by E11.14. No routing mutation was performed by E11.14. Apply timer remains held.

## Regression Verdict

delayed_non_cohort_movement_prevented=true
restore_settle_gate_status=GO_BUT_INSUFFICIENT_WITHOUT_RESTORE_BARRIER
runtime_checks_ok=true
regressions_observed=false

Post-fix samples A/B/C:

- `users.registry` hash stable: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`.
- `selected_moves=0` in all samples.
- `v7-users-autoswitch.timer=inactive` in all samples.
- Restore barrier active in all dry-run plans.
- Runtime checkers OK.
- No hidden `v7-user-switch`, `v7-routing-sync`, or active apply service observed.

## Tests

mandatory_tests_completed=true

- `tools/v7-run-tests`: PASS
- targeted autoswitch policy / diagnose / restore-settle / target-readiness tests: PASS
- delayed movement regression test: PASS
- `tools/v7-control-plane-governance-check --pretty`: PASS
- `tools/v7-second-canary-target-readiness --pretty`: PASS
- `tools/v7-second-canary-target-readiness --json`: PASS
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS
- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`: PASS with known lineage warnings only
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`: PASS with known lineage/dirty-worktree warnings only
- `py_compile` for Python governance/autoswitch tools: PASS
- `bash -n` for relevant shell tools: PASS
- `git diff --check`: PASS

## Readiness

mini_cohort_readiness_after=NO-GO
larger_cohort_readiness=NO-GO
lifecycle_promotion_status=BLOCKED_PENDING_APPLY_RESTORE_GOVERNANCE_REHEARSAL
recommended_next_block=E11.15_APPLY_RESTORE_BARRIER_REHEARSAL_AND_GENERATION_GOVERNANCE
execution_allowed_now=false

The two-user cohort is operationally informative but not promotion-clean until apply-restore can be rehearsed with the restore barrier or a stronger generation-token model. Larger cohort is not justified.

## Final Answers

root_cause_classification=H_MIXED_GOVERNANCE_GAP_DELAYED_RECOMPUTE_SERVICE_SIGNAL
fix_path_selected=RESTORE_BARRIER_FAILOVER_QUARANTINE
runtime_fix_executed=true
rollback_performed=false
delayed_non_cohort_movement_prevented=true
restore_settle_gate_status=GO_BUT_INSUFFICIENT_WITHOUT_RESTORE_BARRIER
runtime_checks_ok=true
regressions_observed=false
mini_cohort_readiness_after=NO-GO
larger_cohort_readiness=NO-GO
lifecycle_promotion_status=BLOCKED_PENDING_APPLY_RESTORE_GOVERNANCE_REHEARSAL
recommended_next_block=E11.15_APPLY_RESTORE_BARRIER_REHEARSAL_AND_GENERATION_GOVERNANCE
execution_allowed_now=false

## Final Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: deployed bounded `v7-users-autoswitch` restore-barrier failover quarantine fix; wrote `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
