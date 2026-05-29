# E32.1.3 Demotion Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

demotion_model_defined=true

## Demotion Types

### CERTIFIED To STALE

Causes:

- validation TTL exceeded;
- capacity evidence is old but no active safety failure exists;
- target metadata changed in a way that requires refresh but does not prove failure;
- policy cap changed and requires re-evaluation.

Result:

- historical certification remains;
- forward approval denied until refresh;
- rollback remains allowed.

### CERTIFIED To DEGRADED

Causes:

- readiness NO-GO;
- quality below floor;
- repeated target-local probe failure;
- runtime checker failure;
- restore-settle failure;
- selected moves nonzero outside approved windows;
- hidden movers detected;
- target isolation failure;
- autoswitch or rebalance exclusion failure.

Result:

- forward approval denied;
- remediation or rollback allowed;
- recertification required before returning to CERTIFIED.

### CERTIFIED To EXPIRED

Causes:

- hard expiration threshold exceeded;
- target profile/interface replacement;
- NAT/MSS/provisioning model changed materially;
- evidence cannot be located or verified;
- class schema version incompatible.

Result:

- active certification unusable;
- full validation required.

### CERTIFIED To REVOKED

Causes:

- rollback failure that is not contained;
- replay protection failure;
- audit chain contradiction;
- unauthorized user movement;
- blast radius violation;
- evidence falsification or unresolvable evidence corruption;
- governance bypass discovered.

Result:

- target certification removed;
- target must restart certification from UNCERTIFIED or CANDIDATE after investigation;
- production-pool eligibility denied.

## Demotion Severity

| Trigger | Default Demotion |
| --- | --- |
| TTL exceeded | STALE |
| Readiness NO-GO | DEGRADED |
| Quality floor drop | DEGRADED |
| Runtime checker failure | DEGRADED |
| Missing evidence file | EXPIRED |
| Schema incompatible | EXPIRED |
| Replay accepted | REVOKED |
| Unauthorized movement | REVOKED |
| Rollback failure | REVOKED unless fully contained and reviewed |

## Safety Rule

Demotion can be automatic. Promotion cannot be automatic without accepted evidence and authority.

