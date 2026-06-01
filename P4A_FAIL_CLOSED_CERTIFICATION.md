# P4.A Fail-Closed Certification

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Certified Abort States

The first action design aborts on:

- unknown
- missing
- stale
- expired
- mismatched
- invalid
- inconclusive
- blocked
- replayed
- widened scope

## Certification

Fail-closed behavior is certified at design level for P4.A.

Runtime fail-closed execution tests are not implemented in P4.A and must be part of a later explicitly authorized specification/implementation block.

## Verdict

`fail_closed_certified=true`

