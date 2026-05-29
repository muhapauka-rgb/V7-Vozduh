# E32.1.3 Current Model Intake

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Inputs Reviewed

- `BLOCK_E32_1_1_CAPACITY_CLASS_MODEL_REPORT.md`
- `docs/track7/productization/e32_1_1-evidence/*`
- `BLOCK_E32_1_2_CAPACITY_METADATA_MODEL_REPORT.md`
- `docs/track7/productization/e32_1_2-evidence/*`
- `BLOCK_E25_15_REFRESH_APPROVAL_PACKET_AFTER_REGISTRY_DRIFT_AND_RETRY_MOVEMENT_REPORT.md`
- `BLOCK_E27_2_FIRST_TWO_USER_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION_REPORT.md`
- `BLOCK_E30_3_FIRST_TEN_USER_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E31_POST_TEN_USER_GOVERNANCE_REVIEW_REPORT.md`

current_model_loaded=true

## Current Certified Target

```text
target=amneziawg-exec-20260528-10-8-1-14
current_certified_class=CLASS_10
certified_capacity=10
capacity_status=CERTIFIED
capacity_confidence=HIGH
soft_limit=10
hard_limit=10
```

## Existing Class Model

Certified:

- `CLASS_1`
- `CLASS_2`
- `CLASS_4`
- `CLASS_10`

Candidate / not certified:

- `CLASS_20_CANDIDATE`
- `CLASS_50_CANDIDATE`
- `CLASS_100_CANDIDATE`
- `PRODUCTION_POOL`

## Existing Metadata Model

Authoritative fields include:

- `capacity_class`
- `certified_capacity`
- `capacity_status`
- `capacity_confidence`
- `hard_limit`
- `active_policy_cap`
- validation timestamps and evidence pointers

Derived fields include:

- `effective_batch_cap`
- `current_capacity`
- `available_capacity`
- `is_execution_eligible`

## Lifecycle Gap

E32.1.1 and E32.1.2 define what a class and metadata mean. E32.1.3 must define how a target moves between states, how certification is granted, how it expires, how it is revoked, and what evidence is authoritative.

