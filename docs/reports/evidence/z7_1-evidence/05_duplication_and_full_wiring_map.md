# Z7.1 Evidence 05 - Duplication Audit and Full Wiring Map

## Duplication Audit

| Area | Duplicate / Legacy / Dormant Wiring | Risk | Classification |
|---|---|---|---|
| Operation flow | Historical operator `operation_id`, P2.7 candidate operation ids, execution contract ids | MEDIUM | REUSE; do not create a second operation root |
| Lifecycle flow | Autoswitch runtime result, operator historical lineage, execution contract/event preview, closure records | MEDIUM | EXTEND autoswitch lineage into existing audit/closure |
| Audit flow | `v7-audit-log`, Admin `audit_admin`, operator execution append-only audit, security audit/event normalization | MEDIUM | REUSE canonical sink; map producers |
| Closure flow | Admin closure object model plus proposal/evidence default closure states | LOW/MEDIUM | REUSE Admin closure; avoid report/stdout closure truth |
| Rollback flow | Autoswitch rollback branch, generic rollback primitive, Admin rollback apply, Admin direct-switch rollback | HIGH | CONSTRAIN non-autoswitch rollback as break-glass |
| Selected move flow | Autoswitch selected moves, Admin/operator selected move adapters, historical copied selected-move files | MEDIUM | REUSE autoswitch as owner; adapters read-only |
| Restore barrier flow | Autoswitch barrier enforcement, Admin/operator barrier previews | LOW/MEDIUM | REUSE autoswitch as enforcement owner |
| Runtime recheck flow | Autoswitch runtime checks, operator packet recheck | LOW/MEDIUM | Keep operator recheck governance-only |
| Orchestrator wiring | Autoswitch runtime chain, Admin guarded apply, Admin direct switch, draft planner | MEDIUM/HIGH | Reuse autoswitch; constrain bypass/dormant paths |

## Full Wiring Map

```text
Runtime
  tools/v7-users-autoswitch
  status: PARTIAL
  reason: runtime mechanics connected, operation_id missing

  -> Operation
     operation_id
     status: PARTIAL
     reason: connected in operator/governance/historical layers, missing in autoswitch output

  -> Audit
     v7-audit-log / audit_admin / operator execution audit
     status: PARTIAL
     reason: audit sink connected, runtime operation_id audit bridge missing

  -> Closure
     Admin closure store / operator observability
     status: PARTIAL
     reason: closure store connected, autoswitch operation closure bridge missing
```

## Connection Matrix

| Connection | Status | Evidence |
|---|---|---|
| Scheduler -> autoswitch runtime | CONNECTED | systemd autoswitch timer/service from Z6 inventory |
| Autoswitch runtime -> selected moves | CONNECTED | `plan()` returns `selected_moves` |
| Autoswitch runtime -> selected move hash | PARTIAL | hash computed internally for barrier checks; not emitted as canonical operation fact in all cases |
| Autoswitch runtime -> planner generation | CONNECTED internally | `safety.generation.planner_generation_id` |
| Planner generation -> operation_id | MISSING | no autoswitch `operation_id` |
| Autoswitch runtime -> operation_id | MISSING | no `operation_id` in autoswitch |
| Autoswitch execution -> audit | MISSING/PARTIAL | Admin wrapper audits guarded apply; autoswitch itself does not write operation audit |
| Operator packet -> governance audit | CONNECTED | operator execution records include `operation_id` |
| Historical report -> operator operation | CONNECTED | observability derives operation summary from reports |
| Operator operation -> audit export preview | CONNECTED | preview-only |
| Runtime operation -> closure | MISSING | closure accepts `runtime` object type, but autoswitch does not provide object id |
| Admin closure -> audit | CONNECTED | closure-set calls `audit_admin` |
| Autoswitch rollback -> operation_id | MISSING | rollback result lacks operation id |
| Generic rollback -> audit | CONNECTED | primitive calls `v7-audit-log` |
| Generic rollback -> operation_id | MISSING | no operation lineage |
| Operator recheck -> operation_id | PARTIAL | packet can include operation id; not autoswitch runtime |
| Restore barrier -> operation_id | MISSING | barrier has generation/selected move facts, no operation id |

## Would Planned Wiring Duplicate Existing Wiring?

Planned wiring would duplicate existing implementation only if it creates:

- a new operation identity,
- a new audit sink,
- a new closure store,
- a new selected-move owner,
- a new rollback owner,
- a new runtime recheck owner,
- a new runtime orchestrator.

Planned wiring would not duplicate existing implementation if it only:

- adds `operation_id` to autoswitch-owned runtime output,
- links existing autoswitch facts to existing `operation_id`,
- sends existing runtime terminal facts to existing `v7-audit-log`,
- lets existing Admin closure close existing runtime operation ids.

## Truth Source Verdict

No duplicate truth source must be created. Existing truth sources are usable but not yet fully wired together.

