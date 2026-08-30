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

## Compatibility for already-open browser tabs

An already-open tab still contains its older half-second JavaScript timer until
it is reloaded.  The server therefore also gains a one-second **transport
cache** for `/api/live-status` and a ten-second socket timeout for disconnected
browser responses.  The cache is rebuilt exclusively from the current users
registry, egress registry and Matrix; it is not persistent and is not a new
truth source.  Thus old tabs cannot repeatedly reparse and serialize the full
read-model or retain request workers indefinitely, while a successful operator
POST still returns its exact new row without waiting for the cache.

## Completion: one-pass profile-artifact projection

Read-only process tracing of the active `v7-admin-api.service` showed the
overview worker repeatedly opening the complete `/root/v7-clients/*/*.conf`
tree: once for each user row and again inside its profile-capability view.
That made a normal overview refresh approximately `users × client configs`,
which is avoidable work on the two-vCPU Runtime and directly explains the
remaining high CPU pressure.

The overview now reuses the existing `client_artifacts_map(users)` single
config-tree scan.  Its per-user artifact rows are passed to the existing
profile projection and capability code.  Users whose profile is VLESS/Karing
only receive the same canonical `user-<ip>` fallback name that the existing
reader would have returned, without another config scan.  This is a read-model
performance repair only: no registry, Matrix, Authority, routing, Planner,
health policy or user assignment changes.

Focused verification after this final edge-case closure:

- `tests.unit.test_admin_realtime_truth` plus
  `tests.unit.test_admin_service_preferences_lifecycle`: **16 PASS**;
- tests prove one scan for a multi-user overview and no re-scan for a user
  without a WireGuard artifact;
- source diff check: PASS.

Next operational check after safe deployment: observe the existing health
caller under the reduced UI CPU load.  No client recovery is induced or moved
by this repair; any recovery evidence must originate from the live V7 Runtime.
