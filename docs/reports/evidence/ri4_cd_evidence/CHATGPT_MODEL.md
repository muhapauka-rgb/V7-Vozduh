# CHATGPT_MODEL

Schema: `ri4cd.chatgpt-quality-model.v1`

Implemented in: `admin_core/routing_intelligence.py`

## Criteria

| Criterion | Weight |
| --- | ---: |
| availability | 0.22 |
| response_latency | 0.18 |
| stream_start_latency | 0.15 |
| stream_continuity | 0.14 |
| error_rate | 0.12 |
| stability | 0.10 |
| confidence | 0.06 |
| freshness | 0.03 |

## Input Aliases

- `response_latency_ms`, `chatgpt_response_latency_ms`, `latency_ms`
- `stream_start_latency_ms`, `chatgpt_stream_start_latency_ms`, `first_byte_ms`, `latency_ms`
- `stream_continuity`

## Verdict

```text
chatgpt_model_implemented=true
runtime_authority=none
```

