# E35.B Boundary Priority Chain

## Final Constitutional Hierarchy

```text
1. Safety
2. Containment
3. Governance
4. Operator
5. Group
6. User Intent
7. Autoswitch
8. Scheduler
9. Scoring / Speed / Preference
10. Proposal Explanation
```

## Rationale

### 1. Safety

Safety is first because unsafe forward movement must be impossible.

### 2. Containment

Containment comes after Safety because it can act only to reduce active harm. It cannot bypass a kill switch or hard safety block that forbids mutation.

### 3. Governance

Governance defines exact scope, replay safety and execution approval. It prevents broad or stale action.

### 4. Operator

Operator owns explicit human routing intent but cannot defeat Safety/Governance.

### 5. Group

Group defines policy boundaries for classes of users and channels. It constrains Operator by default where regulated, but can be overridden only with explicit review/audit.

### 6. User Intent

User input is not authority. It influences required services/proposals only.

### 7. Autoswitch

Autoswitch acts only inside boundaries created above.

### 8. Scheduler

Scheduler only times work already admitted. It has no movement authority.

### 9. Scoring / Speed / Preference

Scoring is last among decision inputs because it never overrides hard boundaries.

### 10. Proposal Explanation

Proposal explains and recommends. It is not authority.

## Tests

- Safety blocks all forward movement.
- Containment can override pin only with emergency trigger.
- Governance stale packet denies all execution.
- Operator pin beats autoswitch.
- Group hard exclude beats operator unless explicit override.
- Speed never beats boundary.

## Verdict

```text
priority_chain_defined=true
```
