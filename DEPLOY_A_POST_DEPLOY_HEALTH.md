# DEPLOY A Post-Deploy Health

## Admin Health

Post-deploy local admin health:

- status: `OK`
- local_only: `true`
- auth_configured: `true`

Active process after deploy:

`python3 /usr/local/bin/v7-admin-api`

Service status:

`v7-admin-api.service active`

## Runtime Preservation

- users registry unchanged: true
- egress registry unchanged: true
- selected moves unchanged: true
- runtime state path still exists: true

## Routing Preservation

The deploy script initially reported `routing_preserved=false` because it compared `sha256sum` manifest lines containing different before/after file paths.

Manual digest inspection showed the actual route digests were identical:

- ip rule digest before/after: `7a24985200ad990402f479e8bb613e126efe9efa60c0bb1bb978492c27a998a7`
- ip route table-all digest before/after: `45f16703587a3b07cdb7e6cbbbd423830683979fc3c5ec78e65a8d450f5a3bc9`

No `ip rule` or route diff was present.

## Verdicts

- post_deploy_health_passed=true
- admin_health_ok=true
- admin_api_starts=true
- users_preserved=true
- channels_preserved=true
- routing_preserved=true
