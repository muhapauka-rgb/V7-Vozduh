# P5R Action Execution

Project: V7 Vozduh

Block: P5 RETRY

## Executed Action

Executed only:

`ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`

Execution used:

`execute_packet(packet, /opt/v7/audit/operator-execution-audit.jsonl, /opt/v7/egress/state, mode="runtime_action", runtime_governance_store=/opt/v7/audit/operator-runtime-governance-actions.jsonl)`

## Stores

- audit store: `/opt/v7/audit/operator-execution-audit.jsonl`
- governance store: `/opt/v7/audit/operator-runtime-governance-actions.jsonl`

## Counts

- audit records before action: `0`
- governance records before action: `0`
- audit records after action: `1`
- governance records after action: `1`

## Appended Records

Governance record:

- record_type: `zero_move_governance_state_transition`
- record_hash: `2a55595d95b73fc910dc6bdb6446c803efa5a834e274627ef9dfdadd23620def`
- previous_record_hash: `GENESIS`
- runtime_mutation_scope: `append_only_runtime_governance_state`
- user_movement: false
- routing_mutation: false
- autoswitch_apply: false

Audit record:

- record_type: `runtime_action_record_persisted`
- record_hash: `4dc953c09fbe887964737d4a9d088f88af51fb5387adc4869c2d4051747dea4e`
- previous_record_hash: `GENESIS`
- runtime_action_record_hash: `2a55595d95b73fc910dc6bdb6446c803efa5a834e274627ef9dfdadd23620def`
- runtime_action_performed: true
- runtime_mutation_scope: `append_only_runtime_governance_state`
- user_movement: false
- routing_mutation: false
- autoswitch_apply: false

## Verdict

- action_executed=true
- governance_record_appended=true
- audit_record_appended=true
- user_movement_performed=false
- routing_mutation_performed=false
- autoswitch_apply_run=false
