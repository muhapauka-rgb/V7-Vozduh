# Runtime Orchestrator Reality Audit

Date: 2026-06-01

Scope: repository and local runtime-evidence audit for V7 Vozduh runtime execution ownership.

Runtime mutation performed: NO

Implementation performed: NO

Live VPS mutation performed: NO

Live SSH read-only check: NOT COMPLETED. Key-based SSH was attempted and denied by the server; password-based SSH was not used to avoid placing the password in shell history or tool logs.

## 1. Verdict

There is no single certified Runtime Orchestrator in the current repository state.

The current system is operated by a split ownership model:

- systemd timers launch signal refresh and autoswitch apply loops;
- `v7-users-autoswitch` acts as the strongest current runtime "hands" for planner, selection, restore-barrier guard, optional user movement, verification and immediate rollback-on-verify-fail;
- Admin API can manually invoke movement, autoswitch apply, rollback, and many other apply tools;
- P2 execution surfaces are read-only contract/event/readiness visibility and explicitly do not execute;
- operator/governance packets validate and record narrow zero-movement approvals, not general movement execution.

So the practical answer is:

```text
current daily runtime hands = v7-users-autoswitch.timer + Admin API/manual operator actions + supporting signal timers
hidden orchestrator = no
mini-orchestrator = v7-users-autoswitch, but only for autoswitch movement scope
full runtime loop owner = absent
```

## 2. Evidence Summary

### 2.1 systemd launchers

`systemd/v7-users-autoswitch.service` launches:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

Evidence: `systemd/v7-users-autoswitch.service:7-9`.

`systemd/v7-users-autoswitch.timer` runs it every 20 seconds:

```text
OnUnitActiveSec=20s
Unit=v7-users-autoswitch.service
```

Evidence: `systemd/v7-users-autoswitch.timer:4-8`.

`systemd/v7-telegram-sentinel.service` launches sentinel with `--no-autoswitch`:

```text
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Evidence: `systemd/v7-telegram-sentinel.service:7-9`.

`systemd/v7-service-matrix-refresh.timer` refreshes service matrix every 15 minutes.

`systemd/v7-egress-quality-compact.timer` compacts quality every 5 minutes.

`systemd/drafts/v7-autoswitch-planner.*` exists only under `systemd/drafts/`, so it is not evidence of a current production owner.

### 2.2 Autoswitch owns the strongest runtime movement path

`tools/v7-users-autoswitch` builds decisions, selects moves, applies restore-barrier generation guards, persists dynamic load summary, and returns selected moves.

Evidence: `tools/v7-users-autoswitch:938-990`.

When `--apply` is present and mode permits movement, it calls:

```text
v7-user-switch <ip> <target>
```

then runs route verification and can rollback to the previous egress on verification failure.

Evidence: `tools/v7-users-autoswitch:1775-1810`.

It also writes anti-flap/safety state after successful movement.

Evidence: `tools/v7-users-autoswitch:1815-1855`.

This means `v7-users-autoswitch` is not merely a planner. In apply mode it is a bounded autoswitch executor.

### 2.3 Sentinel is signal owner, not production movement owner

The sentinel code has an optional path to call:

```text
v7-users-autoswitch --mode guarded --apply --service telegram --route-class GLOBAL_STABLE --pretty
```

but the production unit passes `--no-autoswitch`.

Evidence: `tools/v7-telegram-sentinel:380-420` and `systemd/v7-telegram-sentinel.service:7-9`.

Current conclusion: sentinel updates Telegram/service state for the autoswitch engine; it does not own production movement in the unit profile.

### 2.4 Admin API is a manual operator action runner

Admin autoswitch read/dry-run/apply endpoints shell out to `v7-users-autoswitch`.

Evidence: `admin/v7-admin-api:15548-15585`.

Admin manual user switch shells out to:

```text
v7-user-switch <ip> <egress>
```

and can rollback the manual switch if proxy runtime switch fails.

Evidence: `admin/v7-admin-api:34338-34375`.

Admin rollback apply shells out to:

```text
v7-rollback-last-change --apply
```

Evidence: `admin/v7-admin-api:33968-33980`.

This makes Admin API another "hands" path, but it is operator-triggered and endpoint-specific, not a single runtime loop.

### 2.5 P2 execution layer is read-only

The new `/api/execution/*` surfaces expose contracts, events, timeline, verification, rollback and readiness visibility. They explicitly state they cannot:

- move users;
- change routing;
- apply autoswitch;
- create authority;
- execute a proposal.

Evidence: `admin/v7-admin-api:12645-12670`.

P2.1 report also states:

```text
execution_engine_implemented=false
runtime_hooks_implemented=false
autoswitch_apply_run=false
```

Current conclusion: P2 has visibility and readiness modeling, not runtime ownership.

### 2.6 Operator execution packet module is not a general executor

`admin_core/operator_execution.py` says it never performs user movement, routing changes, service control or runtime apply actions.

Evidence: `admin_core/operator_execution.py:1-7`.

Its `execute_packet` path can validate/recheck/append audit records and a very narrow append-only zero-move governance state transition. It records:

```text
user_movement=False
routing_mutation=False
autoswitch_apply=False
```

Evidence: `admin_core/operator_execution.py:287-345`.

Current conclusion: this module is governance/audit persistence, not the runtime orchestrator.

## 3. What Currently Launches Each Stage

| Stage | Current launcher | Current owner | Notes |
|---|---|---|---|
| Snapshot/state | draft `v7-health.service`, runtime support tools, external runtime jobs | split | Draft service loops `v7-egress-history`, `v7-egress-stability`, `v7-egress-load`, `v7-egress-diagnose`, `v7-state-json-save`; production status not live-confirmed in this pass. |
| Service matrix | `v7-service-matrix-refresh.timer` | service-matrix refresh tool | 15-minute cadence. |
| Telegram fast signal | `v7-telegram-sentinel.timer` | sentinel | 4-second cadence, no direct autoswitch in production unit. |
| Quality history | `v7-egress-quality-compact.timer` | quality compactor | 5-minute cadence. |
| Planner | `v7-users-autoswitch` | autoswitch tool | Reads state/policy/matrix/quality/sentinel/safety/restore barrier. |
| Proposal | Admin `/api/proposals` generated/read models | Admin API | Proposal is explanatory/review layer, not execution authority. |
| Selected moves | `v7-users-autoswitch` | autoswitch tool | Selected moves are generated inside plan response; guard can zero them. |
| Restore barrier | `v7-users-autoswitch` reads/enforces; other governance tools write/update | split | Root blocker lives here: stale/expired generation/clearance lifecycle. |
| Runtime recheck | operator execution packet module for zero-move packet; execution previews for P2 | split/read-only | No general movement recheck executor yet. |
| Movement | `v7-users-autoswitch --apply`, Admin `/api/actions/user-switch`, manual `v7-user-switch` | split | No central contract-bound movement engine. |
| Verification | `v7-users-autoswitch` route check, preview/readiness tools, manual evidence | split | Autoswitch has immediate route verification only. |
| Rollback | autoswitch immediate rollback-on-verify-fail, Admin rollback endpoint, manual `v7-user-switch`, runtime rollback tools | split | No unified rollback decision owner. |
| Audit | `v7-audit-log`, admin audit calls, operator execution audit JSONL, events | split | Multiple audit writers/readers. |

## 4. State Carried Between Stages

Primary runtime state:

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/egress/state/v7-state.json`
- `/opt/v7/egress/state/egress-speed.json`
- `/opt/v7/egress/state/client-speed.json`
- `/opt/v7/egress/state/service-matrix.json`
- `/opt/v7/egress/state/egress-quality-summary.json`
- `/opt/v7/egress/state/telegram-sentinel.json`
- `/opt/v7/egress/state/autoswitch-safety.json`
- `/opt/v7/egress/state/client-reconnect-state.json`
- `/opt/v7/egress/state/egress-load-summary.json`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json`

Governance/read-only state:

- proposal records JSONL;
- execution contracts JSON;
- execution events JSONL;
- runtime trust JSONL;
- release trust JSONL;
- closure records JSONL;
- operator execution audit JSONL.

The state model is mostly file-mediated. There is not yet a single loop context object or run envelope that binds snapshot, proposal, selected moves, approval, recheck, execution, verification, rollback and audit into one lifecycle record.

## 5. Implementation Conflict Audit

No duplicate full orchestrator implementation was found.

Potential overlap/conflict zones:

- `v7-users-autoswitch` already owns much of autoswitch orchestration. A future Runtime Orchestrator must reuse it as a bounded stage or extract its stage interface, not replace it blindly.
- Admin API can manually invoke the same movement primitives. A future orchestrator must coordinate with Admin manual action paths and avoid concurrent movement.
- P2 execution surfaces model execution contracts/readiness but do not execute. A future orchestrator should consume these models rather than creating a parallel execution truth source.
- `systemd/drafts/v7-autoswitch-planner.*` suggests a possible planner-only loop, but production evidence points to the apply timer as the active autoswitch owner.

## 6. Truth Source Audit

Current authoritative runtime truth remains:

```text
runtime registry/state files > planner output > admin previews/proposals/reports
```

Current risk:

The chain is traceable, but not unified. Different stages read/write different files and logs without a single run id.

Required future truth source for orchestration:

```text
orchestrator_run_id
-> exact input snapshot hashes
-> planner generation id
-> proposal/authority ids
-> selected moves hash/count
-> restore barrier verdict
-> runtime recheck verdict
-> execution/rollback/verification events
-> closure state
```

This should reference existing state, not duplicate it.

## 7. Runtime Audit Answer

### What currently acts as the hands of the system?

Main hands:

1. `v7-users-autoswitch --apply` via `v7-users-autoswitch.timer`.
2. Admin API action endpoints invoking runtime tools.
3. Manual/operator CLI use of `v7-user-switch`, rollback tools, and support tools.

Secondary/signal hands:

1. `v7-telegram-sentinel` writes sentinel/matrix signal.
2. `v7-service-matrix-refresh-all` writes matrix refresh evidence.
3. `v7-egress-quality-compact` writes quality summary/ring.

### What launches decisions?

Autoswitch decisions are launched by:

- `v7-users-autoswitch.timer` every 20 seconds in apply mode;
- Admin `/api/autoswitch-plan` and `/api/actions/autoswitch-dry-run`;
- Admin `/api/actions/autoswitch-apply-guarded`.

Execution contract/readiness decisions are rendered read-only by Admin `/api/execution/*`.

### What launches movement?

Movement is launched by:

- `v7-users-autoswitch --apply` calling `v7-user-switch`;
- Admin `/api/actions/user-switch` calling `v7-user-switch`;
- Admin `/api/actions/autoswitch-apply-guarded` calling `v7-users-autoswitch --apply`;
- manual/CLI `v7-user-switch` in governed execution blocks.

### What launches rollback?

Rollback is launched by:

- `v7-users-autoswitch` immediate rollback if route verification fails after apply;
- Admin `/api/actions/rollback-apply` calling `v7-rollback-last-change --apply`;
- Admin manual switch rollback on proxy runtime failure;
- manual/CLI `v7-user-switch <ip> <previous-egress>` in governed movement reports;
- runtime-support rollback tools for specific subsystems.

There is no unified rollback decision loop.

### What launches audits?

Audit is launched by:

- Admin `audit_admin()` wrapper invoking `v7-audit-log`;
- runtime support tools invoking `v7-audit-log`;
- operator execution packet module appending audit JSONL records;
- event writers under `/opt/v7/events`.

There are several audit writers, not one orchestrator-owned audit stream.

### What launches autoswitch?

Production unit evidence:

```text
v7-users-autoswitch.timer -> v7-users-autoswitch.service -> v7-users-autoswitch --apply
```

Admin can also launch guarded autoswitch manually.

Telegram sentinel does not launch autoswitch in the production unit because of `--no-autoswitch`.

### Is there already a hidden orchestrator?

No.

There is an autoswitch mini-orchestrator and an Admin action runner. Neither owns the full daily runtime loop.

## 8. Roadmap: Runtime Orchestrator Program

### R0 - Live Read-Only Runtime Confirmation

Goal: confirm live service/timer/process/state reality without mutation.

Required evidence:

- `systemctl list-timers 'v7-*'`
- `systemctl status v7-users-autoswitch.timer v7-users-autoswitch.service v7-telegram-sentinel.timer v7-service-matrix-refresh.timer v7-egress-quality-compact.timer`
- `ps -eo pid,ppid,etime,command` scan for `v7-user-switch`, `v7-routing-sync`, `v7-users-autoswitch.*--apply`
- hashes and mtimes for key state files
- tail of autoswitch, audit and event logs

Do this only through a safe SSH secret path.

### R1 - Orchestrator Boundary Contract

Define the orchestrator as a coordinator, not a replacement.

It should call/reuse:

- existing state readers;
- `v7-users-autoswitch` planner/apply only through explicit stage contracts;
- P2 execution contract/readiness models;
- existing audit/event writers;
- existing rollback primitives.

### R2 - Orchestrator Run Envelope

Add a read-only run envelope first:

```text
run_id
started_at
actor
mode=observe
input_hashes
stage_results
decision_verdict
execution_allowed_now=false
```

No movement.

### R3 - Stage Inventory and Lock Model

Define exact stage ownership:

- snapshot
- health/capacity/trust
- planner
- proposal/authority
- selected moves
- restore barrier
- runtime recheck
- execution
- verification
- rollback
- audit/closure

Add a single concurrency lock/read model so Admin/manual/autoswitch paths cannot unknowingly overlap.

### R4 - Dry-Run Orchestrator

Implement `observe` and `dry-run` only.

It must:

- collect current runtime snapshot;
- call planner read-only;
- read proposal/authority/execution readiness;
- compute a deny/review/ready verdict;
- emit an orchestrator event;
- never call `v7-user-switch` or `v7-users-autoswitch --apply`.

### R5 - Contract-Bound Enforce Hook

Only after certification:

- require execution contract;
- require fresh runtime recheck;
- require rollback manifest;
- require no selected moves/hidden movers;
- require lock acquisition;
- call movement primitive;
- verify exact scope;
- rollback exact scope on failure;
- write closure.

### R6 - Admin Integration

Expose orchestrator status as a read surface first:

- current run;
- last run;
- blocked stage;
- next safe operator action;
- runtime loop freshness;
- timer/service owners;
- exact reason why no movement happened.

Do not add a new execution button before R5 certification.

## 9. Stop Condition

Audit and roadmap complete.

No orchestrator implementation started.

No runtime mutation performed.
