# DEPLOY A Code Deploy

## Deployment

DEPLOY A installed code only from GitHub `v7-next` commit:

`12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`

Installed paths:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/admin_core/*.py`
- `/usr/local/bin/v7-*`

## Service Restart

Restarted only:

`v7-admin-api.service`

No routing service, autoswitch service, VPN tunnel service, policy service, or systemd unit file was changed.

## Installed Code Hashes

- admin API hash: `acbdce035c6f33ad28bd40abb8b76ac1887db9e57f87d696eae98633d760345a`
- `admin_core/operator_execution.py`: `2314798e7a083426c604e6166175423b1097ead0d667d527461e0eecea1b5558`
- `admin_core/operator_observability.py`: `006447583c765570f0c224a17117b0e413e65f10892d70c5212385bd34947f72`
- `admin_core/registry_readers.py`: `f9e85012f989d19c6f67cdf02c8d17a0b492da912bf4597abaeb3ba1c2037166`

These match the local/GitHub `v7-next` checkout.

## Verdicts

- code_deployed=true
- deploy_performed=true
- admin_service_restarted=true
- systemd_changed=false
- runtime_state_overwritten=false
- users_registry_overwritten=false
- egress_registry_overwritten=false
