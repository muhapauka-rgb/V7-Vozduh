# DEPLOY A Backup Plan

## Backup Target

Backup directory:

`/root/v7-deploy-backups/deploy-a-v7-next-12e51a5-20260601T093725Z`

Deployment metadata directory:

`/opt/v7/ops/deploy-a-v7-next-12e51a5-20260601T093725Z`

## Backed Up

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/admin_core`
- existing `/usr/local/bin/v7-*` tool files
- active `v7-admin-api.service` unit rendering
- V7 service/timer listing before deploy
- code hashes before deploy
- runtime hashes before deploy
- selected moves summary before deploy
- routing snapshots before deploy
- admin health before deploy
- deployment metadata

## Excluded

The backup process did not copy runtime secrets into Git.

Runtime state stayed on the server and was not copied into the repository.

## Verdicts

- backup_ready=true
- backup_created=true
- backup_contains_current_code=true
- backup_contains_runtime_state=false
- secrets_copied_to_git=false
