# CONFIRMED_L3_WAKE Provenance Audit

Date: 2026-07-01
Workspace: `/Users/ponch/Documents/New project`
Mode: read-only audit

## Summary

`CONFIRMED_L3_WAKE` is not currently produced as a consumable production artifact for the real `openvpn-1779388847-d2ad7c` service failure.

The raw production failure exists:

- channel: `openvpn-1779388847-d2ad7c`
- service matrix status: `FAIL`
- services: `0/14` OK
- affected users in `users.registry`: `14`
- recent service-matrix refresh rows repeatedly report `FAIL`, `ok_count=0`, `total=14`

The L3 wake artifact does not exist in the forms consumed by executable code:

- `/opt/v7/events/l3-wake-events.jsonl`: missing
- `/opt/v7/events/service-failure-events.jsonl`: missing
- `/opt/v7/events/runtime-wake-events.jsonl`: missing
- inferred wake from selected move evidence: missing in the latest production lease

Verdict: `CONFIRMED_L3_WAKE_NEVER_PRODUCED`.

## Scope

This audit answers one question: where should a valid `CONFIRMED_L3_WAKE` come from in executable production code?

No runtime change, code patch, deploy, authority change, user movement, or synthetic event was performed.

## Semantic Duplicate Audit

Searched repository semantics:

- service failure
- channel failure
- required service failure
- incident
- wake
- event
- runtime resume
- incident resume
- telegram sentinel
- quality
- service matrix
- planner evidence
- failure evidence
- producer
- consumer
- event bus
- jsonl
- state
- runtime event
- transition

Executable findings:

1. `tools/v7-users-autoswitch` is the only executable L3 wake consumer.
2. It consumes external wake events from:
   - `l3-wake-events.jsonl`
   - `service-failure-events.jsonl`
   - `runtime-wake-events.jsonl`
3. It can also infer wake from selected move evidence when a selected move includes current service failures.
4. `tools/v7-service-matrix-refresh-all` produces raw service matrix refresh evidence, not an L3-compatible wake event.
5. `tools/v7-telegram-sentinel` produces telegram sentinel events and service-matrix updates, not an L3-compatible wake event.
6. `admin_core/events.py` shapes events for read-only surfaces only; it is not a producer and has no side effects.

No duplicate executable `CONFIRMED_L3_WAKE` producer was found.

## Canonical Executable Consumer

Owner: `tools/v7-users-autoswitch`

Relevant code:

- `DEFAULT_EMERGENCY_FAILOVER_AUTONOMY_POLICY`: allowed wake sources are:
  - `confirmed_service_failure`
  - `confirmed_current_channel_failure`
  - `verified_incident_resume`
  - `recorded_runtime_resume`
- `_l3_external_wake_events()`: reads only:
  - `l3-wake-events.jsonl`
  - `service-failure-events.jsonl`
  - `runtime-wake-events.jsonl`
- `_emergency_failover_move_evidence()`: derives current service failures from selected move candidate evidence.
- `_l3_wake_decision()`: accepts wake only when an allowed external event exists or inference from move evidence succeeds.

## Provenance Graph

### Path A: External Wake Event

Service Matrix / Runtime Resume / Incident Resume

-> L3-compatible wake event

-> `/opt/v7/events/l3-wake-events.jsonl`
or `/opt/v7/events/service-failure-events.jsonl`
or `/opt/v7/events/runtime-wake-events.jsonl`

-> `_l3_external_wake_events()`

-> `_l3_wake_decision()`

-> `ACCEPT_WAKE`

-> L3 incident

-> Runtime action

Current status: broken before L3 wake event file. Raw service-matrix failure exists, but no consumed wake file exists.

### Path B: Inferred Wake From Planner Evidence

Planner selected move

-> selected move includes `important_services`

-> current candidate includes `service_suitability.per_service`

-> `_emergency_failover_move_evidence()`

-> `current_failures`

-> `_l3_wake_decision()`

-> inferred `confirmed_service_failure` and `confirmed_current_channel_failure`

-> `ACCEPT_WAKE`

Current status: broken in latest production lease. `move_evidence=[]`, `failed_sources=[]`, `failed_services=[]`, and wake decision is `REJECT_WAKE`.

## Live Production Evidence

### Channel State

`openvpn-1779388847-d2ad7c`:

- service matrix status: `FAIL`
- `ok_count`: `0`
- `total`: `14`
- failed services:
  - anthropic
  - apple
  - chatgpt
  - claude
  - facebook
  - google
  - google_auth
  - instagram
  - openai_auth
  - soundcloud
  - spotify
  - telegram
  - whatsapp
  - youtube

### Affected Users

Users currently recorded on the channel:

- `10.0.0.2`
- `10.0.0.3`
- `10.0.0.6`
- `10.7.0.2`
- `10.7.0.3`
- `10.7.0.4`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.9`
- `10.7.0.10`
- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.13`
- `10.7.0.15`

### Existing Event Files

Existing raw producer logs:

- `/opt/v7/events/service-matrix-refresh-20260701.jsonl`
- `/opt/v7/events/telegram-sentinel-20260701.jsonl`

Missing L3 wake consumer files:

- `/opt/v7/events/l3-wake-events.jsonl`
- `/opt/v7/events/service-failure-events.jsonl`
- `/opt/v7/events/runtime-wake-events.jsonl`

### Latest L3 Runtime Decision Evidence

Latest lease diagnostics:

- `l3_wake_decision`: `REJECT_WAKE`
- `accepted_wake_sources`: `[]`
- `observed_events`: `[]`
- `failed_sources`: `[]`
- `failed_services`: `[]`
- `move_evidence`: `[]`
- blockers:
  - `confirmed_l3_wake_required`
  - `no_selected_moves_for_emergency_failover`
  - `restore_barrier_required_for_emergency_failover`

The raw service failure exists, but no executable L3 wake artifact reached the wake consumer.

## Lifecycle

### Birth

Expected:

- birth from confirmed service failure, confirmed current channel failure, verified incident resume, or recorded runtime resume.

Actual:

- raw service-matrix failure is born in `tools/v7-service-matrix-refresh-all`.
- `CONFIRMED_L3_WAKE` is not born.

### Propagation

Expected:

- wake event persists to one of the files consumed by `_l3_external_wake_events()`, or is carried in selected move evidence.

Actual:

- raw failure propagates only to service-matrix state and dated service-matrix refresh logs.
- it does not propagate to L3 wake files.
- it was not carried into latest `move_evidence`.

### Transformation

Expected:

- raw service failure transforms into `confirmed_service_failure` / `confirmed_current_channel_failure`.

Actual:

- no executable transformation was found from `service-matrix-refresh-YYYYMMDD.jsonl` into `service-failure-events.jsonl`.
- no latest inference from selected move evidence occurred.

### Consumption

Expected:

- `_l3_wake_decision()` consumes allowed wake source and returns `ACCEPT_WAKE`.

Actual:

- `_l3_wake_decision()` received no accepted source and returned `REJECT_WAKE`.

### Deletion / Deduplication

Expected:

- runtime state keeps processed event ids and limits them to the latest 500.

Actual:

- no wake event id was consumed, so no deletion/deduplication lifecycle occurred for this incident.

## First Missing Transition

`service-matrix-refresh confirmed FAIL`

-> `L3-compatible confirmed wake artifact`

This transition did not happen.

The concrete missing artifact is either:

- a row in `/opt/v7/events/service-failure-events.jsonl` or `/opt/v7/events/l3-wake-events.jsonl`; or
- selected move evidence containing current required-service failures sufficient for `_l3_wake_decision()` inference.

Neither path is present for the current production incident.

## Responsible Owner

Primary producer owner:

- `tools/v7-service-matrix-refresh-all`

Existing consumer owner:

- `tools/v7-users-autoswitch._l3_external_wake_events`
- `tools/v7-users-autoswitch._l3_wake_decision`

No new owner is required.

## Minimal Executable Correction

Reuse the existing service matrix producer and existing L3 wake consumer.

Smallest correction:

Extend `tools/v7-service-matrix-refresh-all` to emit an L3-compatible service failure wake event to `/opt/v7/events/service-failure-events.jsonl` when it confirms a current channel required-service failure that affects assigned users.

The event must be consumable by the existing `_l3_external_wake_events()` contract, for example:

- `wake_source`: `confirmed_service_failure`
- `channel`: affected egress id
- `service`: failed service id or compact service list
- `ts` / `observed_at`: producer timestamp
- `event_id`: stable id for deduplication

Safety boundaries:

- do not enable broad automation
- do not bypass planner
- do not bypass authority
- do not bypass approved plan lock
- do not bypass restore barrier
- do not bypass verification
- do not bypass rollback
- do not move more than one user for the first L3 validation rung

Secondary validation after the correction should confirm that the existing consumer sees the event and that `_l3_wake_decision()` changes from `REJECT_WAKE` to `ACCEPT_WAKE` only for the approved L3 production validation conditions.

## Verdict

`CONFIRMED_L3_WAKE_NEVER_PRODUCED`
