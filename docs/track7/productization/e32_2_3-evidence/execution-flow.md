# E32.2.3 Execution Flow

execution_flow_defined=true

## Purpose

Execution flow defines how a batch becomes executable and enters `EXECUTING`.

The transition requires fresh execution-time recheck and all gates passing.

## Entry Preconditions

Allowed entry:

```text
SCHEDULED -> EXECUTING
```

Required:

```text
packet_non_expired=true
batch_non_expired=true
packet_not_replayed=true
batch_generation_matches_packet=true
allowed_users_exact_match=true
source_targets_match_current_runtime=true
destination_target_exact_match=true
rollback_manifest_complete=true
```

## Execution-Time Recheck

Execution-time recheck must collect and verify:

- users registry hash;
- egress registry hash;
- all candidate rows;
- route table mapping;
- target readiness;
- target users count;
- capacity status;
- effective batch cap;
- available capacity;
- runtime checkers;
- restore-settle gate;
- selected moves;
- hidden movers;
- audit lineage state.

## Capacity Gates

Required:

```text
capacity_status=CERTIFIED
movement_budget <= effective_batch_cap
movement_budget <= available_capacity
target_eligible=true
```

## Runtime Gates

Required:

```text
runtime_checkers_ok=true
restore_settle_gate_status=GO
selected_moves_count=0
hidden_movers_absent=true
```

## Target Eligibility

Required:

- target exists;
- target role permits requested batch type;
- target not stale/degraded/expired/revoked;
- target not exposed to forbidden autoswitch/rebalance path unless future policy explicitly certifies it.

## Execution Output

On success:

```text
SCHEDULED -> EXECUTING
execution_started_at=<now>
forward_event_created=true
```

On denial before mutation:

```text
SCHEDULED -> FAILED_CLOSED
```

On partial mutation:

```text
EXECUTING -> ROLLBACK_READY
```

until partial-completion semantics are separately certified.

## Execution Verdict

Execution flow is defined and fails closed.

