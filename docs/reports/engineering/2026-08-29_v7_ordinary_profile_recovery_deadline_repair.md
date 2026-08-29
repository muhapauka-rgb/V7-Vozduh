# V7 ordinary profile-recovery deadline repair

Date: 2026-08-29

## Measured gap

The live Chuck2 observation proved that the repaired HTTP sentinel reaches the
normal Matrix receiver, but also exposed a deadline contradiction: the
ordinary `other_required` role ran every five seconds and required two
lightweight observations before it invoked independent Matrix confirmation.
Even with zero execution time, the second observation alone could arrive after
the seven-second recovery objective.

The live pass also measured a 3846 ms first fast-contract result and ordinary
detector passes between 2352 and 13475 ms.  The incident recovered during
Matrix confirmation, so it was not valid recovery/S11 evidence, but this
detector topology could not meet the product deadline for a continuing
failure.

## Bounded repair

The existing one-second bounded HTTP observation now immediately requests the
existing Matrix confirmation after **one** failure sample.  It still cannot
create T0 or move a user: Matrix must create a fresh incident and validate
current source, profile, Authority, target, route and required-service S11.

After that confirmation, the already-running `v7-health` owner reads the same
current Matrix, users registry and service-preference owners to identify only
an assigned user whose own required service matches the confirmed failure.
It then uses the existing in-process Matrix consumer.  The prior separate
systemd wake becomes a harmless compatibility acknowledgement, avoiding an
extra scheduling/process boundary.  A persistent-consumer fault retains the
existing external Matrix fallback.

No owner, timer, queue, registry, truth source, Planner, route writer or
manual recovery path was added.  Engineering tooling did not move Chuck2.

## Verification before deployment

- focused handoff and fast-producer regressions: 5 passed;
- full `tests.unit.test_v7_health_fast_deadline_loop`: 21 passed;
- `git diff --check`: passed.

## Required production proof

After safe deployment, only normal V7 Runtime may consume the next continuing
profile-required-service failure.  Valid proof is:

```text
fresh protocol-level observation
-> Matrix incident/T0
-> existing health consumer
-> existing Authority and Planner
-> governed route execution
-> required-service S11
```

The resulting report must retain each timing boundary and must reject the
seven-second objective if all affected ordinary users are not recovered by
that deadline.

## Live reconciliation and second repair

After the first deployment, Chuck2 (`10.7.0.127`) was assigned to `vless` by
an operator and its actual profile required Google, Google Auth, Instagram and
Telegram. Matrix then independently recorded current protocol-level failures
for required `google_auth` and `instagram` on `vless`; the compact source
scope was exactly one ordinary user. No engineering command created an
incident, chose a target or changed this assignment.

The normal health loop was running, but the profile incident could be skipped
in its in-process handoff. The root cause was process-local de-duplication
shared by the `hard`, `telegram` and `other_required` roles: a numerically
newer T0 from one independent incident family suppressed an earlier still-open
profile-service T0. This was not a Matrix or Planner safety decision and did
not protect against replay of the profile incident.

The repair makes the existing local de-duplication key role-scoped. Matrix
remains the sole durable incident owner; each role still consumes each exact
T0 at most once. A focused regression proves a newer Telegram T0 does not
suppress a lower, independent profile-required-service T0, while replay of
the same profile T0 remains blocked.

Verification before deployment of this second repair:

- `tests.unit.test_v7_health_fast_deadline_loop`: 22 passed;
- `git diff --check`: passed.

Deployment and final acceptance still require a new continuing real Matrix
incident and an entirely Runtime-originated Candidate → Packet → Lease →
Barrier → Apply → required-service S11 chain. The prior incident recovered
before that proof could complete, so it receives no seven-second credit.
