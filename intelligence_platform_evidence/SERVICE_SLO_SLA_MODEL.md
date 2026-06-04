# SERVICE_SLO_SLA_MODEL

Implemented in:

- `admin_core/intelligence_platform.py::service_slo_sla_model`

## Status Thresholds

| Status | Score Min | Confidence Min | User Impact |
| --- | ---: | ---: | --- |
| GOOD | 85 | 0.80 | none |
| WARNING | 70 | 0.65 | minor |
| DEGRADED | 50 | 0.50 | visible |
| BAD | 25 | 0.35 | major |
| CRITICAL | 0 | 0.00 | service_unusable |

## Covered Services

- Telegram
- YouTube
- Instagram
- ChatGPT
- Google
- Google Auth

## Verdict

```text
service_slo_defined=true
runtime_decision_authority=none_contract_only
```

