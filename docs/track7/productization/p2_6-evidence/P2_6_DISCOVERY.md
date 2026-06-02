# P2.6 Discovery

## Result

discovery_completed=true

P2.6 audited Proposal, Evidence, Contract Draft, Validation Preview, Simulation, Readiness Forecast, and P2.4 Operator Workflow.

## Finding

Proposal-derived contract drafts already behaved like execution candidates, but the concept was implicit. P2.6 makes candidate a first-class read model without creating execution authority or a runtime write path.

## Classification

| Area | Classification | Decision |
| --- | --- | --- |
| Proposal Store | Reuse | Candidate is derived from proposals. |
| Evidence Store | Reuse | Candidate keeps evidence references. |
| Authority Store | Reuse | Candidate carries authority references from draft preview. |
| Contract Drafts | Extend | Drafts become candidate source material, not candidate identity. |
| Validation Preview | Reuse | Candidate readiness consumes validation state. |
| Simulation | Reuse | Candidate risk and explanation include simulation state. |
| Candidate Persistent Writes | Do Not Touch | No write path in P2.6. |
| Execution Engine | Do Not Touch | Still forbidden. |

## Safety

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
