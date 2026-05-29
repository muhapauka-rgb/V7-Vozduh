# E32.1.2 Authoritative Vs Derived Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

authoritative_vs_derived_defined=true

## Principle

Authoritative fields are stored facts or governance decisions. Derived fields are recalculated from authoritative fields and live runtime snapshots. Derived fields must never be edited as a source of truth.

## Authoritative Fields

| Field | Why Authoritative |
| --- | --- |
| `capacity_class` | Formal certification decision. |
| `certified_capacity` | Class taxonomy result. |
| `capacity_status` | Lifecycle decision controlling eligibility. |
| `capacity_confidence` | Evidence quality decision. |
| `soft_limit` | Registry/operator advisory cap. |
| `hard_limit` | Registry/operator hard cap. |
| `active_policy_cap` | Policy engine cap. |
| `capacity_validation_time` | Accepted validation timestamp. |
| `capacity_validation_method` | Accepted validation method list. |
| `capacity_validation_evidence` | Accepted evidence references/hashes. |
| `capacity_validation_version` | Schema/tool version. |
| `capacity_stale_after` | TTL policy output. |
| `capacity_expiration` | TTL policy output. |
| `reservation_owner` | Governance ownership. |
| `autoswitch_allowed` | Assignment policy. |
| `rebalance_allowed` | Assignment policy. |
| `production_assignment_allowed` | Assignment policy. |
| `max_concurrent_packets` | Concurrency policy. |

## Derived Fields

| Field | Formula Or Source |
| --- | --- |
| `effective_batch_cap` | `min(certified_capacity, hard_limit, active_policy_cap)` if status permits. |
| `current_capacity` | `effective_batch_cap` when fresh and certified, otherwise `0`. |
| `available_capacity` | `current_capacity - target_users_count - capacity_reserved`. |
| `target_users_count` | Derived from users registry. |
| `last_readiness_status` | Snapshot from readiness helper. |
| `last_restore_settle_status` | Snapshot from restore-settle helper. |
| `last_runtime_checkers_status` | Snapshot from runtime checkers. |
| `is_fresh` | Current time before stale/expiration thresholds and no invalidation trigger. |
| `is_execution_eligible` | Derived from status, freshness, readiness, restore-settle, hard limit, policy, and isolation. |

## Effective Batch Cap

```text
if capacity_status != CERTIFIED:
  effective_batch_cap = 0
elif now >= capacity_expiration:
  effective_batch_cap = 0
elif now >= capacity_stale_after:
  effective_batch_cap = 0 until refresh
else:
  effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
```

## Execution Eligibility

```text
is_execution_eligible = (
  capacity_status == CERTIFIED
  and now < capacity_stale_after
  and now < capacity_expiration
  and readiness_status == GO
  and restore_settle_status == GO
  and runtime_checkers_ok == true
  and selected_moves == 0
  and hidden_movers_absent == true
  and autoswitch_allowed == false for execution-only targets
  and rebalance_allowed == false for execution-only targets
)
```

## Safety Rule

No approval packet may store only a derived cap. It must bind:

- authoritative class;
- authoritative hard limit;
- authoritative policy cap;
- derived effective cap;
- current registry hashes;
- current readiness/restore-settle status;
- evidence references.

