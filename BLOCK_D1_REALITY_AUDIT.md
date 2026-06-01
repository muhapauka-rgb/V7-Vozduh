# Block D1 Reality Audit

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

Mode: analysis only

## Scope

No runtime mutation was performed.

No users were moved.

No rollback, autoswitch apply, rebalance, policy apply, deploy, systemd change, git push, or git merge was performed.

## Current Runtime

Execution target:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Current users: `10`
- Soft limit: `10`
- Hard limit: `10`
- Headroom: `0`

Execution cohort:

- `10.7.0.2`
- `10.7.0.3`
- `10.7.0.4`
- `10.7.0.5`
- `10.7.0.6`
- `10.7.0.8`
- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.14`
- `10.7.0.15`

## Registry Reality

Actual enabled egress rows in `/opt/v7/egress/state/egress.registry`:

- `vless`
- `awg0`
- `awg3`
- `1`
- `openvpn-1779388847-d2ad7c`
- `wireguard-1779454504-c43409`
- `amneziawg-exec-20260528-10-8-1-14`

Actual enabled egress count: `7`

## Runtime Hashes

- `users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `egress_hash=4e6cce7183353bf5eeb211858112b6ef8a02ba5d6b39a7ef3df6f70c4dc5b805`
- `selected_count=0`
- `selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `routes_all_hash=1f42974ceb4aee43ce1c05a88f50bb5101cbd155aea0c2a7a2b0098acd13cd68`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Shadow Planner

Read-only shadow run:

- `apply_requested=false`
- `candidate_moves=12`
- `selected_moves=0`
- `action_counts={"keep":6,"switch":12}`
- `move_type_counts={"failover":12,"none":6}`

## Safety Review

Safety review:

- `status=critical`
- Critical finding: no enabled egress found for active users

## Health

Runtime checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API:

- unavailable at `127.0.0.1:8017`

## Verdict

Reality audit complete.

