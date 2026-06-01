# P4 Runtime Recheck Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Purpose

The runtime recheck is the last gate between an approved plan and any future execution block.

## Recheck Questions

- Did runtime state change?
- Did users registry hash change?
- Did egress registry hash change?
- Did selected moves change?
- Did service health degrade?
- Did capacity change?
- Did runtime trust change?
- Did candidate lifecycle change?
- Did execution preview consistency fail closed?
- Did dry-run verification become stale, inconclusive or mismatched?
- Did rollback preview become stale or unavailable?

## Required Inputs

- runtime state refs and hashes
- users/egress registry hashes
- selected moves fingerprint
- service matrix
- capacity summary
- runtime trust state
- candidate detail
- execution readiness/verification/rollback preview
- dry-run verification
- audit/event availability

## Recheck Outcomes

- `RECHECK_PASS`
- `RECHECK_ABORT_STALE`
- `RECHECK_ABORT_CHANGED`
- `RECHECK_ABORT_HEALTH`
- `RECHECK_ABORT_TRUST`
- `RECHECK_ABORT_CAPACITY`
- `RECHECK_ABORT_CANDIDATE`
- `RECHECK_ABORT_ROLLBACK`
- `RECHECK_ABORT_VERIFICATION`

## Verdict

`runtime_recheck_defined=true`

