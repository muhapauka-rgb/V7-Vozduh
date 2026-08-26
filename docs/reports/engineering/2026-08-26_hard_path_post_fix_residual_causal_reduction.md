# HARD path post-fix residual causal reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Mission:** `V7_HARD_PATH_POST_FIX_RESIDUAL_CAUSAL_REDUCTION`  
**State:** instrumentation implemented locally and verified; publication and
controlled evidence are the next gated step

## Owner decision and scope

The prior `HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED` terminal remains
historical evidence.  The owner authorizes exactly this bounded causal
reduction mission.  It may instrument the existing path, repair only a
measured and falsified safe recurring cause, publish/deploy that repair, and
run certification-only Polygon evidence.

It does not authorize an SLO change, VDS resize, a new owner, Runtime,
Planner, timer, weakened S11 semantics, or ordinary-user movement.  No other
closed work is reopened.  The only valid outcomes are
`HARD_PATH_RUNTIME_SLO_CONVERGENCE_CONSUMED` and
`HARD_PATH_POST_FIX_RESIDUAL_EXHAUSTED`.

## Frozen starting evidence

The previous homogeneous, S11-preserving certification-only series on
fingerprint `ba7161f5f0eeb959fb193b7ec94370185f686e6ba0fe7d80b695c6727a926cd3`
was: `2696.992`, `4114.938`, `4449.524`, `4893.144`, `5014.885` ms.  Its
nearest-rank P95 is `5014.885 ms`; every sample remains in the new comparison
as historical baseline only.

## Fresh baseline capture

| Item | Observation |
|---|---|
| Local / published commit | `d26d62f109fd1cc1d48e4ec9624665b77d5a878e` on `Updatesystem` |
| Deployed performance code | `e4106fd647978adf481d78201ed10a183a130fcb`; health-loop SHA-256 `71968c7094a410f6c6c8ffe65def0424c6b156ddda6a83c18b4b3d4f0722c746` |
| Health service | active; invocation `ce3856ca2c28464f8e9146ebe3b18f8d` |
| Legacy standalone timers | Matrix inactive; Telegram inactive, as intended |
| Runtime owners at snapshot | one health-loop daemon; one Matrix projection-refresh child; no route-writer child |
| Canonical state fingerprints | `egress.registry` `e42bd1a3…`; `users.registry` `0c7c422c…` |
| Prepared projection | fresh; produced `2026-08-26T06:35:04.854131+00:00`; no world-model rebuild or registry scan |
| Synthetic evidence scope | certification-only identity `10.7.0.124`; five prior reservations each have a terminal cleanup record |
| Ordinary-user scope | no ordinary movement is admitted or observed in the baseline |

## Initial observation, not a root cause

The health journal records `hot_target` deadline misses caused by a previous
`hot_target` invocation still running, and `other_required` is deferred while
`planner_projection` runs.  This is a candidate for causal analysis only.
It is not yet evidence that a lower-priority role delays the HARD path, so no
scheduler change is admitted from this observation alone.

## Implemented diagnostic surface

The implementation retains the existing health-loop, Matrix consumer, Planner
and governed route writer.  It adds no state store, timer, route writer or
decision path.  It records evidence only:

- the split from canonical T0 to health-owner dispatch and from that dispatch
  to Matrix entry, together with process CPU, scheduler wait, context-switch
  and load observations;
- the existing route writer's lock wait, control validation, kernel mutation,
  assignment-state write, registry commit, audit and post-apply observation
  spans;
- the resulting spans are attached to the pre-existing controlled performance
  evidence only when the exact HARD path runs.

The legacy combined timing fields remain intact, so no consumer is migrated
or reinterpreted by this diagnostic change.

## Verification before publication

| Check | Result |
|---|---|
| Shell syntax for the governed route writer | PASS |
| Python compilation of all changed Runtime owners | PASS |
| Route-writer policy suite | PASS, 200 tests |
| V5.3 lifecycle binding suite | PASS, 8 tests |
| Expanded V5.3 regression | PASS; sandbox socket restriction was avoided by the existing isolated test environment |
| CPS/OMP live-pointer reconciliation | PASS; only expected local-unpublished/remote-readability blockers remain |

The lifecycle fixture was corrected to model a single synthetic atomic CPS
state across the live section, registry and protected WIP.  It does not alter
production state or relax any validator.

## Deployment reconciliation and controlled-preparation repair

The first safe-deploy invocation was intentionally a read-only plan: its
output described the intended Runtime fingerprint but did not copy files.
Direct post-plan SHA-256 reads found the prior binaries, so no controlled
sample was started.  The existing apply path was then invoked with its exact
confirmation and the required restart of the existing health service.

Deployment `deploy-z8-14-Updatesystem-9a89565-20260826T100805` is independently
confirmed: local, GitHub and Runtime now match commit
`9a895658428df2111dcc3c0734ccdd23926d9292`; `v7-health.service` is active;
the legacy standalone Matrix and Telegram timers remain inactive.

The first controlled preparation stopped before mutation with
`ct_m0f_condition_fingerprint_binding_changed`.  Two immediately repeated
read-only selections proved that the source, user and target stayed the same
while the preparation fingerprint changed.  The sole volatile contributor was
the target's ordinary fresh health observation.  That observation belongs to
the post-T0 Matrix/Planner selection, not to the pre-T0 certification
identity/source reservation.

The bounded repair keeps the exact selected target identifier in the
preparation contract but excludes only its volatile observation fingerprint
until post-T0.  After T0, the existing Matrix/Planner owner still selects and
validates the target afresh.  A regression test changes that target observation
between two otherwise identical preparations and proves the reservation
fingerprint remains stable; `116` service-failure tests and `200` autoswitch
policy tests pass (`316` total).  No ordinary user, route, timer, Authority or
S11 rule changed.

## First controlled measurements after the repair

The preparation repair was published as
`4e4d4a987ee8152f4c261a0b73d2da2338a4f037` and independently confirmed on
Runtime: the autoswitch SHA-256 is
`4b72f309570bfc9fc0a50313b376ee2023a5d2543d2e199dbd4921ec02c5dd01`, the
existing health service is active, and the old standalone Matrix and Telegram
timers remain inactive.

Two automatic, certification-only transactions completed end to end through
the existing health -> Matrix -> Planner -> Candidate/Packet/Lease -> governed
route writer -> exact kernel/required-service S11 chain.  The system, not the
operator, selected `awg0`; the only identity was `10.7.0.124`; both records
show `ordinary_user_delta = 0`.

| Sample | Result | T0 -> decision | decision -> apply | apply -> assignment | onset -> S11 |
|---|---:|---:|---:|---:|---:|
| cold | functionally valid | 2405.922 ms | 222.711 ms | 424.888 ms | 3783.960 ms |
| warm | functionally valid | 1282.353 ms | 190.210 ms | 399.889 ms | 2222.483 ms |

The second sample demonstrates that the current safe path can meet the
three-second objective.  The cold sample does not: its target-preparation
owner validation was `646.463 ms` versus `10.883 ms` warm, while both samples
also recorded roughly `0.70 s` of scheduler run-queue wait under a load average
near five on the two-vCPU Runtime.  This is evidence of variability, not yet a
proven recurring code defect.

## Second diagnostic increment awaiting publication

The measured timeline had one remaining blind interval before the first Matrix
stage: a fresh read of the policy and the exact implementation fingerprint
(which hashes the current governed executable set).  The current local change
adds only two diagnostic records, `matrix_policy_snapshot_read` and
`runtime_implementation_fingerprint`; it does not reuse, cache, relax or alter
either validation.  Compilation and 126 focused service-failure/causal-Polygon
tests pass.  It is the next safe-deploy candidate.

## Exact next step

Safely publish this diagnostic-only increment, confirm Runtime alignment, then
run one further controlled cold sample.  That sample will decide whether the
unattributed pre-Stage interval contains a recurring, safely removable span
over 100 ms.  The current one-user Authority contract explicitly permits only
one concurrent controlled transaction; higher-cohort Runtime movement is
therefore not lawful in this phase.  Any 2/5/10/20 result can only be reported
as isolated Polygon model evidence unless a later existing Authority decision
admits a different certification profile.
