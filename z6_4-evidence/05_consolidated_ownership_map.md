# Consolidated Ownership Map

| Lifecycle Stage | Primary Owner | Secondary Owner | Supporting Owners | Legacy Owners | Truth Source | Authority Source | Closure Source | Conflict Level | Migration Difficulty |
|---|---|---|---|---|---|---|---|---:|---:|
| Signals | Specialized signal writers | Admin/observability | service matrix, sentinel, quality, health/speed tools | historical captures | signal JSON/event JSONL | signal tool ownership | Admin/operator evidence closure | MEDIUM | LOW |
| Health | health/state tooling | Autoswitch consumer | quality/speed/client tooling | unknown scripts | `v7-state.json` and speed state | health tool ownership | Admin/operator evidence closure | MEDIUM | MEDIUM |
| Capacity | `tools/v7-users-autoswitch` | Admin proposal surface | registries, load summary | packet checks | runtime plan/load summary | runtime owner | Admin/operator closure | MEDIUM | MEDIUM |
| Trust | Admin trust/read model | Autoswitch consumer | release/runtime evidence | historical trust docs | Admin trust surfaces | operator/governance read model | Admin closure | LOW/MEDIUM | MEDIUM |
| Policy | policy/org policy files | Admin policy surface | operator controls | manual edits | policy files | policy authority | Admin closure/evidence | MEDIUM | LOW/MEDIUM |
| Eligibility | `tools/v7-users-autoswitch` | Admin gates | signals/policy/capacity/trust | historical proposals | autoswitch plan | runtime owner | Admin closure | MEDIUM | MEDIUM |
| Planner | `tools/v7-users-autoswitch` | Admin dry-run | signal writers | draft planner | autoswitch plan JSON | runtime owner | Admin/operator timeline | LOW/MEDIUM | LOW |
| Selected Moves | `tools/v7-users-autoswitch` | Admin visibility/gates | restore-settle samples | selected-move files | in-process autoswitch plan | runtime owner | Admin/operator timeline | HIGH | MEDIUM/HIGH |
| Restore Barrier | `tools/v7-users-autoswitch` | Admin closure/visibility | restore-settle gate | manual barrier writes | barrier file interpreted by runtime owner | runtime owner | Admin closure + audit | HIGH | HIGH |
| Runtime Recheck | `tools/v7-users-autoswitch` | Admin/operator evidence | operator_execution, Admin gates | zero-move-only engine as executor | runtime owner result | runtime owner | Admin closure | HIGH | HIGH |
| Execution | `tools/v7-users-autoswitch` | Admin controlled surface | `v7-user-switch` primitive | direct CLI/manual authority | runtime owner outcome | runtime owner | Admin closure + audit | HIGH | HIGH |
| Verification | `tools/v7-users-autoswitch` | Admin/operator views | runtime checkers | manual reports | runtime verify result | runtime owner | Admin closure + audit | MEDIUM | MEDIUM |
| Rollback | `tools/v7-users-autoswitch` for movement lifecycle | `v7-rollback-last-change` primitive | Admin rollback surface, proxy guard | raw fallback commands | runtime rollback result / generic rollback result | runtime owner / primitive | Admin closure + audit | HIGH | HIGH |
| Audit | `v7-audit-log` | Admin audit wrapper | service event writers, operator export | markdown reports | audit JSONL | audit sink owner | Admin closure references audit | HIGH | MEDIUM |
| Closure | Admin closure + operator observability | autoswitch outcome + audit log | evidence/proposal closure controls | report closeouts | closure records | closure owner | Admin closure records | HIGH | HIGH |

## Conflict Reduction Target

The target model reduces conflict by assigning exactly one primary owner per lifecycle stage while keeping existing supporting components in their natural roles.

No new truth source is required.

