# V7 ordinary identity / certification-orphan reconciliation

## Trigger and current truth

The canonical identity owner records `10.7.0.16` (Митяй) and `10.7.0.17`
(Тесть) as active human users with active devices.  The Runtime user registry
nevertheless marked both as `certification_user=1` in the obsolete
`polygon-l7-canary` group.  That group has no current controlled source or
active reservation.  Consequently the ordinary automatic-recovery owner
correctly excluded them, but on an incorrect lifecycle classification.

`10.7.0.17` was additionally placed on a source carrying a detached
`t48-*` controlled-source marker.  The source had no reservation id, expiry,
reservation owner, execution/canary reservation, or matching certification
member; it was stale lifecycle residue rather than a live certification scope.

## Repair

The existing `v7-egress-set-state` lifecycle owner now provides the bounded
`certification-orphan-reconcile` action.  It can remove certification markers
only when all of the following are true:

1. each requested address is enabled on the exact source and has the exact
   obsolete certification group;
2. the canonical identity database proves one active human identity and one
   active device for that address;
3. no current controlled source still claims that group;
4. the source marker may be removed only when it has no matching member and
   no reservation, expiry, owner, execution, or canary state;
5. the source fingerprint is still exact and the caller supplies the explicit
   reconciliation confirmation.

The action creates registry backups and an audit event.  It does not select a
target, invoke the Planner, write a route, mutate an assignment, or progress a
recovery transaction.  After deployment, the normal Matrix/health caller is
the only component allowed to discover and recover the now-ordinary users.

## Verification before deploy

- shell syntax: `bash -n tools/v7-egress-set-state` — PASS;
- focused lifecycle regression: `23` tests — PASS;
- coverage includes exact active identity, dry-run versus apply, stale source
  marker removal, and refusal when a controlled source still claims the group.

## Boundary

This repair corrects classification only.  It does not claim a recovery or an
S11 result; those require a subsequent live, owner-originated V7 event.
