# DEPLOY A Rollback Plan

## Rollback Target

Rollback target is the previous server code captured in:

`/root/v7-deploy-backups/deploy-a-v7-next-12e51a5-20260601T093725Z/usr-local-bin`

## Rollback Scope

Rollback is code-only:

- restore `/usr/local/bin/v7-admin-api`
- restore `/usr/local/bin/admin_core`
- restore relevant `/usr/local/bin/v7-*` files if needed
- restart only `v7-admin-api.service` if admin health requires it

## Preserved During Rollback

Rollback must not modify:

- `/opt/v7/egress/state`
- `users.registry`
- `egress.registry`
- runtime state files
- logs/events
- client profiles
- routing tables
- autoswitch state
- policy state

## Rollback Execution

Rollback was not executed because post-deploy health passed.

## Verdicts

- rollback_ready=true
- rollback_executed=false
- rollback_scope_code_only=true
