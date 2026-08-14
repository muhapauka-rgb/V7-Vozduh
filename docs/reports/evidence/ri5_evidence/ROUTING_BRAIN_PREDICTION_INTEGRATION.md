# ROUTING_BRAIN_PREDICTION_INTEGRATION

## Integration

Existing `RoutingBrain` remains the advisory surface.

Runtime planner now includes optional:

```text
routing_brain.prediction_advice
```

This comes from `prediction-summaries` and contains:

- availability flag;
- channel forecast count;
- service forecast count;
- risk forecast;
- trust forecast;
- authority flags.

## Forbidden Systems

```text
RoutingBrainV2_created=false
PredictionBrain_created=false
FutureBrain_created=false
AlternativeBrain_created=false
```

## Verdict

```text
routing_brain_extended=true
planner_authority_changed=false
```

