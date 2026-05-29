# E32.1.3 Recertification Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

recertification_model_defined=true

## STALE To CERTIFIED

Required:

- fresh readiness GO;
- fresh restore-settle GO;
- runtime checkers OK;
- selected moves zero;
- hidden movers absent;
- target users count matches assumptions;
- class-appropriate refresh window;
- evidence pointers updated.

If all pass:

- preserve capacity class;
- update validation time, stale threshold, expiration threshold;
- keep confidence if evidence quality matches prior class.

## DEGRADED To CERTIFIED

Required:

- classify degradation root cause;
- remediate safely;
- rerun class-appropriate readiness and validation;
- prove runtime checkers OK;
- prove restore-settle GO;
- if degradation occurred during movement, prove rollback/audit chain integrity;
- final safety review.

If degradation was severe:

- return to lower certified class first;
- require promotion again for higher class.

## EXPIRED To CERTIFIED

Required:

- full validation evidence for the desired class;
- evidence schema compatibility check;
- long-window validation;
- approval packet proof if class movement proof is required;
- audit/replay/rollback evidence refreshed or reaccepted.

Expired certification may not be restored by timestamp update alone.

## REVOKED To CERTIFIED

Required:

- governance incident review;
- root-cause fix;
- evidence chain rebuild;
- target may re-enter as CANDIDATE only;
- full certification path required.

## Fail-Closed Behavior

During RECERTIFYING:

```text
forward_execution_allowed=false
current_capacity=0 for the target class being recertified
rollback_allowed=true
```

If a lower class remains unrelated and fresh, a policy decision is required before using it. Default safe behavior is to suspend forward execution until recertification completes.

