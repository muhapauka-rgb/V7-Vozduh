# E35.B Test Plan

## Boundary Tests

- Operator pin respected.
- Group restriction respected.
- Autoswitch blocked by pin.
- Autoswitch blocked by group.
- Autoswitch blocked by required services.
- Autoswitch blocked by safety.
- Containment override allowed for emergency.
- Containment override denied for speed-only improvement.
- Safety override allowed for forward denial.
- Governance denial respected.
- Manual mode respected.
- Scheduler cannot override operator.

## Conflict Tests

- Group AUTO vs Operator MANUAL deterministic.
- Group allows A vs Operator pins B deterministic.
- Operator pin vs Required Services deterministic.
- Operator pin vs Safety deterministic.
- Containment vs Manual deterministic.
- Proposal vs Authority deterministic.

## Admin Tests

- User drawer shows authority chain.
- User drawer shows movement allowed/blocked reason.
- Channel drawer shows group boundary.
- Home shows conflict counts.
- Logs show boundary violation and override events.

## Audit Tests

- Every override is audited.
- Every containment action has trigger and expiry.
- Every denied movement has reason.
- Audit chain remains append-only.

## Safety Scans

- no runtime mutation in boundary read APIs;
- no `v7-user-switch` in read/preview paths;
- no autoswitch apply;
- no routing sync;
- no policy apply;
- no kill switch mutation.

## Verdict

```text
test_plan_defined=true
```
