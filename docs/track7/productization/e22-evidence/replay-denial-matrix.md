# E22 Replay / Denial Matrix

## Executed Denials

| Case | Expected | Actual | Record |
|---|---|---|---|
| invalid selected-move hash | DENY_PACKET_INVALID | DENY_PACKET_INVALID | denial_record |
| missing live runtime registry | DENY_STALE_RUNTIME | DENY_STALE_RUNTIME | denial_record |
| replay same approval id | DENY_REPLAY | DENY_REPLAY | denial_record |

## Unit-Tested Denials

| Case | Expected | Covered |
|---|---|---|
| expired packet | DENY_PACKET_INVALID | true |
| missing second confirmer | DENY_PACKET_INVALID | true |
| modified selected-move hash | DENY_PACKET_INVALID | true |
| missing generation id | DENY_PACKET_INVALID | true |
| packet attempting runtime action | DENY_PACKET_INVALID | true |
| packet attempting user movement | DENY_PACKET_INVALID | true |
| missing runtime state | DENY_STALE_RUNTIME | true |
| replay same packet | DENY_REPLAY | true |

## Runtime Mutation Check

All denial records include:

- runtime_mutation=false
- user_movement=false
- routing_mutation=false

## Matrix Verdict

replay_rejection_verified=true
denial_records_written=true
real_runtime_action_performed=false
execution_allowed_now=false
