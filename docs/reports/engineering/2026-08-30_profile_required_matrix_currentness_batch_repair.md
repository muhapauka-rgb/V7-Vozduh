# Profile-required Matrix currentness: bounded-batch repair

Date: 2026-08-30  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_LIVE_HEALTH_ROLE_LATENCY_SWEEP_AND_AUTOMATIC_7S_RECOVERY`

## Finding

Live Runtime inspection found two enabled ordinary assignments on `vless` with
persisted required-service profiles. Matrix recorded failures of required
services, but the relevant observations were older than the live ten-second
admission window. The automatic recovery owner therefore correctly refused
to move users from stale evidence.

The cause was measured in the existing `other_required` health role: it is
scheduled every five seconds but one live invocation took `236999 ms`.
Subsequent runs were reported as `PREVIOUS_INVOCATION_RUNNING`. This created
a Matrix-currentness gap; it is not valid seven-second recovery evidence.

## Change

`v7-health-loop` now invokes its existing `other_required` producer with
`--lightweight-batch-producer` in addition to its existing bounded
`--fast-producer-only` mode and eight-way concurrency cap.

During the first live verification, the batch made VLESS evidence fresh, but
the detector still waited inside a per-source downstream consumer wake. One
cycle therefore took `49977 ms`; later cycles ranged from `7351 ms` to
`25751 ms`. The health parent is already the existing persistent Matrix
consumer. The default detector command no longer synchronously wakes a second
consumer per source; it returns the canonical Matrix evidence to that parent.
This removes duplicate downstream work from the detector's five-second window
without removing the governed recovery consumer.

The batch implementation already existed. It makes one ephemeral,
source-scoped sentinel pass, retains Matrix as the only persistent writer,
and treats stale or unknown results as non-actionable. No owner, policy,
Planner, authority, timer, route writer, or target-selection rule changed.

## Verification before deployment

- `tests.unit.test_v7_health_fast_deadline_loop`: 25 passed.
- Batch-specific `tests.unit.test_v7_egress_diagnose`: 4 passed.
- Static diff check: passed.

## Runtime acceptance still required

After safe deployment, observe at least one ordinary live `other_required`
cycle. It must produce fresh Matrix evidence within the role window, after
which only the normal V7 chain may proceed:

`fresh Matrix evidence -> existing health caller -> automatic scope discovery -> Authority -> Planner -> governed execution -> S11`.

Codex must not move the affected users or invoke an operational recovery
command. A restart gap or an observation older than ten seconds is reported
as `MATRIX_RUNTIME_CURRENTNESS_FAILURE` and receives no seven-second credit.
