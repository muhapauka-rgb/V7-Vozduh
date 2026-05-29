# E32.2.2 Derived Batch Fields

derived_fields_defined=true

## Principle

Derived fields are computed views over authoritative metadata, runtime state, capacity state, packet state, and audit lineage.

Derived fields must fail closed if their inputs are missing, stale, or conflicting.

## Derived Field Matrix

| Field | Formula / Source | Freshness | Fail-Closed Behavior |
| --- | --- | --- | --- |
| `effective_blast_radius` | Count of unique users in allowed users, rollback manifest, and affected events | Current batch view | Unknown if sets conflict; deny forward. |
| `target_capacity_required` | `movement_budget` plus target occupancy delta | At approval and execution-time recheck | Deny if required capacity cannot be computed. |
| `target_available_capacity` | Capacity model: `effective_batch_cap - target_users_count - reserved_capacity` | Fresh runtime/capacity snapshot | Deny forward if stale or below budget. |
| `risk_score` | Policy-derived score from batch size, type, target class, confidence, rollback completeness, and incident state | Recomputed before approval and execution | Treat unknown as high risk; require review or deny. |
| `execution_eligibility` | Combined gates: packet, capacity, runtime, restore-settle, exact scope, no replay | Execution-time recheck only | Deny unless explicitly true. |
| `rollback_completeness` | `rollback_manifest` covers all affected users and route tables | Before forward and before rollback | Deny forward if incomplete; allow containment review if post-failure. |
| `runtime_drift_status` | Compare current registry/routes/checkers against packet-bound snapshot | Execution-time recheck | Deny forward on drift unless fresh packet generated. |
| `packet_freshness_status` | Compare `now` to packet/batch `expires_at` and generation | Execution-time recheck | Deny if expired or generation mismatch. |
| `capacity_gate_status` | E32.1 capacity gates for destination target | Approval and execution-time recheck | Deny forward if not fresh `CERTIFIED`. |
| `audit_lineage_status` | Presence and consistency of lineage ids and prior replay records | Approval, execution, closure | Deny replay; deny forward if lineage conflict. |

## Risk Score Model

Initial risk bands:

```text
LOW=rollback_or_containment_with_exact_scope
MEDIUM=operator_movement_with_CLASS_10_or_below_and_HIGH_confidence
HIGH=evacuation_or_rebalance_or_staged_migration
BLOCKED=missing_rollback_or_capacity_or_packet_or_audit_lineage
```

Risk score is advisory until the policy engine is defined, except `BLOCKED`, which is a hard denial.

## Execution Eligibility Formula

```text
execution_eligibility =
  packet_valid
  and packet_non_expired
  and batch_non_expired
  and exact_user_set_matches
  and exact_target_set_matches
  and rollback_completeness == COMPLETE
  and capacity_gate_status == GO
  and runtime_checkers_ok
  and restore_settle_gate_status == GO
  and selected_moves_zero
  and hidden_movers_absent
  and replay_not_consumed
```

## Derived Field Verdict

Derived fields are defined and fail closed on missing, stale, or conflicting inputs.

