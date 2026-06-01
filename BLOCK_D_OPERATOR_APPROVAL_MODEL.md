# Block D Operator Approval Model

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Proposal

An autoswitch proposal must include:

- Proposal ID
- Planner generation ID
- Runtime input hashes
- Candidate users
- Current egress
- Recommended egress
- Movement budget
- Rollback manifest
- Checker requirements
- Observation window
- Expiry timestamp

## Approval

Approval must include:

- Two approval roles
- Exact allowed users
- Exact allowed targets
- TTL
- Replay protection
- Runtime recheck requirement
- Fail-closed denial on mismatch

## Invalidation

Proposal invalidates on:

- Expired TTL
- Users registry hash mismatch
- Egress registry hash mismatch
- Selected moves non-zero
- Safety review not OK
- Admin health unresolved when operator UI is required
- Route checker failure
- Scope mismatch

## Model Verdict

The approval model is certified as a design.

`operator_approval_model_certified=true`

