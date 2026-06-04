# AUTONOMY_READINESS_MODEL

Status: PASS

Implementation:

- `autonomy_readiness_model`

Levels:

- NOT_READY
- SHADOW_READY
- OPERATOR_VISIBLE_READY
- OPERATOR_APPROVAL_READY
- BOUNDED_AUTONOMY_READY
- PRODUCTION_AUTONOMY_READY

Boundary:

- Autonomy remains disabled.
- Automatic user movement remains disabled.
- Planner authority remains unchanged.
- Governance remains unchanged.
- Execution remains unchanged.

RI6 can only report readiness. It cannot grant authority.

