# V7 Phase 7 Runtime Self-Healing Maturity

## Purpose

Self-healing must remain bounded, deterministic, audited, and verified.

## Allowed Repair Classes

May be supported when policy allows:

- read-only reconcile;
- safe interface restart;
- missing route rule restore;
- nft consistency rebuild;
- egress quarantine;
- maintenance/drain suggestion;
- stale process cleanup under V7-managed paths.

## Required Gates

Every repair needs:

- actor;
- reason;
- affected object;
- before state;
- intended after state;
- rollback context;
- verification command;
- bounded retry count.

## Confidence Levels

low:

- recommend only.

medium:

- allow preview and operator confirmation.

high:

- allow guarded action if policy permits and rollback exists.

## Forbidden Repair

Do not:

- rebuild datapath silently;
- delete unknown runtime files;
- move users without confidence and bounds;
- disable safeguards;
- treat failed verification as success.

