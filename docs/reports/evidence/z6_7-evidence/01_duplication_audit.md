# Z6.7 Evidence 01 - Duplication Audit

Mode: READ ONLY  
Scope: duplicate orchestrators, programs, schedulers, execution chains, rollback chains, lifecycle chains, closure chains, audit chains, operation identities, ownership models

## Duplicate Orchestrator Risk

No fully equivalent orchestrator was found.

Partial and latent duplicates were found:

| Area | Existing Source | Duplicate Risk | Required Treatment |
|---|---|---|---|
| Runtime orchestrator | Autoswitch runtime chain | Canonical partial owner | Reuse and extend. |
| Planner scheduler | `systemd/drafts/v7-autoswitch-planner.*` | Latent scheduler/program duplicate | DO NOT TOUCH unless explicitly merged into canonical model. |
| Admin guarded apply | `admin/v7-admin-api` calling `v7-users-autoswitch --mode guarded --apply` | Secondary entry into same runtime owner | Keep as controlled invocation of autoswitch owner. |
| Admin direct user switch | `admin/v7-admin-api` calling movement primitive | Possible execution bypass | Model as break-glass or migrate under orchestrator authority later. |
| CLI direct movement | `v7-user-switch` outside autoswitch | Possible execution bypass | Break-glass only; audit and close as exceptional operation. |
| Generic rollback | `v7-rollback-last-change --apply` | Rollback bypass if independent | Primitive only; lifecycle owner remains orchestrator/Admin closure. |
| Sentinel execution behavior | Sentinel tooling contains autoswitch-related capability, production timer uses `--no-autoswitch` | Latent movement path | Keep signal-only in normal program. |

## Duplicate Scheduler Audit

Canonical scheduler:

- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-users-autoswitch.service`

Supporting signal schedulers:

- Telegram sentinel timer/service.
- Service matrix refresh timer/service.
- Egress quality compact timer/service.

Latent duplicate:

- `systemd/drafts/v7-autoswitch-planner.timer`
- `systemd/drafts/v7-autoswitch-planner.service`

Verdict:

- There must be exactly one runtime-cycle scheduler.
- Signal timers are not runtime orchestrator schedulers.
- Draft planner timer is not a canonical runtime scheduler and should remain out of the program unless merged deliberately.

## Duplicate Execution Chain Audit

Canonical execution path:

1. `systemd/v7-users-autoswitch.timer`
2. `systemd/v7-users-autoswitch.service`
3. `tools/v7-users-autoswitch --apply`
4. `v7-user-switch`
5. verification
6. rollback-on-verify-fail if needed
7. runtime result

Secondary paths:

- Admin guarded autoswitch apply: acceptable only as a controlled entry into the canonical runtime owner.
- Admin direct user switch: break-glass candidate.
- CLI direct `v7-user-switch`: break-glass candidate.
- Generic rollback apply: break-glass/primitive candidate.

Verdict:

- A new execution chain would duplicate existing execution authority.
- The program design must reduce all normal execution to the autoswitch-owned path.

## Duplicate Lifecycle Chain Audit

Observed lifecycle fragments:

| Fragment | Current Owner | Role |
|---|---|---|
| Runtime plan/apply/no-op/rollback result | `tools/v7-users-autoswitch` | Runtime lifecycle root. |
| Approval packet validation and denial | `admin_core/operator_execution.py` | Governance lifecycle fragment. |
| Execution contracts and readiness previews | `admin_core/operator_observability.py`, Admin API | Read-only lifecycle preview. |
| Closure records | Admin closure model | Closure lifecycle fragment. |
| Historical reports | Markdown/evidence reports | Human-readable lineage, not runtime source. |

Verdict:

- Lifecycle is fragmented but can be consolidated without replacing owners.
- Runtime terminal state must be emitted by autoswitch, audited by `v7-audit-log`, and closed by Admin closure.

## Duplicate Audit Chain Audit

Canonical audit sink:

- `tools/runtime-support/v7-audit-log`

Audit wrappers/producers:

- Admin `audit_admin(...)`.
- Operator execution append-only audit record.
- Runtime tools with local output/state.
- Historical evidence/report files.

Verdict:

- `v7-audit-log` remains audit truth.
- Wrappers may produce audit entries, but must not become separate audit truth sources.

## Duplicate Closure Chain Audit

Canonical closure owner:

- Admin closure model in `admin/v7-admin-api`.
- Operator observability consumes and summarizes closure facts.

Potential pseudo-closure sources:

- Command exit codes.
- Runtime stdout JSON.
- Markdown reports.
- Operator preview states.

Verdict:

- Exit codes and reports are evidence, not closure.
- Closure remains Admin/operator closure record.

## Duplicate Operation Identity Audit

Canonical semantic identity from Z6.6:

- `operation_id`

Lineage identities:

- `proposal_id`
- `contract_id`
- `approval_id`
- `packet_id`
- `selected_move_hash`
- `planner_generation_id`
- `runtime_snapshot_hash`
- restore-barrier identifiers
- audit identifiers
- closure key
- evidence identifiers

Verdict:

- No competing semantic operation identity should be introduced.
- Runtime Orchestrator Program must bind all lineage identities under `operation_id`.

## Duplication Verdict

Creating a new standalone orchestrator, lifecycle engine, scheduler, audit sink, closure model, rollback engine, or operation identity would duplicate existing ownership. The safe design path is reuse and extension of the autoswitch-centered chain.

