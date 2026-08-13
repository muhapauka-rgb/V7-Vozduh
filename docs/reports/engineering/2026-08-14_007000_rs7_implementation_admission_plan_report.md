# RS7 Implementation Admission Plan Report

**Decision:** `NOT_READY`
**Selected conditional candidate:** `ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1`
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## 1. CPS successor and scope

CPS Section 0 remains authoritative:

```text
ACTIVE_PROGRAM = V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1
CURRENT_STAGE = RS6_RUNTIME_PACKAGE_MINIMIZATION
SUCCESSOR = EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION
```

RS7, RS7A, RS8 and RS9 already define the First Implementation Candidate,
Product Contract, Hot Path, responsibility-split, consumer migration, old-path
closure and physical-delta gates. The Program was strengthened in place with
one logical admission-plan rule; no new phase, Program, owner, truth source,
registry or audit framework was created.

The existing knowledge graph (`3,585` nodes / `3,979` edges) was used only for
orientation because its analyzed commit predates current `HEAD`. Every value
used for selection was rechecked against current source, current canonical
owners and the accepted RS reports. Graph presence, file size and static
imports are not treated as current Runtime evidence.

## 2. RS6 closure summary

RS6 classification is bounded, but physical admission is not open. The final
RS6 closure reports `NOT_READY_FOR_RS6_PHYSICAL_MINIMIZATION` and
`REMOVE_CANDIDATE = NONE`; live provenance/lifecycle residuals retain exact
existing owners and re-entry conditions. This plan therefore selects a
candidate conditionally but cannot advance CPS or authorize implementation.

## 3. Candidate inventory

| Component / slice | Current responsibility and layer | Existing owner / current consumers | Complexity signal | Risk | Possible action / classification |
| --- | --- | --- | --- | --- | --- |
| `tools/v7_sync_lib.py` | Engineering: CPS/OMP consistency, Polygon, truth/convergence, deploy/release and service-failure continuation | existing CPS/OMP/deploy/truth owners; at least nine executable importers, including `v7-truth-check`, safe deploy/sync tools and Runtime-related `v7-service-matrix-refresh-all` | `25,475` LOC, `289` functions, several 500–1,996 LOC functions, mixed lifecycles | medium/high | `MOVE` only per coherent existing-owner interface; not first |
| `admin/v7-admin-api` whole file | Management plus guarded Control adapters and embedded UI | existing Admin/API, guarded-action and read-model owners; browser/public gateway/operator consumers | `41,024` LOC, `687` functions, `2` classes, `279` endpoints; size alone is not a split reason | medium | `SHRINK` / `MOVE` in separately proven slices |
| Admin operator read-model wrapper slice | Management read-only façade over existing `admin_core/operator_views.py` | Admin API and existing operator read-model owner; internal P2.7 composition plus operator endpoints | `10` two-line wrappers, `22` in-file call sites and one redundant call hop | low | `SHRINK` + `MERGE`; selected conditionally |
| embedded `html_page_v2` | Management UI presentation inside API source | Admin UI/API; `Handler.send_html_v2` and browser | one `16,528`-line literal UI function | medium | later `MOVE`; not first because it adds a deployable module/file edge and is not physical shrink by itself |
| `tools/v7-users-autoswitch` | Control/recovery fallback, planner, governed movement, rollback, diagnostics and certification | autoswitch, safety, Authority and rollback owners; Admin actions, manual/systemd paths and OMP consumers | `23,639` LOC, `66` functions, `4` classes; several 600–2,241 LOC functions cross safety boundaries | high | engineering-only `MOVE` later; fallback remains `LEGACY_EXCEPTION`; not first |
| state-merge/path-sanity/API/benchmark/MSS/proxy provenance residuals | live Control/Management/Data support | exact component and deploy/package owners | incomplete source/deploy evidence | unknown/high | `OWNER_BACKED_EXCEPTION`; not an implementation candidate |
| retained autoswitch backup executables | legacy residue with no proved current consumer | autoswitch and deploy/package owners | dynamic/manual lifecycle unproven | unknown | `OWNER_BACKED_EXCEPTION`; no removal admission |

## 4. Candidate comparison

| Criterion | sync library interface extraction | Admin wrapper collapse | autoswitch engineering extraction |
| --- | --- | --- | --- |
| Runtime/routing risk | medium/high: deployed library and Runtime-related importer | low: read-only Management projection; no routing writer | high: movement, recovery, rollback and Authority-adjacent paths |
| Observability | high, but broad test/consumer surface | high: deterministic payloads, endpoint inventory and focused tests | high, but safe proof requires recovery/rollback coverage |
| Existing owner | multiple coherent owners require per-interface split | exact Admin API + `admin_core/operator_views.py` | exact owners exist but boundaries are safety-sensitive |
| Consumer clarity | many CLI/test/Runtime-related consumers | `22` current in-file calls; no executable external caller of the local wrapper names found | multiple CLI, API, timer/manual and continuation consumers |
| Before/after measurability | broad and costly | exact functions, calls, hop and response equality | broad and safety-dependent |
| Rollback | multi-consumer revert/deploy | single source revert and Admin-only redeploy/restart | movement/recovery rollback semantics involved |
| First-candidate verdict | reject | select conditionally | reject |

## 5. Selected first candidate

```text
TARGET_COMPONENT = admin/v7-admin-api
TARGET_SLICE = ten operator read-model wrapper functions
ACTION = SHRINK + MERGE
TARGET_EXISTING_OWNER = admin_core/operator_views.py
```

Current chain:

```text
Handler / P2.7 read-model composition
  -> local admin wrapper
  -> admin_core.operator_views
  -> admin_core.operator_observability / execution pipeline
  -> read-only response
```

Target chain:

```text
Handler / P2.7 read-model composition
  -> admin_core.operator_views with the same explicit roots/arguments
  -> admin_core.operator_observability / execution pipeline
  -> byte/structure-equivalent read-only response
```

The selected slice excludes HTML, auth, CSRF, safe-mode policy, guarded
actions, routing, path guard, recovery, rollback semantics, Runtime state and
Authority. It creates no file, module, owner, state, writer or decision path.

## 6. V7_IMPLEMENTATION_ADMISSION_PACKET

| Field | Value |
| --- | --- |
| `TARGET COMPONENT` | `admin/v7-admin-api` operator read-model façade only |
| `CURRENT STATE` | ten local wrappers bind existing roots/arguments and immediately delegate to `admin_core/operator_views.py`; 22 current calls |
| `PROBLEM` | redundant façade functions add a duplicate naming/trace hop and obscure the already canonical read-model owner |
| `WHY CHANGE NOW` | lowest routing risk, clear owner/consumers, deterministic outputs, bounded diff and rollback; matches Management/Admin-first risk priority |
| `TARGET STATE` | all current callers invoke the existing `operator_views` functions directly with identical arguments; local wrappers absent |
| `RESPONSIBILITY CHANGE` | no behavior/owner transfer; remove duplicate Admin-local delegation responsibility and expose existing owner directly |
| `CURRENT CONSUMERS` | P2.7 candidate approval/governance/rehearsal composition and 15 operator read endpoints; all remain within `admin/v7-admin-api` |
| `MIGRATION PLAN` | record fresh before hash/counts; replace 22 calls; run response/endpoint tests; only then remove ten definitions in the same atomic change |
| `VALIDATION PLAN` | compile; focused operator/P2.7/endpoint tests; endpoint inventory equality; wrapper-call residue search; deterministic before/after payload equality; local truth and safe-deploy dry run |
| `ROLLBACK PLAN` | revert the single implementation commit; if separately deployed, restore previous safe-deploy Admin binary and restart only `v7-admin-api.service`; verify the same read endpoints |
| `RESIDUE CHECK PLAN` | zero definitions/calls of the ten local wrappers in executable source; no endpoint/RBAC/CSRF/safe-mode change; historical reports remain historical evidence |
| `EXPECTED COMPLEXITY DELTA` | `-10` local functions and `-10` redundant delegation hops; `22` call sites migrated; files/modules/owners/state/writers/endpoints/services/timers/routing edges unchanged |

## 7. Immutable affected-scope BEFORE measurement

| Metric | Before |
| --- | ---: |
| `admin/v7-admin-api` LOC | `41,024` |
| files in implementation slice | `1` product source file |
| top-level functions / classes in Admin | `687 / 2` |
| selected local wrappers | `10` |
| selected wrapper definition LOC | `20` |
| selected current call sites | `22` |
| Admin endpoints | `279` (`126 GET`, `10 HEAD`, `143 POST`) |
| action handlers / RBAC mappings | `138 / 138` |
| state surfaces added by slice | `0` |
| Runtime writers / routing writers | `0 / 0` |
| owners | existing Admin API and operator read-model owners |
| hot-path impact | `NONE`; Management read-only projection only |

Baseline validation passed: Python compilation; `25` focused unit/contract
tests; endpoint inventory; Admin static review with `0` critical findings.
Existing safe-mode classification warnings are outside the selected slice and
must remain unchanged rather than being folded into this implementation.

## 8. Migration safety and rollback

```text
OLD RESPONSIBILITY
  local binding wrappers for existing read models
    -> TARGET RESPONSIBILITY
       direct explicit binding at each current Admin consumer
         -> EXISTING OWNER
            admin_core/operator_views.py
              -> CONSUMER MIGRATION
                 all 22 calls in one atomic patch
                   -> VALIDATION
                      payload + endpoint + focused tests
                        -> OLD PATH CLOSED
                           zero wrapper defs/calls
```

The implementation must stop if any wrapper has an executable external
consumer, any payload differs without an accepted Product Contract reason, an
endpoint/RBAC/CSRF/safe-mode map changes, or safe deploy requires a component
other than the existing Admin package. No compatibility wrapper may remain
indefinitely; failure rolls the whole slice back.

## 9. Risks and validation gates

| Risk | Required proof |
| --- | --- |
| lost implicit `REPO_ROOT` / `STATE_DIR` / `EVENT_DIR` binding | every migrated call passes the exact existing arguments; deterministic payload equality |
| accidental endpoint behavior drift | endpoint count/path/method/auth/risk inventory unchanged; focused Handler tests pass |
| hidden external wrapper consumer | source/AST search across executable scopes returns none before removal and zero residue after |
| Admin production regression | separate OMP/CPS admission, safe-deploy dry run, explicit Admin-only restart, authenticated read-only smoke and rollback readiness |
| scope expansion into actions/safety | diff gate rejects changes outside the ten wrappers, their exact call sites and necessary focused tests |

`PRODUCT_CONTRACT_PRESERVATION_GATE`: unchanged endpoint paths, auth, payload
semantics and operator visibility. `HOT_PATH_PROTECTION_GATE`: non-applicable
after proving no recovery/routing edge; no global latency ritual is created.
`RESPONSIBILITY_SPLIT_QUALITY_GATE`: passes only if the redundant façade hop is
actually removed; LOC alone is not success.

## 10. Expected complexity delta

The expected class is `PHYSICAL_REDUCTION` of ten function definitions plus
dependency-hop simplification inside one existing component. Total file count,
module count, owner count, state surfaces, writers, endpoints, services,
timers, processes and routing objects remain unchanged. Exact added/removed
LOC and edges must be mechanically recalculated after implementation; the plan
does not pre-claim net LOC reduction.

## 11. Decision and exact re-entry

```text
NOT_READY
SELECTED_CANDIDATE = ADMIN_OPERATOR_READ_MODEL_WRAPPER_COLLAPSE_V1
CODE_CHANGE_AUTHORITY = NONE
```

Exact blockers:

1. CPS remains at `RS6_RUNTIME_PACKAGE_MINIMIZATION`; RS7 is not admitted.
2. `RUNTIME_PROVENANCE_CLOSURE_PASS` / `RUNTIME_PACKAGE_MINIMAL_PASS` are not
   established as passing; the final RS6 report remains `NOT_READY`.
3. The selected slice still requires a separately admitted OMP/CPS Mission,
   exact Admin/read-model owner acceptance and a fresh affected-scope baseline.
4. Production implementation additionally requires an Admin response baseline,
   safe-deploy plan and explicit Admin-only rollback/restart proof.

Re-enter this same plan—without repeating broad archaeology—when those four
conditions are satisfied. The next CPS successor remains
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; physical implementation was not
performed.

## PROGRAMMATIC_CHANGE_DELTA

Program contract: `+11/-0` documentation lines; one bounded admission-plan
paragraph added. Engineering report: `+212/-0` documentation lines; this file
added. Product/test/generated code LOC, functions, classes, entrypoints,
dependency/state/Runtime-package/routing edges, services, timers, processes
and production files changed: `0`. Physical removal, logical exclusion and
responsibility move performed: `0 / 0 / 0`.
