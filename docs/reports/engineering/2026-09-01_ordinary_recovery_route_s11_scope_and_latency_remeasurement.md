# Ordinary recovery: exact route S11 scope and latency remeasurement

**Date:** 2026-09-01
**Mission:** V7 T0-to-consumer-start serialization repair and live S11 remeasurement
**Scope:** a bounded correction to the existing automatic ordinary service-failure recovery path.

## Execution law

No client, source, target, incident, Candidate, Packet, Lease, Barrier, route or
recovery state was created, selected, advanced or mutated manually for this work.
The change was deployed, then control was returned to the existing V7 Runtime
health caller.  Only a Runtime-originated recovery can count as new acceptance
evidence.

## Fresh reconciliation

The premise that `T0 -> consumer start` currently takes about ten seconds was
not confirmed.  Fresh production receipts on the prior deployed version show
that the consumer starts in 108--328 ms, while work *inside* the consumer takes
17.489--27.330 s:

| Matrix T0 (MSK) | Source | Members | T0 -> consumer start | Consumer execution | T0 -> complete |
| --- | --- | ---: | ---: | ---: | ---: |
| 19:12:47 | vless | 2 | 328 ms | 19,382 ms | 19,710 ms |
| 19:17:06 | `1` | 1 | 238 ms | 27,330 ms | 27,568 ms |
| 19:46:37 | vless | 1 | 108 ms | 17,489 ms | 17,597 ms |

Therefore no artificial serialisation/concurrency change was made.  The
largest proven synchronous residual was selected instead.

## Cause selected

Historic packet-bound execution evidence showed that, after the governed route
writer had already applied a specific ordinary user Packet, the path ran a
whole-system route scan before reaching S11.  Two observed spans were:

| Ordinary recovery | Route writer | Whole-system post-apply route scan |
| --- | ---: | ---: |
| one affected user | 1,998 ms | 5,442 ms |
| one affected user | 2,561 ms | 9,841 ms |

That global scan can be delayed by unrelated stale records and is not proof of
the affected user's route.  It was incorrectly on the per-user critical path.

## Change

Commit `40c29ed06999d375d60c5667acc2de6e339f2d7f` changes only the existing
`v7-users-autoswitch` post-Apply choice:

- ordinary Matrix-confirmed service-failure recovery now verifies the exact
  affected user's assignment, policy rule, table/default route and target;
- emergency, strict, certification setup and certification cleanup keep their
  existing exact scope;
- the broad whole-system route check remains an existing independent owner,
  but is no longer a blocking prerequisite to the affected user's required
  service S11;
- Matrix, Planner, Authority, Candidate, Packet, Lease, Barrier and the sole
  route writer were not changed.

The exact route proof still fails closed and retains the established rollback
path when the affected user's route is not correct.

## Verification and deployment

- syntax compilation: PASS;
- focused policy tests: 3/3 PASS;
- full `test_v7_users_autoswitch_policy`: 243/243 PASS;
- the separate full `test_service_failure_automation_evolution` suite remains
  blocked at its pre-existing CPS/OMP consistency fixture, before this route
  scope is exercised.  Reported divergence: stale CPS completion/frontier
  projections.  It was not modified or waived;
- GitHub, local source and Runtime truth gate: `FULLY_ALIGNED`, PASS;
- deployed Runtime file hash equals local source hash:
  `8cf21bdcd8a72be25705d311818dbed0f15157247d426c88143d42002d1e732d`;
- `v7-health.service`: active after deployment;
- no standalone Matrix or Telegram timer is active.

## Current result and exact next step

The first live V7-originated automatic recovery after the route-scope deploy
was observed.  It handled two ordinary members from source `1` to `awg0` with
no Codex operational action:

- consumer start after its current T0: **757 ms**;
- governed consumer completion: **35,014 ms**;
- two route assignments were recorded at 20:01:37.852 and 20:01:39.089 MSK;
- the existing state owner recorded both members on `awg0` at 20:01:41.314
  MSK.

The route mutations prove the automatic caller remained functional, but the
pre-existing receipt did not expose the governed sub-stages or an exact S11
timestamp.  It cannot be credited to the seven-second contract.

Commit `67fcaa977c63d173e4440b181c50eceb9fe78816` adds only a compact projection
of the existing governed monotonic timing into that same health receipt:
`planner`, `Packet/Lease/Barrier`, `Apply/verification`, total and dominant
stage.  It passed its focused unit test and was deployed through the safe
deploy owner.  GitHub/local/Runtime are again `FULLY_ALIGNED`; health service
is active.  The separate full health-loop suite still has three historical
timing-sensitive role-scheduling failures outside this receipt change.

The exact next step is the next naturally occurring V7 Runtime ordinary
failure/recovery transaction.  It will now record Matrix T0, consumer start,
governed sub-stages, exact route verification, required-service S11 and
all-affected completion.  That one result determines the next measured
residual; no manual test transition is permitted.

## Live rebind follow-up: failed-source exclusion and cooldown safety

### Observed live input

The operator re-bound three ordinary users through the Admin interface, without
any Codex route or recovery action:

| User | Operator binding (MSK) | Source |
| --- | --- | --- |
| `10.7.0.125` | 20:21:28 | `1` |
| `10.7.0.126` | 20:21:32 | `vless` |
| `10.7.0.127` | 20:21:36 | `1` |

Fresh Matrix evidence marked both sources unsuitable.  The existing Runtime
then performed its own governed recovery.  The audit trail records only
`autoswitch_failover` for each resulting mutation:

| User | Runtime target | Automatic mutation (MSK) | Elapsed from operator binding |
| --- | --- | --- | ---: |
| `10.7.0.126` | `awg3` | 20:22:17 | 44.7 s |
| `10.7.0.125` | `awg0` | 20:37:02 | 15 min 34.2 s |
| `10.7.0.127` | `awg0` | 20:37:02 | 15 min 26.3 s |

All three current assignments were subsequently read from `users.registry` as
`awg0`, `awg3`, and `awg0` respectively.  This confirms that recovery was
performed by the live V7 caller, not Codex; it **does not** satisfy the 7 s
ordinary-recovery product contract.

### Two generic defects repaired

1. Commit `bf170c18` prevents a source already confirmed failed by the fresh
   Matrix from being reintroduced as its own fallback candidate.  The prior
   planner could see the failure and still retain the same source in a later
   fallback ranking.
2. Commit `f6e051cf` makes the ordinary anti-flap cooldown yield only when the
   same current source is freshly Matrix-confirmed failed and the live
   ordinary-failure caller supplied that exact source.  It does not select a
   target or relax Candidate, Packet, Lease, Barrier, Apply, route proof, or
   required-service S11.

The second change has 2 focused tests and the full policy suite at 245/245
PASS.  It was published and safely deployed.  The independent truth check
reports `FULLY_ALIGNED`: local, GitHub and Runtime all use
`f6e051cfa105ad73d46df174fc426efc46cebf39`; `v7-health.service` is active.

### Current state and residual

At the last read no ordinary user remained on `1` or `vless`; the automatic
operation has closed.  The latest completed two-member source-`1` transaction
still took 37.333 s from its then-current Matrix T0 to consumer completion
(planner 1.888 s, Packet/Lease 0.707 s, barrier 0.304 s,
Apply/verification 7.778 s).  The remainder reflects prior stale handoff and
execution timing, so it is evidence of a failed SLO, not a valid 7-second
result.  A new naturally-originated ordinary failure is required to measure
the newly deployed cooldown behaviour end-to-end.

The independent current route check also reports registry/assignment agreement
and verified Core-primary coverage for all three recovered users:
`10.7.0.125 -> awg0`, `10.7.0.126 -> awg3`, and `10.7.0.127 -> awg0`.
