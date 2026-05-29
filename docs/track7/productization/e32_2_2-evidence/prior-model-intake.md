# E32.2.2 Prior Model Intake

prior_model_loaded=true

## Scope

This intake loads the certified Capacity Program, the E32.2.1 Execution Batch Model, and the historical governed execution proofs from E25/E27/E28/E30.

The block is read-only architecture work. No runtime mutation, user movement, routing mutation, autoswitch apply, UI execution, canary, or cohort execution was performed.

## Capacity Program Inputs

E32.1 certified:

```text
capacity_program_certified=true
internal_consistency=true
production_pool_compatible=true
```

Current certified target:

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
certified_capacity=10
capacity_status=CERTIFIED
capacity_confidence=HIGH
```

Capacity rule:

```text
effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
```

## Execution Batch Model Inputs

E32.2.1 defined:

```text
execution_batch_model_defined=true
batch_is_authority=false
```

Authority remains with:

- approval packet;
- execution-time recheck;
- capacity gates;
- runtime gates;
- operator confirmation where required.

Defined batch types:

- `OPERATOR_MOVEMENT_BATCH`
- `ROLLBACK_BATCH`
- `EVACUATION_BATCH`
- `CAPACITY_REBALANCE_BATCH`
- `STAGED_MIGRATION_BATCH`
- `CONTAINMENT_BATCH`

## Historical Execution Inputs

Historical proofs map to batch sizes:

```text
E25.15 -> batch_size=1
E27.2  -> batch_size=2
E28.2  -> batch_size=4
E30.3  -> batch_size=10
```

Common proof chain:

```text
approval_packet=true
execution_time_recheck=true
forward_proof=true
rollback_proof=true
delayed_monitoring=true
replay_denial=true
audit_lineage=true
```

## Intake Verdict

The prior model is loaded and suitable for defining formal batch metadata.

