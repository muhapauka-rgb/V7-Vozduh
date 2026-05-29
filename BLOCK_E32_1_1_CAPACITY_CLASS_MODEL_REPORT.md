# BLOCK E32.1.1 Capacity Class Model Report

e32_1_1_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_class_model_defined=true
capacity_dimensions_defined=true
class_taxonomy_defined=true
class_transition_rules_defined=true
batch_size_constraints_defined=true
e25_e31_compatibility_confirmed=true

current_certified_class_for_amneziawg_exec=CLASS_10

## Summary

E32.1.1 defines capacity class as the formal V7 certification level for how large a governed movement batch a target may safely accept.

The model is intentionally evidence-bound. A class is not granted by metadata alone; it requires capacity validation, long-window readiness, exact approved movement, rollback, delayed monitoring, replay denial, restore-settle, runtime checker health, and fresh evidence.

## Certified Classes

```text
CLASS_1=CERTIFIED
CLASS_2=CERTIFIED
CLASS_4=CERTIFIED
CLASS_10=CERTIFIED
```

Current target:

```text
target=amneziawg-exec-20260528-10-8-1-14
current_certified_class=CLASS_10
max_approved_batch_size=10
```

## Candidate Classes

```text
CLASS_20_CANDIDATE=NOT_CERTIFIED
CLASS_50_CANDIDATE=NOT_CERTIFIED
CLASS_100_CANDIDATE=NOT_CERTIFIED
PRODUCTION_POOL=ARCHITECTURE_TARGET_NOT_CERTIFIED
```

These classes may be prepared, modeled, and validated, but they do not authorize live movement until promoted by the full governance evidence chain.

## Capacity Dimensions

Required dimensions:

- user count;
- throughput;
- minimum Mbps;
- stability;
- readiness status;
- target users count;
- runtime checker health;
- restore-settle state;
- validation age;
- confidence level.

## Batch Constraint

The effective batch cap is:

```text
effective_batch_cap = min(certified_class_limit, target.hard_limit, active_policy_cap)
```

For `amneziawg-exec-20260528-10-8-1-14` today:

```text
certified_class_limit=10
hard_limit=10
active_policy_cap=10
effective_batch_cap=10
```

## Compatibility Verdict

The model matches E25-E31:

- E25.15 maps to CLASS_1.
- E27.2 maps to CLASS_2.
- E28.2 maps to CLASS_4.
- E30.2 plus E30.3 map to CLASS_10.
- E31 remains intact: governance is production-grade through 10 users, while 20/50/100-user execution and production-pool operation remain unproven.

## Remaining Open Questions

- exact freshness TTL for capacity evidence;
- encoding format for capacity class metadata;
- confidence field representation;
- production-pool policy cap behavior;
- concurrent packet handling.

recommended_next_block=E32_1_2_CAPACITY_METADATA_MODEL

## Evidence Files

- `docs/track7/productization/e32_1_1-evidence/certified-scale-intake.md`
- `docs/track7/productization/e32_1_1-evidence/capacity-dimensions.md`
- `docs/track7/productization/e32_1_1-evidence/class-taxonomy.md`
- `docs/track7/productization/e32_1_1-evidence/class-transition-rules.md`
- `docs/track7/productization/e32_1_1-evidence/batch-size-constraints.md`
- `docs/track7/productization/e32_1_1-evidence/e25-e31-compatibility-review.md`
- `docs/track7/productization/e32_1_1-evidence/final-model-decision.md`
- `docs/track7/productization/e32_1_1-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

