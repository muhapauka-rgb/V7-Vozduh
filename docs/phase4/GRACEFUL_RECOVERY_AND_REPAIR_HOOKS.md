# V7 Phase 4 Graceful Recovery And Repair Hooks

## Purpose

Self-healing must reduce operator firefighting without creating hidden routing behavior.

## Graceful Recovery

After an egress recovers, autoswitch must not immediately move users back.

Recovery should require:

- stable service checks;
- route verification;
- no recent failed switch;
- no active quarantine;
- load compatibility;
- sufficient recovery window.

## Repair Hooks

Autoswitch MAY request or suggest:

- routing reconciliation;
- egress quarantine;
- maintenance/drain mode;
- safe interface restart;
- provisioning verification;
- route table check;
- nft consistency check.

## Safety Rules

Repair hooks must be:

- bounded;
- audited;
- explicit;
- reversible when possible;
- verified after action.

Autoswitch MUST NOT:

- silently disable kill switch;
- silently rewrite routing policy;
- silently enable unverified egress;
- silently override route classes.

## Operator UX

Repair should appear as:

- issue summary;
- likely cause;
- suggested action;
- safety impact;
- rollback status.

Deep command details belong in diagnostics, not the main overview.

