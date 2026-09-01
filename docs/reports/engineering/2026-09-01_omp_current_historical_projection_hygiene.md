# OMP current/historical projection hygiene

Date: 2026-09-01  
Scope: the P1/P2 document-only corrections identified by the full OMP audit. No Runtime, Matrix, Planner, Authority, health cadence, route, client, timer or production configuration changed.

## Change consumed

`OMP_CURRENT_HISTORICAL_PROJECTION_HYGIENE = CONSUMED`.

The OMP was updated from `4.87` to `4.88` only to make existing truth ownership easier to read correctly:

1. Header report references that were historical are now labelled historical; the header no longer carries an independent “current active Mission” value.
2. The V4.86 non-admission wording is labelled `HISTORICAL_REGISTRATION` and points to CPS/OMP §26 for its later/current disposition.
3. OMP §20.2 and §26 now explicitly state that they are CPS-derived projections, updated only by the existing atomic reconciliation owner and machine-validated; neither is an independent truth source.
4. V4.87 is named the common simplification law. RT2 §28.9 and RS7 §47.3 are explicitly specialized gates, not separate programs or schedulers.

## Verification and next action

```text
CPS section 0
-> existing atomic CPS/OMP reconciliation owner
-> OMP §20.2 + §26 derived projections
-> one current Recovery Stability Foundation frontier
```

The correction preserves all fail-closed, consumer-migration, rollback, hot-path-protection and no-duplicate-owner laws. It supplies no Runtime effect and grants no implementation or recovery authority.

Resume the existing `RECOVERY_STABILITY_FOUNDATION` only from CPS section 0. A future repair must be a measured generic recovery-lifecycle defect through the existing Matrix/health reconciliation consumer; it must not use a historical OMP paragraph as a runtime instruction.
