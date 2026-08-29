# V7 Live Profile Recovery: Fast-Producer Contention Repair

Date: 2026-08-30 (MSK)  
Scope: ordinary live recovery only; no user was moved by Codex.

## Trigger and observed behaviour

The operator manually placed two ordinary identities (Lisa `10.7.0.125` and
Chuck `10.7.0.126`) on VLESS while their required-service contracts could not
be satisfied there.  This is valid live acceptance input.  The V7 Runtime,
not Codex, automatically moved Lisa from VLESS to `awg0` at
`2026-08-29T22:15:45.193744+00:00` with reason
`autoswitch_governed_canary`.  Chuck remained on VLESS while the detector
became delayed.

## Root cause

The `other_required` five-second health role launched 128 simultaneous
one-second network checks on a 2-vCPU Runtime.  Fresh Runtime evidence showed
mass timeout bursts for healthy source and target contracts and role durations
of roughly 94 s and 139 s.  The same role then launched ordinary-duration
Matrix shadow confirmations, making a seven-second recovery physically
impossible.  This is a generic producer scheduling defect, not a Chuck-specific
exception and not a target-selection decision.

## Repair

1. Bound the existing batch producer to eight concurrent checks.
2. Keep the existing Matrix as the independent failure owner, but run an exact
   source/profile shadow confirmation with its supported one-second fast
   verifier.  Timeout or unknown remains fail-closed: it creates no recovery
   admission.
3. Do not change the Planner, Authority, route writer, user registry,
   service contract, Matrix owner, cadence, or target-selection rules.

## Verification before deploy

- `tests.unit.test_v5_3_role_based_recovery`: 22 PASS
- `tests.unit.test_v7_health_fast_deadline_loop`: 24 PASS
- `tests.unit.test_v7_egress_diagnose`: 31 PASS
- Total focused checks: 77 PASS.

## Live acceptance status

The repair is not credited as success merely from tests.  After safe deploy,
control returns to the normal V7 health caller.  The required evidence is a
fresh VLESS source failure followed by automatic affected-scope discovery,
Authority, Planner target choice, governed route apply, and exact required
service S11 for both current ordinary identities.  No manual operational
transition is permitted.  The measured first-valid-observation to
all-affected-recovered interval must be at most seven seconds; over eight
seconds is a failure.

## Exact next step

Publish and safely deploy this generic repair, then observe the live Runtime
until it either automatically completes the current two-client recovery with
full timing evidence or exposes the next generic stopping point.
