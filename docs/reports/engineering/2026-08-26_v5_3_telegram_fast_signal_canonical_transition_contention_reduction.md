# V5.3 Telegram fast-signal writer-contention reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Status:** deployed and live-verified; the following controlled attempt stopped
before route application and is invalid for performance credit.
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

## Deployment and live observation

Commit `e1d04fa775d817f78b9be9c464e12455090797eb` passed the existing
safe-deploy gate and was deployed as
`deploy-z8-14-Updatesystem-e1d04fa-20260826T165746`. Local, GitHub and Runtime
fingerprints aligned; `v7-health.service` remained active and the standalone
Matrix/Telegram timers remained disabled.

Live steady-state Telegram runs then completed in approximately 0.25--0.50 s
with `service_matrix_lock.scope=no_canonical_matrix_transition`. This confirms
the repeated healthy writer acquisition is gone. No route, Matrix ownership,
ordinary assignment or client was changed by deployment.

One later certification-only attempt selected `awg3` through the existing
Matrix/Planner owner but stopped before a route write at the final immutable
snapshot gate. It therefore supplies no timing credit. The controlled
Telegram condition was removed through the existing `v7-egress-set-state`
recovery owner; the test identity returned to its isolated source and
ordinary-user delta is zero. The exact diagnostic and its cleanup are recorded
separately in
`docs/reports/engineering/2026-08-26_v5_3_telegram_controlled_apply_handoff_diagnostic.md`.

## Exact next action

Deploy a diagnostics-only extension of the existing route writer and its
governed caller. The next permitted certification attempt will persist the
exact snapshot-gate reason and changed inputs if it stops again. Only then may
the existing owner be corrected for that specific, proven state transition;
the safety gate itself is not relaxed by this report.
