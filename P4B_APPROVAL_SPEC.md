# P4.B Approval Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Approval Text

Author:

`I approve P4B zero-move governance action design for final runtime recheck only. I understand this approval does not authorize user movement, routing changes, autoswitch apply, rollback execution, deploy, systemd changes, or runtime hooks.`

Reviewer:

`I independently approve P4B zero-move governance action design for final runtime recheck only. I confirm the action scope is zero users, zero routes, zero autoswitch apply, zero rollback execution, zero deploy, and zero systemd change.`

## Approval Scope

Approval covers only:

- one packet id
- one approval id
- one action id
- `ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`
- zero selected moves
- exact runtime hashes
- exact expiry window

## Approval TTL

Approval TTL: 900 seconds.

## Invalidation

Approval is invalid if:

- expired
- same operator signs both roles
- roles missing
- packet scope changes
- runtime hashes change
- selected moves hash changes
- dry-run verification becomes stale or mismatched
- rollback preview becomes unavailable
- observation target unavailable

## Renewal

Renewal requires a new packet id, approval id, hashes and dual approvals.

## Rejection

Any operator may reject before action. Rejection requires a reason and leaves no action authority.

## Verdict

`approval_spec_complete=true`

