# Block D Reality Audit

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

Mode: Discovery, Certification, Shadow Operation, Operator Approved Execution

## Scope

No autonomous execution was enabled.

No autoswitch apply was run.

No user movement, deploy, systemd change, routing change, or runtime hook authority was performed.

## Existing Functionality Found

Repository and runtime already contain autoswitch and governance functionality:

- `v7-users-autoswitch`
- `v7-autoswitch-safety-review`
- `v7-route-movement-preview`
- `v7-operator-execution-packet`
- `v7-second-canary-target-readiness`
- `admin_core/operator_execution.py`
- `admin_core/operator_observability.py`
- `systemd/v7-users-autoswitch.service`

Runtime autoswitch timer:

- `v7-autoswitch.timer=inactive`

## Runtime State

Execution target:

- `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Count: `10`
- Hard limit: `10`
- Headroom: `0`

Selected moves:

- `selected_count=0`
- `selected_hash=7023312b1b17c2e59cc4b596f9715c68a364be3d837a8bfdf816b63006c2216d`

Runtime hashes:

- `users_hash=600ca744661e76ddb4d77098b7faedb333b4cd3f6daa2027de104939a88e165b`
- `egress_hash=4e6cce7183353bf5eeb211858112b6ef8a02ba5d6b39a7ef3df6f70c4dc5b805`
- `routes_all_hash=1f42974ceb4aee43ce1c05a88f50bb5101cbd155aea0c2a7a2b0098acd13cd68`
- `rules_hash=200fc826c0f26d7e05ff11ef7600d3c9141f9ebe3b084c68946ceb825b1d9ac4`

## Health

Runtime checkers:

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

Admin health:

- `127.0.0.1:8017` unavailable, curl rc `7`

## Verdict

Reality audit complete. Existing implementation must be reused; no parallel autoswitch system is justified.

