# Admin live-refresh contention repair

## Observed production condition

The two-vCPU Runtime showed load averages above 6 while the V7 admin process
used a material core share and retained hundreds of long-lived request
threads.  At the same time, normal health roles missed their own intervals and
the `other_required` client-contract detector had a 14.061-second outlier.

The Admin v2 browser issued a full `/api/live-status` canonical read-model
request every 500 ms.  That endpoint reads the users registry, egress registry
and complete service Matrix and serializes them for the UI.  This passive UI
poll was therefore able to contend with the health owner on the same small
Runtime.  It is not a safety prerequisite for recovery.

## Change

The passive live-status interval is now two seconds.  This does not slow an
operator action: profile priorities already receive the exact canonical write
result in the POST response and the UI applies it locally before the request
completes; an inline channel selection is likewise reflected optimistically
while the existing governed operation runs in the background.

No Matrix, Planner, Authority, route writer, user assignment or service
contract was changed.  Restarting the existing API through safe deploy clears
the accumulated old request workers so only the new bounded cadence remains.

## Verification

- `tests.unit.test_admin_realtime_truth`: PASS.
- `tests.unit.test_admin_service_preferences_lifecycle`: PASS.
- Next runtime check: API is active, active handler count/load returns to a
  stable level, and the health role has no contention-driven long tail before
  any fresh ordinary-recovery event is credited.
