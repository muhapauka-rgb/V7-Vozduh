# E32.2.1 Capacity Integration

batch_capacity_integration_defined=true

## Capacity Program Dependency

Execution batches consume the certified E32.1 Capacity Program.

Capacity remains a gate, not an authority.

## Required Capacity Inputs

Every forward-capable batch must bind:

```text
capacity_class
certified_capacity
capacity_status
capacity_confidence
hard_limit
active_policy_cap
effective_batch_cap
available_capacity
capacity_validation_evidence
capacity_expiration
```

## Eligibility Formula

Batch capacity eligibility:

```text
capacity_status == CERTIFIED
capacity_not_stale == true
capacity_confidence >= required_confidence
movement_budget <= effective_batch_cap
movement_budget <= available_capacity
destination_target_eligible == true
```

## Current Certified Mapping

Current certified target:

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
certified_capacity=10
capacity_status=CERTIFIED
capacity_confidence=HIGH
```

Historical mapping:

```text
CLASS_1 -> max exact batch size 1
CLASS_2 -> max exact batch size 2
CLASS_4 -> max exact batch size 4
CLASS_10 -> max exact batch size 10
```

## Denial Conditions

Forward batch approval or execution must deny if:

- capacity status is `STALE`;
- capacity status is `DEGRADED`;
- capacity status is `EXPIRED`;
- capacity status is `REVOKED`;
- capacity evidence is missing;
- movement budget exceeds effective batch cap;
- movement budget exceeds available capacity;
- policy cap is exceeded;
- reservation conflict exists;
- target eligibility is false.

## Rollback Exception

Rollback batch may proceed even when capacity is stale, degraded, or expired, if:

- exact rollback scope is known;
- rollback does not expand blast radius;
- rollback target is valid;
- rollback is containment.

## Capacity Integration Verdict

Batch capacity integration is defined and consistent with E32.1.

