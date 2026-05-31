# P1.C Relationship Model

runtime_convergence_relationships_defined=true

## Evidence Bundle

Runtime convergence must produce or link to Evidence Bundle.

Evidence explains:

- what was checked;
- what release was expected;
- what runtime was observed;
- whether drift exists;
- what verification passed or failed.

## Proposal System

Proposal System must consider runtime convergence before recommending risky forward actions.

If runtime trust is `RUNTIME_UNKNOWN`, `RUNTIME_DRIFT` or `RUNTIME_BLOCKING`, proposals should show blockers or require refresh/review.

## Release Surface

Release Surface provides expected release identity and provenance.

Runtime Convergence Surface answers whether current runtime matches that identity.

## Backup / Restore

Backup and Restore workflows use convergence:

- before restore: understand current trust state;
- after restore: verify restored runtime;
- after backup: confirm backup scope maps to current runtime;
- during recovery: prove closure.

## Governance

Governance uses runtime convergence as a gate.

Forward movement requires acceptable runtime trust. Rollback and containment remain allowed when they reduce risk.

## Relationship Verdict

Runtime Convergence is the trust bridge between release/provenance, evidence, proposals, backup/restore and governance.
