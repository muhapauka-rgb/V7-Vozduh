# P6 Rollback Readiness

Project: V7 Vozduh

Block: P6

## Rollback Scope

Rollback path:

`10.7.0.11 -> 1`

Rollback was not executed.

## Rollback Preview

Read-only rollback preview after movement:

- mutation: false
- runtime_commands_executed: false
- errors: `[]`
- warnings: `[]`
- user: `10.7.0.11`
- from egress: `amneziawg-exec-20260528-10-8-1-14`
- to egress: `1`
- route table: `1009`
- target interface for rollback: `v7e356a192b79`
- route would change: `ip route replace default dev v7e356a192b79 table 1009`

## Verification Requirements

If rollback is authorized in a later block, verify:

- `10.7.0.11 current=1`
- table `1009` uses `v7e356a192b79`
- target users on execution egress returns to `0`
- users outside scope remain unchanged
- selected moves remain `0`
- checkers remain `OK`

## Verdict

- rollback_ready=true
- rollback_executed=false
