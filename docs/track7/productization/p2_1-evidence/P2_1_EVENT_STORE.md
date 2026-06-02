# P2.1 Execution Event Store

## Store

Path:
`STATE_DIR/execution-events.jsonl`

Environment override:
`V7_EXECUTION_EVENTS_FILE`

The event store is JSONL and read-only in P2.1.

## Event Fields

Normalized fields:

- `event_id`
- `event_type`
- `contract_id`
- `batch_id`
- `ts`
- `status`
- `severity`
- `summary`
- `reason`
- `affected_users`
- `affected_targets`
- `source`

Safety fields always set:

- `read_only=true`
- `non_authoritative=true`

## Supported Event Types

`EXECUTION_EVENT`, `EXECUTION_CREATED`, `EXECUTION_CONTRACT_CREATED`, `EXECUTION_VALIDATED`, `EXECUTION_STARTED`, `EXECUTION_COMPLETED`, `EXECUTION_FAILED`, `VERIFICATION_STARTED`, `VERIFICATION_COMPLETED`, `VERIFICATION_FAILED`, `ROLLBACK_CREATED`, `ROLLBACK_STARTED`, `ROLLBACK_COMPLETED`, `ROLLBACK_FAILED`, `REPLAY_DENIED`.

Unknown event types normalize to `EXECUTION_EVENT`.

## Verdict

event_store_implemented=true
event_store_read_only=true
runtime_mutation_performed=false
