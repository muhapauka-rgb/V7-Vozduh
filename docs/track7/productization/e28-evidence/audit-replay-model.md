# E28 Audit And Replay Model

date_utc=2026-05-29T06:18:00Z

## Audit Scaling

packet_lineage_required=true
forward_record_required=true
rollback_record_required=true
denial_record_required_for_replay=true
audit_ordering_required=true
audit_tail_records_parsed=26
audit_tail_parse_errors=0

E27.2 proved the two-user replay model after replacing order-dependent grep with JSON parsing for audit records. The same approach scales to a small cohort packet by matching exact `packet_id` and cohort movement event type.

audit_scales_to_small_cohort=true

## Replay Scaling

packet_uniqueness_required=true
consumed_forward_record_lookup=json_packet_id_and_event
replay_expected_verdict=DENY_REPLAY
movement_during_replay_allowed=false
routing_mutation_during_replay_allowed=false

replay_scales_to_small_cohort=true

