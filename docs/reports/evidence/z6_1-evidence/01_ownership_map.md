# Z6.1 Ownership Map

## Component Classification

| Component | Existing Ownership | Classification | Notes |
|---|---|---|---|
| `tools/v7-users-autoswitch` | Planner, selected move selection, autoswitch apply, restore-barrier enforcement, anti-flap state, immediate verify rollback | REUSE + EXTEND | Closest existing Runtime Orchestrator candidate. Do not replace or duplicate. Later work should wrap/coordinate this path. |
| `systemd/v7-users-autoswitch.timer` + service | Runtime scheduling for recurring autoswitch apply | REUSE | Active scheduler starts a movement-capable cycle every 20 seconds. Any orchestrator design must not create a second uncoordinated scheduler. |
| `admin/v7-admin-api` action endpoints | Operator/admin/owner action runner; direct autoswitch, user-switch, rollback wrappers; audit writer | REUSE + EXTEND | Existing high-authority control plane. Later orchestration must integrate with action authorization and audit instead of bypassing it. |
| `admin/v7-admin-api` execution APIs | Read-only execution contract/event/readiness surfaces | EXTEND | Contains execution-state vocabulary but explicitly cannot execute proposals or mutate runtime. |
| `admin_core/operator_execution.py` | Zero-move packet validation, runtime recheck, append-only audit/governance records | EXTEND | Useful governance/recheck model, but authority is intentionally not movement-capable. |
| `admin_core/operator_observability.py` | Read-only operator workflow, approval preview, rehearsal, selected moves/barrier summaries | REUSE | Advisory/read surface. No runtime execution authority. |
| `tools/v7-telegram-sentinel` + timer/service | Fast Telegram signal writer; production mode disables autoswitch launch | REUSE | Production unit is signal-only, but binary has latent direct autoswitch launch path if run without `--no-autoswitch`. |
| `tools/v7-service-matrix-refresh-all` + timer/service | Service health signal writer | REUSE | Supporting scheduler/state writer for autoswitch decisions. |
| `tools/v7-egress-quality-compact` + timer/service | Historical quality summary writer | REUSE | Supporting signal; should remain subordinate to planner/safety policy. |
| `tools/runtime-support/v7-rollback-last-change` | Generic latest-backup rollback apply | REFACTOR LATER | Existing rollback authority is broad and not contract-scoped. Do not touch in Z6.1. Later work should bound it behind orchestration/contract semantics. |
| `tools/runtime-support/v7-audit-log` | Generic audit JSONL writer | REUSE | Existing shared audit sink. Completion semantics are distributed, not unified. |
| `tools/v7-restore-settle-gate` | Read-only restore settle classifier | REUSE | Gate/recheck support only; no runtime authority. |
| `tools/v7-second-canary-target-readiness` | Read-only target readiness checker | REUSE | Read-only readiness support only; no runtime authority. |
| `systemd/drafts/v7-autoswitch-planner.*` | Draft read-only planner scheduler | DO NOT TOUCH | Draft/stale scheduler candidate. Should not be activated or duplicated during audit. |
| `systemd/drafts/v7-health.service` | Draft health ordering dependency | DO NOT TOUCH | Draft/stale health service. Not an active execution owner from local evidence. |

## Ownership By Required Category

| Category | Current Owner(s) | Ownership Status |
|---|---|---|
| Runtime execution authority | `v7-users-autoswitch --apply`, Admin `/api/actions/user-switch`, Admin `/api/actions/autoswitch-apply-guarded`, Admin `/api/actions/rollback-apply`, manual CLI tools if available | Split |
| Planner authority | `tools/v7-users-autoswitch` | Central for autoswitch, absent for generic execution contracts |
| Rollback authority | `v7-users-autoswitch` immediate verify rollback, Admin rollback endpoint, `v7-rollback-last-change`, Admin manual switch rollback | Split |
| Governance authority | Admin role/CSRF model, `operator_execution.py`, `operator_observability.py`, control-plane governance docs/checker | Split/read-only for packet path |
| Restore-barrier lifecycle | `v7-users-autoswitch` reads/enforces; Admin/read adapters observe; writer not singular in active local code scan | Partial/orphan writer risk |
| Execution lifecycle | `v7-users-autoswitch` owns one autoswitch run; Admin execution APIs model future lifecycle read-only | Partial |
| Runtime scheduling | systemd timers for autoswitch, Telegram sentinel, service matrix, quality compact; draft planner timer exists | Split |
| Runtime state transitions | Autoswitch writes safety/reconnect/load; sentinel writes sentinel/matrix/events; Admin writes many action states; rollback restores broad file targets | Split |

## Gate 0 Verdict

A partial Runtime Orchestrator already exists. The strongest existing ownership chain is:

`systemd/v7-users-autoswitch.timer` -> `systemd/v7-users-autoswitch.service` -> `tools/v7-users-autoswitch.plan()` -> selected moves -> `tools/v7-users-autoswitch.apply()` -> `v7-user-switch` -> verification -> immediate rollback-on-verify-fail -> safety/reconnect state writes.

This chain must be reused and coordinated before any new runtime-orchestrator architecture is considered.
