# V5.3 Matrix health — Phase-G cross-egress Polygon measurement

Date: 2026-08-20  
Scope: controlled measurement of the existing complete Matrix probe portion at
cross-egress caps `1`, `2`, `4`. This report does not change Runtime,
production scheduling, routes, users, cadence or automatic FAST eligibility.

## Result

`PASS; NO_CROSS_EGRESS_PARALLELISM_ADMITTED`

Eight isolated egresses each ran the existing 14-service Matrix path against a
temporary local response surface with a bounded 25 ms per-HTTP-response delay.
Each egress retained the existing inner service parallelism; caps apply only
to the outer cross-egress traversal. All 112 service observations were
healthy, all eight Matrix rows were written, no failure event was produced,
and no Runtime, route, user or Authority effect occurred.

| Run | Cap 1 | Cap 2 | Cap 4 | Interpretation |
| --- | ---: | ---: | ---: | --- |
| A | 0.838884 s | 0.640213 s | 0.982904 s | cap 2 is 23.7% lower than serial; cap 4 is worse |
| B | 0.855855 s | 0.648959 s | 0.746633 s | cap 2 is 24.2% lower than serial; cap 4 remains 15.1% slower than cap 2 |
| C | 0.839652 s | 0.941068 s | 0.972804 s | both concurrent caps are slower than serial |

The cap-2 result did not reproduce in the third controlled run. Cap 4 was
similarly unstable and never beat cap 2. The same Polygon suite held the
existing Matrix atomic writer at one writer under every cap. Eight healthy
egress rows were preserved with no failure-event file. The only evidence-based
decision is therefore to retain serial cross-egress traversal.

In Run C, the existing process surfaces recorded: cap 1 / 2 / 4 peak local
request pressure `8 / 15 / 21`, peak RSS `27,744 / 29,440 / 29,680 KiB`, and
CPU `383 / 425 / 544 ms` (user plus system). These are Polygon-host numbers,
not production resource claims, but they confirm that higher caps add pressure
without a reproducible latency benefit.

## What this proves and what it does not

Proved in the controlled polygon:

- an isolated run can make cap 2 appear faster, but that benefit is not
  reproducible across the same controlled profile;
- cap 4 adds more pressure and has no reproducible benefit;
- the existing canonical Matrix writer remains single-writer under all caps;
- no test caused an event, route change, client movement or production effect.

Not proved:

- production endpoint latency or production time saving;
- production endpoint, interface/SOCKS/process or failure-domain suitability;
- permission to add a scheduler, alter the deployed timer, enable automatic
  FAST, or weaken the full-Matrix fallback.

## Evidence

`tests.unit.test_v5_3_matrix_controlled_comparison`: `6/6 PASS`.

The continuation run added a cap-2 two-egress transient-failure/recovery
check. A one-sample required-service failure was `WARN` on both egresses, did
not create an incident event, and the next healthy observation restored `OK`
on both egresses. This preserves the existing persistence and recovery rules;
it does not prove persistent-failure or production behavior.

The cap measurement is implemented as an extension of the existing controlled
Matrix Polygon suite. It invokes the existing `run_service` and
`update_matrix` paths, uses a temporary state/event directory and a temporary
localhost endpoint only. The host sandbox required an explicit local-port
permission; no production host was contacted.

## Exact next action

Consume the Phase-G no-parallelism result through the existing OMP/CPS atomic
owner. Then Phase H records that no Runtime implementation is admitted: the
full Matrix and its serial cross-egress traversal remain live, the subset is a
shadow comparison, and automatic FAST remains held. No scheduler, timer or
production cap is permitted.
