# Z6.7 Evidence 04 - Final Program Maps

## Runtime Orchestrator Program Map

```text
Signal refresh programs
  -> systemd/v7-users-autoswitch.timer
  -> systemd/v7-users-autoswitch.service
  -> tools/v7-users-autoswitch
      -> operation_id binding
      -> runtime truth read
      -> planning
      -> selected moves
      -> restore barrier / generation clearance
      -> runtime recheck
      -> no-op / deny / execute
      -> v7-user-switch
      -> verify
      -> rollback branch when required
      -> terminal runtime verdict
  -> tools/runtime-support/v7-audit-log
  -> admin/v7-admin-api closure model
  -> admin_core/operator_observability.py
```

## Component Ownership Map

| Component | Program Role | Ownership |
|---|---|---|
| `systemd/v7-users-autoswitch.timer` | Runtime cycle start | Canonical scheduler |
| `systemd/v7-users-autoswitch.service` | Runtime cycle invocation | Canonical scheduler/service bridge |
| `tools/v7-users-autoswitch` | Runtime program root | Primary runtime/execution/lifecycle terminal owner |
| `v7-user-switch` | Movement primitive | Controlled by autoswitch in normal path |
| `tools/runtime-support/v7-audit-log` | Audit sink | Canonical audit owner |
| `admin/v7-admin-api` | Operator/API/closure/break-glass surface | Operator and closure owner; not primary runtime owner |
| `admin_core/operator_execution.py` | Governance validator | Approval/replay/freshness validator, read-only runtime authority |
| `admin_core/operator_observability.py` | Operation/closure visibility | Read-only operation and closure summary owner |
| `tools/runtime-support/v7-rollback-last-change` | Generic rollback primitive | Break-glass primitive, not normal lifecycle owner |
| Signal tools/timers | Runtime evidence production | Signal-only authority |
| `systemd/drafts/v7-autoswitch-planner.*` | Draft duplicate planner scheduler | DO NOT TOUCH |

## Lifecycle Map

| Lifecycle Stage | Canonical Owner | Output |
|---|---|---|
| Start | systemd autoswitch timer/service | Runtime cycle invoked |
| Operation binding | Autoswitch runtime program | `operation_id` and lineage context |
| Plan | Autoswitch | Candidate plan |
| Select | Autoswitch | selected moves and selected move hash |
| Guard | Autoswitch | restore-barrier/generation/runtime recheck verdict |
| Execute | Autoswitch | movement attempts |
| Verify | Autoswitch | success/failure verification |
| Rollback | Autoswitch rollback branch; generic rollback only as break-glass primitive | rollback outcome |
| Runtime terminal | Autoswitch | completed/failed/rolled_back/denied/no-op terminal verdict |
| Audit | `v7-audit-log` | durable audit record |
| Closure | Admin closure model | VERIFIED/CLOSED/EXPIRED/reopened closure state |

## Operation Map

| Operation Fact | Owner |
|---|---|
| `operation_id` | Canonical semantic identity from Z6.6, bound by Runtime Orchestrator Program |
| `planner_generation_id` | Autoswitch/runtime planning |
| `runtime_snapshot_hash` | Autoswitch/runtime recheck context |
| `selected_move_hash` | Autoswitch selected move ownership |
| `restore_barrier_id` / restore state | Autoswitch restore-barrier lifecycle context |
| `approval_id` / `packet_id` | Admin/operator governance lineage |
| audit identifier | `v7-audit-log` |
| closure key | Admin closure model |
| evidence identifiers | Report/evidence producers, as references only |

## Audit Map

Audit flow:

```text
runtime terminal result
  -> v7-audit-log action/component/object/result metadata
  -> Admin audit search/export/read APIs
  -> operator observability summary
```

Rules:

- `v7-audit-log` is audit truth.
- Admin `audit_admin(...)` is a producer/wrapper, not a new sink.
- Operator execution audit records must map back to `operation_id`.
- Markdown reports are evidence, not audit truth.

## Closure Map

Closure flow:

```text
runtime terminal result
  -> audit present
  -> Admin closure record
  -> operator observability operation summary
  -> CLOSED / VERIFIED / EXPIRED / reopened lineage
```

Rules:

- Closure is not process exit.
- Closure is not stdout.
- Closure is not a markdown report.
- Closure belongs to Admin/operator closure records.

## Rollback Map

Normal rollback:

```text
autoswitch execution failure
  -> autoswitch verification failure
  -> autoswitch rollback branch
  -> runtime terminal rolled_back/failed_closed verdict
  -> audit
  -> closure
```

Break-glass rollback:

```text
operator emergency
  -> generic rollback primitive
  -> operation_id lineage required
  -> audit required
  -> closure required
```

## Break-Glass Map

| Path | Program Classification |
|---|---|
| Admin guarded autoswitch apply | Controlled entry to canonical runtime owner |
| Admin direct user switch | Break-glass; must be audited and closed |
| CLI direct user switch | Break-glass; must be audited and closed |
| Generic rollback apply | Break-glass primitive; must be audited and closed |
| Emergency runtime guard rollback | Break-glass; must be audited and closed |
| Draft planner scheduler | Not break-glass; latent duplicate, DO NOT TOUCH |

