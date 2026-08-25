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

