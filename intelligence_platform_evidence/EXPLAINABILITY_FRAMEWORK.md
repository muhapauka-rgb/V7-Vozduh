# EXPLAINABILITY_FRAMEWORK

Implemented in:

- `admin_core/intelligence_platform.py::explainability_framework`
- `admin_core/intelligence_platform.py::explain_score`

## Payloads

- service scores;
- candidate suitability;
- best available pool;
- predictions;
- risk;
- trust.

## Required Fields

- subject;
- score;
- components;
- confidence;
- source;
- authority.

## Snapshot Integration

`service-scores` metadata now includes explainability framework metadata.

## Verdict

```text
explainability_implemented=true
```

