# Engineering Report — Service Failure Authority Re-entry Loop

Date: 2026-07-26

## Objective

Close the existing `STOP_SAFE_AUTHORITY_REQUIRED` producer-to-consumer gap so
that an `ENGINEERING_AUTHORITY` terminal becomes the explicit input of the
next existing owner, rather than a manual dead end.

## Discovery

The current CPS correctly keeps the VLESS service-failure episode at
`ENGINEERING_AUTHORITY`: no fresh one-use action-class contract exists, and no
historical Candidate, Packet, lease or Authority is reusable. The existing
`tools/v7-users-autoswitch` owner already validates
`current_action_class_contract` from `/etc/v7/policy.json`, but it previously
had no machine-readable read-only request output describing the return link to
that policy owner.

## Implemented existing-owner loop

Added `tools/v7-users-autoswitch --action-class-contract-reconciliation-only`.
It builds a deterministic `v7.action-class-contract-reconciliation-request.v1`
from the existing Shadow/action-boundary plan and returns:

`STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`
→ request template only
→ existing `/etc/v7/policy.json` authority owner
→ existing event-driven autoswitch revalidation
→ `STOP_SAFE`, `NO_ACTION`, or `PACKET_MATERIALIZATION_ELIGIBLE`
→ existing Service Failure obligation/OMP consumer.

The template is non-durable and contains no policy write or grant. A policy
owner must independently bind a fresh Situation, Decision Trace, selected
move/snapshot identities, one-user scope, short expiry and all required gates.
The autoswitch owner then revalidates those inputs before any later
Candidate/Packet/lease lifecycle. The implementation adds no Authority owner,
registry, queue, watcher or timer.

## Verification

Focused entrypoint and service-failure tests: PASS (8 tests).

Broader affected suite: PASS (306 tests):

- `tests.unit.test_service_failure_automation_evolution`
- `tests.unit.test_v7_users_autoswitch_policy`
- `tests.unit.test_v7_truth_check`
- `tests.unit.test_autonomy_trust_acceleration`

The tests prove both missing-contract and active-contract paths, and prove the
new entrypoint has `policy_write=false`, `authority_granted=false`,
`runtime_apply=false`, `routing_mutation=false`, `users_moved=0`, and no
Candidate/Packet/lease creation.

## CPS / OMP result

CPS is intentionally unchanged: there is no new owner-backed production
result and no action-class contract has been issued. The legal current terminal
remains `ENGINEERING_AUTHORITY_SERVICE_FAILURE_ACTION_CLASS_RECONCILIATION_REQUIRED`.
The new loop makes its exact re-entry consumer executable without changing
Authority, Runtime policy, routing, user scope, Production Maturity, L7 or L8
credit.

## Exact next frontier

`V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION` through the deployed
read-only entrypoint. If and only if the existing policy owner issues a fresh
one-use scoped contract for a fresh owner-backed situation, the existing
autoswitch boundary revalidates it and emits the next legal terminal. Natural
L8 remains passive and unmanufactured.
