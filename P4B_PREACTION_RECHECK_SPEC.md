# P4.B Pre-Action Recheck Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Exact Recheck Inputs

- packet `expires_at`
- packet approvals
- packet constraints
- users registry file
- egress registry file
- selected moves state
- computed runtime snapshot hash
- health status
- capacity status
- trust status
- candidate/action validity
- dry-run verification state
- rollback preview availability
- observation availability

## Exact Recheck Algorithm

1. Validate packet schema.
2. Validate `selected_first_action`.
3. Validate `runtime_action`.
4. Validate zero movement constraints.
5. Validate dual approvals.
6. Validate packet has not expired.
7. Compute users registry hash.
8. Compute egress registry hash.
9. Compute selected moves hash and count.
10. Compute runtime snapshot hash from users, egress and selected moves hashes.
11. Compare all expected hashes.
12. Confirm health/capacity/trust are not degraded from frozen evidence.
13. Confirm candidate/action validity.
14. Confirm dry-run verification is current and not mismatched.
15. Confirm rollback preview is available.
16. Confirm observation targets are available.

## Required Pass State

`RECHECK_PASS_ZERO_MOVE_GOVERNANCE`

## Any Mismatch

Any mismatch returns `ABORT`.

## Verdict

`preaction_recheck_complete=true`

