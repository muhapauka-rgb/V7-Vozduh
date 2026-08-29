# V7 ordinary recovery — advisory snapshot deferral

Date: 2026-08-29  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Logical block: automatic ordinary failed-source recovery latency

## Result

The existing Matrix consumer no longer synchronously refreshes advisory
intelligence snapshots before an ordinary failed-source recovery transaction.
The removed wait had a configured limit of 90 seconds.

This is deliberately narrow. The current canonical Matrix incident, source
scope, target selection, Authority, Candidate, Packet, Lease, Barrier, route
verification and required-service S11 remain on the governed path. No owner,
timer, registry, Planner, queue or route writer was added.

## Cause and change

`run_bounded_delegated_service_failure_action` detected expired or mismatched
ranking/learning snapshots and invoked the existing snapshot writer before it
started the existing governed executor. This was valid for certification work,
but it made an ordinary active incident wait for an advisory refresh even when
fresh Matrix failure evidence and all execution-safety checks were available.

For `ordinary_execution` only, the refresh is now recorded as
`DEFERRED_ADVISORY_OUTSIDE_RUNTIME_HOT_PATH`. Other transaction classes retain
the established refresh behavior. The governed executor is still invoked with
`--ordinary-service-failure-only`, so it retains its existing Matrix-backed
scope, admission, rollback and S11 checks.

## Verification

- Focused service-failure lifecycle regression: `PASS` (1 test).
- The regression proves an expired/missing advisory snapshot is deferred,
  never executed synchronously, and the ordinary governed context reaches the
  existing executor.
- Source syntax compilation: `PASS`.
- Diff whitespace check: `PASS`.

## Production status and limitation

This is not yet a production latency claim. Commit
`c5e284a34472eabf2184c96f27ea54ff962d2164` was independently confirmed on
GitHub. The deployed Runtime still reports
`2b4e86896aab1a43b0399537b7f6c227e55fd26d`, and its read-only convergence
snapshot is stale: it contains an obsolete wider command set and cannot prove
the exact deployment baseline. No route, assignment, Matrix cadence, timer or
live Runtime was changed by this block.

Once a safe deploy is admissible, the next proof is one controlled Matrix
failure followed by the existing automatic ordinary consumer. Its receipt must
show first failure observation, T0, Candidate/Packet/Lease/Barrier, every
member's S11 and the last-member completion time. Only then can the real
reduction be measured against the 7-second cohort target.

## Deployment gate

The existing `v7-safe-deploy` gate passed with the published commit. Its
production apply was then blocked by the execution safety control: the control
classified deferring the advisory refresh as a possible permanent weakening of
the production safety contour and requires explicit owner confirmation after
this risk is stated. The apply was not retried and no Runtime effect is
claimed. This is an external deployment-authorization boundary, not a failed
test or a bypassable technical error.

## Consumed deployment and current Polygon boundary

The owner confirmation was subsequently supplied. The existing safe deploy
owner completed deployment `deploy-z8-14-Updatesystem-436303f-20260829T100148`
and performed its required controlled restart of `v7-health.service`.
Runtime provenance now identifies commit
`436303f3a5b2bf9cee7a131e9ee7e7462c42250e`; the live Matrix owner is active.
No customer assignment was changed by deployment.

The existing controlled-certification preflight was then run read-only on the
Runtime. It stopped safely because there is no current exact owner-backed
Polygon transaction: the certification identity/source pair and engineering
one-use Authority are incomplete or stale. The stop includes
`certification_user_ip_invalid`,
`controlled_certification_source_not_enabled`,
`exact_initial_egress_not_ready`, and invalid/expired exact Authority lineage.
This cannot lawfully be repaired by inventing a source, selecting a target
manually, or replaying historical state. It prevents a new controlled
end-to-end timing receipt, but does not prevent the deployed ordinary
production recovery path from using its separate current Matrix and standing
Authority contract.

The residual owner action is to admit one fresh isolated certification-only
source, identity and one-use Authority through the existing certification
lifecycle. Only after that can Polygon produce a valid `T_FIRST_VALID_FAILURE`
to last-member S11 measurement. Until then the seven-second target is a
deployed binding requirement, not a certified observed result.
