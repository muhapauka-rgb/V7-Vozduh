# Pipeline Contract Summary

Schema: `v7.operator-governed-execution-pipeline.v1`

Single path:

- planner: `tools/v7-users-autoswitch`
- approval packet: `tools/v7-operator-execution-packet`
- packet owner: `admin_core/operator_execution.py`
- runtime apply: `tools/v7-users-autoswitch --apply --verify`
- rollback: `tools/v7-users-autoswitch --rollback-packet --apply --verify`
- direct user switch allowed: `false`

Recommendation execution candidate required fields:

- user
- current_channel
- recommended_channel
- confidence
- trust
- prediction
- risk
- rollback_plan
- snapshot_generation
- source_hashes
- reason_summary

Execution states:

- EXECUTION_READY
- EXECUTION_BLOCKED
- EXECUTION_RUNNING
- EXECUTION_SUCCESS
- EXECUTION_PARTIAL
- EXECUTION_FAILED
- ROLLBACK_REQUIRED
- ROLLBACK_RUNNING
- ROLLBACK_SUCCESS
- ROLLBACK_FAILED

Every state has:

- Condition
- Decision
- Action
- Executor
- Trigger
- Written Evidence
- Blocked Actions
- Next State

