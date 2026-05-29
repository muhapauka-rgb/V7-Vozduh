# E32.2.1 Prior Execution Intake

prior_executions_mapped_to_batches=true

## Scope

This intake maps the proven E25-E31 governed executions into the new Execution Batch architecture.

The review is read-only architecture work. No runtime mutation, user movement, routing mutation, autoswitch apply, canary, or cohort execution was performed.

## Historical Batch Mapping

| Historical Block | Batch Size | Batch Type | Approved Users | Destination | Rollback | Certification Result |
| --- | ---: | --- | --- | --- | --- | --- |
| E25.15 | 1 | `OPERATOR_MOVEMENT_BATCH` | `10.7.0.11` | `amneziawg-exec-20260528-10-8-1-14` | `1` | CLASS_1 proof |
| E27.2 | 2 | `OPERATOR_MOVEMENT_BATCH` | `10.7.0.11`, `10.7.0.12` | `amneziawg-exec-20260528-10-8-1-14` | `1` | CLASS_2 proof |
| E28.2 | 4 | `OPERATOR_MOVEMENT_BATCH` | `10.7.0.11`, `10.7.0.12`, `10.7.0.14`, `10.7.0.15` | `amneziawg-exec-20260528-10-8-1-14` | `1` | CLASS_4 proof |
| E30.3 | 10 | `OPERATOR_MOVEMENT_BATCH` | `10.7.0.2`, `10.7.0.3`, `10.7.0.4`, `10.7.0.5`, `10.7.0.6`, `10.7.0.8`, `10.7.0.11`, `10.7.0.12`, `10.7.0.14`, `10.7.0.15` | `amneziawg-exec-20260528-10-8-1-14` | `1` | CLASS_10 proof |

## Common Batch Shape Proven Historically

Each historical execution included:

- exact approved user set;
- exact destination target;
- exact rollback target;
- movement budget equal to blast radius;
- fresh approval packet;
- execution-time recheck;
- forward execution;
- forward verification;
- observation window;
- default rollback;
- rollback verification;
- post-rollback restore-settle;
- delayed monitoring;
- replay denial;
- audit lineage.

## Evidence Alignment

The historical executions already behaved like batches, even before a formal batch architecture existed.

Common invariant:

```text
movement_budget == blast_radius == len(allowed_users)
```

Common safety result:

```text
only_approved_users_moved=true
routing_mutation_limited_to_candidates=true
rollback_success=true
delayed_movement_observed=false
replay_rejection_verified=true
```

## Intake Verdict

The proven E25-E31 movements can be represented cleanly as formal execution batches.

