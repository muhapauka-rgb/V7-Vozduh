# Block D0 Reality Audit

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

Mode: Runtime Governance, Capacity Decision, Read-Only Certification

## Scope

Decision only. No user movement, rollback execution, autoswitch apply, rebalance, deploy, routing change, systemd change, or runtime hook authority was performed.

## Current Execution Target

- Target: `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Role: `EXECUTION_ONLY`
- Enabled: `1`
- Manual only: `1`
- Reserve only: `1`
- Autoswitch allowed: `false`
- Rebalance allowed: `false`
- Production assignment allowed: `false`
- Soft limit: `10`
- Hard limit: `10`
- Current count: `10`
- Headroom: `0`

## Current Cohort

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

All ten users are currently assigned to `amneziawg-exec-20260528-10-8-1-14`.

## Fresh Runtime Hashes

- `users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `egress_hash=4e6cce7183353bf5eeb211858112b6ef8a02ba5d6b39a7ef3df6f70c4dc5b805`
- `selected_count=0`
- `selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`
- `routes_all_hash=1f42974ceb4aee43ce1c05a88f50bb5101cbd155aea0c2a7a2b0098acd13cd68`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`
- `audit_count=16`
- `switch_history_count=2750`

## Health

Runtime checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin API health:

- `curl rc=7`
- `127.0.0.1:8017` was not accepting connections.

## Selected Moves

No selected move files were present.

## Verdict

Reality audit complete.

