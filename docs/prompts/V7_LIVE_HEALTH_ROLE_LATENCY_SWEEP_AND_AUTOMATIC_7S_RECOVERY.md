# V7 live health-role latency sweep and automatic 7-second recovery

Discover → Reuse → Extend → Implement.

Continue OMP.

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_LIVE_HEALTH_ROLE_LATENCY_SWEEP_AND_AUTOMATIC_7S_RECOVERY`

This is the effective addendum to the owner-supplied mission prompt. Its
existing scope, 7-second product law, strict system-owned execution law and
all existing-owner constraints remain unchanged.

## 3A. Matrix currentness is a P0 acceptance gate

An active `v7-health.service` is not proof that the detector works. For each
affected source, prove from the current owners that the relevant Matrix service
observation is fresh under the ordinary-detector freshness bound, its
`source_incident_id` matches that fresh observation, the user still has the
same current source, and the user profile still requires that failed service.

If the service is active but this evidence is stale, missing, internally
inconsistent or hidden by a restart/dead child, emit:

`MATRIX_RUNTIME_CURRENTNESS_FAILURE`

Treat it as a P0 generic Runtime defect. Repair it only through the existing
health/Matrix owner. A later regenerated Matrix row cannot retrospectively
credit the time spent in the stale gap toward the seven-second SLO.

## 4A. Exact ordinary recovery admission

An ordinary recovery may start only from this current four-way intersection:

```text
enabled current assignment
AND saved required-service profile
AND fresh Matrix failure of one of those required services
AND current owner-admitted healthy compatible target
```

Do not move all users of a `WARN` source merely because some source services
are failed. If any one input is absent or stale, repair the generic producer or
consumer defect, then return control to the normal V7 caller.

## 21A. Restart and stale-gap accounting

During every live measurement record Matrix age, health-service restart count,
child exit status and any dead-child interval. A restart must re-read current
Matrix, assignment and profile truth and level-trigger the existing automatic
consumer when an outstanding scope remains. A restart that loses or delays
that obligation is a product failure, not a reason to wait for another outage.

## 25A. Lawful cohort evidence

The four-user gate uses a naturally current compatible cohort when one exists.
If it does not, use the existing lawful Polygon with identical owners. Do not
assemble real users manually just to fill the cohort.

## Execution order

1. Reconcile stale CPS/OMP pointers against fresh Runtime evidence without
   allowing historical state to suppress this live failure.
2. Establish the Matrix-currentness gate and identify the first blocking span.
3. Repair only the proven generic cause, test, publish and safe-deploy.
4. Return control to the normal V7 Runtime and measure its automatic outcome.
5. Iterate on the largest remaining measured causal interval until the product
   SLO is met or a genuine external/product boundary is proven.
