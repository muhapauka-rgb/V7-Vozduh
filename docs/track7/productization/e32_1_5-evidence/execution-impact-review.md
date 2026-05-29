# E32.1.5 Execution Impact Review

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

execution_impact_defined=true

## Runtime Decisions Affected By Capacity

Capacity affects these runtime decisions:

- approval packet creation;
- execution-time recheck;
- target eligibility;
- batch size;
- scheduler eligibility;
- production-pool admission;
- rollback exception handling;
- replay validation assumptions.

Capacity does not replace governance. It is one input into governance gates.

## Approval Packet Creation

Capacity gates packet creation by requiring:

```text
capacity_status=CERTIFIED
capacity_fresh=true
movement_budget <= effective_batch_cap
blast_radius <= effective_batch_cap
available_capacity >= movement_budget
capacity_confidence >= required_confidence
```

If any capacity input is missing, packet creation must produce a non-executable draft or deny creation.

## Execution-Time Recheck

Capacity must be recomputed at execution time:

```text
effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
available_capacity = effective_batch_cap - target_users_count - capacity_reserved
```

Execution is denied if packet-bound capacity values do not match live authoritative metadata.

## Target Eligibility

A target is eligible for forward movement only when:

- capacity status is fresh `CERTIFIED`;
- readiness is GO;
- restore-settle is GO;
- runtime checkers are OK;
- target role permits the requested execution type;
- isolation/exclusion constraints are intact.

## Rollback

Rollback remains allowed when capacity is stale, degraded, or expired because rollback is containment, not expansion. Rollback must still be exact and must not increase blast radius.

## Replay

Replay validation is capacity-aware only as a denial context:

- replay must deny regardless of capacity availability;
- capacity becoming available again does not make an executed packet reusable.

## Restore-Settle

Restore-settle is both:

- an input to capacity-based execution eligibility;
- an output validation after rollback.

If restore-settle is not GO, forward execution is denied even if capacity class is certified.

