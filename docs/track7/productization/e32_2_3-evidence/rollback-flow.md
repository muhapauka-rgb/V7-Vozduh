# E32.2.3 Rollback Flow

rollback_flow_defined=true

## Purpose

Rollback flow returns affected users to their approved rollback targets or performs containment when forward or observation fails.

Rollback is not a new forward movement.

## Rollback States

```text
ROLLBACK_READY
ROLLING_BACK
```

## Rollback Triggers

Rollback may be triggered by:

- planned proof-style completion;
- forward verification failure;
- observation failure;
- target degradation after movement;
- operator default rollback instruction;
- containment after partial execution.

## ROLLBACK_READY Entry

Required:

```text
rollback_manifest_complete=true
affected_user_set_exact=true
rollback_targets_known=true
route_tables_known_when_applicable=true
```

## ROLLING_BACK Entry

```text
ROLLBACK_READY -> ROLLING_BACK
```

Requires:

- exact rollback commands or transaction;
- rollback audit event initialized;
- no blast-radius expansion.

## Rollback Completion

Successful rollback verifies:

- all affected users returned to rollback targets;
- route tables restored when applicable;
- no unrelated users changed;
- target users count restored as expected;
- selected moves zero;
- hidden movers absent;
- runtime checkers OK;
- restore-settle GO.

Exit:

```text
ROLLING_BACK -> COMPLETED
```

## Rollback Failure

If rollback fails:

```text
ROLLING_BACK -> FAILED_CLOSED
```

Operator next action:

- containment review;
- exact failed user list;
- audit preservation;
- no further expansion.

## Containment Rules

Rollback/containment remains allowed when capacity is stale, degraded, or expired if:

- exact rollback scope is known;
- rollback target is valid;
- action reduces or does not expand risk;
- audit is written.

## Rollback Verdict

Rollback flow is defined and preserves containment semantics.

