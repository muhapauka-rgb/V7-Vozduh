# P5.1 Action Compatibility Review

## P5 Requirements

P5 needs these fresh values before packet creation and runtime recheck:

- users registry hash
- egress registry hash
- selected moves hash
- runtime snapshot hash

## Compatibility With Existing Implementation

The existing implementation can produce all required values if it receives a live `state_dir` containing:

- `users.registry`
- `egress.registry`
- current selected moves source or no selected-move file when zero is valid

## Current Environment

The current environment cannot provide these values from live runtime truth.

Missing:

- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/egress.registry`
- `/opt/v7/egress/state/v7-state.json`
- live selected-move files

## Verdicts

- action_compatible=false
- implementation_action_compatible=true
- current_environment_action_compatible=false
- safe_to_rerun_p5=false
