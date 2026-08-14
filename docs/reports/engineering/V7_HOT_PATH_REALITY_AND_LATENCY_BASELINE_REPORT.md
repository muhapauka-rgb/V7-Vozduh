# V7 Hot-Path Reality and Latency Baseline Report

**Status:** `BASELINE_COMPLETE; FIRST_CHANGE_REQUIRES_ADMISSION`  
**Scope:** real production failover path only; no routing, Authority or CPS mutation.  
**Runtime effects:** `NONE` · **Production effects:** `NONE` · **Authority effects:** `NONE`

## Observed path

```text
Telegram TCP observation (4 s cadence)
  -> 14 s confirmed-failure grace
  -> existing Matrix event publication
  -> systemd wake of v7-autoswitch-planner.service
  -> event-only Matrix consumer
  -> existing governed decision / Packet / lease / restore barrier
  -> v7-users-autoswitch apply + route and service verification
```

`v7-telegram-sentinel` is a fast producer only.  It neither creates a Candidate,
Packet, lease nor route mutation.  The existing Matrix owner remains the only
canonical event owner; the governed executor remains the only apply owner.

## Production baseline (2026-08-14)

| Observation | Evidence | Consequence |
| --- | --- | --- |
| Fast sentinel timer | `v7-telegram-sentinel.timer`: 4 s, `AccuracySec=1s` | Detection cadence is not the dominant observed delay. |
| Failure confirmation | sentinel service: `--threshold-seconds 14 --timeout 1 --no-autoswitch` | The 14-second grace is an intentional false-positive guard. |
| Event consumer | `v7-autoswitch-planner.service` runs `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only` | Existing consumer is correctly reused; no second planner service exists. |
| Recent planner wall time | systemd: 70.398 s, 71.844 s, 91.417 s | A new `systemctl start --no-block` event can wait while the oneshot unit is active. |
| Recent planner resource cost | 48.212–54.244 CPU s; 546.5–551.7 MiB peak | This is materially incompatible with a fast event consumer when it has no ordinary users to protect. |
| Current ordinary affected scope | `active=false`; no `active_sources` | No ordinary production user was eligible for a move in the observed cycles. |
| Current certification-only scope | six failed-source records, 11 certification identities; `requires_scope_reconciliation=true` | Engineering/certification reconciliation is forcing the slow path. |
| Passive consumer | timed out at 30 s in the current compact receipt | It is not an apply prerequisite and did not create a route mutation. |
| Advisory consumer | completed in 53.003 s; prepared decisions were fresh with `world_model_rebuilt=false` | The repeated advisory work is not a current ordinary-user failover. |

There is no claim of an end-to-end production client-cutover latency sample in
this report: the observed source scope was not actionable, so no actual user
move was performed or fabricated.

## Required vs. non-hot work

| Segment | Classification | Reason |
| --- | --- | --- |
| Fast observation, source scope and canonical failure event | `HOT_REQUIRED` | Detects a real affected source and wakes the existing consumer. |
| Target decision, fresh Packet, lease, restore barrier, apply and verification | `HOT_REQUIRED` | Existing safety and Product Contract boundary; no bypass is admissible. |
| Full Matrix refresh | `ASYNC` | Existing 15-minute timer; not a synchronous prerequisite of the sentinel event. |
| Reports, OMP, learning and historical analysis | `ASYNC` | They may consume outcome, never gate routing apply. |
| Certification-only scope reconciliation | `ENGINEERING_DEFERRED_CANDIDATE` | It has zero ordinary affected users and no route action, but its existing durable reconciliation obligation must remain closed. |

## First bounded implementation candidate

`V7_HOT_PATH_CERTIFICATION_SCOPE_ISOLATION_V1`

Objective: make the event-only planner unit return promptly when no ordinary
affected source exists, while preserving exactly one existing-owner durable
reconciliation of a certification-only terminal and leaving the CT-M0F lane
available for its own consumer.

This is **not yet admitted**.  Admission must prove all of the following before
any code change:

1. an unchanged certification-only terminal already has an owner-backed
   reconciliation receipt, so repeated advisory planning is not required;
2. a changed incident, source scope or generation re-enters the existing
   reconciliation consumer exactly once;
3. no ordinary affected source can be classified as certification-only;
4. the wake remains the existing planner service, with no new timer, queue,
   worker, owner or truth source;
5. Packet, lease, restore barrier, route apply and verification remain
   untouched.

## Exact next action

Perform the bounded read-only admission check above against the existing event,
closure and OMP receipt owners.  If it passes, implement only that isolation,
test the no-ordinary-scope and changed-generation re-entry cases, deploy through
the existing safe path, and compare planner wall time before/after.  Otherwise
stop safe with the missing reconciliation-owner evidence.

## Programmatic delta

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Runtime files changed | 0 | 0 | 0 |
| Runtime LOC changed | 0 | 0 | 0 |
| Services/timers changed | 0 | 0 | 0 |
| Routing/Authority/CPS changes | 0 | 0 | 0 |
| Engineering reports | 0 | 1 | +1 |
