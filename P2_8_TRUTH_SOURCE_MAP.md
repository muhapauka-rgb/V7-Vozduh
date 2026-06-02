# P2.8 Truth Source Map

| Domain | Canonical Truth Source | Derived Sources | Dangerous Duplicates |
| --- | --- | --- | --- |
| Authority | `STATE_DIR/routing-authority.json` when present; otherwise authority previews remain non-authoritative | authority read models, admin drawers | stale docs claiming authority without runtime state |
| Candidate | P2.6 derived candidate model from proposals and preview drafts | candidate approval/governance/rehearsal bridge | persisted duplicate candidate queue |
| Execution | `STATE_DIR/execution-contracts.json` and `STATE_DIR/execution-events.jsonl` for stored contracts/events; previews for non-executable stages | execution summary/readiness/outcome APIs | execution docs that imply runtime engine exists |
| Proposal | `STATE_DIR/proposal-records.jsonl` | proposal APIs and candidate derivation | copied proposal reports outside store |
| Evidence | `STATE_DIR/evidence-bundles.jsonl` and evidence files under docs | evidence API, lineage archive | duplicate evidence bundles without shared id |
| Runtime Trust | `STATE_DIR/runtime-trust.jsonl` plus live runtime files | runtime convergence/fingerprint/drift APIs | stale truth snapshots treated as current |
| Release Trust | `STATE_DIR/release-trust.jsonl`, Git HEAD, deploy manifest | release current/history APIs | docs without Git/runtime hash |
| Users | `/opt/v7/egress/state/users.registry` in production | admin overview, state JSON, route checks | local fixture registries |
| Channels | `/opt/v7/egress/state/egress.registry` in production | admin egress views, capacity/readiness previews | stale backup registries |
| Routing | live route tables plus users registry and policy | route reality/readiness previews | docs or dry-run output used as live routing truth |
| Events | `/opt/v7/events/*` and execution event stores | normalized events API | copied event excerpts |
| Audit | `/opt/v7/audit/audit.jsonl` and operator execution audit files | security audit, operator audit search | report excerpts as audit authority |
| Readiness | validation adapters over runtime files | readiness APIs and forecast | manual status labels |
| Simulation | P2.5 derived outcome/impact previews | candidate rehearsal bridge | any executable dry-run packet store |

truth_source_map_complete=true
