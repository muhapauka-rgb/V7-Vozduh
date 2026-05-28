# E8.4 Evidence Index

Block: E8.4.

Mode: bounded live deploy.

Live mutation was limited to the approved systemd split.

## Evidence Files

```text
pre-deploy.txt
pre-deploy-process-guard.txt
backup-manifest.txt
deploy-output.txt
post-deploy-authority.txt
post-deploy-process-guard-clean.txt
post-deploy-safety.txt
```

## Runtime Backup Location

```text
/root/v7-e84-systemd-split-20260525T123450Z/backups/
```

## Result Summary

```text
deploy_success=true
rollback_performed=false
v7-health.service_health_only=true
planner_authority_separated=true
apply_authority_unchanged=true
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
kill_switch_ok=true
user_route_check_ok=true
provisioning_reconcile_ok=true
reconcile_result_after_deploy=FAIL
```
