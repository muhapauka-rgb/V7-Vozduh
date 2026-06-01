# Lifecycle Owner Suitability Matrix

## Legend

- Primary owner candidate: strongest existing component that should become authoritative for this stage.
- Secondary owner candidate: component that should support or expose the stage without taking primary authority.
- Supporting owners: signal/evidence/visibility helpers.
- Legacy owners: historical, dormant, draft, manual, or conflicting ownership to keep contained or retire later.

## Consolidation Matrix

| Lifecycle Stage | Current Owners | Primary Owner Candidate | Secondary Owner Candidate | Supporting Owners | Legacy Owners | Conflict Level | Reuse Recommendation |
|---|---|---|---|---|---|---:|---|
| Signals | service matrix refresh, Telegram sentinel, quality compact, health/speed/client tools | Existing specialized signal writers | `tools/v7-users-autoswitch` as consumer | Admin/observability | None material | MEDIUM | Reuse distributed signal owners; do not centralize signals into a new orchestrator. |
| Health | health/state/speed tooling; `v7-state.json` readers | Existing health/state tooling | Autoswitch consumer | Admin read surfaces, quality compact | Unknown historical scripts | MEDIUM | Keep as signal authority; runtime owner consumes. |
| Service Matrix | `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-telegram-sentinel` | Service matrix refresh/tooling | Telegram sentinel for service-specific updates | Autoswitch/Admin readers | Duplicate ad hoc writers | MEDIUM | Keep refresh owner; make sentinel advisory/service-specific. |
| Capacity | Autoswitch dynamic load summary, registry limits, Admin proposals | Autoswitch for runtime capacity admission | Admin proposal/visibility | Registry/state readers | Historical packet capacity checks | MEDIUM | Reuse autoswitch because it already gates movement. |
| Trust | Admin runtime/release trust read surfaces | Admin trust/read model | Runtime owner consumes trust result if connected later | Operator observability | Historical docs | LOW/MEDIUM | Keep Admin read-only trust surface. |
| Policy | `policy.json`, `org-egress-policy.json` via operator/Admin | Policy files as hard authority | Autoswitch consumer/enforcer | Admin visibility | Manual edits | MEDIUM | Keep policy authority external to runtime owner. |
| Eligibility | Autoswitch decisions and Admin proposal gates | Autoswitch | Admin proposal/gate visibility | Service matrix, policy, capacity, trust | Historical proposal packets | MEDIUM | Reuse autoswitch for live eligibility. |
| Planner | `tools/v7-users-autoswitch` | `tools/v7-users-autoswitch` | Admin dry-run/preview | Signal writers | draft planner unit | LOW/MEDIUM | Reuse; do not add planner. |
| Proposal | Admin generated proposals, historical approval packets | Admin proposal/read model | Operator observability | Evidence bundles | historical markdown packets | MEDIUM | Keep proposal as operator/governance input, not execution owner. |
| Selected Moves | Autoswitch in-process plan; multiple file readers | `tools/v7-users-autoswitch` | Admin selected-move gates/observability | Restore-settle samples | Persistent selected-move evidence files | HIGH | Reuse autoswitch selected moves; avoid duplicate selected-move truth. |
| Restore Barrier | Autoswitch enforcement; fragmented write/closure | `tools/v7-users-autoswitch` for authoritative enforcement/lifecycle suitability | Admin closure/visibility | restore-settle gate, operator observability | manual/historical barrier writes | HIGH | Consolidate around autoswitch later; no new barrier source. |
| Runtime Recheck | Autoswitch checks, operator zero-move recheck, Admin preview gates | `tools/v7-users-autoswitch` for live movement recheck | `admin_core/operator_execution.py` / Admin gates | Admin observability | zero-move-only packet engine as execution owner | HIGH | Extend existing checks; do not create separate admission engine. |
| Execution | Autoswitch apply, Admin autoswitch apply, Admin direct switch, CLI `v7-user-switch` | `tools/v7-users-autoswitch` | Admin as operator surface | `v7-user-switch` primitive | direct Admin/CLI lifecycle authority | HIGH | Keep primitive but route ownership through autoswitch later. |
| Verification | Autoswitch route verification; Admin endpoint final route checks | `tools/v7-users-autoswitch` | Admin observability | Runtime checkers | Historical manual verification scripts | MEDIUM | Reuse autoswitch verification as live authority. |
| Rollback | Autoswitch local rollback, Admin endpoint rollback, `v7-rollback-last-change`, proxy guard rollback | `tools/v7-users-autoswitch` for movement rollback lifecycle | `v7-rollback-last-change` for broad low-level rollback | Admin rollback surface, audit log | raw fallback rollback commands | HIGH | Centralize lifecycle ownership around runtime owner; keep generic rollback as primitive. |
| Audit | `v7-audit-log`, Admin audit wrapper, operator execution audit, event JSONL | `tools/runtime-support/v7-audit-log` | Admin/operator audit surfaces | service event writers, autoswitch JSON/journal | historical report-only audit | HIGH | Use existing audit sink; avoid a second audit truth source. |
| Closure | Admin closure records, operator observability, historical reports; no runtime closer | Admin/operator closure layer | Runtime owner supplies execution outcome; `v7-audit-log` supplies immutable event sink | proposal/evidence closure controls | historical report closeouts | HIGH | Reuse Admin closure model; connect ownership later without new truth source. |

## Stage Suitability Notes

- Autoswitch should own stages that require live movement truth: eligibility, planner, selected moves, restore-barrier enforcement, runtime recheck for movement, execution, verification, and movement rollback.
- Admin should own human/operator surfaces: proposal visibility, dry-run review, execution contract preview, closure controls, audit search, and manual governance view.
- `v7-audit-log` should remain the canonical audit sink candidate because Admin already calls it and runtime-support tools can use it.
- Systemd should remain scheduler-only; it should not own lifecycle state or closure.
- `v7-user-switch` should remain a primitive; independent use is a bypass risk.

