# E35.C Implementation Readiness

## Recommended P2 Order

1. Evaluator model.
2. Conflict resolver.
3. Read APIs.
4. Admin visibility.
5. Event model.
6. Runtime hooks.
7. Controlled write paths.

## Classification

| Area | Classification |
|---|---|
| Autoswitch gates | Reuse as inputs |
| Approval packets | Extend with authority/evaluator hashes later |
| Manual switch | Extend with evaluator precheck later |
| Group constraints | Reuse/extend |
| Required services | Reuse as input |
| Capacity/quality | Reuse as input |
| Runtime/Release Trust | Reuse as input |
| Evidence/Proposal | Reuse as links/context |
| Score/speed | Do Not Touch |
| Movement commands | Do Not Touch in evaluator |
| Admin | Extend |
| API | Add read APIs first |

## Build Readiness

E35.C is implementation-ready for a read-only evaluator surface.

Do not start with runtime hooks that can block live movement until:

- read-only evaluator matches expected decisions;
- admin explanations are operator-readable;
- tests prove fail-closed behavior.

## Verdict

```text
implementation_ready=true
e35_d_ready=true
```
