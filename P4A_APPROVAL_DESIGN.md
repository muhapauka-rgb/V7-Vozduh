# P4.A Approval Design

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Who Approves

Required approvals:

- `approval_author`
- `approval_reviewer`

The two approvals must come from different operator identities.

## Approval Meaning

Approval means the operators authorize a future block to attempt a zero-movement governance state transition if and only if the immediate runtime recheck still passes.

Approval does not execute.

## Expiry

Recommended TTL: 900 seconds.

Expired approval aborts and requires a fresh packet.

## Invalidation Conditions

Approval is invalidated by:

- registry hash mismatch
- runtime snapshot hash mismatch
- selected moves hash mismatch
- dry-run verification stale/mismatch/inconclusive
- service health degradation
- trust degradation
- candidate/action packet scope change
- rollback preview unavailable
- observation unavailable
- any operator identity conflict

## Re-Approval

Any invalidation requires a new action packet and new dual approval.

## Verdict

`approval_defined=true`

