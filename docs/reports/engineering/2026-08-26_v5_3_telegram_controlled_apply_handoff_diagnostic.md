# V5.3 Telegram controlled apply-handoff diagnostic

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Status:** bounded diagnostic correction ready for safe deployment.  
**Scope:** explain one invalid certification-only run; no performance claim.

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

## Exact next action

Safely deploy this diagnostics-only extension. If the existing campaign
admits another fresh Matrix generation, run one isolated controlled attempt.
If it again stops, use the recorded exact changed inputs to repair only the
existing owner’s applicable lease/validation rule; if it applies, collect the
complete automatic S11 evidence and reset through existing owners.
