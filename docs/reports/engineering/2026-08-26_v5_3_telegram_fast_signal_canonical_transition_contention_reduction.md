# V5.3 Telegram fast-signal writer-contention reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Status:** implementation tested locally; deployment and one new controlled proof pending.  
**Scope:** reduce a measured pre-T0 delay without changing Matrix ownership,
failure criteria, Planner, Authority, routing or ordinary users.

## Evidence and cause

The previous valid cold Telegram-critical proof on the deployed required-S11
scope completed mandatory service verification in 1,183.018 ms, down from
6,931.644 ms. Its remaining dominant time was before the decision:

| Interval | Measured |
| --- | ---: |
| failure observation/confirmation before T0 | 13,566.293 ms |
| failure -> decision | 14,755.000 ms |
| onset -> S11 | 17,759.208 ms |

The existing `v7-health.service` runs Telegram observation every second. Its
journal shows multiple Telegram executions lasting 11.682 s and 16.230 s,
with consecutive one-second deadlines skipped while the same shared Matrix
writer lock was held by concurrent prepared-target/projection work. The
sentinel took that lock even for a healthy observation and merged the same
healthy value into Matrix. Those writes did not create a new actionable event
or improve target selection, but could delay the next Telegram observation.

## Bounded correction

`tools/v7-telegram-sentinel` now keeps its existing local observation state on
every run but enters the canonical Matrix writer only for either transition:

1. a confirmed, independently non-correlated Telegram failure; or
2. recovery from a failure that this same sentinel previously published.

Both transitions still call the existing `v7-service-matrix-test.update_matrix`
owner under the single existing Matrix writer lock. A healthy steady-state
observation never writes Matrix. Therefore the correction does not add a
writer, state source, scheduler, timer, queue, Planner, registry or route
writer; it removes redundant contention from an existing producer.

Failure and recovery fail closed. If the canonical owner or lock is unavailable,
the transition is not claimed as published and the normal Matrix lifecycle
remains responsible for later reconciliation.

## Verification before publication

Focused owner/transition tests passed:

```text
359 tests OK
tests.unit.test_telegram_sentinel_lock_scope
tests.unit.test_v5_3_role_based_recovery
tests.unit.test_v5_3_fast_signal_coverage
tests.unit.test_service_failure_episode
tests.unit.test_v7_users_autoswitch_policy
```

The tests prove that a healthy observation does not attempt the shared writer
lock; a published failure is still sent to the existing Matrix owner; a later
healthy result is published as recovery through that same owner; and a failed
recovery publication releases the lock rather than leaving a partial state.
No test performs a route change or moves a user.

## Exact next action

Run the existing safe-deploy gate, publish and deploy this single correction.
Then verify the live health service, owner/timer counts and absence of ordinary
user changes. Only if the current certification campaign law admits its next
fresh generation, run one controlled Telegram-critical proof and compare
failure-to-T0 against the 13,566.293 ms baseline. Do not run a fabricated
five-sample campaign, alter Telegram failure confirmation, or begin N10/N11.
