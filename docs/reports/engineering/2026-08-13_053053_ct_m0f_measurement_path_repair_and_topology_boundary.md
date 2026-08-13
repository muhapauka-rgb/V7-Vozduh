# CT-M0F: repair of the measurement path and topology boundary

Date: 2026-08-13 UTC  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Parent Mission: `CT-M0F CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`

## Result

`MEASUREMENT_CONSUMER_REPAIRED_DEPLOYED_AND_PRODUCTION_CALLED`.

The first VALID CT-M0F latency sample was **not** manufactured.  The current
legal terminal is:

`SAFE_PREDECESSOR_REQUIRED:EXISTING_CONTROLLED_SOURCE_RESERVATION_AND_CERTIFICATION_GROUP_OWNER`.

## Exact producer-consumer defect repaired

Earlier controlled attempts reached fresh reservation, Candidate, Packet,
lease, route verification and target payload probing, but were terminalized as
`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID`.

Two exact failures were proven from existing owner evidence:

1. The Matrix incident shell could be present with zero monotonic failure
   clocks, while the exact matching append-only controlled-condition record
   held the owner-backed clocks.  The consumer only read that record when the
   incident ID was absent.
2. The target-only payload socket already used `SO_BINDTODEVICE`, but its
   route proof asked the main routing table without `oif`.  That truthfully
   returned `ens3`, even though the bound probe path was `awg0` or `awg3`.

Commit `9155006ec5c62b16f9be08164ae883d65d27a169` repairs only existing
owners:

- `tools/v7-users-autoswitch` always loads the exact matching condition for a
  standing CT-M0F contract, preserves Matrix incident identity, and uses its
  clocks only as a non-zero fallback;
- `tools/v7-client-speed-api` adds `oif <target-interface>` only to the
  already target-only, interface-bound payload proof.  Exact-client probes
  remain unchanged.

No new owner, queue, registry, Runtime, Authority, scheduler or VLESS-specific
logic was introduced.

## Verification and deploy

- Focused existing-owner tests: `354` passed.
- Safe deploy manifest: PASS; changed production paths were exactly
  `tools/v7-users-autoswitch` and `tools/v7-client-speed-api`.
- Safe deploy: PASS, deploy ID
  `deploy-z8-14-Updatesystem-9155006-20260813T082420`.
- Production binaries match the deployed hashes; the ordinary
  `v7-autoswitch-planner.timer` remained active and called the existing Matrix
  consumer after deploy.
- Truth and convergence: PASS / `FULLY_ALIGNED` at commit `9155006e` across
  local, GitHub and production.

No routing apply, user movement, restore-barrier write, rollback apply,
Authority expansion or Production Maturity change occurred during this repair.

## Why a first valid sample cannot yet run

The live CT-M0F selector is correctly fail-closed:

- no healthy isolated controlled source with a group-aligned certification
  identity;
- no exact certification identity on such a source;
- no distinct controlled-contract-admitted target.

The topology owner confirms the standing delegated CT-M0F and controlled
topology policies are active and audit-backed.  The blocker is not an Authority
decision and is not VLESS recovery: the former isolated reservation expired;
the 52 certification identities are now spread over ordinary/shared channels;
there is no empty owner-verified source or ready existing draft that may become
the one-user controlled failure domain.  Reusing any occupied source would
violate the proven whole-interface failure isolation invariant.

## Durable next action

Existing owner: `admin/v7-admin-api egress draft lifecycle` followed by the
existing `v7-egress-set-state` reservation owner.

Re-entry condition: an owner-verified egress profile/peer configuration is
available as an existing ready draft or empty isolated source.  The existing
selector then automatically performs:

`source reservation -> one certification identity -> controlled condition -> ordinary Matrix -> Candidate -> Packet -> lease -> cutover -> Time receipt`.

Only then can the measurement loop collect the required five valid samples and
evaluate the p95/max CT-M0F gate.  This report does not claim a latency sample,
client recovery, Natural L8 evidence, or CT-M0F completion.
