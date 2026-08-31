# EIGHT_MINUTE_LATENCY_COLLAPSE

## Purpose and execution rule

This report consolidates the causal repair work after the real three-user
ordinary bad-placement event.  Codex repaired generic V7 implementation only.
It did not select a source or target, change an ordinary assignment, create an
incident/Authority/Candidate/Packet/Lease/Barrier, invoke `v7-user-switch`, or
wake a recovery as a substitute for the live V7 caller.

The binding acceptance remains:

```text
first valid failure observation -> all affected required-service S11 <= 7 s
maximum <= 8 s
```

No fresh homogeneous V7-owned end-to-end sample exists after the final repair,
so this report does **not** claim the SLO as consumed.

## Immutable failure evidence

| Boundary | UTC | Observed delay |
| --- | --- | ---: |
| Operator bad placement of three ordinary users onto VLESS | 2026-08-30 21:43:29–21:43:41 | baseline |
| First relevant Matrix observation | 21:45:22.262 | 101–113 s from placement |
| First automatic route commit | 21:51:37.969 | 375.707 s after first observation |
| Last automatic route commit | 21:51:39.847 | 1.878 s member spread |
| User-visible total | — | 478.482–488.585 s |

The kernel/Core-primary spread was not the dominant problem.  The material
delays were detection and a repeated Matrix-to-governed-execution lifecycle.

## Causal map and repaired blockers

| Rank | Stage | Evidence before repair | Cause | Repair through existing owner | Result after repair |
| ---: | --- | --- | --- | --- | --- |
| P0 | A4–A5, first exact failure -> Matrix T0 | a foreground confirmation could wait up to 90 s for the Matrix writer lock | bounded recovery confirmation inherited the general lock wait | `v7-egress-diagnose` now invokes the same Matrix writer with exact one-second role and lock budgets | a busy advisory writer produces fail-closed retry, not a minute-long blind wait |
| P0 | B1–B11, Matrix -> governed Apply | multi-user handoff dropped the already confirmed failed source | an empty source was passed to the batch Apply revalidation | existing Packet-bound source is retained for the full affected cohort | consumer retains exact current source scope |
| P0 | B4–B6, target/admission work | completed certification diagnostic ran despite no active certification campaign | inactive controlled diagnostic rebuilt broad target inventory synchronously | the existing Matrix scheduler reads the existing binding first and performs that diagnostic only for an active controlled campaign | ordinary recovery no longer pays inactive certification work |
| P0 | A1–A3, passive Runtime contention | old `other_required` runs reached 30–66 s and historic runs 43–78 s | advisory/deep work contended with the only ordinary profile detector | existing health loop preempts non-critical advisory roles for the detector | current detector is 1.78–1.98 s in the stable observed window |
| P0 | A1–A3, Admin contention | `v7-admin-api` used about 39% CPU on the two-vCPU host | passive overview repeatedly ran the full user-route shell report although Admin already has an exact route read-model | existing `v7-killswitch-check` gained read-only `--admin-summary`; Admin retains global guard checks and uses its existing per-user `route_status` rows | admin CPU fell below 1%; summary output is 1,111 bytes versus the full checker’s 32,599 bytes |
| P1 | A1, placement -> next profile observation | ordinary detector cadence was 5 s | avoidable blind interval after a placement | existing `v7-health-loop` interval is 3.5 s, with a 750 ms initial offset | stable 1.78–1.98 s probes retain about 1.5 s headroom for target readiness |

The former full checker remains unchanged for deploy and dedicated security
diagnostics.  The summary mode does not remove a safety invariant; it only
omits a duplicate per-user textual dump from passive browser refreshes.

## Current Runtime evidence

Deployed commits and safe-deploy records:

| Commit | Change | Deployment |
| --- | --- | --- |
| `64cf9b1eba1e3e5e0ebd4503870fcc4a5525fcbe` | one-second canonical confirmation lock + cohort failed-source handoff | safely deployed before this report |
| `51a134de050b1dd320760a5bef33836462d04038` | defer inactive certification diagnostic | safely deployed before this report |
| `b10fb860c973ce221ddd08edb3af9d92eeb51f0e` | keep Admin overview off the recovery hot path | `deploy-z8-14-Updatesystem-b10fb86-20260831T024725` |
| `d68908f1d203e010a3c94035e23638f42219230d` | reduce ordinary detector blind window | `deploy-z8-14-Updatesystem-d68908f-20260831T025344` |

Final direct Runtime checks (the report-only commit following this deployment
does not change Runtime code):

- deployed Runtime implementation commit:
  `d68908f1d203e010a3c94035e23638f42219230d`;
- report commit: `b2c2c69c`; it contains evidence only and was not deployed;
- `v7-health.service` and `v7-admin-api.service`: `active`;
- Runtime health-loop SHA-256:
  `3857d642900c216283b72b2cc65519024d30421c195d644d0b174a5e1ae7476e`;
- normal ordinary detector cadence: `3500 ms`;
- stable observed detector completions: `1778`, `1824`, `1838`, `1876`,
  `1903`, `1908`, `1928`, `1932`, `1973`, `1979 ms`;
- prepared target role remains current and independent; no new owner, timer,
  Planner, Matrix writer, registry or state source was introduced;
- the obsolete standalone `v7-users-autoswitch.service` had no trigger,
  timer, process or reverse dependency.  Its stale failed marker from
  2026-08-28 was reset to `inactive/dead`; it was not started.

Current read-only reconciliation found no ordinary user whose declared service
contract is currently failed on its assigned source.  The one user still on
the failed historical OpenVPN source is a `certification_user=1` identity;
the ordinary recovery owner correctly excludes it.  No ordinary recovery was
manually produced to make the system look healthy.

## Tests

Passed before the deployments:

- `tests.unit.test_admin_realtime_truth`;
- `tests.unit.test_api5_runtime_route_diagnostic_views`;
- `tests.contracts.endpoint_inventory_test`;
- focused health-loop, service-failure and non-Telegram regressions;
- `bash -n hardening/v7-killswitch-check`;
- `git diff --check`.

One broader health-loop simulation suite currently has three incompatible
fixtures: each starts a controlled ordinary detector at time zero yet asserts
that the detector cannot preempt the same simulated background roles. These
fixtures do not model production’s staggered role offsets. They received no
SLO credit and do not invalidate the focused production checks above.

## Remaining boundary and exact next action

The minute-scale and >10-second avoidable dependencies identified in the
eight-minute trace have been removed or bounded.  What remains is evidence,
not an implementation patch: observe the next fresh V7-owned ordinary
required-service failure (or a lawful fresh certification Polygon context),
and record:

```text
placement -> first probe -> Matrix T0 -> current scope -> Authority
-> Candidate -> Packet -> Lease -> Barrier -> Apply -> every member S11
-> all affected recovered
```

All timing samples, including failures, must remain in the distribution.  The
terminal may be emitted only after repeatable `P95 <= 7 s` and `MAX <= 8 s`;
until then the Program remains at `IMPLEMENTATION_RESIDUAL / evidence required`.

## Final fresh reconciliation after deployment

At `2026-08-31 03:04 MSK` (the Matrix file uses UTC, therefore this is
`00:04 UTC`) the current Runtime was read again.  `v7-health.service` and
`v7-admin-api.service` were active.  The role loop was continuously completing
the profile-required ordinary detector in `1.95--2.37 s` on its `3.5 s`
cadence, while the canonical Matrix itself was being written on each cycle.

There is no current enabled ordinary affected scope from which a valid product
recovery measurement can be taken.  The only current ordinary registry entry
on VLESS is disabled.  Its Matrix failure is consequently correctly retained
as history and does not permit a production route change.

The existing Polygon identities are also not a lawful substitute at this
moment: no certification identity is currently bound to the live source of
its matching certification group, and the execution-only source is not marked
as an active controlled source.  Rebinding either by hand would manufacture
the test, bypass the existing reservation/Authority lifecycle, and make any
seven-second result invalid.

Therefore no fresh controlled or ordinary end-to-end timing was claimed in
this report.  The implementation is deployed and live; the only remaining
boundary is an owner-admitted fresh ordinary incident or a newly admitted
controlled certification context created by its existing lifecycle owner.
