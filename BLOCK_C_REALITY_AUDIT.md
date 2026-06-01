# Block C Reality Audit

Project: V7 Vozduh

Block: C - Blast Radius Expansion Program

Date: 2026-06-01

## Runtime Source

Artifacts:

- `/tmp/block-c-blast-radius-20260601T143750Z/reality_audit.env`
- `/tmp/block-c-blast-radius-20260601T143750Z/admin_health_initial.json`

Canonical runtime sources:

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/audit/operator-execution-audit.jsonl`
- `/opt/v7/events/switch-history.jsonl`

## Initial State

- `initial_target_count=2`
- `initial_rollback_count=8`
- `initial_selected_count=0`
- `initial_autoswitch_timer=inactive`
- `initial_audit_count=14`
- `initial_switch_history_count=2742`

Initial target users:

- `10.7.0.11`
- `10.7.0.12`

Initial rollback candidates on egress `1`:

- `10.7.0.3`
- `10.7.0.4`
- `10.7.0.5`
- `10.7.0.2`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.14`
- `10.7.0.15`

## Initial Hashes

- `initial_users_hash=0c8a625da1e572f49247b87c95d1188a98f02fb079be01f0a7ef6ad599ed3d4d`
- `initial_outside_scope_hash=f06aedcc6e8459553f14c2e110409e36cb4bc50c60979968de9649b78c0647cb`
- `initial_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `initial_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `initial_routes_outside_scope_hash=0c7a2021bf63faff31ff6970fa72c2ad2ef776ca6a4c7f9510df81e01417b12a`
- `initial_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Health

Runtime checkers passed before Block C:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API health at `127.0.0.1:8017` was unavailable with curl rc `7`.

## Verdict

Reality audit completed. Runtime health was sufficient for governed movement; admin API health remained a blocker risk.

