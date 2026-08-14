# V7 Next Bounded Simplification Candidate Report

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**Discovery type:** `READ_ONLY_BOUNDED_CANDIDATE_DISCOVERY`  
**CPS successor:** `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Runtime / Production / Authority effects:** `NONE / NONE / NONE`

## 1. Current frontier and completed input

CPS Section 0 remains unchanged: the active Program is the V7
responsibility-realignment/simplification Program, its current stage is
`RS6_RUNTIME_PACKAGE_MINIMIZATION`, and its exact successor is
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`. The completed Evidence Repository
Retention Mission is Historical Evidence only; it does not create a new active
Mission or bypass RS6/OMP/CPS admission.

This discovery reused the current knowledge graph, System Reality and Physical
Shrink evidence, the RS6 bounded-consumption rule, the completed Admin wrapper
Mission and the sync-library readiness evidence. It did not reopen RS1A/RS6,
scan Runtime as a removal target, or treat file size as a verdict.

## 2. Candidate matrix

| Component | Responsibility / existing owner | Layer | Callers / consumers / effect | Risk and delta | Disposition |
| --- | --- | --- | --- | --- | --- |
| `admin/v7-admin-api:capacity_pool_row` | duplicate local delegation to existing `admin_core.diagnostic_views.capacity_pool_row` | `MANAGEMENT` | `0` internal callers; `0` test callers; no string/dynamic reference; the existing target is a pure capacity read-model builder, so this wrapper has no state, Runtime or Product effect | low; remove `1` function / `2` source LOC / one unreachable delegation edge; one-commit revert | `READY_FOR_MISSION` |
| `admin/v7-admin-api:traffic_zero_summary` | local delegation to existing `diagnostic_views` owner | `MANAGEMENT` | `2` internal callers and one direct module-level test; feeds a user-visible diagnostic fallback response | known read-only effect, but endpoint behavior and test migration must be baselined | `NEEDS_MORE_EVIDENCE` |
| `admin/v7-admin-api:client_speed_summary` | local delegation to existing `diagnostic_views` owner | `MANAGEMENT` | `1` internal dashboard-summary caller and one direct module-level test | known read-only effect, but dashboard payload equivalence must be baselined | `NEEDS_MORE_EVIDENCE` |
| six registry wrappers (`parse_registry`, `egress_registry_rows`, `egress_registry_map`, `egress_exists`, `default_egress_id`, `egress_interface`) | local `STATE_DIR` adapters over existing `admin_core.admin_registry_views` owner | `MANAGEMENT` | `84` internal calls in aggregate; `egress_interface` is monkey-patched by a focused test; several callers are guarded action handlers | bounded cluster but not a first low-risk slice; consumer/test migration and action-path equivalence required | `NEEDS_MORE_EVIDENCE` |
| `tools/v7_sync_lib.py` interface extraction | mixed existing CPS/OMP/truth/deploy owner boundaries | `ENGINEERING` | real deploy/truth/OMP/Matrix consumers; no single coherent interface with complete migration proof | broad split would violate bounded scope; earlier unreachable helpers are already removed | `NOT_A_CANDIDATE` |
| RS6 Runtime exceptions | existing health, recovery, Direct, package/deploy and Runtime owners | `CONTROL` / `DATA` | current services/timers/state/recovery effects remain retained or owner-backed exceptions | Product/safety/recovery impact; no `REMOVE_CANDIDATE` | `KEEP` |

## 3. Recommended next Mission

```text
ADMIN_CAPACITY_POOL_WRAPPER_REMOVAL_V1
```

**Scope:** remove only the local `capacity_pool_row` definition in
`admin/v7-admin-api` (lines 9399–9400 at discovery). No call-site migration is
needed because no caller exists. The target owner already exists:
`admin_core.diagnostic_views.capacity_pool_row`.

**Admission packet required before implementation:**

```text
CURRENT: unreachable local two-line delegation wrapper
TARGET: no local wrapper; existing diagnostic_views owner unchanged
CONSUMERS: none proven in source, tests, imports, strings or dynamic lookup
VALIDATION: Python compile; exact residue search; focused Admin-module import
ROLLBACK: revert the single implementation commit
EXPECTED_DELTA: -1 function; -2 source LOC; one dead delegation edge removed
FORBIDDEN_EFFECTS: endpoint/auth/RBAC/CSRF/safe-mode/actions/routing/state/runtime/Authority
```

The candidate is ready **for existing OMP/CPS Mission admission**, not for
automatic implementation. It does not change the global RS6 completion state.

## 4. Rejected scope and exact re-entry

No Runtime, recovery, Authority, routing-Core or large-file split candidate is
admitted by this report. `traffic_zero_summary` and `client_speed_summary`
re-enter only after an endpoint payload baseline and test-consumer migration
plan. The registry-wrapper cluster re-enters only after all 84 call sites and
the `egress_interface` monkey-patch have an exact behavior/rollback plan.
`v7_sync_lib.py` re-enters only after one existing-owner interface has full
caller, consumer, deploy, state/effect, validation and rollback proof.

**Exact next action:** create one existing-format bounded Mission admission
packet for `ADMIN_CAPACITY_POOL_WRAPPER_REMOVAL_V1`; do not implement it in
this discovery step.
