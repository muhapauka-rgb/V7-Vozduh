# E32.2.1 Batch Boundary Model

batch_boundary_model_defined=true

## Boundary Principle

An execution batch is valid only when all boundaries are exact, explicit, and fail-closed.

No implicit user expansion, target expansion, rollback expansion, budget expansion, or evidence expansion is allowed.

## Exact User Set

Requirement:

```text
allowed_users_exact=true
wildcard_users_allowed=false
```

Execution-time recheck must verify:

- every allowed user exists;
- every allowed user is enabled if forward movement requires it;
- every allowed user is still on expected source target;
- no extra user is included by helper output or route sync.

## Exact Target Set

Requirement:

```text
destination_target_exact=true
allowed_targets_exact=true
```

Forward movement must deny if:

- target differs from packet;
- target loses eligibility;
- target class/capacity no longer satisfies batch;
- target is not allowed for the batch type.

## Exact Rollback Set

Requirement:

```text
rollback_manifest_required=true
rollback_scope_exact=true
```

Rollback may proceed only for users in the rollback manifest, except when a separately approved containment batch is created.

## Exact Budget

Required invariants:

```text
movement_budget <= blast_radius
actual_forward_moved <= movement_budget
actual_affected_users <= blast_radius
```

For exact movement batches:

```text
movement_budget == len(allowed_users)
blast_radius == len(allowed_users)
```

## Exact Expiry

Batch and approval packet must expire.

Execution is denied if:

```text
now > expires_at
```

If a packet expires before execution, a fresh equivalent packet may be generated only after a fresh runtime snapshot and recheck.

## Exact Evidence Scope

Evidence must bind:

- user set;
- target;
- packet;
- registry hashes;
- capacity state;
- runtime checks;
- forward proof;
- rollback proof;
- replay proof.

Evidence from one batch cannot authorize another batch.

## Boundary Verdict

Batch boundary model is defined and preserves exact blast-radius control.

