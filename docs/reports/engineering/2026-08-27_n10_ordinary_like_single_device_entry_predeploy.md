# N10 ordinary-like single-device entry — pre-deploy reconciliation

**Date:** 2026-08-27  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_N10_ORDINARY_LIKE_SINGLE_DEVICE_PRODUCTION_ENTRY`  
**Status:** `IMPLEMENTATION_READY_FOR_SAFE_DEPLOY`

## Fresh reality

The stale VLESS record was reconciled through the existing passive-event
consumer.  It did not move a user or create Candidate, Packet or Lease.

VLESS is not the current source of the active failure scope.  Its new Matrix
observation is `WARN`: Telegram and the base Google services are reachable,
while several non-universal services have connection-reset observations.  The
current owner-backed active source is instead
`openvpn-1779388847-d2ad7c`, with an exact two-identity affected scope.  Pasha
`10.7.0.5` is on `wireguard-1779454504-c43409` and is outside that scope.

The existing Planner correctly found an ordinary rebalance candidate for Pasha
but then removed it because its incident filter globally serialised all moves
behind the unrelated OpenVPN incident.  That was stricter than the stated
product boundary: a one-user action with its own exact Authority, Candidate,
Packet, Lease, Barrier and sole route writer can coexist while the unrelated
incident remains protected.

## Implemented bounded correction

The existing policy/Authority owner and `tools/v7-users-autoswitch` now support
the exact action class `N10_ORDINARY_LIKE_SINGLE_DEVICE`.

- It binds only one named identity, its current source, canonical owner hashes,
  an expiry, one-use consumption, rollback and S11 requirements.
- It deliberately does **not** bind a target at issuance.  The target must be
  selected fresh by the existing Planner at consumption and must still pass the
  existing Candidate/Packet/Lease/Barrier checks.
- Its scope remains one user and one concurrent operation.  No other Pasha
  device and no other ordinary user can enter it.
- An unrelated active incident remains open and unchanged; N10 uses the same
  governed apply serialization rather than bypassing it.
- The route writer remains only `v7-user-switch`; no direct route command was
  added.

The new request-only entry point is
`v7-users-autoswitch --n10-ordinary-like-authority-request-only --user <IP>`.
It only registers the Authority preimage in the existing audit owner.  It
cannot issue Authority, select a target, create execution objects or move a
user.

## Verification

Focused automated checks passed:

- `tests.unit.test_operator_execution_packet`: 105 passed;
- `tests.unit.test_v7_users_autoswitch_policy`: 203 passed, including a new
  exact N10 request test;
- combined focused run: 308 passed;
- Python compilation and diff whitespace checks passed.

The broader historical service-failure module was also started.  Its result is
not a release veto for this change: one test cannot open a localhost HTTP
socket in the desktop sandbox, and a separate pre-existing test has an
obsolete fixed-date standing-policy fixture.  Neither executes the changed N10
path.  They remain visible rather than being hidden or changed in this Mission.

## Effects so far

- route changes: `0`;
- ordinary-user assignment changes: `0`;
- Candidate/Packet/Lease creation: `0`;
- Matrix/Planner/timer changes: `0`;
- OpenVPN incident state: retained.

## Exact next action

Run the existing safe-deploy gate, publish and deploy this bounded correction.
Then create and issue one fresh N10 Authority for `10.7.0.5`, run the Planner
without a target argument, and continue only if it creates the normal governed
Candidate → Packet → Lease → Barrier → `v7-user-switch` transaction.  Any
generation drift, capacity loss or service failure remains `STOP_SAFE`.
