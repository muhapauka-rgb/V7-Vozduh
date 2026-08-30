# V7 Packet-lock to Apply revalidation repair

## Scope

This logical block repairs the automatic ordinary service-failure path only.
It does not select a user or target, write a route, invoke the route writer,
or create/replay a recovery transaction.

## Live evidence before the repair

The live VLESS incident `sfinc_99304cdfa08542e6579acaf0de1963ac` remained
actionable with two ordinary identities on the failed source.  The normal
`v7-health` / Matrix caller automatically created an owner-bound transaction:

`Packet pkt_dea17c316a2a3aa9f1b0e229` ->
`Lease execlease_bdd312889f42030a82c2e5e7` ->
`Barrier rbclear_673805fa160c088006d56f10`.

Its immutable approved lock contained both selected members, the single
V7-selected target, source incident and operation
`govexec_c356c365233764a95fd7ffb6`.  It then stopped without route mutation.
The downstream diagnostic was `runtime_apply_not_performed` plus
`verification_results_missing`; there was no route-writer error, no rollback
failure, and no ordinary-user movement.

## Cause

The revalidation path treated only the controlled cutover lane as an exact
Packet-bound incident.  A regular ordinary failure with a valid
Packet/Lease/Barrier therefore performed a broad pre-planner refresh between
the immutable Packet and Apply.  That duplicate reconstruction can race the
Matrix owner and leave the Apply consumer with no executable locked cohort,
despite the canonical Packet lock retaining it.

## Change

`tools/v7-users-autoswitch` now classifies a transaction as exact Packet-bound
when all existing immutable Apply identities are present and it is either the
controlled cutover lane or the explicit ordinary-service-failure context.
The ordinary path therefore reuses the Packet lock through Apply rather than
performing the lossy broad refresh.  It still reloads and validates current
registry assignment, Matrix, target suitability, policy, Barrier, Authority
and operation-control state before the sole route writer may run.

No owner, state store, timer, planner, route writer, policy grant or parallel
truth source was added.

## Verification

- Focused two-member ordinary Packet-lock handoff regression: PASS.
- Relevant policy, governed-cycle and service-failure suites: 527 PASS.
- Python compile and `git diff --check`: PASS.

## Runtime and next step

The repair has not itself mutated Runtime routes.  After safe deployment, the
still-actionable VLESS incident must be re-entered by the normal health/Matrix
caller.  Only a V7-originated run that reaches per-member route/kernel and
required-service S11 can credit the seven-second recovery contract.

## Follow-up observation instrumentation

The first post-deploy automatic run again reached the downstream handoff but
reported no child Apply result.  Current read-only inspection confirmed that
the latest Packet lock contains two members and its independently rebuilt
operation binding is `BOUND`; therefore a route change was still not inferred
or performed.  The compact Matrix receipt now also carries only the structural
child receipt facts (payload keys, Apply-result presence/keys and whether the
existing in-process Planner was reused).  This makes the next normal V7 retry
diagnostic without logging an unbounded child payload or adding a state owner.

## Packet-to-Apply orphan closure repair

The new structural receipt showed a second generic lifecycle defect.  When a
governed child returned after its operation-control window had already been
finalized to the normal global `OPEN` state, an unapplied Packet lease could
remain active until its fifteen-minute expiry.  The existing Matrix cleanup
accepted only an exactly matching `CLOSED` window, so it could not close this
proven no-mutation orphan and the next ordinary recovery correctly stopped
behind the stale lease.

The existing Matrix cleanup now also accepts a resting, valid global `OPEN`
control state, but only after proving all of the following: the lease is for
the exact ordinary failed source; it records no Apply, route mutation or moved
users; all Packet-bound users remain on that failed source; and no governed
route process is alive.  A `CLOSED` window for another operation, any
mutation, any moved user, or any live route worker remains fail-closed.

The Matrix invokes that proof after every exited ordinary child, rather than
only for one particular non-zero child exit code.  It never starts a recovery,
selects a target or writes a route; it merely releases the stale lease through
the existing execution-lease owner.  This prevents an unstarted transaction
from blocking the normal caller for its full lease duration.

### Verification update

- Exact closed-window orphan regression: PASS.
- Newly covered already-global-OPEN orphan regression: PASS.
- Relevant service-failure, policy and governed-cycle suites: 528 PASS.
- Python compile and `git diff --check`: PASS.
