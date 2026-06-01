# PROGRAM Z3.2 Repeatability Test

## Objective

Verify multiple bounded autonomy cycles:

1. proposal
2. recheck
3. execution
4. rollback
5. observation

## Live Result

The first cycle succeeded:

- execution: `10.7.0.16 vless -> awg3`
- rollback: `10.7.0.16 awg3 -> vless`
- final state restored

The immediate repeat cycle did not proceed:

- command: filtered dry-run for the same user and target
- collected_at: `2026-06-01T17:59:25.696786+00:00`
- candidate_moves: `0`
- selected_moves: `0`
- guard: `restore_barrier_clearance_generation_mismatch`
- generation_ok: `false`
- decision: keep `vless`
- reason: `cooldown_active_877s`
- reason: `no_eligible_failover_target`

## Interpretation

This is good fail-closed behavior, but it does not satisfy the prompt's requirement for multiple immediate bounded autonomy cycles. The live runtime correctly prevented a stale or repeated apply after rollback.

## Verdict

- first_cycle_successful=true
- immediate_repeat_blocked=true
- repeat_block_reason=cooldown_and_generation_mismatch
- repeatability_certified=false
- fail_closed_on_repeat=true

