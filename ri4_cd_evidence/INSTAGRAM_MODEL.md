# INSTAGRAM_MODEL

Schema: `ri4cd.instagram-quality-model.v1`

Implemented in: `admin_core/routing_intelligence.py`

## Criteria

| Criterion | Weight |
| --- | ---: |
| availability | 0.20 |
| feed_load | 0.15 |
| story_load | 0.13 |
| video_load | 0.13 |
| media_load | 0.10 |
| reliability | 0.10 |
| error_rate | 0.09 |
| stability | 0.07 |
| freshness | 0.03 |

## Input Aliases

- `feed_load_ms`, `instagram_feed_load_ms`, `latency_ms`
- `story_load_ms`, `instagram_story_load_ms`, `latency_ms`
- `video_load_ms`, `instagram_video_load_ms`, `latency_ms`
- `media_load_ms`, `instagram_media_load_ms`, `latency_ms`
- `reliability`

## Verdict

```text
instagram_model_implemented=true
runtime_authority=none
```

