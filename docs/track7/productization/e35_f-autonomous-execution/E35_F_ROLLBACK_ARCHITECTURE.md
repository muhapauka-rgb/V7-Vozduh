# E35.F Rollback Architecture

## Rollback Principle

Rollback is a first-class execution path, not an afterthought.

Forward execution is forbidden unless rollback is defined, scoped, and verifiable.

## Rollback Triggers

| Trigger | Source | Automatic allowed |
|---|---|---|
| Forward verification failure | Verifier | Yes if contract rollback is complete |
| Observation failure | Observation window | Yes if bounded |
| Required service failure | Service verifier | Conditional |
| Target readiness loss | Readiness helper | Conditional |
| Hidden mover detected | Hidden mover scan | Containment first |
| Selected moves appeared | Selected moves scan | Containment/review |
| Operator rollback request | Operator | Yes through authorized path |
| Governance rollback order | Governance | Yes through authorized path |
| Containment emergency | Containment | Yes within emergency boundary |

## Rollback Scope

Rollback scope must be exactly:

```text
contract.allowed_users -> contract.rollback_manifest
```

No additional users may be included without a new containment contract.

## Rollback Authority

Rollback remains allowed even when forward movement is denied due to:

- stale capacity;
- degraded capacity;
- expired forward contract;
- target degradation;
- policy denial of further forward execution.

Rollback may not bypass:

- exact scope;
- audit;
- verification;
- containment boundaries.

## Rollback Expiry

Rollback data must survive forward contract expiry long enough to support safe recovery. Forward execution expires quickly; rollback manifest remains active until closure.

## Rollback Audit

Rollback events must include:

- contract id;
- trigger;
- user set;
- rollback target per user;
- stdout/stderr/exit summary if executed;
- registry and route diff;
- verification result;
- operator/system actor.

## Rollback Verdict

rollback_architecture_defined=true
runtime_mutation_performed=false
