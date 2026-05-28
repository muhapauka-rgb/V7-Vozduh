# E22 First Execution Result

## Result

first_zero_movement_packet_executed=true
approval_record_written=false
denial_records_written=true
result=DENY_STALE_RUNTIME
execution_allowed_now=false

The packet consumer ran in `--execute-approval-record` mode and stopped before
any runtime action. Because this local workspace has no `/opt/v7/egress/state`
runtime registry files, the live recheck failed closed with:

```text
DENY_STALE_RUNTIME
runtime_registry_missing
```

This is the correct result for this environment. The consumer wrote an immutable
denial record instead of an approval record.

## Record

approval_id=appr_e22_zero_movement_approval_record_20260528_r2
record_type=denial_record
record_hash=0e86b24f1ef933fdede4e2570f688c95d7b0d560a6dfac99dbb02fdae1f3bbe5
previous_record_hash=02be272d7576e142998f7d224d7494b44632269d0f6d0af3881004e1c6732751

## Mutation Statement

runtime_mutation=false
user_movement=false
routing_mutation=false
real_runtime_action_performed=false
