# Operator channel rebind — exact Core-primary commit — 2026-09-02

## Trigger and evidence

After the admin Runtime was refreshed, new manual selections reached the
correct endpoint but failed as `writer_rc=124`,
`operator_profile_rebind_deadline_exceeded`, or an incomplete verification.
The audit made the cause precise: the route writer could mutate a user before
its seven-second parent deadline, yet still be running its final projection
work when the parent declared the selection failed.

The expensive operation was not target health evaluation.  A single explicit
operator rebind invoked `v7-routing-sync --core-primary-apply`, which rebuilds
the complete Core-primary projection and retires legacy primary routes for the
whole registry.  That is the already-rejected global-rebuild shape for a
one-user change.  Concurrent browser clicks therefore contended for one route
writer and each could outlive the UI deadline.

## Repair

The existing Core-primary owner now admits its already-implemented exact nft
member delta for one explicitly bound `USER_SWITCH` operation.  This is only
available when all of the following are true:

- the existing operation control binds exactly one user;
- the admin endpoint has supplied its explicit operator-rebind context;
- Core-primary is active and the normal full-cohort defer mode is not active;
- the existing exact map baseline and whole-system verification pass.

The route writer remains `v7-user-switch`.  It still writes the route, source
rule, assignment and canonical registry, then calls the existing
`v7-routing-sync` owner.  Only the final Core-primary projection changes from
a full rebuild to the exact selected-member commit.  If the exact baseline is
not valid, it fails closed; no target is substituted and no user is reported
as moved without verification.

Automatic recovery semantics, its 2–4 user bounded cohort law, Matrix,
Authority, Planner and S11 are unchanged.

## Verification

- Bash syntax and Python compilation: PASS.
- Exact one-user operator commit test: PASS.
- Core-primary exactness, fallback and cohort tests: PASS.
- Route-writer control, rollback and ownership tests: PASS.
- Admin selection/retry/verification tests: PASS.
- Focused total: 56 PASS.

## Deployment and live re-entry

Published commit: `17cadef59b15fe55c3afe733b95c7e78b6c59fa6` on
`Updatesystem`.

The existing safe-deploy owner completed with `--restart-admin-if-changed`.
At 2026-09-02 13:40:30 MSK `v7-admin-api.service` was active.  The deployed
SHA-256 values for `v7-user-switch`, `v7-routing-sync`, and `v7-admin-api`
matched the published working tree exactly.  No user assignment, route, or
automatic recovery policy was changed by deployment.

No manual route action was used as evidence.

After deployment, the next normal operator click is the live proof.  Expected
user experience: the chosen channel appears immediately; V7 performs the
existing governed route mutation in the background and returns an exact
success or fail-closed reason.  Several clicks may be accepted independently,
while the one existing route writer still serializes kernel writes safely.
