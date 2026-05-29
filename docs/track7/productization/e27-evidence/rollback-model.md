# E27 Rollback Model

## Rollback Manifest

```text
rollback_user_A=10.7.0.11 -> 1
rollback_user_B=10.7.0.12 -> 1
```

## Route Restoration

Expected rollback route state:

```text
10.7.0.11 table=1009 default dev v7e356a192b79
10.7.0.12 table=1010 default dev v7e356a192b79
```

## Safety Requirements

Two-user rollback is safe only if:

- both users started on `1`;
- both users moved only to the approved execution target;
- no third user moved;
- target users count increased by exactly 2 during forward and returned to 0 after rollback;
- route tables `1009` and `1010` are restored;
- runtime checkers remain OK;
- selected_moves remains 0;
- hidden movers remain absent.

## Verdict

`two_user_rollback_safe=true`

This is a model verdict only. It is not an execution proof. Target capacity remains the blocker for actual movement.

