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

## Post-deploy Runtime evidence

Commit `661c0f33124b046fe63f3fa169da826b8a61ddf7` was pushed to
`Updatesystem` and deployed by `tools/v7-safe-deploy` as
`deploy-z8-14-Updatesystem-661c0f3-20260907T003113`.  Local, GitHub and the
Runtime manifest aligned; `v7-health.service` was active and the installed
owner hash matched the deployed source.

After the lifecycle-only correction, the normal V7 health caller, Matrix,
Authority, Planner, Candidate/Packet/Lease/Barrier and `v7-user-switch` chain
automatically completed two real recoveries:

| User | Source | V7-selected target | Consumer entry to required-service S11 | Provenance |
| --- | --- | --- | ---: | --- |
| `10.7.0.16` (Митяй) | `vless` | `awg3` | 15.662 s | `other_required:vless` health receipt |
| `10.7.0.17` (Тесть) | `1` | `awg3` | 14.228 s | `other_required:1` health receipt |

Both receipts report `ACTION_COMPLETED`, `runtime_mutation_performed=true` and
`users_moved=1`.  Codex did not invoke a recovery consumer, select either
target, or call the route writer.

The correction is therefore consumed.  It does **not** meet the 7-second
latency target: the receipts attribute roughly 4.8–6.0 seconds to the current
profile-obligation advisory and 6.9–7.5 seconds to governed Apply plus
verification.  Those are separate existing-owner latency residuals.
