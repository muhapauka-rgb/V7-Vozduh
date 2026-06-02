# P2.3 Validation Integration

## Result

validation_integrated=true

## Change

`execution_validation_preview_for_draft` now consumes the read-only adapter layer instead of returning static placeholder checks for core runtime gates.

## Runtime mapping

Product Capability:
Operator can see whether a proposal-derived execution draft is ready, review-required, or fail-closed.

Admin Surface:
Execution readiness card and drawer in current V7 Admin.

Runtime Service:
`admin/v7-admin-api` preview layer.

Storage:
Read-only state files and existing JSON/JSONL stores.

API:
`/api/execution/validation-preview`, `/api/execution/gates`, `/api/execution/readiness`.

UI Component:
Gate health table and gate detail drawer.

## Behavior

UNKNOWN is no longer used for gates with readable state. Missing or incomplete but inspectable state becomes REVIEW_REQUIRED. Unsafe state becomes FAIL. Clean state becomes PASS.
