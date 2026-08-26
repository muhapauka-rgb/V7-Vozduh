# V5.3 Telegram post-fix clean evidence and Pasha reconciliation

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_TELEGRAM_POST_FIX_CLEAN_EVIDENCE_AND_ROLLOUT_GATE`  
**Result:** `STOP_SAFE_FRESH_SOURCE_AND_ORDINARY_SCOPE_REQUIRED`

## What was checked

Fresh owner-backed checks were run before starting a new Telegram controlled
sample.  They covered the Matrix-backed source selector, the test identity,
temporary Telegram profile, live health services, current source inventory and
the existing controlled-substrate Authority entrypoint.  No failure condition,
Packet, Lease, route mutation or client move was created.

`v7-health.service` and `v7-admin-api.service` were active.  Their current
memory use was about 121 MB and 148 MB respectively; both had zero restarts.
The temporary Telegram profile for the former test identity was absent.

## Telegram result

The existing owner returned:

`STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED`

Its exact blockers were:

- no healthy isolated controlled source with a group-aligned certification
  identity;
- no exact certification identity for the controlled condition;
- no distinct controlled-contract-admitted target for that transaction.

The subsequent existing Authority-request owner independently confirmed the
same prerequisite: `STOP_SAFE_PREDECESSOR_REQUIRED` with
`healthy_isolated_controlled_source_or_existing_candidate_required`.

The current inventory explains this result.  The healthy empty execution
channel `amneziawg-exec-20260528-10-8-1-14` is correctly an
`EXECUTION_ONLY` controlled **target**, not a controlled failure source.
Its production assignment and ordinary reassignment flags are false.  The
only isolated source candidates are `1` and `vless`; both fail their current
Matrix baseline.  `awg0`, `awg3` and the WireGuard channel are healthy but
shared, therefore cannot be faulted for this certification transaction.

The prior cleanup deliberately returned `10.7.0.108` to `awg0` and released
its expired reservation.  It is now clean, but is no longer a certification
identity on an isolated healthy source.  Reusing the execution target as a
source, restoring an old group marker directly, or weakening the health gate
would violate the existing owner contracts.  Consequently no Telegram S11
sample was run and the historical slow sample was not reused as fresh proof.

## "Pasha" request

The identity database contains one user named `Паша` with **three active
devices**, not one unambiguous client:

| Device IP | Current route |
| --- | --- |
| `10.7.0.5` | `wireguard-1779454504-c43409` |
| `10.7.0.10` | `awg3` |
| `10.7.0.13` | `awg0` |

Each device was sent only through the existing guarded planner in read-only
mode.  It found current Matrix data but returned
`ordinary_user_eligible=false`: there is no admitted failure transaction,
fresh exact one-user product cohort contract, or prepared governed execution
handoff.  It therefore produced no Candidate, Packet, Lease, target or move.
The user name alone cannot decide which of the three independent devices may
be moved, and the running Program explicitly forbids treating an ordinary
client as a certification identity.

## Safety and effect

- ordinary-user assignment delta: `0`;
- ordinary-user route delta: `0`;
- test-identity route delta: `0`;
- Matrix, Planner, timer and policy semantics: unchanged;
- no source/target was selected manually.

## Exact next actions

1. For a new Telegram evidence series, the existing Admin/Authority lifecycle
   needs one fresh healthy isolated controlled **source** and an exact
   certification identity on it.  The current execution-only channel must
   remain a target unless its owner contract is deliberately redesigned in a
   separate mission.
2. For a real Pasha switch, provide the exact device (one of `10.7.0.5`,
   `10.7.0.10`, `10.7.0.13`) and the intended product/failure scope, or create
   the current Program's one-user ordinary-like cohort contract.  The existing
   Planner can then choose the target and the existing governed chain can
   execute and verify it without manual routing.

## Follow-up: operator selected any Pasha device (2026-08-27)

The operator selected an arbitrary Pasha device.  The deterministic active
record chosen was `10.7.0.5`, currently on
`wireguard-1779454504-c43409`.  A fresh existing-Planner run recommended
`awg0` automatically as the best target: Telegram, YouTube and Google were
healthy there; the current target projection was 35/80 users, with current
quality 90.88 Mbps average and 0.978 stability.  No target was supplied to the
planner.

The Planner correctly did **not** turn that recommendation into a selected
move.  It has a live, unrelated VLESS incident scope for eleven certification
identities.  Existing lifecycle rules serialise the active incident first and
exclude unrelated planned/rebalance moves from the executable set.  A
read-only causal-projection reconciliation was run through the same owner and
reported `PASS`; it did not create a Candidate, Packet or Lease and did not
close the active VLESS incident because its current source evidence remains
present.

The previous restore-barrier lock was also invalid and expired, bound to the
former certification identity `10.7.0.108`, not Pasha.  It was ignored for
fresh planning rather than reused.  The standing one-user action contract is
available only for certification-only controlled failover and cannot be
repurposed for an ordinary Pasha rebalance.

Therefore this follow-up intentionally performed no route mutation.  It
proved the desired target but also proved that executing it now would bypass
the active-incident serialisation and the ordinary-user action contract.  The
safe successor is: resolve or close the current VLESS incident through its own
existing lifecycle, then request a fresh one-user ordinary action contract and
run the same Planner selection again.  The target must be reselected at that
time, not cached from this observation.
