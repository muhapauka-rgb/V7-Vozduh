# API.2 Endpoint Inventory Comparison

## Commands

```bash
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/reports/evidence/api2_evidence/before_endpoint_inventory.json
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/reports/evidence/api2_evidence/after_endpoint_inventory.json
```

## Summary

- before endpoint count: `264`
- after endpoint count: `264`
- summary unchanged: `true`
- stable endpoint definitions unchanged: `true`

## Stable Summary

```json
{
  "by_auth": {"public": 19, "required": 245},
  "by_family": {"action": 133, "page": 14, "public_api": 3, "public_delivery": 5, "read_api": 109},
  "by_method": {"GET": 118, "HEAD": 8, "POST": 138},
  "by_risk": {"critical": 13, "high": 95, "low": 118, "medium": 38},
  "csrf_required_count": 133,
  "endpoint_count": 264,
  "safe_mode_blocked_count": 86
}
```

## Expected Metadata Drift

- `source_line_count`: `36468` -> `36459`
- Endpoint line metadata shifted because code was extracted from `admin/v7-admin-api`.

This drift is expected and does not represent endpoint behavior change. Stable endpoint definitions, excluding source line metadata, remained unchanged.
