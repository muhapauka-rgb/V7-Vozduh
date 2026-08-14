# BLOCK E11.15 Apply Restore Barrier Rehearsal and Generation Governance Report

block=E11.15
mode=LARGE_BOUNDED_RESTORE_BARRIER_REHEARSAL_AND_GOVERNANCE_VALIDATION
canary_performed=false
cohort_execution_performed=false

## Executive Verdict

E11.15 executed the bounded apply-timer restore rehearsal under the active
E11.14 restore barrier. The rehearsal was clean inside the approved observation
window: the timer was restored, at least one timer-triggered apply generation
ran, the barrier was active and consumed by apply logic, selected moves stayed
zero, users.registry stayed stable, switch-history stayed stable, WireGuard
stayed empty, and runtime checkers remained OK.

The apply timer was returned to hold at the end of the rehearsal because the
barrier TTL expiry is outside the bounded E11.15 window. Therefore E11.15 is
not a full unattended apply-timer promotion. It is a conditional pass for the
restore-barrier rehearsal and a blocker for larger cohort promotion until
post-TTL behavior or a generation-token model is governed.

## Rehearsal Facts

barrier_rehearsal_executed=true
apply_timer_restored=true
apply_timer_final_state=held
user_movement_observed=false
delayed_non_cohort_movement_prevented=true
barrier_consumed_by_apply=true
selected_moves_during_rehearsal=0
barrier_ttl_status=ACTIVE_NOT_EXPIRED_NOT_OBSERVED_POST_TTL
runtime_checks_ok=true
regressions_observed=false

Evidence:

- Pre-rehearsal: apply timer held, planner active, barrier active,
  selected_moves=0, checkers OK.
- Dry-run: `barrier_detected=true`, `failover_selection_suppressed=true`,
  `selected_moves=[]`.
- Apply restore: `systemctl start v7-users-autoswitch.timer`.
- Timer apply run: `apply_requested=true`, `restore_barrier.active=true`,
  `selected_moves=0`, `apply_result.reason=no_selected_moves`.
- Observations A-E: registry hash
  `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`,
  switch-history count `2698`, WireGuard users `0`, selected moves `0`.
- Final re-hold: `v7-users-autoswitch.timer=inactive`,
  `v7-users-autoswitch.service=inactive`.

## Classification

readiness_classification=APPLY_RESTORE_BARRIER_CONDITIONAL

The barrier prevents the E11.14 failure mode during the bounded rehearsal. The
remaining gap is not the observed timer-window behavior; it is unobserved TTL
expiry and lack of explicit restore generation ownership.

## Readiness

mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
execution_allowed_now=false

Mini-cohort promotion can only be considered conditional and must include an
explicit apply-timer hold/rehearsal/rehhold lifecycle. Larger cohort execution is
not justified.

## Recommended Next Block

recommended_next_block=E11.16_POST_TTL_BARRIER_EXPIRY_AND_GENERATION_TOKEN_GOVERNANCE

E11.16 should either validate post-TTL behavior in a bounded window or implement
a generation-token model so apply can reject stale or unrelated post-restore
generations.

## Final Answers

barrier_rehearsal_executed=true
apply_timer_restored=true
apply_timer_final_state=held
user_movement_observed=false
delayed_non_cohort_movement_prevented=true
barrier_consumed_by_apply=true
selected_moves_during_rehearsal=0
barrier_ttl_status=ACTIVE_NOT_EXPIRED_NOT_OBSERVED_POST_TTL
runtime_checks_ok=true
regressions_observed=false
mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
recommended_next_block=E11.16_POST_TTL_BARRIER_EXPIRY_AND_GENERATION_TOKEN_GOVERNANCE
execution_allowed_now=false

## Test Summary

mandatory_tests_completed=true

- `tools/v7-run-tests`: PASS, 89 tests.
- targeted reservation enforcement / diagnose / autoswitch policy /
  restore-barrier / restore-settle / target-readiness tests: PASS, 40 tests.
- `tools/v7-control-plane-governance-check --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --pretty`: PASS, GO target
  readiness for `wireguard-1779454504-c43409`.
- `tools/v7-second-canary-target-readiness --json`: PASS.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS, GO.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS, GO.
- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`:
  PASS with known partial-governance warnings.
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`:
  PASS with known lineage/dirty-worktree warnings.
- Python `py_compile` for Python governance/autoswitch tools: PASS.
- `bash -n` for relevant shell scripts: PASS.
- `git diff --check`: PASS.

Detailed summary:
`docs/track7/control-plane/e11_15-evidence/tests/mandatory-test-summary.md`.

## Final Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: bounded apply timer restore/re-hold rehearsal only:
`systemctl start v7-users-autoswitch.timer`, then
`systemctl stop v7-users-autoswitch.timer v7-users-autoswitch.service`.
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
