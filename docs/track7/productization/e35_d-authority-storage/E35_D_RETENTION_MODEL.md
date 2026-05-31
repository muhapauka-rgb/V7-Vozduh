# E35.D Retention Model

## Current Authority State

Retention:

- while user exists;
- removed only by explicit user deletion/archive process;
- final state should remain archived with user audit.

## Event Retention

| Event Type | Active Retention | Archive |
|---|---:|---|
| verdict events | 90 days | compressed/archive |
| conflicts | 180 days | keep unresolved active |
| reviews | 180 days | keep unresolved active |
| emergencies | 180 days | keep unresolved active |
| authority state changes | 365 days | long-term audit archive |

## Cleanup Rules

- never delete unresolved review;
- never delete active emergency;
- never delete latest authority state;
- archive before cleanup;
- cleanup must not affect runtime routing.

## Operator Visibility

Active window visible in admin by default.

Archive available through Logs/advanced view later.

## Tests

- unresolved review survives cleanup;
- active emergency survives cleanup;
- latest state survives cleanup;
- archived events retain hashes/links.

## Verdict

```text
retention_model_defined=true
```
