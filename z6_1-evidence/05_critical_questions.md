# Z6.1 Critical Questions

## Q1. What currently starts the runtime cycle?

For autoswitch movement, `systemd/v7-users-autoswitch.timer` starts the cycle by invoking `v7-users-autoswitch.service`, which runs `/usr/local/bin/v7-users-autoswitch --apply`.

Supporting signal cycles are started by `v7-telegram-sentinel.timer`, `v7-service-matrix-refresh.timer`, and `v7-egress-quality-compact.timer`.

## Q2. What currently ends the runtime cycle?

There is no unified runtime-cycle closure owner. The autoswitch command exits after plan/apply and prints JSON. Terminal states include dry-run, autoswitch disabled, observe mode, no selected moves, applied results, verify failure rollback results, and safety/reconnect state writes. No global execution contract completion record is written by the active autoswitch cycle.

## Q3. Who owns planner execution?

`tools/v7-users-autoswitch` owns autoswitch planner execution. Admin can invoke it for dry-run or guarded apply, but the planner logic lives in the tool.

No generic P2 execution-contract planner has runtime execution authority.

## Q4. Who owns selected moves?

For autoswitch runs, selected moves are generated in `tools/v7-users-autoswitch.plan()`. Admin/operator read adapters inspect `selected-moves.json`, `autoswitch-selected-moves.json`, and historical copies, but a single active selected-move truth writer was not identified in the local scan.

## Q5. Who owns restore barrier generation?

No singular active restore-barrier generation owner was identified in the local code scan. `tools/v7-users-autoswitch` owns restore-barrier enforcement and Admin/observability own read adapters. Generation/write/closure ownership remains partial and must be resolved before implementation.

## Q6. Who owns runtime recheck?

`admin_core/operator_execution.runtime_recheck()` owns zero-move packet runtime recheck. Admin execution/readiness surfaces also provide read-only adapter checks for selected moves and restore settle. There is no general movement-capable, contract-bound runtime recheck executor.

## Q7. Who owns execution?

Execution is split:

- Autoswitch execution: `tools/v7-users-autoswitch --apply`.
- Admin manual movement: `/api/actions/user-switch` -> `v7-user-switch`.
- Admin autoswitch execution: `/api/actions/autoswitch-apply-guarded` -> `v7-users-autoswitch --mode guarded --apply`.
- Generic rollback execution: `/api/actions/rollback-apply` -> `v7-rollback-last-change --apply`.
- P2 execution contracts: read-only foundation, no execution authority.

## Q8. Who owns rollback?

Rollback is split:

- `tools/v7-users-autoswitch` owns immediate rollback-on-verify-fail for moves it just applied.
- Admin manual user switch owns rollback to previous egress if proxy runtime switching fails.
- `tools/runtime-support/v7-rollback-last-change` owns broad latest-backup rollback when called with `--apply`.
- Admin execution rollback views are read-only summaries.

## Q9. Who owns audit completion?

No single audit completion owner exists. Audit is written by Admin action audit, `tools/runtime-support/v7-audit-log`, `admin_core/operator_execution.py`, and event writers such as Telegram sentinel. There is no unified run envelope that closes the lifecycle across plan, approval, apply, verify, rollback, and completion.

## Q10. Can any component bypass the intended governance path?

Yes. Admin manual user switch can move a user without a P2 execution contract. Admin autoswitch apply can invoke the autoswitch mini-orchestrator with confirmation. The active systemd autoswitch timer can run movement-capable cycles. Generic rollback can restore broad file targets. Telegram sentinel has a latent direct autoswitch launch path if invoked without `--no-autoswitch`, although the production unit uses `--no-autoswitch`.

## Final Verdict Inputs

existing_full_orchestrator=false

existing_partial_orchestrator=true

closest_orchestrator_candidate=tools/v7-users-autoswitch plus systemd/v7-users-autoswitch.timer/service

duplicate_authority_risk=HIGH

manual_bypass_risk=HIGH

safe_to_continue_to_Z6_2=true

Condition: Z6.2 must continue from DISCOVER -> REUSE -> EXTEND -> MERGE -> IMPLEMENT and must not create a parallel executor, duplicate scheduler, duplicate selected-move truth source, or duplicate restore-barrier lifecycle owner.
