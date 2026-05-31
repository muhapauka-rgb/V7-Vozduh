# E35.A Authority Priority Chain

## Purpose

This chain defines decision order for movement admission.

Authority does not pick the target. It admits or denies a proposed action.

## Final Chain

```text
1. Safety / Kill Switch / Runtime Trust
2. Emergency Containment
3. Governance Packet / Approval Scope
4. Routing Authority Mode
5. Group Hard Constraints
6. Required Services Hard Constraints
7. Channel Suitability
8. Capacity Hard Gates
9. Stability / Quality Floors
10. Soft Preferences
11. Speed / Score
12. Proposal Explanation
13. Execution-Time Recheck
14. Runtime Execution
15. Observation / Rollback
```

## Rationale

### 1. Safety / Kill Switch / Runtime Trust

Nothing can override hard safety blocking for forward movement.

Outcome:

- forward: `DENY`;
- rollback/containment: may be allowed if it reduces risk.

### 2. Emergency Containment

Containment is evaluated early because it may be the only allowed action when normal authority is denied.

Outcome:

- normal forward: blocked;
- emergency escape/rollback: `EMERGENCY_ONLY`.

### 3. Governance Packet / Approval Scope

Governance defines exact approved users, targets, budget and replay protection.

Outcome:

- outside scope: `DENY`;
- stale/replayed: `DENY`;
- valid packet: continue.

### 4. Routing Authority Mode

User intent is checked before group/service/capacity scoring.

Outcome:

- AUTO: continue;
- OPERATOR_PINNED: deny normal movement away from pin;
- MANUAL: deny autonomous movement.

### 5-9. Hard Runtime Constraints

Group constraints, required services, suitability, capacity and stability are hard admission gates.

No soft preference can override these.

### 10-12. Preferences and Explanation

Preferred egress, sticky route, speed and score are soft and only matter after hard gates pass.

Proposal explains; it does not authorize.

### 13. Execution-Time Recheck

The last guard before mutation. It confirms runtime truth has not drifted.

## Operator Meaning

In admin, a user/channel movement should explain:

```text
Denied by Safety
Denied by Authority Mode
Denied by Required Services
Denied by Capacity
Allowed by Authority, pending execution-time recheck
```

## Tests

- speed cannot beat safety;
- speed cannot beat pin;
- proposal cannot beat authority;
- valid authority cannot beat stale packet;
- containment can override pin only when emergency condition exists.

## Verdict

```text
authority_priority_chain_defined=true
```
