# Block B Runtime Audit

Project: V7 Vozduh

Block: B - Small Batch Program

Date: 2026-06-01

## Captured Runtime Hashes

- `users_registry_hash=f00a0956230b4f9e7484b5487f1ec5307edda2e1badca99afee6e3c1940fcbf5`
- `egress_registry_hash=09a9234fa7ac9310d289e2b8e1e2b4f62d8926339ed610b09360c0a3cb626eb0`
- `selected_moves_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `routes_outside_scope_hash=fe5efd3e8d3833426edd1f8328509c736ec56973632272d341c8bf7770edecdf`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Runtime Health

Runtime health checkers passed:

- `v7-user-route-check`
- `v7-killswitch-check`
- `v7-provisioning-reconcile-check`

Admin API health was unavailable with curl rc `7`.

## Capacity And Trust

Target:

- `amneziawg-exec-20260528-10-8-1-14`
- Enabled: `1`
- Interface: `v7execwg0`
- Hard limit: `10`
- Users before Block B: `0`
- Users after Block B: `2`

The target was execution-reserved and manual-only, so it was appropriate only for operator-governed batch certification.

## Verdict

Runtime audit completed. Runtime movement was bounded to the packet scope.

