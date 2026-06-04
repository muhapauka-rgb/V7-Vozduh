# TELEGRAM_MODEL

Schema: `ri4cd.telegram-quality-model.v1`

Implemented in: `admin_core/routing_intelligence.py`

## Criteria

| Criterion | Weight |
| --- | ---: |
| availability | 0.22 |
| message_latency | 0.16 |
| media_latency | 0.12 |
| upload_latency | 0.08 |
| download_latency | 0.08 |
| media_success_rate | 0.10 |
| connection_success | 0.08 |
| error_rate | 0.08 |
| stability | 0.05 |
| freshness | 0.03 |

## Input Aliases

- `message_latency_ms`, `telegram_message_latency_ms`, `latency_ms`
- `media_latency_ms`, `telegram_media_latency_ms`, `latency_ms`
- `upload_latency_ms`, `media_upload_latency_ms`
- `download_latency_ms`, `media_download_latency_ms`
- `media_success_rate`
- `connection_success`

## Calibration Note

The existing `service_matrix.score` remains part of the blended score. This prevents RI4.CD from flattening current probe truth while adding richer criteria.

## Verdict

```text
telegram_model_implemented=true
runtime_authority=none
```

