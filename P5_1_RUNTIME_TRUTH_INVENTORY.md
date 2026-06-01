# P5.1 Runtime Truth Inventory

| Item | Location | Owner | Freshness | Hashability | Accessibility |
| --- | --- | --- | --- | --- | --- |
| Users | `/opt/v7/egress/state/users.registry` | runtime state | not certified | file hash | inaccessible in current environment |
| Egress | `/opt/v7/egress/state/egress.registry` | runtime state | not certified | file hash | inaccessible in current environment |
| Selected Moves | `/opt/v7/egress/state/selected-moves.json`, `selected_moves.json`, `current-selected-moves.json` | autoswitch/runtime state | not certified | canonical selected-list hash | inaccessible in current environment |
| Health | `summary.state`, `egress-status.state`, `v7-state.json` | runtime support tools | not certified | file hash | inaccessible in current environment |
| Capacity | `egress-load.state`, `egress-load-summary.json` | runtime load/capacity tools | not certified | file hash | inaccessible in current environment |
| Trust | `runtime-trust.jsonl`, `trusted-ru-diagnostic.state`, `trusted-ru-decision.state` | runtime trust/diagnostic tools | not certified | file hash/jsonl chain | inaccessible in current environment |
| Candidate State | `proposal-records.jsonl`, candidate-derived stores | candidate workflow | not certified | jsonl/file hash | inaccessible in current environment |
| Execution State | `execution-contracts.json`, `execution-events.jsonl` | execution preview workflow | not certified | file hash/jsonl hash | inaccessible in current environment |
| Audit State | `/opt/v7/audit/audit.jsonl`, `/opt/v7/events/*.jsonl` | audit/events | not certified | jsonl hash/tail hash | inaccessible in current environment |
| Observation State | `v7-state.json`, service matrix, event files | observability/runtime | not certified | file hash | inaccessible in current environment |

## Notes

Temporary files found under `/private/tmp` are not certified runtime truth.

Historical evidence under `docs/track7` is not certified runtime truth.

## Verdicts

- runtime_truth_inventory_complete=true
- all_required_domains_classified=true
- live_accessibility_confirmed=false
