# Block D1 Enabled Egress Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Registry State

Actual enabled egress rows:

- `vless`
- `awg0`
- `awg3`
- `1`
- `openvpn-1779388847-d2ad7c`
- `wireguard-1779454504-c43409`
- `amneziawg-exec-20260528-10-8-1-14`

## Planner View

Planner sees:

- `egress_total=7`
- `healthy_egress_total=2`

Planner is reading the registry sufficiently to make decisions.

## Safety Review View

Safety review sees:

- `enabled_egress=0`

## Actual Runtime State

Runtime routes and checkers show active, usable egress interfaces.

## Which Component Is Wrong

`v7-autoswitch-safety-review` is wrong for current registry format.

The runtime registry is valid KV format and the planner can read it.

## Verdict

`enabled_egress_issue_understood=true`

