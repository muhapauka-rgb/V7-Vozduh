# P6 Target Readiness

Project: V7 Vozduh

Block: P6

## Readiness Command

`v7-second-canary-target-readiness --state-dir /opt/v7/egress/state --candidate-user 10.7.0.11 --current-egress 1 --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty`

## Result

- candidate_user: `10.7.0.11`
- candidate_still_valid: true
- current_egress: `1`
- execution_only_mode: true
- execution_target_id: `amneziawg-exec-20260528-10-8-1-14`
- selected_target: `amneziawg-exec-20260528-10-8-1-14`
- approval_status: `GO`
- second_canary_readiness: `GO`
- runtime_commands_executed: false
- execution_allowed_now: false

## Target State

- target users before movement: `0`
- target interface: `v7execwg0`
- target readiness: `GO`

## Verdict

- target_ready=true
- candidate_still_valid=true
- approval_status_go=true
- second_canary_readiness_go=true
