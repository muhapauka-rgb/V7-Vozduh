# Ordinary recovery S11 terminal — causal repair

## Scope

This block continues the active `RECOVERY_LATENCY_SLO` frontier of
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`.  It changes neither
target selection, Authority, Matrix ownership, route writing nor ordinary
assignments.  It corrects a proven terminal-classification defect in the
existing governed cohort consumer.

## Current runtime evidence

The real three-member VLESS incident had one current source scope and was
handled only by the live V7 Runtime.  Before this repair, successive automatic
attempts stopped with:

`core_primary_cohort_not_admissible_before_authority_consumption`, then
`l3_production_validation_downstream_proof_failed`.

The first defect was repaired in deployed commit `51bd07e0`: a cohort with
different lawful targets now retains the existing governed member path rather
than treating the optional single-target Core-primary optimisation as an
admission gate.

The resulting automatic three-member transaction did move the members away
from VLESS, but its Health receipt completed in `42,991 ms`.  The durable
runtime evidence has the following reliable boundaries:

| Stage | Observed duration | Classification |
|---|---:|---|
| Matrix T0 to governed consumer completion | 39,494 ms | Product SLO fail |
| Full `other_required` role duration | 42,991 ms | Product SLO fail |
| Matrix T0 to first assignment | 15.25 s | Too slow for the 7 s contract |
| Matrix T0 to last assignment | 16.39 s | Too slow for the 7 s contract |
| Child route/apply/S11 evidence | 5.66 s | Safety-required work; needs new exact sample |
| Passive/learning historical tail | 8–18 s in prior attempts | Engineering-plane, not a user terminal |

The assignment-clock rows and the Matrix monotonic clock were recorded by
different owners; the table therefore deliberately does **not** turn their
wall-time difference into a false sub-millisecond claim.  A fresh sample after
this repair records a common monotonic chain.

## Causal map and blocker priority

| Blocker | Stage | Owner | Observed delay | Mandatory before S11 | Avoidable | Repair |
|---|---|---|---:|---|---|---|
| Deferred learning required as an L3 success condition | post-Apply terminal classification | existing governed cohort consumer | repeated 37–43 s attempts | No | Yes, P0 | Treat verified ordinary runtime S11 as the product terminal; leave learning deferred |
| Optional single-target Core-primary path stopped multi-target scope | pre-Authority | existing Planner cohort branch | repeated attempts | No | Yes, P0 | Already deployed in `51bd07e0` |
| Full passive/learning work | after verified S11 | existing Planner consumers | historical 8–18 s | No | Yes, P0 | Existing deferred-finalisation path retained |
| `other_required` normal detector cycle | detection | existing `v7-health` role | current 1.8–2.4 s; previous 3.6–4.3 s peaks | Yes | Under observation | No change in this block |

The repaired condition was contradictory: the route, kernel and required
service could all pass, while the ordinary recovery was still reported as a
failed L3 validation solely because the deliberately deferred learning
projection could not yet declare `production_proven`.  That made V7 retry a
completed recovery instead of closing the current obligation.

## Repair

When all of these existing conditions are true:

- an ordinary service-failure consumer is running;
- it is the existing Runtime hot path;
- the governed apply has completed; and
- every affected member has route and required-service S11;

the governed cohort consumer now emits
`GOVERNED_TRANSACTION_COMPLETED`.  It preserves the separate
`production_proven` field for the later passive/learning plane, so the change
does not falsely grant a production-learning certification.

The normal L3/certification path remains unchanged: it still requires its
existing production-proof contract.  On failed route or required-service
verification the ordinary path remains `STOP_SAFE` and preserves rollback.

## Verification completed locally

- The new runtime-hot ordinary S11 test passed.
- Existing governed pipeline test passed.
- Existing post-S11 deferred-finalisation test passed.
- `git diff --check` passed.

## Next evidence

After safe deployment, the next naturally occurring or owner-admitted Polygon
ordinary failed-source case must be observed, not manually advanced.  It will
record one common monotonic chain from first valid observation through every
member S11.  `RECOVERY_LATENCY_SLO` stays **ACTIVE** until the required
repeatable P95 and maximum bounds are met.
