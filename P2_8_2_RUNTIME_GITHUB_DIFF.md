# P2.8.2 Runtime GitHub Diff

Project: V7 Vozduh
Block: P2.8.2

## Runtime vs `origin/Updatesystem`

`origin/Updatesystem` is the closest committed GitHub branch.

| Source | Hash | Lines | Routes |
| --- | --- | ---: | ---: |
| Runtime | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | 33800 | 221 |
| `origin/Updatesystem` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | 33057 | 213 |

Diff size from runtime to `origin/Updatesystem`: 20 insertions, 763 deletions.

Runtime-only routes compared to `origin/Updatesystem`:

`/api/execution/contracts`, `/api/execution/contracts/`, `/api/execution/events`, `/api/execution/explain`, `/api/execution/rollback`, `/api/execution/summary`, `/api/execution/timeline`, `/api/execution/verification`.

Runtime-only functions compared to `origin/Updatesystem`:

`safe_execution_id`, `execution_contract_store_rows`, `normalize_execution_contract`, `execution_contracts`, `normalize_execution_event`, `execution_events`, `execution_contract_by_id`, `execution_events_for_contract`, `execution_contract_summary_item`, `execution_store_consistency`, `execution_summary_response`, `execution_contracts_response`, `execution_contract_detail_response`, `execution_timeline_items`, `execution_timeline_response`, `execution_events_response`, `execution_verification_summary`, `execution_verification_response`, `execution_rollback_summary`, `execution_rollback_response`, `execution_explain_response`.

Runtime-only UI compared to `origin/Updatesystem`:

`executionTimelineHtml`, `openExecutionByObject`, `openExecutionContractDrawer`, `openExecutionSummaryDrawer`.

`origin/Updatesystem` has no detected route or execution helper absent from runtime.

## Runtime vs `origin/main`

Runtime is far ahead of `origin/main`.

| Source | Hash | Lines | Routes |
| --- | --- | ---: | ---: |
| Runtime | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | 33800 | 221 |
| `origin/main` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` | 21624 | 165 |

Runtime has many routes and subsystems absent from `main`, including evidence/proposals, runtime/release trust, operator overview/audit/timeline/evidence, and execution read-only APIs.

## Runtime vs Other GitHub Branches

`origin/codex/dynamic-load-autoswitch`, `origin/codex/integratsiya-tunelya`, and `codex/dynamic-load-autoswitch-pr` are all behind runtime and lack the runtime execution read-only API set.

## Classification

The runtime Admin API is not equal to any inspected GitHub branch and was not found in local Git history. Runtime contains a production-only Admin API patch relative to `origin/Updatesystem`.

runtime_github_diff_understood=true
