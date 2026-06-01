# P4.A Observation Plan

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Before Action

Capture:

- packet id
- approval id
- operator identities
- users registry hash
- egress registry hash
- selected moves hash/count
- runtime snapshot hash
- dry-run summary id
- dry-run verification id/state
- rollback preview id
- audit/event tail baseline

## During Action

In a later authorized execution block, observe:

- action start marker
- governance record append result
- audit record hash
- no user movement
- no routing mutation
- no autoswitch apply
- no rollback execution

## After Action

Verify:

- action record exists once
- replay with same approval id is denied
- selected moves remain empty
- users registry unchanged
- egress registry unchanged
- route state unchanged
- operator timeline shows action
- audit search finds action and denial/replay evidence

## Retention

Use existing audit/event retention. P4.A creates no new unbounded stream.

## Verdict

`observation_plan_defined=true`

