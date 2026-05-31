# P3.C Truth Source Audit

Project: V7 Vozduh
Block: P3.C First Runtime Dry-Run

## Rule

P3.C may create a derived report only. No new truth source is allowed.

## Truth Source Matrix

| Dry-run area | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Runtime evidence | `STATE_DIR/v7-state.json`, `users.registry`, `egress.registry` | `runtime_dry_run_input_adapters()` | `/api/runtime/dry-run/summary` |
| Health | `SERVICE_MATRIX_FILE` | `service_matrix_state()` and status counts | Runtime Dry-Run drawer |
| Capacity | `STATE_DIR/egress-load-summary.json` | Input ref/freshness | Runtime Dry-Run drawer |
| Required services | Service matrix | Service matrix status counts | Runtime Dry-Run drawer |
| Runtime trust | `TRUSTED_RU_DECISION_FILE`, runtime trust store | `trusted_ru_decision_state()` | Runtime Dry-Run drawer |
| Release trust | Release trust store | Input ref/freshness | Runtime Dry-Run drawer |
| Candidate | Proposal store plus execution candidate model | `execution_candidates_from_query()` | Operator preview and dry-run report |
| Execution preview | `EXECUTION_CONTRACTS_FILE`, `EXECUTION_EVENTS_FILE` | `execution_contracts()`, `execution_events()`, consistency check | Dry-run report |
| Simulation | Existing execution preview helpers | Referenced as existing preview family | Runtime Dry-Run drawer |
| Verification | `EXECUTION_EVENTS_FILE` and future observed runtime events | Verification plan only | Dry-run report |
| Rollback | Existing execution contract rollback preview | Rollback simulation only | Dry-run report |

## Output Ownership

The dry-run report includes source refs, hashes, freshness and evidence. It is `derived_on_demand` and has no write path.

## Truth Verdict

`truth_source_audit_complete=true`

