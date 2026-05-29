# E32.1.1 Batch Size Constraints

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

batch_size_constraints_defined=true

## Core Rule

An approval packet's `movement_budget` and `blast_radius` must be less than or equal to the target's active certified capacity class.

```text
movement_budget <= certified_class_limit
blast_radius <= certified_class_limit
approved_user_count == movement_budget
approved_target_count == 1 unless a future multi-target policy explicitly certifies otherwise
```

## Class Limits

| Active Class | Maximum Approved Batch Size | Execution Allowed |
| --- | ---: | --- |
| UNCERTIFIED | 0 | No |
| CLASS_1 | 1 | Yes, one user only |
| CLASS_2 | 2 | Yes, up to two users |
| CLASS_4 | 4 | Yes, up to four users |
| CLASS_10 | 10 | Yes, up to ten users |
| CLASS_20_CANDIDATE | 0 until certified | Prep/model only |
| CLASS_50_CANDIDATE | 0 until certified | Prep/model only |
| CLASS_100_CANDIDATE | 0 until certified | Prep/model only |
| PRODUCTION_POOL | Policy-controlled | Only after production-pool policy certification |

## Hard Limit Interaction

Target hard limit is a runtime safety cap. The effective maximum batch size is:

```text
effective_batch_cap = min(certified_class_limit, target.hard_limit, active_policy_cap)
```

For non-production-pool execution today:

```text
active_policy_cap = certified_class_limit
```

## Soft Limit Interaction

Soft limit is advisory. It may be used by planning and operator UX to warn, but it cannot override the hard limit or certified class.

Rules:

- `soft_limit <= hard_limit`
- movement may not exceed `hard_limit`
- movement may not exceed certified class
- movement may not exceed approval packet budget

## Current Target Constraint

Target:

```text
amneziawg-exec-20260528-10-8-1-14
```

Current certified class:

```text
CLASS_10
```

Current effective cap:

```text
max_approved_batch_size=10
```

Any 20-user movement must first pass E32+ architecture and a later 20-user preparation/requalification/execution proof.

