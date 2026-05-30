# E32.3.A Prior Architecture Intake

prior_architecture_loaded=true

## Scope

This intake loads the certified E32.1 Capacity Program and E32.2 Execution Batches Architecture.

This is read-only architecture work. No runtime mutation, user movement, routing mutation, autoswitch apply, UI execution, canary, or cohort execution was performed.

## Capacity Inputs

Capacity Program verdict:

```text
capacity_program_certified=true
internal_consistency=true
production_pool_compatible=true
```

Capacity gates:

- capacity status must be fresh `CERTIFIED`;
- movement budget must fit `effective_batch_cap`;
- movement budget must fit `available_capacity`;
- capacity confidence must meet policy threshold;
- stale, degraded, expired, revoked, unknown, or conflicting capacity denies forward movement.

## Batch Inputs

Execution Batches Architecture verdict:

```text
execution_batches_architecture_certified=true
internal_consistency=true
fail_closed_behavior_valid=true
production_pool_compatible=true
```

Batch boundaries:

- exact allowed users;
- exact source targets;
- exact destination target;
- exact rollback manifest;
- exact movement budget;
- exact blast radius;
- exact execution window;
- exact audit lineage.

## Batch Lifecycle Inputs

Batch lifecycle states:

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

Lifecycle rules:

- approval does not authorize mutation;
- execution requires execution-time recheck;
- terminal states cannot resume execution;
- replay attempts are denied.

## Rollback And Containment Inputs

Rollback and containment rules:

```text
rollback_allowed=only_with_exact_scope
containment_allowed=only_without_blast_radius_expansion
human_review_required=when_scope_or_audit_is_unknown
```

## Remaining Architecture Decisions

Known future decisions include:

- policy-engine ownership of risk score;
- scheduler priority model;
- production-pool reservation ledger;
- production-pool observability schema;
- retained production-pool completion semantics;
- partial-forward recovery policy;
- audit reconstruction authority.

## Intake Verdict

Prior architecture is loaded and ready for Policy Foundation definition.
