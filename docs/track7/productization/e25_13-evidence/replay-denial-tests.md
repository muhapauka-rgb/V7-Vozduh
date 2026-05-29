# E25.13 Replay / Denial Tests

`replay_denial_semantics_valid=true`

| Case | Expected Denial | Actual Reasons | Result |
| --- | --- | --- | --- |
| expired packet | `DENY_EXPIRED` | `DENY_EXPIRED` | PASS |
| unauthorized user | `DENY_UNAUTHORIZED_USER` | `DENY_UNAUTHORIZED_USER` | PASS |
| unauthorized target | `DENY_UNAUTHORIZED_TARGET` | `DENY_UNAUTHORIZED_TARGET` | PASS |
| movement_budget > 1 | `DENY_MOVEMENT_BUDGET` | `DENY_MOVEMENT_BUDGET` | PASS |
| stale users hash | `DENY_STALE_USERS_HASH` | `DENY_STALE_USERS_HASH` | PASS |
| stale egress hash | `DENY_STALE_EGRESS_HASH` | `DENY_STALE_EGRESS_HASH` | PASS |
| stale selected move hash | `DENY_STALE_SELECTED_MOVE_HASH` | `DENY_STALE_SELECTED_MOVE_HASH` | PASS |
| execution target not GO | `DENY_TARGET_NOT_GO` | `DENY_TARGET_NOT_GO` | PASS |
| execution target not execution-only | `DENY_TARGET_NOT_EXECUTION_ONLY` | `DENY_TARGET_NOT_EXECUTION_ONLY` | PASS |
| autoswitch exclusion missing | `DENY_AUTOSWITCH_EXCLUSION_MISSING` | `DENY_AUTOSWITCH_EXCLUSION_MISSING` | PASS |
| missing second confirmation | `DENY_MISSING_SECOND_CONFIRMATION` | `DENY_MISSING_SECOND_CONFIRMATION` | PASS |
| wrong generation | `DENY_WRONG_GENERATION` | `DENY_WRONG_GENERATION` | PASS |
| replay attempt | `DENY_REPLAY` | `DENY_REPLAY` | PASS |

## Runtime Mutation

`runtime_mutation_performed=false`

These tests validated packet semantics locally and did not execute movement or mutate runtime state.
