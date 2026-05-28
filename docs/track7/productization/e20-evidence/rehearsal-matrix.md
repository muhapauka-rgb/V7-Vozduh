# E20 Full Rehearsal Matrix

## Rehearsal Verdicts

The rehearsal model exposes these verdicts:

- EXECUTION_ALLOWED
- STALE_RUNTIME
- GENERATION_MISMATCH
- REPLAY_REJECTED
- BLAST_RADIUS_CHANGED
- RESTORE_INVALID
- APPROVAL_EXPIRED

`EXECUTION_ALLOWED` means the governance recheck would pass in simulation. It
does not enable real runtime execution in E20.

## Matrix

| Scenario | Expected | Actual | Result |
|---|---:|---:|---|
| fresh_dual_confirmed_recheck | EXECUTION_ALLOWED | EXECUTION_ALLOWED | PASS |
| stale_approval | APPROVAL_EXPIRED | APPROVAL_EXPIRED | PASS |
| stale_runtime_truth | STALE_RUNTIME | STALE_RUNTIME | PASS |
| generation_mismatch | GENERATION_MISMATCH | GENERATION_MISMATCH | PASS |
| selected_move_fingerprint_mismatch | REPLAY_REJECTED | REPLAY_REJECTED | PASS |
| changed_blast_radius | BLAST_RADIUS_CHANGED | BLAST_RADIUS_CHANGED | PASS |
| restore_settle_invalidated | RESTORE_INVALID | RESTORE_INVALID | PASS |
| dual_confirmation_mismatch | REPLAY_REJECTED | REPLAY_REJECTED | PASS |
| execution_without_recheck | REPLAY_REJECTED | REPLAY_REJECTED | PASS |
| approval_replay_after_rollback | REPLAY_REJECTED | REPLAY_REJECTED | PASS |
| execution_after_containment | REPLAY_REJECTED | REPLAY_REJECTED | PASS |

## Operator UX Result

- allowed path is marked preview-only;
- denial paths show reason and immutable record hash;
- all production execution actions remain disabled.

## Verdict

full_rehearsal_matrix_complete=true
replay_rejection_complete=true
stale_execution_rejection_complete=true
execution_allowed_now=false
