# Polygon reseed and group-binding safety boundary

## Scope

This block continued the frozen HARD-path measurement work only far enough to
restore an isolated one-user controlled substrate.  No ordinary user was
selected, moved, or routed.

## Findings and applied fixes

The healthy execution-reserved Polygon source was excluded from empty-pool
reseed even though it already carried the explicit certification-source,
reservation, and ordinary-user fences.  The existing owner was corrected to
recognise that exact marked source as a source only, never as a controlled
destination or ordinary target.  The bootstrap request was also corrected to
read its existing compact candidate projection.  Finally, incremental identity
capacity is now calculated on the exact selected source rather than from a
different source's certification count.

Published and deployed commits:

- `79d9be20` — reserved certification Polygon source reseed;
- `5e385b32` — existing compact candidate projection consumed for reseed;
- `6b7197c5` — identity capacity bound to the exact source;
- `dc1b4840` — one-user provisioning uses the source-owned certification
  group and fails closed when that group is absent.

Focused regression checks passed for the source/target separation, empty
source reseed, exact-source capacity, source-group requirement and one-user
preflight.  Each commit passed `tools/v7-safe-deploy`; the final deployed
Runtime, local branch and GitHub `Updatesystem` aligned at `dc1b4840`.

## Production / Polygon observation

The existing provisioner created exactly one certification-only synthetic
identity on `amneziawg-exec-20260528-10-8-1-14` and recorded
`IDENTITY_POOL_PROVISIONED_AND_CLASSIFIED`.  Aggregated evidence after the
operation: one enabled certification identity on that source and zero ordinary
users moved.  No Candidate, Packet, Lease, routing mutation, or production
maturity change was created by the substrate operations.

The first historical provisioning had assigned a request-specific group while
the isolated source retained its prior group.  The deployed correction prevents
that mismatch for all future provisions.  The already-created synthetic identity
must be reconciled to the source's current reservation group before it can enter
the controlled hard-path transaction.

## Safety boundary

The existing `v7-egress-set-state certification-reserve` owner correctly
requires an exact current reservation id, expiry and egress fingerprint before
it may update the isolated source's certification group.  A subsequent attempt
to apply hard-coded values was rejected by the execution safety boundary:
the currently supplied id and expiry were not independently confirmed as the
current reservation contract.  No state was changed by that rejected attempt.

## Exact next step

Re-read the current source line through the existing reservation owner and
obtain an explicit approval for the current reservation id/expiry pair, then
use that owner to reconcile the source group with the one synthetic identity.
Re-run `--ct-m0f-standing-source-selection`; only if it returns ready, continue
with a single cold controlled HARD-path sample on the frozen implementation.

## Addendum: current group reconciliation and exact-client readiness

The source reservation was subsequently reconciled through the existing
`v7-egress-set-state certification-reserve` owner.  The single synthetic
identity `10.7.0.124` now belongs to the current certification-only group on
`amneziawg-exec-20260528-10-8-1-14`; the owner recorded zero user moves and
zero route changes.

The existing target-selection owner then chose `awg3` automatically from a
fresh one-shot diagnostic.  Its shared-target, one-synthetic-user policy was
explicitly admitted and records zero ordinary-user effect.  No target was
chosen manually.  A separate dedicated-draft attempt stopped safely because
the requested draft would duplicate an unhealthy interface configuration; no
draft, client or route was created from that stopped branch.

The governed controlled-condition owner next stopped before injecting a
failure: its isolated client-session handshake did not complete.  Diagnostics
proved two retained-profile mismatches in the runtime-only Polygon fixture:

- the client namespace was trying to reach the public endpoint from an
  isolated host-local veth; and
- the retained synthetic profile's peer public key did not match the live
  canonical `wg0` ingress key, so WireGuard correctly rejected the handshake.

Commit `2062e171` corrected the first mismatch by directing only the temporary
namespace's outer UDP packet to the host-side veth gateway.  Its focused test
suite passed (19 checks) and the published/server checksum aligned.  Commit
`74b860b7` then made the temporary namespace copy use the current canonical
ingress public key.  The stored profile, service configuration, ordinary
clients, Matrix, Planner and routes were not modified.

That second deploy exposed one final fixture-only fault.  A five-second
packet trace proved that the server response was emitted, but was delivered
to a different, stale Polygon namespace because every fixture reused the same
`169.254.253.0/30` link.  The current pending correction assigns a stable,
different link-local /30 from each exact synthetic identity.  It therefore
prevents one stale prepared namespace from capturing another identity's reply;
it does not alter an ordinary-user route or any canonical runtime state.

## Current next step

Publish and safely deploy the tested per-identity fixture-link correction,
re-run the exact-client preparation, and only on a successful handshake issue
one governed cold controlled condition.  If preparation remains invalid, stop
before injecting a failure and record the new exact evidence.
