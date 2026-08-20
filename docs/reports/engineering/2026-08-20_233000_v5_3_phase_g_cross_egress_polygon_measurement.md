# V5.3 Matrix health — Phase-G cross-egress Polygon measurement

Date: 2026-08-20  
Scope: controlled measurement of the existing complete Matrix probe portion at
cross-egress caps `1`, `2`, `4`. This report does not change Runtime,
production scheduling, routes, users, cadence or automatic FAST eligibility.

## Result

`PARTIAL_PASS; NO_PRODUCTION_PARALLELISM_ADMITTED`

Eight isolated egresses each ran the existing 14-service Matrix path against a
temporary local response surface with a bounded 25 ms per-HTTP-response delay.
Each egress retained the existing inner service parallelism; caps apply only
to the outer cross-egress traversal. All 112 service observations were
healthy, all eight Matrix rows were written, no failure event was produced,
and no Runtime, route, user or Authority effect occurred.

| Cap | Complete controlled probe traversal | Change vs cap 1 | Interpretation |
| ---: | ---: | ---: | --- |
| 1 | 0.838884 s | baseline | safe serial baseline |
| 2 | 0.640213 s | 23.7% lower | bounded Polygon candidate only |
| 4 | 0.982904 s | 17.2% higher | reject for this controlled profile |

The same Polygon suite separately held the existing Matrix atomic writer at
one writer under every cap. Eight healthy egress rows were preserved with no
failure-event file. Consequently cap 2 is the only measured candidate; it is
not a production setting or FAST-consumer authority.

## What this proves and what it does not

Proved in the controlled polygon:

- cap 2 can reduce the complete latency-injected probe portion relative to
  serial traversal for this exact eight-egress/14-service profile;
- cap 4 is worse in the same profile, so it is not a default;
- the existing canonical Matrix writer remains single-writer under all caps;
- no test caused an event, route change, client movement or production effect.

Not proved:

- production endpoint latency or production time saving;
- CPU/RSS, external-service pressure, interface/SOCKS/process isolation, or
  failure-domain suitability at cap 2;
- permission to add a scheduler, alter the deployed timer, enable automatic
  FAST, or weaken the full-Matrix fallback.

## Evidence

`tests.unit.test_v5_3_matrix_controlled_comparison`: `5/5 PASS`.

The cap measurement is implemented as an extension of the existing controlled
Matrix Polygon suite. It invokes the existing `run_service` and
`update_matrix` paths, uses a temporary state/event directory and a temporary
localhost endpoint only. The host sandbox required an explicit local-port
permission; no production host was contacted.

## Exact next action

Remain in the existing Phase-G frontier and measure cap 2 under failure,
timeout and recovery profiles while recording CPU/RSS and total external probe
pressure through existing Matrix timing/resource surfaces. If any lock,
freshness, failure-domain, resource or external-pressure gate fails, retain
serial traversal. Only a complete Phase-G evidence set may be consumed; even
then Phase H separately controls any Runtime admission.
