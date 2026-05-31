# P2.9 Responsibility Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Responsibility Map

| Responsibility | Owner |
|---|---|
| Runtime truth reading | runtime fingerprint/drift/convergence helpers |
| Execution contract/event reading | execution read API layer |
| Draft contract preview | execution preview layer |
| Validation/verification/readiness | execution gate and preview adapters |
| Candidate derivation | candidate read model layer |
| Approval preview | Approval Center preview |
| Governance preview | operator execution governance preview |
| Rehearsal preview | operator execution rehearsal preview |
| Evidence/audit search | operator observability helpers |
| Admin navigation | existing `/admin-v2` shell |
| Retention visibility | existing retention/closure/maintenance surfaces |

## Findings

Responsibilities are separated by read model and preview owner. Candidate does not own approval.
Approval does not own execution. Governance and rehearsal do not execute runtime actions. The admin UI
does not create an additional ownership boundary.

responsibility_overlap_risk=LOW
dangerous_parallel_systems_found=false
runtime_mutation_performed=false
