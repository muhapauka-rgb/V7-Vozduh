# V7 PHYSICAL SYSTEM SHRINK REPORT

Status: `READ_ONLY_PHYSICAL_REALITY_AUDIT_COMPLETE`

Comparison boundary:

- BEFORE: `7ffa4c06bab741f266070e6506987e320e828922` — parent of the first Reset execution commit;
- AFTER: `d8a2fa436123bd176522974f9861a2cfc376bbb2` — `RESET-M10` terminal commit;
- Git range: `7ffa4c06..d8a2fa43`;
- production-state evidence: the bounded M9/M10 snapshots already captured at the Reset terminal boundary.

This report records physical facts only. It does not treat a document disposition, an intended boundary, or exclusion from an active path as file deletion. `NOT PROVEN` means that the two boundaries do not contain equivalent physical inventories from which a numeric delta can be derived.

## 1. Git and file reality

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Tracked files | 8,775 | 8,814 | +39 |
| Text files | 8,480 | 8,519 | +39 |
| Binary files | 295 | 295 | 0 |
| Added files | 0 | 39 | +39 |
| Modified files | 0 | 10 | +10 |
| Deleted files | 0 | 0 | 0 |
| Git-detected moves/renames | 0 | 0 | 0 |

`git diff --shortstat` for the range: `49 files changed, 4529 insertions(+), 1050 deletions(-)`. No `D`, `R`, or `C` record exists in the name-status diff.

### Modified-file disposition

| File | Action | Old purpose | New status |
|---|---|---|---|
| `admin_core/operator_execution.py` | MODIFIED, +191/-0 | Packet/lease/barrier and governed execution utilities | `RUNTIME_EXCLUDED` from primary class-routing apply; retained governed/fallback consumers |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | MODIFIED, +23/-6 | OMP contract | `ENGINEERING_ONLY` |
| `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | MODIFIED, +55/-47 | CPS current-state projection | `ENGINEERING_ONLY`; not a routing writer |
| `docs/reference/SYSTEM_MAP.md` | MODIFIED, +17/-3 | System topology reference | `ENGINEERING_ONLY` |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | MODIFIED, +15/-3 | Canonical durable reference | `ENGINEERING_ONLY` |
| `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | MODIFIED, +329/-977 | Project handoff/history | `ENGINEERING_ONLY`; physically reduced by 648 lines |
| `docs/reports/engineering/2026-07-25_151500_multi_lane_product_evolution_and_channel_hard_failure_engineering.md` | MODIFIED, +5/-1 | Historical engineering evidence | `ENGINEERING_ONLY` |
| `docs/reports/engineering/2026-07-26_184500_service_failure_automatic_successor_reentry.md` | MODIFIED, +24/-2 | Historical engineering evidence | `ENGINEERING_ONLY` |
| `tools/v7-users-autoswitch` | MODIFIED, +474/-2 | Legacy planner and governed user-movement path | `LEGACY_ONLY`; inactive as automatic primary writer, retained as bounded fallback/tooling |
| `tools/v7_sync_lib.py` | MODIFIED, +109/-9 | OMP, truth-check, Polygon and engineering helpers | `ENGINEERING_ONLY` for Reset routing; still has real engineering CLI consumers |

No modified file was physically deleted, moved, or archived.

### Added-file manifest

- Runtime-capable source: `admin_core/routing_core.py` (265 LOC), `tools/runtime-support/v7-routing-sync` (210 LOC).
- Tests: `tests/unit/test_current_action_class_contract_cancellation.py`, `test_reset_cps_frontier_preservation.py`, `test_routing_core.py`, `test_routing_core_certification_adapter.py`, `test_routing_core_primary_promotion.py`, `test_v7_routing_sync_core.py` (412 LOC total).
- Program: `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md` (577 LOC).
- Historical evidence: 30 Engineering Reports, comprising three added July reports, the routing reality verdict, Reset reports `120000` through `350000`, the Master Audit Report, and the Program Completion Report (1,823 LOC total).

The 39-file increase is therefore: 2 runtime-capable files + 6 test files + 1 Program file + 30 report files.

## 2. LOC reality

Counting rule: newline-delimited lines in every tracked non-binary Git blob at each boundary. The functional categories below are reproducible path/name projections and overlap; they must not be summed.

| LOC projection | Before | After | Delta |
|---|---:|---:|---:|
| Total repository LOC | 21,920,827 | 21,924,306 | +3,479 |
| Production-capable surface LOC (`admin/`, `admin_core/`, `tools/`, `systemd/`, tests excluded) | 181,185 | 182,423 | +1,238 |
| Routing-related LOC (routing-name/path projection, reports excluded) | 2,039,157 | 2,041,193 | +2,036 |
| Engineering LOC (`docs/` + `tests/`) | 5,685,547 | 5,687,788 | +2,241 |
| Named legacy surface LOC | 57,487 | 58,250 | +763 |

The repository contains large tracked data/generated text surfaces; therefore the total is an exact repository count, not an estimate of handwritten source.

### LOC delta classification

| Class | Fact |
|---|---|
| PHYSICAL REMOVAL | 1,050 deleted lines inside modified files; zero deleted files |
| ADDED | 4,529 inserted lines; net repository delta +3,479 LOC |
| MOVED | No Git-detected rename/move; 0 files |
| STILL PRESENT BUT NOT PRIMARY RUNTIME | `v7-users-autoswitch`, `v7-user-switch`, `v7_sync_lib.py`, Packet/lease/barrier code and draft planner units remain physically present |
| LOGICAL EXCLUSION | Legacy planner/Packet/lease/barrier are not in the Core-primary apply path, but their files remain and are not counted as removed |

The Reset produced no source-tree shrink in aggregate. Named legacy code grew by 763 LOC.

## 3. Runtime package reality

### Declared package surface in Git

| Unit type | Before | After | Delta |
|---|---:|---:|---:|
| Tracked `.service` units | 7 | 7 | 0 |
| Tracked `.timer` units | 5 | 5 | 0 |
| Tracked service `ExecStart` declarations | 7 | 7 | 0 |

The systemd unit files and their `ExecStart` commands are byte-identical across the comparison range. `v7-routing-sync` was added as an executable but no new systemd unit was added for it.

### Terminal production snapshot

| Classification | Physical fact at terminal evidence boundary |
|---|---|
| ADDED TO RUNTIME | `/usr/local/bin/v7-routing-sync`; Core-primary class-routing apply path |
| STILL ACTIVE | `v7-admin-api.service`; `v7-service-matrix-refresh.timer` active/waiting in the captured allowlisted snapshot |
| DISABLED/INACTIVE | `v7-users-autoswitch.service`; `v7-users-autoswitch.timer` |
| STILL INSTALLED OR CONSUMABLE | `v7-users-autoswitch`, `v7-user-switch`, governed Packet/lease/barrier code, `v7_sync_lib.py` |
| REMOVED FROM RUNTIME | 124 per-user source rules and 124 per-user default route tables; no source file removal |

An equivalent BEFORE process/service snapshot was not preserved at the selected commit boundary. Consequently, a numeric active-process or active-service before/after delta is `NOT PROVEN`; tracked unit counts are the only symmetric package count.

## 4. Dependency graph shrink

### Removed physical runtime edges

- primary routing writer -> 124 per-user source rules;
- primary routing writer -> 124 per-user default-route tables;
- synchronous Core-primary apply -> OMP/report/history/learning artifacts: no such import or startup dependency exists in `admin_core/routing_core.py` or `tools/runtime-support/v7-routing-sync`.

### Retained physical edges

- `v7-users-autoswitch.timer` -> `v7-users-autoswitch.service` remains declared in Git, although the captured units are inactive;
- install/truth/governance tools -> `/usr/local/bin/v7-users-autoswitch` remain;
- `v7-route-movement-preview` -> proposed `v7-user-switch` command remains;
- `v7-release-sync`, `v7-safe-push`, `v7-convergence-status`, and `v7-truth-check` -> `v7_sync_lib.py` remain;
- `v7-operator-execution-packet` and other engineering/quality consumers -> `admin_core/operator_execution.py` remain;
- legacy planner -> governed `v7-user-switch` movement remains physically implementable as a fallback path;
- draft planner and health unit files remain present.

Therefore the primary forwarding graph is smaller, but the legacy and engineering dependency graph was not physically removed.

## 5. Routing surface shrink

| Routing object/process metric | Before | After | Delta |
|---|---:|---:|---:|
| Per-user source rules | 124 | 0 | -124 |
| Per-user default-route tables | 124 | 0 | -124 |
| Class fwmark rules | 0 | 6 | +6 |
| Class route tables | 0 | 6 | +6 |
| Primary individualized/class routing objects | 248 | 12 | -236 (-95.2%) |
| nft membership entries | 124 | 124 | 0 |
| Primary routing writers | legacy primary writer | `v7-routing-sync` | 1 -> 1 |
| Automatic legacy writer units | available | inactive | logical deactivation; files retained |

The measurable physical shrink is in live kernel routing objects, not in repository files. Class membership remains per user in the nft map; it is not counted as removed.

## 6. State surface shrink

No equivalent machine-readable BEFORE and AFTER inventory enumerating every state surface, writer, and reader exists at the two Git boundaries. Exact total counts are therefore `NOT PROVEN`.

| Disposition | Physically evidenced state |
|---|---|
| REMOVED | 124 per-user rule objects; 124 per-user default-route-table objects |
| MERGED | Per-user routing selection collapsed into 6 class fwmark rules and 6 class route tables |
| RETAINED | 124 nft user-to-class membership entries; legacy planner state files/interfaces; CPS and canonical durable-state owners; Packet/lease/barrier artifacts |
| ADDED | Core class-routing plan/apply representation in `routing_core.py` and `v7-routing-sync` |

No claim of a total state-surface, writer, or reader count is made beyond these directly enumerated objects.

## 7. Legacy reality

| Surface | Size before | Size after | Current role | Real consumer | Removal condition |
|---|---:|---:|---|---|---|
| `tools/v7-users-autoswitch` | 23,167 LOC | 23,639 LOC | `LEGACY_ONLY`; inactive automatic planner/writer, bounded fallback and engineering planning | governance/truth tools, intelligence projections, optional manual/fallback execution | remove only after no fallback, governance, preview, installer, or production recovery consumer remains |
| `tools/runtime-support/v7-user-switch` | 135 LOC | 135 LOC | per-user legacy mutation adapter | `v7-route-movement-preview`; legacy governed movement path | remove after all per-user movement and rollback consumers are retired |
| `tools/v7_sync_lib.py` | 25,279 LOC | 25,379 LOC | OMP/truth/Polygon/engineering library; not Core-primary apply | `v7-release-sync`, `v7-safe-push`, `v7-convergence-status`, `v7-truth-check` and test/engineering consumers | shrink/remove only function-by-function after all named CLI/test consumers disappear or move to existing owners |
| Packet/lease/barrier owner (`admin_core/operator_execution.py`) | 8,853 LOC | 9,044 LOC | governed execution/recovery support; excluded from Core-primary synchronous apply | `v7-operator-execution-packet`, `v7-truth-check`, quality/governance consumers | retain while governed rollback/recovery or approved execution consumes it |
| Old planner units (`systemd/drafts/v7-autoswitch-planner.*`) | 30 LOC | 30 LOC | draft declarations, not Core-primary writer | repository governance checks; no proven loaded production unit at terminal snapshot | archive/delete only after governance references are updated and no deployment consumer exists |

Named legacy total: `57,487 -> 58,250 LOC`, delta `+763`. None of these five surfaces was physically removed.

## 8. V7_PHYSICAL_SHRINK_SUMMARY

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Repository LOC | 21,920,827 | 21,924,306 | +3,479 |
| Runtime-capable surface LOC | 181,185 | 182,423 | +1,238 |
| Active services | NOT PROVEN | 2 proven active allowlisted units | NOT PROVEN |
| Tracked service units | 7 | 7 | 0 |
| Timers (tracked / proven active) | 5 / NOT PROVEN | 5 / 1 | tracked 0; active NOT PROVEN |
| Primary routing writers | 1 legacy | 1 Core | 0 count; owner replaced |
| Enumerated per-user/class routing state objects | 248 | 12 | -236 |
| Routing objects including nft membership | 372 | 136 | -236 |
| Active routing processes | NOT PROVEN | bounded command execution; no new daemon unit | NOT PROVEN |
| Primary synchronous dependencies | legacy planner/user mutation chain | Core plan -> `ip`/`nft` apply/verify | legacy chain excluded, retained physically |

## 9. Factual verdict

### What was physically removed

- Zero tracked files.
- Zero Git-detected moves or archives.
- 1,050 lines inside modified files.
- In production routing state: 124 per-user rules and 124 per-user default-route tables.

### What was only excluded

- The legacy autoswitch planner, per-user switch adapter, Packet/lease/barrier path, OMP/report/history/learning surfaces were excluded from the Core-primary synchronous routing path.
- Their source, unit declarations, imports, governance checks, installers, and fallback consumers remain where enumerated above.

### What remains

- All named legacy files remain; their combined size increased by 763 LOC.
- The repository grew by 39 files and 3,479 LOC.
- Seven service and five timer declarations remain unchanged.
- The 124-entry nft membership map remains.
- Engineering and historical evidence added 31 Program/report documents and six tests; none participates in Core-primary apply.

### Next physical shrink candidates

Candidate status is based only on current consumer evidence:

1. `systemd/drafts/v7-autoswitch-planner.service` and `.timer`: smallest retained surface; deletion requires clearing governance references and proving no deploy consumer.
2. Inactive `v7-users-autoswitch` service/timer/install path: removable only after fallback/recovery use is explicitly retired.
3. `v7-user-switch`: removable after the preview and legacy rollback/movement consumers disappear.
4. Function-level reduction of `v7_sync_lib.py` and `v7-users-autoswitch`: whole-file deletion is not currently supported because real consumers remain.

No deletion is authorized or performed by this audit.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`
