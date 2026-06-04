# REPLAY_FRAMEWORK

Implemented in:

- `admin_core/intelligence_platform.py::replay_framework`

## Question

If current models had existed during historical periods, what would have happened?

## Measures

- agreement;
- disagreement;
- false positives;
- false negatives.

## Scope

Replay is read-only and uses historical predictions/outcomes. It does not mutate runtime state and does not create selected moves.

## Verdict

```text
replay_framework_implemented=true
runtime_replay=false
```

