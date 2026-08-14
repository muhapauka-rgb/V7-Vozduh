# Bounded Autonomy Readiness Evidence: Ownership And Boundary

Дата: 2026-06-08

## Existing Owners

- Planner: `tools/v7-users-autoswitch`
- Approval packet tool: `tools/v7-operator-execution-packet`
- Packet / restore-barrier owner: `admin_core/operator_execution.py`
- Runtime apply executor: `tools/v7-users-autoswitch --apply --verify`
- Rollback executor: `tools/v7-users-autoswitch --rollback-packet --apply --verify`
- Feedback owner: `admin_core/operator_execution_feedback.py`
- Observability owner: `admin_core/operator_observability.py`
- Operator decision surface: `admin_core/operator_decision_surface.py`

## Evidence From Code

- `admin_core/operator_execution_pipeline.py` says autonomy may produce recommendation candidates only and must reuse the same packet, recheck, restore barrier, rollback packet, governed apply, audit and closure.
- `admin_core/operator_execution_pipeline.py` safety model forbids automatic execution, direct user switch, apply without packet, apply without restore barrier, second planner, second truth source and second execution path.
- `admin_core/operator_decision_surface.py` is read-only: it does not plan, approve, execute, rollback or write runtime state.
- `admin_core/operator_execution_feedback.py` is pure: it builds feedback records and does not execute movement, approve governance, create snapshot roots or call runtime tools.
- `admin_core/operator_execution.py` can write restore-barrier clearance for an approved packet, but lifecycle records explicitly set `user_movement=false`, `routing_mutation=false`, `autoswitch_apply=false`.
- `tools/v7-users-autoswitch` authority promotion requires explicit confirmation, truth check, evidence review and audit; promotion result keeps `users_moved=0` and `autoswitch_apply_run=false`.

## Boundary

Current platform supports:

- read-only shadow autonomy,
- autonomous summaries/explanations,
- autonomous recommendation proposals,
- operator approval workflow.

Current platform does not yet certify:

- automatic live apply,
- automatic rollback execution,
- production autonomy,
- autonomy promotion.

