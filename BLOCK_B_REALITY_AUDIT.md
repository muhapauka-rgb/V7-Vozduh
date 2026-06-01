# Block B Reality Audit

Project: V7 Vozduh

Block: B - Small Batch Program

Date: 2026-06-01

## Scope

Approved batch size: `2`

Selected users:

- `10.7.0.11`
- `10.7.0.12`

Target egress:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`

Rollback egress for both users:

- `1`
- Interface: `v7e356a192b79`

## Fresh Runtime Truth

Truth sources:

- Users registry: `/opt/v7/egress/state/users.registry`
- Egress registry: `/opt/v7/egress/state/egress.registry`
- Audit log: `/opt/v7/audit/operator-execution-audit.jsonl`
- Switch history: `/opt/v7/events/switch-history.jsonl`

Before execution:

- `before_target_count=0`
- `before_source_1_count=10`
- `before_selected_count=0`
- `before_autoswitch_timer=inactive`
- `before_10.7.0.11_current=1`
- `before_10.7.0.12_current=1`
- `before_10.7.0.11_route_table=default dev v7e356a192b79 scope link`
- `before_10.7.0.12_route_table=default dev v7e356a192b79 scope link`

Hashes:

- `before_users_hash=f00a0956230b4f9e7484b5487f1ec5307edda2e1badca99afee6e3c1940fcbf5`
- `before_outside_users_hash=6234ab46ee2198db3b3319651942fef1f8838146f239d17535214c59a9373cf8`
- `before_egress_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `before_selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `before_routes_outside_hash=fe5efd3e8d3833426edd1f8328509c736ec56973632272d341c8bf7770edecdf`
- `before_rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Health

Runtime checkers before Block B were OK:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API health at `127.0.0.1:8017` was unavailable before and after execution with curl rc `7`. No deploy or systemd action was taken to change this.

## Verdict

Fresh reality audit completed.

