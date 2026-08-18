# Current VLESS Incident Truth Reconciliation

Mission: `CURRENT_ACTIVE_INCIDENT_TRUTH_RECONCILIATION`
Mission nonce: `2026-08-18T12:51:00Z-vless-current-vs-lineage`
Status: `PASS_WITH_NONBLOCKING_DEPLOY_RESIDUAL`

## Verdict

- Primary classification: `CLASS_D_WRONG_SCOPE_SEMANTICS`.
- Secondary classification: `CLASS_C_STALE_CURRENT_INCIDENT_PROJECTION`.
- CPS `unresolved=40` was neither current ordinary route scope nor the exact cumulative scope of its named incident.
- Current VLESS ordinary route-backed scope is `0`; enabled controlled-certification users on VLESS are `11` and remain a separate existing owner/lane.
- Fresh Matrix still observes VLESS degradation (`1/14` services reachable, `13` hard failures), but there is no current ordinary user incident to drain.
- Product evolution is not blocked by this closed incident. Existing OMP selected `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_48`; V5.3 was not manually admitted.

## Source and reconciliation

The stale CPS producer path was:

`CURRENT_VLESS_UNRESOLVED_SCOPE=40 -> reconcile_rs6_stale_frontier_to_existing_successor -> atomic_reconcile_cps -> OMP consumer`.

Runtime exposed seven legacy VLESS projections from 2026-08-08 through 2026-08-12. Each mixed an older all-user denominator (`15`, `24` or `34`) with the same current `11` certification users and therefore failed `affected = protected + unresolved + excluded` with `INCIDENT_SCOPE_ACCOUNTING_BROKEN`. The existing scope owner required certification count plus protected count to equal the historical denominator before closing ordinary intent. That equality incorrectly made historical membership the current ordinary action scope.

Repair:

- `tools/v7-users-autoswitch` now preserves the legacy denominator as history while classifying a live certification-only source as ordinary `unresolved=0` even when the historical denominator was larger.
- Existing passive-event/outcome reconciliation changed eight compact L3 records, created no Candidate/Packet/lease, performed no route mutation and moved zero users.
- `tools/v7_sync_lib.py` now treats causal-owner `PASS` with no open VLESS projection as authoritative empty current state instead of falling back to stale CPS.
- `tools/v7-truth-check` allows a bounded 90-second status refresh because the fresh Matrix/registry owner normally exceeded the former 30-second bridge timeout.
- CPS and its OMP pointer were updated atomically by the existing owner.

## Current versus cumulative

- Current open VLESS incident count: `0`.
- Current ordinary scope: `affected=0, protected=0, unresolved=0, excluded_or_recovered=0`.
- Current enabled certification scope on VLESS: `11`; current enabled non-certification scope on VLESS: `0`.
- Named stale CPS incident `sfinc_446bf16efcc9f0141973de8be6e558e6` is `INTENT_CLOSED/RECOVERED` since `2026-08-08T17:22:30.672991+00:00`.
- Its frozen historical denominator is `38`, terminal unresolved is `0`, excluded/recovered is `38`.
- Its provable packet-bound cumulative lineage is `0` (`NO_PACKET_BOUND_LINEAGE_YET`); it is explicitly not a current-source denominator. The stale CPS text `cumulative packet-bound lineage=39` was not supported by that incident owner.

## Verification and effects

- Focused scope/projection tests: `6 PASS`.
- Truth-check bridge tests: `30 PASS`.
- Full service-failure unit module: `104 PASS, 1 FAIL`; the single failure is the pre-existing unrelated controlled-target advisory expectation `STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED` versus `STOP_SAFE_NO_SAFE_TARGET`.
- Production causal integrity after repair: `PASS`, `open_incident_count=0`, `invalid_states=[]`.
- CPS after atomic reconciliation: `INCIDENT_FRONTIER=CURRENT_SOURCE_SCOPE_EMPTY`, `CURRENT_VLESS_UNRESOLVED_SCOPE=0`, `CURRENT_VLESS_INCIDENT_ID=NONE_OPEN`.
- OMP read-only continuation: `PASS`, exact next automatic action `CONTINUE_AVAILABILITY_FIRST_CONTROLLED_PRODUCTION_STAGE_48`, Runtime/production/user/Authority effects all `NONE`.
- Deployed core repair commits: `952f3582`, `c83530ea`; deploys `deploy-z8-14-Updatesystem-952f358-20260818T154412` and `deploy-z8-14-Updatesystem-c83530e-20260818T154711`.
- Additional top-level primary-frontier label alignment commit `eba15915` is pushed but not deployed because the external Codex execution-credit limit rejected the safe-deploy call. This does not change the already reconciled current incident scope or selected CPS execution frontier.

## Re-entry

Incident re-entry requires a new owner-backed VLESS service incident with a non-empty current ordinary route-backed source scope. Historical lineage, certification users, Matrix failures, tests or reports alone cannot reopen ordinary incident drain.

The existing Matrix consumer owns the stage-48 revalidation. It must still pass fresh inventory, target, capacity, allocation, Candidate, Packet, lease, restore-barrier, verification and ordinary-user-protection gates; no action was manufactured in this reconciliation.
