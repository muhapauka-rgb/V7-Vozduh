# P5.1 Freshness Certification

## Freshness Model

Existing freshness checks use:

- `v7-state.json` age threshold: 180 seconds
- `summary.state` age threshold: 180 seconds
- `egress-status.state` age threshold: 420 seconds
- runtime trust TTL: 1800 seconds
- dry-run runtime input TTLs from admin runtime dry-run adapters

## Stale Detection

Existing tools and APIs classify missing or stale state as blocking or review-required:

- `tools/runtime-support/v7-state-stale-check`
- `tools/v7-runtime-contract-validate`
- `admin/v7-admin-api::runtime_fingerprint_response`
- `admin/v7-admin-api::runtime_dry_run_evaluate`
- `admin_core/operator_execution.runtime_recheck`

## Current Certification Result

Freshness was not certified because the required live files are missing locally and authenticated runtime APIs were not used.

## Verdicts

- freshness_certified=false
- freshness_model_identified=true
- stale_state_detection_identified=true
- live_freshness_certified=false
