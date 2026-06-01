# DEPLOY A Certification

## Certification

DEPLOY A completed successfully.

## Required Verdicts

- server_code_current=true
- runtime_state_preserved=true
- users_preserved=true
- channels_preserved=true
- routing_preserved=true
- autoswitch_not_applied=true
- p5_runtime_truth_available=true
- safe_to_rerun_p5=true

## Safety Verdict

- users_moved=false
- routing_changed=false
- autoswitch_apply_run=false
- policy_apply_run=false
- killswitch_changed=false
- trusted_ru_changed=false
- direct_ru_changed=false
- runtime_action_executed=false
- rollback_executed=false
- runtime_state_overwritten=false
- users_registry_overwritten=false
- egress_registry_overwritten=false
- deploy_performed=true
- systemd_changed=false

## Notes

Only `v7-admin-api.service` was restarted to activate the updated admin code.

No systemd unit files were changed.
