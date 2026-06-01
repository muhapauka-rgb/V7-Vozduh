# P4 Observation Window Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Window Phases

| Phase | Purpose |
| --- | --- |
| Before action | Freeze evidence, packet, scope, target, rollback and baseline metrics. |
| During action | In a future execution block, monitor exact scoped mutation and stop on deviation. |
| After action | Verify expected state, no hidden movement, no routing drift, no health regression. |

## Checkpoints

- T-0 baseline before any future action
- immediate pre-action recheck
- action start marker in future execution block
- immediate post-action verification
- settle window
- delayed monitoring
- replay denial verification

## Observed Sources

- audit log
- event log
- switch history
- service matrix
- runtime state
- users registry
- egress registry
- route/runtime checkers
- dry-run verification
- execution verification preview/result

## Retention

Observation records must be bounded by existing retention architecture. P4 creates no new unbounded event stream.

## Verdict

`observation_window_defined=true`

