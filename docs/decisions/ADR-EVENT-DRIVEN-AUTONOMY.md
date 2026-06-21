# ADR-EVENT-DRIVEN-AUTONOMY

Status: Accepted
Date: 2026-06-21
Commit: `f875eeee50091382c1332aaa85449010875357b1`

## Context

V7 has a certified governed autoswitch/execution path up to 10 users and has production pool evidence for WireGuard. The existing system already has planner, packet, restore barrier, execution, rollback, feedback, learning, truth, and convergence owners.

POOL.3 found that production runtime is aligned and read-only runtime truth is known, but the continuous autoswitch service/timer is not active:

- `autoswitch_scheduler_active=false`
- `autoswitch_service_active=false`
- `scheduler_inactive_approved_manual_mode=true`

The available periodic checks are useful as probes and read-model refreshers, but a fixed movement timer would not express the product intent. The desired production model is event-driven autonomy.

## Decision

V7 production autonomy must be event-driven:

```text
channel/service regression
  -> planner
  -> execution packet
  -> restore barrier
  -> bounded apply
  -> verification
  -> rollback decision
  -> feedback
  -> learning
```

The production model is not "move users every 5 minutes."

## Why Fixed Timer Movement Is Wrong

Fixed timer movement is wrong because it can:

- move users without a fresh regression event;
- repeatedly react to noise instead of cause;
- bypass operator intent when evidence is stale;
- hide the difference between probes, previews, and applies;
- increase flapping risk;
- make rollback attribution harder;
- turn a governed runtime action into an always-on background mutation.

## What Periodic Checks May Do

Periodic checks may:

- refresh health/read-model evidence;
- compact quality summaries;
- refresh service matrix evidence;
- run sentinel probes;
- run planner previews;
- update intelligence snapshots when explicitly allowed by the existing tools.

## What Periodic Checks Must Not Do

Periodic checks must not:

- move users merely because a timer fired;
- bypass `tools/v7-users-autoswitch`;
- bypass `tools/v7-operator-execution-packet`;
- bypass `admin_core/operator_execution.py` restore barrier ownership;
- bypass rollback readiness;
- bypass feedback/learning closure;
- create a second planner, governance model, execution path, or truth source.

## What Blocks Production Daemon Today

POOL.3 evidence:

- autoswitch timer/service are inactive in truth-derived runtime state;
- autonomous dry-run is simulation-only;
- restore barrier readiness is `BLOCKED`;
- confidence, trust, and prediction confidence floors do not pass;
- the fresh available read-only evidence does not prove the old POOL.2 8-user failover should be applied now;
- full direct CLI `candidate_moves_total` could not be captured through the current admin API because stdout is truncated to a tail and `plan=null`.

## Required Next Implementation Phase

The next phase must be a read-only event-driven autonomy trigger certification:

1. Reuse existing regression/sentinel/service/quality signals.
2. Detect a real channel/service regression event.
3. Run the existing planner in preview.
4. Build the existing execution packet.
5. Validate restore barrier and rollback readiness.
6. Prove bounded apply eligibility without applying.
7. Record feedback/learning preview.
8. Only after certification, allow a separately approved bounded apply.

No new planner, governance, execution path, database, storage, snapshots, or truth source is allowed.

## Consequences

- Periodic probes remain valid.
- Periodic blind movement remains rejected.
- Apply stays governed.
- Event-driven autonomy becomes the canonical direction for production automation.
- Future runtime work must update `docs/reference/V7_CANONICAL_REFERENCE.md` if this contract changes.

## Affected Modules

- `tools/v7-users-autoswitch`
- `tools/v7-operator-execution-packet`
- `tools/v7-restore-settle-gate`
- `admin_core/operator_execution.py`
- `admin_core/operator_execution_feedback.py`
- `admin_core/operator_execution_pipeline.py`
- `admin_core/operator_decision_surface.py`
- `systemd/`

## Related Reports

- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
- `POOL2_STABILITY_WINDOW_RECHECK_REPORT.md`
- `BA4_TEN_USER_AUTONOMY_CERTIFICATION_REPORT.md`
