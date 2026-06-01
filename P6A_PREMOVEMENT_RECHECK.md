# P6.A Pre-Movement Recheck Design

Project: V7 Vozduh

Block: P6.A

## Required Recheck

Before any future P6.B movement certification may execute, recheck:

- admin health
- users registry hash
- egress registry hash
- candidate row
- candidate route table
- destination channel row
- destination capacity
- destination quality/readiness
- trusted/direct route exclusion compatibility
- selected moves count/hash
- autoswitch safety state
- route table `1009`
- `ip rule` for candidate
- runtime checker outputs

## Exact Candidate Recheck

Must verify:

- `10.7.0.11` exists exactly once
- enabled is true
- current egress is `1`
- table is `1009`
- destination `amneziawg-exec-20260528-10-8-1-14` exists
- destination interface is `v7execwg0`
- destination users count is `0`
- destination readiness is `GO`

## Abort Conditions

Any mismatch aborts.

Abort if:

- selected moves are nonzero;
- candidate row changed;
- destination changed;
- target readiness is not GO;
- capacity status is not OK;
- route/checker baseline fails;
- approval expired;
- packet hash mismatch;
- any broader action is requested.

## Verdict

- premovement_recheck_defined=true
- any_mismatch_aborts=true
