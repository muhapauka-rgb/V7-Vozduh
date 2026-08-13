Mission ID: `V7_OMP_BDP_65CB2232971BC224D937140C_V1`
Run Nonce: `rs0_65CB2232971BC224D937140C`

# V7 RS1 Responsibility Realignment Map

**Status:** `RESPONSIBILITY_REALIGNMENT_MAP_PASS_READ_ONLY`
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## Method and scope

This is the RS0-baselined, decision-oriented projection of existing PR2/PR2A
evidence, not a new audit corpus. Each row preserves the required chain
`surface -> owner -> caller/consumer -> state/effect -> target boundary ->
disposition`. RS0's source/deploy divergence is retained: all source findings
describe commit `44e075…`; deployed Runtime remains the separately observed
`b343732…` residual.

## V7_RESPONSIBILITY_REALIGNMENT_MATRIX

| Current responsibility | Existing owner | Real caller / primary consumer | State or effect | Target existing boundary | Disposition / exact residual |
| --- | --- | --- | --- | --- | --- |
| Core nft/ip apply and verify (`v7-routing-sync`) | Routing Core / deploy | routing-sync unit, path guard; kernel forwarding | fwmark rules, tables, verification | Data Plane | `KEEP`; replacement requires equal atomic apply, fence, fallback and traffic proof |
| Core decision contract (`admin_core/routing_core.py`) | Routing Core | shadow/certification adapters | effect-free plan | Control Plane -> Data Plane contract | `KEEP`; no duplicate live writer |
| governed plan and fallback movement (`v7-users-autoswitch`, `v7-user-switch`) | Planner, Authority, rollback | Matrix event consumer, governed/manual CLI | candidate plan, guarded movement, route verify, rollback | Control Plane / legacy fallback | `SHRINK_BY_RESPONSIBILITY`; preserve movement/recovery until equivalent consumer proof |
| planner-hosted topology/Polygon diagnostics | OMP/Polygon | explicit diagnostic CLI, tests | read-only evidence | Engineering Plane | `MOVE_TO_ENGINEERING_PLANE` candidate; function consumer map first |
| CPS consistency, continuation, Polygon and deploy helpers (`v7_sync_lib.py`) | CPS/OMP/deploy/truth | truth-check, safe-deploy, Matrix consumers, CI | engineering projections and atomic CPS writes | Engineering Plane interfaces | `SHRINK_BY_EXISTING_INTERFACE`; retain atomic CPS boundary |
| Admin HTTP dispatch and guarded actions | Admin/API and operator execution | admin service, browser, guarded POST routes | reads plus guarded action adapters | Management Plane -> existing Control Plane | `KEEP_ADAPTER`; no second policy/Authority owner |
| embedded Admin UI (`html_page_v2`) | Admin/UI | GET routes -> browser | presentation only | existing Admin/UI boundary | `MOVE_TO_UI_ASSET` candidate; compatibility/UI test required |
| Packet/lease/barrier/rollback (`operator_execution`) | operator-execution / Authority | governed cycle, packet CLI, admin adapters | exact safety records and bounded clearance | Control Plane safety boundary | `KEEP_SAFETY_BOUNDARY`; no obsolete proof |
| Matrix, sentinel, health and capacity observations | Matrix/Sentinel/health owners | timers, sentinel, admission readers | health/events/state projections | Control Plane | `KEEP`; map per-state writers before any merge |
| path guard repair chain | recovery / restore-barrier owners | 2-minute timer -> guarded repair | may invoke Core sync, safety repair and write state | Control Plane recovery | `LEGACY_EXCEPTION`; failure/Authority/recovery matrix required |
| Direct autosync | existing Direct owner | 10-minute timer -> DNS/config owner | Direct config and restart path | separate Control Plane product boundary | `KEEP_RUNTIME`; not a Core dependency |
| OMP, reports, learning, replay | existing OMP/report owners | asynchronous engineering consumers | historical/evidence outputs | Engineering Plane | `KEEP_OUTSIDE_RUNTIME`; no synchronous forwarding edge found |

## Conclusions, evidence and successor

| Conclusion | Evidence basis | Owner | Disposition | Residual | Next action |
| --- | --- | --- | --- | --- | --- |
| One primary routing writer is proven | PR2 Core/runtime package audit and RS0 baseline | Routing Core | retain narrow Data Plane | ordinary traffic remains unobserved in RS0 | RS1A targeted archaeology |
| Mixed responsibilities are real above the Core | PR2A function/caller/consumer mapping | existing component owners | candidate extraction only | no per-function migration proof yet | RS1A |
| Active runtime package is wider than M10's compact projection | PR1/PR2 plus RS0 runtime snapshot | deploy/package/Runtime owners | retain exact `DEPLOY_REQUIRED` gap | no package-minimality terminal | RS6 after preceding maps |
| No report/OMP/history synchronous edge into Core writer is proven | PR2 graph and Runtime chain inspection | OMP and Core owners | preserve plane separation | dynamic runtime paths remain separately classified | RS2 |

`RESPONSIBILITY_REALIGNMENT_MAP_PASS = PASS`. Exact successor:
`EXECUTE_RS1A_CODE_ARCHAEOLOGY_AND_TARGETED_DEEP_DEPENDENCY_AUDIT`.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`. Documentation/report LOC: `0 -> 55 -> +55`.
Files/functions/classes/entrypoints/dependency/state/Runtime/routing edges
added, removed or changed: `0 / 0 / 0`. Physical removal, logical exclusion
and responsibility move: `0 / 0 / 0`; classifications are not implementation.
`PROGRAMMATIC_CODE_EFFECT = NONE`.
