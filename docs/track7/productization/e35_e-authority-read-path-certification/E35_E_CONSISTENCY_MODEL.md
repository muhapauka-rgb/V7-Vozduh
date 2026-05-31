# E35.E Consistency Model

## Certified Consistency Subjects

These values must appear identically across Store, API, Admin, Evaluator and Conflict Resolver:

- `routing_mode`;
- `authority_owner`;
- `authority_status`;
- `preferred_egress`;
- pin state;
- manual state;
- containment state;
- conflict state;
- review state;
- emergency state;
- group restrictions summary;
- required services summary.

## Required Guarantees

| Scenario | Required Consistency |
|---|---|
| AUTO user | all layers show AUTO and no pin/manual lock |
| PINNED user | all layers show OPERATOR_PINNED and same target |
| MANUAL user | all layers show MANUAL and same owner/reason |
| Conflict | API/Admin/Evaluator/Resolver use same conflict id/type |
| Review | API/Admin/Evaluator show same review requirement |
| Emergency | all layers show same emergency id, trigger and expiry |

## Validation

Every derived object must include:

- `source_hash`;
- `generated_at`;
- `authority_state_version`;
- `event_cursor` or event high-watermark.

## Verdict

```text
consistency_model_defined=true
```
