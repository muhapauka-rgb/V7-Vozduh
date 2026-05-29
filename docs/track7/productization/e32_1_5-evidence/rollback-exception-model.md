# E32.1.5 Rollback Exception Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

rollback_exception_model_defined=true

## Principle

Rollback is containment. It reduces or restores blast radius rather than expanding it. Therefore rollback remains allowed when forward capacity is stale, degraded, or expired, provided exact rollback scope is known.

## Allowed During

Rollback may proceed during:

- STALE;
- DEGRADED;
- EXPIRED;
- forward observation failure;
- readiness degradation after forward movement;
- quality degradation after forward movement;
- runtime checker warning if rollback is the safest containment path.

## Required Rollback Gates

Rollback still requires:

- exact approved rollback user set;
- exact rollback target;
- route table mapping known;
- no unrelated users included;
- audit append;
- post-rollback restore-settle;
- delayed monitoring when applicable.

## Forbidden Rollback Cases

Rollback must stop or require incident containment review when:

- rollback target is unknown;
- rollback would move unrelated users;
- rollback route table mapping is unknown;
- rollback target is unsafe or missing;
- command would exceed original blast radius.

## REVOKED State

In REVOKED, rollback is allowed only as incident containment. No new approval packet or forward movement may be generated until incident review completes.

