# P5R Replay Test

Project: V7 Vozduh

Block: P5 RETRY

## Replay Protection

Duplicate packet execution was attempted with the same approval id:

- approval_id: `appr_p5r_zero_move_governance_state_20260601T095456Z_primary`
- verdict: `DENY_REPLAY`
- error: `approval_id_already_recorded`
- record_type: `denial_record`
- runtime_action_performed: false
- runtime_mutation: false

## Expired Packet

An expired packet was attempted:

- verdict: `DENY_PACKET_INVALID`
- error: `approval_expired`
- record_type: `denial_record`
- runtime_action_performed: false
- runtime_mutation: false

## Store Counts

- governance records before replay/fail-closed tests: `1`
- governance records after replay/fail-closed tests: `1`
- audit records before replay/fail-closed tests: `1`
- audit records after replay/fail-closed tests: `8`

Replay and denial tests wrote audit denial records only. They did not append another governance action.

## Verdict

- replay_protection_verified=true
- duplicate_packet_denied=true
- expired_packet_denied=true
- duplicate_governance_record_created=false
