# E31 Risk Matrix

| Risk | Classification | Current mitigation | Residual note |
| --- | --- | --- | --- |
| Capacity beyond 10 users | MEDIUM | 10-user target-local and execution proof exists | 20/50/100 remain unproven |
| Large rollback sets | MEDIUM | Rollback proven through 10 users | Operational complexity rises with cohort size |
| Large audit volume | MEDIUM | Audit chain valid through 10 users | Larger batches need audit summarization and lineage tooling |
| Large replay volume | MEDIUM | Replay denial validated through certified scale | Multi-packet replay concurrency remains unproven |
| Multi-packet concurrency | HIGH | Not used in certified executions | Requires explicit locking/serialization model |
| Operator error | MEDIUM | Exact packet, exact commands, execution-time recheck | Needs production operator workflow and guardrails |
| Execution batching | MEDIUM | Sequential approved raw fallback worked through 10 users | Larger cohorts may need batch transaction semantics |
| Autonomous governance | HIGH | Manual/operator-driven governance certified | Autonomous proposal/apply remains out of scope |
| Production pool execution | MEDIUM | Execution-only target model certified | Production-pool policies, scheduling, and observability need design |

remaining_risks=capacity_beyond_10_users,large_rollback_sets,large_audit_volume,large_replay_volume,multi_packet_concurrency,operator_error,execution_batching,autonomous_governance,production_pool_execution
