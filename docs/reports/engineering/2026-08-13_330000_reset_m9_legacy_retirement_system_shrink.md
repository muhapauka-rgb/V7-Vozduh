# RESET-M9 Legacy Retirement, System Shrink and Program Cleanup Engineering Report

Status: `RESET_M9_LEGACY_PRIMARY_RETIREMENT_AND_SYSTEM_SHRINK_PASS`

## Disposition

This report consumes the exhaustive object ledger and semantic classifications in `V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`; it does not duplicate that inventory.

| Surface class | Disposition | Evidence and retained meaning |
| --- | --- | --- |
| Core nft source-to-class maps, class route tables, six fwmark rules and `v7-routing-sync` single writer | `STILL_REQUIRED` | current primary production dataplane and restart owner |
| 124 legacy per-user source rules plus 124 per-user default routes | `DELETE` | physically removed after Core verification; exact fallback rebuilt them once, was verified, then Core was reapplied and retired them again |
| `legacy_sync`, users/egress registry inputs and exact fallback command | `LEGACY_EXCEPTION_REQUIRED` | compact deterministic fallback builder; not active primary surface |
| `v7-users-autoswitch`, `v7-user-switch`, governed Packet/lease/barrier, route/payload verification, rollback/recovery functions | `LEGACY_EXCEPTION_REQUIRED` | protected safety/Authority and explicit movement/fallback semantics; excluded from Core hot path |
| Matrix, sentinel, quality and production observation CLIs/services/timers | `STILL_REQUIRED` | real async observation/event consumers; not Core dataplane owners |
| `v7-autoswitch-planner.service/timer` | `STILL_REQUIRED` | despite legacy name, deployed unit consumes existing failure events only; it neither owns the Core maps nor performs an unconditional second Planner pass |
| inactive `v7-users-autoswitch.timer`, manual service and installer surface | `LEGACY_EXCEPTION_REQUIRED` | timer remains held/inactive as an explicit governed recovery surface; no primary authority |
| OMP, CPS, canonical truth, System Map, policy/Authority and audit owners | `STILL_REQUIRED` | development-plane, volatile-state, durable-truth, topology and Authority boundaries unchanged |
| duplicate capacity/health/incident projections and historical closure ledgers | `MERGE` | current facts enter compact generation-bound receipts; retained records are historical evidence, not Runtime truth |
| governed campaign, canary, preview and test helpers | `LEGACY_EXCEPTION_REQUIRED` | acceptance/safety corpus only; no Core hot-path caller |
| admin/read-model modules and reports | `STILL_REQUIRED` | asynchronous presentation/evidence consumers, not routing truth or decision authority |
| superseded Program identities accepted by RESET-M1 | `MERGE` | intent and evidence remain in OMP/canonical owners; documents remain historical artifacts rather than active parallel contracts |

No protected evidence, safety control, rollback/recovery path, Authority gate, owner boundary, Program order or migration invariant was deleted.

## Physical shrink

| Metric | Before | Current | Delta |
| --- | ---: | ---: | ---: |
| compatible-user primary source rules | 124 | 0 | -124 |
| compatible-user primary default route tables | 124 | 0 | -124 |
| Core class mark rules | 0 | 6 | +6 |
| Core class default route tables | 0 | 6 | +6 |
| simultaneous primary routing representations | 2 | 1 | -1 duplicated responsibility |
| primary individualized kernel routing objects | 248 | 12 | -236 (-95.2%) |
| Runtime owners/processes/timers added by Reset | 0 | 0 | 0 |

The remaining 124-member nft membership map is required address-to-class indexing, not 124 routing decisions or route tables. A class target change remains one bounded class-table update. The primary path contains no OMP/report/audit/campaign synchronization.

## Production proof

- Shrink apply: `rules_removed=124`, `routes_removed=124`; post-verify `legacy_primary_rules_present=false`.
- Core consumer: `10.7.0.114`, mark `0x202`, route table `202`, device `awg3`.
- Fallback: `CORE_PRIMARY_FALLBACK_PASS`, `mutations=124`; representative legacy table `1112`, device `awg3`.
- Final state: Core reapplied; `CORE_PRIMARY_VERIFY_PASS`; legacy primary rules absent; fallback ready.

## Closure

- Intent closed: legacy is no longer the primary kernel routing surface; the production surface is physically smaller while exact fallback semantics remain.
- Owners affected: existing routing writer/kernel owners and CPS/OMP projections only.
- Residual: none for RESET-M9. Natural future traffic counters remain operational observation, not a Reset completion dependency.
- Successor: Program completion evaluation.
- Runtime effects: `LEGACY_PRIMARY_KERNEL_SURFACE_RETIRED`.
- Production effects: `CORE_PRIMARY_REMAINS_ACTIVE; 236_NET_PRIMARY_KERNEL_OBJECTS_REMOVED`.
- Authority effects: `NONE_BEYOND_CONSUMED_M8_SCOPE`.

Terminal: `RESET_M9_LEGACY_PRIMARY_RETIREMENT_AND_SYSTEM_SHRINK_PASS`.
