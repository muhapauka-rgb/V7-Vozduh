# Prepared decision: deployment reconciliation and Polygon baseline

Date: 2026-08-25

## Scope

Close the post-deployment reconciliation for the bounded prepared-decision
handoff before the new frozen HARD_PATH evidence series.  This report does not
claim an SLO result and does not change Planner, Matrix, Authority, cadence or
verification semantics.

## Reconciled implementation and Runtime

- Source commit and published branch: `654a45f64afda11fbdd0c25df9bb2bd14128cdda`
  on `Updatesystem`.
- Safe deployment: `deploy-z8-14-Updatesystem-654a45f-20260825T101139`.
- `v7-truth-check --runtime-readonly --json`: `PASS`, `RUNTIME_ALIGNED`.
- The deployed Matrix campaign computed fingerprint:
  `4d62e6d180fbda5bc31b2ef27c1bf685d77c4d53bdf235cafa7dabac50ac0e73`.
- `v7-health.service` is active.  The standalone autoswitch scheduler remains
  inactive in its approved manual mode; the current Matrix timer is live.
- No new owner, timer, queue, state source or Authority was introduced.

## State correction

CPS and OMP had retained a `DEPLOY_PENDING` pointer after deployment.  They now
identify the deployed bounded handoff and the actual next frontier: restore a
certification-only baseline only through its existing owners, then obtain the
new frozen HARD_PATH evidence.  Historical reports and previous evidence were
not changed or reclassified.

## Polygon observation

The current standing CT-M0F policy and its lineage checkpoint are valid:
`CT_M0F_STANDING_LINEAGE_READY`.  A regular Matrix generation completed without
an ordinary-user move.  The controlled selector then stopped safely before
Candidate/Packet/Lease because the current registry lacks an exact usable
triple:

- healthy isolated controlled source;
- unique certification-only identity assigned to it;
- distinct contract-admitted target.

The stop is `STOP_SAFE_CONTROLLED_SOURCE_PREDECESSOR_REQUIRED`, with the exact
owner predicates `no_healthy_isolated_controlled_source_with_group_aligned_certification_identity`,
`no_exact_certification_identity_for_controlled_condition`, and
`no_distinct_controlled_contract_admitted_target`.

This is a Polygon baseline drift after prior controlled samples, not a failure
of the deployed prepared-decision handoff.  No route, ordinary client,
Candidate, Packet, Lease or controlled failure condition was created in these
observations.

## Closure of the inherited controlled sample

The current predecessor reservation
`ctm0fsample_fc11fadddf30115ff68940d7` was closed through
`--reset-ct-m0f-standing-validation-sample`.  Its existing cleanup owner
re-enabled only `amneziawg-exec-20260528-10-8-1-14`; it moved no user,
left no active reservation, and changed no ordinary route.  The historical
sample remains historical evidence and is not credited to the deployed
fingerprint.

## Current external boundary

The fresh owner-backed certification-substrate preflight is STOP_SAFE before
it can issue an Authority request.  It found no healthy isolated source:

- `amneziawg-exec-20260528-10-8-1-14` has 14 reachable services but one hard
  failure;
- the other isolated controlled sources are baseline-unhealthy;
- the only healthy controlled source has ordinary occupants and therefore is
  not a legal test-failure source.

Moving a synthetic identity onto any of those sources would either manufacture
a healthy baseline or expose ordinary users to the controlled failure.  Both
are prohibited.  This is an infrastructure/health boundary, not an Authority
or code-deployment gap.

## Exact re-entry

The existing egress and Matrix owners must first prove one isolated
certification-only source with at least one reachable service and zero hard
service failures.  Then the existing substrate owner may restore an exact
synthetic binding; Matrix can prepare the controlled failure; and the program
can execute one new cold HARD_PATH sample followed by the immutable
five-sample series.  No code, configuration, cadence, Planner, Matrix,
Authority or verifier change is admitted before that precondition is true.
