# E35.A Authority Override Matrix

## Matrix

| Actor / Condition | Can Override AUTOSWITCH | Can Override OPERATOR_PINNED | Can Override MANUAL | Can Override GOVERNANCE DENY | Can Override SAFETY |
|---|---:|---:|---:|---:|---:|
| AUTOSWITCH | n/a | No | No | No | No |
| OPERATOR | Yes | Yes, if same/higher operator permission | Yes | No | No |
| GOVERNANCE | Yes | Review required unless explicit pin override | Review required unless explicit manual override | n/a | No |
| SCHEDULER | No | No | No | No | No |
| CONTAINMENT | Yes | Emergency only | Emergency only | No | No |
| ROLLBACK | Yes | To known safe/previous state only | To known safe/previous state only | If rollback is inside approved/containment scope | No |
| SAFETY | Yes | Yes | Yes | Yes | n/a |

## Rules

### Autoswitch

Autoswitch cannot override human or governance authority.

Autoswitch may move only:

- `routing_mode=AUTO`;
- no hard gate denies;
- apply authority exists;
- execution-time recheck passes.

### Operator

Operator can:

- set pin;
- remove pin;
- set manual mode;
- directly request movement through admin manual switch.

Operator cannot:

- bypass safety;
- bypass kill switch;
- bypass stale runtime trust;
- bypass governance packet denial when using governed path.

### Governance

Governance can authorize bounded movement but must explicitly include:

- user set;
- target set;
- budget;
- rollback;
- pin/manual override reason if touching protected users.

### Containment

Containment can override pins/manual mode only when:

- current target is unsafe;
- required services are hard down;
- channel is quarantined;
- rollback/escape reduces risk;
- action is audited and temporary.

### Scheduler

Scheduler never owns direct override authority. It only runs already admitted work.

## Admin Visibility

Override result must be visible in:

- Users drawer;
- Channels drawer;
- Logs;
- Evidence timeline;
- Proposal drawer when proposal was involved.

## Verdict

```text
override_matrix_defined=true
```
