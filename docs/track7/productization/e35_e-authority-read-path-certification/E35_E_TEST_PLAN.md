# E35.E Test Plan

## Consistency Tests

- AUTO consistency;
- PINNED consistency;
- MANUAL consistency;
- Conflict consistency;
- Review consistency;
- Emergency consistency.

## Parity Tests

- Store/API parity;
- Store/Admin parity;
- Store/Evaluator parity;
- Store/Conflict Resolver parity.

## Failure Tests

- store unreadable;
- events unreadable;
- adapter failure;
- API failure;
- evaluator input missing;
- conflict input missing.

## Drift Tests

- store says PINNED, API says AUTO;
- API says AUTO, evaluator says PINNED;
- evaluator and conflict resolver source hash mismatch.

## Safety Tests

- fail-closed behavior;
- no runtime mutation;
- no user movement;
- no routing mutation;
- no autoswitch apply;
- no policy apply;
- no kill switch mutation.

## Verdict

```text
test_plan_defined=true
```
