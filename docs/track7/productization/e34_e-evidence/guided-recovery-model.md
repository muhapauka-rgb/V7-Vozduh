# E34.E Guided Recovery Model

guided_recovery_defined=true

## Recovery Principle

Guided recovery is a controlled operator path. It is not free-form shell debugging.

Every recovery starts read-only, determines scope, and permits mutation only through a separately certified operational procedure.

## Recovery Types

| Recovery type | Evidence | Safe recovery path | Forbidden shortcut |
| --- | --- | --- | --- |
| Server recovery | Host health, services, disk, memory, network, time sync, release identity, backup readiness. | Restore service health, verify runtime convergence, keep production blocked until checks pass. | Restart or reinstall without lineage and health verification. |
| Restore recovery | Backup object, backup fingerprint, restore logs, release identity, config fingerprint, audit lineage. | Retry from certified backup, reconstruct lineage if authorized, verify governance before READY. | Use uncertified backup or ignore lineage gaps. |
| Release recovery | Release manifest, release fingerprint, health checks, deployment lineage, rollback release. | Roll forward to fixed certified release or rollback to certified previous release. | Patch runtime directly without release identity. |
| Routing recovery | Required services, target readiness, routing intelligence proposal, current user routes, audit lineage. | Deny unsafe proposals, recalculate through routing intelligence, execute only through governance. | Direct route edits outside approved movement. |
| Governance recovery | Approval packets, locks, reservations, audit trail, restore-settle, selected moves, hidden movers. | Fail closed, clear certified stale state, restore invariants, verify audit continuity. | Bypass packet/replay/lock gates. |

## Recovery Flow

```text
detect problem
collect evidence
classify recovery type
select runbook
perform read-only diagnosis
authorize safe action
execute scoped recovery procedure
verify state
close or escalate
```

## Recovery Closure

Recovery is complete only when:

- runtime checkers pass;
- restore-settle is GO where relevant;
- fingerprints and lineage are known;
- audit trail records the recovery;
- forward execution gates remain fail-closed unless re-certified;
- operator receives a closure verdict.
