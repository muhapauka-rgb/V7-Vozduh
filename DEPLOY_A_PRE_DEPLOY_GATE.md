# DEPLOY A Pre-Deploy Gate

## Gate Checks

- package hash verified: true
- runtime state path exists: true
- users registry exists: true
- egress registry exists: true
- admin health before deploy: true
- runtime hashes captured: true
- selected moves captured: true
- routing baseline captured: true
- backup ready: true
- rollback ready: true
- v7-next hash known: true
- server current code hash known: true

## First Attempt Note

An initial deploy script attempt stopped during precheck because the read-only selected-moves helper had a Python syntax error.

That attempt did not reach install or service restart.

The corrected script passed the pre-deploy gate and proceeded.

## Verdicts

- pre_deploy_gate_passed=true
- backup_ready=true
- rollback_ready=true
- runtime_audit_before_complete=true
- selected_moves_protection_required=false
