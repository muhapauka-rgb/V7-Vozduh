# SERVICE_EVALUATION_FRAMEWORK

Schema: `ri4cd.service-quality-framework.v1`

Owner: `ServiceIntelligenceEngine`

Authority: advisory-only read model; no runtime mutation, no planner authority, no governance authority, no execution authority.

## Canonical Meaning

"Service works well" means that a channel can deliver the user-visible service with acceptable availability, latency, throughput, stability, error rate, confidence, and freshness for the relevant service type.

## Canonical Criteria

| Criterion | Meaning |
| --- | --- |
| availability | Service endpoint or functional probe is reachable. |
| latency | User-visible delay is inside service-specific thresholds. |
| throughput | Data flow supports expected service workload. |
| stability | Results remain steady across history windows. |
| error rate | Failures, timeouts, or probe errors remain low. |
| user experience impact | Service-specific quality signals such as stream continuity or media load. |
| confidence | Input completeness and probe confidence. |
| freshness | Source data is recent enough to trust as advisory input. |

## Supported Primary Models

- Telegram: message/media/upload/download latency, media success, connection success.
- YouTube: startup delay, chunk throughput, buffer probability, playback stability, 1080p/4k viability.
- Instagram: feed/story/video/media load, reliability, error rate, stability.
- ChatGPT: response latency, stream start latency, stream continuity, error rate, stability.

## Fallback

Unknown services use the generic service quality model:

- availability;
- latency;
- throughput;
- error rate;
- stability;
- confidence;
- freshness.

## Non-Authority

```text
runtime_decision_authority=none_shadow_only
planner_owner=tools/v7-users-autoswitch
governance_authority=unchanged
execution_authority=none
```

