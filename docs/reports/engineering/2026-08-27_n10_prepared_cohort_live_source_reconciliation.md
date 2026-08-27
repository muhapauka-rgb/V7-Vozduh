# N10 prepared cohort: live-source reconciliation

Date: 2026-08-27  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Frontier: `N10_BOUNDED_PRODUCTION_AUTHORITY_CONTRACT_REQUIRED`

## Purpose

Prepare an exact N10 small-cohort Authority request only from a current,
owner-backed source assignment.  No user, route, target, Authority contract,
Candidate, Packet, Lease, or Matrix cadence was changed in this block.

## Evidence before the correction

The existing request entrypoint stopped safely.  Its prepared class named
ordinary identities `10.7.0.33` and `10.7.0.68` with source
`openvpn-1779388847-d2ad7c`; the canonical `users.registry` instead recorded
both on `awg3`.  The blockers were
`n10_small_cohort_member_source_truth_changed` and
`n10_small_cohort_owner_generation_missing`.  The Authority request was not
registered and no effect owner ran.

An existing Matrix-owner observation-only rebuild completed successfully in
1.879 s and wrote no route or user effect.  It nevertheless retained the
stale Planner direction, proving that generation freshness alone did not bind
a prepared N10 member slice to its canonical live source.

## Correction

`build_prepared_class_decision_projection` now accepts the already-owned
ordinary live assignments when called by the Matrix refresh and advisory
materializer.  A decision whose declared source differs from the canonical
registry assignment is excluded; it is never rewritten, retargeted, or
manually replaced.  The projection records the exclusion count as
`stale_registry_source_exclusions`.

This is a bounded existing-owner lifecycle correction:

```
Planner decision + canonical users.registry agree
  -> prepared N10 class may exist
Planner decision + canonical users.registry disagree
  -> class excluded -> STOP_SAFE / fresh lawful class required
```

## Verification

- Focused policy suite: `212` passed.
- Added regression: a stale Planner source is excluded and yields no prepared
  class.
- Wider historical suite was also sampled.  It exposed pre-existing unrelated
  failures in passive-event fixtures (`AutoswitchPlanner.matrix` absent) and
  legacy compact-projection assertions that already conflict with the current
  bounded member-slice contract.  None is caused by this source-agreement
  correction; they remain outside this N10 repair and are not hidden here.

## Runtime and production effect

The correction was published as `a1e50a343e815277e096de29251d105fd7c5b088`
and safely deployed as `deploy-z8-14-Updatesystem-a1e50a3-20260827T132111`.
The aligned local, GitHub, and Runtime fingerprint checks passed.  The remote
diagnostic and Matrix observation-only rebuild performed zero route mutations
and moved zero users.  No ordinary user was exposed to the stale cohort.

The first post-deploy rebuild produced three current classes and excluded the
stale source slice.  It found no lawful unambiguous 2--4 member N10 class, so
the Authority request remained unregistered.  The response is being narrowed
to this root condition only; a missing class must not be presented as a
spurious member or generation mismatch.

## Exact next step

Safely deploy the final diagnostic narrowing, rebuild through the existing
Matrix owner once, and re-enter the existing Authority owner.  It may create
the N10 request only if it finds one fresh, unambiguous 2--4 member class.
Otherwise the correct terminal is `STOP_SAFE` with no user movement; an
ordinary production cohort must not be manufactured from stale history.
