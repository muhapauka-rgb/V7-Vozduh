# V7_OPERATION_CONTROL_REENTRY_AND_SERIAL_APPLY_LATENCY_REPAIR

Date: 2026-09-03  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Current frontier: `RECOVERY_LATENCY_SLO`

## Current fingerprint and provenance

- Runtime/branch commit: `5dd5380d v7: retain runtime hot path through ordinary apply`.
- Deployed runtime fingerprint: `16bd864d1e1e5d99e53ffbc4bcafe10d4805eaff4259101447c5e69bb4862d71`.
- Local, GitHub `Updatesystem`, and Runtime hashes aligned after safe deploy
  `deploy-z8-14-Updatesystem-5dd5380-20260903T164257`.
- `v7-health.service` active after the deploy restart.

## Phase A — operation control and approved lock

### Root cause and repair

The failing VLESS ordinary path had a fresh exact Packet/Barrier but compared
its exact selected-move binding with a broader pre-Packet operation shape.  A
certification identity in that broader shape changed the count/hash, so the
existing rehydration owner treated the current Packet binding as stale and
stopped safe.  The repair keeps the immutable current Packet operation/id/hash
binding authoritative and normalizes only the stale broad pre-Packet shape.
It does not admit a foreign Packet, Barrier, lease, target, or selected-move
hash.

### Owner placement

| Object | Canonical owner | Final placement |
| --- | --- | --- |
| Current failure/source scope | Matrix / health owner | Current Matrix binding before execution |
| Candidate/Packet/Lease/Barrier | Existing governed execution owners | Exact operation-scoped lineage |
| Approved selected-move binding | Existing approved-plan-lock owner | Exact Packet move hash only |
| Operation control window | `admin_core/operator_execution.py` | Exact Packet/lease operation only |
| Re-entry | Existing Matrix/health invalidator path | New current lineage only; no old control reuse |

No new owner, queue, scheduler, Planner, Matrix, Authority, route writer, or
state source was created.

### Live proof before this deploy

The normal V7 Runtime automatically completed an ordinary VLESS recovery:

- source: `vless`;
- final verdict: `L3_PRODUCTION_PROVEN`;
- downstream governed Apply present and successful;
- ordinary registry assignments moved to
  `wireguard-1779454504-c43409` through the normal governed chain;
- certification identities remained isolated on their certification sources.

This proves `OPERATION_CONTROL_CURRENT_REENTRY_CONSUMED` and
`APPROVED_PLAN_LOCK_CURRENT_BINDING_CONSUMED` for the repaired lineage.  It
does not give SLO credit to any manual action.

### Current re-entry observation

After the semantic deploy restarted health, a separate in-flight ordinary
lease was terminalized as `OPERATOR_CANCELLED` without route mutation.  The
current canonical `service-matrix.json` has no fresh profile-required failure
binding: all relevant Matrix failure observations are older than the existing
ten-second live-evidence limit.  Therefore health correctly does not replay
that historical evidence or create a new Candidate/Packet/Lease.

The compact `service-matrix-refresh-summary.json` still contains an old
`current_failed_source_scope` projection even though it is not actionable by
the health consumer.  This is an explicit projection-freshness residue to
reconcile in the existing Matrix summary owner; it is not a lawful reason to
replay or manually advance recovery.  Thus the Phase-A post-terminal status is
`POST_TERMINAL_OPERATION_RESIDUE_PASS` for the successful exact lineage, with
this separately recorded stale-summary cleanup residual.

## Phase B — serial Apply latency

### Measured current shape

The newest successful ordinary three-member receipt showed:

| Measure | Observed value |
| --- | ---: |
| Matrix consumer to governed dispatch | 643.633 ms |
| Bounded consumer to governed dispatch | 338.080 ms |
| Exact inner Apply and S11 | 7,852.880 ms |
| Low-level route-writer calls | 3 |
| Route-writer spans | 615.290 / 804.699 / 637.967 ms |
| Exact per-member route visibility | 288.015 / 367.831 / 479.363 ms |
| Exact cohort Core-primary commit | 1; 346.683 ms |
| Whole-system Core-primary rebuilds | 0 |
| Required-service verifier groups | 1 compatible target/profile group |

The receipt's larger `apply_and_verification` total of 41,166.888 ms included
post-S11 passive/learning finalization, not required recovery completion:

- passive event consumption: 18,105.797 ms;
- learning closure: 14,735.680 ms.

### Repair

The ordinary governed L3 caller did not pass its existing
`runtime_hot_path_only` contract to `run_autoswitch_apply`.  Consequently the
existing, safe post-S11 deferral branch was unavailable to exactly this
ordinary path.  Commit `5dd5380d` propagates that existing flag.

The existing `AutoswitchPlanner.finalize_operation` now defers only those
noncritical finalizers after exact ordinary Packet S11.  Current-data,
Authority, Packet/Lease/Barrier, route, assignment, and required-service S11
checks remain synchronous.  No route writer or recovery owner was added.

### Structural before/after

| Surface | Before | After |
| --- | ---: | ---: |
| `v7-user-switch` calls for 3 identities | 3 | 3 |
| Whole-system Core-primary rebuilds | 0 | 0 |
| Exact cohort Core-primary commits | 1 | 1 |
| Required-service verifier groups | 1 | 1 |
| Post-S11 synchronous passive + learning work | about 32.84 s | deferred through existing owner |

The remaining required P1 is serial identity policy-table/default-route
mutation and exact per-identity route visibility.  The existing cohort
primitive already collapses Core-primary and required-service work.  Replacing
the remaining N identity mutations with one mutation would require a new batch
route-writer contract, which this Mission forbids.  Therefore
`SERIAL_COHORT_APPLY_AMPLIFICATION` is not consumed and remains the explicit
`CURRENT_DATA_PLANE_SERIAL_IDENTITY_MUTATION_BOUNDARY`.

## Regression and deploy

Focused regressions passed:

- runtime-hot ordinary recovery passes the hot-path flag;
- hot-path propagation remains ordinary-only;
- noncritical finalization is deferred only after exact S11;
- persistent Matrix owner cannot lose that deferred-finalization contract.

An affected 409-test run had two unrelated pre-existing failures outside this
diff: one stale test expectation for preserved source identity and one test
stub that never receives its expected in-process call.  Neither hides or is
changed by this repair.

## SLO and next action

`RECOVERY_LATENCY_SLO` remains active.  The prior 7,852.880 ms exact inner
Apply is above the 7,000 ms P95 target, and there is no fresh post-`5dd5380d`
ordinary Runtime receipt to claim a new timing result.  The next lawful action
is to wait for a fresh V7-originated actionable failure binding, observe the
normal chain without manual advancement, and measure the new S11 boundary.
Any further reduction of serial identity mutation requires a separate,
explicit Data Plane architecture decision.
