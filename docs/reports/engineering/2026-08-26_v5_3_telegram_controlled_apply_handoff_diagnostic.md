# V5.3 Telegram controlled apply-handoff diagnostic

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Status:** deployed, consumed and reconciled.
**Scope:** explain the invalid run, preserve its cause, and record the one
fresh owner-admitted Telegram controlled run that followed it.

## What happened

The existing Matrix/Planner owner received a fresh controlled Telegram failure
for the isolated identity `10.7.0.124`. It selected distinct healthy target
`awg3` automatically and created the normal Candidate, Packet, Lease and
operation-scoped barrier. The existing route writer then stopped safely before
moving the identity:

```text
approved_plan_lock_selected_moves_missing
unsafe blocker: approved_plan_lock_snapshot_gate_stop_required
```

The resulting sample `ctm0fsample_4eafea6b61ce50adb5220d63` is explicitly
`MEASUREMENT_INVALID`: it does not enter a latency distribution. No ordinary
user moved.

## Reconciliation and cleanup

The apparently requested “warm” label was not lost in transit. The standing
campaign owner recomputed its own lawful next kind as `cold`, because it had
no valid cold sample for this implementation fingerprint. That owner decision
was retained; no label was overridden manually.

The temporary Telegram failure condition was recovered by the existing exact
scope recovery operation (`v7-egress-set-state`), bound to the same source,
identity, group, reservation and source fingerprint. Full Matrix recovery
reported all checks healthy. The certification identity again uses its original
source route. Ordinary-user delta remains zero.

One unrelated pre-existing certification identity (`10.7.0.123`) still makes
the global route-check summary non-green. It is not an ordinary user and was
not modified by this work; it is outside this transaction.

## Cause bounded for the next observation

The stop proves that the final snapshot gate discarded an otherwise valid
approved move. Current receipts expose only the generic stop name, not the
gate decision, changed source fields, freshness family or lease evaluation.
Guessing would risk allowing a material change.

The deployed-next correction therefore has one effect only: the existing
route writer returns that already computed diagnostic in its normal fail-closed
result, and the existing governed caller persists it with the invalid sample.
It creates no new owner, Matrix, Planner, state file, timer, queue, registry,
route writer or permission. It cannot make an apply succeed.

## Verification

Focused regression after the correction:

```text
378 tests OK
tests.unit.test_v7_users_autoswitch_policy
tests.unit.test_governed_canary_cli
tests.unit.test_v5_3_role_based_recovery
tests.unit.test_telegram_sentinel_lock_scope
```

## Deployment and exact resolution

Commit `5ac5dd4c5f0b095e1a1333af9f463c1f3a137173` deployed the diagnostic
through the normal safe-deploy gate as
`deploy-z8-14-Updatesystem-5ac5dd4-20260826T171827`. Focused tests passed
`378` checks. Runtime, local and published code aligned; `v7-health.service`
remained active and the obsolete standalone Matrix and Telegram timers remained
disabled.

The next attempt first stopped safely for a now-visible, material reason:
the temporary certification Telegram profile had been added after the Matrix
snapshot, changing the `service_preferences` inputs. This was a test ordering
error, not an owner or routing defect. The condition was recovered through the
existing owner, the profile was installed before the next fresh generation, and
the following automatic run completed.

## Fresh automatic Telegram result

The fresh certification-only run used contract
`ctm0fsdpc_208482a67dc4103e5f0ef7b6` and sample
`ctm0fsample_f428b96f42e835ff5f4614e2`. Existing Matrix/Planner owners chose
the distinct healthy target; no target was supplied manually. Candidate,
Packet, Lease, Barrier, governed Apply, route visibility and required-service
S11 all completed. The result is functionally valid, but fails the current
Telegram performance contract:

| Interval | Measured |
| --- | ---: |
| failure to decision | 18,163.325 ms |
| decision to Apply admission | 240.232 ms |
| assignment commit | 685.845 ms |
| kernel visibility | 17.853 ms |
| kernel to required-service S11 | 6,247.165 ms |
| onset to S11 | 25,354.419 ms |

The valid sample is above both the current per-sample `8 s` ceiling and the
historical `3 s` target. It remains evidence; it was not discarded or
relabelled. The existing terminal reset returned `10.7.0.124` to `awg0`, the
temporary Telegram-only profile was removed, a fresh Matrix generation
(`matrixgen_4d75b489e679c86af12554275b241b18`) was published, and service
state again contained no Telegram-down result for the isolated source.
Ordinary-user delta is zero throughout.

## Exact next action

This diagnostic/reconciliation block is complete. No automatic performance
patch follows from one valid failing sample: the Program freezes the HARD-path
logic, and the Telegram controlled S11 scope is now functionally proven but
performance-failed. The only remaining program frontier that can affect
ordinary users, N10, requires a separate explicit product/Authority
ordinary-like cohort contract; the active shared-target contract does not
grant it. N11 remains read-only with no safe deletion admitted.
