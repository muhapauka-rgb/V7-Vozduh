# Production Validation

Read-only production validation:

- `grep '^ip=10.0.0.2 ' /opt/v7/egress/state/users.registry`
- Result: `ip=10.0.0.2 current=vless table=100 enabled=1`

Read-only production baseline dry-run before deploying this gate:

- `selected_move_count=0`
- `authority_budget_gate=null`
- `apply_requested=false`

Interpretation:

- the previously certified one-user movement remains present;
- this program did not move users;
- this program did not run autoswitch apply;
- the authority gate is implemented locally and must be deployed before it becomes production-active.

