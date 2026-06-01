# Block B Certification

Project: V7 Vozduh

Block: B - Small Batch Program

## Certification Question

Can V7 safely move a small batch?

## Answer

`READY_WITH_BLOCKERS`

## Certification Basis

Block B successfully moved exactly two approved users to the execution target and observed them through delayed final verification.

Passed:

- Exactly two users moved
- No third user moved
- No autoswitch apply
- No rebalance
- No policy apply
- No deploy
- No systemd changes
- Runtime checkers OK
- Rollback readiness verified
- Replay protection verified
- Fail-closed behavior verified

Remaining blocker:

- Admin API health at `127.0.0.1:8017` was unavailable during the audit and observation window.

## Verdicts

- `small_batch_certified=true`
- `safe_to_continue_to_block_c=true`

Block C should include an explicit admin health remediation or acceptance decision before expanding beyond the two-user proof.

