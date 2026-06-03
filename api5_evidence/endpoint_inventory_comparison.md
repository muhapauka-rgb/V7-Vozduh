# API.5 Endpoint Inventory Comparison

## Files

- Before: `api5_evidence/before_endpoint_inventory.json`
- After: `api5_evidence/after_endpoint_inventory.json`

## Stable Comparison

- summary_equal: true
- stable_endpoint_contracts_equal: true
- endpoint_count_before: 264
- endpoint_count_after: 264
- before_source_line_count: 36034
- after_source_line_count: 35747

## Summary Before and After

- public endpoints: 19
- required-auth endpoints: 245
- action endpoints: 133
- page endpoints: 14
- public_api endpoints: 3
- public_delivery endpoints: 5
- read_api endpoints: 109
- GET: 118
- HEAD: 8
- POST: 138
- critical risk: 13
- high risk: 95
- medium risk: 38
- low risk: 118
- csrf_required_count: 133
- safe_mode_blocked_count: 86

## Interpretation

The full JSON files differ because `generated_at`, source line numbers, and `source_line_count` changed after removing pure helper code from the monolith.

Endpoint surface is unchanged for stable contract fields: method, path, prefix, family, auth, role, csrf_required, risk, safe_mode_behavior, and response_type.
