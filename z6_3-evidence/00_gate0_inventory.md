# PROGRAM Z6.3 Gate 0 Inventory

Project: V7 Vozduh
Program: Z6.3 - Runtime Ownership Consolidation Audit
Mode: READ ONLY
Date: 2026-06-02

## Constraint

This file inventories existing ownership and ownership suitability only. It does not design, implement, refactor, deploy, restart, mutate routing, move users, modify systemd, clean up, merge, or push.

## Z6.1/Z6.2 Baseline Reused

- existing_full_orchestrator=false
- existing_partial_orchestrator=true
- closest existing partial orchestrator=`tools/v7-users-autoswitch` + `systemd/v7-users-autoswitch.timer/service`
- runtime_cycle_fully_understood=true
- duplicate_authority_risk=HIGH
- manual_bypass_risk=HIGH
- safe_to_continue_to_Z6_3=true

## Component Classification

| Component | Current Ownership | Z6.3 Suitability | Classification |
|---|---|---|---|
| `tools/v7-users-autoswitch` | Planner, selected moves, restore-barrier enforcement, autonomous apply, verify, local rollback, safety/reconnect/load writes | Strongest existing candidate for primary runtime and execution ownership | REUSE / EXTEND |
| `systemd/v7-users-autoswitch.timer/service` | Autonomous runtime scheduler and command launcher | Should remain scheduler-only; not lifecycle owner | REUSE |
| `v7-user-switch` | Low-level route/user movement primitive | Should remain execution primitive behind the runtime owner, not independent lifecycle authority | REUSE / REFACTOR LATER |
| `admin/v7-admin-api` mutating action endpoints | Manual autoswitch apply, direct user switch, rollback apply, closure setting, audit wrapper | Should become operator surface/secondary owner, not primary runtime owner | REUSE / EXTEND |
| `admin/v7-admin-api` execution contract APIs | Preview-only contracts, validation, rollback preview, event views | Should remain read/validation/governance surface until intentionally connected | REUSE / EXTEND |
| `admin_core/operator_execution.py` | Zero-move packet runtime recheck and append-only governance record | Should support runtime admission/recheck, but currently cannot own movement execution | REUSE / EXTEND |
| `admin_core/operator_observability.py` | Historical operation timeline, audit export preview, governance/rehearsal previews | Strong supporting owner for closure/audit evidence, not executor | REUSE / EXTEND |
| `tools/v7-telegram-sentinel` | Fast Telegram signal writer; latent autoswitch trigger | Should be advisory/signal-only; production unit already uses `--no-autoswitch` | REUSE / REFACTOR LATER |
| `tools/v7-service-matrix-refresh-all` | Service health refresh evidence | Supporting signal owner | REUSE |
| `tools/v7-egress-quality-compact` | Historical quality compaction | Supporting signal owner | REUSE |
| `tools/v7-restore-settle-gate` | Restore-settle evidence classifier | Supporting validation/evidence owner | REUSE |
| `tools/runtime-support/v7-rollback-last-change` | Generic latest-backup rollback | Strongest current low-level rollback primitive, but too broad to be primary lifecycle owner alone | REUSE / REFACTOR LATER |
| `tools/runtime-support/v7-audit-log` | Generic audit event sink | Strongest existing primary audit sink candidate | REUSE / EXTEND |
| Persistent selected-move files/adapters | Multiple read conventions; no canonical live writer | Should not become duplicate selected-move truth without consolidation | REFACTOR LATER |
| `autoswitch-restore-barrier.json` lifecycle | Enforcement consumed by autoswitch; creation/closure fragmented | Should be owned by runtime owner with Admin evidence/closure support | REFACTOR LATER |
| `systemd/drafts/v7-autoswitch-planner.*` | Draft scheduler/planner timer path | Should not be activated or treated as owner in this audit | DO NOT TOUCH |
| New orchestrator/scheduler/planner/execution path | None | Forbidden by Z6.3 | REPLACE = NO |

## Existing Authority Summary

| Authority | Current Holder(s) | Suitability Result |
|---|---|---|
| Runtime owner | Autoswitch partial owner; Admin/manual paths conflict | Primary candidate: `tools/v7-users-autoswitch`. |
| Scheduler | systemd autoswitch timer | Keep scheduler-only. |
| Signals | service matrix, sentinel, quality, health/state tools | Keep as distributed supporting owners. |
| Policy | policy files via operator/Admin | Keep as hard policy authority; runtime owner must consume, not replace. |
| Proposal | Admin generated proposals and historical packets | Keep as operator/governance input, not runtime authority. |
| Selected moves | Autoswitch in-process selected moves | Primary candidate: `tools/v7-users-autoswitch`. |
| Restore barrier | Autoswitch enforcement; lifecycle fragmented | Primary candidate should be runtime owner; Admin supports visibility/closure. |
| Runtime recheck | Autoswitch path-local, operator zero-move, Admin preview gates | Consolidation needed around runtime owner with supporting Admin/operator gates. |
| Execution | Autoswitch, Admin direct switch, CLI primitive | Primary candidate: `tools/v7-users-autoswitch`; direct/manual paths should lose independent lifecycle authority later. |
| Verification | Autoswitch path-local; Admin endpoint verification | Primary candidate: runtime owner; Admin supports visibility. |
| Rollback | Autoswitch local, Admin, generic rollback tool | Primary candidate: `tools/v7-users-autoswitch` for movement lifecycle, supported by `v7-rollback-last-change` for broad rollback. |
| Audit | Admin audit, `v7-audit-log`, operator execution audit, event JSONL | Primary audit sink candidate: `v7-audit-log`; Admin/operator are secondary surfaces. |
| Closure | Admin closure records and operator observability; no runtime cycle closer | Primary closure candidate: Admin/operator observability closure layer backed by audit sink, with runtime owner supplying final outcome. |

