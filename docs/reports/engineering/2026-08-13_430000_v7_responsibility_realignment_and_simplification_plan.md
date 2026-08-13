# V7 Responsibility Realignment and Simplification Plan

**Status:** `RT2_PR2C_RESPONSIBILITY_REALIGNMENT_AND_SIMPLIFICATION_PLAN_PASS_READ_ONLY`
**Scope:** `RT2-PR2C` in `OPERATIONAL_MATURITY_PROGRAM`; plan only.
**Inputs:** PR1 production-reality baseline, PR2 surface audit, PR2A responsibility graph, PR2B alignment audit, `FINAL_ARCHITECTURE_MAP`.
**Owner boundary:** existing component, safety, Authority, Work Placement, Runtime Model, CPS/OMP and canonical architecture owners.
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## Decision

The evidence supports a responsibility-realignment plan before any `RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION`. It does not authorize a mutation, a new owner, a new Runtime component, a new truth source, or a new document framework.

The governing model remains:

```text
Management Plane: Admin UI/API -> guarded request and read model only
Control Plane: Matrix/Sentinel/health -> policy -> bounded movement/recovery decision
Data Plane: routing-sync -> nft/ip apply -> verification
Engineering Plane: OMP/Polygon/reports/certification -> asynchronous evidence only
```

Existing owners retain their boundaries. A target responsibility below means an existing boundary in which an already-proven responsibility belongs; it never creates an owner.

## Logical simplification matrix

| Component / surface | Current responsibility and material gap | Target responsibility / existing boundary | Plan classification | Migration, validation and old-path closure condition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | Bounded fallback, rollback, governed execution and some diagnostics/certification are co-located. Removing or moving its safety path would be unsafe. | Preserve movement, rollback, recovery and governed execution under existing safety/Authority boundaries. Diagnostics, certification helpers and engineering evidence may move only to existing Engineering Plane owners. | `KEEP` safety path; `SHRINK`/`MOVE` candidate for proven non-Runtime helpers. | First prove every helper's caller, consumer and state/effect. Then admit a separate existing OMP/CPS mutation, preserve rollback and test the real consumer. Retire old helpers only after imports, CLI/subprocess callers, units, deploy/install configuration, state, locks/leases/barriers, recovery, dashboards, tests and documents have no live dependency. |
| `v7_sync_lib.py` | CPS continuation, OMP/Polygon, deploy and truth-facing interfaces are co-located; file size alone is not a defect. | Keep authoritative interfaces with their existing CPS/OMP/Polygon/deploy/truth boundaries; reduce mixed presentation or diagnostic responsibility only where evidence proves a safe destination. | `SHRINK`/`MOVE` candidate; no new shared library. | Map function -> caller -> consumer -> durable state -> side effect before a separately admitted migration. Require compatibility validation and old import/path closure before any deletion. |
| Admin API / UI dispatch / read model / guarded action | Presentation, API dispatch, read projection and guarded action can be adjacent, creating a risk that management presentation reaches routing effects directly. | Existing Management Plane UI/API boundary for presentation and read model; existing guarded action and Authority/safety boundary for mutations. | `SHRINK`/`MOVE` candidate; guarded action remains `KEEP`. | Separate only after route/UI/consumer and Authority-fencing proof. Preserve backward-compatible callers during migration. Remove old embedded presentation/action tails only after live consumer conversion and residue proof. |
| Operator execution / governed action path | Safety boundary, command execution and recovery coupling are necessary for bounded operator action. | Existing safety, Authority, movement-protection and recovery owners. | `KEEP`; later helper extraction only if independently proven. | No simplification may weaken Authority checks, rollback or recovery. Any future helper move requires affected-owner tests, safe deploy and production verification. |
| Active path guard | Recovery invocation and path protection remain coupled to an existing runtime safety boundary; its exact present consumer must be proven before narrowing it. | Existing recovery and safety boundary; no Engineering Plane substitution. | `LEGACY_EXCEPTION` pending exact failure-matrix and Authority-state proof. | Retain unchanged until PR3-or-later admitted work proves real callers/consumers, failure behavior and replacement closure. No removal merely because it is historical-looking. |
| Direct autosync | Direct-path synchronization/control responsibility is distinct from Routing Core and may be runtime-required. | Existing Direct/control-plane boundary and Runtime package owner. | `KEEP` pending package-truth reconciliation. | Establish deployed consumer, startup dependency, imports and real product effect. Only then may a later admission classify a helper as `SHRINK` or `engineering_only`; no Core expansion. |
| Health Matrix / Sentinel | Health production, fencing and consumers must remain explicit; a health surface cannot become a synchronous Engineering Plane dependency. | Existing Matrix/Sentinel, health, capacity, policy and admission owners in Control Plane. | `KEEP`; `SHRINK_REVIEW` for duplicate projections only. | Identify each writer, reader, freshness/fencing rule and routing consumer. A duplicate projection can be removed only after retained owner mapping, recovery behavior and residue proof pass. |

## Required physical-plan evidence for every future mutation

The matrix above is the single logical plan output. It must be updated through the existing canonical Program/report path rather than copied into new manifests, generators or maps. A later owner-backed change must record:

1. `BEFORE -> AFTER -> DELTA` for files, LOC, imports, callers, consumers, state surfaces, services/timers/processes and dependency edges.
2. The exact old lifecycle end and new lifecycle beginning, joined by consumer, migration and cleanup proof.
3. `NO_DANGLING_LEGACY_RESIDUE_PASS` over static imports, dynamic imports, CLI/subprocess callers, systemd/cron units, deploy/install configuration, state/locks/leases/barriers, rollback/recovery, nft/ip paths, dashboards, tests and documents.
4. The actual real consumer and, where applicable, affected-owner tests, safe deployment, CPS/canonical reconciliation and production verification.

`runtime_excluded`, `engineering_only` and `fallback_only` are logical classifications; none may be reported as physical removal until the physical closure evidence is complete.

## Authorization and successor

```text
PR2C PLAN
  -> existing OMP/CPS admission with exact owner-backed disposition
  -> separately authorized mutation and validation
  -> old-path closure and NO_DANGLING_LEGACY_RESIDUE_PASS
  -> RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION
```

`NO_CHANGE_AUTHORIZATION_FROM_PLAN` applies. This report makes no code, Runtime, CPS, production, Authority, deployment or migration-state change. The next contractual successor is `RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION`, but only after the existing OMP/CPS admission and exact owner-backed mutation disposition required by the Program.

## Why this closes the present risk

PR2A and PR2B identified mixed responsibilities and valid retained safety paths. Planning their separation before package simplification prevents a cosmetic LOC reduction, a new parallel subsystem, or accidental removal of fallback/recovery behavior. It preserves the evidence depth of the audit while making each future change prove its consumer, owner boundary, transition and residue closure.

## Programmatic delta

| Metric | Value |
| --- | ---: |
| Production source files changed | 0 |
| Production source LOC added/removed | 0 / 0 |
| Runtime services, timers or processes changed | 0 |
| Runtime dependency edges changed | 0 |
| Files deleted, moved or archived | 0 / 0 / 0 |
| Program-contract rows added | 1 (`RT2-PR2C`) |
| Engineering reports added | 1 (this logical plan) |
