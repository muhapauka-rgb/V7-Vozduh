# E34.A Drift Detection Model

drift_detection_defined=true

## Drift Types

| Drift Type | Meaning | Detection |
| --- | --- | --- |
| runtime_drift | Running code or service inventory differs from release object. | Runtime fingerprint mismatch. |
| config_drift | Runtime configuration differs from expected release/config manifest. | Config fingerprint mismatch. |
| release_drift | Runtime reports release different from intended deployment. | Runtime version/lineage mismatch. |
| state_drift | Runtime mutable state violates expected schema or governance invariants. | State fingerprint/schema/runtime checker mismatch. |
| lineage_drift | Deployment history cannot link runtime to release. | Missing deployment id or invalid lineage chain. |

## Severity

| Severity | Meaning | Commercial Impact |
| --- | --- | --- |
| INFO | Expected dev/staging drift or uncommitted docs. | Visible, not production-certified. |
| WARN | Non-critical config mismatch, stale lineage, or missing optional evidence. | Requires review before promotion. |
| BLOCKING | Runtime code/config cannot be proven or safety-critical mismatch exists. | Deny production deployment/execution. |
| CRITICAL | Runtime contradicts certified governance boundary or safety controls. | Containment and operator escalation. |

## Operator Visibility

Each drift finding must show:

```text
drift_id
drift_type
severity
expected
observed
affected_artifacts
first_seen
last_seen
recommended_action
```

## Fail-Closed Behavior

- BLOCKING or CRITICAL drift denies production promotion.
- Unknown runtime fingerprint is BLOCKING for commercial deployment.
- Unknown config fingerprint is BLOCKING if config affects governance, routing, policy, capacity, locks, scheduling, or execution.
- Rollback remains allowed as containment when drift is discovered in production.

drift_detection_defined=true
