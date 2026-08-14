# INTELLIGENCE_TRUTH_SOURCE_MAP

Implemented in:

- `admin_core/intelligence_platform.py::intelligence_truth_source_map`

## Canonical Truth

| Domain | Single Source | Owner |
| --- | --- | --- |
| service quality | service matrix + quality summary | service probe/quality tools |
| service history | ServiceHistoryStore read model | `admin_core.routing_intelligence` |
| candidate suitability | candidate-suitability-summary snapshot | `intelligence_workers` |
| best available pool | best-available-pool snapshot | `intelligence_workers` |
| prediction | prediction-summaries snapshot | PredictiveFoundation / workers |
| risk | risk-summaries snapshot | `intelligence_workers` |
| trust | trust-summaries snapshot | ExecutionTrustModel / workers |
| explainability | model output payloads | producing model |
| replay | historical snapshots/outcomes | read-only replay framework |
| drift | baseline/current model outputs | read-only drift framework |

## Verdict

```text
one_truth_rule=true
new_truth_sources_created=false
```

