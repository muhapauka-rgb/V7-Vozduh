# V7: three-client live recovery — control-window sequencing repair

**Date:** 2026-08-30  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_THREE_CLIENT_LIVE_RECOVERY_7S_ACCEPTANCE`

## Purpose

Restore the existing automatic ordinary-user recovery chain for a real failed
source without manually moving a user or creating a recovery transaction. The
live input is the current VLESS assignment of `10.7.0.125`, `10.7.0.126`, and
`10.7.0.127`. Their required-service profiles were read from the canonical
registry; no user, route, Matrix state, Candidate, Packet, Lease, or Barrier
was written by the engineering session.

## Evidence before the repair

The normal `v7-health` / Matrix consumer did discover VLESS as a failed source
and did start a governed ordinary-recovery transaction. Its durable result was
`GOVERNED_TRANSACTION_STOPPED`, with
`packet_bound_execution_control_window_not_open` before Apply. Therefore the
runtime had not moved any user (`users_moved=0`).

The root cause was sequencing, not target selection: the parent governed
Packet/Lease/Barrier executor checked for a short exact execution-control
window before invoking `v7-user-switch`. The only code that could open that
same window was in the child route writer, so it could never be reached. The
resting global state is intentionally fail-closed (`OPEN`), which made every
otherwise valid automatic recovery stop safely.

## Implemented generic repair

* The existing governed executor now opens a short-lived, Packet/Lease/Barrier
  bound `EMERGENCY_FAILOVER` operation window only after its final mutable
  checks and immediately before its existing pre-Apply decision.
* `v7-user-switch` remains the sole route/Core-primary writer. It can only
  adopt the already-opened window when operation id, selected-move hash, source
  and snapshot hashes, action class, and exact selected count all match.
* The existing control owner permits only an exact emergency-recovery cohort of
  two through four users. This does not create general batch authority.
* The parent binds the actual Packet selection count, not the standing policy
  ceiling; a policy limit of four cannot turn a three-user transaction into a
  four-user one.
* A mismatched, stale, or non-operation-scoped window remains STOP_SAFE and is
  finalized through the existing owner.

No Planner, Matrix owner, timer, route writer, registry, queue, or alternative
truth source was added.

## Verification before publication

* syntax compilation: pass;
* new exact-window ordering and bounded-cohort tests: 4 passed;
* `tests.unit.test_v7_users_autoswitch_policy`: 226 passed.

The broader combined governed test selection retained two pre-existing,
time-dependent failures caused by an expired standing delegated-policy contract;
the six failures introduced during the first unscoped draft were eliminated by
restricting the parent-window behavior to the ordinary-service-failure path.

## Current next step

Publish and deploy the tested repair. Then use only the normal live V7 caller
to observe the current three-user source condition. The pre-existing live
policy is still a one-user tier and must be lawfully re-issued through the
existing Authority owner at the already authorized bounded cohort limit of four
before a three-user automatic recovery can be admitted. No manual recovery is
valid acceptance evidence.
