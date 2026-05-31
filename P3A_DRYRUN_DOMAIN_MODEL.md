# P3.A Dry-Run Domain Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Definition

Runtime Dry-Run is a derived, non-authoritative decision model that observes existing runtime evidence and computes what the system would recommend, block, verify or roll back without executing anything.

It is not:

- A runtime engine.
- A scheduler.
- A routing hook.
- An autoswitch bridge.
- An execution queue.
- A deployment mechanism.

## Core Entities

| Entity | Meaning |
| --- | --- |
| Runtime Observation | Read-only fact from existing runtime state, event logs, service health or trust evidence. |
| Runtime Event | Normalized historical event derived from existing event/audit stores. |
| Dry-Run Candidate | A proposed runtime decision evaluated without authority. |
| Dry-Run Decision | A non-executable decision such as `WOULD_MOVE` or `WOULD_BLOCK`. |
| Dry-Run Contract | Snapshot of inputs, decision, evidence, constraints and verification plan. |
| Dry-Run Report | Operator-facing explanation generated from a contract. |
| Verification Result | Later comparison between prediction and observed reality. |
| Rollback Simulation | Preview of what rollback would require if the decision were real. |

## Inputs

- Runtime state snapshots.
- Runtime and admin audit events.
- Service health and service matrix evidence.
- Trust and authority evidence.
- Candidate/proposal/review/approval previews.
- Existing execution contract and event previews.
- Routing and proxy dry-run evidence.
- Rollback and restore barrier evidence.

## Outputs

- Dry-run decision.
- Dry-run explanation.
- Dry-run evidence bundle.
- Dry-run contract preview.
- Verification plan and later verification result.
- Rollback preview.
- Retention classification.

## Authority Model

Every P3.A output must be:

- `read_only=true`
- `preview_only=true`
- `derived_only=true`
- `non_authoritative=true`
- `execution_allowed_now=false`

## Domain Verdict

`dryrun_domain_defined=true`

