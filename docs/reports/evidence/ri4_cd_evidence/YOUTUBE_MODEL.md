# YOUTUBE_MODEL

Schema: `ri4cd.youtube-quality-model.v1`

Implemented in: `admin_core/routing_intelligence.py`

## Criteria

| Criterion | Weight |
| --- | ---: |
| availability | 0.18 |
| startup_delay | 0.15 |
| chunk_throughput | 0.18 |
| buffer_probability | 0.12 |
| playback_stability | 0.12 |
| 1080p_viability | 0.10 |
| 4k_viability | 0.05 |
| error_rate | 0.07 |
| freshness | 0.03 |

## Input Aliases

- `startup_delay_ms`, `youtube_startup_delay_ms`, `first_byte_ms`, `latency_ms`
- `throughput_mbps`, `avg_mbps`, `mbps`
- `buffer_probability`, `rebuffer_probability`, `buffer_rate`
- `playback_stability`

## Verdict

```text
youtube_model_implemented=true
runtime_authority=none
```

