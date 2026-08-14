# Z7.1 Evidence 00 - Discovery Inventory

Program: PROGRAM Z7.1 - Ownership Wiring Reality Audit  
Project: V7 Vozduh  
Branch target: v7-next  
Mode: READ ONLY reality audit

## Gate Result

The Z6 architecture truths were re-used only as audit anchors. No implementation planning was performed before inventory.

Established anchors checked against working code:

| Anchor | Expected Owner | Reality Status |
|---|---|---|
| Runtime owner | `tools/v7-users-autoswitch` | CONNECTED for planning/apply/verify/rollback mechanics; MISSING for `operation_id` wiring |
| Scheduler | `systemd/v7-users-autoswitch.timer/service` | CONNECTED |
| Audit owner | `tools/runtime-support/v7-audit-log` | CONNECTED as audit sink; PARTIAL for operation lineage |
| Closure owner | `admin/v7-admin-api` + `admin_core/operator_observability.py` | CONNECTED for Admin closure objects; PARTIAL for runtime operation closure |
| Canonical operation | `operation_id` | CONNECTED in operator/governance/historical surfaces; MISSING in autoswitch runtime output |
| Runtime Orchestrator Program | autoswitch-centered chain | PARTIAL in code |

## Major Components

| Component | Wiring Found | Status | Classification |
|---|---|---|---|
| `tools/v7-users-autoswitch` | Plans selected moves, computes `planner_generation_id`, computes selected move hash, checks restore barrier, applies moves, verifies routes, rolls back on verify failure, prints JSON plan/result | PARTIAL | REUSE, EXTEND |
| `systemd/v7-users-autoswitch.timer/service` | Active scheduler/service chain for autoswitch runtime cycle | CONNECTED | REUSE |
| `tools/runtime-support/v7-audit-log` | Writes canonical audit JSONL with `request_id`, object fields, metadata, before/after hashes | CONNECTED audit sink, PARTIAL operation linkage | REUSE, EXTEND |
| `admin/v7-admin-api` autoswitch actions | Dry-run and guarded apply call `v7-users-autoswitch`; Admin audits action wrapper | PARTIAL | REUSE, EXTEND |
| `admin/v7-admin-api` direct user switch | Directly calls `v7-user-switch`, may rollback manually on proxy failure | DUPLICATED execution path | REUSE, CONSTRAIN |
| `admin/v7-admin-api` rollback apply | Calls `v7-rollback-last-change --apply` and audits Admin action | DUPLICATED rollback path | REUSE, CONSTRAIN |
| `admin/v7-admin-api` closure model | `closure-records.jsonl`, `closure_set_response`, closure metadata on evidence/proposal/runtime/release/trust/drift | CONNECTED closure store, PARTIAL operation closure | REUSE, EXTEND |
| `admin_core/operator_execution.py` | Validates approval packet, performs read-only runtime recheck, writes append-only audit/governance records with `operation_id`, `approval_id`, `packet_id` | CONNECTED governance wiring, not runtime movement | REUSE, EXTEND |
| `admin_core/operator_observability.py` | Builds historical operation summaries from `BLOCK_*.md`, exposes `operation_id`, evidence refs, audit export preview, governance preview, rehearsal preview | CONNECTED historical/operator preview wiring | REUSE |
| Admin execution contract/event store | `contract_id`, `event_id`, proposal references, read-only/non-authoritative execution contracts/events | PARTIAL/LEGACY for runtime orchestrator | REUSE, DO NOT PROMOTE AS RUNTIME OWNER |
| Selected move adapters | Admin/operator read adapters inspect state files and historical copies | PARTIAL/DORMANT if live state file missing | REUSE, EXTEND |
| Restore barrier adapters | Autoswitch and Admin/operator read `autoswitch-restore-barrier.json` | PARTIAL | REUSE, EXTEND |
| `tools/runtime-support/v7-rollback-last-change` | Generic rollback primitive writes audit action `rollback_last_change` when applied | CONNECTED primitive, MISSING operation lineage | REUSE, CONSTRAIN |
| `systemd/drafts/v7-autoswitch-planner.*` | Draft scheduler path from Z6.7 | DORMANT duplicate risk | DO NOT TOUCH |

## Primary Reality Finding

The runtime mechanics exist, and the operator/governance operation model exists, but the working autoswitch runtime cycle does not yet carry the canonical `operation_id` through runtime output, audit, closure, rollback, restore barrier, or recheck.

Therefore the end-to-end Runtime Orchestrator Program wiring is:

```text
Runtime -> Operation -> Audit -> Closure
PARTIAL -> PARTIAL -> PARTIAL -> PARTIAL
```

Not:

```text
Runtime -> Operation -> Audit -> Closure
CONNECTED -> CONNECTED -> CONNECTED -> CONNECTED
```

