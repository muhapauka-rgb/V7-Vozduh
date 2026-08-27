# Core-primary route membership reconciliation — 2026-08-27

## Scope

Close the route-health finding that the broad route check reported invalid
per-user routes after the N10 cohort transition.  This block concerns the
existing Core-primary routing projection only.  It does not select a target,
move a client, change Matrix, Planner, Authority, cadence, or service checks.

## Evidence and diagnosis

The historical checker required each of 125 enabled users to have an
individual Linux policy table and used an unmarked route lookup.  That is not
the active Core-primary data plane: ingress marks a user by the `user_class`
nft map, then uses a class-level fwmark route.  Thus absent individual rules
and the host default route are not, by themselves, failures.

Commit `affd3c5affaa6599127a883069c8ab8adb2bcd89` made the verification exact:
it compares the live `user_class` and `class_egress` maps with the canonical
enabled-user registry, instead of only checking that their table exists.
Its first production observation exposed a real temporary drift:

| Map | Expected | Actual | Missing | Unexpected |
|---|---:|---:|---:|---:|
| `user_class` | 125 | 125 | 124 | 124 |
| `class_egress` | 4 | 5 | 0 | 1 |

The cause was a missing hand-off: `v7-user-switch` commits a changed canonical
assignment, while the existing registry-wide Core-primary owner derives the
nft maps from that registry.  The latter was not consumed synchronously by the
former.  No independent state source or route writer is needed.

## Implemented, tested correction

Commit `97692b70` adds only the missing existing-owner hand-off:

1. `v7-routing-sync --core-primary-active` exposes the already-approved
   Core-primary contract without duplicating its policy parsing.
2. After a governed `v7-user-switch` commits the registry, it invokes the
   existing `v7-routing-sync --core-primary-apply --json` owner.
3. A narrow operation-local preimage restores the assignment and rebuilds the
   prior projection if that owner cannot commit.  The caller receives a stable
   failure rather than a successful but stale assignment.
4. Legacy installations keep their existing per-user path.

Focused checks passed: shell syntax, Python compilation, 28 focused unit
tests covering route writer, Core verification, legacy fallback behaviour,
immediate hand-off, and failure rollback; deploy-manifest coverage; and
whitespace validation.

## Current production state

The deployed Runtime remains on the prior safe fingerprint because the
standard safe-deploy gate rejected the new hand-off as a registry-wide routing
rebuild after every individual switch.  That is a genuine broader blast radius
than the local repair and must not be bypassed.

The existing Runtime is presently healthy and reconciled:

- Core-primary contract `rcpp_6bfcaa2063bd7567c9554b6d` is approved for all
  compatible production users.
- Exact Core verification passes: 125/125 `user_class` memberships and 4/4
  class mappings, with zero missing or unexpected entries.
- The broad route checker and desired-state checker both pass in
  `CORE_PRIMARY_CLASS_ROUTING` mode with zero errors.
- `v7-health.service` is active; the retired standalone Matrix and Telegram
  timers are inactive.
- No client assignment, user route, Matrix generation, service profile, or
  ordinary-user traffic was changed during this reconciliation.

## Boundary and successor

The detection problem is closed in the current Runtime and the durable source
fix is committed and published, but it is **not deployed**.  The exact next
step is an explicit owner decision on whether each normal client switch may
atomically refresh the existing whole Core-primary map, followed by the
standard safe deploy and a governed one-client proof that the map remains
exact.  No direct deployment or alternative route mutation is permitted until
that decision.
